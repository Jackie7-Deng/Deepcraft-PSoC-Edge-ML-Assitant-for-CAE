#!/usr/bin/env python3
"""PSoC Edge + DEEPCRAFT 结构化 RAG 公共库。"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "indexes"
VECTOR_DIR = INDEX_DIR / "vector_db"
TEXT_CHUNKS_PATH = INDEX_DIR / "text_chunks.jsonl"
SYMBOL_INDEX_PATH = INDEX_DIR / "symbol_index.json"
PROCESSED_FILES_PATH = INDEX_DIR / "processed_files.json"
INDEX_SUMMARY_PATH = INDEX_DIR / "index_summary.json"
CHUNK_VECTORS_PATH = VECTOR_DIR / "chunk_vectors.jsonl"
TOKEN_POSTINGS_PATH = VECTOR_DIR / "token_postings.json"
VECTOR_META_PATH = VECTOR_DIR / "meta.json"

ALLOWED_EXTENSIONS = {
    ".md", ".txt", ".c", ".h", ".cpp", ".hpp", ".py",
    ".json", ".yml", ".yaml", ".cmake", ".mk", ".ld",
}

EXCLUDED_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", ".cache", ".venv", "venv",
    "node_modules", "indexes", "mcp_servers", "build", "Debug", "Release",
    "x64", "obj", "bin",
}

DOMAIN_SYNONYMS = {
    "psoc edge": ["psoc", "edge", "e84", "e8x", "kit_pse84_eval", "pse84"],
    "psoc 6": ["cy8ckit-062s2-ai", "062s2-ai", "psoc6"],
    "deepcraft": ["imagimob", "studio", "deepcraft studio"],
    "ready model": ["ready models", "test report", "model report", "static library", "precompiled binary", "binary/hex", "hex"],
    "factory alarm detection": ["factory alarms and sirens", "factory alarm", "alarm detection", "alarm ready model"],
    "modustoolbox": ["mtb", "modus toolbox", "dashboard", "project creator"],
    "device configurator": ["design.modus", "generatedsource", "generated source", "notice list", "pins", "clocks", "peripherals", "dma"],
    "machine learning configurator": ["ml configurator", "machine learning", "library level configuration", "library configurator", "mtb ml"],
    "bsp": ["board support package", "target", "target board", "board", "kit"],
    "构建": ["build", "make", "makefile", "toolchain", "program", "compile", "compiler"],
    "编译器": ["compiler", "toolchain", "armclang", "gcc_arm", "llvm", "cy_compiler_arm_dir", "cy_compiler_llvm_arm_dir"],
    "部署": ["deploy", "deployment", "集成", "generate code", "code generation", "mtb ml"],
    "收费": ["licensing", "license", "fees", "price", "commercial deployment", "free", "compute minutes"],
    "申请": ["test now", "download your model", "obtain", "request", "apply"],
    "量产": ["production", "production-ready", "commercial deployment"],
    "排障": ["troubleshoot", "troubleshooting", "debug", "error", "failed", "failure", "问题"],
    "参数": ["parameter", "parameters", "config", "configuration", "macro", "define", "版本", "board", "bsp"],
    "示例": ["example", "examples", "demo", "sample", "readme"],
    "代码": ["source", "function", "函数", "入口", "symbol", "macro"],
    "视觉": ["vision", "camera", "face", "display", "object detection"],
    "语音": ["voice", "audio", "microphone", "pdm", "mfcc"],
    "量化": ["quantization", "int8", "float32", "vela", "npu"],
    "烧录": ["flash", "program", "kitprog", "download"],
    "tensor arena": ["arena", "tensor_arena", "内存", "sram"],
    "faq": ["常见问题", "高频问题"],
}

DOC_CLASS_BY_SOURCE = {
    "knowledge": "knowledge_summary",
    "readme": "readme",
    "web": "web_mirror",
    "source": "source_code",
    "example_doc": "example_doc",
    "generated_info": "generated_info",
    "init": "assistant_control",
    "skill": "assistant_control",
    "prompt": "assistant_control",
    "script": "tooling",
    "governance": "governance",
    "memory": "governance",
    "root_doc": "root_doc",
    "other": "other",
}

EVIDENCE_TIER_BY_SOURCE = {
    "knowledge": "curated_summary",
    "readme": "primary_doc",
    "web": "primary_web",
    "source": "primary_code",
    "example_doc": "primary_doc",
    "generated_info": "generated_artifact",
    "init": "assistant_control",
    "skill": "assistant_control",
    "prompt": "assistant_control",
    "script": "tooling",
    "governance": "governance",
    "memory": "governance",
    "root_doc": "root_doc",
    "other": "other",
}

PLATFORM_RULES = {
    "psoc-edge": ["psoc edge", "pse84", "pse8", "e84", "e8x", "kit_pse84_eval"],
    "psoc6": ["psoc 6", "062s2-ai", "cy8ckit-062s2-ai", "psoc6"],
}

TOOL_RULES = {
    "deepcraft": ["deepcraft", "imagimob", "deepcraft studio"],
    "modustoolbox": ["modustoolbox", "modus toolbox", "dashboard", "project creator"],
    "device-configurator": ["device configurator", "design.modus", "generatedsource", "generated source", "notice list"],
    "ml-configurator": ["machine learning configurator", "ml configurator", "mtb ml"],
    "make": ["makefile", "make build", "make program", "toolchain", "compiler", "target"],
}

DOMAIN_RULES = {
    "deployment": ["deploy", "deployment", "integrate", "集成", "烧录"],
    "training": ["training", "train", "训练", "evaluation", "评估"],
    "troubleshooting": ["troubleshoot", "troubleshooting", "failed", "failure", "error", "排障", "问题"],
    "vision": ["vision", "camera", "face", "display", "image"],
    "audio": ["voice", "audio", "microphone", "pdm", "mfcc"],
    "imu": ["imu", "accelerometer", "gyro", "motion"],
}

QUESTION_PREFIX_RE = re.compile(r"^(请问|请帮我|帮我|麻烦|想问下|我想知道|告诉我|请你|能否|能不能|可否)\s*")
QUESTION_SUFFIX_RE = re.compile(r"[？?！!。.\s]+$")
QUERY_REWRITE_REPLACEMENTS = [
    ("为什么", "原因"),
    ("怎么", "步骤"),
    ("如何", "步骤"),
    ("哪里", "位置"),
    ("在哪", "位置"),
    ("区别", "对比"),
    ("差异", "对比"),
    ("是否", "支持"),
    ("能不能", "支持"),
]
SUMMARY_INTENT_HINTS = ("什么是", "是什么", "为什么", "如何", "怎么", "步骤", "区别", "差异", "建议")
WEB_INTENT_HINTS = ("官网", "网页", "网页内容", "原文", "url", "链接", "页面")
CODE_INTENT_HINTS = ("函数", "宏", "源码", "实现", "symbol", "接口", "定义")
STRICT_EVIDENCE_TIERS = {"curated_summary", "primary_doc", "primary_web", "primary_code", "generated_artifact"}

REVERSE_SYNONYMS: dict[str, set[str]] = defaultdict(set)
for canonical, aliases in DOMAIN_SYNONYMS.items():
    bundle = {canonical, *aliases}
    for alias in bundle:
        REVERSE_SYNONYMS[alias.lower()].update(bundle)

SOURCE_PRIORITIES = {
    "knowledge": 1.20,
    "readme": 1.10,
    "web": 0.95,
    "source": 1.00,
    "example_doc": 1.00,
    "generated_info": 1.05,
    "init": 0.75,
    "skill": 0.70,
    "prompt": 0.60,
    "script": 0.80,
    "governance": 0.55,
    "memory": 0.50,
    "root_doc": 0.65,
    "other": 0.50,
}

def ensure_dirs() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("/", "\\")

def stable_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u3000", " ")
    return text

def file_sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()

def classify_source(rel: str) -> str:
    lower = rel.lower()
    if lower.startswith("knowledge\\"):
        return "knowledge"
    if lower.startswith("docs\\readmes\\") or lower.startswith("readme_") or lower.endswith("\\readme.md") or lower.endswith("\\release.md"):
        return "readme"
    if lower.startswith("ingest\\html\\"):
        return "web"
    if lower.startswith(".claude\\skills\\"):
        return "skill"
    if lower.startswith(".claude\\") or lower == "claude.md" or lower == "agents.md" or lower.startswith(".github\\"):
        return "init"
    if lower.startswith("prompts\\"):
        return "prompt"
    if lower.startswith("governance\\"):
        return "governance"
    if lower.startswith("memory\\"):
        return "memory"
    if lower.startswith("scripts\\"):
        return "script"
    if "mtb_ml_gen\\info\\" in lower:
        return "generated_info"
    if "\\docs\\" in lower:
        return "example_doc"
    if any(segment in lower for segment in ["\\source\\", "\\application_code\\", "\\include\\"]):
        return "source"
    if lower.endswith(".md"):
        return "root_doc"
    return "other"

def should_include_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False
    rel_parts = path.relative_to(ROOT).parts
    if any(part in EXCLUDED_DIRS for part in rel_parts[:-1]):
        return False
    if rel_parts and rel_parts[0] in {"indexes", "mcp_servers"}:
        return False
    if path.name == "temp_toc.txt":
        return False
    return True

def gather_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if should_include_file(path):
            files.append(path)
    return sorted(files)

def safe_read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return normalize_text(path.read_text(encoding=encoding))
        except UnicodeDecodeError:
            continue
    return normalize_text(path.read_text(errors="ignore"))

def first_heading_or_stem(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return path.stem

def tokenize(text: str) -> list[str]:
    text = normalize_text(text).lower()
    tokens: list[str] = []
    tokens.extend(re.findall(r"[a-z0-9_./+-]+", text))
    chinese_parts = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    for part in chinese_parts:
        tokens.append(part)
        if len(part) <= 6:
            for size in (2, 3):
                for idx in range(0, max(0, len(part) - size + 1)):
                    tokens.append(part[idx: idx + size])
    compact = re.sub(r"\s+", "", text)
    if compact:
        for size in (3, 4):
            if len(compact) >= size:
                for idx in range(0, min(len(compact) - size + 1, 128)):
                    gram = compact[idx: idx + size]
                    if re.search(r"[a-z0-9\u4e00-\u9fff]", gram):
                        tokens.append(gram)
    return tokens

def expand_query_terms(query: str) -> list[str]:
    base = tokenize(query)
    expanded = list(base)
    query_lower = query.lower()
    for alias, bundle in REVERSE_SYNONYMS.items():
        if alias in query_lower:
            expanded.extend(tokenize(" ".join(sorted(bundle))))
    return list(dict.fromkeys(term for term in expanded if term))

def top_keywords(text: str, limit: int = 32) -> list[str]:
    counts = Counter(tokenize(text))
    common = []
    for token, _count in counts.most_common(limit * 2):
        if len(token) < 2:
            continue
        common.append(token)
        if len(common) >= limit:
            break
    return common

def rule_tag_hits(haystack: str, rules: dict[str, list[str]]) -> list[str]:
    hits: list[str] = []
    for tag, patterns in rules.items():
        if any(pattern in haystack for pattern in patterns):
            hits.append(tag)
    return hits

def infer_metadata(rel: str, text: str, source_type: str) -> dict[str, Any]:
    haystack = normalize_text(f"{rel}\n{text}").lower()
    return {
        "doc_class": DOC_CLASS_BY_SOURCE.get(source_type, "other"),
        "evidence_tier": EVIDENCE_TIER_BY_SOURCE.get(source_type, "other"),
        "platform_tags": rule_tag_hits(haystack, PLATFORM_RULES),
        "tool_tags": rule_tag_hits(haystack, TOOL_RULES),
        "domain_tags": rule_tag_hits(haystack, DOMAIN_RULES),
    }

def infer_query_metadata(query: str) -> dict[str, list[str]]:
    lower = normalize_text(query).lower()
    return {
        "platform_tags": rule_tag_hits(lower, PLATFORM_RULES),
        "tool_tags": rule_tag_hits(lower, TOOL_RULES),
        "domain_tags": rule_tag_hits(lower, DOMAIN_RULES),
    }

def dedupe_keep_order(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))

def rewrite_query_variants(query: str) -> list[str]:
    normalized = normalize_text(query).strip()
    if not normalized:
        return []
    variants = [normalized]
    trimmed = QUESTION_PREFIX_RE.sub("", normalized).strip()
    trimmed = QUESTION_SUFFIX_RE.sub("", trimmed).strip()
    if trimmed and trimmed != normalized:
        variants.append(trimmed)
    for source, target in QUERY_REWRITE_REPLACEMENTS:
        if source in trimmed:
            variants.append(trimmed.replace(source, target))
    query_meta = infer_query_metadata(trimmed or normalized)
    for field in ("platform_tags", "tool_tags", "domain_tags"):
        for tag in query_meta.get(field, []):
            variants.append(f"{trimmed or normalized} {tag}")
            bundle = REVERSE_SYNONYMS.get(tag.lower(), set())
            if bundle:
                variants.append(f"{trimmed or normalized} {' '.join(sorted(bundle))}")
    return dedupe_keep_order(variants)

def collect_query_terms(query_variants: list[str]) -> list[str]:
    terms: list[str] = []
    for variant in query_variants:
        terms.extend(expand_query_terms(variant))
    return dedupe_keep_order(terms)

def infer_query_intent(query: str) -> dict[str, bool]:
    lower = normalize_text(query).lower()
    return {
        "prefer_summary": any(hint in lower for hint in SUMMARY_INTENT_HINTS),
        "prefer_web": any(hint in lower for hint in WEB_INTENT_HINTS),
        "prefer_code": any(hint in lower for hint in CODE_INTENT_HINTS),
        "prefer_troubleshooting": "排障" in lower or "failed" in lower or "failure" in lower or "error" in lower,
    }

def choose_chunk_end(lines: list[str], start: int, max_lines: int, min_lines: int = 12, lookback: int = 8) -> int:
    raw_end = min(len(lines), start + max_lines)
    if raw_end >= len(lines):
        return raw_end
    lower_bound = max(start + min_lines, raw_end - lookback)
    for idx in range(raw_end, lower_bound, -1):
        current = lines[idx - 1].strip()
        if not current:
            return idx
        if current.startswith("##") or current.startswith("```"):
            return max(start + min_lines, idx - 1)
    return raw_end

def dense_vector(text: str, dimensions: int = 384) -> list[float]:
    values = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.md5(token.encode("utf-8", errors="ignore")).digest()
        idx = int.from_bytes(digest[:2], "little") % dimensions
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        values[idx] += sign
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [round(v / norm, 6) for v in values]

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    size = min(len(vec_a), len(vec_b))
    return sum(vec_a[i] * vec_b[i] for i in range(size))

def markdown_sections(lines: list[str]) -> list[tuple[int, int, list[str]]]:
    sections: list[tuple[int, int, list[str]]] = []
    heading_stack: list[str] = []
    section_headings: list[str] = []
    section_start = 1
    saw_heading = False
    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

    for idx, line in enumerate(lines, start=1):
        match = heading_re.match(line)
        if not match:
            continue
        if idx > section_start:
            sections.append((section_start, idx - 1, section_headings.copy()))
        level = len(match.group(1))
        title = match.group(2).strip()
        heading_stack = heading_stack[: level - 1]
        heading_stack.append(title)
        section_headings = heading_stack.copy()
        section_start = idx
        saw_heading = True

    if lines:
        sections.append((section_start, len(lines), section_headings.copy() if saw_heading else []))
    return sections

def make_chunk_id(rel: str, start_line: int, end_line: int) -> str:
    return stable_hash(f"{rel}:{start_line}:{end_line}")[:16]

def chunk_markdown(path: Path, text: str, max_lines: int = 42, overlap: int = 6) -> list[dict[str, Any]]:
    lines = text.splitlines()
    rel = rel_path(path)
    title = first_heading_or_stem(path, text)
    source_type = classify_source(rel)
    metadata = infer_metadata(rel, text, source_type)
    chunks: list[dict[str, Any]] = []
    for start_line, end_line, headings in markdown_sections(lines):
        section_lines = lines[start_line - 1:end_line]
        if not any(line.strip() for line in section_lines):
            continue
        local_start = 0
        while local_start < len(section_lines):
            local_end = choose_chunk_end(section_lines, local_start, max_lines=max_lines)
            snippet_lines = section_lines[local_start:local_end]
            if not any(line.strip() for line in snippet_lines):
                if local_end >= len(section_lines):
                    break
                local_start = max(local_start + 1, local_end - overlap)
                continue
            absolute_start = start_line + local_start
            absolute_end = start_line + local_end - 1
            chunk_text = "\n".join(snippet_lines).strip()
            keyword_text = " ".join([title, " ".join(headings), rel, chunk_text])
            chunks.append({
                "chunk_id": make_chunk_id(rel, absolute_start, absolute_end),
                "path": rel,
                "source_type": source_type,
                "title": title,
                "heading_path": headings,
                "start_line": absolute_start,
                "end_line": absolute_end,
                "text": chunk_text,
                "keywords": top_keywords(keyword_text),
                **metadata,
            })
            if local_end >= len(section_lines):
                break
            local_start = max(local_start + 1, local_end - overlap)
    return chunks

def chunk_plain_text(path: Path, text: str, max_lines: int = 40, overlap: int = 6) -> list[dict[str, Any]]:
    lines = text.splitlines()
    rel = rel_path(path)
    title = first_heading_or_stem(path, text)
    source_type = classify_source(rel)
    metadata = infer_metadata(rel, text, source_type)
    chunks: list[dict[str, Any]] = []
    start = 0
    while start < len(lines):
        end = choose_chunk_end(lines, start, max_lines=max_lines)
        snippet_lines = lines[start:end]
        if not any(line.strip() for line in snippet_lines):
            if end >= len(lines):
                break
            start = max(start + 1, end - overlap)
            continue
        chunk_text = "\n".join(snippet_lines).strip()
        keyword_text = " ".join([title, rel, chunk_text])
        chunks.append({
            "chunk_id": make_chunk_id(rel, start + 1, end),
            "path": rel,
            "source_type": source_type,
            "title": title,
            "heading_path": [],
            "start_line": start + 1,
            "end_line": end,
            "text": chunk_text,
            "keywords": top_keywords(keyword_text),
            **metadata,
        })
        if end >= len(lines):
            break
        start = max(start + 1, end - overlap)
    return chunks

def build_chunks_for_file(path: Path) -> list[dict[str, Any]]:
    text = safe_read_text(path)
    if not text.strip():
        return []
    if path.suffix.lower() == ".md":
        return chunk_markdown(path, text)
    return chunk_plain_text(path, text)

def extract_symbols(path: Path, text: str) -> list[dict[str, Any]]:
    rel = rel_path(path)
    suffix = path.suffix.lower()
    symbols: list[dict[str, Any]] = []
    lines = text.splitlines()
    seen: set[tuple[str, int]] = set()

    def add_symbol(symbol_type: str, name: str, line_no: int, context: str) -> None:
        key = (name, line_no)
        if key in seen:
            return
        seen.add(key)
        symbols.append({
            "name": name,
            "type": symbol_type,
            "path": rel,
            "line": line_no,
            "context": context.strip(),
        })

    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    define_re = re.compile(r"^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)")
    c_func_re = re.compile(r"^\s*[A-Za-z_][A-Za-z0-9_\s\*]*?\s+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?:\{|;)?\s*$")
    python_def_re = re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    python_class_re = re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\s*[:\(]")

    for line_no, line in enumerate(lines, start=1):
        if suffix == ".md":
            match = heading_re.match(line)
            if match:
                add_symbol("heading", match.group(2).strip(), line_no, line)
            continue
        if suffix in {".c", ".h", ".cpp", ".hpp"}:
            define = define_re.match(line)
            if define:
                add_symbol("macro", define.group(1), line_no, line)
            func = c_func_re.match(line)
            if func:
                name = func.group(1)
                if name not in {"if", "for", "while", "switch", "return", "sizeof"}:
                    add_symbol("function", name, line_no, line)
            continue
        if suffix == ".py":
            match_def = python_def_re.match(line)
            if match_def:
                add_symbol("function", match_def.group(1), line_no, line)
            match_cls = python_class_re.match(line)
            if match_cls:
                add_symbol("class", match_cls.group(1), line_no, line)
    return symbols

def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

def build_all_indexes() -> dict[str, Any]:
    ensure_dirs()
    files = gather_files()
    chunks: list[dict[str, Any]] = []
    symbols: list[dict[str, Any]] = []
    processed_files: list[dict[str, Any]] = []
    type_counter: Counter[str] = Counter()
    doc_class_counter: Counter[str] = Counter()
    evidence_tier_counter: Counter[str] = Counter()
    platform_counter: Counter[str] = Counter()
    tool_counter: Counter[str] = Counter()
    domain_counter: Counter[str] = Counter()

    for path in files:
        text = safe_read_text(path)
        rel = rel_path(path)
        file_chunks = build_chunks_for_file(path)
        file_symbols = extract_symbols(path, text)
        chunks.extend(file_chunks)
        symbols.extend(file_symbols)
        source_type = classify_source(rel)
        metadata = infer_metadata(rel, text, source_type)
        type_counter[source_type] += 1
        doc_class_counter[metadata["doc_class"]] += 1
        evidence_tier_counter[metadata["evidence_tier"]] += 1
        for tag in metadata["platform_tags"]:
            platform_counter[tag] += 1
        for tag in metadata["tool_tags"]:
            tool_counter[tag] += 1
        for tag in metadata["domain_tags"]:
            domain_counter[tag] += 1
        processed_files.append({
            "path": rel,
            "sha1": file_sha1(path),
            "size": path.stat().st_size,
            "source_type": source_type,
            "chunk_count": len(file_chunks),
            "symbol_count": len(file_symbols),
            **metadata,
        })

    write_jsonl(TEXT_CHUNKS_PATH, chunks)
    write_json(SYMBOL_INDEX_PATH, symbols)
    write_json(PROCESSED_FILES_PATH, processed_files)

    summary = {
        "workspace": rel_path(ROOT),
        "file_count": len(processed_files),
        "chunk_count": len(chunks),
        "symbol_count": len(symbols),
        "source_type_counts": dict(type_counter),
        "metadata_counts": {
            "doc_class": dict(doc_class_counter),
            "evidence_tier": dict(evidence_tier_counter),
            "platform_tags": dict(platform_counter),
            "tool_tags": dict(tool_counter),
            "domain_tags": dict(domain_counter),
        },
        "outputs": {
            "text_chunks": rel_path(TEXT_CHUNKS_PATH),
            "symbol_index": rel_path(SYMBOL_INDEX_PATH),
            "processed_files": rel_path(PROCESSED_FILES_PATH),
        },
    }
    write_json(INDEX_SUMMARY_PATH, summary)
    return summary

def build_vector_index() -> dict[str, Any]:
    ensure_dirs()
    chunks = load_jsonl(TEXT_CHUNKS_PATH)
    vector_rows: list[dict[str, Any]] = []
    postings: dict[str, list[str]] = defaultdict(list)
    for chunk in chunks:
        feature_text = " ".join([
            chunk.get("title", ""),
            " ".join(chunk.get("heading_path", [])),
            chunk.get("path", ""),
            chunk.get("text", ""),
        ])
        vector = dense_vector(feature_text)
        vector_rows.append({
            "chunk_id": chunk["chunk_id"],
            "vector": vector,
        })
        terms = set(top_keywords(feature_text, limit=48))
        for term in terms:
            postings[term].append(chunk["chunk_id"])

    write_jsonl(CHUNK_VECTORS_PATH, vector_rows)
    write_json(TOKEN_POSTINGS_PATH, {key: sorted(value) for key, value in postings.items()})
    meta = {
        "model": "hashed-ngram-v1",
        "dimensions": 384,
        "chunk_count": len(vector_rows),
        "token_count": len(postings),
        "outputs": {
            "chunk_vectors": rel_path(CHUNK_VECTORS_PATH),
            "token_postings": rel_path(TOKEN_POSTINGS_PATH),
        },
    }
    write_json(VECTOR_META_PATH, meta)
    return meta

def load_chunk_map() -> dict[str, dict[str, Any]]:
    chunks = load_jsonl(TEXT_CHUNKS_PATH)
    return {chunk["chunk_id"]: chunk for chunk in chunks}

def load_vector_map() -> dict[str, list[float]]:
    rows = load_jsonl(CHUNK_VECTORS_PATH)
    return {row["chunk_id"]: row["vector"] for row in rows}

def metadata_alignment_bonus(chunk: dict[str, Any], query_meta: dict[str, list[str]]) -> float:
    bonus = 0.0
    field_weights = {
        "platform_tags": 0.10,
        "tool_tags": 0.08,
        "domain_tags": 0.06,
    }
    for field, weight in field_weights.items():
        chunk_tags = set(chunk.get(field, []))
        query_tags = set(query_meta.get(field, []))
        if chunk_tags and query_tags and chunk_tags & query_tags:
            bonus += weight
    return bonus

def metadata_bonus(chunk: dict[str, Any], query: str, query_meta: dict[str, list[str]]) -> float:
    bonus = SOURCE_PRIORITIES.get(chunk.get("source_type", "other"), 0.5)
    lower_query = query.lower()
    path_text = chunk.get("path", "").lower()
    title_text = chunk.get("title", "").lower()
    if lower_query and lower_query in path_text:
        bonus += 0.25
    if lower_query and lower_query in title_text:
        bonus += 0.20
    bonus += metadata_alignment_bonus(chunk, query_meta)
    return bonus

def chunk_text_for_matching(chunk: dict[str, Any]) -> str:
    return normalize_text(
        " ".join([
            chunk.get("title", ""),
            " ".join(chunk.get("heading_path", [])),
            chunk.get("path", ""),
            chunk.get("snippet", ""),
        ])
    ).lower()

def query_coverage_score(chunk: dict[str, Any], query_terms: list[str]) -> float:
    haystack = chunk_text_for_matching(chunk)
    unique_terms = [term for term in dedupe_keep_order(query_terms) if len(term) >= 2]
    if not unique_terms:
        return 0.0
    hits = sum(1 for term in unique_terms if term.lower() in haystack)
    return hits / max(1.0, math.sqrt(len(unique_terms)))

def phrase_match_score(chunk: dict[str, Any], query_variants: list[str]) -> float:
    haystack = chunk_text_for_matching(chunk)
    score = 0.0
    for variant in query_variants:
        candidate = QUESTION_SUFFIX_RE.sub("", normalize_text(variant).strip().lower())
        if len(candidate) < 4:
            continue
        if candidate in haystack:
            score += 0.18
    return score

def intent_bonus(chunk: dict[str, Any], query_intent: dict[str, bool]) -> float:
    bonus = 0.0
    doc_class = chunk.get("doc_class")
    evidence_tier = chunk.get("evidence_tier")
    if query_intent.get("prefer_summary"):
        if doc_class == "knowledge_summary":
            bonus += 0.18
        elif evidence_tier == "primary_doc":
            bonus += 0.08
    if query_intent.get("prefer_web") and evidence_tier == "primary_web":
        bonus += 0.18
    if query_intent.get("prefer_code") and evidence_tier == "primary_code":
        bonus += 0.18
    if query_intent.get("prefer_troubleshooting") and "troubleshooting" in chunk.get("domain_tags", []):
        bonus += 0.10
    span = max(1, int(chunk.get("end_line", 0)) - int(chunk.get("start_line", 0)) + 1)
    if span <= 24:
        bonus += 0.04
    elif span >= 48:
        bonus -= 0.03
    return bonus

def ready_model_bonus(chunk: dict[str, Any], query_variants: list[str]) -> float:
    query_text = normalize_text(" ".join(query_variants)).lower()
    if not any(
        marker in query_text
        for marker in (
            "ready model",
            "ready models",
            "factory alarm",
            "gesture recognition",
            "siren detection",
            "baby cry",
            "cough detection",
            "snore detection",
            "fall detection",
            "收费",
            "申请",
            "量产",
            "commercial deployment",
        )
    ):
        return 0.0
    path_text = chunk.get("path", "").lower()
    if "knowledge\\ready_models_catalog.md" in path_text:
        return 0.35
    if "ingest\\html\\deepcraft-ready-models" in path_text:
        return 0.22
    if "legal_licensing-metrics-and-fees" in path_text:
        return 0.16
    return 0.0

def matched_query_terms(chunk: dict[str, Any], query_terms: list[str], limit: int = 12) -> list[str]:
    haystack = chunk_text_for_matching(chunk)
    hits = [term for term in dedupe_keep_order(query_terms) if len(term) >= 2 and term.lower() in haystack]
    return hits[:limit]

def rerank_results(
    results: list[dict[str, Any]],
    query_variants: list[str],
    query_terms: list[str],
    query_intent: dict[str, bool],
) -> list[dict[str, Any]]:
    reranked: list[dict[str, Any]] = []
    for item in results:
        coverage = query_coverage_score(item, query_terms)
        phrase = phrase_match_score(item, query_variants)
        intent = intent_bonus(item, query_intent)
        ready_model = ready_model_bonus(item, query_variants)
        rerank = item["score"] + (coverage * 0.28) + phrase + intent + ready_model
        enriched = dict(item)
        enriched["coverage_score"] = round(coverage, 6)
        enriched["phrase_score"] = round(phrase, 6)
        enriched["intent_score"] = round(intent, 6)
        enriched["ready_model_score"] = round(ready_model, 6)
        enriched["rerank_score"] = round(rerank, 6)
        enriched["matched_query_terms"] = matched_query_terms(item, query_terms)
        reranked.append(enriched)
    reranked.sort(key=lambda item: item["rerank_score"], reverse=True)
    return reranked

def keyword_score(chunk: dict[str, Any], query_terms: list[str]) -> float:
    chunk_keywords = set(chunk.get("keywords", []))
    if not chunk_keywords:
        return 0.0
    hits = sum(1 for term in set(query_terms) if term in chunk_keywords)
    return hits / max(1.0, math.sqrt(len(chunk_keywords)))

def passes_filters(
    chunk: dict[str, Any],
    source_types: list[str] | None = None,
    path_prefix: str | None = None,
    platform_tags: list[str] | None = None,
    tool_tags: list[str] | None = None,
    doc_classes: list[str] | None = None,
    evidence_tiers: list[str] | None = None,
) -> bool:
    if source_types and chunk.get("source_type") not in source_types:
        return False
    if path_prefix:
        normalized_prefix = path_prefix.replace("/", "\\").lower()
        if not chunk.get("path", "").lower().startswith(normalized_prefix):
            return False
    if platform_tags and not (set(chunk.get("platform_tags", [])) & set(platform_tags)):
        return False
    if tool_tags and not (set(chunk.get("tool_tags", [])) & set(tool_tags)):
        return False
    if doc_classes and chunk.get("doc_class") not in doc_classes:
        return False
    if evidence_tiers and chunk.get("evidence_tier") not in evidence_tiers:
        return False
    return True

def search_chunks_detailed(
    query: str,
    top_k: int = 8,
    source_types: list[str] | None = None,
    path_prefix: str | None = None,
    platform_tags: list[str] | None = None,
    tool_tags: list[str] | None = None,
    doc_classes: list[str] | None = None,
    evidence_tiers: list[str] | None = None,
) -> list[dict[str, Any]]:
    chunk_map = load_chunk_map()
    vector_map = load_vector_map()
    postings = load_json(TOKEN_POSTINGS_PATH, {})
    query_variants = rewrite_query_variants(query) or [query]
    query_terms = collect_query_terms(query_variants)
    query_meta = infer_query_metadata(query)
    query_intent = infer_query_intent(query)
    query_vec = dense_vector(" ".join(query_terms) or query)

    candidate_counter: Counter[str] = Counter()
    for term in query_terms:
        for chunk_id in postings.get(term, []):
            candidate_counter[chunk_id] += 1

    if candidate_counter:
        ranked_candidates = [chunk_id for chunk_id, _score in candidate_counter.most_common(300)]
    else:
        ranked_candidates = list(chunk_map.keys())

    results: list[dict[str, Any]] = []
    for chunk_id in ranked_candidates:
        chunk = chunk_map.get(chunk_id)
        vector = vector_map.get(chunk_id)
        if not chunk or vector is None:
            continue
        if not passes_filters(
            chunk,
            source_types=source_types,
            path_prefix=path_prefix,
            platform_tags=platform_tags,
            tool_tags=tool_tags,
            doc_classes=doc_classes,
            evidence_tiers=evidence_tiers,
        ):
            continue
        semantic = cosine_similarity(query_vec, vector)
        keyword = keyword_score(chunk, query_terms)
        meta = metadata_bonus(chunk, query, query_meta)
        score = (semantic * 0.55) + (keyword * 0.30) + (meta * 0.15)
        snippet = re.sub(r"\s+", " ", chunk.get("text", "")).strip()
        results.append({
            "score": round(score, 6),
            "semantic_score": round(semantic, 6),
            "keyword_score": round(keyword, 6),
            "chunk_id": chunk_id,
            "path": chunk["path"],
            "source_type": chunk.get("source_type"),
            "title": chunk.get("title"),
            "heading_path": chunk.get("heading_path", []),
            "start_line": chunk.get("start_line"),
            "end_line": chunk.get("end_line"),
            "doc_class": chunk.get("doc_class"),
            "evidence_tier": chunk.get("evidence_tier"),
            "platform_tags": chunk.get("platform_tags", []),
            "tool_tags": chunk.get("tool_tags", []),
            "domain_tags": chunk.get("domain_tags", []),
            "snippet": snippet[:260],
        })
    results.sort(key=lambda item: item["score"], reverse=True)
    reranked = rerank_results(results[:80], query_variants, query_terms, query_intent)
    return {
        "query": query,
        "query_variants": query_variants,
        "query_terms": query_terms,
        "query_metadata": query_meta,
        "query_intent": query_intent,
        "results": reranked[:top_k],
    }

def search_chunks(
    query: str,
    top_k: int = 8,
    source_types: list[str] | None = None,
    path_prefix: str | None = None,
    platform_tags: list[str] | None = None,
    tool_tags: list[str] | None = None,
    doc_classes: list[str] | None = None,
    evidence_tiers: list[str] | None = None,
) -> list[dict[str, Any]]:
    payload = search_chunks_detailed(
        query=query,
        top_k=top_k,
        source_types=source_types,
        path_prefix=path_prefix,
        platform_tags=platform_tags,
        tool_tags=tool_tags,
        doc_classes=doc_classes,
        evidence_tiers=evidence_tiers,
    )
    return payload["results"]

def citation_of(result: dict[str, Any]) -> str:
    return f"{result['path']}:{result['start_line']}-{result['end_line']}"

def build_grounded_answer_pack(
    query: str,
    top_k: int = 6,
    min_citations: int = 2,
    source_types: list[str] | None = None,
    path_prefix: str | None = None,
    platform_tags: list[str] | None = None,
    tool_tags: list[str] | None = None,
    doc_classes: list[str] | None = None,
    evidence_tiers: list[str] | None = None,
) -> dict[str, Any]:
    payload = search_chunks_detailed(
        query=query,
        top_k=max(top_k, min_citations, 8),
        source_types=source_types,
        path_prefix=path_prefix,
        platform_tags=platform_tags,
        tool_tags=tool_tags,
        doc_classes=doc_classes,
        evidence_tiers=evidence_tiers,
    )
    evidence_items: list[dict[str, Any]] = []
    seen_citations: set[str] = set()
    for item in payload["results"]:
        citation = citation_of(item)
        if citation in seen_citations:
            continue
        seen_citations.add(citation)
        evidence_items.append({
            "citation": citation,
            "path": item["path"],
            "title": item.get("title"),
            "heading_path": item.get("heading_path", []),
            "score": item.get("score"),
            "rerank_score": item.get("rerank_score"),
            "doc_class": item.get("doc_class"),
            "evidence_tier": item.get("evidence_tier"),
            "platform_tags": item.get("platform_tags", []),
            "tool_tags": item.get("tool_tags", []),
            "snippet": item.get("snippet"),
        })
        if len(evidence_items) >= top_k:
            break
    strong_evidence = [
        item for item in evidence_items
        if item["evidence_tier"] in STRICT_EVIDENCE_TIERS and float(item.get("rerank_score") or 0.0) >= 0.65
    ]
    status = "grounded_answer" if len(strong_evidence) >= min_citations else "insufficient_evidence"
    return {
        "query": query,
        "status": status,
        "min_citations_required": min_citations,
        "query_plan": {
            "variants": payload["query_variants"],
            "query_metadata": payload["query_metadata"],
            "query_intent": payload["query_intent"],
        },
        "guardrails": {
            "must_cite": True,
            "must_use_only_local_evidence": True,
            "must_label_inference": "【推断/经验】",
            "must_say_when_missing": "未在当前知识库找到依据",
            "recommended_min_citations": min_citations,
        },
        "evidence": evidence_items,
        "strong_evidence_count": len(strong_evidence),
        "answer_mode_hint": "先给结论，再列证据引用，最后给下一步建议" if status == "grounded_answer" else "证据不足时先说明缺口，再给最小验证步骤",
    }

def search_symbols(query: str, top_k: int = 10) -> list[dict[str, Any]]:
    symbols = load_json(SYMBOL_INDEX_PATH, [])
    query_terms = expand_query_terms(query)
    lower_query = query.lower()
    compact_query = re.sub(r"[^a-z0-9]", "", lower_query)
    ranked: list[dict[str, Any]] = []
    for symbol in symbols:
        name = symbol.get("name", "")
        path = symbol.get("path", "")
        context = symbol.get("context", "")
        score = 0.0
        lower_name = name.lower()
        lower_path = path.lower()
        compact_name = re.sub(r"[^a-z0-9]", "", lower_name)
        if lower_query == lower_name:
            score += 3.0
        if lower_query and lower_query in lower_name:
            score += 2.0
        if compact_query and compact_query in compact_name:
            score += 1.8
        if lower_query and lower_query in lower_path:
            score += 1.0
        context_terms = set(tokenize(context))
        score += sum(0.25 for term in query_terms if term in context_terms)
        if score > 0:
            ranked.append({**symbol, "score": round(score, 6)})
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[:top_k]
