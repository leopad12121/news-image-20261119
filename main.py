#!/usr/bin/env python3
"""Copy entry.png next to this script into the output directory.

Standard library only, no network, no timestamps, no randomness.
The source image is resolved relative to this file, so the program
works from any working directory and from a read-only source dir.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def sha256_hex(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"

    if not source.is_file():
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    shutil.copyfile(source, destination)

    source_digest = sha256_hex(source)
    dest_digest = sha256_hex(destination)
    if source_digest != dest_digest:
        print(
            f"error: digest mismatch after copy: "
            f"source {source_digest} != destination {dest_digest}",
            file=sys.stderr,
        )
        return 1

    print(f"copied to {destination} sha256={dest_digest[:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
