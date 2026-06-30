# Reading queue

Sources queued by the discovery agent, awaiting the reading agent.
Format: url, domains, gap addressed, status (unread | read), source (discovery | manual).

```yaml
queue:

- id: shevlin-use-encapsulation
  url: https://kyleshevlin.com/use-encapsulation
  domains: [coding-js-react]
  gap: "encapsulation patterns in React hooks — not yet addressed in coding-js-react"
  status: unread
  added: 2026-06-29
  source: manual

- id: export-default-mistake
  url: # unknown — search "export default is a mistake" javascript to locate
  domains: [coding-general]
  gap: "module export naming — naming exports and imports identically makes consumers trivially findable; default exports break this"
  status: unread
  added: 2026-06-29
  source: manual
  note: "URL needed. Argument: export default lets importers choose any name, obscuring consumers. Named exports enforce consistent naming."
```
