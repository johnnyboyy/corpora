---
name: corpora:chunk-accounting
description: The command sequence for the chunk ledger — previewing a composition, closing a chunk against its handoff, and summarizing a finished workstream, with the load-bearing ordering constraint that chunk-done must run before handoff-done. The kernel holds the ledger schema and why the ledger records rather than replaces the work.
---

# Chunk accounting

The step-by-step operations against the append-only chunk ledger (`corpora/chunks/<workstream>.md`).
What a chunk *is*, the ledger's YAML schema, and why `domains-composed` is script-written rather
than self-reported all live in `kernel.md`, "Chunk chaining"; this file is the *sequence*.

**Invoked from:** `processes/general-operation.md` Phase 6 (chunk-close, step 8), and the
retrospective (`close-workstream` summary).

## Preview a composition (optional, writes nothing)

```
corpus.py chunk-start --workstream <W> --unit-of-work <U>
```

Runs the same `select` call the spawn brief already made and prints the composition. This is a
preview only — the ledger is append-only and is written *only* once a real handoff exists to point
at, so there is no in-progress entry to record before the spawn starts.

## Close a chunk

```
corpus.py chunk-done --workstream <W> --unit-of-work <U> --stance <S> --handoff <path> [--next <U2>]
```

Use the handoff's own `workstream:`/`stance:` fields and the `unit-of-work:` held from the spawn
brief (Phase 3). This re-runs `select` itself to write `domains-composed` (never self-reported),
appends the entry, and:

- **fails if the handoff file does not exist** — which is what makes ordering load-bearing:
  `chunk-done` must run *before* `handoff-done` closes (deletes or archives) the handoff file it
  points at, never after. This order is not stylistic.
- **fails if the handoff does not name the same `workstream`.**
- **fails if the handoff's `domains-loaded:` field (when present) disagrees with the recomputed
  `select()`** — a real fidelity discrepancy to investigate (fix the composing process or the
  spawn), never a mismatch to paper over by hand-editing the ledger. A handoff written before this
  schema field existed, or by a process that doesn't self-report it, skips this check rather than
  failing retroactively.

Only after `chunk-done` succeeds, close the handoff: `corpus.py handoff-done <file>`.

## Summarize a finished workstream

```
corpus.py close-workstream <W>
```

A read-only summary once every chunk in a workstream is done — it aggregates the ledger for the
retrospective. It does **not** fold multiple chunks' handoffs into one.
