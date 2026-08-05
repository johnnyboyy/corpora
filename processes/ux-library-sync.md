---
name: corpora:ux-library-sync
description: Bring corpora/ux-library.md back in line with the project's actual experience patterns after coder-side drift has accumulated. Suggested alongside processes/ui-library-sync.md off the same library-drift counter, since real UX work rarely happens without UI drift — the operator decides whether the accumulated drift actually touched a flow.
---

# UX library sync

**Trigger:** suggested alongside `processes/ui-library-sync.md`, off the *same* `library-drift`
counter — when `library-drift.since-last-sync ≥ 3`, or a drifting change retired a flow/state/
recoverability convention the `ux-library.md` still teaches, the gate suggests both a UI and a UX
sync. There is no separate `ux-drift` field or counter, deliberately: real UX work (a changed flow,
a new confirmation step, a reworked navigation model) almost always surfaces as changed screens, so
it already lives inside the `ui-drift` signal — UX drift is a subset of UI drift, not a separate
thing to track. The coupling is unfiltered: the same counter suggests both, and the operator
dismisses the UX half when the accumulated drift was purely visual (a restyle that touched no
documented flow). The immediate case still holds too — a `Surfaced` note that a documented flow was
contradicted or retired surfaces a UX sync suggestion right then, ahead of the threshold, since a
stale-but-wrong library is worse than an incomplete one.

The `library-drift` counter is shared with the UI sync and is reset once by `corpus.py sync-done`
after the sync pass completes — whether that pass synced the UI library, the UX library, or both.
Dismissing the UX half doesn't hold the counter open; it re-accumulates and re-suggests on the next
round of drift.

**Composition:** convergent stance, `ux-design`-composed — the full ongoing composition (`scripts/
corpus.py select --unit-of-work design-ux-flow`), not the narrower founding-a-library composition
`processes/ux-library-init.md` uses.

**Execution:** this is one spawn — after composing, follow `processes/general-operation.md`'s Phase 3
onward (spawn brief, execution, relay, ratify gate) exactly as any other unit of work. Everything
below is this spawn's task content.

---

## Task

Documentation work against the actual product behavior, not a fresh design pass: audit `corpora/
ux-library.md` section by section — navigation model, flow inventory, interaction conventions,
state and feedback patterns, recoverability conventions — against how the project actually behaves
today, and correct any entry the library still teaches that the product has since moved away from.

1. For each flow or convention named in the triggering `Surfaced` note, or — when the trigger was
   the drift threshold rather than a specific note — the flows and conventions touching the screens
   the accumulated `ui-drift` named, compare the library's documented behavior against the current
   implementation. Absent any such detail, walk the library's full section list.
2. Write the entry as a standing description of current state, not a copy of any spawn's own
   narrated reasoning — the same restriction `processes/ui-library-sync.md` applies to `ui-library.md`
   corrections applies here: no history tags, no "supersedes the prior X" lead-ins, no naming what
   was rejected or why. Overwrite a superseded entry outright.
3. A discrepancy that reads as an unintended defect rather than a chosen change is a **finding**,
   not a correction to make silently — route it to the handoff's `Surfaced` section per
   `processes/ui-library-init.md`'s "Findings — bugs and gaps are not proposals," the same test applies here.
4. If the audit surfaces genuinely new judgment, propose it through the normal `proposals` field —
   this phase is not exempt from producing principles when the work actually earns one, only from
   treating documentation corrections as if they were.

## Handoff

Write the handoff artifact per `kernel.md`, "The handoff artifact." This phase touches neither
`ui-drift` field — it documents experience, not visuals.
