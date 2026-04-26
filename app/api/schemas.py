"""Pydantic 请求/响应模型"""
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any


# ========== 召回请求 ==========
class RecallRequest(BaseModel):
    query: str = Field(..., description="用户原始 query")
    use_llm_judge: bool = Field(False, description="是否启用 LLM Stage-2 精判")
    parallel: bool = Field(True, description="四路并行执行（默认）")


# ========== 召回结果 ==========
class CandidateItem(BaseModel):
    entity_type: str
    entity_id: int
    display_name: str
    description: str = ""
    score: float
    source: str
    table_id: Optional[int] = None
    dimension_id: Optional[int] = None


class RecallResponse(BaseModel):
    query: str
    clean_query: str
    time_terms: List[str]
    candidates: List[CandidateItem]
    by_path: Dict[str, List[CandidateItem]]
    timings_ms: Dict[str, float]
    llm_judge: Optional[Dict[str, Any]] = None


# ========== 配置 API ==========
class ConfigUpdateRequest(BaseModel):
    recall_mode: Optional[Literal["top_k", "threshold", "hybrid"]] = None
    top_k: Optional[int] = Field(None, ge=1, le=500)
    threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    enabled: Optional[bool] = None
    description: Optional[str] = None


class BatchUpdateItem(BaseModel):
    path_name: str
    entity_type: str
    recall_mode: Optional[Literal["top_k", "threshold", "hybrid"]] = None
    top_k: Optional[int] = Field(None, ge=1, le=500)
    threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    enabled: Optional[bool] = None


class ConfigResponse(BaseModel):
    path_name: str
    entity_type: str
    recall_mode: str
    top_k: int
    threshold: float
    enabled: bool
    description: Optional[str] = None


# ========== 元数据更新 ==========
class MetadataReloadResponse(BaseModel):
    status: str
    counts: Dict[str, int]
    elapsed_seconds: float
