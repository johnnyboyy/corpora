# Domain: design-method

Design *process and discipline* — the clarity/polish priority and documentation rules. A
**convergent** body of correctness guardrails: the anti-mean *stance* is deliberately **not** here —
it is a generative stance, not a principle, and lives on the divergent stance itself (see
`kernel.md`, "Generative stance"); mixing it in was the worked example of the stance hard line.
Loaded by both a UX-composed spawn (`wizards-flows`, `ranking-evaluation`, `validation-feedback`,
`recoverability`, `lists-selection`, `forms-inputs`, convergent) and a UI-composed spawn (`color`,
`surfaces-elevation`, `visual-hierarchy`, `motion`, `validation-feedback`, `recoverability`,
`lists-selection`, `forms-inputs`, divergent). Audit metadata lives in `domains/audit.md`, loaded
only at ratify/retrospective time.

A design spec is iterated on a scale — awful → bad → good → great → perfect — rather than judged
pass/fail. Target great; perfect is aspirational, not a bar every spec must clear before shipping.

Read the project's UI or UX library first — authoritative for current visual character and
experience patterns respectively; do not re-derive either from code or screenshots. If the relevant
library doesn't exist yet, the project needs the founding `bootstrap-ui`/`bootstrap-ux` pass first,
not ongoing design work.

A UX-composed spawn's output is a user flow spec: current experience, proposed flow per step (what's
seen, actions available, system response, error/empty/edge cases), clarity requirements. Describe
what the user perceives and does — never visual layout, styling, colors, or typography; that is a
UI-composed spawn's job. Most proposals are `kind: judgment`; a genuine direction question
mid-work is `status: questions-pending`, never a silent assumption.

A UI-composed spawn's output is a design spec: current state, proposed design per UI state
(elements, layout, hierarchy, interaction behavior, empty/loading/selected/error states). Describe
proportions in relative terms — no pixel values, no CSS class names, no component names;
implementation is not this spawn's concern. Ground visual decisions in a UX flow spec when one was
provided. Most proposals are `kind: direction` (filed to the UI library, not a domain) — a
divergent spawn's output is an identity choice, not a weighable rule; name every screen a spec
changes in `ui-drift.screens` and every shared component it changes in `ui-drift.components`.

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
  rule: "Consult the screenshot cache (`corpora/screenshots/manifest.md`) freely for orientation and reuse-discovery — reading it costs nothing new. Reach for the browser automation tool for a fresh capture only when the cache is missing or stale for a screen you need, or to verify aesthetic quality the text documentation can't fully characterize. Documented specification remains the default source of truth for exact values."
  condition: "Any time visual information about the current product is needed during a design task."
  reason: "Reading cached images is normal now — the cache already paid its capture cost at handoff time, so re-reading it is free. Live capture stays the exception: it still repeats the token cost the design system documentation exists to avoid, and shows a snapshot rather than documented intent."

- id: check-existing-patterns-before-specifying-new
  rule: "Before specifying a new flow pattern, navigation convention, or UI component, check the project's UX/UI library and existing component documentation for one that already covers the need."
  condition: "Any design spec that introduces a flow step, interaction pattern, or visual component not already named in the project's library documentation."
  reason: "A design spec is read by a coder who implements it as written. Specifying a near-duplicate of an existing pattern creates two conventions where one would do, and the coder has no way to know a simpler existing option was available — the check has to happen at design time, not implementation time."

killed:
```
