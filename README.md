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
| `/export` | Export everything to a JSON bundle. |

## Data
- `problems/ knowledge/ reflections/ decisions/ systems/` — your data, as Markdown.
- `taxonomy.md` — controlled vocabulary. `SCHEMA.md` — the data contract.
- Validate any file: `python tools/validate.py <path>` (run with the `.venv` activated).
- Export: `python tools/export.py [YYYY-MM-DD]` (run with the `.venv` activated).

## Design
See [docs/superpowers/specs/2026-06-07-lifeos-problem-solver-design.md](docs/superpowers/specs/2026-06-07-lifeos-problem-solver-design.md).
