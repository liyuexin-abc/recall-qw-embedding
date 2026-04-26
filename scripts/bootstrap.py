"""
项目初始化脚本：
  1. 建表
  2. 处理元数据并落库
  3. 编码所有 embedding 并写入 embedding_json
  4. 构建索引（验证完整性）

使用：
  cd /home/user/webapp && python scripts/bootstrap.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.schema import init_schema
from app.services.metadata_processor import MetadataProcessor
from app.core.index_builder import RecallIndexBuilder
from app import config


def main():
    print("=" * 60)
    print("Step 1: init schema")
    print("=" * 60)
    init_schema()

    print("=" * 60)
    print("Step 2: process metadata + encode embeddings")
    print("=" * 60)
    proc = MetadataProcessor()
    counts = proc.process(encode_embeddings=True)
    print("Counts:", counts)

    print("=" * 60)
    print("Step 3: build indexes")
    print("=" * 60)
    builder = RecallIndexBuilder(dim=config.EMBEDDING_DIM)
    indexes = builder.build()
    print("Indexes keys:", list(indexes.keys()))

    print("=" * 60)
    print("Bootstrap done.")


if __name__ == "__main__":
    main()
