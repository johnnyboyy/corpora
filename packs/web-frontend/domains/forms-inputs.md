# Domain: forms-inputs (web-frontend pack)

Input fields and their default/empty/derived states. Cross-role — declared by both the
**ux-designer** and **ui-designer** lenses. Audit metadata lives in
`packs/web-frontend/domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: 2026-06-20

principles:

- id: numeric-inputs-start-empty-not-zero
  rule: "Numeric fields that require deliberate user input should start empty (null/blank), not pre-filled with 0."
  condition: "When a numeric input controls a core calculation variable and 0 is indistinguishable from 'the user entered zero intentionally' vs. 'the user hasn't filled this in yet.'"
  reason: "A 0 in a rendered input looks like a completed field. Starting empty puts the field in an obviously-unfilled state that matches the user's mental model of what still needs to be done."

- id: zero-count-orphan-rows
  rule: "When a new row is added via 'Add X', it defaults to count 1 (or is visually marked as unconfigured) — never a 0-count orphan in the list."
  condition: "When a list allows adding items with a quantity field."
  reason: "A 0-count row contributes nothing and creates visual clutter; it implies the user forgot to fill it in."

- id: unified-field-over-derived-dual-fields
  rule: "When two fields are conceptually redundant — one derivable from the other — expose only the field that matches the user's mental model. Derive the internal value in the calculation layer."
  condition: "When the data model has two fields representing the same user decision at different abstraction levels."
  reason: "The data model is allowed to be verbose; the UI should not be. Forcing users to translate between their vocabulary and the system's internal model creates confusion and opens the risk of the two fields contradicting each other."

- id: persistent-controls-not-conditional
  rule: "A field that is always semantically meaningful must always be visible, even if its effect on the output varies by context. Do not confuse effect-level variation with concept-level inapplicability."
  condition: "When a control disappears based on another field's value, but the underlying concept still applies regardless."
  reason: "Hiding a control because its effect on a specific calculation varies is wrong — that's an internal implementation concern leaking into the UI. A control that disappears as the user changes a sibling field is disorienting."

killed:
```
