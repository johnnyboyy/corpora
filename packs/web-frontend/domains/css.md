# Domain: css (web-frontend pack)

CSS / Tailwind authoring and specificity. Declared by the coder lens when `role-pack: web-frontend`.
Audit metadata lives in `packs/web-frontend/domains/audit.md`, loaded only at ratify/retrospective
time.

```yaml
last-retrospective: 2026-06-18

principles:

- id: imports-before-tailwind-directives
  rule: "When splitting a Tailwind CSS entry file into multiple files imported via @import, put the @import statements before the @tailwind directives."
  condition: "When restructuring Tailwind CSS into multiple files via @import."
  reason: "postcss-import emits one warning per import line per build if @import follows @tailwind. Cascade-order change is inert when no named component class collides on equal specificity with a Tailwind utility — verify this holds before assuming safety."

- id: tokenize-only-recurring-magic-values
  rule: "When introducing CSS custom properties during a refactor, tokenize only values that recur with the same conceptual meaning. Single-use literals stay inline with a documentary comment citing the spec range if one is defined."
  condition: "When migrating literal CSS values to tokens during a token-introduction refactor."
  reason: "A token for a single consumer is a rename with extra indirection — the value's meaning is clearer inline next to its only use. Token sprawl makes the token file harder to skim."

killed:

- id: mobile-fixed-bar-bottom-gap
  rule: "Set `bottom: -1px` on a mobile fixed bottom bar to prevent a subpixel gap at the bottom of the viewport on some devices."
  kill_type: knowledge
  reason_killed: "CSS browser rendering behavior — a lookup fact, not a judgment call. A coder hits this once via testing, searches it, finds the fix. No project-specific context encoded."

- id: table-row-color-override
  rule: "To allow row-level text color overrides inside a scoped table, set the base color on the scope's thead (via inheritance) rather than directly on th."
  kill_type: knowledge
  reason_killed: "CSS specificity: inherited color loses to a direct element selector. Derivable from the CSS spec. Same class as preserve-3d-on-every-ancestor — a spec fact, not a judgment call."
```
