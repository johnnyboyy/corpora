---
name: corpora:design-decision-review
description: Review a divergent spawn's Artifact (a UI/UX identity or aesthetic decision) as accept / revise / reject, and file an accepted decision into the project's UI/UX library — entirely separate from the ratify gate, which handles only judgment/knowledge principle proposals.
---

# Design decision review

**Trigger:** any handoff whose `stance: divergent`, or whose `Artifact` targets `ui-library.md`/
`ux-library.md` content (a library-founding spawn, `processes/ui-library-init.md`/
`processes/ux-library-init.md`; an ongoing designer spawn, `processes/ui-library-sync.md`/
`processes/ux-library-sync.md`; or any other divergent-composed spawn). Runs as part of
`processes/general-operation.md`'s Phase 5 (Relay), before Phase 6 (the ratify gate) ever sees the
handoff. See `kernel.md`, "Design decision review," for why this is a separate procedure and not a
third route through the gate.

## Why this is not the ratify gate

A design decision has no condition to weigh a future case against and no fork to guard against
re-litigating — it is simply what the project's identity *is*, right now. It was never a principle
candidate, so it never enters `proposals:` and never reaches Phase 6. The `Artifact` section
already carries the decision in full (the library document, or the delta a design spec proposes
against it) — this process reviews and files that content directly, rather than asking the spawn to
also restate it as a fake principle with a fabricated `rule`/`condition`/`reason` it doesn't have.

## Procedure

1. **Present the `Artifact`** to the operator as a single unit — the whole library document (a
   founding spawn) or the specific section(s) it proposes changing (an ongoing designer spawn).
2. **Accept, revise, or reject** — the operator's only three responses:
   - **Accept**: write the accepted content into `ui-library.md`/`ux-library.md` now, replacing the
     superseded section outright. No "(direction, `<date>`, implemented)" tag, no "supersedes the
     prior X" lead-in, no dates, no naming what was rejected or why — the library describes only
     current state, and git history is its complete audit trail (`kernel.md`, "Design decision
     review"). If the accepting spawn is still live (same turn), have it perform the write itself,
     the same way `processes/ui-library-init.md`'s founding task already does; otherwise the
     orchestrator applies the accepted content directly.
   - **Revise**: relay the operator's specific feedback and resume the same workstream agent — the
     same continuation mechanic `kernel.md`'s `status: questions-pending` uses — returning control
     to Phase 4. This is not a rejection: the workstream and its context survive.
   - **Reject**: discard. There is no kill log entry and no `reason_killed` to write — a rejected
     design decision has no future re-proposal to guard against the way a killed principle does. If
     the rejection reveals a settled constraint worth stating for next time (e.g. "this direction
     conflicts with the density already established in ui-library.md §3"), that's already recorded
     in the library itself; nothing new needs writing.
3. **Ui-drift stays open until accepted.** The handoff's self-reported `ui-drift.screens`/
   `.components` describe what the spawn touched; they only mean the library is caught up once the
   corresponding decision is actually accepted and written. A revised or rejected Artifact leaves
   the drift counters as they were — don't clear them on a revision or rejection.
4. **Resolve deferred decisions.** For any `corpora/deferred-decisions.md` entry this acceptance
   settles, mark it `status: resolved` and remove it (`kernel.md`, "Deferred UI/UX decisions"); run
   `corpus.py lint-deferred` after editing. A revision or rejection does not resolve the entry it
   was answering.
5. **Any genuine judgment or knowledge the session also surfaced** — a real tradeoff whose reason
   will bind future weighing, distinct from the identity choice itself — still goes through
   `proposals:` and Phase 6, same as any other spawn's output. This process only ever handles the
   `Artifact`; it has no opinion on `proposals:` and does not gate them.

## After this step

Once the Artifact is accepted, revised-and-resumed, or rejected, continue Phase 5 as normal (any
`tradeoffs` block, any `status: blocked` scope divergence), then proceed to Phase 6 for whatever
`proposals:` entries remain in the handoff — judgment/knowledge only.
