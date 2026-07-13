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

- id: prefers-reduced-motion-requires-js-hook
  rule: "For JS-driven animations, detect `prefers-reduced-motion` via a custom hook reading `window.matchMedia('(prefers-reduced-motion: reduce)')` and subscribing to its `change` event. Apply the result to conditionally set duration to zero or skip the animation call. Do not rely on CSS media query overrides alone."
  condition: "When implementing any animation whose parameters — duration, keyframes, or whether it fires at all — are configured in JavaScript, including use of Framer Motion, React Spring, GSAP, or manual Web Animations API calls."
  reason: "CSS `@media (prefers-reduced-motion: reduce)` only overrides CSS animation and transition properties. JS animation libraries read configuration from JS objects at runtime; no CSS rule can reach those values. A hook reading `window.matchMedia` is the only way to honor the OS preference for JS-controlled animations. Subscribing to the `change` event rather than reading once at mount ensures the preference stays current if the user toggles the OS setting during the session."
  domains: [motion, coding-js-react]
  provenance:
    source: https://www.joshwcomeau.com/react/prefers-reduced-motion/
    gap: "motion domain has no principles about prefers-reduced-motion; both existing principles assume motion is appropriate for all users"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403 and web search was unavailable; extracted from training-data knowledge of this well-known article."
  see-also: [motion-as-accent]

- id: reduced-motion-instant-not-absent
  rule: "When `prefers-reduced-motion` is active, make state-communicating animations instant (duration → 0) rather than absent. Remove only decorative or continuous motion (auto-playing loops, parallax, background animations) entirely."
  condition: "When adapting animations for the `prefers-reduced-motion` preference. The instant-vs-absent distinction applies to: instant for animations that communicate a state change (item appearing, being removed, reordering); remove entirely for animations that exist only for visual interest with no functional role."
  reason: "An animation communicating a state change (an item appearing or being removed) conveys meaning through its endpoint, not its motion. Removing it entirely causes the UI to jump without context, which can be as disorienting as the motion itself. Setting duration to zero delivers the same endpoint with no motion. Decorative animations serve no function and add no clarity when instant — they should be removed."
  domains: [motion]
  provenance:
    source: https://www.joshwcomeau.com/react/prefers-reduced-motion/
    gap: "motion domain has no principles about prefers-reduced-motion; both existing principles assume motion is appropriate for all users"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403 and web search was unavailable; extracted from training-data knowledge of this well-known article."
  see-also: [motion-as-accent]

- id: optimistic-ui-for-high-confidence-mutations
  rule: "Apply optimistic UI (show assumed-success state immediately) only for mutations where server failure is rare and a visible rollback carries low cost — toggles, likes, reorders, non-destructive inline updates. Do not use optimistic UI for destructive actions, payment flows, or any mutation whose failure would require significant user re-entry."
  condition: "When deciding whether to apply optimistic state patterns (React 19 `useOptimistic`, or manual optimistic state) to a user-triggered server mutation."
  reason: "Optimistic UI trades accuracy for perceived speed. The pattern earns its keep when the assumed-success is almost always correct — the rare rollback is a minor correction. When failure is plausible (a payment that might decline, a delete that might conflict), a visible rollback is disorienting: the user briefly sees success, then it reverses. Worse, a user who misreads the rollback as success stops retrying. The optimistic assumption must be safe to make."
  domains: [coding-js-react, recoverability]
  provenance:
    source: https://dev.to/a1guy/react-19-useoptimistic-deep-dive-building-instant-resilient-and-user-friendly-uis-49fp
    gap: "recoverability domain covers destructive-action recovery but has no principles about optimistic UI — showing assumed success before server confirmation and auto-rolling back on failure"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of React 19 useOptimistic API and standard optimistic UI patterns."
  see-also: [recovery-path-replaces-confirmation]

- id: optimistic-rollback-requires-explicit-error
  rule: "When an optimistic UI mutation fails and state rolls back to its pre-action value, always surface an explicit error message. Never let the visual rollback be the sole signal of failure."
  condition: "When implementing any optimistic state pattern — including React 19 `useOptimistic` — where the state reverts on a failed async action."
  reason: "A state rollback with no error message is experienced as a mysterious 'snap-back': the UI briefly showed the new state, then silently returned to the old one. The user doesn't know if the action failed, is still pending, or partially succeeded — and whether they should retry. An explicit error closes the gap between what happened internally and what the user knows happened, and makes retry decisions possible."
  domains: [coding-js-react, recoverability]
  provenance:
    source: https://dev.to/a1guy/react-19-useoptimistic-deep-dive-building-instant-resilient-and-user-friendly-uis-49fp
    gap: "recoverability domain covers destructive-action recovery but has no principles about optimistic UI — showing assumed success before server confirmation and auto-rolling back on failure"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of React 19 useOptimistic API and standard optimistic UI patterns."
  see-also: [recovery-path-replaces-confirmation, optimistic-ui-for-high-confidence-mutations]

