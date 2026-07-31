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
      reason: "Renamed from color-utility-over-guesswork and widened from color specifically to any deterministic, precision-sensitive, or repeatedly-recurring computation. Operator noticed this was the only coder-facing principle that ever told the coder to recognize and propose a deterministic shortcut candidate — every other domain's equivalent work (date math, geometric layout, hashing) had no trigger at all, since orchestrator-routing's surface-deterministic-shortcut-candidates-liberally is the orchestrator's counterpart and the coder never loads that domain. Color kept as the canonical named instance, including its React Native-specific carve-out."

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

- id: minimize-comments-prefer-self-documenting-code
  domain: coding-general
  kind: judgment
  provenance: "2026-07-15, FAMOUS full-player redesign session. Operator flagged a pattern of liberal inline commenting (layout math, gesture-conflict resolution, UI/UX design rationale) after several of those comments had already gone stale mid-session — a 'shared across three variants' comment surviving two variant deletions, a symmetry comment whose claimed math stopped matching the code, an edge-hint comment describing removed functionality."
  history:
    - date: 2026-07-23
      type: generalized
      reason: "Promoted from FAMOUS's project-level coding-general domain to seed. `spawn-integrity`'s checkpoint-on-context-pressure-tell had referenced 'this project's comment-discipline conventions' as a seed-level given since it was authored, but the underlying rule was never actually promoted alongside it — a dangling reference in the seed layer, caught by an operator noticing verbose comments in a downstream project (motors-and-controls) that had no such rule anywhere in its composed domains. Condition genericized (dropped 'in this project'); rule and reason otherwise unchanged from the FAMOUS original."

- id: derivable-arithmetic-is-not-a-hidden-constraint
  domain: coding-general
  kind: judgment
  provenance: "2026-07-26, motors-and-controls mobile-ux workstream. Commented `minZoom={0.4}` with the ratio to the library's 0.5 default ('~25% more canvas'). Operator's first challenge correctly identified a separate narrative sentence (naming the bug report) as reasoning-leak; the ratio sentence survived that pass. Operator's second challenge caught that the surviving sentence was itself just derivable arithmetic, not new information — self-review had checked for reasoning-leak but not against minimize-comments-prefer-self-documenting-code's own bar."

- id: co-derive-coupled-values-in-one-place
  domain: coding-general
  kind: judgment
  provenance: "2026-07-26, FAMOUS PlayerBarContent.tsx review. A `playbackPhase()`/`PHASE_LABELS` split (state → phase enum → lookup table) was simplified to one function returning both a status label and an action label together per branch, then the underlying feature was cut entirely. Operator generalized the surviving code-organization lesson from the specific status/action-label shape into a standalone principle, and asked to keep its reasoning free of any comparison to single-callsite-helper-scoped so the new principle doesn't read as arguing against its counterpart — the two are disambiguated by their condition fields alone, linked only via see-also."

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

- id: prefer-independent-evaluation
  domain: orchestrator-routing
  provenance: "2026-07-17, retrospective on review-composition cost. A standing reviewer composition was cut the same day for low uptake relative to its cost — this principle captures the replacement approach: an independent coder instance scoped to the review gets the same fresh-context benefit without a rarely-invoked dedicated composition."
  killed: 2026-07-27

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
    - date: 2026-07-27
      type: trimmed
      reason: "Session-mining background-agent audit (FAMOUS project) flagged this as a mixed principle under principle-judgment.md's mined-workflow-stays-a-workflow test: its rule was a three-stage ordered workflow (compose domains, flag in-flight, ask at the seam) rather than a single resolved tradeoff. The domain-composing step was confirmed a near-verbatim duplicate of SKILL.md's own 'For inline spawn work' instructions — not unmined process needing a praxis phase, just redundant restatement — so it was dropped rather than routed anywhere. The judgment kernel (inline work gets the same corpus discipline as a formal spawn; capture principle candidates at the natural seam, not deferred to session-end) was kept, reworded to lead with it directly instead of the procedural framing."

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
  killed: 2026-07-27

- id: no-cost-driven-domain-omission
  domain: orchestrator-routing
  kind: judgment
  provenance: "2026-07-22, operator conversation on lens/domain composition design. Discussion of whether lenses should be the mandatory composition unit (to guard against relevant domains going unloaded) surfaced a distinct, already-observed failure: the orchestrator thinning a composition to save tokens rather than never having known a domain was relevant in the first place. Paired with spawn-integrity's checkpoint-on-context-pressure-tell, added the same session, as the two sides (routing-time vs. spawn-side) of the same pressure."

