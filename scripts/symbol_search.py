#!/usr/bin/env python3
"""符号检索入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import search_symbols


def main() -> None:
    parser = argparse.ArgumentParser(description="查找函数、宏、类或 Markdown 标题")
    parser.add_argument("query", help="符号名或关键词")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = search_symbols(args.query, top_k=args.top_k)
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    for index, item in enumerate(results, start=1):
        print(f"[{index}] score={item['score']:.4f} {item['type']} {item['name']}")
        print(f"  path: {item['path']}:{item['line']}")
        print(f"  context: {item['context']}")
        print()


if __name__ == "__main__":
    main()
