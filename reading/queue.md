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
```
