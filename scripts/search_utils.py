from __future__ import annotations

import re
from typing import Iterable


STOPWORDS = {
    "the", "a", "an", "and", "or", "for", "to", "of", "in", "on", "with",
    "regarding", "issue", "issues", "problem", "question", "help", "support",
    "current", "search", "community", "case", "system", "please", "about",
    "related", "relevant", "need", "this", "that", "project", "example",
    "using", "use", "from", "into",
}

GENERIC_QUERY_MARKERS = {
    "this issue", "the issue", "current issue", "this problem", "the problem",
    "current problem", "this question", "the question", "search this issue",
    "search this problem", "此问题", "这个问题", "当前问题", "这个故障", "这个案例",
}

NATURAL_LANGUAGE_MARKERS = {
    "why", "how", "what", "when", "where", "which", "can", "does", "should",
    "please", "help", "error", "failed", "fail", "support", "requirement",
    "requirements", "format", "formats", "compatible", "compatibility",
    "为什么", "怎么", "如何", "请", "报错", "错误", "要求", "格式", "支持", "兼容",
}

SEMANTIC_HINTS = (
    ("error", ("报错", "错误", "异常", "error", "failed", "fail", "failure")),
    ("model format", ("格式", "format", "formats")),
    ("compatibility", ("兼容", "compatible", "compatibility", "version", "版本")),
    ("unsupported operator", ("算子", "operator", "operators")),
    ("quantization", ("量化", "quantization")),
)

# PSoC Edge DeepCraft AI 专属词表
CHIP_TERMS = [
    "PSoC Edge", "PSOC Edge", "PSoC 6", "PSOC 6", "PSoC", "PSOC",
    "KIT_PSE84_EVAL", "KIT_PSE84_AI", "CY8CKIT-062S2-AI",
    "CY8CKIT-062S2-43012", "CY8C6xx", "CY8C62", "E84", "E8x",
    "DeepCraft", "DEEPCRAFT", "PSOC_EDGE",
]

ML_FRAMEWORK_TERMS = [
    "Imagimob", "MTBML", "MTB-ML", "ModusToolbox ML",
    "TensorFlow Lite", "TFLite", "TF Lite Micro", "TFLM",
    "Imagimob Studio", "Imagimob Deploy", "DEEPCRAFT Studio",
    "DEEPCRAFT Model Converter", "Model Converter",
    "machine learning", "ML model", "neural network",
    "inference", "quantization", "int8",
    "NPU", "neural processing unit", "NNLite", "Ethos-U55",
]

MEMORY_TERMS = [
    "memory placement", "memory map", "memory usage", "memory layout",
    "RRAM", "SRAM", "System SRAM", "SoCMEM", "ITCM", "DTCM",
    "XIP", "MMIO", "SMIF", "external flash", "external RAM",
    "Octal SPI", "QSPI", "OSPI", "HyperBus", "linker script",
    "VMA", "LMA", "tensor arena", "buffer", "stack", "heap",
    "RAM", "Flash", "memory limit", "size limitation", "flash size", "RAM size",
    "memory report", "memoryreport",
]

DEMO_TERMS = [
    "Face ID", "face detection", "face recognition",
    "PSOC_Edge_Machine_Learning_Face_ID_Demo",
    "Machine_Learning_Imagimob_MTBML_Deploy",
    "DEEPCRAFT data collection", "DEEPCRAFT deploy motion", "DEEPCRAFT deploy vision",
    "image classification", "person detection",
    "ML Deploy", "wake word", "keyword detection",
    "anomaly detection", "gesture recognition",
]

TOOLCHAIN_TERMS = [
    "ModusToolbox", "MTB", "Eclipse IDE", "VS Code",
    "make build", "make program", "make clean",
    "make getlibs",
    "BSP", "board support package",
    "cy_retarget_io", "cybsp_init",
    "FreeRTOS", "RTOS",
    "GCC_ARM", "LLVM_ARM", "ARM Compiler 6", "armclang",
    "OpenOCD", "J-Link", "KitProg", "KitProg3",
    "ml-configurator", "Machine Learning Pack", "memoryreport",
]

