"""
四路并行召回服务（路径 A / B / C / D）
严格遵循技术方案 §五：
  - 路径 A：先召回 Top-N 张表，再在每张表内召回指标/维度/维度值
  - 路径 B：主题召回 → 主题下全部实体
  - 路径 C：全局指标+维度兜底
  - 路径 D：派生指标 + 依赖的指标/维度/维度值

日志：
  - 每路在自己专属 logger（path_a/b/c/d.log）输出召回明细
  - 主 logger 输出耗时与候选数
"""
import re
import time
import json
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple, Dict, Any
from concurrent.futures import ThreadPoolExecutor

from app.core.embedding import EmbeddingClient, get_embedding_client
from app.core.config_manager import RecallConfigManager, PathConfig, get_config_manager
from app.utils.logger import get_logger, path_logger

main_logger = get_logger("recall.service", "recall.log")
log_a = path_logger("path_a")
log_b = path_logger("path_b")
log_c = path_logger("path_c")
log_d = path_logger("path_d")
log_merge = path_logger("merge")


@dataclass
class RecallResult:
    entity_type: str
    entity_id: int
    display_name: str
    description: str
    score: float
    source: str
    table_id: Optional[int] = None
    dimension_id: Optional[int] = None

    def to_dict(self):
        return asdict(self)


def _entity_id_of(entity: Dict) -> Optional[int]:
    et = entity.get("entity_type")
    key_map = {
        "table": "table_id", "metric": "metric_id",
        "dimension": "dimension_id", "dim_value": "value_id",
        "topic": "topic_id", "derived_metric": "derived_id",
    }
    key = key_map.get(et)
    if key is None:
        return None
    val = entity.get(key)
    return int(val) if val is not None else None


def _apply_recall_mode(scores: np.ndarray, ids: np.ndarray,
                       cfg: PathConfig) -> List[Tuple[int, float]]:
    """根据召回模式过滤 (id, score) 序列"""
    pairs = [(int(i), float(s)) for i, s in zip(ids, scores) if i >= 0]
    if cfg.recall_mode == "top_k":
        return pairs[:cfg.top_k]
    elif cfg.recall_mode == "threshold":
        return [(i, s) for i, s in pairs if s >= cfg.threshold]
    elif cfg.recall_mode == "hybrid":
        filtered = [(i, s) for i, s in pairs if s >= cfg.threshold]
        if filtered:
            return filtered[:cfg.top_k]
        return pairs[:cfg.top_k]
    return pairs[:cfg.top_k]


