from __future__ import annotations

import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import Context, FastMCP  # noqa: E402
from mcp.server.session import ServerSession  # noqa: E402

from scripts.case_read_playwright import read_case  # noqa: E402
from scripts.case_search_playwright import run_search as run_case_search  # noqa: E402
from scripts.community_read_playwright import read_article  # noqa: E402
from scripts.community_search_playwright import run_search as run_community_search  # noqa: E402
from scripts.search_utils import (  # noqa: E402
    build_psoc_edge_query_plan,
    build_case_query_variants_from_problem,
    build_community_query_variants,
    derive_search_seed,
    normalize_external_search_query,
    score_community_result,
    score_result_set_quality,
)


DEFAULT_CDP_URL = os.environ.get("IFX_MCP_CDP_URL", "http://127.0.0.1:9222")
DEFAULT_COMMUNITY_BASE_URL = os.environ.get("IFX_COMMUNITY_BASE_URL", "https://community.infineon.com")
DEFAULT_CASE_BASE_URL = os.environ.get("IFX_CASE_BASE_URL", "https://ifxcasemanagement.crm4.dynamics.com")
DEFAULT_CASE_APP_ID = os.environ.get("IFX_CASE_APP_ID", "4d4c3d73-64de-ec11-bb3c-002248810ede")
DEFAULT_LOG_LEVEL = os.environ.get("IFX_MCP_LOG_LEVEL", "INFO").upper()

SERVER_INSTRUCTIONS = """
Infineon browser-backed MCP server for PSoC Edge + DeepCraft AI support workflows.

This server is intentionally read-only. It does not modify Community or Case content.
It reuses a real, already-open browser session through CDP so the client can access:
- public Infineon Community pages that block direct fetches with 403
- internal Dynamics Case pages that require an existing logged-in browser session

Preferred usage model:
1. answer from the local PSoC Edge / PSoC 6 knowledge base first
2. trigger Community or Case lookup manually when the engineer decides more field evidence is needed
3. search iteratively: chip/demo + symptom -> add toolchain/framework -> add platform/peripheral keywords
4. summarize external results before using them in the final answer
""".strip()

mcp = FastMCP(
    name="psoc-edge-browser-mcp",
    instructions=SERVER_INSTRUCTIONS,
    json_response=True,
    log_level=DEFAULT_LOG_LEVEL if DEFAULT_LOG_LEVEL in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"} else "INFO",
)


# Cross-call diagnostics/cache for community browsing.
# This stays in-process and resets when MCP server restarts.
_COMMUNITY_SEARCH_COUNTS: dict[str, int] = {}
_COMMUNITY_READ_COUNTS: dict[str, int] = {}
_COMMUNITY_SEARCH_CACHE: dict[str, dict[str, Any]] = {}
_COMMUNITY_READ_CACHE: dict[str, dict[str, Any]] = {}
_COMMUNITY_REPEAT_LIMIT = 3
_COMMUNITY_STALE_VARIANT_LIMIT = 2
_COMMUNITY_SEARCH_TIME_BUDGET_SEC = 75
_COMMUNITY_EARLY_STOP_QUALITY = 0.72
_COMMUNITY_EARLY_STOP_RESULTS = 3


def _normalize_query(value: str | None) -> str:
    if not value:
        return ""
    return normalize_external_search_query(value).lower()


def _normalize_url(value: str | None) -> str:
    if not value:
        return ""
    return value.strip()


def _community_defaults(cdp_url: str | None, base_url: str | None) -> tuple[str, str]:
    return (cdp_url or DEFAULT_CDP_URL, base_url or DEFAULT_COMMUNITY_BASE_URL)


def _case_defaults(cdp_url: str | None, base_url: str | None, app_id: str | None) -> tuple[str, str, str]:
    return (
        cdp_url or DEFAULT_CDP_URL,
        base_url or DEFAULT_CASE_BASE_URL,
        app_id or DEFAULT_CASE_APP_ID,
    )


