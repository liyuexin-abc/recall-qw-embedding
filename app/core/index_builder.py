"""
索引构建：从 DB 中读取已 embedding 的实体，构建 5 类 FAISS HNSW 索引：
  1. table_index            -> 表级
  2. topic_index            -> 主题级
  3. table_entity_indexes   -> 按表分组的子索引（指标+维度+维度值）
  4. global_entity_index    -> 全局指标+维度（路径 C 兜底）
  5. derived_index          -> 派生指标 / 业务知识（路径 D）

同时构建辅助映射：
  - topic_entity_mapping       -> {topic_id: [entity_meta, ...]}
  - derived_dependency_mapping -> {derived_id: [entity_meta, ...]}
"""
import json
import numpy as np
import faiss
from typing import Dict, List, Any
from app.core.database import get_db
from app.utils.logger import get_logger

logger = get_logger("index_builder", "index_builder.log")


def _embedding_from_json(s: str):
    if not s:
        return None
    return np.array(json.loads(s), dtype="float32")


def _build_hnsw(embeddings: np.ndarray, dim: int) -> faiss.Index:
    if embeddings is None or len(embeddings) == 0:
        idx = faiss.IndexHNSWFlat(dim, 32, faiss.METRIC_INNER_PRODUCT)
        return idx
    idx = faiss.IndexHNSWFlat(dim, 32, faiss.METRIC_INNER_PRODUCT)
    idx.hnsw.efConstruction = 200
    idx.hnsw.efSearch = 64
    idx.add(embeddings)
    return idx