- id: spawn-only-when-judgment-remains
  domain: orchestrator-routing
  kind: judgment
  provenance: "2026-07-26, Blog UI-library-sync task. The task brief for a ui-design-composed spawn already specified the exact before/after text for every edit — no design decision remained; the spawn's job had degraded to text transcription, and the isolation overhead (composed prompt, spawn execution, handoff review) cost more than making the edit directly would have."

- id: concern-class-diversity-triggers-decomposition
  domain: orchestrator-routing
  kind: judgment
  provenance: "Operator-authored, 2026-07-30, based on observed behavior in motors-and-controls' sim-09 task (2.5-3x the tool calls/tokens of sibling tasks, bundling engine-design judgment, catalog/UI plumbing, and lab-content re-derivation into one task), root-caused and refined through direct dialogue rather than a spawned proposal."
  history:
    - date: 2026-07-26
      type: moved
      reason: "Ratified into Blog's project-layer orchestrator-routing domain first, then promoted to this kernel-seed layer the same day — operator confirmed the pattern had recurred across projects (Blog, FAMOUS, Meridian) and was part of the original motivation for building corpora/praxis at all: superpowers' plan-then-execute skills were solving the same ambiguity-resolution problem twice, once in the plan and again when agents re-litigated it during execution."

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

- id: narrated-computation-is-sufficient-utility-evidence
  domain: ratify-gate
  provenance: "2026-07-25, backlog-triage/praxis-design discussion. Generalized from the color-utility precedent (a coder guessing warmer/cooler colors by narrated trial and error, resolved by building a deterministic color utility instead) once the operator named the underlying tell directly: narrated step-by-step simulation of an exact procedure is itself sufficient single-instance evidence, distinguishable from the fuzzier candidates surface-deterministic-shortcut-candidates-liberally's repeated-evidence requirement is actually meant for."

# domain: interviewing (new domain, seeded 2026-07-22)
# scope note: widened 2026-07-22 from "any convergent composition" to composition-agnostic once
# ui-design's own clarifying-dialogue moments (e.g. narrowing to two aesthetic-direction questions
# during bootstrap) showed the convergent-only restriction was never load-bearing — moved out of the
# working file's own prose 2026-07-25 (composition names in a domain loaded by every composition put
# every other composition's name in whichever spawn is currently reading it, for no functional benefit).
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

- id: checkpoint-on-context-pressure-tell
  domain: spawn-integrity
  kind: judgment
  provenance: "2026-07-22, operator conversation on lens/domain composition design. Operator reported repeatedly observing a concrete tell in practice — dragged-out reasoning and task logic leaking into code comments — under large composed contexts, and framed it as a symptom worth self-monitoring rather than a model competence failure."

- id: read-config-before-composing
  domain: spawn-integrity
  kind: knowledge
  provenance: "2026-07-22, lens retirement. Migrated from domains/lenses.md's per-lens notes field (near-identical text repeated in coder, dependency-management, ux-design, and ui-design's notes) to a single universal home once lenses were retired as a schema layer — see LINEAGE.md."

- id: library-is-narrative-not-corpus-shape
  domain: spawn-integrity
  kind: knowledge
  provenance: "2026-07-22, lens retirement. Migrated from ux-design's and ui-design's near-identical notes text in domains/lenses.md, generalized to any spawn touching either library file rather than only the two design compositions — see LINEAGE.md."

- id: periodic-scope-and-integrity-checkpoint
  domain: spawn-integrity
  kind: judgment
  provenance: "Operator-authored, 2026-07-30, based on observed behavior in motors-and-controls (sim-09's scope bundling went unnoticed mid-task despite no context-pressure tell), root-caused and refined through direct dialogue rather than a spawned proposal."

- id: proposal-self-cleanup-before-including
  domain: spawn-integrity
  kind: judgment
  provenance: "Operator-authored, 2026-07-30, based on observed behavior in motors-and-controls' sim-09 gate (two proposals both had rule fields absorbing condition-scoping preambles and trailing justifications, caught only by the operator rereading and rewriting both before ratifying), root-caused and refined through direct dialogue rather than a spawned proposal."