- id: semantic-tokens-required-for-theme-switching
  rule: "Any color token system that must support dark mode or theme switching needs at least two tiers: a primitive tier (raw values, e.g. `--color-blue-500: oklch(...)`) and a semantic tier (role-named aliases, e.g. `--color-action-primary: var(--color-blue-500)`). Theme switching redefines only semantic token values. Components reference only semantic tokens."
  condition: "When building or refactoring a token system where the same component must display correctly across two or more color themes (light/dark, brand variants)."
  reason: "If components reference primitive tokens directly, switching themes requires updating every component that uses any color. A semantic layer decouples 'what role does this color serve?' from 'what is the value for that role in this theme?' — theme switching becomes a single redefinition of the semantic tier, with no component changes needed."
  domains: [color, css]
  provenance:
    source: https://www.smashingmagazine.com/2024/05/naming-best-practices/
    gap: "color domain has no principles about dark mode token architecture; tokenize-only-recurring-magic-values in css covers when to tokenize but not how to name tokens for theme-switching"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of this well-known Smashing Magazine article on design token naming."
  see-also: [tokenize-only-recurring-magic-values]

- id: semantic-token-names-by-role-not-value
  rule: "Semantic token names must describe the color's role or purpose, never its visual appearance. Use `--color-text-danger`, `--color-surface-interactive`, `--color-border-subtle` — never `--color-red-text`, `--color-light-gray-bg`."
  condition: "When naming any token in the semantic tier of a design token system — tokens that map a purpose to a value, as opposed to primitive tokens that simply name a raw value."
  reason: "A name like `--color-red-text` encodes both the role and the current value. If the brand's danger color changes from red to orange, every reference to the token is now semantically wrong — the name claims 'red' but it isn't. A role-based name like `--color-text-danger` remains correct regardless of what value it maps to. Role names also survive dark-mode redefinition: the purpose is stable; only the value changes."
  domains: [color, css]
  provenance:
    source: https://www.smashingmagazine.com/2024/05/naming-best-practices/
    gap: "color domain has no principles about dark mode token architecture; tokenize-only-recurring-magic-values in css covers when to tokenize but not how to name tokens for theme-switching"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of this well-known Smashing Magazine article on design token naming."
  see-also: [tokenize-only-recurring-magic-values, semantic-tokens-required-for-theme-switching]

- id: tailwind-extract-component-before-apply
  rule: "When a Tailwind utility pattern needs to be centralized, extract a React component (or template partial) rather than using `@apply`. Reserve `@apply` for contexts where a component abstraction is impossible — CSS-only environments, base-layer overrides for third-party HTML, or legacy non-component templates."
  condition: "When the same set of Tailwind utility classes appears on multiple independent elements in a React codebase and needs to be deduplicated."
  reason: "A React component is a structural boundary that accepts props, renders conditionally, and is tracked by IDE find-references. `@apply` in a CSS file creates a hidden coupling between a class name and a utility set, with no mechanism for props or conditions. Centralizing with a component keeps style and behavior co-located and visible; centralizing with `@apply` creates a second source of truth (markup + stylesheet) that can drift."
  domains: [css, coding-js-react]
  provenance:
    source: https://tailwindcss.com/docs/reusing-styles
    gap: "css domain has no principle about when to accept utility class duplication vs extract a component or use @apply — a recurrent Tailwind decision"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of the Tailwind CSS official documentation on reusing styles."

- id: tailwind-loop-duplication-is-not-a-problem
  rule: "Repeated Tailwind utility strings inside a template loop do not require extraction. The loop body is the single source of truth; runtime duplication across rendered instances is not authoring duplication."
  condition: "When reviewing Tailwind markup and finding the same utility class string in multiple iterations of a `map()`, `for`, or template loop."
  reason: "Extracting a component from a loop to 'remove duplication' creates a component with exactly one callsite — the loop body — adding indirection with no reuse benefit. The authoring-level source of truth is already unique; only the rendered output repeats. The duplication concern that motivates component extraction is when independent elements in different templates share a style — not when one template loop generates identical markup."
  domains: [css, coding-js-react]
  provenance:
    source: https://tailwindcss.com/docs/reusing-styles
    gap: "css domain has no principle about when to accept utility class duplication vs extract a component or use @apply — a recurrent Tailwind decision"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of the Tailwind CSS official documentation on reusing styles."
  see-also: [tailwind-extract-component-before-apply]

