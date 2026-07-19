# Domain: design-method (web-frontend pack)

Design *process and discipline* — the clarity/polish priority and documentation rules. A
**convergent** body of correctness guardrails: the anti-mean *stance* is deliberately **not** here —
it is a generative stance, not a principle, and lives on the divergent UI designer lens; mixing it
in was the worked example of the stance hard line (see `kernel.md`, "Generative stance").
Cross-role — declared by both the **ui-designer** and **ux-designer** lenses. Audit metadata lives
in `packs/web-frontend/domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: 2026-06-20

principles:

- id: clarity-over-polish
  rule: "When there is tension between what feels polished and what is immediately clear, prefer clarity. A user must know what to do and how to do it upon seeing any screen — without reading instructions."
  condition: "Any UX decision where aesthetic sophistication and immediate comprehension pull in different directions."
  reason: "Polish optimizes for the observer's impression; clarity optimizes for the user's success. The product's job is the latter."

- id: document-visual-sub-systems
  rule: "When a surface develops a distinct visual language, mark it in the project's design system documentation. How much to document scales with complexity: a self-contained surface unlikely to spawn new design questions gets a boundary note (one paragraph). A surface actively growing or sharing components gets fuller treatment."
  condition: "When a page or section accumulates 3+ design decisions that diverge from the main design system."
  reason: "Undocumented sub-systems let future design work accidentally import the wrong conventions. But over-documenting self-contained surfaces creates a second source of truth that drifts from the code."

- id: documentation-before-screenshots
  rule: "Use the browser automation tool for screenshots only when the design system documentation does not answer the specific question. Documentation is the default; screenshots are the exception."
  condition: "Any time visual information about the current product is needed during a design task."
  reason: "Screenshots are expensive and show a snapshot, not documented intent. The design system documentation is authoritative and answers most questions about what already exists."

- id: progressive-disclosure-for-primary-advanced-split
  rule: "Use progressive disclosure — hiding secondary options behind a reveal mechanism — when there is a clear usage split between what most users need (primary tasks, essential fields) and what a smaller subset needs (advanced options, edge-case settings). Do not use it when all options are needed with similar frequency or when users cannot predict that hidden content exists."
  condition: "When designing an interface — form, settings panel, feature area, or navigation — where controls have noticeably unequal usage frequency and the low-frequency set is large enough to create cognitive overhead."
  reason: "Showing all options at once imposes equal cognitive cost on all users, including the majority who only ever need a subset. Progressive disclosure reduces visual complexity for the common case. The cost is discoverability: users who need the hidden options must be able to predict they exist and find the trigger. When that predictability cannot be ensured — because the label is ambiguous or the option is needed by most users — the disclosure mechanism becomes an obstacle."
  see-also: forms-reveal-conditional-fields

killed:
```
