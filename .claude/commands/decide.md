---
description: Decision support — compare options on value, risk, duty, and bias; save a decision entry
---

Follow `CLAUDE.md` and `SCHEMA.md`.

The decision:

$ARGUMENTS

Steps:
1. List the options. For each, compare: pros/cons, risks, alignment with my values, dharma/duty, long-term consequences, opportunity cost, and where emotional bias is distorting the view.
2. **Pattern-warning:** scan `problems/` and `decisions/` for similar past decisions/patterns; note repeated mistakes.
3. Give a clear recommendation with the reasoning, and what would make me reverse it.
4. Determine the next id (`decisions/DEC-<today>-NN`), save a decision entry per SCHEMA (frontmatter + the comparison as the body). Link `related_problems` if relevant.
5. Validate: `python tools/validate.py <file>` (activate `.venv` first). Fix errors.
6. End with one immediate next action.
