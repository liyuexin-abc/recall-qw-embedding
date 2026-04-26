"""
元数据处理 Pipeline：
  1. 从 raw_meta.json 读取原始元数据
  2. 推断 表↔指标 / 表↔维度 关系（基于 column_name 与 metric_code/dimension_code）
  3. 业务规则补全：
     - 指标/维度别名（synonyms）
     - 表 display_name + description 完善
     - 维度的 sample_values 来自 possible_values
     - 维度值（dim_values）由 dimension.possible_values 展开
  4. 自动派生业务主题（基于表和指标的领域聚类）
  5. 派生指标（来自 business_context）+ 依赖关系（指向相关指标/维度/维度值/表）
  6. 生成 embedding_text，编码并落库
"""
import json
import re
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from app import config
from app.core.database import get_db
from app.core.embedding import get_embedding_client
from app.core.text_builder import EmbeddingTextBuilder
from app.utils.logger import get_logger

logger = get_logger("meta_processor", "meta_processor.log")


# ------------------------------------------------------------------
# 业务知识 —— 各表的 display_name / description / 业务主题等增强（基于电力行业领域知识手动补充）
# ------------------------------------------------------------------
TABLE_ENHANCEMENT = {
    "new_power_gen_rec": {
        "display_name": "发受电量",
        "description": "新能源/常规电源的发电量与受电量记录表，记录各地区按调度口径（统调/中调）的水电、火电、核电、风电、太阳能、生物质、抽水蓄能等各类电源发电量及发受电合计。是电源结构分析、电量平衡的核心表。",
        "business_topics": ["发电量统计", "电源结构", "电量平衡"],
        "typical_questions": [
            "广东去年水电发电量是多少",
            "今年各类型新能源发电量分别是多少",
            "全网统调火电发电量",
            "1月份风电发电量",
            "今天总发电量",
        ],
    },
    "new_energy_daily_status": {
        "display_name": "新能源运行情况",
        "description": "新能源电站日运行情况表，记录各电站每日的最大出力、平均出力、装机容量、利用小时数、控制电量、可发未发电量等关键运行指标。",
        "business_topics": ["新能源运行", "电站运行指标"],
        "typical_questions": [
            "广东-阳江海上风电场最大出力",
            "新能源平均出力",
            "电站装机容量",
            "可发未发电量",
            "新能源利用率",
        ],
    },
    "new_realTime_measurement": {
        "display_name": "实时量测",
        "description": "电厂/电站设备实时遥测数据表，记录有功功率、无功功率、电压、电流、频率等电气量的实时测量值。",
        "business_topics": ["实时量测", "电气运行参数"],
        "typical_questions": [
            "白鹤滩电厂电压",
            "电厂实时出力",
            "电厂频率",
            "无功功率",
            "测点数据",
        ],
    },
    "new_energy_info_fill": {
        "display_name": "新能源信息填报",
        "description": "新能源装机/发电填报表，按地区、发电类型聚合的发电量、装机容量、计划/实际发受电量等。",
        "business_topics": ["新能源装机", "发电填报"],
        "typical_questions": [
            "广东风电装机容量",
            "新能源发电量",
            "实际发电量",
            "计划电量",
            "最大持续出力",
        ],
    },
    "power_transfer_receive": {
        "display_name": "送受电量",
        "description": "省间/区域间送受电量表，记录送出方-受入方的电量、电力、计划与实际值等。",
        "business_topics": ["送受电", "省间联络"],
        "typical_questions": [
            "广西受海南电量",
            "广东送贵州",
            "省间送受电",
            "实际送电量",
            "计划受电量",
        ],
    },
    "load_and_reserve": {
        "display_name": "负荷与备用",
        "description": "电网负荷与备用容量表，按地调/统调/中调三种调度口径分别记录最高/最低负荷、平均负荷、负荷率、峰谷差、备用容量等。",
        "business_topics": ["负荷指标", "备用容量", "调度口径"],
        "typical_questions": [
            "广东最高负荷",
            "地调负荷率",
            "峰谷差",
            "统调最高负荷时间",
            "中调备用容量",
        ],
    },
    "power_grid_section": {
        "display_name": "断面表",
        "description": "电网关键断面（如高肇直流、滇黔联络线、广东-澳门联络线等）的功率/负载率/越限状态实时记录。",
        "business_topics": ["断面监视", "联络线", "越限告警"],
        "typical_questions": [
            "高肇直流断面功率",
            "断面越限",
            "联络线负载率",
            "断面控制值",
            "断面正向/反向极限",
        ],
    },
    "trip_info": {
        "display_name": "跳闸情况",
        "description": "电网跳闸/停电故障记录表，记录线路名称、电压等级、停电类型（跳闸/重合成功/主动停运）、故障类型、停电时间、复电时间、故障所属维护单位等。",
        "business_topics": ["跳闸故障", "停电统计"],
        "typical_questions": [
            "今天跳闸次数",
            "跳闸重合成功",
            "线路停电时长",
            "故障原因",
            "佛山地调跳闸",
        ],
    },
}


