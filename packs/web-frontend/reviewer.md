# Reviewer overlay — web-frontend pack

Overlays the base reviewer lens (`reviewer.md`) when `corpora/config.md` declares
`role-pack: web-frontend`: adds the stack-specific coding domains so the reviewer evaluates
JS/React and CSS against their principles in addition to `coding-general`. The base lens still
applies in full — this only extends the domain declaration.

## domains

Added to the reviewer lens's declaration (load order per `kernel.md` — pack-seed working file,
then `corpora/domains/<domain>.md` if it exists):

- `coding-js-react` — `packs/web-frontend/domains/coding-js-react.md`. JS/TS/React code patterns.
- `css` — `packs/web-frontend/domains/css.md`. CSS/Tailwind authoring and specificity.

Audit metadata (`packs/web-frontend/domains/audit.md`) is reached only at ratify/retrospective
time; each domain's kill log lives in its working file.
