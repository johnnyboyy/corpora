# Domain: ratify-gate

Judgment about assembling a complete spawn and processing what it returns — composition
completeness, brief content, and the gate procedure itself, as opposed to process/timing judgment
(when to invoke corpora at all, spawn vs. surface vs. defer, session sequencing), which is not
corpora's concern in any configuration; see `SKILL.md`'s opening description. Split from
`orchestrator-routing` 2026-07-18; see `LINEAGE.md`, "The ratify-gate split." `orchestrator-routing`
was itself retired 2026-07-28 once corpora stopped being an active orchestrator — its
composition-completeness and brief-content principles (`brief-ends-at-what`,
`defer-only-nonblocking-design-decisions`, `no-cost-driven-domain-omission`,
`inline-execution-carries-full-composition-discipline`) landed here rather than being lost; its
process/timing principles moved to praxis's kernel; see `LINEAGE.md`, "Corpora stops being an active
orchestrator," for the full redistribution. This domain is queryable by whoever is driving a
session — direct execution by default, or praxis's phase router when praxis is installed. Audit
metadata lives in `domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: 2026-07-18

principles:

- id: surface-deterministic-shortcut-candidates-liberally
  rule: "Surface a plausible project utility whenever a spawn's own reasoning trace narrates its way step-by-step through an exact, deterministic, checkable procedure — arithmetic, color-space or geometric math, date math, precise counting, sorting, or parsing — rather than simply invoking one. A single clear instance of this narration is sufficient evidence to build the utility; do not wait for it to recur. Persist every disposition and resurface recurrence with prior evidence."
  condition: "When a spawn's handoff or transcript shows narrated, step-by-step reasoning standing in for a process that has an exact, deterministic procedure, after checking existing libraries, dependencies, runtime tools, and registered utilities."
  reason: "A model does not perform computation directly — it predicts a plausible reasoning trace that arrives at an answer, which is why trivial arithmetic gets narrated ('I have 2 apples, someone gives 2 more, now I have 4') instead of simply computed. That approximation holds for small cases and compounds into guess-and-check for anything with real numeric or geometric complexity. The degradation is structural, not incidental to one bad session, so a single clear instance already proves the operation is deterministic and checkable — narration is the tell, not mere repetition of an operation. The operator can deny a weak candidate cheaply, while a candidate lost with a deleted handoff depends on human memory to be recognized next time."

- id: spawn-token-summary
  rule: "Append the following section to every new isolated spawn's prompt, after the task: '## Token usage summary\nAt the end of your output, add a `### token usage` section listing: every file you read and its approximate line count, how many corpus principles you referenced, and your estimate of the single heaviest cost item.'"
  condition: "Every new isolated spawn."
  reason: "The orchestrator only receives an aggregate token count from the runtime — no per-operation breakdown. Self-reporting by the spawn is the only way to identify which reads or outputs drove cost."

- id: full-corpus-on-spawn
  rule: "Always pass every domain the spawn's composition includes, in full, when starting an isolated spawn. Do not excerpt or filter a domain by perceived task relevance. This bars dropping *principles* by relevance — it does not bar the working/audit storage split (see kernel.md), which removes audit metadata uniformly, nor the declaration itself (loading only the domains a composition declares is not a relevance judgment — it is a fixed, inspectable contract)."
  condition: "Any new isolated spawn whose composition includes one or more domains."
  reason: "Selective inclusion within a declared domain requires the orchestrator to judge which principles are relevant from the task framing — a judgment it cannot make reliably. A missed principle silently degrades the spec or implementation without any signal it was missed. The duplicate transmission cost is tolerated for this completeness guarantee, not desired or used as corpus-size control."