def _run_community_search_with_variants(
    cdp_url: str,
    base_url: str,
    query: str | None,
    problem_text: str | None,
    limit: int,
    max_queries: int,
) -> dict[str, Any]:
    derived_query = derive_search_seed(query, problem_text=problem_text, mode="community")
    if not derived_query:
        raise ValueError("community_search 需要 query 或 problem_text。")
    query_plan = build_psoc_edge_query_plan(
        problem_text or query or derived_query,
        max_queries=max_queries,
        source_text=problem_text or query or derived_query,
    )

    raw_variants = build_community_query_variants(query, problem_text=problem_text, max_queries=max_queries)
    queries_tried: list[str] = []
    variant_seen: set[str] = set()
    for variant in raw_variants:
        key = _normalize_query(variant)
        if not key or key in variant_seen:
            continue
        variant_seen.add(key)
        queries_tried.append(variant)

    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    page_title = ""
    page_url = ""
    variant_diagnostics: list[dict[str, Any]] = []
    query_errors: list[dict[str, str]] = []
    stale_variants = 0
    started_monotonic = time.monotonic()

    per_query_limit = max(limit, min(limit * 2, 8))
    for variant in queries_tried:
        if time.monotonic() - started_monotonic >= _COMMUNITY_SEARCH_TIME_BUDGET_SEC:
            variant_diagnostics.append({"query": variant, "stopped": "time_budget"})
            break
        before_count = len(seen)
        try:
            payload = run_community_search(cdp_url, variant, per_query_limit, base_url)
            page_title = payload.get("page_title", page_title)
            page_url = payload.get("page_url", page_url)
            variant_diagnostics.append(
                {
                    "query": variant,
                    **payload.get("diagnostics", {}),
                }
            )
            for item in payload.get("results", []):
                url = item.get("url", "")
                if not url or url in seen:
                    continue
                seen.add(url)
                score, reasons = score_community_result(item, derived_query, queries_tried)
                enriched = dict(item)
                enriched["score"] = score
                enriched["match_reasons"] = reasons
                enriched["matched_query"] = variant
                merged.append(enriched)
            if len(seen) == before_count:
                stale_variants += 1
            else:
                stale_variants = 0
            current_quality = score_result_set_quality(merged[:limit], derived_query, queries_tried, url_key="url")
            if len(merged) >= min(limit, _COMMUNITY_EARLY_STOP_RESULTS) and current_quality >= _COMMUNITY_EARLY_STOP_QUALITY:
                variant_diagnostics.append({"query": variant, "stopped": "quality_budget", "quality": current_quality})
                break
            if stale_variants >= _COMMUNITY_STALE_VARIANT_LIMIT and merged:
                variant_diagnostics.append({"query": variant, "stopped": "stale_variants", "stale_variants": stale_variants})
                break
        except Exception as exc:
            query_errors.append({"query": variant, "error": str(exc)})
            variant_diagnostics.append({"query": variant, "error": str(exc)})
            continue

    merged.sort(key=lambda item: (-item.get("score", 0), item.get("title", "")))
    result_quality_score = score_result_set_quality(merged[:limit], derived_query, queries_tried, url_key="url")
    return {
        "query": derived_query,
        "queries_tried": queries_tried,
        "page_title": page_title,
        "page_url": page_url,
        "results": merged[:limit],
        "diagnostics": {
            "variants_before_dedupe": len(raw_variants),
            "variants_after_dedupe": len(queries_tried),
            "unique_urls_collected": len(seen),
            "variant_diagnostics": variant_diagnostics,
            "query_errors": query_errors,
            "query_plan": query_plan,
            "result_quality_score": result_quality_score,
            "stop_reason": "results_found" if merged else ("query_errors_only" if query_errors else "empty_results"),
            "stale_variant_limit": _COMMUNITY_STALE_VARIANT_LIMIT,
            "search_time_budget_sec": _COMMUNITY_SEARCH_TIME_BUDGET_SEC,
            "early_stop_quality": _COMMUNITY_EARLY_STOP_QUALITY,
        },
    }


@mcp.resource("config://defaults")
def server_defaults() -> dict[str, Any]:
    """Return the server's effective default configuration."""
    return {
        "server_name": "psoc-edge-browser-mcp",
        "mode": "read-only-browser-backed",
        "default_cdp_url": DEFAULT_CDP_URL,
        "community_base_url": DEFAULT_COMMUNITY_BASE_URL,
        "case_base_url": DEFAULT_CASE_BASE_URL,
        "case_app_id": DEFAULT_CASE_APP_ID,
        "notes": [
            "Community and Case access depend on a live browser session opened with remote debugging.",
            "Case reading requires the browser session to already be logged in.",
            "Use local KB first; external search is manual and evidence-oriented.",
        ],
    }


