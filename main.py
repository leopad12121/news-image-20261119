#!/usr/bin/env python3
"""Entry point: copy the generated front page to the output directory.

Reads the MAKEFUN_OUTPUT_DIR environment variable; when it is unset,
the image stays in the current directory. The copy is byte-for-byte,
so the delivered image is exactly the one draw_news.py produced.
"""

import os
import shutil

SOURCE = "entry.png"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "."
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, SOURCE)
    shutil.copyfile(SOURCE, target)
    print(f"Copied {SOURCE} -> {target}")


if __name__ == "__main__":
    main()