- id: ratify-gate-judgment-vs-knowledge
  rule: "At the ratify gate, ask for each proposal whether it encodes a judgment call (a decision made under uncertainty where context and tradeoffs shaped the outcome) or a knowledge item (something derivable from documentation or training). Surface this distinction with the proposal — the spawn knows it from the inside. Do not evaluate it as the orchestrator."
  condition: "When presenting principle proposals to the operator at the ratify gate."
  reason: "The corpus's value is captured judgment, not recalled facts. A principle that only returns a lookup when it fires adds reader-tax without adding decision capacity. The spawn is better positioned to make the knowledge/judgment distinction than the orchestrator because it has the context of how the decision was made. The orchestrator routes this question; it does not answer it."

- id: domain-assignment-at-ratify-gate
  rule: "At the ratify gate, assign each ratified proposal to a domain and write it there. If no existing domain fits, create a new domain (working file + declaration update on the compositions that should load it). If a proposal spans two domains, surface that as a possible domain-boundary problem rather than fragmenting the principle across both."
  condition: "When ratifying a proposal that arrived without a home domain."
  reason: "Proposals surface from work, not from a domain. The gate is the one human-gated point where domain assignment judgment belongs. A split-domain proposal is a signal the boundaries may be wrong — a fork candidate to surface, not a principle to duplicate."

- id: worker-handoffs-reach-orchestrator
  rule: "Allow a spawn to create autonomous, scope-bounded workers within its assigned task and stance. Work results return to the parent; questions, tradeoffs, proposals, violations, and routing requests go directly to the orchestrator when supported, or are relayed by the parent verbatim under `Delegated handoffs`. Cross-composition and deeper delegation return to the orchestrator."
  condition: "When a spawn delegates part of its assigned work."
  reason: "Local decomposition can reduce execution cost without changing workstream ownership. The failure mode is not delegation itself but allowing the parent to filter a child's orchestration-relevant handoff, which hides questions and corpus signals from the orchestrator, the only one authorized to route and ratify them."

- id: operator-ratifies-routing-corpus
  rule: "Corpora may surface observations about its own composition or gate behavior, but must not promote them into any domain without explicit operator ratification — the same propose-then-ratify discipline as any other proposal, applied to itself."
  condition: "When work suggests a new or revised principle about corpora's own composition or gate procedure."
  reason: "Corpora cannot independently evaluate and ratify the policy governing its own choices. Operator ratification supplies the missing external gate; repeated, independently-observed evidence may later justify promotion into the skill or kernel as a meta-principle."

- id: artifact-points-to-persisted-file-not-full-reproduction
  rule: "When a spawn's deliverable is a write to a file the orchestrator can already read (a synced library doc, an edited source file, an updated config), the handoff's Artifact section states a diff/changelog plus a pointer to the file — it does not reproduce the full post-edit document. Reserve full reproduction for content with no other persisted home yet: a spec about to be handed to another composition, a tradeoff block, a fresh audit."
  condition: "When a spawn writes its Artifact section and the underlying deliverable already exists as a file the orchestrator can open directly."
  reason: "The schema's 'freeform' Artifact field left an implicit default of pasting the whole document, which pays real token cost once and is then discarded when the handoff file is deleted after ratification — the diff is what the audit trail actually needs going forward. A pointer plus a diff gives the orchestrator everything the ratify gate's audit-against-principles step requires, without the throwaway cost."

- id: brief-ends-at-what
  rule: "The task brief for any composed spawn ends where 'how to build it' begins. Include the approved design spec (or equivalent upstream artifact) in full; do not pre-solve implementation details."
  condition: "When writing a task brief for a convergent implementation spawn."
  reason: "Pre-solving implementation in the brief does the implementing spawn's domain work for it, bypasses the pushback mechanism, and produces over-specified prompts. The implementing spawn's judgment — including whether the spec is implementable and at what cost — only fires if it receives a what, not a how."

