#!/usr/bin/env python3
"""生成带证据约束的回答证据包。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import build_grounded_answer_pack


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成 grounded answer 证据包")
    parser.add_argument("query", help="自然语言问题")
    parser.add_argument("--top-k", type=int, default=6, help="返回证据条数")
    parser.add_argument("--min-citations", type=int, default=2, help="建议最少引用条数")
    parser.add_argument("--source-type", action="append", help="限制 source_type，可重复传入")
    parser.add_argument("--path-prefix", help="限制路径前缀，例如 knowledge\\")
    parser.add_argument("--platform-tag", action="append", help="限制平台标签")
    parser.add_argument("--tool-tag", action="append", help="限制工具链标签")
    parser.add_argument("--doc-class", action="append", help="限制文档类别")
    parser.add_argument("--evidence-tier", action="append", help="限制证据层级")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    payload = build_grounded_answer_pack(
        query=args.query,
        top_k=args.top_k,
        min_citations=args.min_citations,
        source_types=args.source_type,
        path_prefix=args.path_prefix,
        platform_tags=args.platform_tag,
        tool_tags=args.tool_tag,
        doc_classes=args.doc_class,
        evidence_tiers=args.evidence_tier,
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"status={payload['status']} strong_evidence={payload['strong_evidence_count']}")
    print("query_variants:")
    for variant in payload["query_plan"]["variants"]:
        print(f"- {variant}")
    print("evidence:")
    for item in payload["evidence"]:
        print(f"- {item['citation']} score={item.get('rerank_score', item.get('score'))}")
        print(f"  {item['snippet']}")


if __name__ == "__main__":
    main()
