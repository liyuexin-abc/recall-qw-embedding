"""FastAPI 路由：召回、配置、元数据"""
import time
from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any

from app.api.schemas import (
    RecallRequest, RecallResponse, CandidateItem,
    ConfigUpdateRequest, BatchUpdateItem, ConfigResponse,
    MetadataReloadResponse,
)
from app.services.recall_service import RecallService
from app.services.llm_judge import LLMJudge
from app.services.metadata_processor import MetadataProcessor
from app.core.index_builder import RecallIndexBuilder
from app.core.config_manager import get_config_manager
from app.utils.logger import get_logger
from app import config

logger = get_logger("api", "api.log")

router = APIRouter()


# 这些会在 main.py 启动时填充
_state: Dict[str, Any] = {}


def init_state(recall_service: RecallService, llm_judge: LLMJudge):
    _state["recall"] = recall_service
    _state["judge"] = llm_judge


# ----------------------------------------------------------
# 健康检查
# ----------------------------------------------------------
@router.get("/health")
def health():
    return {"status": "ok", "ts": int(time.time())}


# ----------------------------------------------------------
# 1. 召回主接口
# ----------------------------------------------------------
@router.post("/api/recall", response_model=RecallResponse)
def recall(req: RecallRequest):
    rs: RecallService = _state.get("recall")
    if rs is None:
        raise HTTPException(503, "Recall service not ready")
    out = rs.recall(req.query, parallel=req.parallel)

    if req.use_llm_judge:
        judge: LLMJudge = _state["judge"]
        try:
            judgement = judge.judge(req.query, out["candidates"])
            out["llm_judge"] = judgement
        except Exception as e:
            logger.error(f"LLM judge fail: {e}")
            out["llm_judge"] = {"error": str(e)}

    return out


@router.get("/api/recall")
def recall_get(query: str, use_llm_judge: bool = False):
    """GET 方式调用，便于 curl 测试"""
    return recall(RecallRequest(query=query, use_llm_judge=use_llm_judge))


# ----------------------------------------------------------
# 2. 配置管理（动态调整召回参数）
# ----------------------------------------------------------
@router.get("/api/recall/config", response_model=List[ConfigResponse])
def list_configs():
    mgr = get_config_manager()
    return [
        ConfigResponse(
            path_name=c.path_name, entity_type=c.entity_type,
            recall_mode=c.recall_mode, top_k=c.top_k,
            threshold=c.threshold, enabled=c.enabled,
            description=c.description,
        ) for c in mgr.list_all()
    ]


@router.get("/api/recall/config/{path_name}/{entity_type}", response_model=ConfigResponse)
def get_config(path_name: str, entity_type: str):
    mgr = get_config_manager()
    cfg = mgr.get(path_name, entity_type)
    return ConfigResponse(
        path_name=cfg.path_name, entity_type=cfg.entity_type,
        recall_mode=cfg.recall_mode, top_k=cfg.top_k,
        threshold=cfg.threshold, enabled=cfg.enabled,
        description=cfg.description,
    )


@router.put("/api/recall/config/{path_name}/{entity_type}", response_model=ConfigResponse)
def update_config(path_name: str, entity_type: str, req: ConfigUpdateRequest):
    mgr = get_config_manager()
    upd = req.model_dump(exclude_none=True)
    if not upd:
        raise HTTPException(400, "至少需要提供一个待更新字段")
    try:
        cfg = mgr.update(path_name, entity_type, **upd)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return ConfigResponse(
        path_name=cfg.path_name, entity_type=cfg.entity_type,
        recall_mode=cfg.recall_mode, top_k=cfg.top_k,
        threshold=cfg.threshold, enabled=cfg.enabled,
        description=cfg.description,
    )


