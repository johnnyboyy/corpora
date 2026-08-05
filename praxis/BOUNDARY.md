# praxis (in-repo, pre-split)

Praxis is the **process / orchestration layer** — routing, phases, workflows, the framing step, and the
hard "one unit-of-work = one spawn = one handoff" rule. Corpora is the **judgment / composition layer**
it invokes. The horizon is for these to be two systems that compose, with praxis eventually its own repo.

This subtree grows praxis **inside corpora for now**, on purpose: the last attempt externalized too
early and regressed. We build the boundary here, prove it under real use, and lift the whole `praxis/`
directory out only once it holds.

## The extraction contract — keep the lift cheap

1. **No corpora imports, ever.** Nothing under `praxis/` imports `corpus.py` or reads corpora's
   kernel/domains as logic. Praxis reads the filesystem and invokes judgment engines through a generic
   contract, never by naming corpora as a dependency. (The first failure was praxis pointing at corpora
   in its own kernel — do not repeat it.)
2. **Runs off `corpora/config.md` for now.** There is no praxis-native config yet. A root is a directory
   carrying `corpora/config.md`; `root_tree.py` also recognizes `praxis/config.md` so a future
   praxis-native config is a one-line default change, not a rewrite.
3. **Self-contained subtree.** Everything praxis lives under `praxis/` (`scripts/`, `tests/`, and later
   its own kernel/phases). Lifting praxis = moving this directory out and flipping the config default.
4. **Corpora must stop owning orchestration** as praxis takes it over — the "I am the orchestrator"
   framing in corpora's SKILL/kernel is extracted into praxis, not left to compete with it. (This is the
   second failure to avoid; it is a later step, tracked, not done yet.)

## The migration method — deterministic-first

Every corpora process moves here eventually. The rule for each: **whatever can be a script should be
a script** — scripts are testable and can't be wrong the way inference can. So each process is sorted
into two piles:

- its **deterministic** surface (which root, what composition, what drifted, what files changed) →
  a praxis **script** under `scripts/`, with tests;
- its **judgment** surface (size this, decide that, weigh the tradeoff) → a thin **phase** under
  `phases/` that runs the scripts for facts, then invokes the judgment engine only where judgment
  actually remains.

Not every process yields a new script. `root_tree` was almost all deterministic → a script. `framing`
is mostly judgment whose deterministic core is *already* scripted (`root_tree` + composition) → a
phase that consumes those facts, no redundant wrapper. Building each process this way is what orients
the whole move.

### Phase schema (the template every migrated process follows)

A phase file (`phases/<name>.md`) declares in its own prose — the idea carried over from the old
praxis, rewritten decoupled:

- **entry condition** — the task-state test that selects this phase (stated in the file, no lookup table)
- **stance** — convergent / divergent / none
- **invocations** — which judgment engine(s) it calls, with stance + scope; omit for a purely
  mechanical phase. Named generically; praxis never hard-depends on a specific engine.
- **deterministic facts** — the scripts it runs first, whose output is fact not judgment
- **artifact** — the concrete deliverable it hands forward
- **surfaced/lacking** — what a run reports as still missing or newly revealed (drives re-routing)

## The invocation contract — how praxis calls a judgment engine

A phase (or a sequence script) invokes an engine for a *capability*, generically. Praxis never
re-derives what the engine provides, never imports it, never learns its schema — and, now, never
names an engine verb in its own prose or code. The capability surface is **plugin-declared**: the
engine ships a capabilities manifest and praxis resolves a capability *name* against it.

- The manifest is `engine/plugins/corpora.json` — the exact analogue of `handoff/plugins/corpora.json`.
  It maps each capability to a corpora CLI verb plus an argument shape (`flag`/`positional`/`global`/
  `boolean`, `required`) and a one-line description. It is the only place a corpora verb name lives.
  Declared capabilities: **compose** (`select`), **principle-add** (`add-principle`),
  **import-ratify** (`ratify-import-candidate`), **import-file** (`import-candidate`),
  **import-file-pool** (`import-default-pool`), **domain-import-list** (`import-list`),
  **kill-report**, **kill-graduate** (`graduate-kill`), **domain-migrate** (`migrate-domains`),
  **measure**, **domain-verify** (`verify`), **lint-domains**, **gate-record** (`record-gate`),
  **triggers**. A second engine drops its own manifest declaring its own capability→verb map and
  praxis core resolves against it identically; nothing in praxis enumerates these in prose.
