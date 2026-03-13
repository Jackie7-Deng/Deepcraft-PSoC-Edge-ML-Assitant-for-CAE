#!/usr/bin/env python3
"""执行增量检查后重建索引。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_index_lib import PROCESSED_FILES_PATH, build_all_indexes, build_vector_index, gather_files, file_sha1, load_json, rel_path


def main() -> None:
    old_files = {
        item["path"]: item["sha1"]
        for item in load_json(PROCESSED_FILES_PATH, [])
    }
    current_files = {rel_path(path): file_sha1(path) for path in gather_files()}
    changed = sorted(
        path for path, sha in current_files.items()
        if old_files.get(path) != sha
    )
    removed = sorted(path for path in old_files if path not in current_files)
    summary = build_all_indexes()
    vector_meta = build_vector_index()
    print(json.dumps({
        "changed_files": changed,
        "removed_files": removed,
        "index_summary": summary,
        "vector_meta": vector_meta,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
