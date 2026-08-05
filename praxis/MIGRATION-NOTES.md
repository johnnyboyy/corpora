# praxis migration notes

Working notes from migrating corpora's processes into praxis. Two parts: (1) open judgment forks the
deterministic-first pattern did not resolve, each with a recommendation for the operator; (2) the
analysis + migration PLAN for the two orchestration-spine processes (`general-operation`, `bootstrap`)
that were deliberately **not** rebuilt — extracting them is the delicate "move orchestration out of
corpora" step reserved for operator review.

This file is additive and advisory. Nothing here modified corpora; the migration built only under
`praxis/`.

---

## Part 1 — Open judgment forks (operator review)

### F1. The invocation contract widened from one capability to a set of engine write-verbs

`BOUNDARY.md` names exactly one decided capability praxis invokes on the engine: **compose**
(`frame.py::engine_compose`). Migrating the deterministic-procedure files (chunk-accounting,
ratify-write-back, kill-graduation, domain-import, domain-repo-migration) required praxis to invoke
corpora *write* verbs too — `chunk-done`, `handoff-done`, `add-principle`, `ratify-import-candidate`,
`kill-report`, `graduate-kill`, `import-list`, `migrate-domains`, `verify`, `lint-domains`, etc.

- **What I did:** isolated *all* of these behind a single new binding, `scripts/engine.py::invoke`,
  the exact analogue of `engine_compose` — one function that knows where corpora is and how to call
  it, overridable with `--corpus-py`, degrading (not crashing) when the engine is absent. Praxis
  still never imports corpora and never learns a verb's semantics; each sequence script owns only the
  *order/preconditions/guards* (which are what I tested against a stub engine). On lift,
  `engine_compose` + `engine.invoke` collapse into the one engine registry `BOUNDARY.md` anticipates.
- **The fork:** is a corpora write-verb (e.g. `add-principle`, `migrate-domains`) legitimately a
  praxis-invoked *capability*, or is it purely a corpora engine concern that praxis should only ever
  *name in a phase* (as framing names compose) and never call? I read the task's explicit instruction
  ("map their command sequences into praxis scripts + tests") as sanctioning the former, but this is a
  real widening of the contract in `BOUNDARY.md`.
- **Recommendation:** accept the widening but record the *capability set* explicitly in `BOUNDARY.md`'s
  invocation contract (compose · handoff-close · principle-write-back · kill-graduation · import ·
  migrate · verify), so the coupling surface stays enumerated rather than open-ended. Keep `engine.py`
  as the single binding. If instead the operator wants the contract to stay at *compose only*, these
  five scripts should degrade to phase prose that names the corpora commands without a praxis binding
  — cheaper coupling, but the ordering guards (chunk-done-before-handoff-done, the migration
  verify-gate) stop being testable, which is the thing that made them worth scripting.

### F2. `handoff-done` (closing a handoff) lives on both sides of the boundary

The handoff is declared a **praxis primitive** (`BOUNDARY.md`, "Built so far"; `handoff/`), yet
*closing* a handoff is a corpora verb (`corpus.py handoff-done`, which deletes/archives the file), and
the load-bearing ordering rule (`chunk-done` must precede `handoff-done`) is what makes
`chunk_ledger.py` worth having.

- **The fork:** should the handoff *lifecycle* (create → validate → close) become fully praxis-owned,
  with praxis doing the close (delete/archive) itself and corpora's `handoff-done` retiring? That
  would put the whole primitive on the praxis side of the line.
- **Recommendation:** yes, eventually — praxis already owns create (`handoff.py template`) and
  validate (`handoff.py validate`); close is the missing third. For now `chunk_ledger.py` delegates
  close to corpora and only *orders* it, which is correct and testable. Flagging it so the eventual
  lift moves close to praxis rather than leaving a primitive split across the boundary.

### F3. Six library processes vs. one `library_state` script + two phases

The six ui/ux/screenshot × init/sync processes share one deterministic surface (which library exists,
`has-ui`, the ui→{screenshot,ux} ordering). I put that whole surface in `library_state.py` and
collapsed the six process files into two phases (`library-init`, `library-sync`) that branch on the
variant.

- **The fork:** is two phases-over-six-processes the right granularity, or does the operator want one
  phase file per original process (six), matching corpora 1:1 for reviewability?
- **Recommendation:** keep the two. init-vs-sync is the real judgment fork; ui/ux/screenshot are
  variants of each, and the variant selection is now a *fact* from `library_state.py`, not prose to
  duplicate six times. This is the same consolidation `testing.md` makes for the three test processes.