- id: tool-passing-is-not-a-principle-check
  domain: spawn-integrity
  kind: judgment
  provenance: "2026-07-?? (exact date not recorded in the FAMOUS project audit at time of promotion), FAMOUS project. One session produced three misses across two soft principles — a comment duplicating ux-library.md content written twice in QueueRows.tsx, the same architectural point re-explained three times in player.tsx, and tag-identity-dependencies-check-before-handoff never once applied to a matching ref-based committer pattern — while self-check-against-composed-domains-before-finalizing was already loaded and verification commands stayed green throughout."
  history:
    - date: 2026-07-23
      type: generalized
      reason: "Promoted from FAMOUS's project-level spawn-integrity domain to seed, alongside minimize-comments-prefer-self-documenting-code (its reason text names 'comment discipline' as one of the unenforced-principle examples this principle guards). Rule/reason otherwise unchanged from the FAMOUS original."

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
  history:
    - date: 2026-07-28
      type: corrected
      reason: "motors-and-controls SchematicNode.tsx review: the rule's ref-holding-previous-value parenthetical failed the project's react-hooks/refs lint (React Compiler-safe, forbids ref access/mutation during render). Same failure mode that killed the sibling behavior-flags-in-refs, but here the core claim (derivable state belongs in render, not an effect) still holds and is not knowledge-tier — corrected the rule to hold the previous value in useState instead of a ref, which is safe under both classic and Compiler-safe React with no condition split needed, rather than killing the principle."

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
  killed: 2026-07-28
  history:
    - date: 2026-07-06
      type: generalized
      reason: "Retrospective: absorbed timer-handles-in-refs-not-state. Timer IDs are behavioral flags; the dep-cascade concern is now part of this principle's reason. Rule and condition extended to name timer handles explicitly."
    - date: 2026-07-18
      type: generalized
      reason: "Structural-kinship retrospective signal: absorbed stable-ref-for-document-listeners. Both were instances of the same ref-vs-state test — mirroring current state for an external listener is a specific case of 'does this value drive rendered output.' Rule and reason extended to name the document-listener case explicitly."
    - date: 2026-07-28
      type: killed
      reason: "kill_type: knowledge — see coding-react.md's killed: log for the full reason. Standard React-documentation content plus a concrete Compiler-safe-lint failure surfaced in motors-and-controls."

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
# composition: declared by ui-design and ux-design (moved out of the working file's own prose 2026-07-25
# so a consuming spawn's context doesn't carry the sibling composition's name for no functional benefit)
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
# composition: declared by ux-design and ui-design (moved out of the working file's own prose 2026-07-25
# so a consuming spawn's context doesn't carry the sibling composition's name for no functional benefit)
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
# composition: declared by ux-design and ui-design (moved out of the working file's own prose 2026-07-25
# so a consuming spawn's context doesn't carry the sibling composition's name for no functional benefit)
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
# composition: declared by ux-design and ui-design (moved out of the working file's own prose 2026-07-25
# so a consuming spawn's context doesn't carry the sibling composition's name for no functional benefit)
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
# composition: declared by ux-design and ui-design (moved out of the working file's own prose 2026-07-25
# so a consuming spawn's context doesn't carry the sibling composition's name for no functional benefit)
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
    - date: 2026-07-30
      type: graduated-to-convention
      reason: "proposals/domain-repo-import.md §1: unstructured preamble prose replaced by an id-addressable conventions: entry — same id, same unconditioned status, now killable/graduatable/importable instead of dissolved into prose."

- id: no-early-returns
  domain: coding-ts
  provenance: "2026-06-17, Blog project, 'Explicit by Default' post (content/posts/coding/explicit-by-default.mdx). Derived from Crockford's heuristic, not style: indentation-as-grammar (Henney) means early returns let a multi-condition line sit at base indentation as if unconditional; the guard-clause exception reintroduces a per-function 'still simple enough?' judgment a block body removes; the strong counterexample (a flat row of order-independent guards) resolves to extraction-and-naming, not exception. Scoped to this pack because some ecosystems (Go) idiomatically prefer guard clauses; the reasoning is general."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-ts's own preamble."
    - date: 2026-07-30
      type: graduated-to-convention
      reason: "proposals/domain-repo-import.md §1: unstructured preamble prose replaced by an id-addressable conventions: entry — same id, same unconditioned status, now killable/graduatable/importable instead of dissolved into prose."

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

- id: consuming-lens-includes-agent-vs-human-gap
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-23, FAMOUS skill-mining ratify session. Generalized from that session's four-candidate borderline review (coding-expo.md): three killed for targeting human-specific habits/memory rather than agent-relevant mechanism risk, one kept for naming a concrete trap in the agent's own verification workflow — see LINEAGE.md."

- id: mined-workflow-stays-a-workflow
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-23, FAMOUS skill-mining ratify session. Generalized from that session's decision to drop six web-to-native candidates that atomized a coherent migration workflow rather than encoding independent mechanism-level judgment — see LINEAGE.md."

