---
name: corpora:ui-library-sync
description: Bring corpora/ui-library.md back in line with the project's actual rendered state after coder-side drift has accumulated. Suggested, never automatic — the operator decides whether and when it runs.
---

# UI library sync

**Trigger:** evaluated at every ratify gate (`general-operation.md`, Phase 6, step 8), never run
automatically. `direction` filings already update the library directly at the gate as they land —
this phase is for the gap a single filing doesn't close: accumulated coder-side drift the library
hasn't caught up to yet. Suggest a sync when `library-drift.since-last-sync ≥ 3` (`kernel.md`, "The
retrospective," "Triggers"), or immediately when a drifting change *retired* something the library
still teaches — a stale-but-wrong library is worse than an incomplete one. Handoffs self-report
`ui-drift`; the gate counts it into `library-drift` mechanically (`corpus.py record-gate
--ui-drift`) — the operator's decision to act on the suggestion is the judgment call, not the count
itself.

**Composition:** divergent stance, `ui-design`-composed — the full ongoing composition (`scripts/
corpus.py select --unit-of-work design-ui-surface`), not the narrower founding-a-library
composition `ui-library-init.md` uses. A sync project already has concrete components and screens
for every domain to weigh against; there is no "nothing exists yet" restraint to apply here.

**Execution:** this is one spawn — after composing, follow `general-operation.md`'s Phase 3
onward (spawn brief, execution, relay, ratify gate) exactly as any other unit of work. Everything
below is this spawn's task content.

---

## Task

Documentation work against the rendered state, not a fresh design pass: audit `corpora/
ui-library.md` section by section against what the project's components and screens actually look
like and do today, and correct any entry the library still teaches that the code has since moved
away from.

1. For each screen or component named in `library-drift`'s contributing handoffs (or, absent that
   detail, the library's full component vocabulary), compare the library's documented values
   (color tokens, spacing, states, visual character) against the current implementation.
2. Write the entry as a standing description of current state, not a copy of any spawn's own
   narrated reasoning — the same restriction `general-operation.md`'s "UI library upkeep" states
   for direction filings applies here: no "(direction, <date>, implemented)" tags, no "supersedes
   the prior X" lead-ins, no dates, no naming what was rejected or why. When a corrected entry
   replaces an existing one, overwrite it outright rather than layering the correction on top; the
   library should never require reading two versions to know the current one.
3. A discrepancy that reads as an unintended defect rather than a chosen change is a **finding**,
   not a correction to make silently — route it to the handoff's `Surfaced` section per
   `ui-library-init.md`'s "Findings — bugs and gaps are not proposals," the same test applies here.
4. If the audit surfaces genuinely new judgment (a pattern that recurred enough to generalize, not
   just a documentation correction), propose it through the normal `proposals` field — this phase
   is not exempt from producing principles when the work actually earns one, only from treating
   documentation corrections as if they were.

## Handoff

Write the handoff artifact per `kernel.md`, "The handoff artifact." `ui-drift.screens`/
`.components` should be empty on this handoff — the sync's entire job is to *close* drift, not
accumulate more of it; if the sync work itself changed a component's rendered appearance, that's a
separate coder-side change and gets its own handoff. After the gate processes this handoff, reset
the counter: `corpus.py sync-done`.
