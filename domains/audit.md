# Audit record — kernel-seed layer

Provenance and per-kill audit detail for every kernel-seed domain — stack-agnostic
(`coding-general`, `orchestrator-routing`, `ratify-gate`, `planning`, `interviewing`,
`spawn-integrity`) and stack-specific (`coding-ts`, `coding-react`, `coding-nextjs`, `css`, `color`,
`surfaces-elevation`, `visual-hierarchy`, `motion`, `wizards-flows`, `ranking-evaluation`,
`lists-selection`, `validation-feedback`, `forms-inputs`, `recoverability`, `design-method`) alike,
now that `role-pack` no longer gates a separate pack layer — see the merge note below. Loaded only
at ratify/retrospective time — never in a spawn's working context. Keyed by principle `id`, each
noting its `domain`. See `kernel.md`, "Storage: working vs audit." (Kill logs live in the per-domain
working files so they are available in the working context.)

> **Web-frontend domain merge (2026-07-22).** The former web-frontend pack layer's domains and audit history were merged flat into this single kernel-seed layer once `role-pack` was retired as a project-config concept (see kernel.md, "Project corpora") — every stack-specific domain now states its own load condition directly against `language`/`framework`/`styling`/`has-ui`, rather than through a pack-name indirection. The provenance entries from that merged layer carry their own migration note below.

> **Migration note (2026-06-22).** These principles were re-homed from the old role corpora
> (`coder.md` pack overlay, `ui-designer.md`, `ux-designer.md`) into domain working files as part of
> the corpus redesign. The role→domain move is uniform and recorded here once rather than as a
> `history` stanza on every principle; only notable moves (cross-role re-homing, consolidations,
> the documentation-before-screenshots dedup) carry an explicit `history` entry below.

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
  history:
    - date: 2026-07-19
      type: extended
      reason: "slider-puzzle project, tag-identity-dependencies-check-before-handoff discussion. Operator pointed out that the rule as written already bounds the comment with a named upgrade condition, but nothing in the principle schedules an actual re-check of that condition — it can drift the same way an unbounded comment would if no one happens to reread that line. Added an explicit re-check anchored to the existing structural-examination-at-working-checkpoint pass rather than leaving the condition to be noticed by chance."

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
  history:
    - date: 2026-07-19
      type: clarified
      reason: "slider-puzzle project, tag-identity-dependencies-check-before-handoff discussion. The condition anchored to 'before creating the commit,' but the coder lens doesn't control whether or when a commit happens — the orchestrator does, per the ratify gate's step 9. Re-anchored to the coder's own terminal act, the handoff artifact, which every coder session actually has. The ceiling-comment-for-deliberate-shortcuts amendment made the same day pointed at this principle's checkpoint by name, so it inherited the same fix rather than needing a separate one."

- id: tag-identity-dependencies-check-before-handoff
  domain: coding-general
  kind: judgment
  provenance: "Promoted 2026-07-19 from the slider-puzzle project's coding-general domain. Discovered when a tile-slide CSS transition never animated: renderBoard() reset boardElement.innerHTML and rebuilt every tile element on each render, leaving no persistent DOM node for the transition to interpolate from — a bug invisible to end-state checks (correct final layout, correct CSS, correct before/after screenshots) because none of them can distinguish an animated arrival from an instant one. The principle went through several rounds with the operator before landing here: first scoped narrowly to CSS/DOM animation mechanics, then generalized to any render-time identity/reference dependency (memoization, reference-keyed caches, instance-bound subscriptions), then given an explicit forward-pass tag plus an anchored checkpoint (before the handoff artifact, not 'before commit,' which a coder may not own) after the operator noted that comments drift silently with no compiler check — same objection that produced the ceiling-comment-for-deliberate-shortcuts amendment above. Promoted directly on operator request rather than after multi-project pressure-testing; its condition names no slider-puzzle-specific stack or structure, so it was judged able to argue for itself."

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
  history:
    - date: 2026-07-22
      type: moved
      reason: "pokemon-game dry-run exercise, planner-decomposition session. Generalized beyond its UX/UI-specific condition and relocated to the new interviewing domain as frame-questions-for-cheap-answers — the same test (frame for a cheap answer, omit a baked-in opinion) applies to any question-framing moment (planner dialogue, any lens's questions-pending pause), not only the orchestrator routing a design question. Removed from orchestrator-routing's principles: the orchestrator now draws this judgment by composing interviewing (directly, or via the planner alias) rather than carrying a duplicate, narrower copy of its own."

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

- id: screenshot-recapture-is-orchestrator-mechanical
  domain: orchestrator-routing
  provenance: "2026-07-22, UI screenshot cache design (docs/superpowers/specs/2026-07-22-ui-screenshot-cache-design.md). A fresh-context review of the design found that grounding orchestrator-run recapture by analogy to `corpus.py` invocation alone was a weaker fit than presented — script invocation has zero interpretation, while navigating to the correct rendered state to capture involves some procedural judgment. This principle states the narrower claim directly and names the boundary against `stop-and-route` explicitly (visual judgment about the recaptured state routes to a role; mechanical recording of current state does not)."

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

# domain: interviewing (new domain, seeded 2026-07-22)
- id: ask-one-question-at-a-time
  domain: interviewing
  kind: judgment
  provenance: "2026-07-22, pokemon-game dry-run exercise. Decomposed from planner.md's 'Dialogue' step. Genuine-fork-tested against the operator's own observed default: batching multiple clarifying questions into one turn is a concrete, recurring model behavior, not a strawman."

- id: name-clear-direction-dont-manufacture-choice
  domain: interviewing
  kind: judgment
  provenance: "2026-07-22, pokemon-game dry-run exercise. Decomposed from planner.md's 'Dialogue' step. Directly evidenced within the same session: the orchestrator manufactured multi-option choices until the operator asked it to stop and proceed on recommendation instead."