### F4. `ratified`-vs-`exists` proxy in `library_state.py`

The processes trigger ux-init / screenshot-init on the ui-library being *ratified*; `library_state.py`
uses *file existence* as the deterministic proxy (ratified state is a corpora gate counter, not a
filesystem fact praxis can read without coupling).

- **Recommendation:** acceptable — a `ui-library.md` on disk is the near-universal case of "ui-init
  ratified," and praxis explicitly does not read gate state. If the gap ever bites (a drafted-but-
  unratified library unlocking ux-init early), expose a one-line `ratified?` check as an engine
  capability rather than having praxis parse corpora's gate ledger. Noted in the script's docstring.

### F5. `ratify_writeback.py` is the thinnest migration — part script, part "this is manual"

Of the named deterministic-procedure files, ratify-write-back has the least scriptable content: two
of its five operations have corpora commands (`add-principle`, `ratify-import-candidate`); three
(reject-to-kill-log, reshape-history, graduate-to-convention) are hand-edits with *no* command. I
built the script to dispatch the two scripted verbs and, for the three manual ones, print the exact
hand-edit steps while invoking nothing — so the deterministic fact it carries is *the map of
scripted-vs-manual*, not a fake wrapper.

- **The fork:** is a script whose main value is "honestly telling you which paths aren't scripted"
  worth being a script, or should those three be phase prose only? I kept it a script so the
  scripted/manual split is one testable place and the retrospective/gate phases can call one thing.
- **Recommendation:** keep as-is; revisit if corpora ever grows `reject`/`graduate-convention`
  commands, at which point the manual verbs become scripted dispatches with no interface change.

### F6. `comment-cleanup` queue reconciliation — a deferred script candidate

`comment-cleanup` is judgment (per-comment classification), migrated as a phase. Its one candidate
deterministic sliver is *queue reconciliation* (drop `corpora/comment-cleanup-queue.md` entries whose
comment no longer exists at `file:line`, append new ones). I left it as phase prose because "the
comment no longer exists / the surrounding code changed" needs the judgment pass to establish — a pure
`file:line still has a comment?` check would be brittle against line drift.

- **Recommendation:** defer. If it recurs as real burden, a `comment_queue.py reconcile` that diffs
  the queue's `file:line` anchors against current comment positions is the shape — but only if the
  project accepts the line-drift fragility. Not built.

---

## Part 2 — The orchestration spine: `general-operation` + `bootstrap` (PLAN, not built)

These two are the "I am the orchestrator" framing itself. `BOUNDARY.md`'s failure-mode-2 is corpora
continuing to own orchestration while praxis competes with it; extracting the spine is *how* corpora
stops owning it, and doing it wrong is what killed the last praxis. So this is a plan for operator
review, not code.

### What they are

- **`general-operation.md`** (~24k) is the session loop, nine phases: (1) session entry → (2) routing
  → (3) spawn brief + composition → (4) execution → (5) relay → (6) ratify gate → (7) post-gate
  maintenance → (8) retrospective → (9) architecture scan. Phases 2–6 are the per-unit-of-work cycle;
  7–9 are maintenance/periodic.
- **`bootstrap.md`** (~16k) is the first-run pipeline: Phase 1 (config/shape, always) → the
  `has-ui` fork into Phase 2 (ui-init) → Phase 3 (screenshot) + Phase 4 (ux), with a "reapply the
  orchestrator between every phase" checkpoint. It is invoked *from* general-operation's Phase 1.

### Deterministic vs judgment, phase by phase

| spine phase | deterministic (→ praxis script) | judgment (→ praxis phase / engine) |
|---|---|---|
| GO-1 session entry | detect project shape/commands (already `corpus.py`); read config | "is this bootstrap or resume" routing |
| GO-2 routing | `frame` (root, span/decompose) — **already built** | produce stance + unit-of-work + inline/resume/isolate — **the core routing judgment; the thing that must move to praxis** |
| GO-3 spawn brief + composition | `compose` (engine) + `handoff template` — **already built**; `chunk-start` preview — **built** | writing the task content of the brief |
| GO-4 execution | — | all judgment; delegates to the composed domains |
| GO-5 relay | route: divergent/library-Artifact → design-decision-review; else gate — **the routing test is in `phases/design-decision-review.md`** | accept/revise/reject; scope-divergence read |
| GO-6 ratify gate | `record-gate`, `add-principle`, `ratify-import-candidate`, `triggers` — **sequences built** (`ratify_writeback`, `chunk_ledger` close) | per-proposal ratify/reject/edit; **domain assignment** (the one irreducible gate judgment) |
| GO-7 post-gate maintenance | `library_state` (which sync is eligible) + screenshot-sync verbs — **built**; `sync-done` | whether accumulated drift actually touched a flow (operator call) |
| GO-8 retrospective | `kill_graduation` report, `close-workstream` — **built** | the whole retrospective read — **`phases/retrospective.md`** |
| GO-9 architecture scan | `churn` — **built** | the deep-module read — **`phases/architecture-scan.md`** |
| BS-1 config | `corpus.py` shape detection; config write | two bootstrap questions when greenfield |
| BS-2/3/4 library bootstrap | `library_state` eligibility + ordering — **built** | the init work — **`phases/library-init.md`** |

