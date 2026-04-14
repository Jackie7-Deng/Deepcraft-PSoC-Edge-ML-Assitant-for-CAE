from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lightweight_rag import INDEX_OUTPUT, INDEX_TARGETS, CHUNK_OVERLAP, CHUNK_SIZE, build_index  # noqa: E402


if __name__ == "__main__":
    output_path = Path(INDEX_OUTPUT)
    result = build_index(output_path, include_pdfs=False)
    result["index_targets"] = INDEX_TARGETS
    result["chunk_size"] = CHUNK_SIZE
    result["chunk_overlap"] = CHUNK_OVERLAP
    result["include_pdfs"] = False
    result["index_output"] = str(output_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
