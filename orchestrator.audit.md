# Orchestrator audit record

Provenance and promotions for `skill.md`. Loaded only at ratify/retrospective time — never in
the orchestrator's working context. Keyed by principle `id`. See `kernel.md`, "Storage: working
vs audit." (The kill log lives in `skill.md` so it is available in the working context.)

```yaml
provenance:

- id: brief-ends-at-what
  provenance: "2026-06-01, box-fill calculator box picker. Orchestrator computed SVG coordinates and TypeScript types in the brief, leaving the coder nothing to transcribe."

- id: stop-and-route
  provenance: "2026-06-01, box-fill calculator redesign. Orchestrator entered designer mode and produced the full design spec inline rather than spawning the designer role."

- id: frame-before-routing
  provenance: "2026-06-01, orchestrator corpus setup."

- id: pre-scan-before-spawning
  provenance: "2026-06-02, codebase audit session. Three parallel agents each ran independent discovery; user noted the redundancy."

- id: route-questions-not-roles
  provenance: "2026-06-12, operator feedback: established pipeline caused reflex spawning; question-routing better matches actual cost structure."

- id: surface-design-questions-neutrally
  provenance: "2026-06-12, operator clarified: orchestrator should not drift into design thinking even when capable."

- id: spawn-threshold-is-spec-scope
  provenance: "2026-06-12, operator noted spawn cost often exceeds decision value."

- id: inline-coder-session-protocol
  provenance: "2026-06-17, orchestrator retrospective. Merged from inline-session-enters-coder-role and close-inline-role-at-approval-gate."

- id: design-question-during-coder-session
  provenance: "2026-06-17, orchestrator retrospective."

- id: audit-request-means-spawn-designer
  provenance: "2026-06-13, load calculator audit session — orchestrator implemented operator-listed concerns as code and skipped the designer spawn."

- id: spawn-token-summary
  provenance: "2026-06-19, operator requested visibility after aggregate-only reporting made cost analysis opaque."

- id: full-corpus-on-spawn
  provenance: "2026-06-19, operator rejected selective inclusion after orchestrator proposed it as a cost-reduction strategy."

- id: ratify-gate-judgment-vs-knowledge
  provenance: "2026-06-22, FAMOUS 3D keyboard-key grid ratify session. Orchestrator killed preserve-3d-chain on its own judgment ('a model would know this from training') without routing the distinction to the operator. Post-session reflection surfaced why the role is better positioned to make this call than the orchestrator. Operator confirmed the orchestrator principle is thinner: route the question, don't answer it."

promoted:
```