@mcp.resource("policy://external-search")
def external_search_policy() -> str:
    """Return the intended external-search policy for the PSoC Edge + DeepCraft assistant."""
    return (
        "Default to local PSoC Edge / PSoC 6 knowledge base answers. "
        "Use Community/Case search only when the engineer explicitly asks for external evidence or when the local KB is clearly insufficient. "
        "Before external search, compress the real problem into short PSoC Edge or PSoC 6 query variants. "
        "Keep search and read separate: search first, then read selected results, then summarize. "
        "Treat community and case results as field experience, not as silicon specification."
    )


@mcp.prompt(title="PSoC Edge external search plan")
def external_search_plan(user_question: str, mode: str = "community") -> str:
    """Generate a disciplined external-search plan before calling tools."""
    return (
        f"请先把用户问题抽象成检索计划，而不是直接乱搜。\n"
        f"用户问题：{user_question}\n"
        f"优先模式：{mode}\n\n"
        f"要求：\n"
        f"1. 先识别平台词、示例词、ML 框架词、memory/toolchain 词和主症状词。\n"
        f"2. 为 case/community 生成 3~5 个短关键词变体。\n"
        f"3. 先搜最短、最稳定的查询，再根据命中结果调整下一轮关键词。\n"
        f"4. 强制分离 search 和 read：先挑 2~3 条最相关结果，再读正文。\n"
        f"5. 读到结果后先摘要成：问题 / 现象 / 调试过程 / 解决建议 / 未决项。\n"
        f"6. 不要把 case/community 经验直接当作官方规格。"
    )


