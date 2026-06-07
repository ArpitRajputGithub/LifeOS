# How to Use LifeOS — A Practical Guide

LifeOS is your **personal problem-solving agent that runs inside Claude Code**. This guide shows you how to actually use it day to day.

---

## The mental model (read this first)

LifeOS is **your data as Markdown files + a set of slash commands that read and write those files.** There is no app to launch and no server to run. You open this folder in Claude Code and *talk to it* using `/` commands.

```
You type:   /solve I keep procrastinating on my taxes
              ↓
Claude:     analyzes it → shows the full breakdown → saves problems/PRB-2026...md
              ↓
Later:      /search, /analytics, /outcome read those saved files back
```

Three files define how it behaves — you rarely edit them, but it helps to know they exist:

| File | What it is |
|---|---|
| `CLAUDE.md` | The "constitution" — persona, the 13-step problem-solving process, output format, safety rule. |
| `SCHEMA.md` | The data contract — what fields each entity must have. |
| `taxonomy.md` | The controlled vocabulary — the only allowed tags. This is what makes analytics possible. |

Your data lives in: `problems/  knowledge/  reflections/  decisions/  systems/`

---

## One-time setup

Only needed for the validation/export **tools** (the slash commands themselves just need Claude Code open in this folder):

```bash
cd "/Users/0xdeadbeef/dev/Tools/AI Problem Solver"
python3 -m venv .venv && . .venv/bin/activate && pip install -r tools/requirements.txt
```

---

## The core loop — what you'll actually do

### 1. You have a problem → `/solve`
```
/solve I got a job offer and I can't stop overthinking whether to take it
```
You get the full breakdown: the deeper issue, 1–10 ratings, root-cause analysis, relevant wisdom **cited from your knowledge base**, what's in vs out of your control, a ranked action plan, and one immediate next step small enough to do today. It saves a `PRB-…` file and tells you the ID.

> If a problem involves serious medical / mental-health / legal / financial risk, LifeOS will tell you to contact a qualified professional **first**, before the analysis.

### 2. You learn something worth keeping → `/add-knowledge`
```
/add-knowledge [paste a YouTube transcript, book notes, or an article]
```
It classifies the material into the 15 subjects of life and files it as a `KND-…` doc. **This is the flywheel:** the more you feed it, the better `/solve` and `/ask` get, because they cite *your own* saved material instead of giving generic advice.

### 3. A problem plays out → `/outcome`
```
/outcome PRB-20260607-01 — I took the job; writing down my 3 fears is what unstuck me
```
It records what happened, what worked, what failed, the lesson, and the pattern to remember — then flips the problem's status to `resolved`.

> **This is the step most people skip, and it's the most valuable one.** No outcomes = no pattern detection. Recording outcomes is what lets LifeOS later warn you: *"you're repeating PRB-20260607-01."*

---

## Retrieval & insight commands

| When you want to… | Command | Example |
|---|---|---|
| Find past problems | `/search` | `/search anxiety problems about career` |
| Ask your knowledge base | `/ask` | `/ask what does my material say about handling fear?` |
| See what you committed to | `/actions` | `/actions overdue` |
| Step back and see patterns | `/analytics` | `/analytics` |

- **`/ask`** answers **only from your saved knowledge** and cites every source by id + title. If it has nothing relevant, it says so plainly and suggests what to `/add-knowledge`.
- **`/analytics`** is your review command: recurring emotions, who keeps appearing in your problems, what you start vs finish, avoided areas, and which recurring problem types **have no preventive system yet**.

---

## The lighter commands

- **`/decide`** — stuck between options. Compares them on values, risk, duty/dharma, long-term consequences, opportunity cost, and emotional bias; saves a `DEC-…` entry and gives a clear recommendation (plus what would make you reverse it).
- **`/reflect`** — daily/weekly check-in. You dump what's on your mind; it reflects it back honestly and surfaces hidden problems or emotional patterns, offering to `/solve` anything real.
- **`/systems`** — when something keeps recurring, build a rule / routine / checklist / habit / boundary so it stops. (Seed example: the *"48-hour rule for big decisions."*)

---

## Data ownership

- **`/export`** — bundles everything to `exports/export-YYYY-MM-DD.json`. Your full, portable copy.
- From the terminal anytime (venv active): `python tools/validate.py` checks every file is schema-valid; `python tools/export.py 2026-06-07` regenerates the JSON bundle.

Your data is always **two formats you own**: the Markdown files *and* the JSON export. Nothing is locked in.

---

## A realistic first week

```
Day 1:  /add-knowledge   (paste 2–3 things you've been meaning to save)
        /solve           (your most nagging current problem)
Day 2:  /reflect         (5-min brain-dump; let it surface hidden issues)
Day 3:  /solve           (another problem) → watch the pattern-warning kick in
Day 5:  /outcome         (close the loop on Day 1's problem)
Day 7:  /analytics       (your first patterns) → /systems for anything recurring
        /export          (snapshot your data)
```

---

## Three habits that make it actually work

1. **Feed the knowledge base.** It's the difference between generic advice and advice grounded in what *you* find wise.
2. **Always record outcomes.** Without them, LifeOS is just a fancy notepad — outcomes are what create pattern detection.
3. **Trust the structure.** The controlled tags feel rigid, but that rigidity is exactly why `/search` and `/analytics` can find real patterns later.

---

## Quick reference — all 11 commands

| Command | What it does | Writes |
|---|---|---|
| `/solve` | Full problem-solving process on a problem you describe | `problems/PRB-…` |
| `/add-knowledge` | Classify & file a transcript / note / book / article | `knowledge/KND-…` |
| `/outcome` | Record how a past problem turned out; update status | updates a `PRB-…` |
| `/analytics` | Insights & review across all problems | (optional snapshot) |
| `/search` | Find past problems by category, emotion, person, date, tag | — |
| `/ask` | Ask your knowledge base a question (cited answers) | — |
| `/actions` | See open actions across all problems by status | — |
| `/decide` | Decision support between options | `decisions/DEC-…` |
| `/reflect` | Daily/weekly reflection check-in | `reflections/REF-…` |
| `/systems` | Build a preventive system for a recurring pattern | `systems/SYS-…` |
| `/export` | Export everything to a JSON bundle | `exports/export-…json` |

---

*For the underlying rules see `CLAUDE.md`, `SCHEMA.md`, and `taxonomy.md`. For the v1 acceptance results see `MANUAL_ACCEPTANCE.md`.*
