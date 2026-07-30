---
name: corpora:screenshot-library-sync
description: Keep corpora/screenshots/manifest.md current as coder-side changes invalidate existing captures. Runs inline at the ratify gate — mechanical, no design judgment, so it never spawns a design composition.
---

# Screenshot library sync

**Trigger:** right after processing any handoff whose `ui-drift.screens` or `.components` is
non-empty (`processes/general-operation.md`, Phase 6, step 7, and Phase 7). Unlike `processes/ui-library-sync.md`, this
runs every time the signal appears, not on a threshold — invalidating a stale screenshot is cheap
to check and expensive to leave silently wrong.

**No composition, no stance.** This is orchestrator procedure, not a composed spawn — the same
reasoning that keeps `processes/screenshot-library-init.md` out of a design composition. It does not go
through `processes/general-operation.md`'s spawn lifecycle as its own unit of work; it runs inline within the
gate pass that produced the drift signal and produces no handoff of its own.

---

## Procedure

1. Run `corpus.py screenshot-mark-stale --screens <ids> --components <names>` using the handoff's
   own `ui-drift.screens`/`.components` — it expands `.components` into every screen the manifest's
   own tags already show it on, so the handoff never has to enumerate the ripple itself.
2. For each screen the command reports as invalidated, recapture immediately using the project's
   browser automation tool and register the result with `corpus.py screenshot-record`, still inline
   in the same gate pass.
3. If no browser automation tool is available this session, leave the invalidated screens marked
   stale; capture is deferred until a session with the tool processes them.

A screen or component with no prior manifest entry at all is not this phase's concern —
`screenshot-mark-stale` is a no-op for an unknown screen, and a genuinely new screen (bootstrap
time) is `processes/screenshot-library-init.md`'s job, not this one's.
