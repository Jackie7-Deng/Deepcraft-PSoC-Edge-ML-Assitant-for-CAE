from __future__ import annotations

import argparse
import json
import re
import sys
import time
from typing import Any
from urllib.parse import quote
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.search_utils import (
    build_case_query_variants_from_problem,
    normalize_external_search_query,
    score_case_result,
    score_result_set_quality,
)


DEFAULT_CDP_URL = "http://127.0.0.1:9222"
DEFAULT_APP_ID = "4d4c3d73-64de-ec11-bb3c-002248810ede"
DEFAULT_BASE_URL = "https://ifxcasemanagement.crm4.dynamics.com"
SEARCH_TIME_BUDGET_SEC = 75
STALE_QUERY_LIMIT = 2
EARLY_STOP_QUALITY = 0.72
EARLY_STOP_RESULTS = 3
SEARCH_INPUT_SELECTORS = [
    "input[placeholder='Search']",
    "input[title='Search']",
    "input[placeholder*='Search']",
    "input[title*='Search']",
    "input[type='text']",
]


def pick_context(browser):
    if browser.contexts:
        return browser.contexts[0]
    raise RuntimeError("未找到可用浏览器上下文，请先启动带远程调试端口的 Edge/Chrome。")


def build_search_url(base_url: str, app_id: str, query: str) -> str:
    encoded = quote(normalize_external_search_query(query), safe="")
    return f"{base_url}/main.aspx?appid={app_id}&pagetype=search&searchText={encoded}&searchType=0"


def get_body_text(page, timeout: int = 3000) -> str:
    return page.locator("body").inner_text(timeout=timeout)


def is_login_page(body: str, url: str) -> bool:
    body = body or ""
    url = url or ""
    return ("login.microsoftonline.com" in url) or ("Sign in" in body and "Microsoft" in body)


def has_search_results(body: str) -> bool:
    body = body or ""
    return (
        ("Search results" in body or "Tech Support Hub" in body or "Top results" in body)
        and "Cases(" in body
    )


def has_cases_grid(page, body: str | None = None) -> bool:
    body = body or ""
    if "Case number" in body and "Subject" in body and "Description" in body:
        return True
    selectors = [
        '[role="gridcell"][col-id="ticketnumber"]',
        '[role="gridcell"][col-id="description"]',
        '[role="gridcell"][col-id="customerid"]',
    ]
    for selector in selectors:
        locator = page.locator(selector)
        try:
            if locator.count() > 0:
                return True
        except Exception:
            pass
    return False


def wait_for_results(page, timeout_seconds: int = 25) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        body = get_body_text(page, timeout=3000)
        if is_login_page(body, page.url):
            raise RuntimeError("当前页面落到了登录页，说明浏览器会话还没有进入已登录状态。")
        if has_search_results(body):
            return
        page.wait_for_timeout(1000)
    raise RuntimeError("已进入 case 搜索页，但未等到结果区域加载完成。")


def switch_to_cases_view(page) -> None:
    body = get_body_text(page, timeout=5000)
    if has_cases_grid(page, body):
        return

    attempts: list[str] = []
    locators = [
        ("role-tab", page.get_by_role("tab", name=re.compile(r"^Cases(\(\d+\))?$", re.IGNORECASE)).first),
        ("role-button", page.get_by_role("button", name=re.compile(r"^Cases(\(\d+\))?$", re.IGNORECASE)).first),
        ("text", page.get_by_text(re.compile(r"^Cases(\(\d+\))?$", re.IGNORECASE)).first),
    ]

    for name, locator in locators:
        try:
            locator.click(timeout=4000)
            page.wait_for_timeout(4000)
            body = get_body_text(page, timeout=5000)
            if has_cases_grid(page, body):
                return
        except Exception as exc:
            attempts.append(f"{name}-click: {exc}")

        try:
            locator.click(timeout=4000, force=True)
            page.wait_for_timeout(4000)
            body = get_body_text(page, timeout=5000)
            if has_cases_grid(page, body):
                return
        except Exception as exc:
            attempts.append(f"{name}-force: {exc}")

        try:
            locator.evaluate("(el) => el.click()")
            page.wait_for_timeout(4000)
            body = get_body_text(page, timeout=5000)
            if has_cases_grid(page, body):
                return
        except Exception as exc:
            attempts.append(f"{name}-js: {exc}")

    raise RuntimeError(" ; ".join(attempts))


def find_search_box(page):
    for selector in SEARCH_INPUT_SELECTORS:
        locator = page.locator(selector)
        try:
            if locator.count() > 0 and locator.first.is_visible():
                return locator.first
        except Exception:
            pass
    return None


def submit_search_via_ui(page, query: str) -> None:
    query = normalize_external_search_query(query)
    box = find_search_box(page)
    if box is None:
        raise RuntimeError("未找到 case 搜索框，无法执行页面内搜索回退。")
    box.click(timeout=3000)
    box.fill(query, timeout=3000)
    box.press("Enter")
    page.wait_for_timeout(5000)


