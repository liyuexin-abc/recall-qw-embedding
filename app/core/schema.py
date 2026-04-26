"""
建表 DDL —— 与技术方案 2.1 完全对齐
适配 MySQL / SQLite（自动按 backend 转换 AUTO_INCREMENT、JSON、ON UPDATE 等差异）
"""
from sqlalchemy import text
from app.core.database import ENGINE, DB_BACKEND
from app.utils.logger import get_logger

logger = get_logger("schema", "db.log")


DDL_MYSQL = """
CREATE TABLE IF NOT EXISTS meta_business_topic (
  topic_id        BIGINT PRIMARY KEY AUTO_INCREMENT,
  topic_name      VARCHAR(100)  NOT NULL,
  parent_id       BIGINT        DEFAULT NULL,
  topic_level     TINYINT       NOT NULL,
  description     TEXT          NOT NULL,
  typical_queries TEXT,
  embedding_text  TEXT          NOT NULL,
  embedding_json  JSON          NULL,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_topic_name(topic_name),
  INDEX idx_parent(parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS meta_table (
  table_id        BIGINT PRIMARY KEY AUTO_INCREMENT,
  table_name      VARCHAR(100)  NOT NULL UNIQUE,
  display_name    VARCHAR(100)  NOT NULL,
  description     TEXT          NOT NULL,
  embedding_text  TEXT          NOT NULL,
  embedding_json  JSON          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS meta_metric (
  metric_id       BIGINT PRIMARY KEY AUTO_INCREMENT,
  metric_name     VARCHAR(150)  NOT NULL,
  display_name    VARCHAR(150)  NOT NULL,
  description     TEXT          NOT NULL,
  synonyms        VARCHAR(500),
  calculation     VARCHAR(500),
  unit            VARCHAR(50),
  caliber_scope   VARCHAR(20)   DEFAULT 'none',
  embedding_text  TEXT          NOT NULL,
  embedding_json  JSON          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_metric_name(metric_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS meta_dimension (
  dimension_id    BIGINT PRIMARY KEY AUTO_INCREMENT,
  dimension_name  VARCHAR(150)  NOT NULL,
  display_name    VARCHAR(150)  NOT NULL,
  description     TEXT          NOT NULL,
  synonyms        VARCHAR(500),
  embedding_text  TEXT          NOT NULL,
  embedding_json  JSON          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_dim_name(dimension_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS meta_dimension_value (
  value_id        BIGINT PRIMARY KEY AUTO_INCREMENT,
  dimension_id    BIGINT        NOT NULL,
  value_name      VARCHAR(200)  NOT NULL,
  display_name    VARCHAR(200)  NOT NULL,
  description     TEXT,
  synonyms        VARCHAR(500),
  embedding_text  TEXT          NOT NULL,
  embedding_json  JSON          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_dim_id(dimension_id),
  INDEX idx_value_name(value_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS meta_derived_metric (
  derived_id      BIGINT PRIMARY KEY AUTO_INCREMENT,
  derived_name    VARCHAR(150)  NOT NULL,
  display_name    VARCHAR(150)  NOT NULL,
  description     TEXT          NOT NULL,
  aliases         VARCHAR(500),
  calculation_rule TEXT         NOT NULL,
  knowledge_type  VARCHAR(30)   DEFAULT 'derived_metric',
  embedding_text  TEXT          NOT NULL,
  embedding_json  JSON          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_derived_name(derived_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rel_derived_dependency (
  derived_id      BIGINT NOT NULL,
  entity_type     VARCHAR(30) NOT NULL,
  entity_id       BIGINT NOT NULL,
  PRIMARY KEY (derived_id, entity_type, entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rel_topic_entity (
  topic_id        BIGINT NOT NULL,
  entity_type     VARCHAR(30) NOT NULL,
  entity_id       BIGINT NOT NULL,
  PRIMARY KEY (topic_id, entity_type, entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rel_table_metric (
  table_id BIGINT NOT NULL,
  metric_id BIGINT NOT NULL,
  PRIMARY KEY (table_id, metric_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rel_table_dimension (
  table_id BIGINT NOT NULL,
  dimension_id BIGINT NOT NULL,
  PRIMARY KEY (table_id, dimension_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rel_table_dimension_value (
  table_id        BIGINT NOT NULL,
  dimension_id    BIGINT NOT NULL,
  value_id        BIGINT NOT NULL,
  PRIMARY KEY (table_id, dimension_id, value_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS recall_config (
  config_id       BIGINT PRIMARY KEY AUTO_INCREMENT,
  path_name       VARCHAR(50)  NOT NULL,
  entity_type     VARCHAR(30)  NOT NULL,
  recall_mode     VARCHAR(20)  NOT NULL DEFAULT 'top_k',
  top_k           INT          NOT NULL DEFAULT 20,
  threshold       DECIMAL(5,4) NOT NULL DEFAULT 0.5000,
  enabled         TINYINT      NOT NULL DEFAULT 1,
  description     VARCHAR(200),
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  updated_by      VARCHAR(50),
  UNIQUE KEY uk_path_entity(path_name, entity_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


DDL_SQLITE = """
CREATE TABLE IF NOT EXISTS meta_business_topic (
  topic_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  topic_name      VARCHAR(100)  NOT NULL,
  parent_id       INTEGER       DEFAULT NULL,
  topic_level     INTEGER       NOT NULL,
  description     TEXT          NOT NULL,
  typical_queries TEXT,
  embedding_text  TEXT          NOT NULL,
  embedding_json  TEXT          NULL,
  created_at      DATETIME      DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_topic_name ON meta_business_topic(topic_name);
CREATE INDEX IF NOT EXISTS idx_topic_parent ON meta_business_topic(parent_id);

CREATE TABLE IF NOT EXISTS meta_table (
  table_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  table_name      VARCHAR(100)  NOT NULL UNIQUE,
  display_name    VARCHAR(100)  NOT NULL,
  description     TEXT          NOT NULL,
  embedding_text  TEXT          NOT NULL,
  embedding_json  TEXT          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS meta_metric (
  metric_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  metric_name     VARCHAR(150)  NOT NULL,
  display_name    VARCHAR(150)  NOT NULL,
  description     TEXT          NOT NULL,
  synonyms        VARCHAR(500),
  calculation     VARCHAR(500),
  unit            VARCHAR(50),
  caliber_scope   VARCHAR(20)   DEFAULT 'none',
  embedding_text  TEXT          NOT NULL,
  embedding_json  TEXT          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_metric_name ON meta_metric(metric_name);

CREATE TABLE IF NOT EXISTS meta_dimension (
  dimension_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  dimension_name  VARCHAR(150)  NOT NULL,
  display_name    VARCHAR(150)  NOT NULL,
  description     TEXT          NOT NULL,
  synonyms        VARCHAR(500),
  embedding_text  TEXT          NOT NULL,
  embedding_json  TEXT          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_dim_name ON meta_dimension(dimension_name);

CREATE TABLE IF NOT EXISTS meta_dimension_value (
  value_id        INTEGER PRIMARY KEY AUTOINCREMENT,
  dimension_id    INTEGER       NOT NULL,
  value_name      VARCHAR(200)  NOT NULL,
  display_name    VARCHAR(200)  NOT NULL,
  description     TEXT,
  synonyms        VARCHAR(500),
  embedding_text  TEXT          NOT NULL,
  embedding_json  TEXT          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_dim_id ON meta_dimension_value(dimension_id);
CREATE INDEX IF NOT EXISTS idx_value_name ON meta_dimension_value(value_name);

CREATE TABLE IF NOT EXISTS meta_derived_metric (
  derived_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  derived_name    VARCHAR(150)  NOT NULL,
  display_name    VARCHAR(150)  NOT NULL,
  description     TEXT          NOT NULL,
  aliases         VARCHAR(500),
  calculation_rule TEXT         NOT NULL,
  knowledge_type  VARCHAR(30)   DEFAULT 'derived_metric',
  embedding_text  TEXT          NOT NULL,
  embedding_json  TEXT          NULL,
  created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_derived_name ON meta_derived_metric(derived_name);

CREATE TABLE IF NOT EXISTS rel_derived_dependency (
  derived_id      INTEGER NOT NULL,
  entity_type     VARCHAR(30) NOT NULL,
  entity_id       INTEGER NOT NULL,
  PRIMARY KEY (derived_id, entity_type, entity_id)
);

CREATE TABLE IF NOT EXISTS rel_topic_entity (
  topic_id        INTEGER NOT NULL,
  entity_type     VARCHAR(30) NOT NULL,
  entity_id       INTEGER NOT NULL,
  PRIMARY KEY (topic_id, entity_type, entity_id)
);

CREATE TABLE IF NOT EXISTS rel_table_metric (
  table_id INTEGER NOT NULL,
  metric_id INTEGER NOT NULL,
  PRIMARY KEY (table_id, metric_id)
);

CREATE TABLE IF NOT EXISTS rel_table_dimension (
  table_id INTEGER NOT NULL,
  dimension_id INTEGER NOT NULL,
  PRIMARY KEY (table_id, dimension_id)
);

CREATE TABLE IF NOT EXISTS rel_table_dimension_value (
  table_id        INTEGER NOT NULL,
  dimension_id    INTEGER NOT NULL,
  value_id        INTEGER NOT NULL,
  PRIMARY KEY (table_id, dimension_id, value_id)
);

CREATE TABLE IF NOT EXISTS recall_config (
  config_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  path_name       VARCHAR(50)  NOT NULL,
  entity_type     VARCHAR(30)  NOT NULL,
  recall_mode     VARCHAR(20)  NOT NULL DEFAULT 'top_k',
  top_k           INTEGER      NOT NULL DEFAULT 20,
  threshold       REAL         NOT NULL DEFAULT 0.5,
  enabled         INTEGER      NOT NULL DEFAULT 1,
  description     VARCHAR(200),
  updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_by      VARCHAR(50),
  UNIQUE (path_name, entity_type)
);
"""


DEFAULT_RECALL_CONFIGS = [
    ('path_a_table',     'table',          'top_k',     3,   0.5000, '路径A第一阶段：表级召回，默认3张表'),
    ('path_a_entity',    'metric',         'top_k',     20,  0.5500, '路径A第二阶段：表内指标召回'),
    ('path_a_entity',    'dimension',      'top_k',     20,  0.5500, '路径A第二阶段：表内维度召回'),
    ('path_a_entity',    'dim_value',      'top_k',     20,  0.5500, '路径A第二阶段：表内维度值召回'),
    ('path_b_topic',     'topic',          'threshold', 5,   0.6000, '路径B：主题召回，按阈值过滤'),
    ('path_c_global',    'metric',         'top_k',     20,  0.5000, '路径C：全局指标向量召回'),
    ('path_c_global',    'dimension',      'top_k',     20,  0.5000, '路径C：全局维度向量召回'),
    ('path_d_derived',   'derived_metric', 'hybrid',    10,  0.5500, '路径D：派生指标召回'),
    ('path_d_derived',   'metric',         'top_k',     20,  0.0000, '路径D：依赖指标随派生指标召回'),
    ('path_d_derived',   'dimension',      'top_k',     20,  0.0000, '路径D：依赖维度随派生指标召回'),
    ('path_d_derived',   'dim_value',      'top_k',     20,  0.0000, '路径D：依赖维度值随派生指标召回'),
]


def init_schema():
    ddl = DDL_SQLITE if DB_BACKEND == "sqlite" else DDL_MYSQL
    statements = [s.strip() for s in ddl.split(";") if s.strip()]
    with ENGINE.begin() as conn:
        for s in statements:
            try:
                conn.execute(text(s))
            except Exception as e:
                logger.error(f"DDL execute fail: {s[:80]}... err={e}")
                raise
    logger.info(f"Schema initialized on {DB_BACKEND} ({len(statements)} stmts)")

    with ENGINE.begin() as conn:
        rs = conn.execute(text("SELECT COUNT(*) AS c FROM recall_config"))
        n = rs.scalar()
        if n == 0:
            for path_name, entity_type, mode, k, th, desc in DEFAULT_RECALL_CONFIGS:
                conn.execute(text(
                    "INSERT INTO recall_config (path_name, entity_type, recall_mode, top_k, threshold, description) "
                    "VALUES (:p,:e,:m,:k,:t,:d)"
                ), dict(p=path_name, e=entity_type, m=mode, k=k, t=th, d=desc))
            logger.info(f"Inserted {len(DEFAULT_RECALL_CONFIGS)} default recall configs")


if __name__ == "__main__":
    init_schema()