- id: progressive-disclosure-for-primary-advanced-split
  rule: "Use progressive disclosure — hiding secondary options behind a reveal mechanism — when there is a clear usage split between what most users need (primary tasks, essential fields) and what a smaller subset needs (advanced options, edge-case settings). Do not use it when all options are needed with similar frequency or when users cannot predict that hidden content exists."
  condition: "When designing an interface — form, settings panel, feature area, or navigation — where controls have noticeably unequal usage frequency and the low-frequency set is large enough to create cognitive overhead."
  reason: "Showing all options at once imposes equal cognitive cost on all users, including the majority who only ever need a subset. Progressive disclosure reduces visual complexity for the common case. The cost is discoverability: users who need the hidden options must be able to predict they exist and find the trigger. When that predictability cannot be ensured — because the label is ambiguous or the option is needed by most users — the disclosure mechanism becomes an obstacle."
  domains: [design-method, forms-inputs]
  provenance:
    source: https://www.nngroup.com/articles/progressive-disclosure/
    gap: "design-method domain has no principle about when to use progressive disclosure vs showing all options upfront — a core information architecture decision"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of this NNGroup article."

- id: forms-reveal-conditional-fields
  rule: "In a form, reveal fields only when a prior answer makes them relevant. Do not show conditional fields disabled or grayed out; keep them hidden until the condition is met, then show them as active."
  condition: "When a form has fields whose relevance depends on the value of a sibling field — for example, a billing-address section that only applies when 'different from shipping address' is selected, or a 'specify other' field that appears only when 'Other' is chosen."
  reason: "A form that shows all conditional fields — even disabled — forces every user to parse and consciously skip irrelevant content. This creates confusion (why is this grayed out?), implies the field may later matter, and makes the form appear longer and more complex than the user's actual task requires. Revealing fields on demand minimizes apparent complexity and matches form length to the user's actual data-entry needs. Contrast with `persistent-controls-not-conditional`: that principle covers fields that are always conceptually relevant but vary in effect — this covers fields that are genuinely inapplicable until a prior condition is met."
  domains: [forms-inputs, design-method]
  provenance:
    source: https://www.nngroup.com/articles/progressive-disclosure/
    gap: "design-method domain has no principle about when to use progressive disclosure vs showing all options upfront — a core information architecture decision"
    extracted: 2026-07-06
    fetch-note: "Source URL returned 403; extracted from training-data knowledge of this NNGroup article."
  see-also: [progressive-disclosure-for-primary-advanced-split, persistent-controls-not-conditional]

- id: module-boundaries-precede-deployment-separation
  rule: "Before splitting code into separately-deployed services or packages, verify that the equivalent module boundaries are already clean in the existing codebase — no cycles, no cross-module access to internals. Deploy the boundary only after the code already respects it."
  condition: "When planning a migration from a monolith to microservices, separate repositories, or separately-deployed packages — at the point of deciding whether the split is ready to make."
  reason: "Deployment separation enforces physical isolation; it cannot create logical isolation. If module A depends on module B's internal functions rather than its exported API, the same entanglement persists after separation as a network call or inter-package import. The coupling is not resolved — it is made harder to refactor. Physical separation of clean logical boundaries is a deployment decision; separation of entangled code instantiates the coupling as a distributed-systems dependency."
  domains: [coding-general]
  provenance:
    source: https://www.youtube.com/watch?v=4qfsmE11Ejo
    gap: "coding-general has principles about code placement at the file/module level but none about when to establish and enforce module boundary contracts — when internal dependencies are clean enough to justify separation"
    extracted: 2026-07-13
  see-also: [code-lives-at-consumer-level]

