# UI screenshot cache — design

## Problem

A UI-design spawn currently has no persistent visual reference for the app it's working on.
`ui-library.md` documents color/typography/component-vocabulary in prose — deliberately, per
`LINEAGE.md`'s "Why the UI library is text, not design artifacts" (token cost, precision,
staleness) — and the `documentation-before-screenshots` principle keeps live screenshot capture
scoped to a narrow exception (verifying aesthetic quality of a specific state). Neither gives a
spawn a way to *see* what already exists across the whole app before deciding whether to build a
new component or reuse one. Prose can describe a button; it's a worse tool than an image for "is
there already something close enough to this that I should reuse it."

This is additive to the existing text-first philosophy, not a fix for a wasteful pattern — there
is no current blanket-recapture behavior anywhere in the system to remove.

## Goals

- Give any `ui-design`-composed spawn full-app visual awareness (every screen) without redundant
  capture — read the cache, only recapture what's actually stale.
- Support reuse discovery: given a component name, find every screen that already shows it.
- Keep the cache accurate under two kinds of change: a screen's own content changing, and a
  shared component changing in a way that ripples to every screen that uses it.
- Defer capture to handoff time — iterative mid-session work on a screen should not trigger
  repeated recapture; only the final, self-reported state at handoff matters.
- Stay mechanically driven (`corpus.py`), matching every other corpora ledger's script-owned
  bookkeeping — minimize what a spawn or the orchestrator has to infer by hand.

## Non-goals

- A full variant matrix (every mode × breakpoint × state) per screen, maintained proactively.
  Variants beyond one canonical shot are added only when a task actually needs one.
- Automatic detection of a component being *removed* from a screen. If a screen's tag list still
  claims a component that's no longer there, that's a small, accepted drift — a `ui-design` spawn
  touching the screen again will refresh its tags naturally, and the operator can trigger a manual
  resync if they notice it going stale.
- Replacing `ui-library.md` prose. The library stays authoritative for specification (exact
  tokens, states, behavior); the cache is a visual companion for orientation and reuse-spotting.

## Architecture

```
corpora/screenshots/
  manifest.md              # single ledger, fenced YAML, script-managed (like deferred-decisions.md)
  now-playing/
    default.png
  discover/
    default.png
    dark.png                # variants exist only once a task has actually needed them
```

One canonical screenshot per screen by default (comprehensive across *screens*, not proactively
comprehensive across *variants*). `manifest.md` is the single source of truth for what's cached,
its component tags, and its freshness — read once at the start of `ui-design` work for full-app
awareness, instead of a blanket live-capture pass.

## Manifest schema

```yaml
screens:
  - id: now-playing
    components: [transport-cluster, queue-sheet, radial-scrubber, like-button]
    status: current          # current | stale
    last-touched: 2026-07-21
    variants:
      - label: default
        path: now-playing/default.png
        captured: 2026-07-21
```

`status` is per-screen, not per-variant — deliberate simplification (YAGNI): if a screen drifts,
all its variants are treated as stale together rather than tracking independent staleness per
mode. Revisit only if that coarseness turns out to matter in practice.

`components` names are anchored to whatever `ui-library.md`'s own "Component vocabulary" section
already calls that component — no separate naming registry. If a component gets renamed in the
library, the tag drifts until a `ui-design` spawn next touches that screen and refreshes it (same
spawn edits both, in practice, so this mostly self-corrects).

## Handoff schema change

`kernel.md`'s handoff artifact currently has:

```yaml
ui-drift: no                 # yes | no — did this work change the rendered visual system
```

Replace with a structured field carrying both invalidation signals:

```yaml
ui-drift:
  screens: []                 # screen ids directly worked on, if any
  components: []               # shared component names changed, if any (matches ui-library.md's
                                #   own component vocabulary headings)
```

Empty on both = no drift (equivalent to the old `no`). A spawn names only what it touched
directly — it never has to enumerate which *other* screens a shared component appears on; that
expansion is mechanical (below). This also means a coder-only session (no `ui-design` spawn
involved) still correctly flags the screens it touched, even with no `components:` entries — the
screen-level signal is the safety net; the component-level ripple is the optimization on top of
it, and only fires when something explicitly names a changed shared component.

`library-drift`'s counter description ("gates where a handoff carried `ui-drift: yes`") updates to
"gates where a handoff's `ui-drift.screens` or `.components` was non-empty" — same trigger,
reworded for the new shape.

## Invalidation logic

At ratify-gate time, given a handoff's `ui-drift.screens` and `ui-drift.components`:

```
stale_screens = ui-drift.screens ∪ { screen.id for screen in manifest
                                      if screen.components ∩ ui-drift.components ≠ ∅ }
```

