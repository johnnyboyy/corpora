# Coder overlay audit record — web-frontend pack

Provenance, promotions, and the kill log for `packs/web-frontend/coder.md`. Loaded only at
ratify/retrospective time — never in a coder's working context. Keyed by principle `id`
(kills carry no id and move wholesale). See `kernel.md`, "Storage: working vs audit."

```yaml
provenance:

- id: undefined-check-by-source
  provenance: "Merged from strict-undefined-check-in-arrays + array-access-undefined-not-null, Blog project, 2026-06-01."

- id: null-first-ternary
  provenance: "2026-06-18, Blog project explicit-by-default post review."

- id: mobile-fixed-bar-bottom-gap
  provenance: "2026-06-03, Blog project Box Selector mobile bottom bar."

- id: imports-before-tailwind-directives
  provenance: "2026-06-12, Blog project globals.css restructure."

- id: tokenize-only-recurring-magic-values
  provenance: "2026-06-12, Blog project globals.css restructure."

- id: css-var-over-mapped-class-for-dynamic-color
  provenance: "2026-06-13, Blog project WireCircle refactor."

- id: font-mono-at-element-not-container
  provenance: "2026-06-13, Blog project FixedBottomResultsBar refactor."

- id: table-row-color-override
  provenance: "2026-06-15, Blog project ampacity table temperature header text color."

- id: hook-params-named-for-hook-concern
  provenance: "2026-06-15, Blog project useHistoryState."

- id: hook-options-object-for-named-args
  provenance: "2026-06-15, Blog project useHistoryState."

- id: wizard-callbacks-unconditional
  provenance: "2026-06-14, Blog project load-calculator, Issue 19."

promoted:
# Conventions that graduated to this overlay's "Conventions" section.

- id: arrow-block-body
  promoted_to: web-frontend coder overlay — "Conventions" section
  provenance: "2026-06-18, Blog project. {} ambiguity + single consistent style removes per-function judgment call. A JS instance of the base prefer-error-exposing-form meta-rule."

- id: no-early-returns
  promoted_to: web-frontend coder overlay — "Conventions" section
  provenance: "2026-06-17, Blog project, 'Explicit by Default' post (content/posts/coding/explicit-by-default.mdx). Derived from Crockford's heuristic, not style: indentation-as-grammar (Henney) means early returns let a multi-condition line sit at base indentation as if unconditional; the guard-clause exception reintroduces a per-function 'still simple enough?' judgment a block body removes; the strong counterexample (a flat row of order-independent guards) resolves to extraction-and-naming, not exception. Scoped to this pack because some ecosystems (Go) idiomatically prefer guard clauses; the reasoning is general."

killed:
```
