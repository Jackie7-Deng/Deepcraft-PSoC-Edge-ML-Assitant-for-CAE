#!/usr/bin/env python3
"""执行当前工作区的检索回归样例。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import search_chunks

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "retrieval_cases.json"
DEFAULT_REPORT = ROOT / "evals" / "retrieval_report.json"


def normalize_path(path: str) -> str:
    return path.replace("/", "\\").lower()


def load_cases(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_hit(results: list[dict], case: dict) -> tuple[bool, str]:
    expected_paths = {normalize_path(path) for path in case.get("expected_paths", [])}
    expected_prefixes = [normalize_path(path) for path in case.get("expected_path_prefixes", [])]
    for item in results:
        current = normalize_path(item["path"])
        if current in expected_paths:
            return True, current
        if any(current.startswith(prefix) for prefix in expected_prefixes):
            return True, current
    return False, ""


def run_case(case: dict) -> dict:
    results = search_chunks(
        query=case["query"],
        top_k=int(case.get("top_k", 5)),
        source_types=case.get("source_types"),
        path_prefix=case.get("path_prefix"),
        platform_tags=case.get("platform_tags"),
        tool_tags=case.get("tool_tags"),
        doc_classes=case.get("doc_classes"),
        evidence_tiers=case.get("evidence_tiers"),
    )
    hit, matched_path = is_hit(results, case)
    return {
        "id": case["id"],
        "query": case["query"],
        "hit": hit,
        "matched_path": matched_path,
        "expected_paths": case.get("expected_paths", []),
        "top_results": [
            {
                "path": item["path"],
                "score": item["score"],
                "doc_class": item.get("doc_class"),
                "evidence_tier": item.get("evidence_tier"),
            }
            for item in results[: min(len(results), 5)]
        ],
    }


def build_report(cases: list[dict]) -> dict:
    case_results = [run_case(case) for case in cases]
    hit_count = sum(1 for case in case_results if case["hit"])
    return {
        "total_cases": len(case_results),
        "hit_count": hit_count,
        "hit_rate": round(hit_count / len(case_results), 4) if case_results else 0.0,
        "failed_cases": [case for case in case_results if not case["hit"]],
        "cases": case_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="执行检索回归样例")
    parser.add_argument("--cases", default=str(DEFAULT_CASES), help="样例文件路径")
    parser.add_argument("--write-report", action="store_true", help="写入 evals\\retrieval_report.json")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    cases = load_cases(Path(args.cases))
    report = build_report(cases)
    if args.write_report:
        DEFAULT_REPORT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print(f"检索回归: {report['hit_count']}/{report['total_cases']} 命中，hit_rate={report['hit_rate']:.2%}")
    for case in report["failed_cases"]:
        print(f"- 失败: {case['id']} -> {case['query']}")
        for item in case["top_results"]:
            print(f"  - {item['path']} score={item['score']:.4f}")
    if report["failed_cases"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
