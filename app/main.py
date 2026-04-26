"""
FastAPI 应用入口
启动顺序：
  1. 初始化数据库（schema 建表）
  2. 加载召回配置
  3. 构建/加载 FAISS 索引
  4. 注入 RecallService 到 API state
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app import config
from app.core.schema import init_schema
from app.core.config_manager import get_config_manager
from app.core.embedding import get_embedding_client
from app.core.index_builder import RecallIndexBuilder
from app.services.recall_service import RecallService
from app.services.llm_judge import LLMJudge
from app.api.endpoints import router, init_state
from app.utils.logger import get_logger

logger = get_logger("main", "main.log")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("====== 召回服务启动 ======")
    init_schema()
    cfg_mgr = get_config_manager()
    embed = get_embedding_client()

    # 检查是否已经有元数据；没有则提示需要先执行 rebuild
    from app.core.database import get_db
    db = get_db()
    n_tables = db.query("SELECT COUNT(*) AS c FROM meta_table")[0]["c"]
    if n_tables == 0:
        logger.warning("No metadata loaded. Please POST /api/metadata/rebuild to bootstrap")
        indexes = {}
    else:
        builder = RecallIndexBuilder(dim=config.EMBEDDING_DIM)
        indexes = builder.build()
        logger.info(f"Indexes built: {list(indexes.keys())}")

    recall_service = RecallService(
        embed_client=embed, indexes=indexes, config_manager=cfg_mgr,
    )
    judge = LLMJudge()
    init_state(recall_service, judge)

    logger.info("====== Service Ready ======")
    yield
    logger.info("====== Service Shutdown ======")


app = FastAPI(
    title="智能问数召回服务",
    version="1.0.0",
    description="基于 DashScope text-embedding-v4 的四路并行召回服务（路径 A/B/C/D）",
    lifespan=lifespan,
)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=config.HOST, port=config.PORT, log_level=config.LOG_LEVEL.lower())
