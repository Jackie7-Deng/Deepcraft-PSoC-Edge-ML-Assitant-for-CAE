from __future__ import annotations

import argparse
import json
import re
import sys
import time
from typing import Any
from urllib.parse import quote
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.case_summary import summarize_case_payload
from scripts.search_utils import build_case_query_variants, normalize_external_search_query, score_case_result


DEFAULT_CDP_URL = "http://127.0.0.1:9222"
DEFAULT_APP_ID = "4d4c3d73-64de-ec11-bb3c-002248810ede"
DEFAULT_BASE_URL = "https://ifxcasemanagement.crm4.dynamics.com"
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


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def build_search_url(base_url: str, app_id: str, query: str) -> str:
    encoded = quote(normalize_external_search_query(query), safe="")
    return f"{base_url}/main.aspx?appid={app_id}&pagetype=search&searchText={encoded}&searchType=0"


def build_detail_url(base_url: str, app_id: str, row_id: str) -> str:
    return f"{base_url}/main.aspx?appid={app_id}&pagetype=entityrecord&etn=incident&id={row_id}"


def looks_like_guid(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-fA-F-]{36}", value))


def looks_like_case_number(value: str) -> bool:
    return bool(re.fullmatch(r"IFX-\d{6}-\d+", value, re.IGNORECASE))


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


def has_detail_content(body: str) -> bool:
    return ("Case Summary" in body and "Discussion board" in body and "Description" in body)


def detail_markers_ready(page, body: str) -> bool:
    if has_detail_content(body):
        return True

    selectors = [
        '[data-id="form-header"]',
        'textarea[aria-label="Description"]',
        '[role="tab"][title="Discussion board"]',
        '[role="tabpanel"][aria-label="Discussion board"]',
    ]
    for selector in selectors:
        locator = page.locator(selector)
        try:
            if locator.count() > 0:
                return True
        except Exception:
            pass
    return False


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