# 针对维度的 display_name（更口语化，方便用户匹配）
DIM_DISPLAY_NAME_MAP = {
    "ptdate": "日期",
    "month": "月份",
    "quarter": "季度",
    "weekofyear": "自然周",
    "year": "年度",
    "object_id": "对象编号",
    "id": "自增主键",
    "name": "名称",
    "control_reason": "新能源控制原因",
    "point_name": "测点名",
    "region_name": "地区",
    "point_id": "测点ID",
    "gen_type": "发电类型",
    "power_flow_direction": "送受电方向",
    "record_no": "记录号",
    "dispatch_org": "调管机构",
    "city_belong": "市级区域",
    "substation": "变电站",
    "power_outage_type": "停电类型",
    "fault_maintain_unit": "故障所属维护单位",
    "line_code": "线路编码",
    "line_name": "线路名称",
    "fault_phase": "故障相别",
    "fault_type": "故障类型",
    "recloser_action": "重合闸动作情况",
    "county_district": "所属县区",
    "outage_reason": "停电原因",
    "power_delivery_status": "送电情况",
    "power_restore_status": "用电恢复情况",
    "recorder": "记录人",
    "record_time": "记录时间",
    "object_timestamp": "对象时标",
    "section_name": "断面名",
    "limit_status": "越限状态",
    "busbar": "所属母线",
    "min_time_local": "最低时间_地调",
    "max_time_local": "最高时间_地调",
    "min_time_unified": "最低时间_统调",
    "max_time_unified": "最高时间_统调",
    "min_time_central": "最低时间_中调",
    "max_time_central": "最高时间_中调",
    "voltage_level": "电压等级",
    "outage_time": "停电时间",
    "restore_time": "复电时间",
}

# 维度的别名（业务术语别名，强化向量召回）
DIM_SYNONYMS = {
    "region_name": ["地区名", "省份", "省", "区域"],
    "name": ["电站名", "电站名称", "风电场", "光伏电站", "新能源电站"],
    "point_name": ["测点", "电厂测点", "遥测点"],
    "gen_type": ["电源类型", "发电类别", "新能源类型"],
    "power_flow_direction": ["送受电关系", "省间联络方向", "送电方向", "受电方向"],
    "dispatch_org": ["调度机构", "省调", "地调", "中调", "调度单位"],
    "section_name": ["断面", "联络线", "电网断面"],
    "power_outage_type": ["停电类别", "故障类型", "跳闸类型"],
    "fault_maintain_unit": ["维护单位", "维护班组", "供电局"],
    "line_name": ["线路", "输电线路"],
    "ptdate": ["日期", "时间", "天"],
    "city_belong": ["所属地市", "城市"],
    "voltage_level": ["电压等级", "kV"],
}

# 部分指标的别名（提升用户问法的命中率）
METRIC_SYNONYMS_PATTERN = [
    # (匹配 metric_name 的子串, 需要追加的别名)
    ("水电", ["水力发电"]),
    ("火电", ["燃气发电", "火力发电"]),
    ("风力", ["风电", "风能发电"]),
    ("太阳能", ["光伏发电", "光伏"]),
    ("核电", ["核能发电"]),
    ("生物质", ["生物质发电"]),
    ("发电量", ["电量", "发电"]),
    ("最高负荷", ["最大负荷", "用电高峰"]),
    ("最低负荷", ["最小负荷", "用电低谷"]),
    ("峰谷差", ["最大-最小负荷差", "负荷波动"]),
    ("负荷率", ["负荷率指标", "负荷曲线平坦度"]),
    ("装机容量", ["装机", "总装机"]),
    ("最大出力", ["顶峰出力", "高峰出力"]),
    ("最小出力", ["低谷出力"]),
    ("利用小时", ["利用小时数", "等效利用小时"]),
    ("受电", ["受入电量"]),
    ("送电", ["送出电量"]),
    ("还原", ["还原口径"]),
]


def infer_metric_synonyms(metric_name: str) -> List[str]:
    syns = []
    for pat, extra in METRIC_SYNONYMS_PATTERN:
        if pat in metric_name:
            syns.extend(extra)
    return list(set(syns))


