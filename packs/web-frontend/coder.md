# Coder overlay — web-frontend pack

This overlays the base coder (`coder.md`). Load it alongside the base for any project whose
`corpora/config.md` declares `role-pack: web-frontend`. It adds JavaScript/TypeScript/React/CSS
conventions and a web-coupled seed corpus. The base coder's prompt and corpus still apply in
full — this only extends them.

## Conventions (extend the base "General conventions")

These are the JS/React instances of the base meta-rule (choose the form that exposes the error)
plus a settled style stance:

- **Block arrow bodies always** (`() => { return value; }`) — `{}` after an arrow is a function
  body, not a value; the concise form has a silent failure mode and forces a per-function
  judgment call.
- **No early returns or guard clauses** — use if/else block bodies. Indentation should encode the
  conditions under which each line runs: an early return lets a line that needs two conditions to be
  true sit at the function's base indentation as if it needs nothing, while if/else puts it where it
  belongs. The guard-clause "exception" also forces a recurring per-function judgment — is this one
  still simple enough? — that a block body removes. And a flat row of guards whose order doesn't
  matter is not a case for keeping them; it is a signal to extract and name the combined condition
  (`const error = validateRequest(req)`), after which if/else costs nothing. Same Crockford /
  Explicit-by-Default lineage as block arrow bodies; it sits in this pack only because some
  ecosystems (e.g. Go) idiomatically prefer guard clauses — the reasoning itself is general.

For project-specific conventions (quotes, type vs interface, hook patterns, import order),
read the project's CLAUDE.md before starting.

## Coder seed corpus (web-frontend)

Provenance, the `promoted:` audit trail, and the kill log live in `coder.audit.md` (in this
pack directory) — loaded only at ratify/retrospective time, never in a coder's working
context. See `kernel.md`, "Storage: working vs audit."

```yaml
last-retrospective: 2026-06-18

principles:

- id: undefined-check-by-source
  rule: "Match the equality operator to the source of the value: optional props (T | undefined) use === undefined / !== undefined; array element access and Array.find() also use !== undefined. Never == null for either."
  condition: "When guarding any value that may be absent — optional props, array element access, or Array.find() results."
  reason: "Strict equality is a common codebase convention. Both sources yield undefined (not null), but distinguishing them by name keeps intent clear. A loose == null silently absorbs both, hiding contract violations."
  status: ratified

- id: null-first-ternary
  rule: "Use null-first ternary (`condition ? null : <Component />`) for conditional rendering; never `condition && <Component />`."
  condition: "Any JSX conditional rendering expression."
  reason: "`&&` returns whichever operand it lands on, not a boolean. A legitimate `0` (e.g. a numeric state value) renders as the literal number 0 on the page instead of rendering nothing. The null-first ternary asks the actual question — is this condition met — rather than whether something is falsy."
  status: ratified

- id: mobile-fixed-bar-bottom-gap
  rule: "Set `bottom: -1px` (not `bottom: 0`) on a mobile fixed bottom bar to prevent a subpixel gap at the bottom of the viewport on some devices."
  condition: "When positioning a fixed bar at the bottom of the viewport on mobile."
  reason: "Subpixel rendering on some devices leaves a 1–2px sliver between bottom: 0 and the screen edge. Overlapping by 1px eliminates it without visible effect."
  status: ratified

- id: imports-before-tailwind-directives
  rule: "When splitting a Tailwind CSS entry file into multiple files imported via @import, put the @import statements before the @tailwind directives."
  condition: "When restructuring Tailwind CSS into multiple files via @import."
  reason: "postcss-import emits one warning per import line per build if @import follows @tailwind. Cascade-order change is inert when no named component class collides on equal specificity with a Tailwind utility — verify this holds before assuming safety."
  status: ratified

- id: tokenize-only-recurring-magic-values
  rule: "When introducing CSS custom properties during a refactor, tokenize only values that recur with the same conceptual meaning. Single-use literals stay inline with a documentary comment citing the spec range if one is defined."
  condition: "When migrating literal CSS values to tokens during a token-introduction refactor."
  reason: "A token for a single consumer is a rename with extra indirection — the value's meaning is clearer inline next to its only use. Token sprawl makes the token file harder to skim."
  status: ratified

- id: css-var-over-mapped-class-for-dynamic-color
  rule: "When a component's fill color must track a CSS custom property that changes based on an ancestor's data attribute, use an inline style (`background: rgb(var(--token))`) rather than a Record mapping prop values to utility class names. Remove the prop entirely once it's no longer needed."
  condition: "Any component with a Record<SomeProp, string> mapping prop values to color utility classes, where those colors are meant to track a CSS custom property set on an ancestor."
  reason: "Utility class names are static strings resolved at build time; inline styles read the computed CSS variable at paint time, so the component correctly responds to ancestor scope changes."
  status: ratified

- id: font-mono-at-element-not-container
  rule: "Apply font-mono to the individual element containing code-register data — not to a wrapper div. A container-wide font-mono forces every child into mono regardless of semantic role, requiring special overrides to correct."
  condition: "Any time font-mono is being placed on a wrapper div rather than on specific text elements inside it."
  reason: "Each element should declare its own register. Container-wide mono is an implicit contract that must be opted out of rather than opted into — the opposite of intentional."
  status: ratified

- id: table-row-color-override
  rule: "To allow row-level text color overrides inside a scoped table, set the base color on the scope's thead (via inheritance) rather than directly on th. A direct `th` selector wins over anything placed on a `<tr>`, but an inherited color from `thead` loses to a class on `<tr>`."
  condition: "When a table scope needs group-level text color overrides on specific header rows."
  reason: "CSS specificity: a direct element selector (`th`) outranks an inherited value from a parent class, so `className` on a `<tr>` can't win. Moving the default to `thead` keeps it as inheritance, which any descendant class can override."
  status: ratified

- id: hook-params-named-for-hook-concern
  rule: "Hook parameters should be named for what the hook does with them, not for the caller's state variable. The mapping from caller concept to hook concept is documentation in the code itself."
  condition: "When a hook accepts a parameter whose name implies the caller's concept but the hook uses it for a different purpose."
  reason: "A param named for the caller's concept is opaque at the callsite — a reader sees useX(isOpen) and has to look inside the hook to understand why open-ness controls data loading. A param named for the hook's concern makes the contract legible without reading the implementation."
  see-also: hook-options-object-for-named-args
  status: ratified

- id: hook-options-object-for-named-args
  rule: "Wrap hook boolean (and other ambiguous primitive) parameters in a single options object so the callsite reads as named arguments."
  condition: "When a hook accepts a boolean or other primitive whose meaning isn't self-evident at the callsite."
  reason: "A bare boolean arg is opaque: useX(true) forces the reader to count positional args. An options object makes the mapping explicit at the callsite: useX({ shouldRefresh: isOpen })."
  see-also: hook-params-named-for-hook-concern
  status: ratified

- id: wizard-callbacks-unconditional
  rule: "When the same screen is reachable via both linear (Next/Back) and non-linear (tab) navigation, wire all core callbacks (onGoToStep, onEdit) unconditionally. Never make a callback conditional on which navigation path was taken."
  condition: "When implementing a wizard where a summary or output screen is reachable via multiple navigation paths."
  reason: "Conditional wiring produces two different capability levels for the same screen. Users who navigate non-linearly should never see a degraded experience compared to those who stepped through sequentially."
  status: ratified
```
