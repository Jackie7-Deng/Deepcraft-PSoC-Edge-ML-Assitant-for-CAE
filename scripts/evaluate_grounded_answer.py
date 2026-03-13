#!/usr/bin/env python3
"""校验 grounded answer 证据包是否满足最小约束。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import build_grounded_answer_pack

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "grounded_answer_cases.json"
DEFAULT_REPORT = ROOT / "evals" / "grounded_answer_report.json"


def normalize_path(path: str) -> str:
    return path.replace("/", "\\").lower()


def run_case(case: dict) -> dict:
    payload = build_grounded_answer_pack(
        query=case["query"],
        top_k=int(case.get("top_k", 6)),
        min_citations=int(case.get("min_citations", 2)),
        source_types=case.get("source_types"),
        path_prefix=case.get("path_prefix"),
        platform_tags=case.get("platform_tags"),
        tool_tags=case.get("tool_tags"),
        doc_classes=case.get("doc_classes"),
        evidence_tiers=case.get("evidence_tiers"),
    )
    expected_status = case.get("expected_status", "grounded_answer")
    expected_paths = {normalize_path(path) for path in case.get("expected_paths", [])}
    actual_paths = {normalize_path(item["path"]) for item in payload["evidence"]}
    path_hit = not expected_paths or bool(actual_paths & expected_paths)
    ok = payload["status"] == expected_status and path_hit and payload["strong_evidence_count"] >= int(case.get("min_citations", 2))
    return {
        "id": case["id"],
        "query": case["query"],
        "ok": ok,
        "status": payload["status"],
        "strong_evidence_count": payload["strong_evidence_count"],
        "expected_paths": case.get("expected_paths", []),
        "actual_paths": [item["path"] for item in payload["evidence"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="验证 grounded answer 约束")
    parser.add_argument("--cases", default=str(DEFAULT_CASES), help="样例文件路径")
    parser.add_argument("--write-report", action="store_true", help="写入 evals\\grounded_answer_report.json")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    cases = json.loads(Path(args.cases).read_text(encoding="utf-8"))
    case_results = [run_case(case) for case in cases]
    ok_count = sum(1 for case in case_results if case["ok"])
    report = {
        "total_cases": len(case_results),
        "ok_count": ok_count,
        "ok_rate": round(ok_count / len(case_results), 4) if case_results else 0.0,
        "failed_cases": [case for case in case_results if not case["ok"]],
        "cases": case_results,
    }
    if args.write_report:
        DEFAULT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print(f"grounded answer 校验: {report['ok_count']}/{report['total_cases']} 通过，ok_rate={report['ok_rate']:.2%}")
    for case in report["failed_cases"]:
        print(f"- 失败: {case['id']} status={case['status']} strong={case['strong_evidence_count']}")
    if report["failed_cases"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