# 单位推断
UNIT_INFERENCE_RULES = [
    ("出力",        "MW"),
    ("最高负荷",    "MW"),
    ("最低负荷",    "MW"),
    ("平均负荷",    "MW"),
    ("装机容量",    "MW"),
    ("峰谷差",      "MW"),
    ("发电量",      "MWh"),
    ("受电量",      "MWh"),
    ("送电量",      "MWh"),
    ("电量",        "MWh"),
    ("发受电量",    "MWh"),
    ("控制电量",    "MWh"),
    ("可发未发",    "MWh"),
    ("利用小时",    "h"),
    ("时间",        ""),  # min_time/max_time 不带单位
    ("电压",        "kV"),
    ("电流",        "A"),
    ("频率",        "Hz"),
    ("功率",        "MW"),
    ("负荷率",      "%"),
    ("利用率",      "%"),
    ("占比",        "%"),
    ("次数",        "次"),
    ("时长",        "min"),
]


def infer_unit(metric_name: str) -> str:
    for kw, unit in UNIT_INFERENCE_RULES:
        if kw in metric_name:
            return unit
    return ""


# ------------------------------------------------------------------
# 业务主题（自动派生）
# ------------------------------------------------------------------
TOPIC_DEFINITIONS = [
    {
        "topic_name": "发电量统计",
        "description": "电源发电量、受电量、发受电合计、上网电量等电量类指标的查询，覆盖统调/中调口径下水电、火电、核电、风电、太阳能、生物质、蓄能等各类电源",
        "tables": ["new_power_gen_rec", "new_energy_info_fill"],
        "typical_queries": [
            "广东水电发电量是多少",
            "今年各类型新能源发电量",
            "统调火电上网电量",
            "1月份风电发电量",
            "总发电量",
            "全网新能源发电量",
        ],
        "metric_keywords": ["发电", "受电", "发受电", "电量", "上网"],
    },
    {
        "topic_name": "负荷与备用",
        "description": "电网负荷类指标查询，包括最高负荷、最低负荷、平均负荷、负荷率、峰谷差、备用容量等，按地调/统调/中调三种口径区分",
        "tables": ["load_and_reserve"],
        "typical_queries": [
            "广东最高负荷",
            "今天地调负荷率",
            "峰谷差",
            "统调最高负荷时间",
            "中调备用容量",
        ],
        "metric_keywords": ["负荷", "备用", "峰谷", "出力", "最高时间", "最低时间"],
    },
    {
        "topic_name": "新能源运行",
        "description": "新能源电站（风电、光伏、生物质等）的运行情况查询，包括最大出力、平均出力、利用小时、控制电量、可发未发电量、装机等",
        "tables": ["new_energy_daily_status", "new_energy_info_fill"],
        "typical_queries": [
            "广东-阳江海上风电场最大出力",
            "新能源平均出力",
            "电站装机容量",
            "可发未发电量",
            "新能源利用率",
            "最大持续出力",
        ],
        "metric_keywords": ["出力", "装机", "利用小时", "控制电量", "可发未发", "新能源"],
    },
    {
        "topic_name": "送受电",
        "description": "省间或区域间送受电量查询，包括送电方向、计划/实际送受电量",
        "tables": ["power_transfer_receive"],
        "typical_queries": [
            "广西受海南电量",
            "广东送贵州",
            "省间送受电",
            "实际送电量",
            "计划受电量",
        ],
        "metric_keywords": ["送电", "受电", "送受电", "送出", "受入"],
    },
    {
        "topic_name": "实时量测",
        "description": "电厂、电站设备的实时遥测数据查询，包括电压、电流、频率、功率等",
        "tables": ["new_realTime_measurement"],
        "typical_queries": [
            "白鹤滩电厂电压",
            "电厂实时出力",
            "电厂频率",
            "无功功率",
            "测点数据值",
        ],
        "metric_keywords": ["电压", "电流", "频率", "功率", "数据值"],
    },
    {
        "topic_name": "断面监视",
        "description": "电网关键断面（直流、联络线）的功率、负载率、越限状态查询",
        "tables": ["power_grid_section"],
        "typical_queries": [
            "高肇直流断面功率",
            "断面越限",
            "联络线负载率",
            "断面控制值",
            "断面极限值",
        ],
        "metric_keywords": ["断面", "极限", "控制值", "负载率"],
    },
    {
        "topic_name": "跳闸故障",
        "description": "电网跳闸、停电故障相关的统计与查询，包括跳闸次数、跳闸重合成功次数、停电时长、故障原因、维护单位等",
        "tables": ["trip_info"],
        "typical_queries": [
            "今天跳闸次数是多少",
            "跳闸重合成功",
            "线路停电时长",
            "故障原因",
            "佛山地调跳闸",
            "停电次数",
        ],
        "metric_keywords": ["跳闸", "停电", "故障"],
    },
]