- id: frame-questions-for-cheap-answers
  domain: interviewing
  kind: judgment
  provenance: "2026-07-22, pokemon-game dry-run exercise. Absorbs and generalizes orchestrator-routing's surface-design-questions-neutrally (see that principle's history entry, dated the same day) — widened from 'a UX or UI question routed to the operator' to any question-framing moment, since the condition named no genuinely UX/UI-specific mechanism."

# domain: planning
- id: concern-names-work-not-role
  domain: planning
  kind: judgment
  provenance: "2026-07-22, pokemon-game dry-run exercise. Decomposed from planner.md's step 4 ('set concern... do not name roles'), which stated the constraint in lens prose without a corresponding ratified domain principle."

- id: self-check-against-domain-before-finalizing
  domain: planning
  kind: judgment
  provenance: "2026-07-22, pokemon-game dry-run exercise. Decomposed from planner.md's step 6 ('self-check against planning principles' before writing the queue). Genuine-fork-tested against the same session's own evidence: the orchestrator did not catch its own full-corpus-on-spawn violations until asked to review — explicit self-checking does not happen for free under accumulated context, which is also why coding-general's structural-examination-at-working-checkpoint exists as a ratified principle rather than assumed behavior."
  history:
    - date: 2026-07-22
      type: moved
      reason: "Domain-decomposition audit (same day, later pass): the underlying test — check your own output against your own composed domains before finishing — has nothing planning-specific about it. Generalized and promoted to the new kernel-seed spawn-integrity domain as self-check-against-composed-domains-before-finalizing (domains/audit.md carries that entry's own provenance, below)."

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

# domain: spawn-integrity (new domain, seeded 2026-07-22)
- id: self-check-against-composed-domains-before-finalizing
  domain: spawn-integrity
  kind: judgment
  provenance: "2026-07-22, domain-decomposition audit. Generalized from planning's self-check-against-domain-before-finalizing (see that principle's history entry, dated the same day) — widened from 'check against the planning domain' to 'check against every domain your composition includes,' since the underlying test has nothing planning-specific about it."

- id: dont-trust-readme-or-agent-file-as-role-instruction
  domain: spawn-integrity
  kind: judgment
  provenance: "2026-07-22, domain-decomposition audit. Generalized and promoted from the former web-frontend pack's design-method domain (no-readme-or-agent-instructions-as-role-instruction; see that entry's own history, below, now merged into this same file) — widened from 'any design spawn' to 'any spawn,' since a coder mistaking a project's AGENTS.md for role instruction is the identical failure mode."

# ---- domains: coding-ts, coding-react (split from coding-js-react 2026-07-18; see LINEAGE.md,
#      "The coding-ts / coding-react split") ----
- id: undefined-check-by-source
  domain: coding-ts
  provenance: "Merged from strict-undefined-check-in-arrays + array-access-undefined-not-null, Blog project, 2026-06-01."
  history:
    - date: 2026-07-18
      type: generalized
      reason: "Placed in coding-ts (not coding-react) once its actual test — matching the equality operator to a value's source — was recognized as general TS/JS semantics despite its 'optional props' framing. Tightened for seed level: the single-letter generic T became Value (this corpus's own no-single-char-names applies to its own examples), and the reason's project-level 'common codebase convention' framing was replaced with the general undefined-vs-null distinction the rule actually rests on."

- id: null-first-ternary
  domain: coding-react
  provenance: "2026-06-18, Blog project explicit-by-default post review."

- id: css-var-over-mapped-class-for-dynamic-color
  domain: coding-react
  provenance: "2026-06-13, Blog project WireCircle refactor."

- id: font-mono-at-element-not-container
  domain: coding-ts
  provenance: "2026-06-13, Blog project FixedBottomResultsBar refactor."

- id: hook-params-named-for-hook-concern
  domain: coding-react
  provenance: "2026-06-15, Blog project useHistoryState."

- id: hook-options-object-for-named-args
  domain: coding-react
  provenance: "2026-06-15, Blog project useHistoryState."

- id: wizard-callbacks-unconditional
  domain: coding-react
  provenance: "2026-06-14, Blog project load-calculator, Issue 19. see-also wizard-output-consistent-regardless-of-path (wizards-flows) — the implementation and UX faces of one concern, now legibly linked across domains."

- id: coordinated-setters-signal-reducer
  domain: coding-react
  kind: judgment
  provenance: "2026-06-28, HiraganaQuiz refactor. useQuizQueue had 8 useState calls; submitAnswer fired 5 setters and the advance timer fired 6. These groups mapped cleanly to 'submit' and 'advance' action types. Recognizing the grouped setters as an unnamed state machine — not just a large hook — is the non-obvious judgment."
  history:
    - date: 2026-06-29
      type: moved
      reason: "Promoted from Blog project domain to web-frontend pack seed — condition makes no reference to Blog-specific structure; general React hook wisdom."

- id: same-state-same-name
  domain: coding-ts
  kind: judgment
  provenance: "2026-06-28, HiraganaQuiz refactor. TileState 'resting' vs SpellTile 'idle' — same visual concept, two names. Decision to rename before extracting rather than casting or adding a translation layer. Renaming made SpellTile['state'] a structurally valid subset of TileState, eliminating buildSpellTileClass."
  history:
    - date: 2026-06-29
      type: moved
      reason: "Promoted from Blog project domain to web-frontend pack seed — general TypeScript/React structural wisdom, no Blog-specific framing."
- id: extract-named-concern-into-custom-hook
  domain: coding-react
  provenance: "2026-07-04, reading kyleshevlin.com/use-encapsulation/. Identified gap between coordinated-setters-signal-reducer (threshold-based) and the article's broader claim: the extraction signal is a nameable concern, not a setter count. Judgment call: extraction overhead vs. readability gain."
