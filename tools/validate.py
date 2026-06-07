#!/usr/bin/env python3
"""Validate LifeOS entity files against SCHEMA.md and taxonomy.md."""
import glob
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ID_PATTERNS = {
    "problem": r"^PRB-\d{8}-\d{2}$",
    "knowledge": r"^KND-\d{8}-\d{2}$",
    "reflection": r"^REF-\d{8}-\d{2}$",
    "decision": r"^DEC-\d{8}-\d{2}$",
    "system": r"^SYS-\d{8}-\d{2}$",
}

REQUIRED = {
    "problem": ["id", "type", "title", "created", "updated", "status",
                "subjects", "life_areas", "problem_types", "deeper_issue", "ratings"],
    "knowledge": ["id", "type", "title", "created", "source_type", "subjects"],
    "reflection": ["id", "type", "created", "period"],
    "decision": ["id", "type", "title", "created", "status", "options"],
    "system": ["id", "type", "title", "created", "status", "kind"],
}

# entity field -> taxonomy list key
CONTROLLED = {
    "subjects": "subjects",
    "related_subjects": "subjects",
    "life_areas": "life_areas",
    "problem_types": "problem_types",
    "prevents_problem_types": "problem_types",
    "deeper_issue": "deeper_issue",
    "emotions": "emotions",
    "mood": "emotions",
    "source_type": "source_type",
    "period": "reflection_period",
    "kind": "system_kind",
}

STATUS_KEY = {
    "problem": "problem_status",
    "decision": "decision_status",
    "system": "system_status",
}

RATING_KEYS = ["urgency", "importance", "emotional_intensity", "controllability",
               "long_term_impact", "recurrence_likelihood", "effort_required"]


def load_taxonomy(path=None):
    path = path or os.path.join(ROOT, "taxonomy.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"```yaml\n(.*?)```", text, re.S)
    if not m:
        raise ValueError("No ```yaml block found in taxonomy.md")
    return yaml.safe_load(m.group(1))


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    return yaml.safe_load(m.group(1))


def _as_list(v):
    return v if isinstance(v, list) else [v]


def validate_file(path, tax):
    errors = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm = parse_frontmatter(text)
    if fm is None:
        return [f"{path}: no YAML frontmatter"]
    t = fm.get("type")
    if t not in REQUIRED:
        return [f"{path}: unknown or missing type: {t!r}"]

    for field in REQUIRED[t]:
        if field not in fm or fm[field] in (None, "", []):
            errors.append(f"{path}: missing required field '{field}'")

    pat = ID_PATTERNS.get(t)
    if pat and not re.match(pat, str(fm.get("id", ""))):
        errors.append(f"{path}: id '{fm.get('id')}' does not match {pat}")

    for field, key in CONTROLLED.items():
        if field not in fm or fm[field] is None:
            continue
        allowed = set(tax.get(key, []))
        for v in _as_list(fm[field]):
            if v not in allowed:
                errors.append(f"{path}: '{field}' value '{v}' not in taxonomy[{key}]")

    skey = STATUS_KEY.get(t)
    if skey and "status" in fm and fm["status"] not in set(tax.get(skey, [])):
        errors.append(f"{path}: status '{fm['status']}' not in taxonomy[{skey}]")

    if t == "problem":
        ratings = fm.get("ratings") or {}
        for rk in RATING_KEYS:
            val = ratings.get(rk)
            if not isinstance(val, int) or not (1 <= val <= 10):
                errors.append(f"{path}: ratings.{rk} must be int 1-10, got {val!r}")
        for a in fm.get("actions") or []:
            if a.get("status") not in set(tax.get("action_status", [])):
                errors.append(f"{path}: action {a.get('id')} status '{a.get('status')}' invalid")
            if a.get("difficulty") not in set(tax.get("difficulty", [])):
                errors.append(f"{path}: action {a.get('id')} difficulty '{a.get('difficulty')}' invalid")
        for o in fm.get("outcomes") or []:
            if not isinstance(o, dict):
                errors.append(f"{path}: outcome entry is not a mapping: {o!r}")
                continue
            for k in ("id", "date"):
                if not o.get(k):
                    errors.append(f"{path}: outcome '{o.get('id', '?')}' missing '{k}'")

    return errors


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for f in glob.glob(os.path.join(p, "**", "*.md"), recursive=True):
                if os.path.basename(f) != "README.md":  # folder docs, not entities
                    yield f
        elif p.endswith(".md"):
            yield p


def main(argv):
    tax = load_taxonomy()
    targets = argv[1:] or ["problems", "knowledge", "reflections", "decisions", "systems"]
    targets = [os.path.join(ROOT, t) if not os.path.isabs(t) else t for t in targets]
    all_errors = []
    for fpath in iter_files(targets):
        all_errors += validate_file(fpath, tax)
    for e in all_errors:
        print(e)
    if all_errors:
        print(f"\n{len(all_errors)} error(s)")
        return 1
    print("All files valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
