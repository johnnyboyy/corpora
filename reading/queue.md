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
```
