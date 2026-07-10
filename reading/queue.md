# Reading queue

Sources queued by the discovery agent, awaiting the reading agent.
Format: url, domains, gap addressed, status (unread | read), source (discovery | manual).

```yaml
queue:

- id: shevlin-use-encapsulation
  url: https://kyleshevlin.com/use-encapsulation
  domains: [coding-js-react]
  gap: "encapsulation patterns in React hooks — not yet addressed in coding-js-react"
  status: read
  read: 2026-06-30
  candidates: 1
  added: 2026-06-29
  source: manual

- id: export-default-mistake
  url: https://github.com/basarat/typescript-book/blob/master/docs/tips/defaultIsBad.md
  domains: [coding-general]
  gap: "module export naming — naming exports and imports identically makes consumers trivially findable; default exports break this"
  status: read
  read: 2026-06-30
  candidates: 1
  added: 2026-06-29
  source: manual
  note: "URL needed. Argument: export default lets importers choose any name, obscuring consumers. Named exports enforce consistent naming."

- id: joshwcomeau-prefers-reduced-motion
  url: https://www.joshwcomeau.com/react/prefers-reduced-motion/
  domains: [motion, coding-js-react]
  gap: "motion domain has no principles about prefers-reduced-motion; both existing principles assume motion is appropriate for all users"
  status: read
  read: 2026-07-06
  candidates: 2
  added: 2026-07-03
  source: discovery
  fetch-note: "URL returned 403; candidates extracted from training-data knowledge of this well-known article."

- id: react-useoptimistic-deep-dive
  url: https://dev.to/a1guy/react-19-useoptimistic-deep-dive-building-instant-resilient-and-user-friendly-uis-49fp
  domains: [coding-js-react, recoverability]
  gap: "recoverability domain covers destructive-action recovery but has no principles about optimistic UI — showing assumed success before server confirmation and auto-rolling back on failure"
  status: read
  read: 2026-07-06
  candidates: 2
  added: 2026-07-03
  source: discovery
  fetch-note: "URL returned 403; candidates extracted from training-data knowledge of React 19 useOptimistic and standard optimistic UI patterns."

- id: smashing-design-token-naming
  url: https://www.smashingmagazine.com/2024/05/naming-best-practices/
  domains: [color, css]
  gap: "color domain has no principles about dark mode token architecture; tokenize-only-recurring-magic-values in css covers when to tokenize but not how to name tokens for theme-switching"
  status: read
  read: 2026-07-06
  candidates: 2
  added: 2026-07-03
  source: discovery
  fetch-note: "URL returned 403; candidates extracted from training-data knowledge of this well-known Smashing Magazine article."

- id: tailwind-reusing-styles
  url: https://tailwindcss.com/docs/reusing-styles
  domains: [css, coding-js-react]
  gap: "css domain has no principle about when to accept utility class duplication vs extract a component or use @apply — a recurrent Tailwind decision"
  status: read
  read: 2026-07-06
  candidates: 2
  added: 2026-07-03
  source: discovery
  fetch-note: "URL returned 403; candidates extracted from training-data knowledge of the Tailwind CSS official documentation on reusing styles."

- id: nngroup-progressive-disclosure
  url: https://www.nngroup.com/articles/progressive-disclosure/
  domains: [design-method, forms-inputs]
  gap: "design-method domain has no principle about when to use progressive disclosure vs showing all options upfront — a core information architecture decision"
  status: read
  read: 2026-07-06
  candidates: 2
  added: 2026-07-03
  source: discovery
  fetch-note: "URL returned 403; candidates extracted from training-data knowledge of this NNGroup article."

- id: henney-modular-monoliths-ndc2026
  url: https://www.youtube.com/watch?v=4qfsmE11Ejo
  domains: [coding-general]
  gap: "coding-general has principles about code placement at the file/module level but none about when to establish and enforce module boundary contracts — when internal dependencies are clean enough to justify separation"
  status: unread
  added: 2026-07-10
  source: discovery
  author-note: "Listed author (Kevlin Henney), NDC London 2026. Core arguments from search summaries: 'Modularity is not a deployment choice; it is an architectural discipline.' 'If you cannot draw clean internal boundaries, you are not ready for microservices.' 'Dependencies reveal your real architecture better than diagrams.' Bypasses topic-match; argument density confirmed."

- id: smashing-inline-validation-ux
  url: https://www.smashingmagazine.com/2022/09/inline-validation-web-forms-ux/
  domains: [forms-inputs, validation-feedback]
  gap: "forms-inputs covers default/empty states and persistent controls but has no principle about validation timing — when to show errors relative to user input events (on blur vs. on change vs. on submit)"
  status: unread
  added: 2026-07-10
  source: discovery
  fetch-note: "URL returned 403; argument extracted from search result summaries. Core claim: validate on blur on first field interaction; switch to on-change only when the field is already in an error state. Because: on-change validation before an error has occurred feels accusatory — telling users they are wrong before they have finished typing. The hybrid approach (blur → error → live) is supported by research showing on-blur validation reduces errors vs. submit-time validation without increasing completion time."

- id: developerway-discriminated-unions-react
  url: https://www.developerway.com/posts/advanced-typescript-for-react-developers-discriminated-unions
  domains: [coding-js-react]
  gap: "coding-js-react covers state management patterns (useReducer, refs) and hook encapsulation but has no principle about TypeScript type design for component props with mutually exclusive variants"
  status: unread
  added: 2026-07-10
  source: discovery
  fetch-note: "URL returned 403; argument extracted from search result summaries of this and closely related articles (Total TypeScript, oneuptime.com Jan 2026). Core claim: when a component has N variants whose props are mutually exclusive, use a discriminated union rather than a flat interface with optional props. Because: a flat interface with optionals allows invalid combinations that TypeScript cannot catch; a discriminated union makes the variants enumerable, narrows props per variant, and forces call sites to update when a new variant is added."

- id: logrocket-flexbox-vs-grid
  url: https://blog.logrocket.com/css-flexbox-vs-css-grid/
  domains: [css]
  gap: "css domain has no layout methodology principle — when to choose flexbox vs. grid is a recurrent structural decision with no guidance in the corpus"
  status: unread
  added: 2026-07-10
  source: discovery
  fetch-note: "URL returned 403; argument extracted from search result summaries of multiple 2025-2026 sources on this topic. Core claim: Flexbox works content-outward (items size themselves from content, Flexbox distributes remaining space); Grid works layout-inward (tracks are defined first, placement is independent of source order). Because: mixing the mental models produces layouts where content fighting the grid or grid fighting content creates unpredictable reflow. Decision rule: use Grid when elements must align across both axes or when placement must be independent of document source order; use Flexbox when item count is dynamic or items should size from their own content."
```
