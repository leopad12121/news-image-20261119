#!/usr/bin/env python3
"""Entrypoint for news-image-20261119 (make.fun).

Copies the finished front-page image, entry.png, which this repository
holds, into the output directory as entry.png. Standard library only,
no network, fully deterministic: both runs write the same bytes.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    assert sha256(src) == sha256(dst), "copy mismatch"
    print("wrote", dst, sha256(dst)[:16])


if __name__ == "__main__":
    main()
