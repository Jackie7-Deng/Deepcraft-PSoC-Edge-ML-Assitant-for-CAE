#!/usr/bin/env python3
"""校验当前知识索引与向量索引是否已落地。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import (
    CHUNK_VECTORS_PATH,
    INDEX_SUMMARY_PATH,
    PROCESSED_FILES_PATH,
    SYMBOL_INDEX_PATH,
    TEXT_CHUNKS_PATH,
    TOKEN_POSTINGS_PATH,
    VECTOR_META_PATH,
    load_json,
    load_jsonl,
)


def main() -> None:
    missing = [
        str(path) for path in [
            TEXT_CHUNKS_PATH,
            SYMBOL_INDEX_PATH,
            PROCESSED_FILES_PATH,
            INDEX_SUMMARY_PATH,
            CHUNK_VECTORS_PATH,
            TOKEN_POSTINGS_PATH,
            VECTOR_META_PATH,
        ]
        if not path.exists()
    ]
    summary = load_json(INDEX_SUMMARY_PATH, {})
    chunks = load_jsonl(TEXT_CHUNKS_PATH)
    symbols = load_json(SYMBOL_INDEX_PATH, [])
    postings = load_json(TOKEN_POSTINGS_PATH, {})
    vector_meta = load_json(VECTOR_META_PATH, {})
    result = {
        "missing_files": missing,
        "chunk_count": len(chunks),
        "symbol_count": len(symbols),
        "posting_terms": len(postings),
        "vector_chunk_count": vector_meta.get("chunk_count", 0),
        "source_type_counts": summary.get("source_type_counts", {}),
        "status": "ok" if not missing and chunks and symbols and postings else "failed",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()