class RecallIndexBuilder:
    def __init__(self, dim: int = 1024):
        self.dim = dim
        self.db = get_db()

    def build(self) -> Dict[str, Any]:
        logger.info("Building FAISS indexes...")
        indexes: Dict[str, Any] = {}

        # 1. 表级
        rows = self.db.query("SELECT table_id, table_name, display_name, description, embedding_json FROM meta_table")
        embs, metas = [], []
        for r in rows:
            v = _embedding_from_json(r["embedding_json"])
            if v is None: continue
            embs.append(v); metas.append({
                "table_id": r["table_id"], "table_name": r["table_name"],
                "display_name": r["display_name"], "description": r["description"],
            })
        indexes["table_index"] = _build_hnsw(np.stack(embs) if embs else None, self.dim)
        indexes["table_meta"] = metas
        logger.info(f"table_index: {len(embs)} entries")

        # 2. 主题级
        rows = self.db.query("SELECT topic_id, topic_name, description, embedding_json FROM meta_business_topic")
        embs, metas = [], []
        for r in rows:
            v = _embedding_from_json(r["embedding_json"])
            if v is None: continue
            embs.append(v); metas.append({
                "topic_id": r["topic_id"], "topic_name": r["topic_name"],
                "display_name": r["topic_name"], "description": r["description"],
            })
        indexes["topic_index"] = _build_hnsw(np.stack(embs) if embs else None, self.dim)
        indexes["topic_meta"] = metas
        logger.info(f"topic_index: {len(embs)} entries")

        # 3. 按表分组：指标+维度+维度值
        table_entity_indexes = {}
        for tr in self.db.query("SELECT table_id, table_name FROM meta_table"):
            tid = tr["table_id"]
            entities = []
            # 指标
            for r in self.db.query(
                "SELECT m.metric_id, m.metric_name, m.display_name, m.description, "
                "m.synonyms, m.unit, m.caliber_scope, m.embedding_json "
                "FROM meta_metric m JOIN rel_table_metric r ON m.metric_id=r.metric_id "
                "WHERE r.table_id=%s", [tid]):
                v = _embedding_from_json(r["embedding_json"])
                if v is None: continue
                entities.append((v, {
                    "entity_type": "metric", "metric_id": r["metric_id"],
                    "metric_name": r["metric_name"], "display_name": r["display_name"],
                    "description": r["description"], "synonyms": r["synonyms"],
                    "unit": r["unit"], "caliber_scope": r["caliber_scope"],
                    "table_id": tid,
                }))
            # 维度
            for r in self.db.query(
                "SELECT d.dimension_id, d.dimension_name, d.display_name, d.description, "
                "d.synonyms, d.embedding_json "
                "FROM meta_dimension d JOIN rel_table_dimension r ON d.dimension_id=r.dimension_id "
                "WHERE r.table_id=%s", [tid]):
                v = _embedding_from_json(r["embedding_json"])
                if v is None: continue
                entities.append((v, {
                    "entity_type": "dimension", "dimension_id": r["dimension_id"],
                    "dimension_name": r["dimension_name"], "display_name": r["display_name"],
                    "description": r["description"], "synonyms": r["synonyms"],
                    "table_id": tid,
                }))
            # 维度值
            for r in self.db.query(
                "SELECT v.value_id, v.dimension_id, v.value_name, v.display_name, "
                "v.description, v.synonyms, v.embedding_json, d.dimension_name "
                "FROM meta_dimension_value v "
                "JOIN rel_table_dimension_value r ON v.value_id=r.value_id AND r.dimension_id=v.dimension_id "
                "JOIN meta_dimension d ON v.dimension_id=d.dimension_id "
                "WHERE r.table_id=%s", [tid]):
                vec = _embedding_from_json(r["embedding_json"])
                if vec is None: continue
                entities.append((vec, {
                    "entity_type": "dim_value", "value_id": r["value_id"],
                    "dimension_id": r["dimension_id"], "dimension_name": r["dimension_name"],
                    "value_name": r["value_name"], "display_name": r["display_name"],
                    "description": r["description"], "synonyms": r["synonyms"],
                    "table_id": tid,
                }))
            if entities:
                vecs = np.stack([e[0] for e in entities])
                metas = [e[1] for e in entities]
                table_entity_indexes[tid] = {
                    "index": _build_hnsw(vecs, self.dim),
                    "entities": metas,
                }
        indexes["table_entity_indexes"] = table_entity_indexes
        logger.info(f"table_entity_indexes: {len(table_entity_indexes)} tables")

        # 4. 全局实体（仅指标+维度，避免维度值噪声）
        global_metas, global_vecs = [], []
        for r in self.db.query(
            "SELECT m.metric_id, m.metric_name, m.display_name, m.description, "
            "m.synonyms, m.embedding_json, r.table_id "
            "FROM meta_metric m JOIN rel_table_metric r ON m.metric_id=r.metric_id"):
            v = _embedding_from_json(r["embedding_json"])
            if v is None: continue
            global_vecs.append(v); global_metas.append({
                "entity_type": "metric", "metric_id": r["metric_id"],
                "metric_name": r["metric_name"], "display_name": r["display_name"],
                "description": r["description"], "synonyms": r["synonyms"],
                "table_id": r["table_id"],
            })
        for r in self.db.query(
            "SELECT d.dimension_id, d.dimension_name, d.display_name, d.description, "
            "d.synonyms, d.embedding_json, r.table_id "
            "FROM meta_dimension d JOIN rel_table_dimension r ON d.dimension_id=r.dimension_id"):
            v = _embedding_from_json(r["embedding_json"])
            if v is None: continue
            global_vecs.append(v); global_metas.append({
                "entity_type": "dimension", "dimension_id": r["dimension_id"],
                "dimension_name": r["dimension_name"], "display_name": r["display_name"],
                "description": r["description"], "synonyms": r["synonyms"],
                "table_id": r["table_id"],
            })
        if global_vecs:
            indexes["global_entity_index"] = _build_hnsw(np.stack(global_vecs), self.dim)
            indexes["global_entity_meta"] = global_metas
            logger.info(f"global_entity_index: {len(global_vecs)} entries")

        # 5. 派生指标
        rows = self.db.query("SELECT derived_id, derived_name, display_name, description, "
                             "aliases, calculation_rule, embedding_json FROM meta_derived_metric")
        embs, metas = [], []
        for r in rows:
            v = _embedding_from_json(r["embedding_json"])
            if v is None: continue
            embs.append(v); metas.append({
                "entity_type": "derived_metric", "derived_id": r["derived_id"],
                "derived_name": r["derived_name"], "display_name": r["display_name"],
                "description": r["description"], "aliases": r["aliases"],
                "calculation_rule": r["calculation_rule"],
            })
        if embs:
            indexes["derived_index"] = _build_hnsw(np.stack(embs), self.dim)
            indexes["derived_meta"] = metas
            logger.info(f"derived_index: {len(embs)} entries")

        # 主题↔实体映射
        indexes["topic_entity_mapping"] = self._build_topic_entity_mapping()
        # 派生指标依赖映射
        indexes["derived_dependency_mapping"] = self._build_derived_dependency_mapping()

        logger.info(
            f"All indexes built. topic_mappings={len(indexes['topic_entity_mapping'])} "
            f"derived_deps={len(indexes['derived_dependency_mapping'])}"
        )
        return indexes

    def _build_topic_entity_mapping(self):
        result: Dict[int, List[Dict]] = {}
        for r in self.db.query("SELECT topic_id, entity_type, entity_id FROM rel_topic_entity"):
            ent = self._fetch_entity(r["entity_type"], r["entity_id"])
            if ent is None: continue
            result.setdefault(r["topic_id"], []).append(ent)
        return result

    def _build_derived_dependency_mapping(self):
        result: Dict[int, List[Dict]] = {}
        for r in self.db.query("SELECT derived_id, entity_type, entity_id FROM rel_derived_dependency"):
            ent = self._fetch_entity(r["entity_type"], r["entity_id"])
            if ent is None: continue
            result.setdefault(r["derived_id"], []).append(ent)
        return result

    def _fetch_entity(self, entity_type: str, entity_id: int):
        if entity_type == "table":
            r = self.db.query("SELECT table_id, table_name, display_name, description "
                              "FROM meta_table WHERE table_id=%s", [entity_id])
            if r:
                x = r[0]; x["entity_type"] = "table"; return x
        elif entity_type == "metric":
            r = self.db.query("SELECT metric_id, metric_name, display_name, description, "
                              "synonyms, unit FROM meta_metric WHERE metric_id=%s", [entity_id])
            if r:
                x = r[0]; x["entity_type"] = "metric"; return x
        elif entity_type == "dimension":
            r = self.db.query("SELECT dimension_id, dimension_name, display_name, description, "
                              "synonyms FROM meta_dimension WHERE dimension_id=%s", [entity_id])
            if r:
                x = r[0]; x["entity_type"] = "dimension"; return x
        elif entity_type == "dim_value":
            r = self.db.query("SELECT v.value_id, v.dimension_id, v.value_name, v.display_name, "
                              "v.description, v.synonyms, d.dimension_name "
                              "FROM meta_dimension_value v JOIN meta_dimension d "
                              "ON v.dimension_id=d.dimension_id WHERE v.value_id=%s", [entity_id])
            if r:
                x = r[0]; x["entity_type"] = "dim_value"; return x
        return None