**Reading of the table:** the spine's *periodic and maintenance* phases (GO-7/8/9, BS-2/3/4) are
**already migrated** — their scripts and phases exist. What remains genuinely un-migrated is the
**per-unit loop's spine**: GO-2 routing (produce stance + unit-of-work + execution-shape) and the
GO-2→3→4→5→6 *sequencing itself* — i.e. the orchestrator's control flow.

### The migration plan (proposed, gated)

1. **`scripts/route.py` (deterministic surface of GO-2).** Praxis already owns the *facts* routing
   consumes (`frame`: root, span/decompose, composition). What GO-2 adds is: given a task and those
   facts, emit the *candidate* unit-of-work(s) and the execution-shape signals (does it resume an
   existing workstream? does it isolate?). Much of this is deterministic — an existing workstream id
   is a ledger lookup; span→decompose is already `frame`. Build `route.py` to bundle these into a
   routing *fact sheet*; leave the actual stance + unit-of-work *decision* to a phase. **This is the
   first extraction step and the lowest-risk one** — it is more `frame`, not new orchestration.
2. **`phases/routing.md` (the GO-2 judgment).** The convergent judgment on top of `route.py`: pick the
   unit-of-work, the stance, inline/resume/isolate. This is the single most important thing to move
   from corpora to praxis, because it is *the* "I am the orchestrator" decision. It should read almost
   entirely from `route.py` facts + `framing.md`'s proportionality.
3. **`phases/session.md` (the loop spine, GO-1 + the 2→3→4→5→6 control flow).** The thin conductor
   that runs framing → routing → (compose + brief) → execution → relay → gate, one unit of work at a
   time, looping. This is where the "one unit-of-work = one spawn = one handoff" invariant lives as
   control flow, and where the handoff primitive and chunk close (`chunk_ledger`) are sequenced. **This
   is the highest-risk extraction** — it is literally the orchestrator — and should be the *last*
   step, done only once routing (steps 1–2) has proven itself under real use, exactly the incremental
   discipline `BOUNDARY.md` prescribes.
4. **`phases/bootstrap.md` (BS control flow).** A conductor like `session.md` but for first-run:
   config (BS-1) → `library_state`-driven init pipeline (BS-2/3/4, already a phase) with the
   reapply-the-orchestrator checkpoint between phases. Lower risk than `session.md` because its
   sub-phases are already migrated; it is mostly sequencing + the has-ui fork (a `library_state` fact).

### Risks specific to the spine (why it is gated)

- **Failure mode 2 (the killer):** the moment `phases/session.md` exists, praxis and corpora both
  contain an orchestrator. The last praxis died because routing was ceded to praxis but praxis's
  routing was *gap-triggered only* — no rule that a queue-task boundary is itself a routing point — so
  per-task spawning collapsed into inline execution (see the operator's own regression evidence). The
  plan's mitigation: build routing (steps 1–2) and prove it *actively fires per unit of work* before
  building the loop (step 3), and when the loop lands, corpora's `general-operation.md` framing must
  be *retired in the same change*, not left to compete. That retirement is an operator-gated edit to
  corpora — out of scope for this additive migration.
- **The domain-assignment judgment (GO-6)** must stay a live decision, never scripted — it is the one
  point corpora itself keeps as judgment. `route.py`/`session.md` must route *to* it, not automate it.
- **Ordering invariants** already captured (`chunk_ledger` close order, the migration verify-gate)
  must be the loop's, not re-implemented inline in `session.md`.

### Recommendation

Do steps 1–2 (`route.py` + `phases/routing.md`) next, as their own operator-gated task, and stop
there for a while — run real tasks through praxis routing while corpora still owns the loop. Only
after routing demonstrably fires per unit of work should steps 3–4 (the loop conductor + bootstrap
conductor) be attempted, paired with the corpora-side retirement of the competing orchestrator
framing. Everything in Part 2 is deliberately left unbuilt pending that review.
