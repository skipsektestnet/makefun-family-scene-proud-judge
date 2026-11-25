#!/usr/bin/env python3
"""Family scene entry for the make.fun bounty.

Writes the one-line family scene to /output/entry.txt after validating
it against the bounty entry rules (non-empty, at most 280 characters,
at most 2 lines, no leading or trailing whitespace).
"""

import os
import sys

ENTRY = (
    "Dad burned the toast again, so Mom trimmed off the black edges, "
    "called it 'extra crispy,' and served it like it was the plan all along."
)

MAX_CHARS = 280
MAX_LINES = 2
OUTPUT_PATH = "/output/entry.txt"


def validate(text):
    """Check the entry against the bounty rules; raise on violation."""
    if not text:
        raise ValueError("entry must not be empty")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    lines = text.split("\n")
    if len(lines) > MAX_LINES:
        raise ValueError(f"entry exceeds {MAX_LINES} lines")
    if any(not line for line in lines):
        raise ValueError("entry must not contain an empty line")
    if any(ord(ch) < 32 and ch != "\n" for ch in text):
        raise ValueError("entry must not contain control characters")
    return True


def main():
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")
    print(f"Wrote {len(ENTRY)}-character entry to {OUTPUT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
