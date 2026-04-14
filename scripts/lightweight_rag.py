from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover
    PdfReader = None

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.search_utils import dedupe_keep_order, detect_chip_protocol, detect_context_hints, top_symptom_phrases, tokenize_query  # noqa: E402

INDEX_VERSION = 2
DEFAULT_INDEX_PATH = ROOT / "indexes" / "lightweight_index.json"
MAX_TEXT_FILE_BYTES = 2_500_000

# PSoC Edge DeepCraft AI 轻量 RAG 配置
INDEX_TARGETS = [
    {"path": "knowledge", "glob": "*.md", "priority": "high"},
    {"path": ".", "glob": "CLAUDE.md", "priority": "high"},
    {"path": "memory", "glob": "*.md", "priority": "medium"},
    {"path": ".claude", "glob": "*.md", "priority": "medium"},
    {"path": "docs", "glob": "*.md", "priority": "medium"},
    {"path": "docs", "glob": "*.txt", "priority": "medium"},
]
INDEX_OUTPUT = ROOT / "indexes" / "lightweight_index.json"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80

PSOC_EDGE_SYNONYMS = {
    "MTBML": ["ModusToolbox ML", "MTB-ML", "mtb-ml"],
    "Imagimob": ["imagimob", "Imagimob Studio", "Imagimob Deploy"],
    "TFLite": ["TensorFlow Lite", "TF Lite Micro", "TFLM", "tflite"],
    "NPU": ["neural processing unit", "hardware accelerator"],
    "inference": ["model inference", "ML inference", "run model"],
    "Face ID": ["face detection", "face recognition", "face id"],
    "ModusToolbox": ["MTB", "modustoolbox"],
    "build failed": ["compilation error", "build error", "make failed"],
    "KitProg": ["KitProg3", "programmer", "debugger"],
}
DOMAIN_SYNONYMS = {key.lower(): tuple(value.lower() for value in values) for key, values in PSOC_EDGE_SYNONYMS.items()}
SOURCE_TYPE_PRIORITY = {
    "knowledge": 14,
    "init": 13,
    "config": 11,
    "pdf": 10,
    "code": 8,
    "tooling": 4,
    "other": 5,
}
TEXT_SUFFIXES = {".h", ".hpp", ".c", ".cc", ".cpp", ".md", ".txt", ".json", ".py", ".yml", ".yaml", ".xml"}
EXCLUDED_DIR_NAMES = {"__pycache__", ".git", ".venv", "node_modules", "indexes", "Debug", "Release", "build"}


@dataclass
class ChunkRecord:
    chunk_id: str
    source_path: str
    source_type: str
    title: str
    anchor: str | None
    text: str
    chunk_index: int
    page: int | None = None
    start_line: int | None = None
    end_line: int | None = None
    keywords: list[str] | None = None
    content_hash: str | None = None
    source_mtime_utc: str | None = None


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def normalize_rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_mtime_utc(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def content_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]


def slugify_anchor(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", normalize_space(text).lower()).strip("-")
    return value or "chunk"


def is_path_excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIR_NAMES for part in path.parts)


def classify_source_type(path: Path) -> str:
    rel = normalize_rel_path(path)
    if rel.startswith("knowledge/"):
        return "knowledge"
    if path.name in {"CLAUDE.md", "retrieval_strategy.md"} or rel.startswith(".claude/") or rel.startswith("memory/"):
        return "init"
    if rel.startswith("scripts/") or rel.startswith("mcp_servers/") or rel.startswith(".vscode/"):
        return "tooling"
    if path.suffix.lower() in {".json", ".xml", ".yaml", ".yml"}:
        return "config"
    if path.suffix.lower() == ".pdf":
        return "pdf"
    if path.suffix.lower() in TEXT_SUFFIXES:
        return "code"
    return "other"


def extract_keywords(text: str, limit: int = 16) -> list[str]:
    counts: dict[str, int] = {}
    for token in tokenize_query(text):
        counts[token] = counts.get(token, 0) + 1
    return [item for item, _count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]


def iter_candidate_paths(root: Path, include_pdfs: bool = False) -> list[Path]:
    candidates: list[Path] = []
    seen: set[str] = set()
    for target in INDEX_TARGETS:
        target_base = (root / target["path"]).resolve()
        pattern = target["glob"]
        if target_base.is_file():
            matches = [target_base]
        elif target_base.is_dir():
            matches = list(target_base.rglob(pattern))
        else:
            continue
        for path in matches:
            if not path.is_file() or is_path_excluded(path):
                continue
            suffix = path.suffix.lower()
            if suffix == ".pdf" and not include_pdfs:
                continue
            if suffix not in TEXT_SUFFIXES and suffix != ".pdf":
                continue
            if suffix != ".pdf" and path.stat().st_size > MAX_TEXT_FILE_BYTES:
                continue
            rel = normalize_rel_path(path)
            if rel in seen:
                continue
            seen.add(rel)
            candidates.append(path)
    candidates.sort(key=lambda p: normalize_rel_path(p))
    return candidates


