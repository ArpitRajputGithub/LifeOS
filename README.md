# LifeOS — Personal Problem-Solving AI Agent

A local-first, Markdown-based personal agent that helps me understand, organize, and solve life problems — built to later become a hosted LifeOS web app.

## Setup
```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r tools/requirements.txt
```

## How to use (inside Claude Code)
| Command | What it does |
|---|---|
| `/solve` | Describe a problem; runs the full process and saves an entry. |
| `/add-knowledge` | Add and classify a transcript / note / book / PDF text. |
| `/outcome` | Record how a past problem turned out. |
| `/analytics` | Insights across all problems; review open items. |
| `/search` | Search past problems by category, emotion, person, area, date, tag, outcome. |
| `/ask` | Ask the knowledge base a question (cited answers). |
| `/actions` | See open actions across all problems by status. |
| `/decide` | Decision support between options. |
| `/reflect` | Daily/weekly reflection check-in. |
| `/systems` | Build a preventive system for a recurring pattern. |
| `/precedents` | Look up how others have solved a similar problem. |
| `/add-precedent` | Add a precedent (how a problem was solved) to the shared library. |
| `/export` | Export everything to a JSON bundle. |

## Data
- `problems/ knowledge/ reflections/ decisions/ systems/` — your data, as Markdown.
- `taxonomy.md` — controlled vocabulary. `SCHEMA.md` — the data contract.
- Validate any file: `python tools/validate.py <path>` (run with the `.venv` activated).
- Export: `python tools/export.py [YYYY-MM-DD]` (run with the `.venv` activated).

## Privacy & data ownership
Your personal entries stay on your machine. These folders are **gitignored** (local-only): `problems/ reflections/ decisions/ systems/ exports/ analytics/`. Each keeps a `README.md` so the folder still exists after a clone.

Public/tracked (safe to open-source): the framework, `knowledge/` (your wisdom library), `precedents/` (shared solutions), and `examples/` (fictional samples).

> **Caveat:** `/add-knowledge`, `/add-precedent`, and the `/outcome` "distill a precedent" step write to **public** folders. Do not put personal identifying details (names, employer, exact dates/places) in them.

## Design
See [docs/superpowers/specs/2026-06-07-lifeos-problem-solver-design.md](docs/superpowers/specs/2026-06-07-lifeos-problem-solver-design.md).
