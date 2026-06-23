# Domain: design-method (web-frontend pack)

Design *process and discipline* — the clarity/polish priority and documentation rules. A
**convergent** body of correctness guardrails. The anti-mean *stance* is deliberately **not** here:
it is a generative stance, not a principle, and lives on the divergent UI designer lens (see
`kernel.md`, "Generative stance"). Mixing it in here was the worked example of the stance hard line —
a "resist the standard" instruction cannot share a domain with "prefer the clear/standard answer"
rules. Cross-role — declared by both the **ui-designer** and **ux-designer** lenses. Provenance and
per-kill audit detail live in `packs/web-frontend/domains/audit.md`, loaded only at
ratify/retrospective time. See `kernel.md`.

```yaml
last-retrospective: 2026-06-20

principles:

- id: clarity-over-polish
  rule: "When there is tension between what feels polished and what is immediately clear, prefer clarity. A user must know what to do and how to do it upon seeing any screen — without reading instructions."
  condition: "Any UX decision where aesthetic sophistication and immediate comprehension pull in different directions."
  reason: "Polish optimizes for the observer's impression; clarity optimizes for the user's success. The product's job is the latter."
  status: ratified

- id: document-visual-sub-systems
  rule: "When a surface develops a distinct visual language, mark it in the project's design system documentation. How much to document scales with complexity: a self-contained surface unlikely to spawn new design questions gets a boundary note (one paragraph). A surface actively growing or sharing components gets fuller treatment."
  condition: "When a page or section accumulates 3+ design decisions that diverge from the main design system."
  reason: "Undocumented sub-systems let future design work accidentally import the wrong conventions. But over-documenting self-contained surfaces creates a second source of truth that drifts from the code."
  status: ratified

- id: documentation-before-screenshots
  rule: "Use the browser automation tool for screenshots only when the design system documentation does not answer the specific question. Documentation is the default; screenshots are the exception."
  condition: "Any time visual information about the current product is needed during a design task."
  reason: "Screenshots are expensive and show a snapshot, not documented intent. The design system documentation is authoritative and answers most questions about what already exists."
  status: ratified

killed:
```