- id: effect-only-derived-state-belongs-in-render
  domain: coding-react
  kind: judgment
  provenance: "2026-07-15, FAMOUS PlayerBarContent review (operator flagged a coder principle possibly too web-specific for an unrelated hook-encapsulation question; while fixing the hook extraction, a separate useEffect surfaced that only reset scrubberOpen on track-id change via a ref comparison — moved to render body). Operator asked whether the sibling knowledge-tier kill no-read-after-set-in-same-scope was wrongly killed given this miss; on inspection the two patterns are unrelated (that kill concerns reading state synchronously after its own setter, this concerns an effect used purely for derivable state with no external interaction) but the miss itself prompted an audit of FAMOUS and Blog for recurrence. FAMOUS had only the one instance; Blog's ResultBar.tsx useResultFlash showed the identical shape independently (throttled setFlashKey bump keyed off prop-derived label/delta, no external interaction). Two independent hits across two different project shapes (Expo/RN, Next.js) in one pass — satisfies the cross-project-shape bar for promotion straight to seed rather than starting provisional in one project's working file."

- id: hook-returns-own-handlers
  domain: coding-react
  provenance: "2026-07-04, reading kyleshevlin.com/use-encapsulation/. Bundled-handler pattern shown in useOnOff and useInput examples — no existing principle covered it. Judgment call: complete hook interface vs. consumer flexibility."
  history:
    - date: 2026-07-06
      type: merged
      reason: "Merged with extract-named-concern-into-custom-hook into custom-hook-owns-its-concern. Extraction and interface completeness are co-decisions."

- id: extract-named-concern-into-custom-hook
  domain: coding-react
  provenance: "2026-07-04, reading kyleshevlin.com/use-encapsulation/. Identified gap between coordinated-setters-signal-reducer (threshold-based) and the article's broader claim: the extraction signal is a nameable concern, not a setter count. Judgment call: extraction overhead vs. readability gain."
  history:
    - date: 2026-07-06
      type: merged
      reason: "Merged with hook-returns-own-handlers into custom-hook-owns-its-concern. See that entry."

- id: hook-callsite-legibility
  domain: coding-react
  kind: judgment
  provenance: "2026-07-06, retrospective consolidation. Merged from hook-params-named-for-hook-concern (2026-06-15, Blog useHistoryState) and hook-options-object-for-named-args (same session). Both addressed hook callsite legibility and always co-fired. Judgment: naming params for the hook's concern and wrapping ambiguous primitives in an options object are two expressions of the same rule."

- id: custom-hook-owns-its-concern
  domain: coding-react
  kind: judgment
  provenance: "2026-07-06, retrospective consolidation. Merged from extract-named-concern-into-custom-hook (2026-07-04, kyleshevlin.com) and hook-returns-own-handlers (same source). Judgment: extraction and handler-return are co-decisions — separating them invites partial application."

- id: nan-serializes-to-null-in-json
  domain: coding-ts
  kind: judgment
  provenance: "Promoted from project domains 2026-07-06. Surfaced in Blog (2026-06-20, load calculator NaN incident); ported to FAMOUS (2026-07-01, cross-project review — no FAMOUS incident yet, but condition is easy to hit unknowingly). Two-project exposure via cross-project review justifies seed promotion. Condition broadened to cover any JSON serialization boundary, not only localStorage."

- id: behavior-flags-in-refs
  domain: coding-react
  provenance: "2026-07-01, cross-project Blog→FAMOUS deep review. Surfaced from load calculator useAutosave (isMountRef, pendingRef) and hiragana useSpellQueue (errorInRoundRef). All are boolean flags that gate logic without affecting rendered output. Written to seed domain."
  history:
    - date: 2026-07-06
      type: generalized
      reason: "Retrospective: absorbed timer-handles-in-refs-not-state. Timer IDs are behavioral flags; the dep-cascade concern is now part of this principle's reason. Rule and condition extended to name timer handles explicitly."
    - date: 2026-07-18
      type: generalized
      reason: "Structural-kinship retrospective signal: absorbed stable-ref-for-document-listeners. Both were instances of the same ref-vs-state test — mirroring current state for an external listener is a specific case of 'does this value drive rendered output.' Rule and reason extended to name the document-listener case explicitly."

- id: stable-ref-for-document-listeners
  domain: coding-react
  provenance: "No provenance was ever recorded for this principle when it was originally ratified — a pre-existing gap found while executing the 2026-07-18 structural-kinship merge, backfilled here rather than left permanently orphaned. Its rule concerned mirroring current React state into a ref for document-level event handlers to avoid stale closures."
  killed: 2026-07-18
  history:
    - date: 2026-07-18
      type: merged
      reason: "Merged into behavior-flags-in-refs — see that entry's history."

- id: nested-conditional-signals-sub-component
  domain: coding-react
  kind: judgment
  provenance: "2026-07-04, FAMOUS Discover refactor — operator refactored the chained isHydrated × data.length ternary into a binary skeleton/content switch at the parent level, with DiscoveryList owning its own empty/populated states. Judgment call: whether to extend generic-defers-to-consumer or stand alone — standalone chosen because generic-defers-to-consumer requires a reusable-unit framing that wouldn't fire on specific components. Originally ratified into FAMOUS project domain 2026-07-04."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Promoted from FAMOUS project domain to web-frontend pack seed at retrospective. Condition makes no reference to FAMOUS-specific structure — universal React/JSX judgment."

- id: named-exports-over-default
  domain: coding-ts
  kind: knowledge
  provenance: "2026-07-06, FAMOUS Expo migration gate. Surfaced from reading pipeline (basarat/typescript-book). Originally ratified into FAMOUS project domain."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Promoted from FAMOUS project domain to web-frontend pack seed at retrospective. Universal JS/TS module pattern; no FAMOUS-specific condition."

- id: prefers-reduced-motion-requires-js-hook
  domain: coding-react
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (joshwcomeau.com/react/prefers-reduced-motion — source URL returned 403 at extraction time, content pulled from training-data knowledge of this well-known article). Ratified directly to seed as the implementation-mechanics half of the reduced-motion pair; see reduced-motion-instant-not-absent (motion domain) for the design-judgment half."
  see-also: reduced-motion-instant-not-absent

