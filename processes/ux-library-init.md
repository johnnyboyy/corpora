---
name: corpora:ux-library-init
description: Found a project's UX library from nothing. Runs once, as processes/bootstrap.md's Phase 4, only when has-ui yes, after processes/ui-library-init.md has ratified. Produces corpora/ux-library.md and proposed experience principles/directions.
---

# UX library init

**Trigger:** `has-ui: yes`, no `ux-library.md` exists yet, and `processes/ui-library-init.md`'s handoff has
already been ratified — the UX library cites the UI library's tokens and components, a content
dependency, not an arbitrary ordering choice. Runs once, as processes/bootstrap.md's Phase 4 — see
`processes/bootstrap.md` for what precedes and follows this phase in the bootstrap sequence. Independent of
`processes/screenshot-library-init.md`: both phases depend only on `processes/ui-library-init.md`, not on each other,
and may run in either order.

**Composition:** convergent stance, `unit-of-work: bootstrap-ux-surface` — run `scripts/corpus.py
select --unit-of-work bootstrap-ux-surface` rather than asserting the set freehand. Narrower than
ongoing `ux-design` work (`design-ux-flow`, which also composes `ranking-evaluation`/
`wizards-flows`), same restraint `processes/ui-library-init.md` applies — again expressed in each
contributing domain's own frontmatter, not hard-listed here.

**Execution:** this is one spawn — after composing, follow `processes/general-operation.md`'s Phase 3
onward (spawn brief, execution, relay, ratify gate) exactly as any other unit of work. Everything
below is this spawn's task content.

---

## Task

Identity is already set by `processes/ui-library-init.md`; this phase's job is convergent documentation of
how the product *works* as an experience, so future UX sessions weigh established patterns instead
of re-deriving them.

Write `corpora/ux-library.md` (or the path config names under `ux-library`) covering, as they
exist in the project:

- **Navigation model** — how users move between surfaces; what is global vs contextual
- **Flow inventory** — the primary user journeys, each in a few lines: entry, steps, exit,
  what state persists
- **Interaction conventions** — selection, editing, confirmation, dismissal; where the project
  asks vs acts
- **State and feedback patterns** — loading, empty, error, success; how progress and failure
  are communicated
- **Recoverability conventions** — which actions are undoable, where recovery surfaces live

Document what exists or was decided — from the codebase, the UI library's behavioral notes, and
any operator-provided product documentation. Do not invent aspirational patterns; a greenfield
project gets a short library that grows with the work. The same restraint as `processes/ui-library-init.md`
applies to proposals: no target count — most foundational choices are identity/experience
decisions that live in the `Artifact` itself, reviewed via `processes/design-decision-review.md`,
never a `proposals:` entry.

When this task arrived via a planner-produced queue, it names a concrete feature to scope against —
cover the sections above only to the depth that feature actually needs, same restraint
`processes/ui-library-init.md` applies.

---

## Findings — bugs and gaps are not proposals

Documenting an existing project will surface defects: treatments that contradict the system's own
evident intent, states with no defined behavior, broken or missing affordances. These are
**findings, not principles** — a defect observation is not earned judgment, and proposing it
pollutes the handoff's `proposals` field with entries the gate can only kill.

Route findings to the handoff's `Surfaced` section, one line each: what was observed, where, and
why it reads as unintended rather than chosen. The orchestrator relays `Surfaced` verbatim; the
operator triages — fix now, queue as coder work, or declare it intended (at which point it may
become part of the library's documented pattern).

The library records the **intended** pattern, not the defect: where the dominant convention is
clear, document that and note the deviation as a deviation. Documenting a bug as if it were a
convention re-teaches it to every future session.

---

## Output format

### corpora/ux-library.md

Structure the document with a section per topic above, in `processes/bootstrap.md`'s library document format
(narrative prose, concrete named values, never the domain-corpus `principles:` shape).

### Proposed experience principles

Distill any genuine judgment the session surfaced — a real tradeoff whose reason will bind future
weighing, distinct from the identity/experience decisions the library itself records — into
principles in the standard schema, and surface them in the handoff's `proposals` field with
`kind: judgment` (rarely `knowledge`). You propose the judgment; the orchestrator assigns each
ratified principle to a design domain at the gate and writes it to `corpora/domains/<domain>.md`.
No target count — propose what the work genuinely surfaced, and none is a valid outcome when the
library captured everything as identity/experience decisions.

### Handoff

End by writing the handoff artifact per `kernel.md`, "The handoff artifact": the library goes in
the `Artifact` section — reviewed via `processes/design-decision-review.md`, not filed as a
proposal — and any genuine judgment goes in `proposals` (provenance `"Bootstrap session, [date],
[project name]."`). This phase documents experience, not visuals — leave `ui-drift.screens`/
`.components` empty; it has no shared components of its own to name.
