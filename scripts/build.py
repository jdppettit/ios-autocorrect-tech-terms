#!/usr/bin/env python3
"""Build Text Replacements plists from the word lists in terms/.

Each terms/<category>.txt holds one term per line. Blank lines and lines
starting with # are ignored. Every term becomes a Text Replacement whose
shortcut and phrase are identical, which stops iOS/macOS autocorrect from
"fixing" it.

Outputs:
  dist/tech-terms.plist         every category combined
  dist/categories/<name>.plist  one file per category

Run with --check to validate the lists without writing anything (used in CI).
"""

import plistlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TERMS = ROOT / "terms"
DIST = ROOT / "dist"


def load(path: Path) -> list[str]:
    terms = []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if any(c.isspace() for c in line):
            sys.exit(f"{path.name}:{n}: '{line}' contains whitespace; shortcuts must be a single word")
        terms.append(line)
    return terms


def entries(terms: list[str]) -> list[dict]:
    return [{"phrase": t, "shortcut": t} for t in terms]


def main() -> None:
    check_only = "--check" in sys.argv
    categories = {p.stem: load(p) for p in sorted(TERMS.glob("*.txt"))}

    seen: dict[str, str] = {}
    problems = []
    for name, terms in categories.items():
        for t in terms:
            key = t.lower()
            if key in seen:
                problems.append(f"duplicate: '{t}' in {name} (already in {seen[key]})")
            else:
                seen[key] = name
    if problems:
        sys.exit("\n".join(problems))

    combined = [t for terms in categories.values() for t in terms]
    if check_only:
        print(f"OK: {len(combined)} terms across {len(categories)} categories")
        return

    (DIST / "categories").mkdir(parents=True, exist_ok=True)
    for old in (DIST / "categories").glob("*.plist"):
        old.unlink()
    for name, terms in categories.items():
        with open(DIST / "categories" / f"{name}.plist", "wb") as fh:
            plistlib.dump(entries(terms), fh)
    with open(DIST / "tech-terms.plist", "wb") as fh:
        plistlib.dump(entries(combined), fh)

    print(f"Wrote {len(combined)} terms across {len(categories)} categories")
    for name, terms in categories.items():
        print(f"  {name:<24} {len(terms)}")


if __name__ == "__main__":
    main()
