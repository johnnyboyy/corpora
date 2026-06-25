# Reviewer overlay — web-frontend pack

This overlays the base reviewer lens (`reviewer.md`). Load it alongside the base for any project
whose `corpora/config.md` declares `role-pack: web-frontend`. It adds the stack-specific coding
domains so the reviewer evaluates JS/React and CSS code against their principles in addition to
`coding-general`. The base reviewer's lens still applies in full — this only extends the domain
declaration.

## domains

This overlay adds these coding domains to the reviewer lens's declaration (each domain's pack-seed
working file, then the same-named `corpora/domains/<domain>.md` when it exists):

- `coding-js-react` — `packs/web-frontend/domains/coding-js-react.md`. JS/TS/React code patterns.
- `css` — `packs/web-frontend/domains/css.md`. CSS/Tailwind authoring and specificity.

Provenance, promotions, and per-domain kill logs are reached only at ratify/retrospective time
(`packs/web-frontend/domains/audit.md`); each domain's kill log lives in its working file.