SYMPTOM_TERMS = [
    "build failed", "compilation error", "linker error",
    "undefined reference", "out of memory", "heap overflow",
    "model not loading", "inference failed", "wrong prediction",
    "low accuracy", "face not detected", "false positive",
    "flash overflow", "RAM overflow",
    "HardFault", "assert failed",
    "USB not recognized", "KitProg not detected",
    "programming failed", "erase failed",
    "model size too large", "quantization error",
    "MTBML error", "Imagimob error",
    "camera not working", "display blank", "no UART output",
    "unsupported operator", "operator not supported", "size limitation",
]

PLATFORM_TERMS = [
    "Windows 10", "Windows 11",
    "Ubuntu", "Linux", "macOS",
    "ModusToolbox 3.0", "ModusToolbox 3.1", "ModusToolbox 3.2", "ModusToolbox 3.6", "ModusToolbox 3.8",
    "VS Code", "Eclipse", "Command line",
]

VERSION_TERMS = [
    "EAP", "BSP 1.0.0", "BSP 1.1.0", "ML Pack 2.0", "ML Pack 3.0",
    "ModusToolbox 3.0", "ModusToolbox 3.1", "ModusToolbox 3.2", "ModusToolbox 3.3",
    "ModusToolbox 3.6", "ModusToolbox 3.7", "ModusToolbox 3.8",
]

PERIPHERAL_TERMS = [
    "camera", "OV7675", "OS02F10", "Logitech C920", "image sensor",
    "PDM microphone", "IMU", "accelerometer", "gyroscope",
    "I2C", "SPI", "UART", "USB", "DSI", "DVP",
    "DMA", "SMIF", "QSPI", "LCD", "display",
]

SYMPTOM_GROUPS = {
    "build": (
        "build failed", "compilation error", "linker error", "undefined reference", "flash overflow", "RAM overflow",
    ),
    "deploy": (
        "programming failed", "erase failed", "KitProg not detected", "USB not recognized", "no UART output",
    ),
    "inference": (
        "model not loading", "inference failed", "wrong prediction", "low accuracy", "quantization error",
    ),
    "vision": (
        "face not detected", "false positive", "camera not working", "display blank",
    ),
    "runtime": (
        "HardFault", "assert failed", "out of memory", "heap overflow", "model size too large",
    ),
    "memory": (
        "memory placement", "memory map", "linker error", "flash overflow", "RAM overflow",
        "tensor arena", "stack overflow", "heap overflow", "XIP",
        "memory limit", "size limitation", "flash size", "RAM size",
    ),
}


TERM_BUCKETS = (
    CHIP_TERMS,
    DEMO_TERMS,
    ML_FRAMEWORK_TERMS,
    MEMORY_TERMS,
    TOOLCHAIN_TERMS,
    VERSION_TERMS,
    PLATFORM_TERMS,
    PERIPHERAL_TERMS,
)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_external_search_query(text: str | None) -> str:
    value = normalize_space(text or "")
    if not value:
        return ""
    value = re.sub(r"(?<=\w)\s*\+\s*(?=\w)", " ", value)
    value = re.sub(r"(?<=\w)\s*[|,;]\s*(?=\w)", " ", value)
    value = re.sub(r"[\"“”‘’()\[\]{}]+", " ", value)
    return normalize_space(value)


def contains_cjk(text: str | None) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def normalize_query(text: str) -> str:
    return normalize_space(text).lower()


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9_+#.-]+", normalize_query(text))
    return [token for token in tokens if token and token not in STOPWORDS]