- id: cost-of-discovery-is-not-judgment-evidence
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-24, backlog-triage discussion. Named directly from a recurring rationalization pattern the operator has observed agents use — arguing a hard-to-trace bug fix should become a principle because it was difficult or costly to find, independent of whether the insight recurs."

- id: strip-specifics-to-find-the-transferable-method
  domain: principle-judgment
  kind: judgment
  provenance: "2026-07-24, backlog-triage discussion. Paired with cost-of-discovery-is-not-judgment-evidence as the constructive counterpart: rather than reject every hard-won-fix candidate outright, test whether a transferable diagnostic method survives once the specific facts are stripped out."

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
  provenance: "2026-07-22, reading pipeline (docs.expo.dev/guides/new-architecture), reworded from Expo-specific to general form when moved out of the then-uncreated coding-expo domain. Originally weighed for a kill-as-knowledge ('fairly standard') but held as judgment on review: the operator's own framing was that this is standard-but-under-practiced discipline (deferring an optional migration to its deadline is a real, recurring failure mode despite being agreed-upon in the abstract), which is exactly what the genuine-fork test is for — distinct from a lookup fact. Reassigned from coding-general to a new dependency-management domain + matching lens: this judgment applies to tasks actually about upgrading/migrating, not to every convergent coding spawn regardless of task shape (kernel.md, 'Recognizing that a task needs a different lens'). First seen concretely in Expo's New Architecture migration (support for the old architecture ends at SDK 55 while still optional at the time of writing) — real breakage there was only discoverable by running the app against it, not by reading the migration guide."

- id: audit-transitive-dependencies-after-major-upgrade
  domain: dependency-management
  kind: judgment
  provenance: "2026-07-22, reading pipeline (buildmvpfast.com/blog/expo-sdk-56-inline-native-modules-router-fork-new-features-2026), reworded from Expo-specific to general form. Same reassignment reasoning as adopt-forced-migration-early-on-disposable-branch — held as judgment, moved to the new dependency-management domain rather than coding-general. First seen concretely when Expo SDK 56 stopped bundling @expo/vector-icons as a transitive dependency."

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

- id: no-color-platformcolor-values-in-reanimated-styles
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/building-native-ui/SKILL.md, references/animations.md), not the URL reading pipeline. Ratified directly to seed — names the specific silent-failure mechanism (opaque platform color handle vs. interpolable JS value) rather than a generic animation-API caveat."

- id: medialibrary-save-requires-local-file-not-base64
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/building-native-ui/references/media.md). Ratified directly to seed — a sharp, specific API gotcha (no inline-data code path) rather than an API-reference restatement."

- id: liquid-glass-feature-detect-with-blur-fallback
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/building-native-ui/references/visual-effects.md). Ratified directly to seed — names the specific OS-version coupling risk of treating a newest-iOS-only material as always available."

- id: blurview-requires-overflow-hidden-for-rounded-corners
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/building-native-ui/references/visual-effects.md). Ratified directly to seed — a concrete, silent visual bug (blur bleeding past rounded corners) with no compiler or runtime signal."

- id: css-gradients-require-new-architecture
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/building-native-ui/references/gradients.md). Ratified directly to seed — names what the experimental_ prefix actually gates (Fabric-only, not general instability) rather than a generic 'experimental APIs are risky' truism."

- id: expo-go-default-until-native-code-needed
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/building-native-ui/SKILL.md, .agents/skills/expo-dev-client/SKILL.md). Merged from two drafted candidates (expo-go-before-custom-native-build, expo-go-outgrown-once-native-code-needed) covering the same default from both directions — ratified as one entry rather than two near-duplicates."

- id: expo-ui-list-not-virtualized-avoid-for-large-lists
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/web-to-native/references/native-patterns.md, .agents/skills/expo-ui/references/jetpack-compose.md, references/universal.md). Merged from two near-identical drafted candidates (expo-ui-list-not-for-large-feeds, expo-ui-list-not-virtualized) surfaced independently from web-to-native and expo-ui sources — ratified as one entry."

- id: expo-router-toolbar-children-not-behind-wrapper
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/toolbar-and-headers.md). Ratified over operator's non-obviousness challenge to the batch: Stack.Toolbar is a newer, sparsely-documented API whose children-introspection mechanism isn't the kind of thing a generic search on the blank-toolbar symptom surfaces — distinct from the sibling candidates killed in the same batch for being easily-searchable, well-documented gotchas."

- id: expo-router-always-resolve-root-path (killed)
  domain: coding-expo
  kind: knowledge
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/SKILL.md). Killed at ratify — see kill_type/reason_killed in domains/coding-expo.md's killed: log."

