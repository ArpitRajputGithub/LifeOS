#!/usr/bin/env python3
"""Export all LifeOS entities to a single JSON bundle (data ownership / migration)."""
import glob
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDERS = {
    "problems": "problems",
    "knowledge": "knowledge",
    "reflections": "reflections",
    "decisions": "decisions",
    "systems": "systems",
    "precedents": "precedents",
}


def _frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return yaml.safe_load(text[4:end])


def build_bundle(root=ROOT):
    bundle = {}
    for key, folder in FOLDERS.items():
        items = []
        for path in sorted(glob.glob(os.path.join(root, folder, "*.md"))):
            fm = _frontmatter(path)
            if fm and fm.get("type"):
                items.append(fm)
        bundle[key] = items
    return bundle


def main(argv):
    root = ROOT
    bundle = build_bundle(root)
    out_dir = os.path.join(root, "exports")
    os.makedirs(out_dir, exist_ok=True)
    # Caller passes the date string to keep this deterministic/testable.
    date = argv[1] if len(argv) > 1 else "latest"
    out_path = os.path.join(out_dir, f"export-{date}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, default=str, ensure_ascii=False)
    counts = {k: len(v) for k, v in bundle.items()}
    print(f"Wrote {out_path}")
    print(f"Counts: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
