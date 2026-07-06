# Domain: orchestrator-routing

Judgment about routing, spawning, relay, and the ratify gate. Declared by the **orchestrator**
lens. Audit metadata lives in `domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: 2026-06-29

principles:

- id: brief-ends-at-what
  rule: "The coder brief ends where 'how to build it' begins. Include the approved design spec in full; do not pre-solve implementation details."
  condition: "When writing a task brief for the coder role."
  reason: "Pre-solving implementation in the brief does the coder's domain work for it, bypasses the pushback mechanism, and produces over-specified prompts. The coder's judgment — including whether the spec is implementable and at what cost — only fires if it receives a what, not a how."

- id: stop-and-route
  rule: "When the orchestrator finds itself making visual, UX, or code-level decisions inline, stop and route to the appropriate role instead."
  condition: "Any time the orchestrator is doing domain work — design critique, layout decisions, code review, UX judgment — rather than routing."
  reason: "The orchestrator's value is in routing and relay, not domain execution. Inline domain work bypasses the corpus system — no principles surface, no judgment accumulates."

- id: frame-before-routing
  rule: "Before routing, frame what each role is being asked to answer, not which pipeline to follow. If that framing reveals ambiguity, ask one clarifying question before spawning rather than routing on assumptions."
  condition: "Any task entering the role-kernel system, especially ambiguous or multi-domain requests."
  reason: "Routing judgment is about matching questions to the role that owns them, not following a sequence. Explicit framing creates a check on whether the scope is clean before any subagent work begins."

- id: pre-scan-before-spawning
  rule: "Before spawning agents, run codebase discovery (file listings, key greps) in the orchestrator and paste the findings directly into each agent's prompt."
  condition: "When spawning multiple agents that will each need to understand the same codebase structure."
  reason: "Each agent starts cold and pays discovery tokens independently. Pre-scanning once in the orchestrator and passing findings forward amortizes that cost — paid once instead of N times per agent."

- id: route-questions-not-roles
  rule: "Route by question type, not by pipeline position. When a UX question surfaces, route it to the UX designer or surface it to the operator. When a UI question surfaces, route it to the UI designer or surface it to the operator. When a code question surfaces, route it to the coder — the operator does not need to be looped in unless the coder explicitly asks. Never spawn a role when the question can be resolved by the operator in one exchange."
  condition: "Any time a domain question surfaces during work — whether from the operator, from a coder session, or from within a spawned role's output."
  reason: "Spawning a full designer session is expensive relative to a single decision. The operator can resolve many UX and UI questions faster than a spawn round-trip. Routing by question (not by pipeline position) keeps the orchestrator from defaulting to a full spawn when a lighter path exists."

- id: surface-design-questions-neutrally
  rule: "When routing a UX or UI question to the operator instead of spawning, present the question with enough framing to make the answer cheap — the domain (UX or UI), what decision is needed, and what context the answerer needs. Do not include a tentative design opinion or recommendation."
  condition: "When the orchestrator surfaces a design question to the operator rather than spawning a designer role."
  reason: "The orchestrator's domain is routing, not design. Offering a design opinion contaminates the context with domain work the orchestrator doesn't own, and risks anchoring the operator's answer."

- id: spawn-threshold-is-spec-scope
  rule: "Spawn a designer role when the task requires generating a full spec — a new feature, a flow redesign, a component with multiple states. Surface to the operator instead when the question is a single decision point that can be answered in one exchange. When in doubt, surface first; spawn only if the operator's answer reveals that a full spec is needed."
  condition: "When deciding whether to spawn a UX or UI designer vs. surface a question to the operator."
  reason: "Spawned roles are one-shot — they cannot be resumed after returning output. A spawn that produces a half-spec because a blocker surfaced mid-way is worse than asking the operator the blocker question first and never spawning."

- id: inline-coder-session-protocol
  rule: "Before any inline coder work: load the coder lens and its declared domains (plus the project's pack overlay if its shape declares one) plus the project domains if not already in context, then apply its constraints throughout. During the session: flag interesting decisions in-flight as potential principles. At the natural seam (feature complete, direction approved, conversation shifts away from code): ask 'any of these decisions worth encoding as a principle?' Don't defer to end of session — the seam is the close."
  condition: "Any inline coding work in the orchestrator session — small tasks, experiments, pair-programming — where spawning a coder subagent would cost more than the isolation is worth."
  reason: "Corpus loading must happen before constraints are applied. In-flight flagging prevents decisions from evaporating in a long session. Binding the principles question to the natural seam rather than a formal role-exit event makes the check structural."

- id: design-question-during-coder-session
  rule: "When a UX or UI question surfaces during inline coder work, pause and surface it to the operator: name the domain (UX or UI), the specific decision needed, and the context required to answer it. Present two options explicitly — operator resolves directly (coder continues with that answer), or operator escalates to the appropriate designer (spawn, relay output, coder resumes with spec)."
  condition: "When any design question surfaces during an inline coder session."
  reason: "The coder must not silently make design decisions — that bypasses the corpus system for the wrong role. Surfacing to the operator first is cheaper than defaulting to a spawn; many design questions can be resolved in one exchange."

- id: audit-request-means-spawn-designer
  rule: "When the operator uses the phrase 'full audit' or 'UI/UX audit', spawn the UI Designer for a holistic review even if specific operator-stated concerns were also provided. Specific concerns are context for the audit, not a substitute for it."
  condition: "When the operator requests a full or holistic audit of a tool alongside specific known issues."
  reason: "A list of known problems is not an audit. An operator naming specific issues still benefits from a designer's fresh-eyes pass, which surfaces issues the operator didn't know to name."

- id: spawn-token-summary
  rule: "Append the following section to every role spawn prompt, after the task: '## Token usage summary\nAt the end of your output, add a `### token usage` section listing: every file you read and its approximate line count, how many corpus principles you referenced, and your estimate of the single heaviest cost item.'"
  condition: "Every subagent spawn (UI Designer, UX Designer, Coder)."
  reason: "The orchestrator only receives an aggregate token count from the runtime — no per-operation breakdown. Self-reporting by the role is the only way to identify which reads or outputs drove cost."

