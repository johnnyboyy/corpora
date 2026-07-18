# Domain fork adoption

Projects currently always merge seed domains (kernel `domains/` + pack `packs/<pack>/domains/`)
with their own project domains (`corpora/domains/<domain>.md`) — every edit to a seed file changes
what every project using it loads, with no per-project isolation. This adds an opt-in **fork**: a
project can adopt a domain, after which its local copy is the sole source of truth for that domain
and the seed is no longer consulted. Resyncing a fork against later seed changes is out of scope —
noted as future work.

## Mechanism

- **Trigger:** `corpus.py adopt <domain>`, run from a project root. The script locates the seed or
  pack file for that domain (same lookup roles already use per `coder.md`/`ui-designer.md`'s "Load
  order" sections) and prints its principles. It does not judge — same separation of arithmetic
  from judgment as every other `corpus.py` command.
- **Curation:** the assistant proposes which of the printed principles are project-relevant vs.
  droppable, with a one-line reason each. Operator approves or edits the split.
- **Write:** the assistant writes the approved principles into `corpora/domains/<domain>.md`,
  merged by `id` with any principles already there, and sets frontmatter:
  `fork-status: forked`, `forked-from: <seed path>`, `forked-date: <YYYY-MM-DD>`.
- **Load-order change (`kernel.md`, "Project corpora"):** the existing rule — "for each domain the
  role declares, load the seed domain (if any) then the project domain (if any) of the same name" —
  gains one clause: if the project domain file declares `fork-status: forked`, load *only* the
  project file; otherwise behavior is unchanged (seed + project, as today).

## Errors

- Adopting a domain with no seed/pack counterpart (project-only domain) is a no-op error — nothing
  to fork from.
- Re-running `adopt` on an already-forked domain refuses (one-way for now; not a resync).

## Out of scope

Drift-checking or re-syncing a fork against later seed changes. Left as the next open thread.

## Testing

- `tests/test_corpus.py`: `adopt` resolves the correct seed file across kernel vs. pack layers;
  errors correctly on no-seed and already-forked cases.
- The load-order clause is prose the model follows during role assembly, not code — no runtime
  loader exists to unit-test. Verified by inspection of `kernel.md`'s wording, not by a script test.