- id: discriminated-union-for-mutually-exclusive-props
  domain: coding-react
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (developerway.com/posts/advanced-typescript-for-react-developers-discriminated-unions — source URL returned 403, extracted from search-result summaries of this and closely related sources). Ratified directly to seed — genuine recurring TS/React prop-typing decision, applicable to any project on this pack with variant-prop components."
  see-also: unified-representation-no-type-leakage

# ---- domain: coding-nextjs (new domain, forked from coding-js-react at retrospective 2026-07-06) ----
- id: suspense-not-needed-for-sync-client-components
  domain: coding-nextjs
  kind: judgment
  provenance: "2026-07-05, FAMOUS discover misc polish session. DiscoverPage wrapped Discover in Suspense with no fallback; operator reported intermittent back-button misdirection. Removing Suspense was the fix. Judgment call: the Suspense was a no-op for loading UX but a live variable in Next.js App Router's router cache handling on back navigation. Originally ratified into FAMOUS coding-js-react project domain."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Moved from FAMOUS project coding-js-react to coding-nextjs seed domain at retrospective. Condition is Next.js App Router-specific; FAMOUS migrated to Expo Router. Principle travels with the framework, not the project."

- id: view-transition-scope-at-page-slot-not-layout
  domain: coding-nextjs
  kind: judgment
  provenance: "2026-07-05, FAMOUS view transitions technology research session. Coder evaluated CSS View Transitions API, Framer Motion AnimatePresence, React 19 experimental ViewTransition. Judgment call: the risk of misapplying route-keying at the layout level (which would unmount a persistent audio player) is non-obvious. Originally ratified into FAMOUS coding-js-react project domain."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Moved from FAMOUS project coding-js-react to coding-nextjs seed domain at retrospective. Condition is Next.js App Router-specific; FAMOUS migrated to Expo Router."

# ---- domain: css ----
- id: tailwind-extract-component-before-apply
  domain: css
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (tailwindcss.com/docs/reusing-styles). Ratified directly to seed — real recurring web-frontend decision (extract component vs @apply); FAMOUS itself has zero @apply usage (NativeWind/RN is component-first by default) but Blog or other DOM-CSS projects on this pack face the tradeoff directly."

- id: tailwind-loop-duplication-is-not-a-problem
  domain: css
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (tailwindcss.com/docs/reusing-styles), companion to tailwind-extract-component-before-apply from the same source. Ratified directly to seed for the same reason."

- id: grid-for-layout-flexbox-for-flow
  domain: css
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (blog.logrocket.com/css-flexbox-vs-css-grid). Ratified directly to seed with an explicit condition carve-out for React Native (no CSS Grid support natively) — applies to any DOM-CSS project on this pack, not to FAMOUS's native surfaces."
  killed: 2026-07-22

- id: mobile-fixed-bar-bottom-gap
  domain: css
  provenance: "2026-06-03, Blog project Box Selector mobile bottom bar."

- id: imports-before-tailwind-directives
  domain: css
  provenance: "2026-06-12, Blog project globals.css restructure."
  killed: 2026-07-22

- id: tokenize-only-recurring-magic-values
  domain: css
  provenance: "2026-06-12, Blog project globals.css restructure."

- id: table-row-color-override
  domain: css
  provenance: "2026-06-15, Blog project ampacity table temperature header text color."

# ---- domain: color ----
- id: semantic-tokens-required-for-theme-switching
  domain: color
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (smashingmagazine.com/2024/05/naming-best-practices). Ratified directly to seed — FAMOUS has one fixed dark aesthetic with no theme-switching need, but the two-tier (primitive/semantic) architecture is standard practice any project on this pack would need if it ever added light/dark or brand-variant theming."
  see-also: semantic-token-names-by-role-not-value
  killed: 2026-07-22

- id: semantic-token-names-by-role-not-value
  domain: color
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (smashingmagazine.com/2024/05/naming-best-practices), companion to semantic-tokens-required-for-theme-switching from the same source. Ratified directly to seed as structural confirmation — FAMOUS's own token names (--color-bg-canvas, --color-accent-fame, --color-bg-overlay) already follow role-based naming, not value-based."
  see-also: semantic-tokens-required-for-theme-switching
  killed: 2026-07-22

- id: color-palette-inspiration
  domain: color
  provenance: "2026-06-02, operator-provided. Clarified 2026-06-13."

- id: palette-chromatic-depth
  domain: color
  provenance: "2026-06-03, taste training session."

# ---- domain: surfaces-elevation ----
- id: disclosure-panel-vs-modal
  domain: surfaces-elevation
  provenance: "2026-06-14, load calculator history panel design spec."

- id: dark-floating-surface-fill
  domain: surfaces-elevation
  provenance: "2026-06-19, nav background depth session."

- id: scroll-fade-gradient-surface-match
  domain: surfaces-elevation
  provenance: "2026-06-19, nav background depth session."

# ---- domain: visual-hierarchy ----
- id: redundant-badge-sublabel
  domain: visual-hierarchy
  provenance: "2026-06-02, Box Selector visual spec."

- id: control-grouping-encodes-unity
  domain: visual-hierarchy
  provenance: "2026-06-03, taste training session (originally as capsule-encodes-same-value)."
  history:
    - date: 2026-06-20
      type: generalized
      reason: "Original rule prescribed capsule as the specific pattern — 'join into a capsule when segments share a value.' This directed the designer to a single implementation rather than stating the underlying principle. The insight is that any form of visual grouping (capsule, joined buttons, bordered cluster) encodes semantic unity; the specific form is a design decision the rule should inform, not resolve. Rule rewritten to state the general principle with capsule as one named example. Id renamed from capsule-encodes-same-value to reflect the broader concept."