- id: no-bare-group-route-file (killed)
  domain: coding-expo
  kind: knowledge
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/route-structure.md). Killed at ratify — see kill_type/reason_killed in domains/coding-expo.md's killed: log."

- id: expo-router-renamed-initialroutename-to-anchor (killed)
  domain: coding-expo
  kind: knowledge
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/route-structure.md). Operator asked to verify against real FAMOUS usage before ratifying; grep found zero instances of initialRouteName/unstable_settings in the project. Killed — see kill_type/reason_killed in domains/coding-expo.md's killed: log."

- id: expo-router-array-group-for-shared-tab-screens
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/SKILL.md). Ratified directly to seed — names a real route-identity divergence risk (duplicated screens carrying independent back-stack/state) not obvious from the array-group feature's own name."

- id: native-tabs-must-be-statically-defined
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/tabs.md). Ratified directly to seed — a silent full-navigator remount triggered by what reads as an ordinary conditional render, genuinely hard to attribute without knowing the native-controller mechanism."

- id: native-tabs-bottomaccessory-state-outside-component
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/tabs.md). Ratified directly to seed — the dual-instance mounting behavior (regular + inline placement simultaneously) is a non-obvious mechanism no amount of staring at the component's own code would reveal."

- id: native-tabs-transparency-requires-first-opaque-child-not-collapsed
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/tabs.md). Ratified directly to seed — reproduces only in optimized/release builds where View-collapsing actually happens, a classic dev-vs-release divergence that's hard to nail down from the release-build symptom alone."

- id: zoom-transition-dismissal-bounds-for-inner-scrollview
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/zoom-transitions.md). Ratified directly to seed — a gesture-arbitration conflict between two independently-reasonable-looking APIs (zoom dismissal + inner scroll), not discoverable by reading either API's docs in isolation."

- id: formsheet-detent-index-controls-background-interactivity
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-router/references/form-sheet.md). Ratified directly to seed — the default-dims-at-every-detent behavior is a specific, non-obvious default that only a form-sheet-specific prop (sheetLargestUndimmedDetentIndex) resolves."

# domain: dependency-management-expo (new domain, seeded 2026-07-23)
- id: pin-multi-package-versions-for-native-graphics-stack
  domain: dependency-management-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/building-native-ui/references/webgpu-three.md), not the URL reading pipeline. Ratified directly to seed — names a real compatibility-contract gap semver doesn't express, not a restatement of 'pin your versions.'"

- id: recheck-workaround-artifacts-every-sdk-upgrade
  domain: dependency-management-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/upgrading-expo/SKILL.md). Ratified directly to seed — same failure shape as ceiling-comment-for-deliberate-shortcuts, applied to expo.install.exclude/patches specifically."

- id: codemod-deprecation-check-after-rewrite
  domain: dependency-management-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/upgrading-expo/references/react-navigation-to-expo-router.md). Operator flagged the initial draft's rule for leaking its reason (naming the specific migration inline instead of stating the general check) — reworded so rule states the generalizable guidance and condition carries the SDK-56-specific instance. Filed to a new dependency-management-expo domain rather than directly into stack-agnostic dependency-management: not general enough on a single data point, and specifically a codemod-migration judgment that may fork further if a comparable non-Expo codemod scenario surfaces."

- id: escalate-unmapped-symbols-dont-diy-workaround
  domain: dependency-management-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/upgrading-expo/references/react-navigation-to-expo-router.md). Ratified directly to seed — same dependency-management-expo homing reasoning as codemod-deprecation-check-after-rewrite; also codemod-migration-shaped rather than strictly Expo-specific."

- id: reanimated-worklets-new-required-peer-post-newarch
  domain: dependency-management-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/upgrading-expo/references/new-architecture.md). Operator flagged the initial draft's rule for leaking its reason (SDK-54/worklets specifics stated as the rule itself) — reworded so rule states the general 'check for new required peer deps after a major upgrade' guidance and condition carries the Reanimated/worklets specifics."

- id: root-stack-vs-js-stack-codemod-collision
  domain: dependency-management-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/upgrading-expo/references/react-navigation-to-expo-router.md). Operator flagged the initial draft's rule for leaking its reason (the Stack/js-stack distinction stated inline in the rule) — reworded so rule states the pure directive and reason carries the explanation. Routed to dependency-management-expo rather than coding-expo on operator's call: migration/codemod-specific judgment, not general Expo implementation judgment."

