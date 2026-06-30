# Principle candidates

Extracted by the reading agent from queued sources. Surfaced at the ratify gate
for domains matching the current project's declared domains. Candidates are removed
once ratified or killed.

```yaml
candidates:

- id: hooks-encapsulated-in-custom-hook
  rule: "Confine direct calls to React hooks (useState, useEffect, useCallback, useMemo, etc.) to custom hooks named for the concern they manage, rather than calling them directly inside a component body. The component should consume the custom hook's returned API, not the raw hook primitives."
  condition: "When a component manages a piece of state, an effect, or a derived value via a directly-called React hook for a specific feature concern, rather than through an extracted custom hook (a function named `use*`)."
  reason: "A custom hook is a function — a structural boundary that groups the related state, effects, and handlers of one concern under a single name and exposes a deliberate API to its caller. Raw hook calls scattered through a component force the reader to reconstruct which state and effects belong together; encapsulating them gives the concern a name and lets its internal implementation change without changing how the component uses it."
  domains: [coding-js-react]
  provenance:
    source: https://kyleshevlin.com/use-encapsulation/
    gap: "encapsulation patterns in React hooks — not yet addressed in coding-js-react"
    extracted: 2026-06-30
  see-also: [coordinated-setters-signal-reducer, hook-params-named-for-hook-concern]

- id: named-exports-over-default
  rule: "Prefer named exports over `export default`. Export a binding under the name it's defined with, and import it by that same name."
  condition: "When adding or refactoring a JS/TS module's exports, in any project (this is an ECMAScript module concept, not a stack-agnostic one — see-also note below)."
  reason: "A default export lets every importer choose its own local name for the same binding, so the same value can appear as `Foo`, `foo`, or a typo'd variant across the codebase, and find-references / auto-import tooling has no canonical name to anchor on. Named exports fix the name at the source, so grep and IDE find-references locate every consumer reliably."
  domains: [coding-js-react]
  provenance:
    source: https://github.com/basarat/typescript-book/blob/master/docs/tips/defaultIsBad.md
    gap: "module export naming — naming exports and imports identically makes consumers trivially findable; default exports break this"
    extracted: 2026-06-30
  note: "Queue entry tagged this coding-general, but export default/named export is an ECMAScript module feature with no equivalent in stack-agnostic languages (Python, Go, Rust have no default-export mechanism to compare against) — re-tagged coding-js-react so it only surfaces for web-frontend-pack projects."
```
