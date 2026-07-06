# Domain: lists-selection (web-frontend pack)

Lists, rows, and active/selected item treatment. Cross-role — declared by both the **ux-designer**
and **ui-designer** lenses. Audit metadata lives in `packs/web-frontend/domains/audit.md`, loaded
only at ratify/retrospective time.

```yaml
last-retrospective: 2026-06-20

principles:

- id: indicator-weight-matches-job
  rule: "When an active-item indicator is the primary way a user orients themselves in a low-differentiation list, it must carry enough visual weight to be the first thing the eye finds. Subtle indicators that work as secondary signals in rich-content lists are insufficient when items have little visual differentiation."
  condition: "When an active/selected indicator must orient the user in a list where items have low visual differentiation — e.g., all items show only timestamps."
  reason: "A dot works as a secondary signal when items have rich content to anchor it. In a sparse list, the dot can read as decoration. Full-row treatment is the established selection affordance users already know."

- id: active-row-is-inert
  rule: "The currently active entry in a selection list must suppress its hover state and produce no action on click. Do not give the active row an interactive cursor or hover background."
  condition: "When a list allows switching the active item by clicking a row, and one row represents the currently active item."
  reason: "An interactive hover state on the active row implies that clicking does something. When nothing happens, the user loses confidence in the UI. Inert treatment communicates 'you are already here' without needing to explain it."

- id: section-level-explanation-not-row-level
  rule: "Explanatory tooltips or help text that apply uniformly to all rows in a list belong on the section header, not repeated per row."
  condition: "When every row in a repeatable list carries the same info tooltip with identical content. Does not apply when tooltip content is row-specific."
  reason: "Per-row repetition of identical explanatory content adds visual noise without adding information. A single tooltip on the section heading correctly signals that the concept applies to the section as a class."

killed:
```
