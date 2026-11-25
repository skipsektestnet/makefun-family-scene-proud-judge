"""Family scene entry for make.fun: "Make the AI Judge Feel Proud".

Writes the scene (one line, at most 280 characters) to entry.txt inside
the output directory. The output directory comes from MAKEFUN_OUTPUT_DIR,
else the first CLI argument, else /output.
"""

import os
import sys

SCENE = (
    "Dad burned the toast again, so Mom trimmed off the black edges, "
    "called it 'extra crispy,' and served it like it was the plan all along."
)
MAX_CHARS = 280
MAX_LINES = 2


def problems(text):
    """Collect every rule the scene breaks; empty list means it passes."""
    found = []
    if not text.strip():
        found.append("scene is blank")
    if len(text) > MAX_CHARS:
        found.append(f"scene is {len(text)} chars, over the {MAX_CHARS} limit")
    lines = text.splitlines()
    if len(lines) > MAX_LINES:
        found.append(f"scene has {len(lines)} lines, over the {MAX_LINES} limit")
    if text != text.strip():
        found.append("scene has leading or trailing whitespace")
    for ch in text:
        if ord(ch) < 32 and ch not in "\n":
            found.append(f"scene has a control character U+{ord(ch):04X}")
            break
    return found


def write_scene(text, out_dir):
    """Validate the scene, then write it to entry.txt in out_dir."""
    bad = problems(text)
    if bad:
        raise ValueError("; ".join(bad))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    return path


def main(argv):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = argv[1] if len(argv) > 1 else "/output"
    try:
        path = write_scene(SCENE, out_dir)
    except ValueError as err:
        print(f"entry rejected: {err}", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(SCENE)} chars, {len(SCENE.splitlines())} line)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
