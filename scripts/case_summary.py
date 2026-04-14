from __future__ import annotations

from typing import Any
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.search_utils import normalize_space, split_sentences


ACTION_HINTS = (
    "please",
    "check",
    "confirm",
    "verify",
    "try",
    "refer",
    "monitor",
    "change",
    "replace",
    "remove",
    "use",
    "share",
    "add",
)


def first_meaningful_sentences(text: str, count: int = 4) -> str:
    sentences = split_sentences(text)
    return " ".join(sentences[:count])


def extract_support_actions(messages: list[dict[str, str]], limit: int = 8) -> list[str]:
    actions: list[str] = []
    for msg in messages:
        if msg.get("visibility", "").lower() != "external":
            continue
        for sentence in split_sentences(msg.get("body", "")):
            lower = sentence.lower()
            if any(hint in lower for hint in ACTION_HINTS):
                actions.append(sentence)
    deduped: list[str] = []
    seen: set[str] = set()
    for item in actions:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
        if len(deduped) >= limit:
            break
    return deduped


def extract_customer_observations(messages: list[dict[str, str]], limit: int = 5) -> list[str]:
    observations: list[str] = []
    for msg in messages:
        if msg.get("visibility", "").lower() != "customer":
            continue
        body = normalize_space(msg.get("body", ""))
        if not body:
            continue
        observations.append(first_meaningful_sentences(body, count=3))
        if len(observations) >= limit:
            break
    return observations


def infer_resolution(status: str, messages: list[dict[str, str]]) -> str:
    status_norm = status.lower()
    if status_norm in {"closed", "resolved"}:
        for msg in messages[:4]:
            body = msg.get("body", "").lower()
            if "issue is resolved" in body or "you can resolve" in body:
                return "状态已关闭/解决，讨论中有明确结案语句。"
        return "状态已关闭/解决，但 discussion 中未看到非常明确的最终根因闭环。"
    return f"当前状态为 {status}，case 仍可能需要继续跟进。"


def infer_open_items(status: str, description: str, actions: list[str]) -> list[str]:
    items: list[str] = []
    if status.lower() in {"closed", "resolved"} and not actions:
        items.append("虽然 case 已关闭，但当前记录里没有提取到明确的工程调试动作。")
    if "Additional Questions" in description or "Request for support" in description:
        items.append("描述中包含额外问题/支持请求，需确认这些子问题是否都已闭环。")
    return items


def summarize_case_payload(payload: dict[str, Any]) -> dict[str, Any]:
    description = normalize_space(payload.get("description", ""))
    messages = payload.get("discussion_messages", []) or []
    actions = extract_support_actions(messages)
    observations = extract_customer_observations(messages)
    resolution_note = infer_resolution(payload.get("status", ""), messages)
    open_items = infer_open_items(payload.get("status", ""), description, actions)

    return {
        "problem": first_meaningful_sentences(description, count=5),
        "customer_observations": observations,
        "support_recommendations": actions,
        "resolution_note": resolution_note,
        "open_items": open_items,
    }
