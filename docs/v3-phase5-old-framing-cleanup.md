# v3 phase 5 — old-framing cleanup backlog

Not a superpowers-style plan. Just a list of leftover "this replaces X because Y" comparative
narration in the rewritten files, found by grepping for it after phases 0–3 landed. Pick up after
the UI screenshot cache work. `LINEAGE.md` is exempt — comparative/historical framing belongs
there by design, it already has its v3 entry, don't touch it.

Goal for each item: rewrite to plain present-tense description of the current mechanism. Keep the
*reasoning* (the "why") where it's genuinely load-bearing — the point is to stop referencing the
old, retired thing as the reason for explaining the new one, not to strip all rationale.

## kernel.md

- **"Spawns: stance + composed domain subset" intro** (~lines 128–154): "the one invariant carried
  over unchanged from the earlier lens-file model," "no longer inspectable in advance by reading a
  fixed lens file," "excluded from this collapse" — all reference the transition event instead of
  just stating the current rule. Rewrite plainly: state the no-stance-mixing invariant, the
  handoff's `domains-loaded:` field, and the orchestrator/planner exclusion as current facts, no
  "used to be a file" framing.
- **"Domain assignment at the gate"** (~line 280): "the exact failure mode a persistent named lens
  file used to invite" — reword to state what the fit-justification step guards against directly,
  without the comparison. Keep the LINEAGE.md pointer if a "why this exists" reference is still
  useful, but don't lean the sentence itself on the old mechanism.
- **"Write-back format" / "Retired principle" section** (~lines 311–327): structured almost
  entirely as "the old `promoted:` mechanism did X and Y; the new one doesn't need X because Z,
  and Y because W." Heaviest concentration of leftover comparative framing in the file. Rewrite as
  a plain description of the fold-to-preamble rule and why a separate authority tier is
  undesirable on its own terms (ossification risk) — not "here's what used to happen instead."

## Domain preambles referencing the migration event

- `domains/coding-general.md` (preamble) and `packs/web-frontend/domains/coding-ts.md` (preamble)
  both say "folded here from the audit layer's retired `promoted:` section (v3-redesign-proposal.md,
  2026-07-21)." Once the content has been stable a while, drop the migration citation and just
  state the content as current scene-setting — the `history:` entries in `audit.md` already carry
  the actual provenance record, so the preamble doesn't need to re-explain it.
- `domains/role-aliases.md`'s header: "Seeded 2026-07-21 (v3 lens-collapse migration, retiring
  `coder.md`...)" — same treatment; the seeding note was useful right after the migration, less so
  once aliases have accumulated beyond the original three.

## Checked, found clean (no action needed)

`SKILL.md`, `bootstrap.md`, `README.md`, and the rest of the pack domain files were grepped for
the same patterns and came back clean — the file-reference sweep already done during phase 3/the
consistency pass (Task 16) caught the stale-mechanism references; what's left above is
prose-level "why we changed this" framing, a different and smaller category.
