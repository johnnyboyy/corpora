---
name: corpora:ux-library-sync
description: Bring corpora/ux-library.md back in line with the project's actual experience patterns after coder-side drift has accumulated. Trigger is not yet mechanical, unlike ui-library-sync.md — see the note below before relying on this file as parallel to that one.
---

# UX library sync

**This process has no mechanical trigger yet — unlike `ui-library-sync.md`.** `kernel.md`'s
handoff schema and `corpus.py` track `ui-drift` (screens/components) and a `library-drift` counter
fed by it; nothing equivalent exists for experience/flow drift today. A coder-composed spawn that
changes how a flow behaves has no field to self-report that in, and the gate has no counter to
threshold against. Until that's added — a `ux-drift` handoff field plus an `experience-drift`
counter, the same shape as `ui-drift`/`library-drift` — this phase runs on judgment alone:

**Trigger:** the operator requests it directly, or a handoff's `Surfaced` section notes that an
established flow, state pattern, or recoverability convention the `ux-library.md` documents has
been contradicted or retired by a coder-side change. Surface the latter as a suggestion at the
ratify gate the same way a mechanical trigger would, but it is a judgment call by whoever is
reading `Surfaced`, not a threshold check.

**Composition:** convergent stance, `ux-design`-composed — the full ongoing composition (`scripts/
corpus.py select --unit-of-work design-ux-flow`), not the narrower founding-a-library composition
`ux-library-init.md` uses.

**Execution:** this is one spawn — after composing, follow `general-operation.md`'s Phase 3
onward (spawn brief, execution, relay, ratify gate) exactly as any other unit of work. Everything
below is this spawn's task content.

---

## Task

Documentation work against the actual product behavior, not a fresh design pass: audit `corpora/
ux-library.md` section by section — navigation model, flow inventory, interaction conventions,
state and feedback patterns, recoverability conventions — against how the project actually behaves
today, and correct any entry the library still teaches that the product has since moved away from.

1. For each flow or convention named in the triggering `Surfaced` note (or, absent that detail, the
   library's full section list), compare the library's documented behavior against the current
   implementation.
2. Write the entry as a standing description of current state, not a copy of any spawn's own
   narrated reasoning — the same restriction `ui-library-sync.md` applies to `ui-library.md`
   corrections applies here: no history tags, no "supersedes the prior X" lead-ins, no naming what
   was rejected or why. Overwrite a superseded entry outright.
3. A discrepancy that reads as an unintended defect rather than a chosen change is a **finding**,
   not a correction to make silently — route it to the handoff's `Surfaced` section per
   `ui-library-init.md`'s "Findings — bugs and gaps are not proposals," the same test applies here.
4. If the audit surfaces genuinely new judgment, propose it through the normal `proposals` field —
   this phase is not exempt from producing principles when the work actually earns one, only from
   treating documentation corrections as if they were.

## Handoff

Write the handoff artifact per `kernel.md`, "The handoff artifact." This phase touches neither
`ui-drift` field — it documents experience, not visuals.
