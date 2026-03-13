#!/usr/bin/env python3
"""
网页镜像刷新脚本

以 ingest/urls_checked.txt 为当前权威 URL 清单，逐条抓取 DEEPCRAFT 官网页面，
同步更新以下产物：

- ingest/html/*.md              原始镜像层（YAML front matter + 正文）
- ingest/url_success.txt        成功清单
- ingest/url_missing.txt        失败清单（带失败原因）
- ingest/fetch_audit.json       抓取审计层

说明：
- 保留 urls_checked.txt 中的原始顺序
- 允许 URL 重复，并在 fetch_audit.json 中保留重复项记录
- 当前脚本默认写入 markdown 版网页正文，content_format 会写为 markdown
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as markdownify

# ─── 路径配置 ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
INGEST_DIR = BASE_DIR / "ingest"
URLS_FILE = INGEST_DIR / "urls_checked.txt"
OUTPUT_DIR = INGEST_DIR / "html"
AUDIT_FILE = INGEST_DIR / "fetch_audit.json"
SUCCESS_FILE = INGEST_DIR / "url_success.txt"
MISSING_FILE = INGEST_DIR / "url_missing.txt"

# ─── 请求配置 ─────────────────────────────────────────────────────────────────
REQUEST_DELAY = 0.35
MAX_RETRIES = 2
TIMEOUT = 30
SOURCE_SITE = "https://developer.imagimob.com"
AUTHORITATIVE_LIST = "ingest/urls_checked.txt"
BASE_TAGS = ["deepcraft", "checked-url", "web-mirror"]

session = requests.Session()
session.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
)

HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
BLOCK_TAGS = HEADING_TAGS | {"p", "ul", "ol", "pre", "table", "blockquote", "img", "iframe", "hr"}
CONTAINER_TAGS = {"main", "article", "section", "div", "span"}
DROP_SELECTOR = "script, style, nav, button, noscript, form, header, footer, aside"


# ─── 工具函数 ─────────────────────────────────────────────────────────────────
def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def yaml_quote(value) -> str:
    return json.dumps("" if value is None else value, ensure_ascii=False)


def url_to_filename(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return "index.md"
    safe_name = re.sub(r"[^\w\-/]", "_", path)
    safe_name = safe_name.replace("/", "_")
    return f"{safe_name}.md"


def normalize_space(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\u200b", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def to_plain_excerpt(markdown_text: str, limit: int = 260) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", markdown_text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[#>*`_-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def sanitize_tag(tag: str) -> str:
    tag = re.sub(r"[^a-z0-9\-]+", "-", tag.lower()).strip("-")
    return tag or "untagged"


def build_tags(url: str) -> list[str]:
    segments = [seg for seg in urlparse(url).path.strip("/").split("/") if seg]
    tags = list(BASE_TAGS)
    for seg in segments[:3]:
        tags.append(sanitize_tag(seg))
    deduped = []
    seen = set()
    for tag in tags:
        if tag not in seen:
            deduped.append(tag)
            seen.add(tag)
    return deduped


def read_checked_urls() -> list[dict]:
    urls = []
    seen = set()
    for line in URLS_FILE.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value.startswith("https://"):
            urls.append(
                {
                    "checked_index": len(urls) + 1,
                    "source_url": value,
                    "filename": url_to_filename(value),
                    "duplicate": value in seen,
                }
            )
            seen.add(value)
    return urls


def extract_title(html: str, url: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find(["h1", "h2", "h3"])
    if heading:
        return " ".join(heading.get_text(" ", strip=True).split())
    return f"Fetched from {url}"


def pick_content_root(soup: BeautifulSoup) -> Tag:
    article = soup.find("article")
    if article:
        return article.find("main") or article
    return soup.find("main") or soup.body or soup


def absolutize_links(root: Tag, page_url: str):
    for node in root.find_all("a", href=True):
        node["href"] = urljoin(page_url, node["href"])
    for node in root.find_all("img", src=True):
        node["src"] = urljoin(page_url, node["src"])
    for node in root.find_all("iframe", src=True):
        node["src"] = urljoin(page_url, node["src"])


def render_list(node: Tag) -> str:
    lines = []
    ordered = node.name == "ol"
    for i, li in enumerate(node.find_all("li", recursive=False), 1):
        content = normalize_space(markdownify(str(li), heading_style="ATX"))
        content = content.lstrip("* ").strip()
        if content:
            prefix = f"{i}. " if ordered else "- "
            lines.append(prefix + content)
    return "\n".join(lines)


def render_node(node: Tag) -> str:
    if node.name in HEADING_TAGS:
        level = int(node.name[1])
        text = " ".join(node.get_text(" ", strip=True).split())
        return f"{'#' * level} {text}" if text else ""

    if node.name == "img":
        src = node.get("src", "").strip()
        alt = " ".join(node.get("alt", "").split())
        return f"![{alt}]({src})" if src else ""

    if node.name == "iframe":
        src = node.get("src", "").strip()
        return f"[iframe]({src})" if src else ""

    if node.name == "hr":
        return "---"

    if node.name in {"ul", "ol"}:
        return render_list(node)

    if node.name in {"p", "pre", "table", "blockquote"}:
        return normalize_space(markdownify(str(node), heading_style="ATX"))

    if node.name == "div":
        text = " ".join(node.get_text(" ", strip=True).split())
        if text.startswith("Last updated on"):
            return text

    return ""


def iter_blocks(root: Tag) -> Iterable[Tag]:
    for child in root.children:
        if not isinstance(child, Tag):
            continue
        if child.name in {"script", "style", "noscript"}:
            continue
        if child.name in BLOCK_TAGS:
            yield child
            continue
        if child.name in CONTAINER_TAGS:
            text = " ".join(child.get_text(" ", strip=True).split())
            if child.name == "div" and text.startswith("Last updated on"):
                yield child
                continue
            yield from iter_blocks(child)


def html_to_markdown(html: str, page_url: str, title: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    root = pick_content_root(soup)
    for node in root.select(DROP_SELECTOR):
        node.decompose()
    absolutize_links(root, page_url)

    parts = []
    for node in iter_blocks(root):
        chunk = render_node(node)
        if chunk:
            parts.append(chunk)

    text = "\n\n".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = normalize_space(text)

    if not text:
        text = normalize_space(root.get_text("\n", strip=True))

    heading_match = re.match(rf"^#+\s+{re.escape(title)}\s*$", text, flags=re.IGNORECASE | re.MULTILINE)
    if not heading_match and title:
        text = f"# {title}\n\n{text}".strip()

    return text + "\n"


def fetch_url(url: str) -> dict:
    result = {
        "source_url": url,
        "status": "failed",
        "http_code": 0,
        "reason": "",
        "retries": 0,
        "content": "",
        "title": "",
        "content_format": "markdown",
        "redirect_url": "",
        "fetched_at": now_iso(),
        "excerpt": "",
    }

    for attempt in range(MAX_RETRIES + 1):
        result["retries"] = attempt
        try:
            response = session.get(url, timeout=TIMEOUT, allow_redirects=True)
            result["http_code"] = response.status_code
            result["redirect_url"] = response.url if response.url != url else ""

            if response.status_code == 200:
                html = response.text
                title = extract_title(html, url)
                content = html_to_markdown(html, response.url, title)
                result["title"] = title
                result["content"] = content
                result["content_format"] = "markdown"
                result["status"] = "success"
                result["reason"] = ""
                result["excerpt"] = to_plain_excerpt(content)
                return result

            result["reason"] = f"HTTP {response.status_code}"
            if response.status_code in {404, 401, 403}:
                result["status"] = "failed"
                return result

            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
                continue

        except requests.exceptions.Timeout:
            result["reason"] = "Timeout"
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
                continue
        except requests.exceptions.ConnectionError as exc:
            result["reason"] = f"ConnectionError: {str(exc)[:120]}"
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
                continue
        except Exception as exc:  # noqa: BLE001
            result["reason"] = f"Exception: {str(exc)[:160]}"
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
                continue
        break

    result["status"] = "failed"
    return result


def write_mirror_file(item: dict, result: dict) -> str:
    filename = item["filename"]
    filepath = OUTPUT_DIR / filename
    tags = build_tags(item["source_url"])
    yaml_header = (
        "---\n"
        f"source_url: {yaml_quote(item['source_url'])}\n"
        f"fetched_at: {yaml_quote(result['fetched_at'])}\n"
        f"title: {yaml_quote(result['title'])}\n"
        f"content_format: {yaml_quote(result['content_format'])}\n"
        f"tags: {json.dumps(tags, ensure_ascii=False)}\n"
        "---\n\n"
    )
    filepath.write_text(yaml_header + result["content"], encoding="utf-8")
    return filename


def write_status_lists(records: list[dict]):
    generated_at = now_iso()
    success_lines = [
        "# DEEPCRAFT 已成功抓取 URL 清单",
        f"# 生成时间: {generated_at}",
        f"# 权威源: {AUTHORITATIVE_LIST}",
        "",
    ]
    missing_lines = [
        "# DEEPCRAFT 抓取失败 URL 清单",
        f"# 生成时间: {generated_at}",
        f"# 权威源: {AUTHORITATIVE_LIST}",
        "# 格式: URL | 原因 | HTTP",
        "",
    ]

    for record in records:
        if record["status"] == "success":
            success_lines.append(record["source_url"])
        else:
            code = record["http_code"] if record["http_code"] else "n/a"
            reason = record["reason"] or "Unknown error"
            missing_lines.append(f"{record['source_url']} | {reason} | HTTP {code}")

    SUCCESS_FILE.write_text("\n".join(success_lines) + "\n", encoding="utf-8")
    MISSING_FILE.write_text("\n".join(missing_lines) + "\n", encoding="utf-8")


def build_audit(items: list[dict], records: list[dict], written_files: set[str], removed_stale_files: list[str]) -> dict:
    success_count = sum(1 for record in records if record["status"] == "success")
    failed_count = len(records) - success_count
    unique_urls = len({item["source_url"] for item in items})
    coverage_checked = round(success_count / len(items) * 100, 1) if items else 0.0
    coverage_unique = round(len({record["source_url"] for record in records if record["status"] == "success"}) / unique_urls * 100, 1) if unique_urls else 0.0

    fetch_status = {}
    for item, record in zip(items, records):
        key = f"{item['checked_index']:03d}"
        fetch_status[key] = {
            "checked_index": item["checked_index"],
            "source_url": item["source_url"],
            "status": record["status"],
            "http_code": record["http_code"],
            "reason": record["reason"],
            "retries": record["retries"],
            "fetched_at": record["fetched_at"],
            "output_file": record["output_file"],
            "redirect_url": record["redirect_url"],
            "title": record["title"],
            "content_format": record["content_format"],
            "filename": item["filename"],
            "duplicate": item["duplicate"],
            "excerpt": record["excerpt"],
        }

    return {
        "audit_date": now_iso()[:10],
        "audited_at": now_iso(),
        "source_site": SOURCE_SITE,
        "authority_source": AUTHORITATIVE_LIST,
        "total_checked_urls": len(items),
        "total_unique_urls": unique_urls,
        "duplicate_url_count": len(items) - unique_urls,
        "success_count": success_count,
        "failed_count": failed_count,
        "written_html_files": len(written_files),
        "removed_stale_html_files": removed_stale_files,
        "coverage": {
            "checked_urls_percent": coverage_checked,
            "unique_urls_percent": coverage_unique,
        },
        "fetch_status": fetch_status,
    }


# ─── 主流程 ───────────────────────────────────────────────────────────────────
def main() -> int:
    if not URLS_FILE.exists():
        print(f"[错误] 未找到权威 URL 清单: {URLS_FILE}")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    items = read_checked_urls()
    if not items:
        print(f"[错误] {URLS_FILE} 中没有可抓取的 https:// URL")
        return 1

    removed_stale_files = []
    for filename in sorted({item["filename"] for item in items}):
        target = OUTPUT_DIR / filename
        if target.exists():
            target.unlink()
            removed_stale_files.append(f"ingest/html/{filename}")

    print(f"[镜像刷新] 读取到 {len(items)} 个 checked URL（唯一 {len({item['source_url'] for item in items})} 个）")
    print(f"[镜像刷新] 预清理当前 checked URL 对应旧镜像 {len(removed_stale_files)} 个\n")

    records = []
    written_files = set()

    for index, item in enumerate(items, 1):
        print(f"[{index:3d}/{len(items)}] {item['source_url']}")
        result = fetch_url(item["source_url"])

        output_file = ""
        if result["status"] == "success":
            try:
                filename = write_mirror_file(item, result)
                output_file = f"ingest/html/{filename}"
                written_files.add(filename)
                print(f"        ✓ success ({result['http_code']}) -> {filename}")
            except Exception as exc:  # noqa: BLE001
                result["status"] = "failed"
                result["reason"] = f"WriteError: {str(exc)[:160]}"
                print(f"        ✗ 写文件失败: {result['reason']}")
        else:
            print(f"        ✗ failed ({result['http_code']}) | {result['reason']}")

        records.append(
            {
                "source_url": item["source_url"],
                "status": result["status"],
                "http_code": result["http_code"],
                "reason": result["reason"],
                "retries": result["retries"],
                "fetched_at": result["fetched_at"],
                "output_file": output_file,
                "redirect_url": result["redirect_url"],
                "title": result["title"],
                "content_format": result["content_format"],
                "excerpt": result["excerpt"],
            }
        )
        time.sleep(REQUEST_DELAY)

    write_status_lists(records)
    audit = build_audit(items, records, written_files, removed_stale_files)
    AUDIT_FILE.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    success_count = audit["success_count"]
    failed_count = audit["failed_count"]
    print("\n" + "=" * 64)
    print(f"[完成] checked URL 总数: {audit['total_checked_urls']}")
    print(f"       唯一 URL 数:   {audit['total_unique_urls']}")
    print(f"       成功:         {success_count}")
    print(f"       失败:         {failed_count}")
    print(f"       写入 html:    {audit['written_html_files']}")
    print(f"       覆盖率(checked): {audit['coverage']['checked_urls_percent']}%")
    print(f"       覆盖率(unique):  {audit['coverage']['unique_urls_percent']}%")
    print(f"       success list: {SUCCESS_FILE}")
    print(f"       missing list: {MISSING_FILE}")
    print(f"       audit file:   {AUDIT_FILE}")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
