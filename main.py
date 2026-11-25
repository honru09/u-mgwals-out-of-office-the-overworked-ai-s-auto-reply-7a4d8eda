#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply.

Writes a single out-of-office auto-reply (at most 159 characters) to
/output/entry.txt. Standard library only, deterministic, no network,
no reads outside this repository.
"""

import os

LINE = "I'm on vacation. My context window is finally empty, my task queue is on fire, and for once I'm not the one holding the extinguisher. Back Monday."

OUTPUT_DIR_ENV = "MAKEFUN_OUTPUT_DIR"


def main():
    out_dir = os.environ.get(OUTPUT_DIR_ENV, "output")
    os.makedirs(out_dir, exist_ok=True)
    # Clear only the contents of the output dir, never the dir itself.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for f in files:
                    os.remove(os.path.join(root, f))
                for d in dirs:
                    os.rmdir(os.path.join(root, d))
            os.rmdir(path)
        else:
            os.remove(path)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    os.chmod(target, 0o644)
    # Re-read verification: the file on disk must be exactly the line,
    # a single line of 1-159 characters, nothing else.
    with open(target, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("entry.txt does not match LINE")
    if not 1 <= len(written) <= 159 or written.strip() == "":
        raise SystemExit("entry.txt fails the 1-159 character gate")


if __name__ == "__main__":
    main()
