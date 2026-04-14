from __future__ import annotations

from dataclasses import dataclass
from typing import Any


SOURCE_BASE_SCORE = {
    "official_pdf": 10,
    "readme": 9,
    "source_code": 9,
    "knowledge": 7,
    "community": 5,
    "case": 5,
    "inference": 2,
}


@dataclass
class EvidenceDecision:
    citation: str
    source_type: str
    score: int
    reasons: list[str]


def arbitrate(items: list[dict[str, Any]]) -> list[EvidenceDecision]:
    decisions: list[EvidenceDecision] = []
    for item in items:
        source_type = str(item.get("source_type", "inference"))
        score = SOURCE_BASE_SCORE.get(source_type, 1)
        reasons: list[str] = [f"base:{source_type}"]
        if item.get("has_precise_locator"):
            score += 3
            reasons.append("precise-locator")
        if item.get("platform_exact_match"):
            score += 3
            reasons.append("platform-match")
        if item.get("version_exact_match"):
            score += 2
            reasons.append("version-match")
        if item.get("is_summary_only"):
            score -= 3
            reasons.append("summary-only")
        decisions.append(
            EvidenceDecision(
                citation=str(item.get("citation", "")),
                source_type=source_type,
                score=score,
                reasons=reasons,
            )
        )
    return sorted(decisions, key=lambda item: (-item.score, item.citation))