- id: expo-av-video-android-parity-gap-fails-silently
  domain: dependency-management-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/upgrading-expo/references/expo-av-to-video.md). Ratified directly — every named failure mode is a silent Android-only visual regression invisible to iOS-only testing. Routed to dependency-management-expo alongside root-stack-vs-js-stack-codemod-collision: migration-verification judgment, not general Expo implementation judgment."

- id: dom-component-router-hooks-not-callable
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/web-to-native/references/false-friends.md, .agents/skills/use-dom/SKILL.md — same rule surfaced independently from both sources, merged into one entry). Kept as coding-expo mechanism judgment (not migration-workflow-shaped, per operator's web-to-native split): fires whenever a DOM component touches route state, not only during a bulk migration."

- id: layout-route-cannot-be-a-dom-component
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/web-to-native/references/false-friends.md). Kept as coding-expo mechanism judgment per the same web-to-native split: a structural DOM-component/layout-route rule, not migration-sequencing advice."

- id: streaming-fetch-requires-expo-fetch-not-rn-fetch
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/web-to-native/references/false-friends.md). Kept as coding-expo mechanism judgment: fires whenever native code reads a streaming response, independent of migration context. Six sibling web-to-native candidates (expo-dom-shell-ships-before-nativizing, dom-screen-runtime-cost-caps-nativize-scope, nativize-means-redesign-not-reskin, iap-required-for-digital-goods-decide-at-assess, async-server-components-must-split-before-porting, motion-and-touch-are-part-of-native-not-polish) dropped entirely rather than ratified or kill-logged — operator judgment: these atomize the FAMOUS web-to-native skill's own coherent workflow sequencing, and lose the ordering/connective 'why this step before that step' reasoning the skill file already carries; the skill itself is the better artifact to load for that workflow, not a container mismatch worth a kill-log entry. Two more (stale-expo-go-bundle-trap, verify-migration-by-running-not-compiling) dropped earlier in the same review for being easily-searchable/generic, also not kill-logged since they were never ratified into a domain to begin with."

- id: release-build-cannot-hot-reload-reuse-is-wrong-tool
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/eas-simulator/SKILL.md, references/run-your-app.md, references/troubleshooting.md). Operator questioned whether an agent (vs. a human) would actually trip on this; kept on reasoning that it's a concrete trap in the agent's own verification workflow specifically — screenshotting a stale release build via /run or /verify and misattributing 'no visible change' to a failed fix rather than a stale bundle, with no error signal to distinguish the two."

- id: expo-public-env-vars-are-client-visible (killed)
  domain: coding-expo
  kind: knowledge
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/native-data-fetching/SKILL.md). Killed after operator's consuming-lens challenge — see kill_type/reason_killed in domains/coding-expo.md's killed: log."

- id: dom-component-isolated-context-no-shared-state (killed)
  domain: coding-expo
  kind: knowledge
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/use-dom/SKILL.md). Killed after operator's consuming-lens challenge — redundant with the already-ratified dom-component-router-hooks-not-callable. See kill_type/reason_killed in domains/coding-expo.md's killed: log."

- id: expo-ui-universal-before-platform-specific (killed)
  domain: coding-expo
  kind: knowledge
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-ui/SKILL.md). Killed after operator's consuming-lens challenge, contrasted directly against the kept release-build-cannot-hot-reload-reuse-is-wrong-tool in the same review. See kill_type/reason_killed in domains/coding-expo.md's killed: log."

- id: nativewind-inline-variables-breaks-platform-color
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-tailwind-setup/SKILL.md). Ratified directly to seed — a specific, silent config-interaction break (inlineVariables optimization vs. platformColor's need for a live native reference) with no error signal."

- id: expo-router-loader-data-cached-for-session
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/native-data-fetching/references/expo-router-loaders.md). Ratified directly to seed — a documented-as-limitation-not-cache-control behavior that silently violates the SPA assumption of fresh data per revisit."

- id: expo-router-loader-request-object-mode-dependent
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/native-data-fetching/references/expo-router-loaders.md). Ratified directly to seed — a config-flip-triggered crash (server mode populates request, static mode never does) invisible until the output mode actually changes."

- id: eas-hosting-api-routes-run-on-workers-not-node
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-api-routes/SKILL.md). Ratified directly to seed — classic works-locally-fails-in-production trap (local npx expo serve runs Node, EAS Hosting deploys to Cloudflare Workers)."

- id: expo-ui-platform-specific-import-crashes-wrong-platform
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-ui/SKILL.md). Ratified directly to seed — a runtime-only crash ('Unable to get view config') from an import that resolves fine in JS and only fails at native view registration."