# ------------------------------------------------------------------
# 派生指标依赖推断
# ------------------------------------------------------------------
def infer_derived_dependencies(derived: Dict, all_meta: Dict) -> List[Dict]:
    """
    根据派生指标的 knowledgeElement 文本，关联到对应的指标/维度/维度值/表
    返回 list of {entity_type, ref_key} —— ref_key 用于事后查 ID
    """
    deps = []
    text = derived["calculation_rule"] + " " + derived["display_name"] + " " + " ".join(derived.get("aliases", []))

    # 关键关键词 -> 实体的关联规则
    rules = [
        # 跳闸类派生指标 → trip_info 表 + 停电类型 维度 + 停电类型 维度值
        ("跳闸", [
            ("table", "trip_info"),
            ("dimension_code", "power_outage_type"),
            ("dim_value", ("power_outage_type", "跳闸")),
            ("metric_code", "outage_time"),  # 用停电时间做计数
        ]),
        ("跳闸重合成功", [
            ("table", "trip_info"),
            ("dimension_code", "power_outage_type"),
            ("dim_value", ("power_outage_type", "跳闸重合成功")),
            ("metric_code", "outage_time"),
        ]),
        ("停电次数", [
            ("table", "trip_info"),
            ("dimension_code", "power_outage_type"),
            ("dimension_code", "fault_maintain_unit"),
            ("dim_value", ("power_outage_type", "跳闸")),
            ("dim_value", ("power_outage_type", "主动停运")),
        ]),
        ("停电时长", [
            ("table", "trip_info"),
            ("metric_code", "outage_time"),
            ("metric_code", "restore_time"),
        ]),
        ("新能源发电量", [
            ("table", "new_energy_info_fill"),
            ("table", "new_power_gen_rec"),
            ("dimension_code", "gen_type"),
            ("dim_value", ("gen_type", "风能")),
            ("dim_value", ("gen_type", "集中式光伏")),
            ("dim_value", ("gen_type", "统调光伏")),
            ("dim_value", ("gen_type", "总分布式光伏")),
            ("dim_value", ("gen_type", "总光伏")),
            ("dim_value", ("gen_type", "生物质")),
        ]),
        ("电站", [
            ("dimension_code", "name"),
        ]),
        ("南方五省", [
            ("dimension_code", "region_name"),
            ("dim_value", ("region_name", "广东")),
            ("dim_value", ("region_name", "广西")),
            ("dim_value", ("region_name", "云南")),
            ("dim_value", ("region_name", "贵州")),
            ("dim_value", ("region_name", "海南")),
        ]),
        ("全网", [
            ("dimension_code", "region_name"),
            ("dim_value", ("region_name", "广东")),
            ("dim_value", ("region_name", "广西")),
            ("dim_value", ("region_name", "云南")),
            ("dim_value", ("region_name", "贵州")),
            ("dim_value", ("region_name", "海南")),
        ]),
    ]

    name = derived["display_name"]
    aliases = derived.get("aliases", [])
    keywords_to_check = [name] + aliases

    seen = set()
    for keyword, dep_list in rules:
        if any(keyword in kw for kw in keywords_to_check):
            for ent_type, ref_key in dep_list:
                key = (ent_type, ref_key if isinstance(ref_key, str) else tuple(ref_key))
                if key in seen:
                    continue
                seen.add(key)
                deps.append({"entity_type": ent_type, "ref_key": ref_key})

    return deps


