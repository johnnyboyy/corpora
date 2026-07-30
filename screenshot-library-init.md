---
name: corpora:screenshot-library-init
description: Seed or backfill corpora/screenshots/manifest.md against the ratified corpora/ui-library.md. Runs once as bootstrap.md's Phase 3, or on demand later for a project whose cache is incomplete. Mechanical — no design judgment, so it never spawns a design composition.
---

# Screenshot library init

**Trigger, two shapes of the same procedure:**

- **At bootstrap:** `has-ui: yes`, `corpora/screenshots/manifest.md` doesn't exist yet, and
  `ui-library-init.md`'s handoff has been ratified — this phase reads the *ratified*
  `ui-library.md`, not a draft. Runs once, as `bootstrap.md`'s Phase 3 — see `bootstrap.md` for
  what precedes and follows this phase in the bootstrap sequence. Independent of
  `ux-library-init.md`: both phases depend only on `ui-library-init.md`, not on each other, and
  may run in either order.
- **On demand, later:** the operator asks to backfill an already-bootstrapped project's cache — a
  manifest that was skipped at bootstrap (no browser automation tool that session) or that has
  fallen behind a `ui-library.md` that grew since. Same procedure below, run against the project's
  current `ui-library.md`; step 1 already skips anything the manifest has current, so re-running
  this phase is safe whether the manifest is empty, partial, or already complete.

**No composition, no stance.** This is orchestrator procedure, not a composed spawn — identifying
and capturing a screen needs no design judgment, the same reasoning that keeps
`screenshot-library-sync.md` out of a design composition. It does not go through
`general-operation.md`'s spawn lifecycle; it runs inline and produces no handoff of its own.

---

## Procedure

1. Read the current `corpora/ui-library.md`'s component-vocabulary section. Every component and
   screen named there is a candidate entry. Check each against `corpus.py screenshot-status` (or
   `screenshot-lookup --component <name>`) and skip anything already current — this phase captures
   what's missing, it does not recapture what a sync process would otherwise own.
2. For each screen still missing, use the project's browser automation tool to capture one
   canonical screenshot and register it directly:

   ```
   corpus.py screenshot-record --screen <id> --variant default \
     --path <id>/default.png --components <comma-list of components shown>
   ```

   Save the image under `corpora/screenshots/<id>/default.png` before registering it — `record`
   stamps the manifest but does not itself invoke the browser tool.
3. One canonical shot per screen is enough; do not proactively capture variant states (dark mode,
   error states) unless the task already needs one.

If no browser automation tool is available this session, skip this phase entirely — an incomplete
cache grows the normal way, one `screenshot-record` at a time as later sessions touch
each screen. `bootstrap.md`'s sequence continues without waiting for it.
