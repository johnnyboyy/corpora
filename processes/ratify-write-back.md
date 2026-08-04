---
name: corpora:ratify-write-back
description: The mechanical write operations for a principle's lifecycle — ratifying a proposal into a domain, rejecting one into the kill log, reshaping a ratified principle's history, and graduating a principle to an unconditioned convention. Invoked from the ratify gate (general-operation.md Phase 6) and the retrospective; the kernel holds the YAML schemas these produce.
---

# Ratify write-back

The step-by-step write operations for moving a proposal into (or out of) a domain corpus. The
data contracts — the exact YAML shapes for a ratified principle, a `history:` sub-list, a
convention, a killed entry — live in `kernel.md`, "Write-back format" and "Killed entries"; this
file is the *sequence*, not the schema. Retiring an *old* kill is a different operation, in
`processes/kill-graduation.md`.

**Invoked from:** `processes/general-operation.md` Phase 6 (ratify/reject, per proposal) and
`processes/retrospective.md` (graduate-to-convention, at retrospective time).

None of these hand-edit a YAML block into place where a `corpus.py` command exists for it — the
script writes the working fields, files provenance in the audit layer, and records the gate as one
atomic step. Hand-editing is the manual fallback only for a domains-dir the script can't reach.

## Ratify a proposal into a domain

For a **freshly-authored or mined** proposal the operator ratified (or edited — write the edited
version, not the original):

```
corpus.py add-principle --domain <d> --id <id> --rule "..." --condition "..." --reason "..." \
  --provenance "..." [--kind judgment|knowledge] [--see-also <id>]
```

This appends the working fields to the target domain's `principles:`, files the matching
`provenance` by `id` in that layer's audit file (provenance is captured at proposal time, not
authored here), and records the proposal's own `ratified` count — atomically. The working file's
principle carries no `provenance` field; it lives in the audit layer only.

For a proposal **sourced from an import candidate** (already queued in
`corpora/import-candidates.md` by `import-candidate`/`import-default-pool`, per
`processes/domain-import.md`):

```
corpus.py ratify-import-candidate --id <id> --as-domain <d> [--as-id <id2>]
```

This does the same write-back plus carries the candidate's `imported-from` provenance block, and
removes the entry from the candidates file — all together. The `imported-from` block is additional
provenance, not a different write path.

## Reject a proposal into the kill log

There is no script for this path yet — append by hand:

1. Append to the domain **working file**'s `killed:` log an entry with a stable `id`, a `kill_type`
   (`quality` | `container` | `attribution-noise` — see `kernel.md`, "Killed entries," for what
   each means), and `reason_killed` (the operator's reason).
2. Add the per-kill audit detail to that layer's audit file, keyed by the same `id`: its
   `provenance` (where the principle came from before it was killed) and a `killed: <YYYY-MM-DD>`
   date (required — it is what later enables graduation via `processes/kill-graduation.md`).

## Reshape a ratified principle (history)

When an already-ratified principle is meaningfully generalized, consolidated, split, or **moved to
another domain**, record it so the trail stays legible: add a `history:` sub-list to its audit-file
`provenance` entry, each item carrying `date`, `type` (`generalized` / `consolidated` / `split` /
`moved`), and `reason` (schema in `kernel.md`, "Write-back format"). Moving a principle to a
better-fitting domain is a file move plus a `type: moved` history entry — the principle names no
domain in a field, so the domain is just the file it lives in.

## Graduate a principle to a convention

Run at retrospective time, not at the gate. A principle ratified long enough that checking its
`condition` before every task is friction without benefit graduates into the working file's
`conventions:` list. This has no `corpus.py` command yet — do it by hand:

1. **Apply promotion restraint first (judgment).** This is the one judgment call gating this
   operation; the canonical statement is `kernel.md`, "Write-back format" (Promotion restraint) —
   in short, graduate only if the judgment is stable across the kinds of projects the domain
   serves, and when in doubt leave it in `principles:`. The rest of this operation is mechanical.
2. Move the entry from `principles:` to `conventions:` in the same working file, dropping its
   `condition` and keeping its `id`, `rule`, and `reason` (convention schema in `kernel.md`). A
   convention is unconditioned — checked whenever the domain loads — but keeps its `id`, so it stays
   addressable, killable, and reversible.
3. Add a `history:` entry (`type: graduated-to-convention`) to the principle's audit-layer
   `provenance` record. A principle that reappears as a corpus proposal after graduating is a
   signal of regression, not new insight — the trail is what makes that visible.