- **compose** is no longer special — it is just the read capability `frame` interprets as JSON
  (the domain set for unit-of-work X at root R) rather than branching on pass/fail. Praxis owns the
  *unit-of-work decision* (routing judgment); the engine owns turning it into a domain set.

The whole coupling surface is two small pieces: the manifest (data) and `scripts/engine.py`
(`load_manifest` → `build_argv` → `resolve`, plus the `--corpus-py` locator shared with
`frame.py::engine_compose`). On lift, `engine_compose` + `engine.resolve` + the manifest become the
one engine registry; nothing else changes.

## Built so far

- `scripts/root_tree.py` (+ tests) — deterministic root-tree resolver. `tree` / `resolve` / `span`.
  The "fact prior to everything": which root(s) a task belongs to, produced by script, never inferred.
- `scripts/frame.py` (+ tests) — the deterministic fact bundle for a task: governing root, the
  span→decompose verdict, and the composition (invoked from the engine). Isolates the sole corpora
  binding to one overridable function. 13 tests total: `python3 -m unittest discover -s praxis/tests`.
- `phases/framing.md` — the first phase: the universal, proportional front door (frame facts → sizing
  → assumption-relay → route). The judgment layer that consumes `frame.py`. First worked example of a
  judgment-phase; `root_tree` was the first worked example of a pure-deterministic script.
- `handoff/` + `scripts/handoff.py` (+ tests) — **the handoff is a praxis primitive**: one
  unit-of-work produces one handoff. Praxis owns the envelope (`handoff/base.json`); judgment engines
  hook in as **plugins** (`handoff/plugins/*.json`) declaring the fields they expect. `handoff.py`
  composes the schema from base + plugins, generates a skeleton, and *validates that every registered
  plugin's required fields come out the other side* — praxis enforcing presence without knowing what
  any field means. `handoff/plugins/corpora.json` is corpora registered as the first plugin (this is
  where corpora's handoff schema now lives, instead of baked into corpora's kernel). The handoff
  **lifecycle is now fully praxis-owned**: `template` (create) · `validate` · **`close`** (delete, or
  archive under `<handoffs-dir>/archive/` when the governing root's `corpora/config.md` sets
  `debug: yes`; guarded to a file sitting directly inside the handoffs dir). No engine is invoked for
  any of the three — close was the missing third op and is native (ported from corpora's
  `handoff-done`), so no primitive is split across the boundary.
- `scripts/root_tree.py interop` + `phases/interop.md` — interop is **entering at the right root**.
  `interop_root` deterministically computes the entry root for a spanning task (the deepest root
  containing all spanned roots) — or reports that none exists and names where to define one. The
  phase is the judgment half: at the entry root the boundary decides *done-here* (the interop concern
  itself) vs *defined-and-passed-off* to a child root that executes in its own context and hands back.
- `tests/test_e2e.py` — a throwaway fixture project (two roots), praxis scripts driven as real
  subprocesses: frame a task (with real composition via `corpus.py`) → generate a handoff → validate
  it; and the cross-root decompose path.

### Migrated processes (second wave)

- `scripts/engine.py` — the single overridable corpora binding for engine *write verbs*, the analogue
  of `frame.py::engine_compose` for everything past compose. Every sequence script routes its corpora
  calls through `engine.invoke`; on lift, `engine_compose` + `engine.invoke` become the one engine
  registry. The whole widened coupling surface is this one file (see `MIGRATION-NOTES.md`, F1).