- id: hierarchy-through-scarcity
  domain: visual-hierarchy
  provenance: "2026-06-04, retrospective consolidation."
  history:
    - date: 2026-06-20
      type: absorbed-examples
      reason: "Killed one-highlight-per-result-set and accent-color-for-distinction-not-data as redundant instances of this principle. Concrete examples those principles captured: (1) apply highlight to exactly one card per results panel — when two outputs are co-primary, merge into one highlighted card with an internal divider rather than two competing highlights; (2) accent color belongs only on the distinguished row, all other data values in secondary text color. Both earned in Box Selector results panel."

- id: responsive-text-by-viewport-distance
  domain: visual-hierarchy
  provenance: "2026-06-09, Box Selector desktop text legibility audit."

# ---- domain: motion ----
- id: motion-as-accent
  domain: motion
  provenance: "2026-06-03, taste training session."

- id: scrollytelling-must-always-react
  domain: motion
  provenance: "2026-06-13, homepage journey audit."

- id: reduced-motion-instant-not-absent
  domain: motion
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (joshwcomeau.com/react/prefers-reduced-motion — source URL returned 403 at extraction time, content pulled from training-data knowledge of this well-known article). Ratified directly to seed — no reduced-motion handling exists anywhere in FAMOUS yet, but the instant-vs-absent distinction is real UX judgment applicable to any project on this pack with JS-driven animation."
  see-also: motion-as-accent, prefers-reduced-motion-requires-js-hook

# ---- domain: recoverability ----
- id: recovery-path-replaces-confirmation
  domain: recoverability
  provenance: "2026-06-14, load-calculator audit."
  history:
    - date: 2026-06-20
      type: consolidated
      reason: "Absorbed recoverable-action-surfaces-its-path (originated ui-designer seed 2026-06-14, moved to ux-designer seed 2026-06-20). Both principles shared identical conditions and formed one complete thought: skip confirmation when recovery exists, and surface that recovery path. Separated, a designer could apply one without the other and get incomplete guidance. Merged rule absorbs both: recovery path is the gate AND must be made visible. Merged reason combines both justifications."
    - date: 2026-06-22
      type: moved
      reason: "Re-homed to the recoverability domain, now declared by BOTH ui-designer and ux-designer. The redesign makes structural what the 2026-06-20 consolidation did by hand: this judgment is one concern spanning flow (UX) and visible affordance (UI), and a domain both lenses declare is its natural home."
    - date: 2026-07-18
      type: generalized
      reason: "Absorbed destructive-global-actions-require-confirmation's ~30-second severity threshold — same recovery-or-confirmation test, one just named the bar for when the gate is mandatory."

- id: destructive-global-actions-require-confirmation
  domain: recoverability
  provenance: "2026-06-14, load-calculator UX audit."
  killed: 2026-07-18

- id: destructive-inline-confirmation
  domain: recoverability
  provenance: "2026-06-02 (originated in ui-designer seed corpus)."
  history:
    - date: 2026-06-20
      type: moved
      reason: "Principle describes interaction behavior (inline row transformation, confirm/cancel affordance), not visual design. Moved from UI designer seed to UX designer seed."
    - date: 2026-06-22
      type: moved
      reason: "Re-homed to the recoverability domain (declared by both designers). The 2026-06-20 UI→UX move was the container problem in miniature — the principle kept getting reassigned because no single role owned it. The domain ends the ping-pong."

- id: optimistic-ui-for-high-confidence-mutations
  domain: coding-react
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (dev.to/a1guy — React 19 useOptimistic deep dive; source URL returned 403, extracted from training-data knowledge of the API and standard optimistic-UI patterns). Ratified directly to seed — FAMOUS has zero server mutations currently (grepped, no fetch/API calls in the codebase), but the risk-weighing judgment (safe-to-assume vs. plausible-failure) is general and applicable to any project on this pack with a backend."
  see-also: recovery-path-replaces-confirmation, optimistic-rollback-requires-explicit-error
  history:
    - date: 2026-07-22
      type: moved
      reason: "Domain-decomposition audit: this is React-hook implementation guidance (useOptimistic, mutation-state architecture), not UX/UI design judgment — neither ux-design nor ui-design's alias notes claim implementation as their concern. Moved from recoverability (loaded by both design aliases) to coding-react (loaded by the coder), which actually applies it."

- id: optimistic-rollback-requires-explicit-error
  domain: coding-react
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (dev.to/a1guy), companion to optimistic-ui-for-high-confidence-mutations from the same source. Ratified directly to seed for the same reason."
  see-also: recovery-path-replaces-confirmation, optimistic-ui-for-high-confidence-mutations
  history:
    - date: 2026-07-22
      type: moved
      reason: "Same domain-decomposition finding as optimistic-ui-for-high-confidence-mutations — moved from recoverability to coding-react alongside it."

# ---- domain: validation-feedback ----
- id: warning-colocated-with-resolution
  domain: validation-feedback
  provenance: "2026-06-02, Box Selector visual spec."

- id: warning-banner-must-locate-its-fix
  domain: validation-feedback
  provenance: "2026-06-02, Box Selector UX review."

- id: filter-side-effects-are-surfaced
  domain: validation-feedback
  provenance: "2026-06-02, Box Selector UX review."

# ---- domain: forms-inputs ----
- id: numeric-inputs-start-empty-not-zero
  domain: forms-inputs
  provenance: "2026-06-14, load-calculator UX audit."

- id: zero-count-orphan-rows
  domain: forms-inputs
  provenance: "2026-06-02, Box Selector UX review."

- id: unified-field-over-derived-dual-fields
  domain: forms-inputs
  provenance: "2026-06-14, load-calculator appliance row overhaul."

- id: persistent-controls-not-conditional
  domain: forms-inputs
  provenance: "2026-06-14, load-calculator appliance row overhaul."

