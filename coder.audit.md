# Coder audit record (base — stack-agnostic)

Provenance and promotions for `coder.md`. Loaded only at ratify/retrospective time — never in a
coder's working context. Keyed by principle `id`. See `kernel.md`, "Storage: working vs audit."
(The kill log lives in `coder.md` so it is available in the working context.)

```yaml
provenance:

- id: ask-before-architecture
  provenance: "2026-06-26, Blog project. Reached for a CSS class without checking whether the intent was component extraction — required redirection."

- id: verify-before-bulk-edit
  provenance: "2026-05-26, Blog project."

- id: grep-subdirs-before-delete
  provenance: "2026-06-02, Blog project cross-tool shared components refactor."

- id: code-lives-at-consumer-level
  provenance: "Merged from hook-colocation-by-usage, duplicate-formatters-belong-in-lib, tool-shared-components-level, Blog project 2026-06-17."

- id: generic-defers-to-consumer
  provenance: "2026-06-04, Blog project Modal component."

- id: single-callsite-helper-scoped
  provenance: "2026-06-04, Blog project box-selector refactor. Generalized from className-builder framing."

- id: ceiling-comment-for-deliberate-shortcuts
  provenance: "2026-06-15, adapted from ponytail skill review."

- id: two-approaches-then-decide
  provenance: "2026-06-16, Blog project dropdown positioning — cycled through five approaches before floating-ui replaced it with a one-line CSS change."

- id: unified-representation-no-type-leakage
  provenance: "Merged from hook-api-hides-internal-branching + no-special-cased-current-item, Blog project 2026-06-17."

- id: color-utility-over-guesswork
  provenance: "LINEAGE.md, 'Why a color utility exists.' Color derivation session where iterative guessing produced inaccurate LCH results and burned tokens; a small script replaced that with exact single-command output."

promoted:
# Principles that graduated from corpus entries to baked-in conventions in the base coder
# prompt. Kept here so the audit trail is legible — a ratified principle that also appears in
# the prompt should not be re-proposed as a corpus entry.

- id: explicit-by-default
  promoted_to: coder role prompt — "General conventions" section
  provenance: "Blog project, 'Explicit by Default' post (content/posts/coding/explicit-by-default.mdx). The umbrella the operator's individual coding rules turned out to be instances of — named by Claude Code while it was taught the rules alongside their whys. The realization that the whys mattered more than the rules is what seeded this corpora system. Held as a PEER of prefer-error-exposing-form, not its parent: whether one subsumes the other is a question for a future retrospective to surface from evidence, not a top-down call."

- id: prefer-error-exposing-form
  promoted_to: coder role prompt — "General conventions" section
  provenance: "2026-06-19, Blog project. JSLint/Crockford analysis. A peer of explicit-by-default; its concrete instances live in pack overlays."

- id: deletion-over-addition
  promoted_to: coder role prompt — "What you do" section (prefer smaller net addition)
  provenance: "2026-06-17, Blog project retrospective."

- id: yagni-gate-before-implementing
  promoted_to: coder role prompt — "What you do" section (ask whether it needs to exist, stdlib, installed dep)
  provenance: "2026-06-17, Blog project retrospective."

- id: verify-build-not-just-lint
  promoted_to: coder role prompt — "What you do" section (run the project's verification commands before finishing)
  provenance: "2026-06-17, Blog project retrospective."

```