@router.post("/api/recall/config/batch", response_model=List[ConfigResponse])
def batch_update_configs(items: List[BatchUpdateItem]):
    mgr = get_config_manager()
    results = []
    for item in items:
        upd = item.model_dump(exclude={"path_name", "entity_type"}, exclude_none=True)
        if not upd:
            continue
        try:
            cfg = mgr.update(item.path_name, item.entity_type, **upd)
            results.append(ConfigResponse(
                path_name=cfg.path_name, entity_type=cfg.entity_type,
                recall_mode=cfg.recall_mode, top_k=cfg.top_k,
                threshold=cfg.threshold, enabled=cfg.enabled,
                description=cfg.description,
            ))
        except ValueError as e:
            raise HTTPException(400, f"{item.path_name}/{item.entity_type}: {e}")
    return results


@router.post("/api/recall/config/reload")
def reload_configs():
    mgr = get_config_manager()
    mgr.reload()
    return {"status": "ok", "count": len(mgr._configs)}


# ----------------------------------------------------------
# 3. 元数据管理
# ----------------------------------------------------------
@router.post("/api/metadata/rebuild", response_model=MetadataReloadResponse)
def rebuild_metadata(encode: bool = True, raw_path: str = None):
    """
    全量重建元数据：
    - 读取 raw_meta.json
    - 推断关系，生成 embedding_text
    - 编码（encode=True 时）
    - 重建 FAISS 索引并更新 RecallService
    """
    t0 = time.time()
    proc = MetadataProcessor()
    counts = proc.process(raw_path=raw_path, encode_embeddings=encode)

    # 重建索引
    builder = RecallIndexBuilder(dim=config.EMBEDDING_DIM)
    new_indexes = builder.build()
    rs: RecallService = _state["recall"]
    rs.update_indexes(new_indexes)

    elapsed = time.time() - t0
    logger.info(f"Metadata rebuilt in {elapsed:.1f}s, counts={counts}")
    return MetadataReloadResponse(
        status="ok", counts=counts, elapsed_seconds=round(elapsed, 2)
    )


@router.post("/api/metadata/reload-index")
def reload_index():
    """仅重新构建索引（不重新写库），用于元数据已落库但需要刷索引"""
    t0 = time.time()
    builder = RecallIndexBuilder(dim=config.EMBEDDING_DIM)
    new_indexes = builder.build()
    rs: RecallService = _state["recall"]
    rs.update_indexes(new_indexes)
    return {"status": "ok", "elapsed": round(time.time() - t0, 2)}


@router.get("/api/metadata/stats")
def metadata_stats():
    from app.core.database import get_db
    db = get_db()
    return {
        "tables":         db.query("SELECT COUNT(*) AS c FROM meta_table")[0]["c"],
        "metrics":        db.query("SELECT COUNT(*) AS c FROM meta_metric")[0]["c"],
        "dimensions":     db.query("SELECT COUNT(*) AS c FROM meta_dimension")[0]["c"],
        "dim_values":     db.query("SELECT COUNT(*) AS c FROM meta_dimension_value")[0]["c"],
        "topics":         db.query("SELECT COUNT(*) AS c FROM meta_business_topic")[0]["c"],
        "derived_metrics":db.query("SELECT COUNT(*) AS c FROM meta_derived_metric")[0]["c"],
    }


@router.get("/api/metadata/list/{entity_type}")
def list_metadata(entity_type: str, limit: int = 100):
    from app.core.database import get_db
    db = get_db()
    table_map = {
        "table": ("meta_table", "table_id, table_name, display_name, description"),
        "metric": ("meta_metric", "metric_id, metric_name, display_name, description, unit, caliber_scope"),
        "dimension": ("meta_dimension", "dimension_id, dimension_name, display_name, description, synonyms"),
        "dim_value": ("meta_dimension_value", "value_id, dimension_id, value_name, display_name"),
        "topic": ("meta_business_topic", "topic_id, topic_name, description"),
        "derived_metric": ("meta_derived_metric", "derived_id, derived_name, display_name, calculation_rule"),
    }
    if entity_type not in table_map:
        raise HTTPException(400, f"Unknown entity_type: {entity_type}")
    table, cols = table_map[entity_type]
    rows = db.query(f"SELECT {cols} FROM {table} LIMIT {int(limit)}")
    return {"count": len(rows), "items": rows}