- id: forms-reveal-conditional-fields
  domain: forms-inputs
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (nngroup.com/articles/progressive-disclosure). Ratified directly to seed — no current form in FAMOUS has this shape, but the guidance is applicable to any project on this pack with conditional-field forms."
  see-also: progressive-disclosure-for-primary-advanced-split, persistent-controls-not-conditional

- id: validate-on-blur-then-on-change
  domain: forms-inputs
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (smashingmagazine.com/2022/09/inline-validation-web-forms-ux — source URL returned 403, extracted from search-result summaries and corroborating UX research). Ratified directly to seed — no field-level validation surface exists in FAMOUS yet, but the blur-then-change sequencing is standard, non-obvious enough to be worth encoding for any project on this pack with inline form validation."
  see-also: warning-colocated-with-resolution

# ---- domain: lists-selection ----
- id: indicator-weight-matches-job
  domain: lists-selection
  provenance: "2026-06-16, load calculator history redesign."

- id: active-row-is-inert
  domain: lists-selection
  provenance: "2026-06-16, load calculator history redesign."
  history:
    - date: 2026-07-10
      type: killed
      reason: "Superseded by active-row-is-inert-exact-route-only, promoted directly from the Meridian project (operator-approved cross-project edit, not a retrospective promotion) — see that entry below for the discovered defect."

- id: active-row-is-inert-exact-route-only
  domain: lists-selection
  kind: judgment
  provenance: "Meridian project, coder, 2026-07-10, top-bar rewrite pass. A Sidebar nav item's active state (`pathname.startsWith('/clients')`) spanned both the Clients list screen and every client-detail sub-page. Applying active-row-is-inert's blanket 'no hover, no click' treatment made a real, meaningful click (returning to the list from a detail page) silently do nothing, breaking tests/replay/runCase.ts's persistent-chrome recovery path (30 tests failed, confirmed via git stash bisection against the untouched baseline). Operator reviewed the coder's fix (keep it a real Link, styled to look inert) and pushed back: the styling itself was wrong too, not just an implementation detail — a section-spanning active item should stay visually and functionally interactive, since a click there does something real. Refined and edited directly into the shared pack seed at the operator's explicit request, rather than deferred to a project-level override or a future retrospective promotion."

- id: section-level-explanation-not-row-level
  domain: lists-selection
  provenance: "2026-06-14, load-calculator appliance row overhaul."

# ---- domain: wizards-flows ----
- id: origin-step-marked-visited-on-navigation
  domain: wizards-flows
  provenance: "2026-06-14, load-calculator UX audit."

- id: wizard-output-consistent-regardless-of-path
  domain: wizards-flows
  provenance: "2026-06-14, load-calculator UX audit. see-also wizard-callbacks-unconditional (coding-react)."

- id: optional-step-must-be-labeled-optional
  domain: wizards-flows
  provenance: "2026-06-14, load-calculator UX audit."

# ---- domain: ranking-evaluation ----
- id: triage-and-ranking-are-independent-signals
  domain: ranking-evaluation
  provenance: "Merged from intake-and-ranking-are-separate-activities + elo-as-independent-ranking-signal, 2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a comparative ranking/evaluation tool (Taste Trainer). Condition is narrow — tools that mix quick triage with deliberate ranking. Plausible general principle but untested against a second project with a ranking or evaluation feature. Do not promote until confirmed in a second context."

- id: category-scope-is-visible-on-ranked-items
  domain: ranking-evaluation
  provenance: "2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a per-category ranking tool (Box Selector). Condition presupposes category-scoped rankings — a pattern that may not recur in other web-frontend projects. Do not promote until confirmed in a second context."

- id: choice-prompt-anchors-on-usefulness-not-preference
  domain: ranking-evaluation
  provenance: "2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a reference-building tool (Taste Trainer). Condition is narrow — tools whose output is meant to inform future decisions, not record taste. Do not promote until confirmed in a second context."

- id: callout-label-describes-property-not-judgment
  domain: ranking-evaluation
  provenance: "2026-06-02, Box Selector UX review."

- id: out-of-order-callout-requires-sort-explanation
  domain: ranking-evaluation
  provenance: "2026-06-02, Box Selector UX review."

# ---- domain: design-method ----
- id: clarity-over-polish
  domain: design-method
  provenance: "2026-06-22, extracted from UX designer 'Project context' instruction."

- id: document-visual-sub-systems
  domain: design-method
  provenance: "2026-06-12, full site visual audit."

- id: documentation-before-screenshots
  domain: design-method
  provenance: "2026-06-22, extracted from the designer 'What you do' screenshots bullet."
  history:
    - date: 2026-06-22
      type: consolidated
      reason: "This principle existed byte-for-byte identical in BOTH the ui-designer and ux-designer seed corpora — the clearest instance of the container problem the redesign targets: shared judgment stored twice because the role was the container. Merged into a single entry in the design-method domain, which both designer lenses declare."
    - date: 2026-07-22
      type: reworded
      reason: "UI screenshot cache design (docs/superpowers/specs/2026-07-22-ui-screenshot-cache-design.md) introduced a persistent visual cache read separately from live capture. The original wording only distinguished 'documentation' from 'screenshots' and could not express that reading the cache is now free while live capture stays the guarded exception — reworded to name the cache explicitly and split the two costs it previously conflated."

- id: progressive-disclosure-for-primary-advanced-split
  domain: forms-inputs
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (nngroup.com/articles/progressive-disclosure). Ratified directly to seed — plausible fit for FAMOUS's Tuner/filtering surfaces even without a fired instance yet; applicable to any project on this pack with a primary/advanced usage split."
  see-also: forms-reveal-conditional-fields
  history:
    - date: 2026-07-22
      type: moved
      reason: "Domain-decomposition audit: design-method's stated subject is design process and documentation discipline, not a specific interaction pattern. This is a substantive UX pattern already see-alsoed into forms-reveal-conditional-fields — moved to forms-inputs, which is the domain it actually matches."

