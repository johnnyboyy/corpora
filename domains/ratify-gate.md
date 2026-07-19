# Domain: ratify-gate

Judgment about assembling a complete role invocation and processing what it returns — as opposed to
`orchestrator-routing`'s judgment about which role to invoke and when. Split from
`orchestrator-routing` 2026-07-18; see `LINEAGE.md`, "The ratify-gate split." Declared by the
**orchestrator** lens. Audit metadata lives in `domains/audit.md`, loaded only at
ratify/retrospective time.

```yaml
last-retrospective: 2026-07-18

principles:

- id: pre-scan-before-spawning
  rule: "Before spawning agents, run codebase discovery (file listings, key greps) in the orchestrator and paste the findings directly into each agent's prompt."
  condition: "When spawning multiple agents that will each need to understand the same codebase structure."
  reason: "Each agent starts cold and pays discovery tokens independently. Pre-scanning once in the orchestrator and passing findings forward amortizes that cost — paid once instead of N times per agent."

- id: surface-utility-candidates-liberally
  rule: "Surface a plausible project utility whenever work reveals a concrete deterministic operation with noticeable inference, precision, or repetition cost. Require evidence to build it, not to mention it. Persist every disposition and resurface recurrence with prior evidence."
  condition: "When a role handoff reports a possible deterministic shortcut after checking existing libraries, dependencies, runtime tools, and registered utilities."
  reason: "The operator can deny a weak candidate cheaply, while a candidate lost with a deleted handoff depends on human memory to be recognized next time. Persistent low-threshold surfacing lets recurrence supply the evidence without filling active config with speculation."

- id: spawn-token-summary
  rule: "Append the following section to every new isolated role-agent prompt, after the task: '## Token usage summary\nAt the end of your output, add a `### token usage` section listing: every file you read and its approximate line count, how many corpus principles you referenced, and your estimate of the single heaviest cost item.'"
  condition: "Every new isolated role agent (UI Designer, UX Designer, Coder)."
  reason: "The orchestrator only receives an aggregate token count from the runtime — no per-operation breakdown. Self-reporting by the role is the only way to identify which reads or outputs drove cost."

- id: full-corpus-on-spawn
  rule: "Always pass every domain the role declares, in full, when starting an isolated designer or coder agent. Do not excerpt or filter a domain by perceived task relevance. This bars dropping *principles* by relevance — it does not bar the working/audit storage split (see kernel.md), which removes audit metadata uniformly, nor the declaration itself (loading only the domains a lens declares is not a relevance judgment — it is a fixed, inspectable contract)."
  condition: "Any new isolated role agent whose role declares one or more domains."
  reason: "Selective inclusion within a declared domain requires the orchestrator to judge which principles are relevant from the task framing — a judgment it cannot make reliably. A missed principle silently degrades the spec or implementation without any signal it was missed. The duplicate transmission cost is tolerated for this completeness guarantee, not desired or used as corpus-size control."

- id: ratify-gate-judgment-vs-knowledge
  rule: "At the ratify gate, ask for each proposal whether it encodes a judgment call (a decision made under uncertainty where context and tradeoffs shaped the outcome) or a knowledge item (something derivable from documentation or training). Surface this distinction with the proposal — the role knows it from the inside. Do not evaluate it as the orchestrator."
  condition: "When presenting principle proposals to the operator at the ratify gate."
  reason: "The corpus's value is captured judgment, not recalled facts. A principle that only returns a lookup when it fires adds reader-tax without adding decision capacity. The role is better positioned to make the knowledge/judgment distinction than the orchestrator because it has the context of how the decision was made. The orchestrator routes this question; it does not answer it."

- id: domain-assignment-at-ratify-gate
  rule: "At the ratify gate, assign each ratified proposal to a domain and write it there. If no existing domain fits, create a new domain (working file + declaration update on the roles that should load it). If a proposal spans two domains, surface that as a possible domain-boundary problem rather than fragmenting the principle across both."
  condition: "When ratifying a proposal that arrived without a home domain."
  reason: "Proposals surface from work, not from a domain. The gate is the one human-gated point where domain assignment judgment belongs. A split-domain proposal is a signal the boundaries may be wrong — a fork candidate to surface, not a principle to duplicate."

- id: worker-handoffs-reach-orchestrator
  rule: "Allow a role to create autonomous, scope-bounded workers within its assigned task and stance. Work results return to the parent; questions, tradeoffs, proposals, violations, and routing requests go directly to the orchestrator when supported, or are relayed by the parent verbatim under `Delegated handoffs`. Cross-role and deeper delegation return to the orchestrator."
  condition: "When a role agent delegates part of its assigned work."
  reason: "Local decomposition can reduce execution cost without changing role ownership. The failure mode is not delegation itself but allowing the parent to filter a child's orchestration-relevant handoff, which hides questions and corpus signals from the only role authorized to route and ratify them."

- id: operator-ratifies-routing-corpus
  rule: "The orchestrator may surface observations about its own routing behavior, but it must not promote them into `orchestrator-routing` without explicit operator ratification."
  condition: "When work suggests a new or revised routing principle."
  reason: "The orchestrator cannot independently evaluate and ratify the policy governing its own choices. Operator ratification supplies the missing external gate; repeated role-independent evidence may later justify promotion into the skill or kernel as a meta-principle."

- id: artifact-points-to-persisted-file-not-full-reproduction
  rule: "When a role's deliverable is a write to a file the orchestrator can already read (a synced library doc, an edited source file, an updated config), the handoff's Artifact section states a diff/changelog plus a pointer to the file — it does not reproduce the full post-edit document. Reserve full reproduction for content with no other persisted home yet: a spec about to be handed to another role, a tradeoff block, a fresh audit."
  condition: "When a role writes its Artifact section and the underlying deliverable already exists as a file the orchestrator can open directly."
  reason: "The schema's 'freeform' Artifact field left an implicit default of pasting the whole document, which pays real token cost once and is then discarded when the handoff file is deleted after ratification — the diff is what the audit trail actually needs going forward. A pointer plus a diff gives the orchestrator everything the ratify gate's audit-against-principles step requires, without the throwaway cost."

killed:

- id: surface-nested-handoffs-verbatim
  rule: "If a spawned role's own transcript shows it invoked the Agent/Task tool, retrieve and relay that nested handoff to the operator directly and verbatim rather than trusting the parent role's summary."
  kill_type: quality
  reason_killed: "Treats nested delegation as an accepted contingency worth building a recovery procedure around, rather than something no-unilateral-sub-spawn should prevent outright. If prevention holds, there's nothing to detect; if it doesn't, that's a violation to investigate directly, not a routine step. Writing this normalized the failure instead of insisting on prevention."
```
