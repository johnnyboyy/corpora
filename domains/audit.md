# Audit record — kernel-seed layer

Provenance and per-kill audit detail for the kernel-seed domains
(`coding-general`, `orchestrator-routing`). Loaded only at ratify/retrospective time — never in a
spawn's working context. Keyed by principle `id`, each noting its `domain`. See `kernel.md`,
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

- id: utility-over-guesswork
  domain: coding-general
  provenance: "LINEAGE.md, 'Why a color utility exists.' Color derivation session where iterative guessing produced inaccurate LCH results and burned tokens; a small script replaced that with exact single-command output."
  history:
    - date: 2026-07-18
      type: generalized
      reason: "Renamed from color-utility-over-guesswork and widened from color specifically to any deterministic, precision-sensitive, or repeatedly-recurring computation. Operator noticed this was the only coder-facing principle that ever told the coder to recognize and propose a utility candidate — every other domain's equivalent work (date math, geometric layout, hashing) had no trigger at all, since orchestrator-routing's surface-utility-candidates-liberally is the orchestrator's counterpart and the coder never loads that domain. Color kept as the canonical named instance, including its React Native-specific carve-out."

- id: no-single-char-names
  domain: coding-general
  provenance: "2026-06-24, authored directly from the meta-rules. Derivable from both Explicit by Default (single-character names force Reader Tax reconstruction on every read) and prefer-error-exposing-form (opaque names hide type mismatches and logic errors that a descriptive name would surface). Not surfaced by the coder — the meta-rule stance already suppresses the violation, so no failure ever triggered a proposal."

- id: structural-examination-at-working-checkpoint
  domain: coding-general
  kind: judgment
  provenance: "Promoted from FAMOUS project domain 2026-07-06. Surfaced 2026-07-05, FAMOUS lens system refactoring session: after implementing view transitions + scroll restoration + typed ref registry, the examination pass surfaced the thin useScrollLensRef wrapper, an anonymous scroll-restoration useLayoutEffect, string-selector coupling, and the emergent LensRowEntry grouping. Promoted from FAMOUS to seed — condition makes no reference to FAMOUS-specific structure."

- id: module-boundaries-precede-deployment-separation
  domain: coding-general
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (youtube.com/watch?v=4qfsmE11Ejo). Ratified directly to seed — stack-agnostic architecture judgment with no FAMOUS-specific condition; FAMOUS itself (single Expo app) has no current use case, but the principle is written for any project considering a monolith-to-services split."

- id: dependency-graph-over-architecture-diagrams
  domain: coding-general
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (youtube.com/watch?v=4qfsmE11Ejo), companion to module-boundaries-precede-deployment-separation from the same source. Ratified directly to seed for the same reason."

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

- id: route-questions-not-roles
  domain: orchestrator-routing
  provenance: "2026-06-12, operator feedback: established pipeline caused reflex spawning; question-routing better matches actual cost structure."
  history:
    - date: 2026-07-18
      type: generalized
      reason: "Absorbed design-question-during-coder-session. Rewrote the operator-surfacing default: it existed because spawned roles couldn't resume (one-shot) and a full spawn was expensive for one decision. Neither holds now — a role can pause on a question and resume, and non-blocking questions queue to the owning role's deferred-decisions queue for its next natural spawn instead of defaulting to the operator."
    - date: 2026-07-18
      type: narrowed
      reason: "Dropped the code-question clause. Operator reported never observing a code question routed to the coder in practice; the theoretical case (coder signal on a design tradeoff) is already better served by the coder's own tradeoffs block, surfaced once actually implementing rather than via a separate pre-implementation question."

- id: surface-design-questions-neutrally
  domain: orchestrator-routing
  provenance: "2026-06-12, operator clarified: orchestrator should not drift into design thinking even when capable."

- id: spawn-threshold-is-spec-scope
  domain: orchestrator-routing
  provenance: "2026-06-12, operator noted spawn cost often exceeds decision value."

- id: planner-over-brainstorming-for-scope
  domain: orchestrator-routing
  provenance: "2026-07-18, operator observation: the orchestrator already splits steps and roles well informally, but ambiguous-scope requests were often absorbed by the superpowers:brainstorming skill where the planner would be the better-fit reach — brainstorming has no corpus artifact, so that path leaves the planning domain permanently thin (planning had never had a retrospective at the time this was surfaced)."

- id: inline-coder-session-protocol
  domain: orchestrator-routing
  provenance: "2026-06-17, orchestrator retrospective. Merged from inline-session-enters-coder-role and close-inline-role-at-approval-gate."
  history:
    - date: 2026-06-22
      type: generalized
      reason: "Reworded from 'load coder.md' to 'load the coder lens and its declared domains' to match the lens+declaration model introduced in the corpus redesign. No change to the judgment."
    - date: 2026-07-21
      type: generalized
      reason: "Reworded from 'load the coder lens and its declared domains' to 'compose the coder alias' to match v3-redesign-proposal.md's stance+composition model — coder.md no longer exists as a file. No change to the judgment."

- id: design-question-during-coder-session
  domain: orchestrator-routing
  provenance: "2026-06-17, orchestrator retrospective."
  killed: 2026-07-18

