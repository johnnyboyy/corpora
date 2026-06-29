# Domain: css (web-frontend pack)

CSS / Tailwind authoring and specificity. Declared by the coder lens when `role-pack: web-frontend`.
Provenance, promotions, and per-kill audit detail live in `packs/web-frontend/domains/audit.md`,
loaded only at ratify/retrospective time. See `kernel.md`, "Storage: working vs audit."

```yaml
last-retrospective: 2026-06-18

principles:

- id: mobile-fixed-bar-bottom-gap
  rule: "Set `bottom: -1px` (not `bottom: 0`) on a mobile fixed bottom bar to prevent a subpixel gap at the bottom of the viewport on some devices."
  condition: "When positioning a fixed bar at the bottom of the viewport on mobile."
  reason: "Subpixel rendering on some devices leaves a 1–2px sliver between bottom: 0 and the screen edge. Overlapping by 1px eliminates it without visible effect."

- id: imports-before-tailwind-directives
  rule: "When splitting a Tailwind CSS entry file into multiple files imported via @import, put the @import statements before the @tailwind directives."
  condition: "When restructuring Tailwind CSS into multiple files via @import."
  reason: "postcss-import emits one warning per import line per build if @import follows @tailwind. Cascade-order change is inert when no named component class collides on equal specificity with a Tailwind utility — verify this holds before assuming safety."

- id: tokenize-only-recurring-magic-values
  rule: "When introducing CSS custom properties during a refactor, tokenize only values that recur with the same conceptual meaning. Single-use literals stay inline with a documentary comment citing the spec range if one is defined."
  condition: "When migrating literal CSS values to tokens during a token-introduction refactor."
  reason: "A token for a single consumer is a rename with extra indirection — the value's meaning is clearer inline next to its only use. Token sprawl makes the token file harder to skim."

- id: table-row-color-override
  rule: "To allow row-level text color overrides inside a scoped table, set the base color on the scope's thead (via inheritance) rather than directly on th. A direct `th` selector wins over anything placed on a `<tr>`, but an inherited color from `thead` loses to a class on `<tr>`."
  condition: "When a table scope needs group-level text color overrides on specific header rows."
  reason: "CSS specificity: a direct element selector (`th`) outranks an inherited value from a parent class, so `className` on a `<tr>` can't win. Moving the default to `thead` keeps it as inheritance, which any descendant class can override."

killed:
```