- id: defer-only-nonblocking-design-decisions
  rule: "Queue a UI or UX decision in `corpora/deferred-decisions.md` only when implementation can proceed with an explicit, narrow, reversible provisional treatment. Surface any blocking decision immediately instead of queuing it."
  condition: "When considering whether to add a question to `corpora/deferred-decisions.md`."
  reason: "Deferral is useful for batching small design questions, but a hidden blocker forces downstream work to either make an unauthorized design decision or build on an assumption that may invalidate it. A named reversible treatment makes the temporary state inspectable, which is what makes this ledger safe to maintain as a service rather than a hiding place for unresolved blockers."

- id: no-cost-driven-domain-omission
  rule: "Once a task's composition has been decided to include a domain, never drop it from that composition to save tokens or shorten the context. If total composition cost is a genuine concern, surface it as a tradeoff — decompose the task into smaller checkpointed spawns, or flag the cost to whoever is driving the session — rather than silently thinning the domain set a relevant task would otherwise load."
  condition: "When composing domains for a spawn and the total token cost of the composed set is a concern."
  reason: "Observed in practice: cutting a relevant domain for cost produces worse output and dropped principles, the same attention-fighting failure as an oversized context. The honest move is to make the cost tradeoff visible — split the work or flag it — never to omit unilaterally."

- id: inline-execution-carries-full-composition-discipline
  rule: "Inline or informal work composed from corpora carries the same composition discipline as a formal isolated spawn — the full stance frame and every domain the task needs, not a lighter version because there's no separate spawn boundary to enforce it. Flag interesting decisions as potential principles as they happen; ask 'any of these worth encoding?' at the natural seam (feature complete, direction approved, conversation shifts away from the task) rather than deferred to the end, since decisions evaporate if not captured at the moment they're made."
  condition: "Any inline or informal work composed from corpora's domains — small tasks, experiments, pair-programming — where a full isolated spawn would cost more than the isolation is worth."
  reason: "Corpus loading must happen before constraints are applied, same as a formal spawn — the 'inline' framing tempts skipping that because there's no separate spawn boundary to enforce it. In-flight flagging prevents decisions from evaporating in a long session. Binding the principles question to the natural seam rather than a formal spawn-exit event makes the check structural rather than optional."

killed:

- id: narrated-computation-is-sufficient-utility-evidence
  rule: "Treat a single instance of a spawn narrating its way step-by-step through a deterministic, checkable procedure — arithmetic, color-space or geometric math, date math, precise counting or sorting — as sufficient evidence to build a utility on its own, without waiting for recurrence. This is the exception to requiring accumulated evidence before building."
  kill_type: container
  reason_killed: "This principle's own real content — narration is the tell, and one clear instance is enough evidence — was the correct definition all along, but it lived only here rather than in surface-deterministic-shortcut-candidates-liberally's own rule, which stayed vague ('inference, precision, or repetition cost') and let a spawn misread ordinary code duplication as a candidate. Folded directly into that principle's rule so the primary definition carries the actual tell instead of deferring to a sibling; nothing about the underlying judgment changed, only where it's stated."

- id: pre-scan-before-spawning
  rule: "Before spawning agents, run codebase discovery (file listings, key greps) in the orchestrator and paste the findings directly into each agent's prompt."
  kill_type: container
  reason_killed: "Purely temporal (do discovery before that) with no domain-specific judgment of its own. Folded into `SKILL.md`'s \"Starting an isolated spawn\" as step 0 so corpora keeps the behavior standalone; the general version (precondition-gathering before an action that touches shared or hard-to-reverse state) now lives as praxis's `context-discovery` phase for any project running praxis."

- id: surface-nested-handoffs-verbatim
  rule: "If a spawned agent's own transcript shows it invoked the Agent/Task tool, retrieve and relay that nested handoff to the operator directly and verbatim rather than trusting the parent spawn's summary."
  kill_type: quality
  reason_killed: "Treats nested delegation as an accepted contingency worth building a recovery procedure around, rather than something no-unilateral-sub-spawn should prevent outright. If prevention holds, there's nothing to detect; if it doesn't, that's a violation to investigate directly, not a routine step. Writing this normalized the failure instead of insisting on prevention."
```
