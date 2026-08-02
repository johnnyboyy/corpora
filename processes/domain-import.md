---
name: corpora:domain-import
description: Re-propose an already-ratified principle or convention from another domains-dir into this project's own corpora/domains/, through the ordinary ratify gate. Mechanical browsing and candidate-filing; the domain-assignment judgment is the same one the ratify gate already applies to any proposal.
---

# Domain import

**Trigger:** a project wants to pull already-ratified content from another corpora location (this
skill's own `domains/`, another project's `corpora/domains/`) into its own `corpora/domains/`
— at bootstrap (the default-pool fast path, `processes/bootstrap.md`), a project migrating off the
old live-merge model (`processes/domain-repo-migration.md`), or any time later to pick up new or
updated content.

**No composition, no stance of its own.** Browsing and filing a candidate needs no design or code
judgment — the one judgment point, which destination domain a picked entry belongs to, is the same
`domain-assignment-at-ratify-gate` judgment the gate already applies to any proposal, applied here
to an imported entry instead of a freshly-mined one. This file is the procedure; the candidate
schema and command syntax are `kernel.md`, "Project corpora → Import."

---

## Procedure

1. **Browse first, propose nothing yet.** `corpus.py import-list --source <domains-dir>` lists
   every principle and convention at the source, flagging which ids already exist anywhere in the
   project's own `corpora/domains/`.
2. **File candidates.** For each entry worth pulling in, `corpus.py import-candidate --source
   <domains-dir> --domain <d> --id <id> [--as-domain <d2>] [--as-id <id2>]` appends it to
   `corpora/import-candidates.md` with its `imported-from` provenance block (schema in
   `kernel.md`). For a bootstrap's bulk pull, `corpus.py import-default-pool [--source
   <domains-dir>]` does this for every entry that already matches the project's shape, in one
   batch, instead of one at a time.
3. **Ratify like any other candidate.** Each filed entry goes through the ordinary ratify gate —
   the operator (or gate-running orchestrator) picks a destination domain per entry, not
   necessarily the source's own domain name, and ratifies or rejects it individually. `kind:
   judgment` is the default (the entry already cleared the fork test once, in its source corpus),
   but the fork test remains available to re-examine a specific entry rather than rubber-stamp it.
4. **Write back with `ratify-import-candidate`.** `corpus.py ratify-import-candidate --id <id>
   [--as-domain <d2>] [--as-id <id2>]` writes a ratified entry into its destination domain, files
   its `imported-from` provenance in the layer's audit file, records the gate, and removes it from
   `corpora/import-candidates.md` — one atomic step, no hand edit to either file (`kernel.md`,
   "Write-back format"). A convention-shaped candidate (no `condition`) isn't handled by that
   command yet — write it back into `conventions:` by hand, matching the same schema.

**Repeat rather than fork.** A project that wants to track a source's domain content as it evolves
re-runs this same procedure periodically (or per updated principle) instead of forking a live copy
— there is no separate sync mechanism to maintain.
