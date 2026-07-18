# Coder overlay — web-frontend pack

Overlays the base coder lens (`coder.md`) when `corpora/config.md` declares
`role-pack: web-frontend`: adds JS/TS/React/CSS conventions and two stack-specific coding domains.
The base lens and its `coding-general` domain still apply in full — this only extends them.

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

## domains

Added to the coder lens's declaration (load order per `kernel.md` — pack-seed working file, then
`corpora/domains/<domain>.md` if it exists):

- `coding-ts` — `packs/web-frontend/domains/coding-ts.md`. Framework-agnostic JS/TS patterns.
- `coding-react` — `packs/web-frontend/domains/coding-react.md`. React-specific patterns (JSX,
  hooks, refs, prop-typing).
- `css` — `packs/web-frontend/domains/css.md`. CSS/Tailwind authoring and specificity.
- `coding-nextjs` — `packs/web-frontend/domains/coding-nextjs.md`. Next.js App Router patterns.
  Loaded only when `corpora/config.md` declares `framework: nextjs` — skip for Expo Router,
  Vite, or other frameworks.

Audit metadata (`packs/web-frontend/domains/audit.md`) is reached only at ratify/retrospective
time; each domain's kill log lives in its working file.
