#!/usr/bin/env python3
"""首次或全量重建 PSoC Edge + DEEPCRAFT 知识索引。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import build_all_indexes


def main() -> None:
    summary = build_all_indexes()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