class RecallService:
    QUERY_INSTRUCT = ("Instruct: 根据用户的数据查询问题，"
                      "检索相关的数据表、指标、维度、维度值和业务术语\nQuery: ")

    _TIME_PATTERNS = [
        r"今[天日]", r"昨[天日]", r"明[天日]",
        r"本[周月年季度]", r"上[周月年]", r"下[周月年]",
        r"近\d+[天日周月年]", r"过去\d+[天日周月年]",
        r"\d{4}[-/年]\d{1,2}([-/月]\d{1,2})?[日号]?",
        r"\d{1,2}月份?", r"\d{1,2}月\d{1,2}[日号]",
        r"第[一二三四1234]季度",
        r"\d{1,2}月前\d+天", r"前\d+[天日]",
        r"去年", r"今年", r"明年",
    ]

    def __init__(self,
                 embed_client: EmbeddingClient = None,
                 indexes: Dict[str, Any] = None,
                 config_manager: RecallConfigManager = None):
        self.embed = embed_client or get_embedding_client()
        self.indexes = indexes or {}
        self.cfg_mgr = config_manager or get_config_manager()
        self.topic_entity_mapping: Dict[int, List[Dict]] = self.indexes.get("topic_entity_mapping", {})
        self.derived_dependency_mapping: Dict[int, List[Dict]] = self.indexes.get("derived_dependency_mapping", {})

        self._executor = ThreadPoolExecutor(max_workers=4)

    def update_indexes(self, indexes: Dict[str, Any]):
        self.indexes = indexes
        self.topic_entity_mapping = indexes.get("topic_entity_mapping", {})
        self.derived_dependency_mapping = indexes.get("derived_dependency_mapping", {})

    def _strip_time(self, query: str) -> Tuple[str, List[str]]:
        time_terms = []
        clean = query
        for pat in self._TIME_PATTERNS:
            for m in re.finditer(pat, clean):
                time_terms.append(m.group(0))
            clean = re.sub(pat, " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()
        return clean or query, time_terms

    def encode_query(self, query: str) -> Tuple[np.ndarray, str, List[str]]:
        clean_query, time_terms = self._strip_time(query)
        query_text = self.QUERY_INSTRUCT + clean_query
        vec = self.embed.encode([query_text])
        return vec, clean_query, time_terms

    def recall(self, query: str, parallel: bool = True) -> Dict[str, Any]:
        t0 = time.time()
        query_vec, clean_query, time_terms = self.encode_query(query)
        t1 = time.time()

        if parallel:
            futA = self._executor.submit(self._path_a_recall, query_vec)
            futB = self._executor.submit(self._path_b_recall, query_vec)
            futC = self._executor.submit(self._path_c_recall, query_vec)
            futD = self._executor.submit(self._path_d_recall, query_vec)
            path_a = futA.result()
            path_b = futB.result()
            path_c = futC.result()
            path_d = futD.result()
        else:
            path_a = self._path_a_recall(query_vec)
            path_b = self._path_b_recall(query_vec)
            path_c = self._path_c_recall(query_vec)
            path_d = self._path_d_recall(query_vec)
        t2 = time.time()

        merged = self._merge_and_deduplicate(path_a, path_b, path_c, path_d)
        t3 = time.time()

        timings = {
            "encode_ms":   round(1000 * (t1 - t0), 2),
            "retrieval_ms":round(1000 * (t2 - t1), 2),
            "merge_ms":    round(1000 * (t3 - t2), 2),
            "total_ms":    round(1000 * (t3 - t0), 2),
        }

        main_logger.info(
            f"Q={query!r} | clean={clean_query!r} | time_terms={time_terms} | "
            f"A={len(path_a)} B={len(path_b)} C={len(path_c)} D={len(path_d)} "
            f"merged={len(merged)} | enc={timings['encode_ms']}ms "
            f"ret={timings['retrieval_ms']}ms mer={timings['merge_ms']}ms"
        )

        return {
            "query": query,
            "clean_query": clean_query,
            "time_terms": time_terms,
            "candidates": [r.to_dict() for r in merged],
            "by_path": {
                "path_a": [r.to_dict() for r in path_a],
                "path_b": [r.to_dict() for r in path_b],
                "path_c": [r.to_dict() for r in path_c],
                "path_d": [r.to_dict() for r in path_d],
            },
            "timings_ms": timings,
        }

    # ============ 路径 A ============
    def _path_a_recall(self, query_vec: np.ndarray) -> List[RecallResult]:
        results = []
        cfg_table = self.cfg_mgr.get("path_a_table", "table")
        if not cfg_table.enabled or "table_index" not in self.indexes:
            log_a.info("path_a disabled or no index")
            return results

        # Stage1: 表级
        k_search = max(cfg_table.top_k, 50)
        scores, ids = self.indexes["table_index"].search(query_vec, k_search)
        recalled_pairs = _apply_recall_mode(scores[0], ids[0], cfg_table)
        recalled_table_ids = []
        log_a.info(f"== Stage1 表级召回 mode={cfg_table.recall_mode} top_k={cfg_table.top_k} "
                   f"th={cfg_table.threshold:.4f}")
        for tid, score in recalled_pairs:
            tmeta = self.indexes["table_meta"][tid]
            results.append(RecallResult(
                entity_type="table", entity_id=int(tmeta["table_id"]),
                display_name=tmeta["display_name"], description=tmeta["description"],
                score=score, source="path_a",
            ))
            recalled_table_ids.append(int(tmeta["table_id"]))
            log_a.info(f"  [table] {tmeta['table_name']:30s} ({tmeta['display_name']}) score={score:.4f}")

        # Stage2: 表内三类实体
        cfg_metric = self.cfg_mgr.get("path_a_entity", "metric")
        cfg_dim = self.cfg_mgr.get("path_a_entity", "dimension")
        cfg_dv = self.cfg_mgr.get("path_a_entity", "dim_value")
        log_a.info(f"== Stage2 表内召回 metric(top_k={cfg_metric.top_k},on={cfg_metric.enabled}) "
                   f"| dim(top_k={cfg_dim.top_k},on={cfg_dim.enabled}) "
                   f"| dim_value(top_k={cfg_dv.top_k},on={cfg_dv.enabled})")

        for tid in recalled_table_ids:
            sub = self.indexes.get("table_entity_indexes", {}).get(tid)
            if not sub:
                continue
            k_search = max(cfg_metric.top_k + cfg_dim.top_k + cfg_dv.top_k, 100)
            e_scores, e_ids = sub["index"].search(query_vec, k_search)
            metric_pool, dim_pool, dv_pool = [], [], []
            for eid, sc in zip(e_ids[0], e_scores[0]):
                if eid < 0:
                    continue
                ent = sub["entities"][eid]
                et = ent["entity_type"]
                if et == "metric":
                    metric_pool.append((eid, float(sc), ent))
                elif et == "dimension":
                    dim_pool.append((eid, float(sc), ent))
                elif et == "dim_value":
                    dv_pool.append((eid, float(sc), ent))

            for pool, cfg, name in [(metric_pool, cfg_metric, "metric"),
                                    (dim_pool, cfg_dim, "dimension"),
                                    (dv_pool, cfg_dv, "dim_value")]:
                if not cfg.enabled or not pool:
                    continue
                scs = np.array([p[1] for p in pool])
                idx = np.arange(len(pool))
                kept = _apply_recall_mode(scs, idx, cfg)
                for local_i, sc in kept:
                    ent = pool[local_i][2]
                    eid_real = _entity_id_of(ent)
                    results.append(RecallResult(
                        entity_type=ent["entity_type"], entity_id=eid_real,
                        display_name=ent["display_name"],
                        description=ent.get("description", ""),
                        score=sc, source="path_a",
                        table_id=tid,
                        dimension_id=ent.get("dimension_id"),
                    ))
                    log_a.info(f"  [{name}] table={tid} {ent['display_name']} score={sc:.4f}")
        return results

    # ============ 路径 B ============
    def _path_b_recall(self, query_vec: np.ndarray) -> List[RecallResult]:
        results = []
        cfg = self.cfg_mgr.get("path_b_topic", "topic")
        if not cfg.enabled or "topic_index" not in self.indexes:
            log_b.info("path_b disabled or no index")
            return results

        scores, ids = self.indexes["topic_index"].search(query_vec, max(cfg.top_k, 20))
        kept = _apply_recall_mode(scores[0], ids[0], cfg)
        log_b.info(f"== 主题召回 mode={cfg.recall_mode} top_k={cfg.top_k} th={cfg.threshold}")
        for tid, score in kept:
            topic = self.indexes["topic_meta"][tid]
            log_b.info(f"  [topic] {topic['topic_name']} score={score:.4f}")
            for ent in self.topic_entity_mapping.get(topic["topic_id"], []):
                eid = _entity_id_of(ent)
                results.append(RecallResult(
                    entity_type=ent["entity_type"], entity_id=eid,
                    display_name=ent.get("display_name", ""),
                    description=ent.get("description", ""),
                    score=score * 0.9, source="path_b",
                    table_id=ent.get("table_id"),
                    dimension_id=ent.get("dimension_id"),
                ))
                log_b.info(f"      └─ {ent['entity_type']:10s} {ent.get('display_name','')} score*0.9={score*0.9:.4f}")
        return results

    # ============ 路径 C ============
    def _path_c_recall(self, query_vec: np.ndarray) -> List[RecallResult]:
        results = []
        cfg_metric = self.cfg_mgr.get("path_c_global", "metric")
        cfg_dim = self.cfg_mgr.get("path_c_global", "dimension")
        if not (cfg_metric.enabled or cfg_dim.enabled) or "global_entity_index" not in self.indexes:
            log_c.info("path_c disabled or no index")
            return results

        k_search = max(cfg_metric.top_k + cfg_dim.top_k, 100)
        scores, ids = self.indexes["global_entity_index"].search(query_vec, k_search)
        metric_pool, dim_pool = [], []
        for eid, sc in zip(ids[0], scores[0]):
            if eid < 0:
                continue
            ent = self.indexes["global_entity_meta"][eid]
            if ent["entity_type"] == "metric":
                metric_pool.append((eid, float(sc), ent))
            elif ent["entity_type"] == "dimension":
                dim_pool.append((eid, float(sc), ent))

        log_c.info(f"== 全局兜底 metric(top_k={cfg_metric.top_k},th={cfg_metric.threshold}) "
                   f"| dim(top_k={cfg_dim.top_k},th={cfg_dim.threshold})")

        for pool, cfg, name in [(metric_pool, cfg_metric, "metric"),
                                (dim_pool, cfg_dim, "dimension")]:
            if not cfg.enabled or not pool:
                continue
            scs = np.array([p[1] for p in pool])
            idx = np.arange(len(pool))
            kept = _apply_recall_mode(scs, idx, cfg)
            for local_i, sc in kept:
                ent = pool[local_i][2]
                eid_real = _entity_id_of(ent)
                results.append(RecallResult(
                    entity_type=ent["entity_type"], entity_id=eid_real,
                    display_name=ent["display_name"],
                    description=ent.get("description", ""),
                    score=sc, source="path_c",
                    table_id=ent.get("table_id"),
                ))
                log_c.info(f"  [{name}] {ent['display_name']} score={sc:.4f}")
        return results

    # ============ 路径 D ============
    def _path_d_recall(self, query_vec: np.ndarray) -> List[RecallResult]:
        results = []
        cfg_derived = self.cfg_mgr.get("path_d_derived", "derived_metric")
        cfg_metric = self.cfg_mgr.get("path_d_derived", "metric")
        cfg_dim = self.cfg_mgr.get("path_d_derived", "dimension")
        cfg_dv = self.cfg_mgr.get("path_d_derived", "dim_value")
        if not cfg_derived.enabled or "derived_index" not in self.indexes:
            log_d.info("path_d disabled or no index")
            return results

        scores, ids = self.indexes["derived_index"].search(
            query_vec, max(cfg_derived.top_k, 30)
        )
        kept = _apply_recall_mode(scores[0], ids[0], cfg_derived)
        log_d.info(f"== 派生指标召回 mode={cfg_derived.recall_mode} top_k={cfg_derived.top_k} "
                   f"th={cfg_derived.threshold}")

        for did, sc in kept:
            d = self.indexes["derived_meta"][did]
            results.append(RecallResult(
                entity_type="derived_metric",
                entity_id=int(d["derived_id"]),
                display_name=d["display_name"],
                description=f"{d.get('description','')} | 计算口径：{d.get('calculation_rule','')}",
                score=sc, source="path_d",
            ))
            log_d.info(f"  [derived] {d['display_name']} score={sc:.4f}")

            deps = self.derived_dependency_mapping.get(d["derived_id"], [])
            metric_added, dim_added, dv_added = 0, 0, 0
            for dep in deps:
                et = dep.get("entity_type")
                allow = False
                if et == "metric" and cfg_metric.enabled and metric_added < cfg_metric.top_k:
                    metric_added += 1; allow = True
                elif et == "dimension" and cfg_dim.enabled and dim_added < cfg_dim.top_k:
                    dim_added += 1; allow = True
                elif et == "dim_value" and cfg_dv.enabled and dv_added < cfg_dv.top_k:
                    dv_added += 1; allow = True
                elif et == "table":
                    allow = True
                if not allow:
                    continue
                eid_real = _entity_id_of(dep)
                results.append(RecallResult(
                    entity_type=et, entity_id=eid_real,
                    display_name=dep.get("display_name", ""),
                    description=dep.get("description", ""),
                    score=sc * 0.85, source="path_d",
                    table_id=dep.get("table_id"),
                    dimension_id=dep.get("dimension_id"),
                ))
                log_d.info(f"      └─ dep {et:10s} {dep.get('display_name','')} score={sc*0.85:.4f}")
        return results

    # ============ 合并去重 ============
    def _merge_and_deduplicate(self, *result_lists) -> List[RecallResult]:
        seen: Dict[Tuple[str, int], RecallResult] = {}
        for lst in result_lists:
            for r in lst:
                if r.entity_id is None:
                    continue
                key = (r.entity_type, r.entity_id)
                if key not in seen or r.score > seen[key].score:
                    seen[key] = r
        merged = sorted(seen.values(), key=lambda x: x.score, reverse=True)
        log_merge.info(f"merged total={len(merged)}; "
                       f"by_type={{ {', '.join(f'{t}:{sum(1 for r in merged if r.entity_type==t)}' for t in ['table','metric','dimension','dim_value','derived_metric'])} }}")
        return merged
