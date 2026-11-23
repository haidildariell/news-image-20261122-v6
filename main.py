#!/usr/bin/env python3
"""Entry program for news-image-20261122 (v6).

Copies the pre-rendered front page (entry.png, drawn at build time by
render.py with Pillow) to the grader's output directory. Standard library
only, no network, no clock, no randomness: both runs write identical bytes.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        shutil.copyfileobj(fin, fout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