def read_source_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_pdf_text(path: Path) -> list[tuple[int, str]]:
    if PdfReader is None:
        return []
    reader = PdfReader(str(path))
    pages: list[tuple[int, str]] = []
    for index, page in enumerate(reader.pages, start=1):
        text = normalize_space(page.extract_text() or "")
        if text:
            pages.append((index, text))
    return pages


def nearest_markdown_heading(lines: list[str], line_number: int) -> str:
    for idx in range(min(line_number - 1, len(lines) - 1), -1, -1):
        line = lines[idx].strip()
        if line.startswith("#"):
            return normalize_space(line.lstrip("#").strip())
    return ""


def chunk_lines(path: Path, text: str) -> list[ChunkRecord]:
    lines = text.splitlines()
    if not lines:
        return []
    rel_path = normalize_rel_path(path)
    source_type = classify_source_type(path)
    records: list[ChunkRecord] = []
    start_line = 0
    chunk_index = 0
    while start_line < len(lines):
        current_chars = 0
        end_line = start_line
        while end_line < len(lines) and (current_chars < CHUNK_SIZE or end_line == start_line):
            current_chars += len(lines[end_line]) + 1
            end_line += 1
        slice_lines = lines[start_line:end_line]
        chunk_text = "\n".join(slice_lines).strip()
        if normalize_space(chunk_text):
            title = nearest_markdown_heading(lines, start_line + 1) if path.suffix.lower() == ".md" else path.stem
            records.append(ChunkRecord(
                chunk_id=f"{rel_path}::chunk-{chunk_index}",
                source_path=rel_path,
                source_type=source_type,
                title=title,
                anchor=f"heading:{slugify_anchor(title)}" if title else f"lines:{start_line + 1}-{end_line}",
                text=chunk_text,
                chunk_index=chunk_index,
                start_line=start_line + 1,
                end_line=end_line,
                keywords=extract_keywords(chunk_text),
                content_hash=content_hash(chunk_text),
                source_mtime_utc=source_mtime_utc(path),
            ))
            chunk_index += 1
        if end_line >= len(lines):
            break
        overlap_chars = 0
        new_start = end_line
        while new_start > start_line and overlap_chars < CHUNK_OVERLAP:
            new_start -= 1
            overlap_chars += len(lines[new_start]) + 1
        start_line = new_start if new_start > start_line else end_line
    return records


def chunk_pdf(path: Path) -> list[ChunkRecord]:
    rel_path = normalize_rel_path(path)
    records: list[ChunkRecord] = []
    chunk_index = 0
    for page_number, page_text in read_pdf_text(path):
        start = 0
        while start < len(page_text):
            end = min(len(page_text), start + 1600)
            chunk_text = page_text[start:end].strip()
            if chunk_text:
                records.append(ChunkRecord(
                    chunk_id=f"{rel_path}::page-{page_number}-chunk-{chunk_index}",
                    source_path=rel_path,
                    source_type="pdf",
                    title=f"{path.stem} page {page_number}",
                    anchor=f"page-{page_number}",
                    text=chunk_text,
                    chunk_index=chunk_index,
                    page=page_number,
                    keywords=extract_keywords(chunk_text),
                    content_hash=content_hash(chunk_text),
                    source_mtime_utc=source_mtime_utc(path),
                ))
                chunk_index += 1
            if end >= len(page_text):
                break
            start = max(0, end - 200)
    return records


def build_index(index_path: Path = DEFAULT_INDEX_PATH, include_pdfs: bool = False) -> dict[str, Any]:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    chunks: list[ChunkRecord] = []
    for path in iter_candidate_paths(ROOT, include_pdfs=include_pdfs):
        if path.suffix.lower() == ".pdf":
            chunks.extend(chunk_pdf(path))
        else:
            chunks.extend(chunk_lines(path, read_source_text(path)))
    payload = {
        "index_version": INDEX_VERSION,
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "include_pdfs": include_pdfs,
        "chunk_count": len(chunks),
        "file_count": len({chunk.source_path for chunk in chunks}),
        "files_indexed": sorted({chunk.source_path for chunk in chunks}),
        "chunks": [asdict(chunk) for chunk in chunks],
    }
    index_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "index_path": str(index_path),
        "chunk_count": len(chunks),
        "file_count": len(payload["files_indexed"]),
        "files_indexed": payload["files_indexed"],
    }


