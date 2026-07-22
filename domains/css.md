# Domain: css

CSS / Tailwind authoring and specificity. Declared by the coder lens when `styling` is not `none`
(tailwind, css-modules, vanilla-css, etc.). Audit metadata lives in `domains/audit.md`, loaded only
at ratify/retrospective time.

```yaml
last-retrospective: 2026-06-18

principles:

- id: tokenize-only-recurring-magic-values
  rule: "When introducing CSS custom properties during a refactor, tokenize only values that recur with the same conceptual meaning. Single-use literals stay inline with a documentary comment citing the spec range if one is defined."
  condition: "When migrating literal CSS values to tokens during a token-introduction refactor."
  reason: "A token for a single consumer is a rename with extra indirection — the value's meaning is clearer inline next to its only use. Token sprawl makes the token file harder to skim."

- id: tailwind-extract-component-before-apply
  rule: "When a Tailwind utility pattern needs to be centralized, extract a React component (or template partial) rather than using `@apply`. Reserve `@apply` for contexts where a component abstraction is impossible — CSS-only environments, base-layer overrides for third-party HTML, or legacy non-component templates."
  condition: "When the same set of Tailwind utility classes appears on multiple independent elements in a React codebase and needs to be deduplicated."
  reason: "A React component is a structural boundary that accepts props, renders conditionally, and is tracked by IDE find-references. `@apply` in a CSS file creates a hidden coupling between a class name and a utility set, with no mechanism for props or conditions. Centralizing with a component keeps style and behavior co-located and visible; centralizing with `@apply` creates a second source of truth (markup + stylesheet) that can drift."
  see-also: tailwind-loop-duplication-is-not-a-problem

- id: tailwind-loop-duplication-is-not-a-problem
  rule: "Repeated Tailwind utility strings inside a template loop do not require extraction. The loop body is the single source of truth; runtime duplication across rendered instances is not authoring duplication."
  condition: "When reviewing Tailwind markup and finding the same utility class string in multiple iterations of a `map()`, `for`, or template loop."
  reason: "Extracting a component from a loop to 'remove duplication' creates a component with exactly one callsite — the loop body — adding indirection with no reuse benefit. The authoring-level source of truth is already unique; only the rendered output repeats. The duplication concern that motivates component extraction is when independent elements in different templates share a style — not when one template loop generates identical markup."
  see-also: tailwind-extract-component-before-apply

killed:

- id: mobile-fixed-bar-bottom-gap
  rule: "Set `bottom: -1px` on a mobile fixed bottom bar to prevent a subpixel gap at the bottom of the viewport on some devices."
  kill_type: knowledge
  reason_killed: "CSS browser rendering behavior — a lookup fact, not a judgment call. A coder hits this once via testing, searches it, finds the fix. No project-specific context encoded."

- id: imports-before-tailwind-directives
  rule: "When splitting a Tailwind CSS entry file into multiple files imported via @import, put the @import statements before the @tailwind directives."
  kill_type: knowledge
  reason_killed: "A postcss-import build-warning fact (import-before-directive ordering), not a judgment call — same class as mobile-fixed-bar-bottom-gap and table-row-color-override below. A coder hits the warning once, fixes the ordering, done."

- id: grid-for-layout-flexbox-for-flow
  rule: "Use CSS Grid when elements must align on two axes simultaneously or when their visual order must differ from source order. Use Flexbox when item count is dynamic or when items should size from their own content with the container distributing remaining space."
  kill_type: knowledge
  reason_killed: "Grid-vs-Flexbox use-case selection is close to textbook CSS knowledge, heavily represented in training data — its own audit provenance already recorded `kind: knowledge` at ratification time, which should have screened it out then. Derivable from documentation, not earned project judgment."

- id: table-row-color-override
  rule: "To allow row-level text color overrides inside a scoped table, set the base color on the scope's thead (via inheritance) rather than directly on th."
  kill_type: knowledge
  reason_killed: "CSS specificity: inherited color loses to a direct element selector. Derivable from the CSS spec. Same class as preserve-3d-on-every-ancestor — a spec fact, not a judgment call."
```
