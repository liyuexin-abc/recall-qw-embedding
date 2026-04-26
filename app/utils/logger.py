"""
统一日志工具
- 不同模块使用独立 logger
- 召回路径分别落不同日志文件，便于排障
"""
import logging
import logging.handlers
import sys
from pathlib import Path
from app.config import LOG_DIR, LOG_LEVEL


_inited = set()


def get_logger(name: str, file_name: str = None) -> logging.Logger:
    """
    Args:
        name: logger 名称（也作为输出 prefix）
        file_name: 单独写入的日志文件名（不含路径），不指定则只写主日志
    """
    logger = logging.getLogger(name)
    if name in _inited:
        return logger

    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)-22s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 主日志文件（按天滚动）
    main_file = LOG_DIR / "recall_service.log"
    main_handler = logging.handlers.TimedRotatingFileHandler(
        main_file, when="midnight", backupCount=14, encoding="utf-8"
    )
    main_handler.setFormatter(fmt)
    logger.addHandler(main_handler)

    # 模块专属日志文件
    if file_name:
        f = LOG_DIR / file_name
        h = logging.handlers.TimedRotatingFileHandler(
            f, when="midnight", backupCount=14, encoding="utf-8"
        )
        h.setFormatter(fmt)
        logger.addHandler(h)

    _inited.add(name)
    return logger


# 各召回路径的专属 logger，便于单独查看
def path_logger(path_name: str) -> logging.Logger:
    """返回某个召回路径专属的 logger（独立日志文件）"""
    file_map = {
        "path_a": "path_a.log",
        "path_b": "path_b.log",
        "path_c": "path_c.log",
        "path_d": "path_d.log",
        "merge": "merge.log",
        "judge": "judge.log",
    }
    return get_logger(f"recall.{path_name}", file_map.get(path_name, f"{path_name}.log"))