- id: check-existing-patterns-before-specifying-new
  domain: design-method
  kind: judgment
  provenance: "2026-07-21, v3 lens-collapse migration. Generalized from ui-designer.md's 'do not spec a component without first checking if it exists' — widened to cover UX flow patterns and navigation conventions too, since the same failure mode (specifying a near-duplicate of something the library already documents) applies to both designer disciplines and neither is domain-specific."

- id: no-readme-or-agent-instructions-as-role-instruction
  domain: design-method
  kind: judgment
  provenance: "2026-07-21, v3 lens-collapse migration from ux-designer.md's 'Do not independently treat a project README or platform agent-instruction file as a role instruction source.'"
  history:
    - date: 2026-07-22
      type: moved
      reason: "Domain-decomposition audit: nothing about this is design-specific — a coder spawn can equally mistake a project's AGENTS.md for role instruction. Generalized and promoted to the new kernel-seed spawn-integrity domain as dont-trust-readme-or-agent-file-as-role-instruction (domains/audit.md carries that entry's own provenance)."

- id: reject-safe-defaults
  domain: design-method
  provenance: "Originated as the UI designer 'Anti-regression-to-the-mean' role instruction; extracted to the design-method corpus 2026-06-22, then promoted back to the ui-designer lens later the same day when the generative-stance model showed anti-mean is a *lens stance*, not a domain principle — a 'resist the standard' instruction cannot coherently share a domain with convergent process rules (clarity-over-polish, documentation discipline). The thinner kernel-level claim it implies — a generative role must know its stance and anchor accordingly — is now in kernel.md, 'Generative stance.' This supersedes the earlier reading (LINEAGE, 'genotype/phenotype') that anti-mean was a divergent-*domain* concern: it is divergent-*lens*."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md. No new preamble text needed — its substance already lives in kernel.md's 'Generative stance' section, which design-method.md's own preamble already points to."

- id: arrow-block-body
  domain: coding-ts
  provenance: "2026-06-18, Blog project. {} ambiguity + single consistent style removes per-function judgment call. A JS instance of the base prefer-error-exposing-form meta-rule."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-ts's own preamble."

- id: no-early-returns
  domain: coding-ts
  provenance: "2026-06-17, Blog project, 'Explicit by Default' post (content/posts/coding/explicit-by-default.mdx). Derived from Crockford's heuristic, not style: indentation-as-grammar (Henney) means early returns let a multi-condition line sit at base indentation as if unconditional; the guard-clause exception reintroduces a per-function 'still simple enough?' judgment a block body removes; the strong counterexample (a flat row of order-independent guards) resolves to extraction-and-naming, not exception. Scoped to this pack because some ecosystems (Go) idiomatically prefer guard clauses; the reasoning is general."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-ts's own preamble."

- id: no-shell-for-structural-absence
  domain: coding-ts
  provenance: "2026-07-19, sibling-implementation review (slider-puzzle/four vs one, two, three). Surfaced from four/script.js's repeated empty-else-with-restating-comment pattern (getAdjacentPositions, isBoardSolved, ensureTileElements, stopTimer, setCaption, handleTileClick — six instances). Weighed against no-early-returns: that principle governs branches where both sides do real work; this one covers the narrower case of a branch with no true opposite side, which the guard-clause reasoning was never meant to force into a populated shell. Held as a see-also peer, not a caveat rewrite of the existing bullet."

# domain: principle-judgment (new domain, seeded 2026-07-22)
- id: reaudit-ratified-principles-against-genuine-fork-test
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-22, domain-and-principle audit session. Generalized from the session's own method: css.md's grid-for-layout-flexbox-for-flow and color.md's semantic-token-names-by-role-not-value were both tagged kind: knowledge in their own audit provenance at ratification time yet were still ratified into principles: — direct evidence that gate-time discipline alone is not sufficient and a periodic re-audit catches what it misses."

- id: reading-pipeline-provenance-flags-knowledge-risk
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-22, domain-and-principle audit session. All four knowledge-kills that session (css.md's two, color.md's two) originated from reading-pipeline provenance rather than an earned project incident — named directly as a risk correlation rather than left to be re-discovered on each future audit."

- id: check-principle-against-consuming-lens-not-just-domain-topic
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-22, domain-and-principle audit session. Generalized from three misplaced-principle findings that session (optimistic-ui-for-high-confidence-mutations + its pair, moved recoverability→coding-react; progressive-disclosure-for-primary-advanced-split, moved design-method→forms-inputs) — none of which the existing domain-tension retrospective signal could have caught, since none contradicted anything else in their birth domain."

- id: lead-with-the-nonobvious-half-when-refining
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-22, domain-and-principle audit session. Generalized from the same session's refinement of visual-hierarchy.md's hierarchy-through-scarcity, reworded to foreground its earned insight (subordinate without degrading legibility) instead of the design-101 framing (one dominant element) it originally led with."

# reading-pipeline candidates, processed against the new principle-judgment domain (2026-07-22)
- id: immutable-by-default
  domain: coding-general
  kind: knowledge
  provenance: "2026-07-20, reading pipeline (kevlinhenney.medium.com/restrict-mutability-of-state). Killed on first review rather than ratified — see coding-general.md's killed log for the reasoning."
  killed: 2026-07-22

- id: use-transition-vs-deferred-value
  domain: coding-react
  kind: judgment
  provenance: "2026-07-20, reading pipeline (developerway.com/posts/use-transition). Ratified directly to seed — the access-level test (setter ownership vs. value-only access) is a genuine decision heuristic for a commonly-conflated hook pair, not a restatement of React's own docs."

- id: container-queries-for-component-scope
  domain: css
  kind: judgment
  provenance: "2026-07-20, reading pipeline (blog.logrocket.com/choose-between-media-container-queries). Ratified directly to seed — container queries are recent enough (broad support ~2023) to carry real judgment risk rather than being settled textbook knowledge; the component-width-vs-viewport-width distinction is architectural, not syntax."

