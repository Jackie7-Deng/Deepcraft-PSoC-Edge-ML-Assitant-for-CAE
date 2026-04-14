from __future__ import annotations

import argparse
import html
import json
import re
import sys
from typing import Any
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.community_summary import summarize_community_payload


def pick_context(browser):
    if browser.contexts:
        return browser.contexts[0]
    raise RuntimeError("未找到可用的浏览器上下文，请先用启动脚本打开浏览器。")


def clean_text(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def iter_nodes(node: Any):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from iter_nodes(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_nodes(item)


def infer_page_kind(url: str) -> str:
    if "/td-p/" in url:
        return "forum-thread"
    if "/ta-p/" in url:
        return "knowledge-base-article"
    return "unknown"


def extract_from_jsonld(parsed_scripts: list[Any]) -> dict[str, str]:
    result = {
        "question_or_article": "",
        "accepted_answer": "",
        "article_body": "",
    }

    for node in iter_nodes(parsed_scripts):
        if not isinstance(node, dict):
            continue

        node_type = str(node.get("@type", ""))
        if not result["question_or_article"]:
            if node.get("headline"):
                result["question_or_article"] = clean_text(str(node["headline"]))
            elif node.get("name"):
                result["question_or_article"] = clean_text(str(node["name"]))

        if not result["accepted_answer"]:
            accepted = node.get("acceptedAnswer")
            if isinstance(accepted, dict) and accepted.get("text"):
                result["accepted_answer"] = clean_text(str(accepted["text"]))

        if not result["article_body"]:
            if node.get("articleBody"):
                result["article_body"] = clean_text(str(node["articleBody"]))
            elif node_type == "Answer" and node.get("text"):
                result["article_body"] = clean_text(str(node["text"]))

    return result


def extract_dom_content(page) -> dict[str, Any]:
    return page.evaluate(
        """
        () => {
          const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim();
          const title = normalize(document.querySelector('h1')?.innerText || document.title || '');
          const messageBodies = Array.from(
            document.querySelectorAll('.lia-message-body-content, .lia-message-body, article')
          )
            .map(el => normalize(el.innerText || el.textContent || ''))
            .filter(Boolean);
          const replyBodies = Array.from(
            document.querySelectorAll('.lia-message-view-display .lia-message-body-content, .lia-message-view-display .lia-message-body')
          )
            .map(el => normalize(el.innerText || el.textContent || ''))
            .filter(Boolean);
          const accepted = Array.from(
            document.querySelectorAll('.lia-message-solution, .lia-component-solution, .lia-message-solution-body')
          )
            .map(el => normalize(el.innerText || el.textContent || ''))
            .filter(Boolean);
          const bodyText = normalize(document.body?.innerText || '');
          return {
            title,
            message_bodies: messageBodies.slice(0, 12),
            reply_bodies: replyBodies.slice(0, 12),
            accepted_blocks: accepted.slice(0, 6),
            body_excerpt: bodyText.slice(0, 6000)
          };
        }
        """
    )


def extract_parsed_jsonld(page) -> list[Any]:
    return page.evaluate(
        """
        () => {
          const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
          const parsed = [];
          for (const script of scripts) {
            try {
              parsed.push(JSON.parse(script.textContent || ''));
            } catch (e) {
            }
          }
          return parsed;
        }
        """
    )


def read_article(cdp_url: str, url: str) -> dict[str, Any]:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = pick_context(browser)
        page = context.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(5000)

            jsonld = extract_parsed_jsonld(page)
            dom = extract_dom_content(page)
            jsonld_content = extract_from_jsonld(jsonld)

            question_body = dom["message_bodies"][0] if dom["message_bodies"] else ""
            article_body = jsonld_content["article_body"]
            accepted = jsonld_content["accepted_answer"] or (dom["accepted_blocks"][0] if dom["accepted_blocks"] else "")
            primary_body = article_body or question_body

            payload = {
                "url": page.url,
                "page_title": page.title(),
                "page_kind": infer_page_kind(page.url),
                "title": jsonld_content["question_or_article"] or dom["title"],
                "question_body": question_body,
                "article_body": article_body,
                "primary_body": primary_body,
                "accepted_answer": accepted,
                "reply_snippets": dom["reply_bodies"][:5],
                "body_excerpt": dom["body_excerpt"],
            }
            payload["summary"] = summarize_community_payload(payload)
            return payload

        finally:
            page.close()
            browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="通过已打开的 Chrome/Edge 会话读取 Infineon Community 帖子或 KBA 正文。")
    parser.add_argument("url", help="Community 帖子或 KBA 链接。")
    parser.add_argument("--cdp-url", default="http://127.0.0.1:9222", help="浏览器远程调试地址。")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出。")
    args = parser.parse_args()

    try:
        payload = read_article(args.cdp_url, args.url)
    except Exception as exc:
        print(f"读取失败：{exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"标题：{payload['title']}")
    print(f"页面类型：{payload['page_kind']}")
    print(f"地址：{payload['url']}")
    print("")
    if payload["question_body"] and payload["page_kind"] == "forum-thread":
        print("问题摘要：")
        print(payload["question_body"])
        print("")
    if payload["primary_body"]:
        print("正文摘要：")
        print(payload["primary_body"])
        print("")
    if payload["accepted_answer"]:
        print("采纳答案：")
        print(payload["accepted_answer"])
        print("")
    if payload.get("summary"):
        print("结构化摘要：")
        print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
        print("")
    if payload["reply_snippets"]:
        print("回复摘录：")
        for idx, reply in enumerate(payload["reply_snippets"], start=1):
            print(f"{idx}. {reply[:240]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
