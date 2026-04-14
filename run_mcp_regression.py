from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.case_search_playwright import DEFAULT_APP_ID, DEFAULT_BASE_URL as DEFAULT_CASE_BASE_URL, DEFAULT_CDP_URL as DEFAULT_CASE_CDP_URL, run_search as run_case_search
from scripts.community_search_playwright import run_search as run_community_search


DEFAULT_COMMUNITY_BASE_URL = "https://community.infineon.com"


def load_suite(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("cases", [])


def run_case(case: dict, cdp_url: str, community_base_url: str, case_base_url: str, app_id: str) -> dict:
    started = time.perf_counter()
    try:
        if case["mode"] == "community":
            payload = run_community_search(
                cdp_url=cdp_url,
                query=case["query"],
                limit=int(case.get("limit", 5)),
                base_url=community_base_url,
            )
            diagnostics = payload.get("diagnostics", {})
            result_count = len(payload.get("results", []))
            quality = diagnostics.get("result_quality_score", 0.0)
            stop_reason = diagnostics.get("stop_reason", "unknown")
            queries_tried = [case["query"]]
            top_titles = [item.get("title", "") for item in payload.get("results", [])[:3]]
        else:
            payload = run_case_search(
                cdp_url=cdp_url,
                base_url=case_base_url,
                app_id=app_id,
                query=case["query"],
                limit=int(case.get("limit", 5)),
                max_queries=int(case.get("max_queries", 4)),
            )
            diagnostics = payload.get("diagnostics", {})
            result_count = len(payload.get("results", []))
            quality = diagnostics.get("result_quality_score", 0.0)
            stop_reason = diagnostics.get("stop_reason", "unknown")
            queries_tried = payload.get("queries_tried", [])
            top_titles = [item.get("subject", "") for item in payload.get("results", [])[:3]]
        elapsed_ms = diagnostics.get("elapsed_ms") or int((time.perf_counter() - started) * 1000)
        passed = result_count >= int(case.get("min_results", 1)) and stop_reason != "query_errors_only"
        return {
            "case_id": case["id"],
            "mode": case["mode"],
            "query": case["query"],
            "elapsed_ms": elapsed_ms,
            "result_count": result_count,
            "result_quality_score": quality,
            "stop_reason": stop_reason,
            "queries_tried": queries_tried,
            "top_titles": top_titles,
            "passed": passed,
            "error": None,
        }
    except Exception as exc:
        return {
            "case_id": case["id"],
            "mode": case["mode"],
            "query": case["query"],
            "elapsed_ms": int((time.perf_counter() - started) * 1000),
            "result_count": 0,
            "result_quality_score": 0.0,
            "stop_reason": "runner_exception",
            "queries_tried": [],
            "top_titles": [],
            "passed": False,
            "error": str(exc),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run fixed MCP regressions for Community and MSD/Case search.")
    parser.add_argument("--suite", default=str(ROOT / "mcp_regression_suite.json"))
    parser.add_argument("--mode", choices=["all", "community", "case"], default="all")
    parser.add_argument("--cdp-url", default=DEFAULT_CASE_CDP_URL)
    parser.add_argument("--community-base-url", default=DEFAULT_COMMUNITY_BASE_URL)
    parser.add_argument("--case-base-url", default=DEFAULT_CASE_BASE_URL)
    parser.add_argument("--app-id", default=DEFAULT_APP_ID)
    args = parser.parse_args()

    session_id = uuid.uuid4().hex[:12]
    cases = load_suite(Path(args.suite))
    if args.mode != "all":
        cases = [item for item in cases if item["mode"] == args.mode]

    governance_dir = ROOT / "governance"
    governance_dir.mkdir(parents=True, exist_ok=True)
    events_path = governance_dir / "mcp_regression_events.jsonl"
    summary_path = governance_dir / "mcp_regression_last_run.json"

    results = []
    for case in cases:
        event = run_case(case, args.cdp_url, args.community_base_url, args.case_base_url, args.app_id)
        event["session_id"] = session_id
        event["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
        results.append(event)
        with events_path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(event, ensure_ascii=False) + "\n")

    summary = {
        "session_id": session_id,
        "ran_at_utc": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "passed": sum(1 for item in results if item["passed"]),
        "failed": sum(1 for item in results if not item["passed"]),
        "results": results,
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
