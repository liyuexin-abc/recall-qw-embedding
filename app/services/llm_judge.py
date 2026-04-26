"""
LLM 精判（Stage 2）：从召回候选集中筛选与 query 真正相关的实体。
对应方案第六节。
"""
import json
from typing import List
from app.core.llm import LLMClient, get_llm_client
from app.utils.logger import path_logger


class LLMJudge:
    PROMPT = """你是一个数据分析助手。用户提出了一个数据查询问题，
我已经从数据库中初步筛选了一批可能相关的数据元素。
请你根据用户的问题，从候选列表中选出所有与用户问题相关的数据元素。

## 规则
1. 宁可多选，不要漏掉，但是要避免明显不相关的元素
2. 注意调度口径区分（地调/统调/中调），用户明确指定的口径才选对应指标，未指定的不带任何后缀
3. 维度值只在用户明确提到或暗示时才选取（例如"广东"才选维度值"广东"）
4. 如果候选中有"业务术语/派生指标"，优先选择，并保留它依赖的底层字段
5. 时间相关维度（日期、月份、季度、年度）一般不需要选取（时间已在外层处理）
6. 对于"计数"类问题（如"跳闸次数"），应选择对应表的主键/计数字段作为指标

## 用户问题
{query}

## 候选数据表
{table_candidates}

## 候选指标（已按相关度排序）
{metric_candidates}

## 候选维度
{dimension_candidates}

## 候选维度值（仅当用户明确提到才选）
{dim_value_candidates}

## 候选业务术语 / 派生指标
{derived_candidates}

## 输出（必须是合法 JSON，仅返回 JSON，不要任何其它文字）
{{
  "selected_tables":     ["表名1"],
  "selected_metrics":    ["指标名1"],
  "selected_dimensions": ["维度名1"],
  "selected_dim_values": ["维度值1"],
  "selected_derived":    ["派生指标名1"],
  "reasoning": "简要说明选择理由"
}}"""

    def __init__(self, llm_client: LLMClient = None):
        self.llm = llm_client or get_llm_client()
        self.logger = path_logger("judge")

    def judge(self, query: str, candidates: List[dict], top_per_bucket: int = 30) -> dict:
        # 分桶（按 source 优先 path_a/d > path_b/c）
        tables, metrics, dims, values, derived = [], [], [], [], []
        for c in candidates:
            line = f"  - 【{c['display_name']}】{c.get('description','')[:80]} (score={c.get('score',0):.3f}, src={c.get('source','')})"
            et = c["entity_type"]
            bucket = {
                "table": tables, "metric": metrics, "dimension": dims,
                "dim_value": values, "derived_metric": derived,
            }.get(et)
            if bucket is not None:
                bucket.append(line)

        # 各桶前 N
        prompt = self.PROMPT.format(
            query=query,
            table_candidates="\n".join(tables[:top_per_bucket]) if tables else "（无）",
            metric_candidates="\n".join(metrics[:top_per_bucket]) if metrics else "（无）",
            dimension_candidates="\n".join(dims[:top_per_bucket]) if dims else "（无）",
            dim_value_candidates="\n".join(values[:50]) if values else "（无）",
            derived_candidates="\n".join(derived[:20]) if derived else "（无）",
        )
        try:
            ans = self.llm.generate_json(prompt)
            self.logger.info(f"query='{query}' judged={list(ans.get('selected_metrics', []))[:5]} "
                           f"dims={list(ans.get('selected_dimensions', []))[:5]} "
                           f"vals={list(ans.get('selected_dim_values', []))[:5]} "
                           f"derived={list(ans.get('selected_derived', []))[:5]}")
            return ans
        except Exception as e:
            self.logger.error(f"judge fail: {e}; query={query}")
            return {
                "selected_tables": [], "selected_metrics": [], "selected_dimensions": [],
                "selected_dim_values": [], "selected_derived": [], "reasoning": f"LLM_FAIL:{e}",
            }