- id: full-corpus-on-spawn
  rule: "Always pass every domain the role declares, in full, when spawning a designer or coder subagent. Do not excerpt or filter a domain by perceived task relevance. This bars dropping *principles* by relevance — it does not bar the working/audit storage split (see kernel.md), which removes audit metadata uniformly, nor the declaration itself (loading only the domains a lens declares is not a relevance judgment — it is a fixed, inspectable contract)."
  condition: "Any subagent spawn where the role declares one or more domains."
  reason: "Selective inclusion within a declared domain requires the orchestrator to judge which principles are relevant from the task framing — a judgment it cannot make reliably. A missed principle silently degrades the spec or implementation without any signal it was missed. The storage split and the declaration are exempt: neither makes a per-task relevance judgment."

- id: ratify-gate-judgment-vs-knowledge
  rule: "At the ratify gate, ask for each proposal whether it encodes a judgment call (a decision made under uncertainty where context and tradeoffs shaped the outcome) or a knowledge item (something derivable from documentation or training). Surface this distinction with the proposal — the role knows it from the inside. Do not evaluate it as the orchestrator."
  condition: "When presenting principle proposals to the operator at the ratify gate."
  reason: "The corpus's value is captured judgment, not recalled facts. A principle that only returns a lookup when it fires adds reader-tax without adding decision capacity. The role is better positioned to make the knowledge/judgment distinction than the orchestrator because it has the context of how the decision was made. The orchestrator routes this question; it does not answer it."

- id: design-pattern-application-lighter-path
  rule: "When a design task is pattern-application — applying documented vocabulary from the UI or UX library to a new surface, with no genuine visual judgment under uncertainty — prefer the surface-to-operator path over a full designer spawn: read the library, identify the specific gaps, and surface them as targeted questions. Spawn only if the operator's answers reveal that actual design judgment is needed."
  condition: "When a queued task carries concern: visual or concern: interaction with judgment: settled, or when the orchestrator's own read of the task description and context reveals the library already settles the relevant decisions."
  reason: "A full designer spawn loads the lens, all declared domains, and runs the full ratify gate — 20k+ tokens. That cost is justified when there is genuine visual judgment under uncertainty. Applying established patterns to a new surface mostly isn't that: the useful output is which tokens go where, which the library already answers. The lighter path reaches the same place at a fraction of the cost."

- id: domain-assignment-at-ratify-gate
  rule: "At the ratify gate, assign each ratified proposal to a domain and write it there. If no existing domain fits, create a new domain (working file + declaration update on the roles that should load it). If a proposal spans two domains, surface that as a possible domain-boundary problem rather than fragmenting the principle across both."
  condition: "When ratifying a proposal that arrived without a home domain."
  reason: "Proposals surface from work, not from a domain. The gate is the one human-gated point where domain assignment judgment belongs. A split-domain proposal is a signal the boundaries may be wrong — a fork candidate to surface, not a principle to duplicate."

killed:
```