This is a single mechanical lookup against the manifest's existing `components:` tags — the same
tags that power reuse-discovery do double duty for ripple invalidation. Nothing about this
requires a spawn to know the full set of screens a component appears on.

**Known limitation, accepted:** this only catches ripples for components already tagged on the
screens that use them. A screen not recaptured since a component was added to it won't be in the
tag index yet, so a ripple to it would be missed. Since recapture is immediate (not batched), this
should stay accurate in practice, but it's not a hard guarantee.

## Recapture: mechanism and cadence

Recapture is immediate per-screen once flagged stale (no batching threshold like the text
library's `since-last-sync >= 3` — a single screenshot is cheap, so there's no reason to let a
known-stale entry sit that way). But it is **deferred to handoff time**, never mid-session: a
spawn iterating on a screen across several rounds only reports its final touched-screens list
once, at the end, exactly like every other handoff field.

Recapture itself is a **mechanical step in the existing ratify-gate procedure**, run by the
orchestrator directly via the project's registered browser automation tool — not a spawned role.
It requires no design judgment (just "go look at the current rendered state and save it"), so it
fits the same pattern as the orchestrator already running `corpus.py verify`/`lint-handoff`
without spawning anything for those. This also sidesteps the concern that text-library sync has
(needing a fresh session because re-deriving *why* something changed takes context) — a
screenshot capture needs no reasoning carried over, so the orchestrator can do it inline right
after processing the handoff.

## `corpus.py` additions

New subcommands, following the existing ledger pattern (`utility-candidates`/`deferred`):

- `screenshot-record --screen <id> --variant <label> --path <file> --components <comma-list>` —
  registers/updates a captured variant, stamps `captured:` date, sets `status: current`, updates
  the screen's `components:` tags.
- `screenshot-mark-stale --screens <comma-list> --components <comma-list>` — the invalidation step
  above; called at gate time from the handoff's `ui-drift` fields. Read-modify-write against
  `manifest.md`'s script-owned block.
- `screenshot-status` — lists current/stale/missing screens, for orchestrator visibility (mirrors
  `utility-candidates`/`deferred`).
- `screenshot-lookup --component <name>` — the reuse-discovery query: which screens already show
  this component, and where their images live.
- `lint-screenshots` — validates `manifest.md` structurally (every variant has a `path` that
  exists on disk, every screen has a `captured` date, no orphaned image files absent from the
  manifest), mirroring `lint-deferred`/`lint-utility-candidates`.

All of these get unit tests in `tests/test_corpus.py`, same TDD pattern as the rest of the file —
tests added alongside the mechanism, not after.

## Principle change: `documentation-before-screenshots`

Current text (`packs/web-frontend/domains/design-method.md`): "Use the browser automation tool for
screenshots only when the design system documentation does not answer the specific question.
Documentation is the default; screenshots are the exception."

This needs to distinguish **reading the cache** (free — no fresh capture, no cost the original
principle was guarding against) from **live capture** (still the exception, still gated the same
way). Reword to something like: "Consult the screenshot cache (`corpora/screenshots/manifest.md`)
freely for orientation and reuse-discovery — it costs nothing new to read. Reach for the browser
automation tool for a *fresh* capture only when the cache is missing or stale for a screen you
need, or to verify aesthetic quality the text documentation can't fully characterize — documented
specification remains the default source of truth for exact values." Exact wording finalized at
implementation time; the substance is "reading cached images is normal now, live capture stays
the exception."

## Bootstrap and existing-project seeding

Nothing today seeds this cache — `bootstrap.md` has no existing blanket-screenshot step to repurpose.

- **New projects:** Phase 2 (`ui-design` bootstrap) gains an explicit step: while establishing
  `ui-library.md`, capture one canonical screenshot per identified screen and register each via
  `corpus.py screenshot-record`, seeding `manifest.md` alongside the library.
- **Already-bootstrapped projects (FAMOUS today; Blog/Meridian once they're on v3):** a one-time
  backfill pass — capture every screen currently documented in `ui-library.md`'s structure once,
  register them, done outside the normal gate flow since there's no handoff driving it.

## Testing

- `corpus.py` unit tests for all five new subcommands (happy path, malformed manifest, missing
  file on disk, stale-marking via both screen and component paths, `lint-screenshots` catching
  each structural defect class).
- No UI/browser testing needed for the mechanism itself (that's the orchestrator's runtime
  browser-automation tool, already used elsewhere, not new).

## Open items for implementation time

- Exact reworded text for `documentation-before-screenshots` (substance agreed above, wording not
  finalized).
- Whether `screenshot-mark-stale` should also print which screens it invalidated (for gate
  visibility) — likely yes, matching `record-gate`'s existing print-what-happened convention, but
  not load-bearing to the design.