def expand_query(query: str) -> tuple[list[str], list[str]]:
    base_tokens = tokenize_query(query)
    chip, interface = detect_chip_protocol(query)
    context_hints = [normalize_space(item).lower() for item in detect_context_hints(query)]
    symptom_phrases = top_symptom_phrases(query)
    phrase_terms = dedupe_keep_order([normalize_space(query).lower(), *[phrase.lower() for phrase in symptom_phrases if phrase]])
    seed_terms = [token.lower() for token in base_tokens]
    if chip:
        seed_terms.append(chip.lower())
    if interface:
        seed_terms.append(interface.lower())
    seed_terms.extend(context_hints)
    expanded = list(seed_terms)
    for token in list(seed_terms):
        expanded.extend(DOMAIN_SYNONYMS.get(token, ()))
    for phrase in symptom_phrases:
        expanded.extend(tokenize_query(phrase))
    return dedupe_keep_order(expanded), dedupe_keep_order(phrase_terms)


def score_chunk(chunk: dict[str, Any], query: str, token_terms: list[str], phrase_terms: list[str]) -> tuple[int, list[str]]:
    text = (chunk.get("text") or "").lower()
    title = (chunk.get("title") or "").lower()
    path = (chunk.get("source_path") or "").lower()
    keywords = set(chunk.get("keywords") or [])
    source_type = chunk.get("source_type", "other")
    score = SOURCE_TYPE_PRIORITY.get(source_type, SOURCE_TYPE_PRIORITY["other"])
    reasons: list[str] = []
    exact = normalize_space(query).lower()
    if exact and exact in title:
        score += 24
        reasons.append("title:exact-query")
    if exact and exact in text:
        score += 18
        reasons.append("text:exact-query")
    for phrase in phrase_terms:
        if phrase and phrase in title:
            score += 12
            reasons.append(f"title:{phrase}")
        elif phrase and phrase in text:
            score += 8
            reasons.append(f"text:{phrase}")
    chip, interface = detect_chip_protocol(query)
    for token in token_terms:
        if token in title:
            score += 7
            reasons.append(f"title:{token}")
        elif token in path:
            score += 5
            reasons.append(f"path:{token}")
        elif token in keywords:
            score += 4
            reasons.append(f"keyword:{token}")
        elif token in text:
            score += 3
            reasons.append(f"text:{token}")
    if chip and chip.lower() in text:
        score += 6
        reasons.append(f"chip:{chip.lower()}")
    if interface and interface.lower() in text:
        score += 4
        reasons.append(f"interface:{interface.lower()}")
    return score, dedupe_keep_order(reasons)


def load_index(index_path: Path = DEFAULT_INDEX_PATH) -> dict[str, Any]:
    return json.loads(index_path.read_text(encoding="utf-8"))


def search_index(query: str, index_path: Path = DEFAULT_INDEX_PATH, limit: int = 8) -> dict[str, Any]:
    payload = load_index(index_path)
    token_terms, phrase_terms = expand_query(query)
    scored: list[dict[str, Any]] = []
    for chunk in payload.get("chunks", []):
        score, reasons = score_chunk(chunk, query, token_terms, phrase_terms)
        if score <= SOURCE_TYPE_PRIORITY["other"]:
            continue
        enriched = dict(chunk)
        enriched["score"] = score
        enriched["match_reasons"] = reasons
        scored.append(enriched)
    scored.sort(key=lambda item: (-item["score"], item["source_path"], item["chunk_index"]))
    return {
        "query": query,
        "index_path": str(index_path),
        "token_terms": token_terms,
        "phrase_terms": phrase_terms,
        "results": scored[:limit],
    }


def format_result_markdown(payload: dict[str, Any]) -> str:
    lines = [f"Query: {payload['query']}", f"Token terms: {', '.join(payload['token_terms'])}", ""]
    for idx, item in enumerate(payload["results"], start=1):
        citation = item["source_path"]
        if item.get("page") is not None:
            citation += f"#page-{item['page']}"
        elif item.get("start_line") is not None and item.get("end_line") is not None:
            citation += f":{item['start_line']}-{item['end_line']}"
        snippet = normalize_space(item["text"])[:280]
        lines.append(f"{idx}. [{item['score']}] {citation}")
        lines.append(f"   title: {item['title']}")
        lines.append(f"   reasons: {', '.join(item['match_reasons'])}")
        lines.append(f"   snippet: {snippet}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and search a lightweight local RAG index.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build", help="Build the lightweight local chunk index.")
    build_parser.add_argument("--index", default=str(INDEX_OUTPUT), help="Output JSON index path.")
    build_parser.add_argument("--include-pdf", action="store_true", help="Include PDF files in the index build.")
    search_parser = subparsers.add_parser("search", help="Search the lightweight local chunk index.")
    search_parser.add_argument("query", help="Natural-language query.")
    search_parser.add_argument("--index", default=str(INDEX_OUTPUT), help="Input JSON index path.")
    search_parser.add_argument("--limit", type=int, default=8, help="Maximum number of results.")
    search_parser.add_argument("--json", action="store_true", help="Print raw JSON instead of markdown.")
    args = parser.parse_args(argv)
    if args.command == "build":
        print(json.dumps(build_index(Path(args.index), include_pdfs=args.include_pdf), ensure_ascii=False, indent=2))
        return 0
    payload = search_index(args.query, Path(args.index), args.limit)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_result_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
