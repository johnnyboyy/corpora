# Audit record — kernel-seed layer

Provenance, promotions, and per-kill audit detail for the kernel-seed domains
(`coding-general`, `orchestrator-routing`). Loaded only at ratify/retrospective time — never in a
role's working context. Keyed by principle `id`, each noting its `domain`. See `kernel.md`,
"Storage: working vs audit." (Kill logs live in the per-domain working files so they are available
in the working context.)

```yaml
provenance:

# domain: coding-general
- id: ask-before-architecture
  domain: coding-general
  provenance: "2026-06-26, Blog project. Reached for a CSS class without checking whether the intent was component extraction — required redirection."

- id: verify-before-bulk-edit
  domain: coding-general
  provenance: "2026-05-26, Blog project."

- id: grep-subdirs-before-delete
  domain: coding-general
  provenance: "2026-06-02, Blog project cross-tool shared components refactor."

- id: code-lives-at-consumer-level
  domain: coding-general
  provenance: "Merged from hook-colocation-by-usage, duplicate-formatters-belong-in-lib, tool-shared-components-level, Blog project 2026-06-17."

- id: generic-defers-to-consumer
  domain: coding-general
  provenance: "2026-06-04, Blog project Modal component."

- id: single-callsite-helper-scoped
  domain: coding-general
  provenance: "2026-06-04, Blog project box-selector refactor. Generalized from className-builder framing."

- id: ceiling-comment-for-deliberate-shortcuts
  domain: coding-general
  provenance: "2026-06-15, adapted from ponytail skill review."

- id: two-approaches-then-decide
  domain: coding-general
  provenance: "2026-06-16, Blog project dropdown positioning — cycled through five approaches before floating-ui replaced it with a one-line CSS change."

- id: unified-representation-no-type-leakage
  domain: coding-general
  provenance: "Merged from hook-api-hides-internal-branching + no-special-cased-current-item, Blog project 2026-06-17."

- id: color-utility-over-guesswork
  domain: coding-general
  provenance: "LINEAGE.md, 'Why a color utility exists.' Color derivation session where iterative guessing produced inaccurate LCH results and burned tokens; a small script replaced that with exact single-command output."

# domain: orchestrator-routing
- id: brief-ends-at-what
  domain: orchestrator-routing
  provenance: "2026-06-01, box-fill calculator box picker. Orchestrator computed SVG coordinates and TypeScript types in the brief, leaving the coder nothing to transcribe."

- id: stop-and-route
  domain: orchestrator-routing
  provenance: "2026-06-01, box-fill calculator redesign. Orchestrator entered designer mode and produced the full design spec inline rather than spawning the designer role."

- id: frame-before-routing
  domain: orchestrator-routing
  provenance: "2026-06-01, orchestrator corpus setup."

- id: pre-scan-before-spawning
  domain: orchestrator-routing
  provenance: "2026-06-02, codebase audit session. Three parallel agents each ran independent discovery; user noted the redundancy."

- id: route-questions-not-roles
  domain: orchestrator-routing
  provenance: "2026-06-12, operator feedback: established pipeline caused reflex spawning; question-routing better matches actual cost structure."

- id: surface-design-questions-neutrally
  domain: orchestrator-routing
  provenance: "2026-06-12, operator clarified: orchestrator should not drift into design thinking even when capable."

- id: spawn-threshold-is-spec-scope
  domain: orchestrator-routing
  provenance: "2026-06-12, operator noted spawn cost often exceeds decision value."

- id: inline-coder-session-protocol
  domain: orchestrator-routing
  provenance: "2026-06-17, orchestrator retrospective. Merged from inline-session-enters-coder-role and close-inline-role-at-approval-gate."
  history:
    - date: 2026-06-22
      type: generalized
      reason: "Reworded from 'load coder.md' to 'load the coder lens and its declared domains' to match the lens+declaration model introduced in the corpus redesign. No change to the judgment."

- id: design-question-during-coder-session
  domain: orchestrator-routing
  provenance: "2026-06-17, orchestrator retrospective."

- id: audit-request-means-spawn-designer
  domain: orchestrator-routing
  provenance: "2026-06-13, load calculator audit session — orchestrator implemented operator-listed concerns as code and skipped the designer spawn."

- id: spawn-token-summary
  domain: orchestrator-routing
  provenance: "2026-06-19, operator requested visibility after aggregate-only reporting made cost analysis opaque."

- id: full-corpus-on-spawn
  domain: orchestrator-routing
  provenance: "2026-06-19, operator rejected selective inclusion after orchestrator proposed it as a cost-reduction strategy."
  history:
    - date: 2026-06-22
      type: generalized
      reason: "Reframed from 'pass the full role corpus' to 'pass every declared domain in full' for the lens+declaration model. Added the explicit note that loading only declared domains is a fixed contract, not a relevance judgment — so domain-scoping does not violate this principle (the central hazard the redesign had to guard)."

- id: ratify-gate-judgment-vs-knowledge
  domain: orchestrator-routing
  provenance: "2026-06-22, FAMOUS 3D keyboard-key grid ratify session. Orchestrator killed preserve-3d-chain on its own judgment ('a model would know this from training') without routing the distinction to the operator. Post-session reflection surfaced why the role is better positioned to make this call than the orchestrator. Operator confirmed the orchestrator principle is thinner: route the question, don't answer it."

- id: domain-assignment-at-ratify-gate
  domain: orchestrator-routing
  provenance: "2026-06-22, corpus redesign. Domain-scoping moved corpus ownership off roles; the ratify gate became the point where a proposal is assigned a domain (or a new domain is born). New principle introduced with the redesign, not yet pressure-tested on a live ratify session — provisional."

# domain: planning
- id: task-describes-output-not-implementation
  domain: planning
  provenance: "2026-06-22, FAMOUS disc-02. Planner described the implementation path (files to touch, data to thread) rather than the observable output. Operator noticed and flagged it; principle surfaced through operator investigation, not through the planner's self-check."

promoted:

# domain: coding-general
- id: explicit-by-default
  domain: coding-general
  promoted_to: coder lens — "General conventions" section
  provenance: "Blog project, 'Explicit by Default' post (content/posts/coding/explicit-by-default.mdx). The umbrella the operator's individual coding rules turned out to be instances of — named by Claude Code while it was taught the rules alongside their whys. The realization that the whys mattered more than the rules is what seeded this corpora system. Held as a PEER of prefer-error-exposing-form, not its parent: whether one subsumes the other is a question for a future retrospective to surface from evidence, not a top-down call."

- id: prefer-error-exposing-form
  domain: coding-general
  promoted_to: coder lens — "General conventions" section
  provenance: "2026-06-19, Blog project. JSLint/Crockford analysis. A peer of explicit-by-default; its concrete instances live in pack overlays."

- id: deletion-over-addition
  domain: coding-general
  promoted_to: coder lens — "What you do" section (prefer smaller net addition)
  provenance: "2026-06-17, Blog project retrospective."

- id: yagni-gate-before-implementing
  domain: coding-general
  promoted_to: coder lens — "What you do" section (ask whether it needs to exist, stdlib, installed dep)
  provenance: "2026-06-17, Blog project retrospective."

- id: verify-build-not-just-lint
  domain: coding-general
  promoted_to: coder lens — "What you do" section (run the project's verification commands before finishing)
  provenance: "2026-06-17, Blog project retrospective."
```