@mcp.tool()
async def community_search(
    ctx: Context[ServerSession, None],
    query: str | None = None,
    problem_text: str | None = None,
    limit: int = 5,
    max_queries: int = 4,
    cdp_url: str | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Search Infineon Community for PSoC Edge / DeepCraft AI field experience through the existing browser session.

    Search returns result cards only. Use `community_read_article` to read one selected thread or KBA body.
    Prefer passing `problem_text` when the user says "search this issue" and the real PSoC Edge / PSoC 6 ML problem only exists in chat context. The server will condense it into short query variants such as `PSoC Edge MTBML model deploy failed` or `PSoC 6 Face ID demo build error`.
    """
    effective_cdp_url, effective_base_url = _community_defaults(cdp_url, base_url)
    derived_query = derive_search_seed(query, problem_text=problem_text, mode="community")
    query_key = _normalize_query(derived_query)
    if query_key:
        _COMMUNITY_SEARCH_COUNTS[query_key] = _COMMUNITY_SEARCH_COUNTS.get(query_key, 0) + 1
    search_repeat_count = _COMMUNITY_SEARCH_COUNTS.get(query_key, 0)
    await ctx.info(f"community_search: query={derived_query!r}, limit={limit}, max_queries={max_queries}")
    if query_key and query_key in _COMMUNITY_SEARCH_CACHE and search_repeat_count > _COMMUNITY_REPEAT_LIMIT:
        cached = dict(_COMMUNITY_SEARCH_CACHE[query_key])
        cached["diagnostics"] = {
            **cached.get("diagnostics", {}),
            "cache_hit": True,
            "repeat_limit_hit": True,
            "normalized_query": query_key,
            "query_repeat_count": search_repeat_count,
            "tracked_unique_queries": len(_COMMUNITY_SEARCH_COUNTS),
        }
        return cached
    payload = await asyncio.to_thread(
        _run_community_search_with_variants,
        effective_cdp_url,
        effective_base_url,
        query,
        problem_text,
        int(limit),
        int(max_queries),
    )
    payload["diagnostics"] = {
        **payload.get("diagnostics", {}),
        "cache_hit": False,
        "repeat_limit_hit": False,
        "normalized_query": query_key,
        "query_repeat_count": search_repeat_count,
        "tracked_unique_queries": len(_COMMUNITY_SEARCH_COUNTS),
    }
    if query_key:
        _COMMUNITY_SEARCH_CACHE[query_key] = payload
    return payload


@mcp.tool()
async def community_read_article(
    url: str,
    ctx: Context[ServerSession, None],
    cdp_url: str | None = None,
) -> dict[str, Any]:
    """Read one selected PSoC Edge / DeepCraft related Community thread or KBA body through the existing browser session."""
    effective_cdp_url, _ = _community_defaults(cdp_url, None)
    normalized_url = _normalize_url(url)
    if normalized_url:
        _COMMUNITY_READ_COUNTS[normalized_url] = _COMMUNITY_READ_COUNTS.get(normalized_url, 0) + 1
    read_count = _COMMUNITY_READ_COUNTS.get(normalized_url, 0)

    await ctx.info(f"community_read_article: url={url} repeat_count={read_count}")

    if normalized_url and normalized_url in _COMMUNITY_READ_CACHE:
        cached = dict(_COMMUNITY_READ_CACHE[normalized_url])
        cached["diagnostics"] = {
            **cached.get("diagnostics", {}),
            "cache_hit": True,
            "repeat_limit_hit": read_count > _COMMUNITY_REPEAT_LIMIT,
            "read_count_for_url": read_count,
            "tracked_unique_urls": len(_COMMUNITY_READ_COUNTS),
        }
        return cached

    payload = await asyncio.to_thread(read_article, effective_cdp_url, url)
    payload["diagnostics"] = {
        **payload.get("diagnostics", {}),
        "cache_hit": False,
        "repeat_limit_hit": False,
        "read_count_for_url": read_count,
        "tracked_unique_urls": len(_COMMUNITY_READ_COUNTS),
    }
    if normalized_url:
        _COMMUNITY_READ_CACHE[normalized_url] = payload
    return payload


@mcp.tool()
async def community_access_stats() -> dict[str, Any]:
    """Return in-process community search/read repetition statistics for debugging tool behavior."""
    top_queries = sorted(_COMMUNITY_SEARCH_COUNTS.items(), key=lambda item: (-item[1], item[0]))[:20]
    top_urls = sorted(_COMMUNITY_READ_COUNTS.items(), key=lambda item: (-item[1], item[0]))[:20]
    return {
        "search": {
            "tracked_unique_queries": len(_COMMUNITY_SEARCH_COUNTS),
            "top_queries": [{"query": query, "count": count} for query, count in top_queries],
        },
        "read": {
            "tracked_unique_urls": len(_COMMUNITY_READ_COUNTS),
            "cache_size": len(_COMMUNITY_READ_CACHE),
            "top_urls": [{"url": url, "count": count} for url, count in top_urls],
        },
    }


@mcp.tool()
async def case_search(
    ctx: Context[ServerSession, None],
    query: str | None = None,
    problem_text: str | None = None,
    limit: int = 5,
    max_queries: int = 4,
    cdp_url: str | None = None,
    base_url: str | None = None,
    app_id: str | None = None,
) -> dict[str, Any]:
    """Search Dynamics cases for PSoC Edge / DeepCraft AI issues with keyword expansion and result scoring.

    Search returns result cards only. Use `case_read` to read one selected case.
    Prefer passing `problem_text` when the user's real PSoC Edge / PSoC 6 ML issue is in chat context rather than already condensed into a short keyword query.
    """
    effective_cdp_url, effective_base_url, effective_app_id = _case_defaults(cdp_url, base_url, app_id)
    derived_query = derive_search_seed(query, problem_text=problem_text, mode="case")
    if not derived_query:
        raise ValueError("case_search 需要 query 或 problem_text。")
    await ctx.info(f"case_search: query={derived_query!r}, limit={limit}, max_queries={max_queries}")
    return await asyncio.to_thread(
        run_case_search,
        effective_cdp_url,
        effective_base_url,
        effective_app_id,
        derived_query,
        int(limit),
        problem_text,
        int(max_queries),
    )


@mcp.tool()
async def case_read(
    ctx: Context[ServerSession, None],
    target: str | None = None,
    query: str | None = None,
    problem_text: str | None = None,
    pick: int = 1,
    cdp_url: str | None = None,
    base_url: str | None = None,
    app_id: str | None = None,
) -> dict[str, Any]:
    """Read one PSoC Edge / DeepCraft AI case by URL/ID/case number or by search query and return a structured summary.

    If only chat context is available, pass `problem_text`; the server will derive a short
    search query before resolving the case result.
    """
    effective_cdp_url, effective_base_url, effective_app_id = _case_defaults(cdp_url, base_url, app_id)
    if target:
        await ctx.info(f"case_read: target={target!r}")
    else:
        query = derive_search_seed(query, problem_text=problem_text, mode="case")
        if not query:
            raise ValueError("case_read 需要 target，或至少提供 query / problem_text。")
        await ctx.info(f"case_read: query={query!r}, pick={pick}")
    return await asyncio.to_thread(
        read_case,
        effective_cdp_url,
        effective_base_url,
        effective_app_id,
        target,
        query,
        int(pick),
    )


def main() -> int:
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