- id: expo-router-no-platform-extension-route-files
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-ui/references/universal.md). Ratified directly to seed — names the specific conflict between two independently-reasonable filename conventions (Metro's platform-extension resolution vs. Expo Router's route resolution)."

- id: expo-ui-usenativestate-silently-degrades-without-worklets
  domain: coding-expo
  kind: judgment
  provenance: "2026-07-23, mined from FAMOUS's local Expo/React Native team skill docs (.agents/skills/expo-ui/references/drop-in-replacements.md). Ratified directly to seed — a silent fallback to normal React render cycle that's easy to misdiagnose as an API limitation rather than a missing prerequisite."
```

<!-- corpus-script:begin — maintained by scripts/corpus.py; do not edit by hand -->

## counters (script-maintained)

```yaml
counters:
  - domain: coding-expo
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 9700
    baseline-tokens: 9663
    principles-at-baseline: 35
    kills-at-baseline: 6
    conventions-at-baseline: 0
  - domain: coding-general
    origin: seed
    since: 2026-07-23
    ratified: 2
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 5715
    baseline-tokens: 5335
    principles-at-baseline: 18
    kills-at-baseline: 1
    conventions-at-baseline: 0
  - domain: coding-nextjs
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 1137
    baseline-tokens: 1119
    principles-at-baseline: 5
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: coding-react
    origin: seed
    since: 2026-07-28
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 4629
    baseline-tokens: 4465
    principles-at-baseline: 12
    kills-at-baseline: 10
    conventions-at-baseline: 0
  - domain: coding-ts
    origin: project
    since: 2026-07-30
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 1547
    baseline-tokens: 1547
    principles-at-baseline: 5
    kills-at-baseline: 2
    conventions-at-baseline: 2
  - domain: color
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 801
    baseline-tokens: 775
    principles-at-baseline: 2
    kills-at-baseline: 2
    conventions-at-baseline: 0
  - domain: css
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 1495
    baseline-tokens: 1474
    principles-at-baseline: 4
    kills-at-baseline: 4
    conventions-at-baseline: 0
  - domain: dependency-management-expo
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 2073
    baseline-tokens: 2035
    principles-at-baseline: 7
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: dependency-management
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 824
    baseline-tokens: 891
    principles-at-baseline: 2
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: design-method
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 1377
    baseline-tokens: 1330
    principles-at-baseline: 4
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: forms-inputs
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 1552
    baseline-tokens: 1526
    principles-at-baseline: 7
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: interviewing
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 827
    baseline-tokens: 810
    principles-at-baseline: 3
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: lists-selection
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 1051
    baseline-tokens: 1027
    principles-at-baseline: 3
    kills-at-baseline: 1
    conventions-at-baseline: 0
  - domain: motion
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 822
    baseline-tokens: 798
    principles-at-baseline: 4
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: orchestrator-routing
    origin: seed
    since: 2026-07-23
    ratified: 0
    killed: 2
    graduated: 0
    gate-violations: 0
    working-file-tokens: 4128
    baseline-tokens: 3460
    principles-at-baseline: 16
    kills-at-baseline: 1
    conventions-at-baseline: 0
  - domain: planning
    origin: seed
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 2312
    baseline-tokens: 2145
    principles-at-baseline: 5
    kills-at-baseline: 1
    conventions-at-baseline: 0
  - domain: principle-judgment
    origin: seed
    since: 2026-07-30
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 3620
    baseline-tokens: 3620
    principles-at-baseline: 11
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: ranking-evaluation
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 873
    baseline-tokens: 853
    principles-at-baseline: 5
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: ratify-gate
    origin: seed
    since: 2026-07-30
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 2418
    baseline-tokens: 2418
    principles-at-baseline: 9
    kills-at-baseline: 2
    conventions-at-baseline: 0
  - domain: recoverability
    origin: seed
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 618
    baseline-tokens: 595
    principles-at-baseline: 2
    kills-at-baseline: 1
    conventions-at-baseline: 0
  - domain: spawn-integrity
    origin: seed
    since: 2026-07-28
    ratified: 2
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 2208
    baseline-tokens: 1592
    principles-at-baseline: 3
    kills-at-baseline: 3
    conventions-at-baseline: 0
  - domain: surfaces-elevation
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 506
    baseline-tokens: 479
    principles-at-baseline: 3
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: validation-feedback
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 417
    baseline-tokens: 390
    principles-at-baseline: 3
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: visual-hierarchy
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 788
    baseline-tokens: 762
    principles-at-baseline: 4
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: wizards-flows
    origin: project
    since: 2026-07-23
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 488
    baseline-tokens: 499
    principles-at-baseline: 3
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: retrospective
    origin: project
    since: 2026-07-30
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 2545
    baseline-tokens: 2545
    principles-at-baseline: 10
    kills-at-baseline: 0
    conventions-at-baseline: 0
  - domain: testing
    origin: project
    since: 2026-07-30
    ratified: 0
    killed: 0
    graduated: 0
    gate-violations: 0
    working-file-tokens: 1816
    baseline-tokens: 1816
    principles-at-baseline: 6
    kills-at-baseline: 0
    conventions-at-baseline: 0
