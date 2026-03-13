#!/usr/bin/env python3
"""PSoC Edge + DEEPCRAFT 混合检索入口。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import search_chunks, search_chunks_detailed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="执行结构化混合检索")
    parser.add_argument("query", help="查询语句，支持中文描述性问题")
    parser.add_argument("--top-k", type=int, default=8, help="返回条目数")
    parser.add_argument("--source-type", action="append", help="限制 source_type，可重复传入")
    parser.add_argument("--path-prefix", help="限制路径前缀，例如 knowledge\\ 或 ingest\\html\\")
    parser.add_argument("--platform-tag", action="append", help="限制平台标签，例如 psoc-edge、psoc6")
    parser.add_argument("--tool-tag", action="append", help="限制工具链标签，例如 modustoolbox、device-configurator")
    parser.add_argument("--doc-class", action="append", help="限制文档类别，例如 knowledge_summary、web_mirror")
    parser.add_argument("--evidence-tier", action="append", help="限制证据层级，例如 primary_doc、curated_summary")
    parser.add_argument("--with-plan", action="store_true", help="输出查询改写与意图分析")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    payload = search_chunks_detailed(
        query=args.query,
        top_k=args.top_k,
        source_types=args.source_type,
        path_prefix=args.path_prefix,
        platform_tags=args.platform_tag,
        tool_tags=args.tool_tag,
        doc_classes=args.doc_class,
        evidence_tiers=args.evidence_tier,
    )
    results = payload["results"]
    if args.json:
        print(json.dumps(payload if args.with_plan else results, ensure_ascii=False, indent=2))
        return
    if args.with_plan:
        print("query_variants:")
        for variant in payload["query_variants"]:
            print(f"- {variant}")
        print(f"query_intent: {json.dumps(payload['query_intent'], ensure_ascii=False)}")
        print()
    for index, item in enumerate(results, start=1):
        heading = " / ".join(item.get("heading_path") or [])
        print(f"[{index}] score={item['score']:.4f} rerank={item.get('rerank_score', item['score']):.4f} semantic={item['semantic_score']:.4f} keyword={item['keyword_score']:.4f}")
        print(f"  path: {item['path']}:{item['start_line']}-{item['end_line']}")
        print(f"  title: {item['title']}")
        if heading:
            print(f"  heading: {heading}")
        print(f"  meta: doc_class={item.get('doc_class')} evidence={item.get('evidence_tier')} platforms={item.get('platform_tags')} tools={item.get('tool_tags')}")
        print(f"  matched_terms: {item.get('matched_query_terms', [])}")
        print(f"  snippet: {item['snippet']}")
        print()


if __name__ == "__main__":
    main()
