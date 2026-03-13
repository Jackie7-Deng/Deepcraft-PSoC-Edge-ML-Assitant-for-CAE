#!/usr/bin/env python3
"""基于 text_chunks.jsonl 构建轻量向量索引。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import build_vector_index


def main() -> None:
    meta = build_vector_index()
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