- id: dependency-graph-over-architecture-diagrams
  rule: "When auditing or enforcing architectural boundaries, derive them from the actual import/dependency graph of the code, not from architectural diagrams or intent statements."
  condition: "When verifying that two modules are genuinely isolated — before any structural separation such as package extraction, service split, or repository division — or when a stated architecture diverges from observed runtime or import behavior."
  reason: "An architecture diagram captures intent, not implementation. Two modules can be depicted as isolated boxes with a single interface arrow while one has twelve files importing from eight internal files of the other. The dependency graph is always current; a diagram is only current until the next unreviewed commit. If clean boundaries are the goal, the test is the dependency graph — a diagram that agrees with it is a summary, not evidence."
  domains: [coding-general]
  provenance:
    source: https://www.youtube.com/watch?v=4qfsmE11Ejo
    gap: "coding-general has principles about code placement at the file/module level but none about when to establish and enforce module boundary contracts — when internal dependencies are clean enough to justify separation"
    extracted: 2026-07-13
  see-also: [code-lives-at-consumer-level, module-boundaries-precede-deployment-separation]

- id: validate-on-blur-then-on-change
  rule: "Validate a field on `blur` the first time the user leaves it. Once the field is in an error state, switch to `change` events so corrections are acknowledged immediately. Never show validation errors while the user is still typing in a field that has not yet been in error."
  condition: "When implementing inline form validation — specifically choosing which DOM event (`blur`, `change`, `input`, `submit`) triggers showing a field-level error message."
  reason: "On-change validation that fires before a field has ever errored is accusatory — it flags the user as wrong before they have finished entering a value. On-blur waits for the user to declare they are done with a field, which is the earliest natural moment for a correctness check. Once an error has already been shown, on-change feedback is helpful rather than accusatory: the user is now attempting to fix a known problem and deserves immediate acknowledgment of their corrections. Research shows blur-first validation reduces error rates versus submit-time validation without increasing form completion time."
  domains: [forms-inputs, validation-feedback]
  provenance:
    source: https://www.smashingmagazine.com/2022/09/inline-validation-web-forms-ux/
    gap: "forms-inputs covers default/empty states and persistent controls but has no principle about validation timing — when to show errors relative to user input events (on blur vs. on change vs. on submit)"
    extracted: 2026-07-13
    fetch-note: "Source URL returned 403; extracted from search-result summaries of this well-known Smashing Magazine article and corroborating UX research."
  see-also: [warning-colocated-with-resolution]

- id: discriminated-union-for-mutually-exclusive-props
  rule: "When a component has N variants whose prop sets are mutually exclusive, model the prop type as a discriminated union, not a flat interface with optional fields. Each union member carries the discriminant field and the props that are required — not optional — for that variant."
  condition: "When designing or refactoring the TypeScript prop interface of a component that has two or more distinct usage modes, each requiring different props, where mixing props from two modes should be a compile-time error."
  reason: "A flat interface with all variant props marked optional allows every combination, including impossible ones (icon and label together, or neither). TypeScript cannot flag these because all props are optional. A discriminated union narrows props at every discriminant check site, makes each variant's required fields explicit, and forces call sites to handle a new variant when one is added — exhaustiveness checks surface missing cases at compile time, not at runtime."
  domains: [coding-js-react]
  provenance:
    source: https://www.developerway.com/posts/advanced-typescript-for-react-developers-discriminated-unions
    gap: "coding-js-react covers state management patterns (useReducer, refs) and hook encapsulation but has no principle about TypeScript type design for component props with mutually exclusive variants"
    extracted: 2026-07-13
    fetch-note: "Source URL returned 403; extracted from search-result summaries of this article and closely related sources (Total TypeScript, oneuptime.com Jan 2026)."
  see-also: [unified-representation-no-type-leakage]

- id: grid-for-layout-flexbox-for-flow
  rule: "Use CSS Grid when elements must align on two axes simultaneously or when their visual order must differ from source order. Use Flexbox when item count is dynamic or when items should size from their own content with the container distributing remaining space."
  condition: "When choosing between `display: grid` and `display: flex` for a new layout container."
  reason: "The two models have opposite starting points: Flexbox is content-outward (the container adapts to its items' content; remaining space is then distributed) and Grid is layout-inward (tracks are declared first; items are placed into them, independently of source order). Using Grid where content-first sizing is needed forces explicit track definitions for what could be automatic; using Flexbox where two-axis alignment is needed requires nested containers or duplicate sizing rules. Match the model to what the layout actually requires."
  domains: [css]
  provenance:
    source: https://blog.logrocket.com/css-flexbox-vs-css-grid/
    gap: "css domain has no layout methodology principle — when to choose flexbox vs. grid is a recurrent structural decision with no guidance in the corpus"
    extracted: 2026-07-13
    fetch-note: "Source URL returned 403; extracted from search-result summaries of multiple 2025–2026 sources on this topic."
```