def open_search_results(page, base_url: str, app_id: str, query: str) -> None:
    query = normalize_external_search_query(query)
    search_url = build_search_url(base_url, app_id, query)
    attempts: list[str] = []

    try:
        page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(8000)
        wait_for_results(page)
        return
    except Exception as exc:
        attempts.append(f"url-goto: {exc}")

    try:
        page.reload(wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(8000)
        wait_for_results(page)
        return
    except Exception as exc:
        attempts.append(f"reload: {exc}")

    try:
        submit_search_via_ui(page, query)
        wait_for_results(page)
        return
    except Exception as exc:
        attempts.append(f"ui-search: {exc}")

    raise RuntimeError(" ; ".join(attempts))


def extract_case_rows(page, base_url: str, app_id: str, limit: int) -> list[dict[str, Any]]:
    rows = page.evaluate(
        """
        (limit) => {
          const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim();
          const visible = (el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
          };
          const results = [];
          const seen = new Set();

          for (const button of document.querySelectorAll('button')) {
            if (!visible(button)) continue;
            const subject = normalize(button.getAttribute('title') || button.innerText || button.textContent || '');
            if (!subject) continue;

            const row = button.closest('[role="row"][row-id]');
            if (!row) continue;

            const cells = {};
            for (const cell of row.querySelectorAll('[role="gridcell"][col-id]')) {
              cells[cell.getAttribute('col-id')] = normalize(cell.innerText || cell.textContent || '');
            }

            const caseNumber = cells.ticketnumber || '';
            if (!caseNumber || !/^IFX-/i.test(caseNumber)) continue;

            const rowId = row.getAttribute('row-id') || '';
            if (!rowId || seen.has(rowId)) continue;
            seen.add(rowId);

            results.push({
              row_id: rowId,
              subject,
              contact: cells.ifx_ccm_primarycontactid || '',
              case_number: caseNumber,
              external_reference_number: cells.ifx_externalreferencenumber || '',
              account_location: cells.customerid || '',
              description: cells.description || '',
            });

            if (results.length >= limit) break;
          }

          return results;
        }
        """,
        limit,
    )

    for item in rows:
        row_id = item["row_id"]
        item["detail_url"] = (
            f"{base_url}/main.aspx?appid={app_id}&pagetype=entityrecord&etn=incident&id={row_id}"
        )
    return rows


def extract_result_stats(page) -> dict[str, Any]:
    body = page.locator("body").inner_text(timeout=5000)
    stats: dict[str, Any] = {}
    for name, count in re.findall(r"([A-Za-z ]+)\((\d+)\)", body):
        label = re.sub(r"\s+", " ", name).strip()
        if label:
            stats[label] = int(count)
    showing_match = re.search(
        r"Showing\s+(\d+)\s+of\s+(\d+)\s+results\s+for\s+(.+?)\s+from\s+(\d+)\s+tables",
        body,
        re.IGNORECASE | re.DOTALL,
    )
    if showing_match:
        stats["visible_results"] = int(showing_match.group(1))
        stats["total_results"] = int(showing_match.group(2))
        stats["query_echo"] = showing_match.group(3).strip().rstrip(".")
        stats["tables"] = int(showing_match.group(4))
    return stats


def run_search_once(
    cdp_url: str,
    base_url: str,
    app_id: str,
    query: str,
    limit: int,
) -> dict[str, Any]:
    query = normalize_external_search_query(query)
    requested_search_url = build_search_url(base_url, app_id, query)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = pick_context(browser)
        page = context.new_page()
        try:
            open_search_results(page, base_url, app_id, query)
            page.wait_for_timeout(3000)

            body = get_body_text(page, timeout=5000)
            if is_login_page(body, page.url):
                raise RuntimeError("当前页面落到了登录页，说明浏览器会话还没有进入已登录状态。")

            switch_to_cases_view(page)
            results = extract_case_rows(page, base_url, app_id, limit)
            stats = extract_result_stats(page)

            return {
                "query": query,
                "search_url": requested_search_url,
                "page_url": page.url,
                "page_title": page.title(),
                "stats": stats,
                "results": results,
            }
        finally:
            page.close()
            browser.close()


def run_search(
    cdp_url: str,
    base_url: str,
    app_id: str,
    query: str,
    limit: int,
    problem_text: str | None = None,
    max_queries: int = 4,
) -> dict[str, Any]:
    started = time.perf_counter()
    original_input = normalize_external_search_query(problem_text or query)
    query = normalize_external_search_query(query)
    queries_tried = build_case_query_variants_from_problem(query, problem_text=problem_text, max_queries=max_queries)
    seed_query = queries_tried[0] if queries_tried else query
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    stats_by_query: list[dict[str, Any]] = []
    last_page_title = ""
    last_search_url = ""
    last_page_url = ""
    query_errors: list[dict[str, str]] = []
    stale_queries = 0

    per_query_limit = max(limit, min(limit * 2, 6))

    for variant in queries_tried:
        if time.perf_counter() - started >= SEARCH_TIME_BUDGET_SEC:
            stats_by_query.append({"query": variant, "stopped": "time_budget"})
            break
        variant_started = time.perf_counter()
        before_count = len(seen)
        try:
            payload = run_search_once(
                cdp_url=cdp_url,
                base_url=base_url,
                app_id=app_id,
                query=variant,
                limit=per_query_limit,
            )
            last_page_title = payload["page_title"]
            last_search_url = payload["search_url"]
            last_page_url = payload.get("page_url", last_page_url)
            stats_by_query.append(
                {
                    "query": variant,
                    "stats": payload.get("stats", {}),
                    "result_count": len(payload.get("results", [])),
                    "elapsed_ms": int((time.perf_counter() - variant_started) * 1000),
                    "search_url": payload.get("search_url", ""),
                    "page_url": payload.get("page_url", ""),
                }
            )
            for item in payload.get("results", []):
                row_id = item["row_id"]
                if row_id in seen:
                    continue
                seen.add(row_id)
                score, reasons = score_case_result(item, query=seed_query, queries_tried=queries_tried)
                enriched = dict(item)
                enriched["score"] = score
                enriched["match_reasons"] = reasons
                enriched["matched_query"] = variant
                merged.append(enriched)
            if len(seen) == before_count:
                stale_queries += 1
            else:
                stale_queries = 0
            current_quality = score_result_set_quality(merged[:limit], seed_query, queries_tried, title_key="subject", body_key="description")
            if len(merged) >= min(limit, EARLY_STOP_RESULTS) and current_quality >= EARLY_STOP_QUALITY:
                stats_by_query.append({"query": variant, "stopped": "quality_budget", "quality": current_quality})
                break
            if stale_queries >= STALE_QUERY_LIMIT and merged:
                stats_by_query.append({"query": variant, "stopped": "stale_queries", "stale_queries": stale_queries})
                break
        except Exception as exc:
            query_errors.append({"query": variant, "error": str(exc)})
            stats_by_query.append(
                {
                    "query": variant,
                    "stats": {},
                    "result_count": 0,
                    "elapsed_ms": int((time.perf_counter() - variant_started) * 1000),
                    "error": str(exc),
                }
            )
            continue

    merged.sort(key=lambda item: (-item.get("score", 0), item.get("subject", "")))
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    quality = score_result_set_quality(merged[:limit], seed_query, queries_tried, title_key="subject", body_key="description")
    stop_reason = "results_found" if merged else ("query_errors_only" if query_errors else "empty_results")

    return {
        "query": seed_query,
        "queries_tried": queries_tried,
        "search_url": last_search_url,
        "page_url": last_page_url,
        "page_title": last_page_title,
        "stats_by_query": stats_by_query,
        "results": merged[:limit],
        "diagnostics": {
            "elapsed_ms": elapsed_ms,
            "result_count": len(merged[:limit]),
            "result_quality_score": quality,
            "stop_reason": stop_reason,
            "query_errors": query_errors,
            "original_input": original_input,
            "search_time_budget_sec": SEARCH_TIME_BUDGET_SEC,
            "stale_query_limit": STALE_QUERY_LIMIT,
            "early_stop_quality": EARLY_STOP_QUALITY,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="通过已登录的 Dynamics 浏览器会话搜索 PSoC Edge / DeepCraft AI 相关 Infineon case。")
    parser.add_argument("query", help="搜索关键词，例如：PSoC 6 ModusToolbox programming failed KitProg")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="浏览器远程调试地址。")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Case 系统域名。")
    parser.add_argument("--app-id", default=DEFAULT_APP_ID, help="Dynamics appid。")
    parser.add_argument("--limit", type=int, default=8, help="最多返回多少条 case 结果。")
    parser.add_argument("--problem-text", help="当 query 只是“搜索此问题”式短语时，可传完整问题上下文。")
    parser.add_argument("--max-queries", type=int, default=4, help="最多尝试多少个扩展查询。")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出。")
    args = parser.parse_args()

    try:
        payload = run_search(
            cdp_url=args.cdp_url,
            base_url=args.base_url,
            app_id=args.app_id,
            query=args.query,
            limit=args.limit,
            problem_text=args.problem_text,
            max_queries=args.max_queries,
        )
    except Exception as exc:
        print(f"搜索失败：{exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"查询：{payload['query']}")
    print(f"结果页标题：{payload['page_title']}")
    print(f"结果页地址：{payload['search_url']}")
    if payload.get("queries_tried"):
        print(f"扩展查询：{json.dumps(payload['queries_tried'], ensure_ascii=False)}")
    print("")

    if not payload["results"]:
        print("未提取到 case 结果。请确认当前浏览器已登录，并且结果仍停留在 Cases 表格。")
        return 0

    print("Case 结果：")
    for idx, item in enumerate(payload["results"], start=1):
        print(f"{idx}. {item['subject']}")
        print(f"   case_number: {item['case_number']}")
        if item["contact"]:
            print(f"   contact: {item['contact']}")
        if item["account_location"]:
            print(f"   account: {item['account_location']}")
        if item["external_reference_number"]:
            print(f"   external_ref: {item['external_reference_number']}")
        print(f"   score: {item['score']}")
        print(f"   matched_query: {item['matched_query']}")
        print(f"   detail_url: {item['detail_url']}")
        if item["description"]:
            print(f"   desc: {item['description'][:240]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
