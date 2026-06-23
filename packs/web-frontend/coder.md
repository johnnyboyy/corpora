# Coder overlay — web-frontend pack

This overlays the base coder lens (`coder.md`). Load it alongside the base for any project whose
`corpora/config.md` declares `role-pack: web-frontend`. It adds JavaScript/TypeScript/React/CSS
conventions and declares two stack-specific coding domains. The base coder's lens and its
`coding-general` domain still apply in full — this only extends them.

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

## domains

This overlay adds these coding domains to the coder lens's declaration (each domain's pack-seed
working file, then the same-named `corpora/domains/<domain>.md` when it exists):

- `coding-js-react` — `packs/web-frontend/domains/coding-js-react.md`. JS/TS/React code patterns.
- `css` — `packs/web-frontend/domains/css.md`. CSS/Tailwind authoring and specificity.

Provenance, promotions, and per-domain kill logs are reached only at ratify/retrospective time
(`packs/web-frontend/domains/audit.md`); each domain's kill log lives in its working file.