def open_search_results(page, base_url: str, app_id: str, query: str) -> None:
    query = normalize_external_search_query(query)
    url = build_search_url(base_url, app_id, query)
    attempts: list[str] = []

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(9000)
        deadline = time.time() + 25
        while time.time() < deadline:
            body = get_body_text(page, timeout=3000)
            if is_login_page(body, page.url):
                raise RuntimeError("当前页面落到了登录页，说明浏览器会话没有继承到 case 登录状态。")
            if has_search_results(body):
                return
            page.wait_for_timeout(1000)
    except Exception as exc:
        attempts.append(f"url-goto: {exc}")

    try:
        page.reload(wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(8000)
        deadline = time.time() + 20
        while time.time() < deadline:
            body = get_body_text(page, timeout=3000)
            if has_search_results(body):
                return
            page.wait_for_timeout(1000)
    except Exception as exc:
        attempts.append(f"reload: {exc}")

    try:
        submit_search_via_ui(page, query)
        deadline = time.time() + 20
        while time.time() < deadline:
            body = get_body_text(page, timeout=3000)
            if has_search_results(body):
                return
            page.wait_for_timeout(1000)
    except Exception as exc:
        attempts.append(f"ui-search: {exc}")

    raise RuntimeError(" ; ".join(attempts))


def open_detail_page(page, detail_url: str) -> None:
    attempts: list[str] = []
    for label in ("goto", "reload", "goto-retry"):
        try:
            if label in ("goto", "goto-retry"):
                page.goto(detail_url, wait_until="domcontentloaded", timeout=30000)
            else:
                page.reload(wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(5000 if label == "goto-retry" else 8000)
            deadline = time.time() + (30 if label == "goto-retry" else 20)
            while time.time() < deadline:
                body = get_body_text(page, timeout=5000)
                if is_login_page(body, page.url):
                    raise RuntimeError("当前页面落到了登录页，说明浏览器会话没有继承到 case 登录状态。")
                if detail_markers_ready(page, body):
                    return
                page.wait_for_timeout(1500)
            attempts.append(f"{label}: detail markers not ready")
        except Exception as exc:
            attempts.append(f"{label}: {exc}")
    raise RuntimeError(" ; ".join(attempts))


def search_cases(page, base_url: str, app_id: str, query: str, limit: int = 12) -> list[dict[str, Any]]:
    open_search_results(page, base_url, app_id, query)
    page.wait_for_timeout(3000)
    switch_to_cases_view(page)
    results = page.evaluate(
        """
        (limit) => {
          const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim();
          const visible = (el) => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
          };
          const items = [];
          const seen = new Set();

          for (const button of document.querySelectorAll('button')) {
            if (!visible(button)) continue;
            const subject = normalize(button.getAttribute('title') || button.innerText || button.textContent || '');
            if (!subject) continue;

            const row = button.closest('[role="row"][row-id]');
            if (!row) continue;
            const rowId = row.getAttribute('row-id') || '';
            if (!rowId || seen.has(rowId)) continue;

            const cells = {};
            for (const cell of row.querySelectorAll('[role="gridcell"][col-id]')) {
              cells[cell.getAttribute('col-id')] = normalize(cell.innerText || cell.textContent || '');
            }

            const caseNumber = cells.ticketnumber || '';
            if (!caseNumber || !/^IFX-/i.test(caseNumber)) continue;

            seen.add(rowId);
            items.push({
              row_id: rowId,
              subject,
              case_number: caseNumber,
              contact: cells.ifx_ccm_primarycontactid || '',
              account_location: cells.customerid || '',
              external_reference_number: cells.ifx_externalreferencenumber || '',
              description: cells.description || ''
            });

            if (items.length >= limit) break;
          }

          return items;
        }
        """,
        limit,
    )
    for item in results:
        item["detail_url"] = build_detail_url(base_url, app_id, item["row_id"])
    return results


def search_cases_with_variants(
    page,
    base_url: str,
    app_id: str,
    query: str,
    limit: int = 12,
    max_queries: int = 4,
) -> tuple[list[str], list[dict[str, Any]]]:
    query = normalize_external_search_query(query)
    queries_tried = build_case_query_variants(query, max_queries=max_queries)
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()

    for variant in queries_tried:
        for item in search_cases(page, base_url, app_id, variant, limit=limit):
            row_id = item["row_id"]
            if row_id in seen:
                continue
            seen.add(row_id)
            score, reasons = score_case_result(item, query=query, queries_tried=queries_tried)
            enriched = dict(item)
            enriched["score"] = score
            enriched["match_reasons"] = reasons
            enriched["matched_query"] = variant
            merged.append(enriched)

    merged.sort(key=lambda item: (-item.get("score", 0), item.get("subject", "")))
    return queries_tried, merged


def resolve_target_case(
    page,
    base_url: str,
    app_id: str,
    target: str | None,
    query: str | None,
    pick: int,
) -> dict[str, Any]:
    query = normalize_external_search_query(query)
    if target:
        if target.startswith("http://") or target.startswith("https://"):
            return {"detail_url": target, "matched_by": "url"}
        if looks_like_guid(target):
            return {"detail_url": build_detail_url(base_url, app_id, target), "matched_by": "row_id"}

    if target and looks_like_case_number(target):
        query_text = query or target
        _, results = search_cases_with_variants(page, base_url, app_id, query_text)
        for item in results:
            if item["case_number"].lower() == target.lower():
                item["matched_by"] = "case_number"
                return item
        raise RuntimeError(f"搜索结果里没有找到 case number = {target}")

    query_text = query or target
    if not query_text:
        raise RuntimeError("请提供 case 详情 URL / row id / case number，或者提供 --query 做一次检索。")

    queries_tried, results = search_cases_with_variants(page, base_url, app_id, query_text)
    if not results:
        raise RuntimeError("搜索到了结果页，但没有提取到可读取的 case。")

    index = max(0, pick - 1)
    if index >= len(results):
        raise RuntimeError(f"pick={pick} 超出范围，当前只提取到 {len(results)} 条结果。")

    result = results[index]
    result["matched_by"] = f"search_pick_{pick}"
    result["search_query"] = query_text
    result["queries_tried"] = queries_tried
    return result


def extract_header_fields(page) -> dict[str, str]:
    title_locator = page.locator('[data-id="header_title"], h1').first
    header_locator = page.locator('[data-id="form-header"]').first

    subject = ""
    header_text = ""

    try:
        subject = normalize(title_locator.get_attribute("title") or title_locator.inner_text(timeout=2000))
    except Exception:
        pass

    try:
        header_text = normalize(header_locator.inner_text(timeout=5000))
    except Exception:
        pass

    fields = {
        "subject": subject,
        "case_number": "",
        "priority": "",
        "status": "",
        "owner": "",
    }

    case_match = re.search(r"(IFX-\d{6}-\d+)", header_text, re.IGNORECASE)
    if case_match:
        fields["case_number"] = case_match.group(1)

    priority_match = re.search(r"Case number\s+(.+?)\s+Priority", header_text, re.IGNORECASE)
    if priority_match:
        fields["priority"] = normalize(priority_match.group(1))

    status_match = re.search(r"Priority\s+(.+?)\s+Status", header_text, re.IGNORECASE)
    if status_match:
        fields["status"] = normalize(status_match.group(1))

    owner_locator = page.locator('[data-id="form-header"] a[aria-label]').first
    try:
        owner_text = normalize(owner_locator.inner_text(timeout=2000))
        if owner_text:
            fields["owner"] = owner_text
    except Exception:
        pass

    return fields


def extract_description(page) -> str:
    selectors = [
        "textarea[aria-label='Description']",
        "[data-id*='description.fieldControl-text-box-text']",
        "[data-id*='description'][aria-label='Description']",
    ]
    for selector in selectors:
        locator = page.locator(selector)
        try:
            if locator.count() > 0:
                text = locator.first.input_value(timeout=2000) if locator.first.evaluate("el => el.tagName === 'TEXTAREA'") else locator.first.inner_text(timeout=2000)
                text = normalize(text)
                if text:
                    return text
        except Exception:
            pass
    return ""


def try_extract_summary_text(page) -> str:
    return ""


def open_discussion_board(page) -> None:
    attempts: list[str] = []
    locators = [
        ("role", page.get_by_role("tab", name="Discussion board").first),
        ("title", page.locator('[role="tab"][title="Discussion board"]').first),
        ("dataid", page.locator('[data-id="tablist-tab_11"]').first),
    ]
    for name, locator in locators:
        try:
            locator.click(timeout=4000)
            page.wait_for_timeout(4000)
            if page.locator('[role="tabpanel"][aria-label="Discussion board"]').count() > 0:
                return
        except Exception as exc:
            attempts.append(f"{name}-click: {exc}")

        try:
            locator.click(timeout=4000, force=True)
            page.wait_for_timeout(4000)
            if page.locator('[role="tabpanel"][aria-label="Discussion board"]').count() > 0:
                return
        except Exception as exc:
            attempts.append(f"{name}-force: {exc}")

        try:
            locator.evaluate("(el) => el.click()")
            page.wait_for_timeout(4000)
            if page.locator('[role="tabpanel"][aria-label="Discussion board"]').count() > 0:
                return
        except Exception as exc:
            attempts.append(f"{name}-js: {exc}")

    raise RuntimeError(" ; ".join(attempts))


def expand_discussion_board(page) -> list[str]:
    events: list[str] = []
    load_all = page.get_by_text("Load all", exact=True).first
    try:
        load_all.click(timeout=3000)
        page.wait_for_timeout(5000)
        events.append("Load all: clicked")
        return events
    except Exception as exc:
        events.append(f"Load all: {exc}")

    load_more = page.get_by_text("Load more", exact=True).first
    try:
        load_more.click(timeout=3000)
        page.wait_for_timeout(5000)
        events.append("Load more: clicked")
    except Exception as exc:
        events.append(f"Load more: {exc}")
    return events


def extract_discussion_panel_text(page) -> str:
    panel = page.locator('[role="tabpanel"][aria-label="Discussion board"]').first
    return normalize(panel.inner_text(timeout=5000))


def parse_discussion_messages(panel_text: str) -> list[dict[str, str]]:
    pattern = re.compile(
        r"(?ms)(\d+)\s+\|\s+([^|]+?)\s+\|\s+([^|]+?)\s+\|\s+(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})\s+(.*?)(?=(?:\s+\d+\s+\|\s+[^|]+?\s+\|\s+[^|]+?\s+\|\s+\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}\s+)|\Z)"
    )
    messages: list[dict[str, str]] = []
    for match in pattern.finditer(panel_text):
        index, visibility, author, timestamp, body = match.groups()
        body = normalize(body)
        if body.endswith("Load all"):
            body = body[: -len("Load all")].strip()
        if body.endswith("Load more"):
            body = body[: -len("Load more")].strip()
        messages.append(
            {
                "index": index,
                "visibility": normalize(visibility),
                "author": normalize(author),
                "timestamp": normalize(timestamp),
                "body": body,
            }
        )
    return messages


def read_case(
    cdp_url: str,
    base_url: str,
    app_id: str,
    target: str | None,
    query: str | None,
    pick: int,
) -> dict[str, Any]:
    query = normalize_external_search_query(query)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = pick_context(browser)
        page = context.new_page()
        try:
            resolved = resolve_target_case(page, base_url, app_id, target, query, pick)
            detail_url = resolved["detail_url"]
            open_detail_page(page, detail_url)

            header = extract_header_fields(page)
            description = extract_description(page)
            summary_text = try_extract_summary_text(page)

            discussion_events: list[str] = []
            discussion_text = ""
            discussion_messages: list[dict[str, str]] = []
            discussion_error = ""

            try:
                open_discussion_board(page)
                discussion_events = expand_discussion_board(page)
                discussion_text = extract_discussion_panel_text(page)
                discussion_messages = parse_discussion_messages(discussion_text)
            except PlaywrightTimeoutError as exc:
                discussion_error = f"切换到 Discussion board 超时：{exc}"
            except Exception as exc:
                discussion_error = str(exc)

            payload = {
                "matched_by": resolved.get("matched_by", ""),
                "search_query": resolved.get("search_query", ""),
                "queries_tried": resolved.get("queries_tried", []),
                "detail_url": page.url,
                "subject": header.get("subject") or resolved.get("subject", ""),
                "case_number": header.get("case_number") or resolved.get("case_number", ""),
                "status": header.get("status", ""),
                "priority": header.get("priority", ""),
                "owner": header.get("owner", ""),
                "contact": resolved.get("contact", ""),
                "account_location": resolved.get("account_location", ""),
                "external_reference_number": resolved.get("external_reference_number", ""),
                "description": description or resolved.get("description", ""),
                "summary_text": summary_text,
                "discussion_events": discussion_events,
                "discussion_error": discussion_error,
                "discussion_text": discussion_text,
                "discussion_messages": discussion_messages,
            }
            payload["summary"] = summarize_case_payload(payload)
            return payload
        finally:
            page.close()
            browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="通过已登录的 Dynamics 浏览器会话读取单个 case 正文。")
    parser.add_argument(
        "target",
        nargs="?",
        help="case 详情 URL / row GUID / IFX case number；如果都不是，则按搜索关键词处理。",
    )
    parser.add_argument("--query", help="先执行搜索，再按 pick 选择结果。")
    parser.add_argument("--pick", type=int, default=1, help="当 target/query 是搜索词时，读取第几条结果。")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL, help="浏览器远程调试地址。")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Case 系统域名。")
    parser.add_argument("--app-id", default=DEFAULT_APP_ID, help="Dynamics appid。")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出。")
    args = parser.parse_args()

    try:
        payload = read_case(
            cdp_url=args.cdp_url,
            base_url=args.base_url,
            app_id=args.app_id,
            target=args.target,
            query=args.query,
            pick=args.pick,
        )
    except Exception as exc:
        print(f"读取失败：{exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"subject: {payload['subject']}")
    print(f"case_number: {payload['case_number']}")
    print(f"status: {payload['status']}")
    print(f"priority: {payload['priority']}")
    print(f"owner: {payload['owner']}")
    if payload["contact"]:
        print(f"contact: {payload['contact']}")
    if payload["account_location"]:
        print(f"account: {payload['account_location']}")
    print(f"url: {payload['detail_url']}")
    print("")

    if payload["description"]:
        print("Description:")
        print(payload["description"])
        print("")

    if payload.get("summary"):
        print("Summary Extract:")
        print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
        print("")

    if payload["summary_text"]:
        print("Summary:")
        print(payload["summary_text"])
        print("")

    if payload["discussion_messages"]:
        print(f"Discussion messages: {len(payload['discussion_messages'])}")
        for item in payload["discussion_messages"][:6]:
            print(
                f"- #{item['index']} | {item['visibility']} | {item['author']} | {item['timestamp']}\n  {item['body'][:320]}"
            )
    elif payload["discussion_text"]:
        print("Discussion:")
        print(payload["discussion_text"][:3000])
    elif payload["discussion_error"]:
        print(f"Discussion board 读取失败：{payload['discussion_error']}")

    if payload["discussion_events"]:
        print("")
        print("Discussion actions:")
        for event in payload["discussion_events"]:
            print(f"- {event}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