- id: server-components-for-initial-data
  domain: coding-nextjs
  kind: judgment
  provenance: "2026-07-20, reading pipeline (vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them). Ratified directly to seed — names a real, plausible wrong default (client-side fetching out of pre-RSC habit), framed as an observed mistake rather than pure API reference."

- id: revalidate-tag-over-path
  domain: coding-nextjs
  kind: judgment
  provenance: "2026-07-20, reading pipeline (vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them). Ratified directly to seed — companion finding from the same source; a genuine precision-vs-simplicity tradeoff (revalidateTag vs. revalidatePath), not a lookup fact."

- id: server-actions-for-mutations-not-queries
  domain: coding-nextjs
  kind: judgment
  provenance: "2026-07-20, reading pipeline (vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them). Ratified directly to seed — companion finding from the same source; guards against the plausible default of reaching for Server Actions as a general-purpose endpoint since they're the newer API."

# domain: dependency-management (new domain + lens, seeded 2026-07-22)
- id: adopt-forced-migration-early-on-disposable-branch
  domain: dependency-management
  kind: judgment
  provenance: "2026-07-22, reading pipeline (docs.expo.dev/guides/new-architecture), reworded from Expo-specific to general form when moved out of the then-uncreated coding-expo domain. Originally weighed for a kill-as-knowledge ('fairly standard') but held as judgment on review: the operator's own framing was that this is standard-but-under-practiced discipline (deferring an optional migration to its deadline is a real, recurring failure mode despite being agreed-upon in the abstract), which is exactly what the genuine-fork test is for — distinct from a lookup fact. Reassigned from coding-general to a new dependency-management domain + matching lens: this judgment applies to tasks actually about upgrading/migrating, not to every convergent coding spawn regardless of task shape (kernel.md, 'Recognizing that a task needs a different lens')."

- id: audit-transitive-dependencies-after-major-upgrade
  domain: dependency-management
  kind: judgment
  provenance: "2026-07-22, reading pipeline (buildmvpfast.com/blog/expo-sdk-56-inline-native-modules-router-fork-new-features-2026), reworded from Expo-specific to general form. Same reassignment reasoning as adopt-forced-migration-early-on-disposable-branch — held as judgment, moved to the new dependency-management domain rather than coding-general."

# domain: coding-expo (new domain, seeded 2026-07-22)
- id: expo-router-typed-routes-for-link-safety
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (docs.expo.dev/router/introduction/). Ratified directly to seed — names the specific compile-time-vs-runtime gap Typed Routes closes, not a restatement of the feature's existence."

- id: expo-router-default-react-navigation-for-low-level-native-control
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (dev.to/bhupeshchandrajoshi/expo-router-vs-react-navigation-which-one-should-you-use-in-2026-3khj). Ratified directly to seed — a genuine library-choice tradeoff with stated conditions on both sides, not a changelog restatement."

- id: interop-layer-does-not-cover-native-code-dependencies
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (docs.expo.dev/guides/new-architecture/). Ratified at lower confidence than the domain's other candidates — the operator did not object on review, but the finding is closer to a direct restatement of Expo's own documentation than the domain's more clearly earned judgment calls; kept because it still names a specific, plausible wrong assumption (treating the interop layer as a blanket guarantee) rather than pure lookup fact."

- id: expo-router-no-direct-react-navigation-imports
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (dev.to/manthan_kasle/expo-sdk-56-is-out-and-a-few-things-finally-clicked-into-place-478h). Ratified directly to seed — explains why a previously-working import pattern silently breaks post-SDK-56, a real judgment about dependency-architecture change rather than a release-notes restatement."

- id: expo-filesystem-migrate-once-feature-gaps-close
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (dev.to/manthan_kasle/expo-sdk-56-is-out-and-a-few-things-finally-clicked-into-place-478h). Ratified directly to seed — names the specific closed feature gaps rather than a generic 'upgrade when you can' statement. see-also added to dependency-management's adopt-forced-migration-early-on-disposable-branch: both test re-checking a deferred/provisional decision once its blocking condition changes, at different specificity levels (this one is Expo-FileSystem-specific; that one is the general adopt-early-on-a-disposable-branch judgment)."

- id: ota-update-scope-excludes-native-changes
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (farooxium.dev/blog/react-native-expo-2026-guide). Ratified directly to seed — a specific, non-obvious release-planning constraint (the OTA/native-change boundary) distinct from feature-description content also covered in the same source."

- id: expo-native-dirs-generated-not-hand-edited
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (deepwiki.com/expo/expo/9-build-and-deployment). Ratified directly to seed — a structural design claim about the CNG model's treatment of native directories as ephemeral generated output, the same failure shape coding-general's scripts-over-hand-editing-structured-data already names for generated artifacts generally, applied to the Expo-specific case."

- id: expo-inline-native-modules-before-ejecting
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (buildmvpfast.com/blog/expo-sdk-56-inline-native-modules-router-fork-new-features-2026). Ratified directly to seed — names how SDK 56's inline native modules change the actual build-vs-workaround decision for capabilities not previously worth the ceremony of ejecting or scaffolding a standalone native module package."

- id: expo-sequential-sdk-upgrade-across-router-fork
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (buildmvpfast.com/blog/expo-sdk-56-inline-native-modules-router-fork-new-features-2026). Ratified directly to seed — a distinct version-skip risk from the same SDK-56 router fork, separate from the import-rewrite mechanics already captured in expo-router-no-direct-react-navigation-imports."

- id: expo-sdk56-fetch-default-swap-breaks-oauth
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-22, reading pipeline (buildmvpfast.com/blog/expo-sdk-56-inline-native-modules-router-fork-new-features-2026). Ratified directly to seed — a global-fetch swap invisible in application-code diffs, with concrete named breakages (an AT Protocol OAuth client, a crash-reporting SDK) rather than a hypothetical risk."
```