- `scripts/chunk_ledger.py` (+ tests) — **praxis-core: unit-of-work accounting.** The chunk ledger is
  a praxis fact, so praxis reads/writes it at `corpora/chunks/<workstream>.md` **natively** (ported
  `parse_chunks`/`render_chunks`, byte-compatible with corpora's format), enforces the load-bearing
  chunk-done-before-handoff-close gate + the handoff-exists precondition, and reconciles the handoff
  against the composition (both failures: workstream mismatch; `domains-loaded` ≠ `domains-composed`).
  The **only** engine call left in the ledger is `compose` (the `domains-composed` ground truth); the
  close sequence now calls `handoff.py close` natively rather than a `handoff-close` engine verb. NOTE:
  the ledger/handoff *files* still live under `corpora/chunks/` and `corpora/handoffs/` (praxis writes
  them there); a later move to a praxis-owned path is out of scope, tracked for the lift.
- Deterministic-procedure scripts (+ tests), each owning ordering/preconditions/guards, tested against
  a stub engine (`tests/_stub_engine.py`):
  - `scripts/domain_migrate.py` — domain-repo-migration: migrate → measure → verify (**hard gate**) →
    lint-domains.
  - `scripts/kill_graduation.py` — kill-graduation: read-only `candidates` vs. one-id `graduate` (no
    batch path, so the judgment gate can't be skipped).
  - `scripts/domain_import.py` — domain-import: browse (read-only) → file/file-pool → ratify.
  - `scripts/ratify_writeback.py` — ratify-write-back: dispatches the two scripted verbs, prints the
    exact hand-edit steps for the three manual ones (the scripted-vs-manual map is the fact).
- Pure-deterministic scripts (+ tests), no corpora coupling at all:
  - `scripts/library_state.py` — the six ui/ux/screenshot library processes' shared fact: `has-ui`,
    which libraries exist, which init/sync phase is eligible, and the ui→{screenshot,ux} ordering.
  - `scripts/churn.py` — architecture-scan's `scan-scope-by-recent-churn`, as a git fact.
- Judgment phases (consume the scripts above; no redundant wrappers): `phases/debugging.md`,
  `phases/runtime-verification.md`, `phases/testing.md` (the three test processes, one composition),
  `phases/retrospective.md`, `phases/architecture-scan.md`, `phases/comment-cleanup.md`,
  `phases/design-decision-review.md`, `phases/library-init.md` + `phases/library-sync.md` (three
  variants each), `phases/domain-import.md`.
- `MIGRATION-NOTES.md` — the open judgment forks (F1–F6, F1 now resolved) and the **plan** (not
  build) for extracting the orchestration spine (`general-operation`, `bootstrap`), the operator-gated
  failure-mode-2 step.
- Full suite: `python3 -m unittest discover -s praxis/tests`.

### Engine capability plugin (resolves F1)

- `engine/plugins/corpora.json` + `scripts/engine.py` (`load_manifest` → `build_argv` → `resolve`) —
  the engine's write-verb surface is now **plugin-declared**, mirroring the handoff plugin. Praxis
  core no longer names a corpora verb anywhere; every sequence script invokes by *capability name*
  and the manifest (data) maps it to the verb + argv. `compose` folded in as just another declared
  capability (`frame.py::engine_compose` builds its argv through `resolve`, still interpreting the
  JSON result). The corpora-plugin sequence scripts (`ratify_writeback`, `kill_graduation`,
  `domain_import`, `domain_migrate`) each carry a one-line header marking them corpora-specific
  orchestration, distinct from praxis-core (`root_tree`, `frame`, `handoff`, `engine`, `route`,
  `chunk_ledger`). (`chunk_ledger` was reclassified corpora-plugin → praxis-core when its writes went
  native; only `compose` still routes through the engine.) Tests: `tests/test_engine_capabilities.py`.

### Routing (GO-2 steps 1–2 of the orchestration-spine plan)

- `scripts/route.py` (+ `tests/test_route.py`) — the deterministic fact-sheet a routing decision
  consumes: it runs `frame` (root, span→decompose, composition) and adds the execution-shape signals
  — `spans → isolate`, and the workstream **ledger** lookup (`exists` = resume candidate vs. `absent`/
  `unknown` = new) as a **native filesystem check** of the praxis-owned ledger file
  (`chunk_ledger.chunks_path`); `unknown` when no workstream is named or no single governing root.
  Facts only; no decision.
- `phases/routing.md` — the GO-2 judgment on top of `route.py`: pick the unit-of-work, the stance, and
  the execution shape (inline / resume / isolate). *The* "I am the orchestrator" decision, thin by
  design (reads from `route` facts + `framing`'s proportionality), routing *to* the irreducible
  judgments (composition GO-3, domain-assignment GO-6) rather than automating them. Fires per unit of
  work — the mitigation for the failure that killed the last praxis. Steps 3–4 (`session.md` loop
  conductor, `bootstrap.md`) remain unbuilt and operator-gated (see `MIGRATION-NOTES.md` Part 2).

## The handoff plugin contract

Praxis's invariant: **a unit-of-work produces a handoff.** The *shape* of that handoff is dynamic —
composed from plugin manifests, not fixed. A plugin drops a `handoff/plugins/<name>.json` declaring
its `frontmatter` fields and `sections` (name, required, shape, desc). Rules praxis enforces:
`handoff.py validate` fails unless every required field from base **and every registered plugin** is
present; a plugin may **not** override a base field (base wins, conflict recorded) so no plugin can
downgrade a required base field. This is how corpora "hooks into" the handoff — and how a second
engine would, without either knowing about the other.