efficacy:
  - id: task-is-actionable-without-planning
    fired: 1
    violated: 0
    idle: 0
  - id: sequence-by-output-dependency
    fired: 1
    violated: 0
    idle: 0
  - id: open-questions-are-explicit
    fired: 1
    violated: 0
    idle: 0
  - id: task-describes-output-not-implementation
    fired: 1
    violated: 0
    idle: 0
  - id: concern-names-work-not-role
    fired: 1
    violated: 0
    idle: 0
  - id: structural-examination-at-working-checkpoint
    fired: 3
    violated: 0
    idle: 0
  - id: no-single-char-names
    fired: 1
    violated: 0
    idle: 0
  - id: unified-representation-no-type-leakage
    fired: 4
    violated: 0
    idle: 0
  - id: code-lives-at-consumer-level
    fired: 7
    violated: 0
    idle: 0
  - id: minimize-comments-prefer-self-documenting-code
    fired: 6
    violated: 0
    idle: 0
  - id: named-exports-over-default
    fired: 1
    violated: 0
    idle: 0
  - id: null-first-ternary
    fired: 1
    violated: 0
    idle: 0
  - id: single-callsite-helper-scoped
    fired: 2
    violated: 0
    idle: 0
  - id: behavior-flags-in-refs
    fired: 4
    violated: 0
    idle: 0
  - id: ceiling-comment-for-deliberate-shortcuts
    fired: 2
    violated: 0
    idle: 0
  - id: custom-hook-owns-its-concern
    fired: 1
    violated: 0
    idle: 0
  - id: scripts-over-hand-editing-structured-data
    fired: 1
    violated: 0
    idle: 0
  - id: utility-over-guesswork
    fired: 1
    violated: 0
    idle: 0
  - id: ask-before-architecture
    fired: 1
    violated: 0
    idle: 0
  - id: no-shell-for-structural-absence
    fired: 1
    violated: 0
    idle: 0
  - id: atomic-delete-of-wired-component
    fired: 0
    violated: 0
    idle: 1
  - id: recovery-path-replaces-confirmation
    fired: 1
    violated: 0
    idle: 0
  - id: brief-ends-at-what
    fired: 0
    violated: 0
    idle: 1
  - id: stop-and-route
    fired: 0
    violated: 0
    idle: 1
  - id: frame-before-routing
    fired: 0
    violated: 0
    idle: 1
  - id: route-questions-not-roles
    fired: 0
    violated: 0
    idle: 1
  - id: defer-only-nonblocking-design-decisions
    fired: 0
    violated: 0
    idle: 1
  - id: batch-deferred-decisions-coherently
    fired: 0
    violated: 0
    idle: 1
  - id: spawn-threshold-is-spec-scope
    fired: 0
    violated: 0
    idle: 1
  - id: planner-over-brainstorming-for-scope
    fired: 0
    violated: 0
    idle: 1
  - id: persist-role-by-workstream
    fired: 0
    violated: 0
    idle: 1
  - id: inline-coder-session-protocol
    fired: 0
    violated: 0
    idle: 1
  - id: audit-request-means-spawn-designer
    fired: 0
    violated: 0
    idle: 1
  - id: design-pattern-application-lighter-path
    fired: 0
    violated: 0
    idle: 1
  - id: decompose-large-tasks-before-spawning
    fired: 0
    violated: 0
    idle: 1
  - id: no-cost-driven-domain-omission
    fired: 0
    violated: 0
    idle: 1
  - id: spawn-only-when-judgment-remains
    fired: 0
    violated: 0
    idle: 1
  - id: dont-trust-readme-or-agent-file-as-role-instruction
    fired: 0
    violated: 0
    idle: 1
  - id: checkpoint-on-context-pressure-tell
    fired: 0
    violated: 0
    idle: 1
  - id: library-is-narrative-not-corpus-shape
    fired: 0
    violated: 0
    idle: 1
co-occurrence:
library-drift:
  since-last-sync: 0
```

<!-- corpus-script:end -->