def dedupe_keep_order(items: Iterable[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        value = normalize_space(str(item))
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def _first_match(text: str, terms: Iterable[str]) -> str:
    norm = normalize_query(text)
    for term in terms:
        if _contains_term(norm, term):
            return term
    return ""


def _contains_term(normalized_text: str, term: str) -> bool:
    escaped = re.escape(term.lower())
    pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    return re.search(pattern, normalized_text) is not None


def detect_chip_protocol(text: str) -> tuple[str, str]:
    chip = _first_match(text, CHIP_TERMS)
    focus = _first_match(text, DEMO_TERMS) or _first_match(text, ML_FRAMEWORK_TERMS)
    return chip, focus


def detect_context_hints(text: str) -> list[str]:
    norm = normalize_query(text)
    found: list[str] = []
    for bucket in (ML_FRAMEWORK_TERMS, MEMORY_TERMS, TOOLCHAIN_TERMS, VERSION_TERMS, PLATFORM_TERMS, PERIPHERAL_TERMS):
        for term in bucket:
            if _contains_term(norm, term):
                found.append(term)
    return dedupe_keep_order(found)


def detect_symptom_groups(text: str) -> list[str]:
    norm = normalize_query(text)
    groups: list[str] = []
    for name, phrases in SYMPTOM_GROUPS.items():
        if any(_contains_term(norm, phrase) for phrase in phrases):
            groups.append(name)
    return groups


def detect_primary_symptom_phrase(text: str) -> str:
    norm = normalize_query(text)
    for phrases in SYMPTOM_GROUPS.values():
        for phrase in phrases:
            if _contains_term(norm, phrase):
                return phrase
    for term in SYMPTOM_TERMS:
        if _contains_term(norm, term):
            return term
    return ""


def top_symptom_phrases(text: str, limit_per_group: int = 2) -> list[str]:
    norm = normalize_query(text)
    out: list[str] = []
    for group in detect_symptom_groups(text):
        phrases = SYMPTOM_GROUPS[group]
        matches = [phrase for phrase in phrases if _contains_term(norm, phrase)]
        out.extend(matches[:limit_per_group] if matches else list(phrases[:limit_per_group]))
    if not out:
        primary = detect_primary_symptom_phrase(text)
        if primary:
            out.append(primary)
    return dedupe_keep_order(out)


def is_generic_search_request(query: str | None) -> bool:
    if not query:
        return True
    normalized = normalize_query(query)
    if not normalized:
        return True
    if normalized in GENERIC_QUERY_MARKERS:
        return True
    if normalized.startswith("search ") and len(tokenize_query(normalized)) <= 2:
        return True
    return False


def looks_like_natural_language_query(query: str | None) -> bool:
    if not query:
        return False
    normalized = normalize_external_search_query(query)
    if not normalized:
        return False
    tokens = tokenize_query(normalized)
    lowered = normalized.lower()
    if len(tokens) >= 7:
        return True
    if contains_cjk(normalized):
        return True
    if any(marker in lowered for marker in NATURAL_LANGUAGE_MARKERS) and len(tokens) >= 4:
        return True
    if any(ch in normalized for ch in ("?", "？", "!", "！", ":", "：")) and len(tokens) >= 4:
        return True
    return False


def infer_semantic_hints(text: str | None, limit: int = 2) -> list[str]:
    source = normalize_external_search_query(text or "")
    lowered = source.lower()
    hints: list[str] = []
    for hint, markers in SEMANTIC_HINTS:
        if any(marker in source or marker in lowered for marker in markers):
            hints.append(hint)
    return dedupe_keep_order(hints)[:limit]


def condense_problem_statement(problem_text: str, mode: str = "community") -> str:
    source = normalize_external_search_query(problem_text)
    if not source:
        return ""
    chip, focus = detect_chip_protocol(source)
    symptoms = top_symptom_phrases(source, limit_per_group=1)[:2]
    semantic_hints = infer_semantic_hints(source, limit=2)
    frameworks = _matches_from_bucket(source, ML_FRAMEWORK_TERMS, limit=2)
    memories = _matches_from_bucket(source, MEMORY_TERMS, limit=1)
    toolchains = _matches_from_bucket(source, TOOLCHAIN_TERMS, limit=1)
    versions = _matches_from_bucket(source, VERSION_TERMS, limit=1)
    platforms = _matches_from_bucket(source, PLATFORM_TERMS, limit=1)
    peripherals = _matches_from_bucket(source, PERIPHERAL_TERMS, limit=1)

    query_parts = dedupe_keep_order([chip, focus, *symptoms[:1], *semantic_hints[:1], *frameworks[:1], *toolchains[:1], *memories[:1]])
    if len(query_parts) < 2:
        query_parts = dedupe_keep_order([chip, focus, *frameworks[:1], *semantic_hints[:2], *toolchains[:1], *peripherals[:1], *platforms[:1], *versions[:1]])
    if len(query_parts) < 2:
        query_parts = _fallback_seed_terms(source)[:5]
    return normalize_external_search_query(" ".join(query_parts[:5]))


def derive_search_seed(query: str | None, problem_text: str | None = None, mode: str = "community") -> str:
    normalized_query = normalize_external_search_query(query or "")
    if normalized_query and not is_generic_search_request(normalized_query):
        if looks_like_natural_language_query(normalized_query):
            condensed_query = condense_problem_statement(normalized_query, mode=mode)
            if condensed_query:
                return condensed_query
        return normalized_query
    if problem_text:
        condensed = condense_problem_statement(problem_text, mode=mode)
        if condensed:
            return normalize_external_search_query(condensed)
    return normalized_query


def _matches_from_bucket(text: str, bucket: Iterable[str], limit: int = 2) -> list[str]:
    norm = normalize_query(text)
    found = [term for term in bucket if _contains_term(norm, term)]
    return dedupe_keep_order(found)[:limit]


def _fallback_seed_terms(seed: str, limit: int = 6) -> list[str]:
    return dedupe_keep_order(tokenize_query(seed))[:limit]


def build_psoc_edge_queries(
    user_question: str,
    context: dict | None = None,
    max_queries: int = 4,
    source_text: str | None = None,
) -> list[str]:
    seed = normalize_external_search_query(user_question)
    if not seed:
        return []

    analysis_text = normalize_external_search_query(source_text or seed)
    chip, focus = detect_chip_protocol(analysis_text)
    toolchains = _matches_from_bucket(analysis_text, TOOLCHAIN_TERMS, limit=2)
    frameworks = _matches_from_bucket(analysis_text, ML_FRAMEWORK_TERMS, limit=2)
    memories = _matches_from_bucket(analysis_text, MEMORY_TERMS, limit=2)
    versions = _matches_from_bucket(analysis_text, VERSION_TERMS, limit=1)
    platforms = _matches_from_bucket(analysis_text, PLATFORM_TERMS, limit=1)
    peripherals = _matches_from_bucket(analysis_text, PERIPHERAL_TERMS, limit=2)
    symptoms = top_symptom_phrases(analysis_text, limit_per_group=1)[:2]
    semantic_hints = infer_semantic_hints(analysis_text, limit=2)
    seed_terms = _fallback_seed_terms(analysis_text)

    context = context or {}
    if context.get("chip") and not chip:
        chip = context["chip"]
    if context.get("focus") and not focus:
        focus = context["focus"]

    variants: list[str] = [seed]

    # 第一轮：芯片词 / Demo 名称 + 主症状词
    round1_parts = dedupe_keep_order([chip, focus, *symptoms[:1], *semantic_hints[:1]])
    if len(round1_parts) < 2:
        round1_parts = dedupe_keep_order([chip, focus, *frameworks[:1], *memories[:1], *symptoms[:1], *semantic_hints[:1]])
    if len(round1_parts) < 2:
        round1_parts = seed_terms[:4]
    variants.append(normalize_external_search_query(" ".join(round1_parts)))

    # 第二轮：补充工具链词 / ML 框架词
    round2 = normalize_external_search_query(
        " ".join(
            dedupe_keep_order([chip, focus, *symptoms[:2], *semantic_hints[:2], *frameworks[:1], *memories[:1], *toolchains[:1]])
        )
    )
    if len(round2.split()) < 2:
        round2 = normalize_external_search_query(" ".join(seed_terms[:5]))
    if round2:
        variants.append(round2)

    # 第三轮：补充平台词 / 外设词
    round3 = normalize_external_search_query(
        " ".join(
            dedupe_keep_order(
                [chip, focus, *symptoms[:2], *frameworks[:1], *memories[:1], *toolchains[:1], *versions[:1], *platforms[:1], *peripherals[:1]]
                + semantic_hints[:2]
            )
        )
    )
    if len(round3.split()) < 2:
        round3 = normalize_external_search_query(" ".join(seed_terms[:6]))
    if round3:
        variants.append(round3)

    return dedupe_keep_order(variants)[:max_queries]


def build_psoc_edge_query_plan(
    user_question: str,
    context: dict | None = None,
    max_queries: int = 4,
    source_text: str | None = None,
) -> dict[str, object]:
    analysis_text = normalize_external_search_query(source_text or user_question)
    seed = derive_search_seed(user_question, problem_text=source_text)
    chip, focus = detect_chip_protocol(analysis_text)
    return {
        "original_input": normalize_external_search_query(user_question),
        "seed_query": seed,
        "chip": chip,
        "focus": focus,
        "symptoms": top_symptom_phrases(analysis_text, limit_per_group=1)[:3],
        "semantic_hints": infer_semantic_hints(analysis_text, limit=3),
        "frameworks": _matches_from_bucket(analysis_text, ML_FRAMEWORK_TERMS, limit=3),
        "memory_terms": _matches_from_bucket(analysis_text, MEMORY_TERMS, limit=3),
        "toolchain_terms": _matches_from_bucket(analysis_text, TOOLCHAIN_TERMS, limit=3),
        "version_terms": _matches_from_bucket(analysis_text, VERSION_TERMS, limit=2),
        "platform_terms": _matches_from_bucket(analysis_text, PLATFORM_TERMS, limit=2),
        "peripheral_terms": _matches_from_bucket(analysis_text, PERIPHERAL_TERMS, limit=3),
        "queries": build_psoc_edge_queries(seed, context=context, max_queries=max_queries, source_text=analysis_text),
    }


def build_case_query_variants(query: str, max_queries: int = 4) -> list[str]:
    return build_psoc_edge_queries(query, max_queries=max_queries)


def build_case_query_variants_from_problem(query: str | None, problem_text: str | None = None, max_queries: int = 4) -> list[str]:
    seed = derive_search_seed(query, problem_text=problem_text, mode="case")
    source = normalize_external_search_query(problem_text or query or seed or "")
    return build_psoc_edge_queries(seed or source, max_queries=max_queries, source_text=source)


def build_community_query_variants(query: str | None, problem_text: str | None = None, max_queries: int = 4) -> list[str]:
    seed = derive_search_seed(query, problem_text=problem_text, mode="community")
    source = normalize_external_search_query(problem_text or query or seed or "")
    return build_psoc_edge_queries(seed or source, max_queries=max_queries, source_text=source)


def important_terms_for_query(query: str, queries_tried: list[str] | None = None) -> list[str]:
    terms: list[str] = []
    for item in [query] + (queries_tried or []):
        if not item:
            continue
        chip, focus = detect_chip_protocol(item)
        symptom = detect_primary_symptom_phrase(item)
        terms.extend([term for term in (chip, focus, symptom) if term])
        terms.extend(_matches_from_bucket(item, TOOLCHAIN_TERMS, limit=2))
        terms.extend(_matches_from_bucket(item, ML_FRAMEWORK_TERMS, limit=2))
        terms.extend(_matches_from_bucket(item, MEMORY_TERMS, limit=2))
        terms.extend(_matches_from_bucket(item, VERSION_TERMS, limit=1))
        terms.extend(_matches_from_bucket(item, PLATFORM_TERMS, limit=1))
        terms.extend(_matches_from_bucket(item, PERIPHERAL_TERMS, limit=2))
        terms.extend(tokenize_query(item))
    return dedupe_keep_order(terms)[:24]


def _score_term(term: str) -> int:
    low = term.lower()
    if any(chip.lower() == low or chip.lower() in low for chip in CHIP_TERMS):
        return 12
    if any(demo.lower() == low or demo.lower() in low for demo in DEMO_TERMS):
        return 10
    if any(sym.lower() == low or sym.lower() in low for sym in SYMPTOM_TERMS):
        return 8
    if any(framework.lower() == low or framework.lower() in low for framework in ML_FRAMEWORK_TERMS):
        return 6
    if any(memory.lower() == low or memory.lower() in low for memory in MEMORY_TERMS):
        return 6
    if any(tool.lower() == low or tool.lower() in low for tool in TOOLCHAIN_TERMS):
        return 5
    if any(version.lower() == low or version.lower() in low for version in VERSION_TERMS):
        return 4
    if any(peripheral.lower() == low or peripheral.lower() in low for peripheral in PERIPHERAL_TERMS):
        return 4
    if any(platform.lower() == low or platform.lower() in low for platform in PLATFORM_TERMS):
        return 3
    return 2


def score_text_match(title: str, body: str, query: str, queries_tried: list[str] | None = None) -> tuple[int, list[str]]:
    title_norm = normalize_query(title)
    body_norm = normalize_query(body)
    combined = f"{title_norm} {body_norm}"
    score = 0
    reasons: list[str] = []
    for term in important_terms_for_query(query, queries_tried):
        low = term.lower()
        weight = _score_term(term)
        if low in title_norm:
            score += weight + 4
            reasons.append(f"title:{term}")
        elif low in combined:
            score += weight
            reasons.append(f"text:{term}")
    return score, dedupe_keep_order(reasons)[:12]


def score_case_result(result: dict, query: str, queries_tried: list[str] | None = None) -> tuple[int, list[str]]:
    subject = normalize_query(result.get("subject", ""))
    description = normalize_query(result.get("description", ""))
    combined = f"{subject} {description}"
    score = 0
    reasons: list[str] = []
    for term in important_terms_for_query(query, queries_tried):
        low = term.lower()
        weight = _score_term(term)
        if low in subject:
            score += weight + 4
            reasons.append(f"subject:{term}")
        elif low in combined:
            score += weight
            reasons.append(f"text:{term}")
    if result.get("case_number", "").startswith("IFX-"):
        score += 1
    return score, dedupe_keep_order(reasons)[:12]


def _community_source_adjustment(url: str) -> tuple[int, str]:
    normalized = normalize_query(url)
    if not normalized:
        return 0, ""
    if "/t5/" in normalized and any(marker in normalized for marker in ("/m-p/", "/td-p/", "/kb-p/")):
        return 10, "source:community-thread"
    if "/t5/" in normalized:
        return 6, "source:community-page"
    if any(marker in normalized for marker in ("docs.infineon.com", "documentation.infineon.com", ".pdf", "/applicationnotes/", "/user-guides/")):
        return -8, "source:document"
    if "github.com/" in normalized:
        return -5, "source:github"
    if "infineon.com" in normalized and "/cms/" in normalized:
        return -4, "source:product-page"
    return 0, ""


def score_community_result(result: dict, query: str, queries_tried: list[str] | None = None) -> tuple[int, list[str]]:
    score, reasons = score_text_match(
        str(result.get("title", "")),
        str(result.get("excerpt", "")),
        query,
        queries_tried,
    )
    source_delta, source_reason = _community_source_adjustment(str(result.get("url", "")))
    score += source_delta
    if source_reason:
        reasons.append(source_reason)
    return score, dedupe_keep_order(reasons)[:12]


def score_result_set_quality(
    results: list[dict],
    query: str,
    queries_tried: list[str] | None = None,
    *,
    title_key: str = "title",
    body_key: str = "excerpt",
    url_key: str | None = None,
) -> float:
    if not results:
        return 0.0

    top_scores: list[int] = []
    for item in results[:5]:
        if "score" in item and isinstance(item["score"], (int, float)):
            top_scores.append(int(item["score"]))
            continue
        score, _reasons = score_text_match(
            str(item.get(title_key, "")),
            str(item.get(body_key, "")),
            query,
            queries_tried,
        )
        if url_key:
            source_delta, _source_reason = _community_source_adjustment(str(item.get(url_key, "")))
            score += source_delta
        top_scores.append(score)

    if not top_scores:
        return 0.0

    avg_top = sum(top_scores) / len(top_scores)
    result_bonus = min(len(results), 5) * 2
    quality = (avg_top + result_bonus) / 100.0
    return round(min(1.0, quality), 3)


def split_sentences(text: str) -> list[str]:
    text = normalize_space(text)
    if not text:
        return []
    return [normalize_space(part) for part in re.split(r"(?<=[.!?。！？])\s+", text) if normalize_space(part)]