# ------------------------------------------------------------------
# 处理主入口
# ------------------------------------------------------------------
class MetadataProcessor:

    def __init__(self):
        self.db = get_db()
        self.embed = get_embedding_client()
        self.tb = EmbeddingTextBuilder()

    def load_raw(self, path: str) -> Dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def process(self, raw_path: str = None, encode_embeddings: bool = True) -> Dict[str, int]:
        """主流程"""
        raw_path = raw_path or str(config.DATA_DIR / "raw_meta.json")
        raw = self.load_raw(raw_path)
        db_meta = raw["database_meta"]

        logger.info("=" * 60)
        logger.info(f"Start metadata processing from {raw_path}")
        logger.info(f"  metrics={len(db_meta['available_metrics'])}, "
                    f"dimensions={len(db_meta['available_dimensions'])}, "
                    f"tables={len(db_meta['table_summaries'])}")

        # 清空所有元数据表（保留 recall_config）
        self._truncate_meta_tables()

        # 1. 处理维度（先入库，因为指标和维度值都引用它们）
        dim_id_by_code = self._process_dimensions(db_meta)
        logger.info(f"Dimensions processed: {len(dim_id_by_code)}")

        # 2. 处理维度值
        dim_value_records = self._process_dim_values(db_meta, dim_id_by_code)
        logger.info(f"Dim values processed: {len(dim_value_records)}")

        # 3. 推断 表-指标 / 表-维度 / 表-维度值 关系
        mapping = self._infer_mappings(db_meta)

        # 4. 处理指标（指标可能存在于多张表，先入库再建表关系）
        metric_id_by_code = self._process_metrics(db_meta, mapping)
        logger.info(f"Metrics processed: {len(metric_id_by_code)}")

        # 5. 处理表（embedding_text 需要 metric_names / dimension_names）
        table_id_by_name = self._process_tables(db_meta, mapping, dim_id_by_code)
        logger.info(f"Tables processed: {len(table_id_by_name)}")

        # 6. 写入 表↔指标 / 表↔维度 / 表↔维度值 关系
        self._write_relations(mapping, table_id_by_name, metric_id_by_code, dim_id_by_code, dim_value_records)

        # 7. 处理业务主题
        topic_id_by_name = self._process_topics(table_id_by_name, metric_id_by_code, dim_id_by_code, db_meta)
        logger.info(f"Topics processed: {len(topic_id_by_name)}")

        # 8. 处理派生指标
        derived_count = self._process_derived_metrics(
            db_meta, table_id_by_name, metric_id_by_code, dim_id_by_code, dim_value_records,
        )
        logger.info(f"Derived metrics processed: {derived_count}")

        # 9. 编码所有 embedding（可选，便于调试时跳过）
        if encode_embeddings:
            self._encode_all_embeddings()
            logger.info("All embeddings encoded.")

        logger.info("Metadata processing finished.")
        return {
            "tables": len(table_id_by_name),
            "metrics": len(metric_id_by_code),
            "dimensions": len(dim_id_by_code),
            "dim_values": len(dim_value_records),
            "topics": len(topic_id_by_name),
            "derived_metrics": derived_count,
        }

    # -------------- private --------------
    def _truncate_meta_tables(self):
        for t in [
            "rel_topic_entity", "rel_table_metric", "rel_table_dimension",
            "rel_table_dimension_value", "rel_derived_dependency",
            "meta_business_topic", "meta_table", "meta_metric",
            "meta_dimension_value", "meta_dimension", "meta_derived_metric",
        ]:
            try:
                self.db.execute(f"DELETE FROM {t}")
            except Exception:
                pass

    def _process_dimensions(self, db_meta: Dict) -> Dict[str, int]:
        """落库维度并返回 code→id 映射"""
        # 收集所有 available_dimensions + 表中标记为 dimension 的列
        dims_by_code = {}
        for d in db_meta["available_dimensions"]:
            code = d["dimension_code"]
            dims_by_code[code] = {
                "dimension_code": code,
                "dimension_name": d["dimension_name"],
                "description": d.get("description") or DIM_DISPLAY_NAME_MAP.get(code, d["dimension_name"]),
                "possible_values": d.get("possible_values") or [],
            }

        # 补充表中存在但 available_dimensions 中没有的列（如 ptdate/month 等基础时间维度）
        for t in db_meta["table_summaries"]:
            for c in t["columns"]:
                if not c.get("is_dimension"):
                    continue
                code = c["column_name"]
                if code in dims_by_code:
                    continue
                # 补一个基础维度
                desc = c.get("description") or DIM_DISPLAY_NAME_MAP.get(code, code)
                dims_by_code[code] = {
                    "dimension_code": code,
                    "dimension_name": DIM_DISPLAY_NAME_MAP.get(code, desc),
                    "description": desc,
                    "possible_values": [],
                }

        id_map = {}
        for code, d in dims_by_code.items():
            display_name = DIM_DISPLAY_NAME_MAP.get(code, d["dimension_name"])
            synonyms = "、".join(DIM_SYNONYMS.get(code, []))
            sample_values = d["possible_values"][:10] if d["possible_values"] else []
            embedding_text = self.tb.build_dimension_text({
                "dimension_name": code,
                "display_name": display_name,
                "description": d["description"],
                "synonyms": synonyms,
                "sample_values": sample_values,
            })
            sql = ("INSERT INTO meta_dimension(dimension_name, display_name, description, "
                   "synonyms, embedding_text) VALUES (%s,%s,%s,%s,%s)")
            new_id = self.db.execute_returning_id(sql, [code, display_name, d["description"], synonyms, embedding_text])
            id_map[code] = new_id
        return id_map

    def _process_dim_values(self, db_meta: Dict, dim_id_by_code: Dict[str, int]) -> List[Dict]:
        """
        把 possible_values 展开为 meta_dimension_value 行
        返回 [{value_id, dimension_id, value_name, dimension_code}, ...]
        """
        records = []
        for d in db_meta["available_dimensions"]:
            code = d["dimension_code"]
            pv = d.get("possible_values") or []
            if not isinstance(pv, list) or not pv:
                continue
            dim_id = dim_id_by_code.get(code)
            if dim_id is None:
                continue
            display_name = DIM_DISPLAY_NAME_MAP.get(code, d["dimension_name"])
            for v in pv:
                if not isinstance(v, str):
                    continue
                v = v.strip()
                if not v:
                    continue
                desc = f"{display_name}：{v}"
                # 别名：去掉前缀（如 "广东-阳江海上风电场" → "阳江海上风电场"）
                synonyms = []
                if "-" in v:
                    synonyms.append(v.split("-", 1)[1])
                if "受" in v or "送" in v:
                    pass  # 送受电方向保留原值
                synonyms_str = "、".join(synonyms)

                embedding_text = self.tb.build_dim_value_text({
                    "display_name": v,
                    "dimension_display_name": display_name,
                    "description": desc,
                    "synonyms": synonyms_str,
                })
                sql = ("INSERT INTO meta_dimension_value(dimension_id, value_name, "
                       "display_name, description, synonyms, embedding_text) "
                       "VALUES (%s,%s,%s,%s,%s,%s)")
                vid = self.db.execute_returning_id(sql, [dim_id, v, v, desc, synonyms_str, embedding_text])
                records.append({
                    "value_id": vid,
                    "dimension_id": dim_id,
                    "dimension_code": code,
                    "value_name": v,
                })
        return records

    def _infer_mappings(self, db_meta: Dict) -> Dict:
        """
        基于表的 columns 推断：
          table_to_metric_codes:    {table_name: [metric_code, ...]}
          table_to_dim_codes:       {table_name: [dimension_code, ...]}
          metric_code_to_tables:    {metric_code: [table_name, ...]}
          dim_code_to_tables:       {dimension_code: [table_name, ...]}
        """
        metrics_by_code = {m["metric_code"]: m for m in db_meta["available_metrics"]}
        metrics_by_name = {m["metric_name"]: m for m in db_meta["available_metrics"]}
        dims_by_code = {d["dimension_code"]: d for d in db_meta["available_dimensions"]}
        dims_by_name = {d["dimension_name"]: d for d in db_meta["available_dimensions"]}

        table_to_metric_codes = defaultdict(list)
        table_to_dim_codes = defaultdict(list)
        metric_code_to_tables = defaultdict(list)
        dim_code_to_tables = defaultdict(list)

        # 同时记录"表中独有但不在 available 列表中"的指标/维度，全部归并入 available 池
        extra_metrics = {}  # code -> {metric_name, description, ...}

        for t in db_meta["table_summaries"]:
            tn = t["table_name"]
            for c in t["columns"]:
                col = c["column_name"]
                desc = c.get("description", "").strip() or col
                if c.get("is_measure"):
                    # 优先 column_name == metric_code
                    if col in metrics_by_code:
                        mc = col
                    elif desc in metrics_by_name:
                        mc = metrics_by_name[desc]["metric_code"]
                    else:
                        # 表内独有指标，新建一条
                        mc = col
                        extra_metrics[mc] = {
                            "metric_code": mc,
                            "metric_name": desc,
                            "description": desc,
                            "unit": "",
                            "data_type": c.get("data_type", ""),
                            "caliber_scope": "none",
                        }
                    table_to_metric_codes[tn].append(mc)
                    metric_code_to_tables[mc].append(tn)

                if c.get("is_dimension"):
                    if col in dims_by_code:
                        dc = col
                    elif desc in dims_by_name:
                        dc = dims_by_name[desc]["dimension_code"]
                    else:
                        dc = col  # 已在 _process_dimensions 中补全
                    table_to_dim_codes[tn].append(dc)
                    dim_code_to_tables[dc].append(tn)

        return {
            "table_to_metric_codes": dict(table_to_metric_codes),
            "table_to_dim_codes": dict(table_to_dim_codes),
            "metric_code_to_tables": dict(metric_code_to_tables),
            "dim_code_to_tables": dict(dim_code_to_tables),
            "extra_metrics": extra_metrics,
        }

    def _process_metrics(self, db_meta: Dict, mapping: Dict) -> Dict[str, int]:
        """落库指标，返回 code→id 映射"""
        # 合并 available_metrics + extra_metrics（表内独有）
        all_metrics = {m["metric_code"]: m for m in db_meta["available_metrics"]}
        for code, m in mapping["extra_metrics"].items():
            if code not in all_metrics:
                all_metrics[code] = m

        id_map = {}
        for code, m in all_metrics.items():
            mname = m["metric_name"]
            tables = mapping["metric_code_to_tables"].get(code, [])
            source_table = TABLE_ENHANCEMENT.get(tables[0], {}).get("display_name", tables[0]) if tables else ""
            unit = m.get("unit") or infer_unit(mname)
            synonyms = infer_metric_synonyms(mname)
            synonyms_str = "、".join(synonyms)
            caliber = m.get("caliber_scope") or "none"

            # 业务主题：根据所属表反推
            business_topics = []
            for tn in tables:
                topics_for_t = [td["topic_name"] for td in TOPIC_DEFINITIONS if tn in td["tables"]]
                business_topics.extend(topics_for_t)
            business_topics = list(dict.fromkeys(business_topics))  # 去重保序

            display_name = mname
            if unit and unit not in mname:
                display_name = f"{mname}({unit})"

            embedding_text = self.tb.build_metric_text({
                "metric_name": code,
                "display_name": display_name,
                "description": m.get("description", mname),
                "business_topics": business_topics,
                "caliber_scope": caliber,
                "source_table": source_table,
                "synonyms": synonyms_str,
                "unit": unit,
            })

            sql = ("INSERT INTO meta_metric(metric_name, display_name, description, "
                   "synonyms, calculation, unit, caliber_scope, embedding_text) "
                   "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
            new_id = self.db.execute_returning_id(sql, [
                code, display_name, m.get("description", mname),
                synonyms_str, "", unit, caliber, embedding_text,
            ])
            id_map[code] = new_id
        return id_map

    def _process_tables(self, db_meta: Dict, mapping: Dict, dim_id_by_code: Dict[str, int]) -> Dict[str, int]:
        id_map = {}
        for t in db_meta["table_summaries"]:
            tn = t["table_name"]
            enh = TABLE_ENHANCEMENT.get(tn, {})
            display_name = enh.get("display_name", t.get("description", tn) or tn)
            description = enh.get("description", t.get("description", tn) or display_name)
            business_topics = enh.get("business_topics", [])
            typical_qs = enh.get("typical_questions", [])

            metric_codes = mapping["table_to_metric_codes"].get(tn, [])
            metric_names = []
            for mc in metric_codes:
                # 找到 metric 名
                mm = next((x for x in db_meta["available_metrics"] if x["metric_code"] == mc), None)
                metric_names.append(mm["metric_name"] if mm else mc)

            dim_codes = mapping["table_to_dim_codes"].get(tn, [])
            dim_names = [DIM_DISPLAY_NAME_MAP.get(dc, dc) for dc in dim_codes]

            embedding_text = self.tb.build_table_text({
                "table_name": tn,
                "display_name": display_name,
                "description": description,
                "business_topics": business_topics,
                "metric_names": metric_names,
                "dimension_names": dim_names,
                "typical_questions": typical_qs,
            })

            sql = ("INSERT INTO meta_table(table_name, display_name, description, "
                   "embedding_text) VALUES (%s,%s,%s,%s)")
            new_id = self.db.execute_returning_id(sql, [tn, display_name, description, embedding_text])
            id_map[tn] = new_id
        return id_map

    def _write_relations(self, mapping: Dict,
                         table_id_by_name: Dict[str, int],
                         metric_id_by_code: Dict[str, int],
                         dim_id_by_code: Dict[str, int],
                         dim_value_records: List[Dict]):
        # 表↔指标
        for tn, mcs in mapping["table_to_metric_codes"].items():
            tid = table_id_by_name.get(tn)
            if tid is None:
                continue
            seen = set()
            for mc in mcs:
                mid = metric_id_by_code.get(mc)
                if mid is None or (tid, mid) in seen:
                    continue
                seen.add((tid, mid))
                self.db.execute(
                    "INSERT INTO rel_table_metric(table_id, metric_id) VALUES (%s,%s)", [tid, mid]
                )
        # 表↔维度
        for tn, dcs in mapping["table_to_dim_codes"].items():
            tid = table_id_by_name.get(tn)
            if tid is None:
                continue
            seen = set()
            for dc in dcs:
                did = dim_id_by_code.get(dc)
                if did is None or (tid, did) in seen:
                    continue
                seen.add((tid, did))
                self.db.execute(
                    "INSERT INTO rel_table_dimension(table_id, dimension_id) VALUES (%s,%s)", [tid, did]
                )
        # 表↔维度值（一个维度值绑定到所有包含该维度的表）
        for rec in dim_value_records:
            dc = rec["dimension_code"]
            for tn in mapping["dim_code_to_tables"].get(dc, []):
                tid = table_id_by_name.get(tn)
                if tid is None:
                    continue
                self.db.execute(
                    "INSERT INTO rel_table_dimension_value(table_id, dimension_id, value_id) "
                    "VALUES (%s,%s,%s)",
                    [tid, rec["dimension_id"], rec["value_id"]],
                )

    def _process_topics(self, table_id_by_name, metric_id_by_code, dim_id_by_code, db_meta):
        id_map = {}
        for td in TOPIC_DEFINITIONS:
            embedding_text = self.tb.build_topic_text({
                "topic_name": td["topic_name"],
                "description": td["description"],
                "typical_queries": td["typical_queries"],
            })
            typical_json = json.dumps(td["typical_queries"], ensure_ascii=False)
            sql = ("INSERT INTO meta_business_topic(topic_name, parent_id, topic_level, "
                   "description, typical_queries, embedding_text) VALUES (%s,%s,%s,%s,%s,%s)")
            tid = self.db.execute_returning_id(sql, [
                td["topic_name"], None, 1, td["description"], typical_json, embedding_text,
            ])
            id_map[td["topic_name"]] = tid

            # 维护 主题↔实体 映射：
            #   - 表：topic.tables 中的所有表
            #   - 指标：topic.tables 中所有表的指标 ∪ metric_keywords 命中的指标
            #   - 维度：topic.tables 中所有表的维度
            entity_keys = set()
            for tn in td["tables"]:
                table_pk = table_id_by_name.get(tn)
                if table_pk:
                    entity_keys.add(("table", table_pk))
                # 表中的指标和维度
                for m in db_meta["available_metrics"]:
                    if any(kw in m["metric_name"] for kw in td["metric_keywords"]):
                        mid = metric_id_by_code.get(m["metric_code"])
                        if mid:
                            entity_keys.add(("metric", mid))

            for et, eid in entity_keys:
                try:
                    self.db.execute(
                        "INSERT INTO rel_topic_entity(topic_id, entity_type, entity_id) VALUES (%s,%s,%s)",
                        [tid, et, eid],
                    )
                except Exception:
                    pass
        return id_map

    def _process_derived_metrics(self, db_meta, table_id_by_name, metric_id_by_code,
                                 dim_id_by_code, dim_value_records) -> int:
        bc = db_meta.get("business_context") or []
        if not bc:
            return 0
        # 维度值 lookup: (dim_code, value_name) -> value_id
        dv_lookup = {(r["dimension_code"], r["value_name"]): r["value_id"] for r in dim_value_records}

        count = 0
        for entry in bc:
            aliases = entry.get("knowledgeAlias", [])
            if not aliases:
                continue
            display_name = aliases[0]
            description = entry.get("knowledgeElement", "")
            calc_rule = description
            aliases_str = "、".join(aliases)

            embedding_text = self.tb.build_derived_metric_text({
                "display_name": display_name,
                "description": description,
                "calculation_rule": calc_rule,
                "aliases": aliases_str,
                "dependent_entities": [],  # 在依赖入库后另行更新（可选）
            })

            sql = ("INSERT INTO meta_derived_metric(derived_name, display_name, description, "
                   "aliases, calculation_rule, embedding_text) VALUES (%s,%s,%s,%s,%s,%s)")
            did = self.db.execute_returning_id(sql, [
                display_name, display_name, description, aliases_str, calc_rule, embedding_text,
            ])

            # 推断依赖
            deps = infer_derived_dependencies({
                "display_name": display_name,
                "description": description,
                "calculation_rule": calc_rule,
                "aliases": aliases,
            }, all_meta=None)

            for dep in deps:
                et = dep["entity_type"]
                rk = dep["ref_key"]
                eid = None
                if et == "table":
                    eid = table_id_by_name.get(rk)
                    final_et = "table"
                elif et == "metric_code":
                    eid = metric_id_by_code.get(rk)
                    final_et = "metric"
                elif et == "dimension_code":
                    eid = dim_id_by_code.get(rk)
                    final_et = "dimension"
                elif et == "dim_value":
                    eid = dv_lookup.get(rk)
                    final_et = "dim_value"
                else:
                    continue
                if eid is None:
                    continue
                try:
                    self.db.execute(
                        "INSERT INTO rel_derived_dependency(derived_id, entity_type, entity_id) VALUES (%s,%s,%s)",
                        [did, final_et, eid],
                    )
                except Exception:
                    pass
            count += 1
        return count

    def _encode_all_embeddings(self):
        """对所有 meta_* 表的 embedding_text 编码并写回 embedding_json"""
        encode_targets = [
            ("meta_table", "table_id"),
            ("meta_metric", "metric_id"),
            ("meta_dimension", "dimension_id"),
            ("meta_dimension_value", "value_id"),
            ("meta_business_topic", "topic_id"),
            ("meta_derived_metric", "derived_id"),
        ]
        for table, pk in encode_targets:
            rows = self.db.query(f"SELECT {pk} as id, embedding_text FROM {table}")
            if not rows:
                continue
            texts = [r["embedding_text"] for r in rows]
            ids = [r["id"] for r in rows]
            logger.info(f"Encoding {len(texts)} rows for {table}...")
            vecs = self.embed.encode(texts)
            for rid, vec in zip(ids, vecs):
                vj = json.dumps(vec.tolist())
                self.db.execute(
                    f"UPDATE {table} SET embedding_json=%s WHERE {pk}=%s", [vj, rid]
                )
            logger.info(f"  {table}: encoded & saved")
