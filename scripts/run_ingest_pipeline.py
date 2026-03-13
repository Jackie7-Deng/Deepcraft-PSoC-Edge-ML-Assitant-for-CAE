#!/usr/bin/env python3
"""一键执行网页刷新、建索引、向量化和校验。"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_step(command: list[str]) -> None:
    print(f"[RUN] {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="执行知识摄取流水线")
    parser.add_argument("--with-fetch", action="store_true", help="先按 ingest\\urls_checked.txt 执行网页刷新")
    args = parser.parse_args()

    python = sys.executable
    if args.with_fetch:
        run_step([python, "scripts\\refresh_html_mirror.py"])
    run_step([python, "scripts\\init_kb.py"])
    run_step([python, "scripts\\build_vector_index.py"])
    run_step([python, "scripts\\verify_ingest.py"])


if __name__ == "__main__":
    main()