- id: audit-request-means-spawn-designer
  domain: orchestrator-routing
  provenance: "2026-06-13, load calculator audit session — orchestrator implemented operator-listed concerns as code and skipped the designer spawn."
  history:
    - date: 2026-07-21
      type: generalized
      reason: "Reworded from 'spawn the UI Designer' to 'spawn a ui-design-composed spawn' — ui-designer.md no longer exists as a file. No change to the judgment."

# domain: ratify-gate (split from orchestrator-routing 2026-07-18; see LINEAGE.md, "The ratify-gate split")
- id: pre-scan-before-spawning
  domain: ratify-gate
  provenance: "2026-06-02, codebase audit session. Three parallel agents each ran independent discovery; user noted the redundancy."

- id: spawn-token-summary
  domain: ratify-gate
  provenance: "2026-06-19, operator requested visibility after aggregate-only reporting made cost analysis opaque."

- id: full-corpus-on-spawn
  domain: ratify-gate
  provenance: "2026-06-19, operator rejected selective inclusion after orchestrator proposed it as a cost-reduction strategy."
  history:
    - date: 2026-06-22
      type: generalized
      reason: "Reframed from 'pass the full role corpus' to 'pass every declared domain in full' for the lens+declaration model. Added the explicit note that loading only declared domains is a fixed contract, not a relevance judgment — so domain-scoping does not violate this principle (the central hazard the redesign had to guard)."

- id: ratify-gate-judgment-vs-knowledge
  domain: ratify-gate
  provenance: "2026-06-22, FAMOUS 3D keyboard-key grid ratify session. Orchestrator killed preserve-3d-chain on its own judgment ('a model would know this from training') without routing the distinction to the operator. Post-session reflection surfaced why the role is better positioned to make this call than the orchestrator. Operator confirmed the orchestrator principle is thinner: route the question, don't answer it."

- id: domain-assignment-at-ratify-gate
  domain: ratify-gate
  provenance: "2026-06-22, corpus redesign. Domain-scoping moved corpus ownership off roles; the ratify gate became the point where a proposal is assigned a domain (or a new domain is born). Exercised in practice 2026-06-28 (HiraganaQuiz ratify session)."

- id: artifact-points-to-persisted-file-not-full-reproduction
  domain: ratify-gate
  provenance: "Meridian project, 2026-07-17, retrospective conversation. Operator flagged that UI-library sync handoffs reproduced the whole ui-library.md document in the Artifact section despite the role having written directly to the file — real token cost paid once and then discarded when the handoff is deleted post-ratify. The schema's 'freeform' Artifact field never mandated full reproduction; this names the actual dividing line (does the content already have a persisted home the orchestrator can read) that the freeform language left implicit."

# domain: planning
- id: open-questions-are-explicit
  domain: planning
  provenance: "No provenance was ever recorded for this principle — a pre-existing gap found while executing the 2026-07-18 structural-kinship merge, backfilled here rather than left orphaned."
  history:
    - date: 2026-07-18
      type: generalized
      reason: "Absorbed surface-shared-concept-before-implementation as a named instance — a shared runtime concept two tasks would each touch is exactly 'information the planner doesn't have.'"

- id: task-describes-output-not-implementation
  domain: planning
  provenance: "2026-06-22, FAMOUS disc-02. Planner described the implementation path (files to touch, data to thread) rather than the observable output. Operator noticed and flagged it; principle surfaced through operator investigation, not through the planner's self-check."

- id: surface-shared-concept-before-implementation
  domain: planning
  provenance: "No provenance was ever recorded for this principle — same pre-existing gap as open-questions-are-explicit, backfilled here rather than left orphaned."
  killed: 2026-07-18

- id: no-re-export-from-peer-module
  domain: coding-general
  provenance: "Promoted 2026-07-06 from both Blog and FAMOUS project coding-general domains (Blog: 2026-06-28, hiragana quiz reviewer; FAMOUS: 2026-07-01, cross-project review). Two-project exposure via cross-project review. Promoted directly to lens convention — rule is near-unconditional (barrel exception is short enough to state inline) and needs no condition-weighing."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-general's own preamble."

- id: explicit-by-default
  domain: coding-general
  provenance: "Blog project, 'Explicit by Default' post (content/posts/coding/explicit-by-default.mdx). The umbrella the operator's individual coding rules turned out to be instances of — named by Claude Code while it was taught the rules alongside their whys. The realization that the whys mattered more than the rules is what seeded this corpora system. Held as a PEER of prefer-error-exposing-form, not its parent: whether one subsumes the other is a question for a future retrospective to surface from evidence, not a top-down call."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-general's own preamble."

- id: prefer-error-exposing-form
  domain: coding-general
  provenance: "2026-06-19, Blog project. JSLint/Crockford analysis. A peer of explicit-by-default; its concrete instances live in pack overlays."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-general's own preamble."

- id: deletion-over-addition
  domain: coding-general
  provenance: "2026-06-17, Blog project retrospective."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-general's own preamble."

- id: yagni-gate-before-implementing
  domain: coding-general
  provenance: "2026-06-17, Blog project retrospective."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-general's own preamble."

- id: verify-build-not-just-lint
  domain: coding-general
  provenance: "2026-06-17, Blog project retrospective."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-general's own preamble."
```
