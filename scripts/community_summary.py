from __future__ import annotations

from pathlib import Path
import re
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
    "use",
    "update",
    "install",
    "rebuild",
    "change",
    "switch",
)

NOISE_MARKERS = (
    "solved! go to solution",
    "view all forum discussions",
    "previous topic",
    "next topic",
    "need help purchasing",
    "how useful is this solution",
    "moderator",
    "accepted solution",
    "like share",
    "topics:",
)


def trim_text(text: str, limit: int = 240) -> str:
    value = normalize_space(text)
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip(" ,;:") + "..."


def strip_boilerplate(text: str) -> str:
    value = normalize_space(text)
    if not value:
        return ""
    for marker in NOISE_MARKERS:
        idx = value.lower().find(marker)
        if idx > 0:
            value = value[:idx].strip()
    value = value.replace("Warm Regards,", "").replace("Warm regards,", "")
    value = value.replace("Best regards,", "").replace("Best Regards,", "")
    return normalize_space(value)


def split_fragments(text: str) -> list[str]:
    value = strip_boilerplate(text)
    if not value:
        return []
    parts = split_sentences(value)
    if len(parts) <= 1:
        parts = [normalize_space(part) for part in re.split(r"\s+(?=\d+\.\s+)", value) if normalize_space(part)]
    return [part for part in parts if is_meaningful_fragment(part)]


def is_meaningful_fragment(text: str) -> bool:
    value = normalize_space(text)
    if len(value) < 12:
        return False
    lowered = value.lower()
    return not any(marker in lowered for marker in NOISE_MARKERS)


def similarity_key(text: str) -> str:
    return normalize_space(text).lower()


def looks_like_duplicate(candidate: str, reference: str) -> bool:
    candidate_key = similarity_key(candidate)
    reference_key = similarity_key(reference)
    if not candidate_key or not reference_key:
        return False
    if candidate_key == reference_key:
        return True
    short = candidate_key if len(candidate_key) < len(reference_key) else reference_key
    long = reference_key if len(candidate_key) < len(reference_key) else candidate_key
    return len(short) >= 40 and short in long


def first_relevant_fragments(text: str, count: int = 3, exclude: tuple[str, ...] = ()) -> str:
    selected: list[str] = []
    for fragment in split_fragments(text):
        if any(looks_like_duplicate(fragment, item) for item in exclude if item):
            continue
        selected.append(fragment)
        if len(selected) >= count:
            break
    return trim_text(" ".join(selected), limit=320)


def first_meaningful_sentences(text: str, count: int = 4) -> str:
    sentences = split_sentences(text)
    return " ".join(sentences[:count])


def extract_recommendations(texts: list[str], limit: int = 8) -> list[str]:
    actions: list[str] = []
    for text in texts:
        for sentence in split_fragments(text):
            lowered = sentence.lower()
            if any(hint in lowered for hint in ACTION_HINTS):
                actions.append(trim_text(sentence, limit=220))
    out: list[str] = []
    seen: set[str] = set()
    for item in actions:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
        if len(out) >= limit:
            break
    return out


def summarize_community_payload(payload: dict) -> dict:
    title = strip_boilerplate(payload.get("title", ""))
    question_body = normalize_space(payload.get("question_body", ""))
    article_body = normalize_space(payload.get("article_body", ""))
    primary_body = normalize_space(payload.get("primary_body", ""))
    accepted_answer = normalize_space(payload.get("accepted_answer", ""))
    replies = [normalize_space(item) for item in payload.get("reply_snippets", []) if normalize_space(item)]

    filtered_replies = [reply for reply in replies if not looks_like_duplicate(reply, question_body)]
    evidence_pool = [accepted_answer, *filtered_replies, primary_body]
    recommendations = extract_recommendations([text for text in evidence_pool if text])
    open_items: list[str] = []
    if payload.get("page_kind") == "forum-thread" and not accepted_answer:
        open_items.append("当前帖子未提取到明确采纳答案，需要结合回复和本地证据继续判断。")
    if not recommendations:
        open_items.append("正文里未提取到明确动作建议，可能仍需人工阅读全文。")

    return {
        "problem": trim_text(title or first_relevant_fragments(question_body or primary_body, count=2), limit=240),
        "phenomena": first_relevant_fragments(question_body, count=3, exclude=(title,)),
        "resolution_hint": first_relevant_fragments(
            accepted_answer or article_body or primary_body,
            count=2,
            exclude=(title, question_body),
        ),
        "recommendations": recommendations,
        "open_items": open_items,
    }
