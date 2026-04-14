from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.search_utils import normalize_external_search_query, score_community_result, score_result_set_quality  # noqa: E402


JSON_ENDPOINT_MARKERS = ("coveo", "search/v2", "rest/search")
SEARCH_HUB_DEFAULT = "InfineonCommunityHub"


def pick_context(browser):
    if browser.contexts:
        return browser.contexts[0]
    raise RuntimeError("未找到可用的浏览器上下文，请先用启动脚本打开浏览器。")


def build_search_url(base_url: str, query: str) -> str:
    normalized_query = normalize_external_search_query(query)
    return f"{base_url.rstrip('/')}/t5/forums/searchpage/tab/message?q={quote(normalized_query, safe='')}"


def build_global_search_url(base_url: str, query: str) -> str:
    normalized_query = normalize_external_search_query(query)
    return f"{base_url.rstrip('/')}/t5/custom/page/page-id/GlobalSearch#q={quote(normalized_query, safe='')}&tab=All"


def normalize_space(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def strip_html(text: str | None) -> str:
    if not text:
        return ""
    no_tags = re.sub(r"<[^>]+>", " ", text)
    return normalize_space(no_tags)


def absolutize_url(base_url: str, maybe_url: str | None) -> str:
    value = normalize_space(maybe_url)
    if not value:
        return ""
    return urljoin(base_url.rstrip("/") + "/", value)


def looks_like_search_json(response) -> bool:
    url = (response.url or "").lower()
    if not any(marker in url for marker in JSON_ENDPOINT_MARKERS):
        return False
    try:
        content_type = (response.headers or {}).get("content-type", "")
    except Exception:
        content_type = ""
    return "json" in content_type.lower()


def extract_results_from_payload(payload: Any, base_url: str) -> list[dict[str, str]]:
    results_node: list[Any] | None = None

    def visit(node: Any) -> list[Any] | None:
        if isinstance(node, dict):
            maybe_results = node.get("results")
            if isinstance(maybe_results, list):
                return maybe_results
            for value in node.values():
                found = visit(value)
                if found:
                    return found
        elif isinstance(node, list):
            for item in node:
                found = visit(item)
                if found:
                    return found
        return None

    results_node = visit(payload)
    if not results_node:
        return []

    extracted: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in results_node:
        if not isinstance(item, dict):
            continue
        title = normalize_space(item.get("title") or item.get("raw", {}).get("title"))
        url = absolutize_url(base_url, item.get("clickUri") or item.get("uri") or item.get("raw", {}).get("clickUri") or item.get("raw", {}).get("uri"))
        excerpt = strip_html(item.get("excerpt") or item.get("excerptHighlights") or item.get("summary"))
        if not title or not url:
            continue
        if url in seen:
            continue
        seen.add(url)
        extracted.append(
            {
                "title": title,
                "url": url,
                "excerpt": excerpt,
            }
        )
    return extracted


def extract_coveo_config(page) -> dict[str, str]:
    scripts_text = page.evaluate(
        "() => Array.from(document.scripts).map((s) => s.textContent || '').join('\\n')"
    )
    if not scripts_text:
        return {}

    patterns = {
        "accessToken": [
            r'coveoTokenKey\s*=\s*"([^"]+)"',
            r'coveoSearchKey\s*=\s*"([^"]+)"',
            r'accessToken\s*:\s*"([^"]+)"',
        ],
        "organizationId": [
            r'organizationId\s*=\s*"([^"]+)"',
            r'organizationId\s*:\s*"([^"]+)"',
            r'ORGid\s*=\s*"([^"]+)"',
        ],
        "platformUrl": [
            r'platformUrl\s*:\s*"([^"]+)"',
            r'platformUrl\s*=\s*"([^"]+)"',
        ],
        "searchHub": [
            r'searchHub\s*=\s*"([^"]+)"',
            r'searchHub\s*:\s*"([^"]+)"',
        ],
    }

    config: dict[str, str] = {}
    for key, regexes in patterns.items():
        for pattern in regexes:
            match = re.search(pattern, scripts_text)
            if match:
                config[key] = match.group(1)
                break

    if not config.get("searchHub"):
        config["searchHub"] = SEARCH_HUB_DEFAULT

    org = config.get("organizationId", "")
    if (not org) or any(ch in org for ch in (' ', '+', '%', '\n', '\r', '\t')):
        org_match = re.search(r'ORGid\s*=\s*"([^"]+)"', scripts_text)
        if org_match:
            config["organizationId"] = org_match.group(1)
            org = config["organizationId"]

    platform = config.get("platformUrl", "")
    if platform and ((not org) or any(ch in org for ch in (' ', '+', '%', '\n', '\r', '\t'))):
        host_match = re.search(r'https://([^./]+)\.org\.coveo\.com', platform)
        if host_match:
            config["organizationId"] = host_match.group(1)
            org = config["organizationId"]

    if not platform and org:
        config["platformUrl"] = f"https://{org}.org.coveo.com"
    return config


def trigger_coveo_fetch(page, query: str, limit: int) -> dict[str, Any]:
    config = extract_coveo_config(page)
    if not config.get("accessToken") or not config.get("organizationId") or not config.get("platformUrl"):
        return {
            "attempted": False,
            "reason": "missing_coveo_config",
            "config_keys": sorted(config.keys()),
        }

    payload = {
        "platformUrl": config["platformUrl"],
        "organizationId": config["organizationId"],
        "accessToken": config["accessToken"],
        "searchHub": config.get("searchHub") or SEARCH_HUB_DEFAULT,
        "query": query,
        "limit": max(limit, 10),
    }
    result = page.evaluate(
        """
        async (cfg) => {
          const url = `${cfg.platformUrl}/rest/search/v2?organizationId=${encodeURIComponent(cfg.organizationId)}`;
          const requestPayload = {
            q: cfg.query,
            searchHub: cfg.searchHub,
            locale: document.documentElement.lang || 'en',
            numberOfResults: cfg.limit,
          };
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${cfg.accessToken}`,
            },
            body: JSON.stringify(requestPayload),
          });
          const contentType = response.headers.get('content-type') || '';
          const preview = (await response.text()).slice(0, 300);
          return {
            ok: response.ok,
            status: response.status,
            contentType,
            preview,
            requestUrl: url,
          };
        }
        """,
        payload,
    )
    page.wait_for_timeout(2000)
    return {
        "attempted": True,
        "config_keys": sorted(config.keys()),
        **result,
    }


def extract_anchor_fallback(page, limit: int, base_url: str) -> list[dict[str, str]]:
    raw_links = page.locator("a[href*='/t5/']").evaluate_all(
        r"""
        (els, limit) => els
          .map((el) => ({
            href: el.getAttribute('href') || '',
            title: (el.innerText || el.textContent || el.getAttribute('title') || '').replace(/\s+/g, ' ').trim(),
          }))
          .filter((item) => item.href.includes('/t5/') && !item.href.includes('/searchpage'))
          .slice(0, limit * 6)
        """,
        limit,
    )
    results: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in raw_links:
        url = absolutize_url(base_url, item.get("href"))
        title = normalize_space(item.get("title"))
        if not url or not title or url in seen:
            continue
        seen.add(url)
        results.append({"title": title, "url": url, "excerpt": ""})
        if len(results) >= limit:
            break
    return results


def run_search(cdp_url: str, query: str, limit: int, base_url: str) -> dict[str, Any]:
    started = time.perf_counter()
    normalized_query = normalize_external_search_query(query)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = pick_context(browser)
        page = context.new_page()
        intercepted_results: list[dict[str, str]] = []
        seen_urls: set[str] = set()
        matched_response_urls: list[str] = []
        fetch_diagnostics: dict[str, Any] = {"attempted": False}

        def handle_response(response) -> None:
            if not looks_like_search_json(response):
                return
            try:
                payload = response.json()
            except Exception:
                return
            extracted = extract_results_from_payload(payload, base_url)
            if not extracted:
                return
            matched_response_urls.append(response.url)
            for item in extracted:
                url = item["url"]
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                intercepted_results.append(item)

        page.on("response", handle_response)

        try:
            search_url = build_search_url(base_url, normalized_query)
            page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except PlaywrightTimeoutError:
                pass
            page.wait_for_timeout(3000)

            if not intercepted_results:
                page.goto(build_global_search_url(base_url, normalized_query), wait_until="domcontentloaded", timeout=30000)
                try:
                    page.wait_for_load_state("networkidle", timeout=10000)
                except PlaywrightTimeoutError:
                    pass
                page.wait_for_timeout(3000)

            if not intercepted_results:
                fetch_diagnostics = trigger_coveo_fetch(page, normalized_query, limit)
                try:
                    page.wait_for_load_state("networkidle", timeout=5000)
                except PlaywrightTimeoutError:
                    pass
                page.wait_for_timeout(1500)

            extraction_mode = "network_intercept" if intercepted_results else "dom_link_fallback"
            results = intercepted_results[:limit] if intercepted_results else extract_anchor_fallback(page, limit, base_url)
            enriched_results: list[dict[str, Any]] = []
            for item in results:
                score, reasons = score_community_result(item, normalized_query, [normalized_query])
                enriched = dict(item)
                enriched["score"] = score
                enriched["match_reasons"] = reasons
                enriched_results.append(enriched)
            enriched_results.sort(key=lambda item: (-item.get("score", 0), item.get("title", "")))
            enriched_results = enriched_results[:limit]
            quality = score_result_set_quality(
                enriched_results,
                normalized_query,
                [normalized_query],
                title_key="title",
                body_key="excerpt",
                url_key="url",
            )
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            stop_reason = "results_found" if enriched_results else "empty_results"
            return {
                "query": normalized_query,
                "page_title": page.title(),
                "page_url": page.url,
                "results": enriched_results,
                "diagnostics": {
                    "extraction_mode": extraction_mode,
                    "intercepted_response_count": len(matched_response_urls),
                    "intercepted_result_count": len(intercepted_results),
                    "intercepted_response_urls": matched_response_urls[:10],
                    "direct_coveo_fetch": fetch_diagnostics,
                    "elapsed_ms": elapsed_ms,
                    "result_count": len(enriched_results),
                    "result_quality_score": quality,
                    "stop_reason": stop_reason,
                },
            }
        finally:
            page.close()
            browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="通过已打开的 Chrome/Edge 会话搜索 Infineon Community 中与 PSoC Edge / DeepCraft AI 相关的话题。")
    parser.add_argument("query", help="要搜索的关键词，例如：PSoC Edge MTBML model deploy failed")
    parser.add_argument("--cdp-url", default="http://127.0.0.1:9222", help="浏览器远程调试地址。")
    parser.add_argument("--base-url", default="https://community.infineon.com", help="Community 首页。")
    parser.add_argument("--limit", type=int, default=8, help="最多返回多少条结果。")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出。")
    args = parser.parse_args()

    try:
        payload = run_search(
            cdp_url=args.cdp_url,
            query=args.query,
            limit=args.limit,
            base_url=args.base_url,
        )
    except Exception as exc:
        print(f"搜索失败：{exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"查询：{payload['query']}")
    print(f"结果页标题：{payload['page_title']}")
    print(f"结果页地址：{payload['page_url']}")
    print(f"提取方式：{payload.get('diagnostics', {}).get('extraction_mode', 'unknown')}")
    print("")
    if not payload["results"]:
        print("未提取到搜索结果。请先确认浏览器中能正常搜索，并且页面未停留在验证码/异常状态。")
        return 0

    print("搜索结果：")
    for idx, item in enumerate(payload["results"], start=1):
        print(f"{idx}. {item['title']}")
        print(f"   {item['url']}")
        if item.get("excerpt"):
            print(f"   摘要：{item['excerpt']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
