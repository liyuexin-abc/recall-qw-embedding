"""
全局配置模块
- LLM/Embedding API（DashScope OpenAI 兼容接口）
- 数据库连接（MySQL 优先，SQLite 兜底）
- 服务参数
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ========== LLM 配置 ==========
LLM_API_KEY = os.getenv("LLM_API_KEY", "sk-bcebd07345bc4c6ca6b38c029d6a9113")
LLM_API_BASE_URL = os.getenv("LLM_API_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3-235b-a22b-instruct-2507")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))

# ========== Embedding 配置 ==========
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", LLM_API_KEY)
EMBEDDING_API_BASE_URL = os.getenv("EMBEDDING_API_BASE_URL", LLM_API_BASE_URL)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
# text-embedding-v4 默认输出 1024 维，可指定 dimensions 参数
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1024"))
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "10"))  # DashScope 单次最多 10 条

# ========== 数据库配置 ==========
# 优先使用 MySQL；连接失败时自动降级到 SQLite
DB_URL = os.getenv("DB_URL", "")
if not DB_URL:
    # 默认 MySQL 配置
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "recall_service")
    DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

# SQLite 兜底地址（当 MySQL 连不上时使用）
SQLITE_FALLBACK_URL = f"sqlite:///{DATA_DIR}/recall_service.db"

# 是否允许自动降级
ALLOW_SQLITE_FALLBACK = os.getenv("ALLOW_SQLITE_FALLBACK", "1") == "1"

# ========== 服务配置 ==========
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# 配置热加载间隔（秒）
CONFIG_REFRESH_INTERVAL = int(os.getenv("CONFIG_REFRESH_INTERVAL", "30"))

# 索引文件路径（持久化）
INDEX_DIR = DATA_DIR / "indexes"
INDEX_DIR.mkdir(parents=True, exist_ok=True)
