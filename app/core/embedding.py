"""
Embedding 客户端 —— 使用 DashScope text-embedding-v4
- 与 OpenAI 接口兼容（自动 L2 归一化）
- 自动批处理（DashScope 单次最多 10 条）
- 支持 query 类型 instruct（DashScope 端区分 query/document）
"""
from typing import List
import numpy as np
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from app import config
from app.utils.logger import get_logger

logger = get_logger("embedding", "embedding.log")


class EmbeddingClient:
    """DashScope text-embedding-v4 调用封装"""

    def __init__(self):
        self.client = OpenAI(
            api_key=config.EMBEDDING_API_KEY,
            base_url=config.EMBEDDING_API_BASE_URL,
        )
        self.model = config.EMBEDDING_MODEL
        self.dim = config.EMBEDDING_DIM
        self.batch_size = config.EMBEDDING_BATCH_SIZE
        logger.info(f"EmbeddingClient init: model={self.model}, dim={self.dim}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
    def _encode_batch(self, texts: List[str]) -> np.ndarray:
        # text-embedding-v4 支持 dimensions 参数
        try:
            resp = self.client.embeddings.create(
                model=self.model,
                input=texts,
                dimensions=self.dim,
                encoding_format="float",
            )
        except TypeError:
            # 旧版 SDK 没有 dimensions 关键字
            resp = self.client.embeddings.create(
                model=self.model,
                input=texts,
            )
        embs = np.array([item.embedding for item in resp.data], dtype=np.float32)
        # L2 归一化（与 FAISS METRIC_INNER_PRODUCT 配合作余弦相似度）
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        embs = embs / norms
        return embs

    def encode(self, texts: List[str], desc: str = "") -> np.ndarray:
        """
        批量编码文本，返回 (N, dim) 的归一化向量
        Args:
            texts: 文本列表
            desc:  日志描述（如 'tables', 'query'）
        """
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)
        all_emb = []
        n = len(texts)
        for i in range(0, n, self.batch_size):
            batch = texts[i:i + self.batch_size]
            try:
                emb = self._encode_batch(batch)
            except Exception as e:
                logger.error(f"encode batch [{i}:{i+len(batch)}] failed: {e}")
                raise
            all_emb.append(emb)
            if n > self.batch_size:
                logger.debug(f"encode {desc} progress: {i+len(batch)}/{n}")
        out = np.concatenate(all_emb, axis=0).astype(np.float32)
        if out.shape[1] != self.dim:
            # 后兜底：若服务端返回了不同维度则直接用返回值并更新 self.dim
            logger.warning(f"encode return dim={out.shape[1]} != configured {self.dim}; using returned dim")
        return out

    def encode_query(self, query: str) -> np.ndarray:
        """对查询文本做单条编码（带 Instruct 前缀，与方案对齐）"""
        instruct_text = (
            "Instruct: 根据用户的数据查询问题，"
            "检索相关的数据表、指标、维度、维度值和业务术语\nQuery: "
            + query
        )
        return self.encode([instruct_text], desc="query")


# 全局单例
_client: EmbeddingClient = None


def get_embedding_client() -> EmbeddingClient:
    global _client
    if _client is None:
        _client = EmbeddingClient()
    return _client
