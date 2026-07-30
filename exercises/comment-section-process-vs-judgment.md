# Exercise: process vs. judgment, run against a real feature

Two literal runs of the same exercise, same feature request, same fresh-scaffold demo project
(`/Users/johnzdanis/jdev/corpora-exercise-blog/`, reset to its pre-exercise state between runs).
Run 1 (below) was against corpora before the `separating-process-from-judgement` restructuring;
Run 2 (bottom of this file) is against the same corpus, mid-restructuring, on this branch, with
substantial uncommitted process-layer changes already in place (chunk ledger, `verify-chunks`,
deterministic-shortcut-candidates rename, orchestrator-as-process framing). Run 2 checks which of
Run 1's three findings the restructuring actually closed, and records what a second literal
execution surfaced that imagining the run never would have.

Ran corpora end-to-end, literally, against a fresh Next.js blog with no `corpora/` yet
(`/Users/johnzdanis/jdev/corpora-exercise-blog/`), on the feature request: "A comment section for
blog posts and the commenters can have their own avatars and profile." Bootstrap Phase 1 →
routed-planner queue → `comments-01` (UI library seed) → `comments-02` (UX library seed) →
`comments-03`/`comments-04` (implementation) → ratify gates → `npm run build` and a live dev
server confirmed the feature actually renders and the flow is wired correctly. Every file in the
demo project's `corpora/` directory and the app code is real output of that run, not a simulation
written after the fact.

This is the backward pass: for every step actually taken, what was **process** (the schema, the
gate procedure, `corpus.py`'s arithmetic — mechanical, deterministic, inspectable independent of
any specific decision) and what was **judgment** (a weighed call under uncertainty, recorded with
a `condition`/`reason` so it can be re-weighed later) — and where the run exposed the seam between
them not holding cleanly.

## Process, as actually exercised

- `corpus.py select --unit-of-work <u>` — deterministic domain-set lookup against
  `corpora/config.md`'s shape fields. No model in the loop; re-running it reproduces the same
  answer.
- `corpus.py compose-spawn-prompt` — byte-for-byte concatenation of the stance frame, every
  composed domain's full text, and the handoff schema. No summarization step, so there's nowhere
  for compression to silently drop content.
- The handoff YAML envelope + `lint-handoff` — fixed fields, structurally validated independent of
  whether the content in them is any good.
- `record-gate` / `measure` / `verify` — all counting and reconciliation arithmetic. The model
  supplies classifications (ratified count, fired/violated/idle) as arguments; the script does the
  bookkeeping and can prove after the fact whether every gate got recorded.
- `handoff-done` — delete-or-archive based on a config flag, no judgment involved.
- The **ratify gate as a numbered sequence of steps** (audit → check candidates → present
  proposals → assign a home → write back → close) is itself process — a fixed order of operations
  applied to whatever content passes through it.

## Judgment, as actually exercised

- Resolving what "commenters can have their own avatars and profile" means for a project with no
  auth system — per-comment declared identity vs. an account system. A real fork existed; I (in the
  planner's seat) picked per-comment identity and recorded why. This is exactly the shape
  `kernel.md`'s genuine-fork test asks for.
- `content-adjacent-surface-blends-not-bolts-on` (visual-hierarchy) — rejecting the default
  "bolted-on comment widget" pattern in favor of continuing the page's existing chrome-free
  register. A named, plausible alternative was actually rejected, not just avoided.
- `preserve-input-on-submission-error` (validation-feedback) — same shape: the plausible
  alternative (clear the form on error, the "unambiguous" option) was named and rejected.
- Choosing the "clean and precise" aesthetic direction — divergent judgment, filed as `direction`
  into `ui-library.md` rather than a domain, per the kernel's third route for identity decisions.
- Weighing `coding-nextjs`'s `revalidate-tag-over-path` against the actual situation (no tagged
  `fetch()` exists on this page at all) and concluding the principle's own stated exception applies
  — `revalidatePath` is fine here. This is judgment operating **on** an existing rule, not judgment
  producing a new one: deciding a codified principle's condition doesn't bind is the same faculty as
  writing the principle in the first place.

## Where the two interact — the actual finding

The clean story would be "process is the container, judgment is the content" — the spawn brief,
handoff, and queue schemas hold fixed shape while `rule`/`condition`/`reason`/task descriptions
carry the weighed content. That mostly held. But three concrete points in this run show the
boundary isn't fully built out yet, and they're the useful output of doing this literally instead
of imagining it:

1. **`select` (pure process) hard-fails on a project with zero accumulated judgment.**
   `Corpus.__init__` calls `fail()` if `corpora/domains/` doesn't exist — but that directory is
   pure judgment-layer state (it only ever holds *ratified* principles). A fresh, correctly
   bootstrapped project that hasn't ratified anything yet has no domains dir, so the very first
   `select` call after bootstrap — needed to route the very first spawn — fails until someone
   (here, me, standing in for the operator) manually `mkdir`s it. Process code has picked up a
   hidden dependency on judgment-layer state existing, which shouldn't be possible if the two are
   meant to evolve independently: a process-layer bugfix here (tolerate/auto-create an empty
   domains dir) requires zero judgment-layer knowledge, and a fresh project shouldn't need a
   judgment-layer workaround to unblock a process-layer command.

2. **Queue task-status transitions are process-shaped but unmechanized.** `corpora/chunks/*.md`
   (workstream ledger) gets `chunk-start`/`chunk-done` — scripted, reconciled by `verify-chunks`.
   `corpora/queue.md` has the identical shape of responsibility (fixed schema, `status` transitions
   the orchestrator is supposed to make "in-place") but no corresponding script command exists; I
   updated `status: pending → complete` with a hand-rolled regex substitution because nothing else
   was available. `kernel.md`'s own stated reason for scripting the chunk ledger and the ratify
   counters — "bookkeeping done by attention is bookkeeping that silently stops" — applies to the
   queue file just as directly and hasn't been applied there yet. This isn't a process/judgment
   boundary violation so much as an incomplete migration: one piece of core workflow state still
   depends on the orchestrator's attention where a sibling piece (chunks) already doesn't.

3. **Bootstrap's Phase 2/3 composition is judgment frozen into prose, not into either layer
   properly.** `select --unit-of-work design-ui-surface` returns the full ongoing-UI-design domain
   set (11 domains, including `forms-inputs`/`lists-selection`/`recoverability`/
   `validation-feedback`). `bootstrap.md` instead hand-lists a narrower 7-domain set for founding a
   library from nothing, justified entirely in prose ("narrower than ongoing `ui-design` work").
   That narrowing is a real, defensible judgment call — but it's expressed as a hard-coded list in
   an instruction file, invisible to `select`, un-re-runnable, and disconnected from the
   `applies-when`/`units-of-work` frontmatter mechanism every other composition decision goes
   through. It's neither pure process (not mechanically derivable/inspectable the way `select`'s
   output is) nor pure judgment-as-content (not a domain principle with a `condition`/`reason` that
   could be re-weighed or promoted) — a third, less legible category: judgment baked into
   procedural prose. Making it a distinct `unit-of-work` (e.g. `bootstrap-ui-surface`) with its own
   frontmatter membership would fold it back into the mechanism that already exists for exactly this
   kind of thing.

## What already works, and the actual split for developing them separately

The architecture already separates these into files that don't need to change together:
`kernel.md` + `SKILL.md` + `scripts/corpus.py` (process: schema, gate procedure, arithmetic,
covered by `tests/test_corpus.py`) vs. `domains/*.md` (judgment: portable principle content with no
procedural logic in it). A process-layer change — fixing finding #1, adding a `queue-*` command
family for finding #2 — touches `corpus.py` and its tests and needs zero domain-content judgment
to review. A judgment-layer change — ratifying, killing, or reweighing a principle — touches a
domain file and needs zero script changes to take effect. That separability is real and this run
depended on it working (the ratify gate, the handoff schema, and `select` never needed to know
anything about avatars or Tailwind to do their jobs correctly).

The three findings above are the boundary's remaining incompleteness, not a wrong design: process
code that assumes judgment-layer state already exists (#1), process-shaped bookkeeping not yet
given a process-layer command (#2), and a judgment call expressed in neither layer's proper form
(#3). The general test this run suggests for "is this properly split": **could this decision change
without touching `corpus.py`, and could `corpus.py`'s handling of it be exercised on a project with
zero ratified content?** Findings #1 and #3 fail the second half; #2 fails the first by omission
(the capability to change it without hand-editing doesn't exist yet at all).

---

## Run 2 — re-run mid-restructuring, on `separating-process-from-judgement`

Same procedure, literally, against the same reset scaffold, this time pointing at the branch's
current (uncommitted) `corpus.py`, `kernel.md`, `general-operation.md`, `bootstrap.md`,
`ui-library-init.md`, and `ux-library-init.md`. Full path: bootstrap Phase 1 → planner (`plan-work`,
one open question raised and resolved in the same pass, same per-comment-identity call as Run 1,
independently re-derived) → `ui-library-init` (divergent) → screenshot phase (correctly no-op — no
browser tool wired this session, and the file's own stated fallback is to skip cleanly) →
`ux-library-init` (convergent) → two coder chunks (storage layer, then UI wiring) → ratify gates →
chunk ledger → `verify-chunks` → `npm run build` and a **live dev server driven with real browser
automation**, not just a build check. That last step mattered: it caught two genuine runtime bugs
(below) that `tsc --noEmit` and `next build` passed cleanly through both times.

### Which Run 1 findings survived

**Findings #1 and #3 reproduce exactly, unfixed**, despite a large amount of other process-layer
work landing on this branch in the meantime (chunk ledger, `verify-chunks`, deterministic-shortcut
rename, orchestrator-as-process framing, `check-composition`). Confirmed by literally re-running
the same commands, not by re-reading the old finding:

- `Corpus.__init__` in the current `scripts/corpus.py` (line ~132) still hard-`fail()`s if
  `corpora/domains/` doesn't exist. `select --unit-of-work plan-work` on the freshly-bootstrapped
  demo project failed with the identical message Run 1 got, until manually `mkdir`ing an empty
  directory — again standing in for the operator, again with zero judgment-layer content to
  justify the directory's existence yet.
- `select --unit-of-work design-ui-surface` returns 11 domains; `ui-library-init.md` still
  hard-lists 7 in prose ("narrower than ongoing `ui-design` work..."). Same gap reproduces
  symmetrically on the UX side: `select --unit-of-work design-ux-flow` returns 9 domains
  (adding `ranking-evaluation` and `wizards-flows` beyond what Run 1 saw missing);
  `ux-library-init.md` still hard-lists the same narrower 7. Two independent instances of the same
  unmechanized judgment-in-prose, not one.

**Finding #2 is half-addressed.** The chunk ledger (`corpora/chunks/*.md`) that finding named as the
scripted sibling now has a full command family that didn't exist in Run 1 — `chunk-start`,
`chunk-done`, `lint-chunks`, `close-workstream`, `verify-chunks` — and this run exercised all of
them successfully; `verify-chunks` correctly reconciled every chunk against a fresh `select()` call
at the end. But `corpora/queue.md` — the sibling Run 1 named as having "the identical shape of
responsibility" and no script — still has no `queue-*` command family. This run's planner phase
still hand-wrote `status: pending → complete` transitions directly into the file (there was only
one task-status edit needed this time, so it's a smaller instance of the same gap, not a new one).

### What a second literal run surfaced that imagining it wouldn't have

**New finding A — `record-gate` for a seed-origin domain writes into the shared skill's own
tracked file, with no isolation between "a real project's earned judgment" and "a demo run."**
`corpora/domains/audit.md` is *one file per layer* by design — the kernel-seed layer's copy lives
in the skill's own repo, at whatever path the project's `corpus.py` was invoked against. This run
pointed the demo project's `corpus.py` calls directly at this live dev checkout (not a copied,
pinned install — the `README.md` "genuine divergence" path exists for exactly this, and wasn't
used, because the demo project's `config.md` has nothing that would prompt using it). Recording a
gate for `interviewing` and `spawn-integrity` (both seed-origin, no project-level file for either)
required pointing `--domains-dir` at the skill repo's own `domains/`, and doing so actually rewrote
this repo's tracked `domains/audit.md` in place — origin fields flipped, token counts changed,
new efficacy rows appended for principles this exercise run exercised, not any real corpora
development work. This was caught and reverted (`git checkout -- domains/audit.md`) before it could
leak into a commit, but only because `git status` was checked afterward, not because anything in
`corpus.py` warned before writing. The mechanism is arguably working as designed — cross-project
accumulation into a shared seed layer is the whole point of "concatenate, don't fork" — but it means
running *any* project's ratify gate against a live, symlinked-or-referenced dev checkout of the
skill (as opposed to a released, copied install) can silently mutate the skill's own audit history
with no confirmation step and no attribution of which project's gate wrote what. This is sharper
than findings #1–#3: those are process code with an awkward dependency; this is process code with a
side effect on shared state outside the project it was invoked for.

**New finding B — the chunk ledger's anti-drift check cannot detect finding #3's drift, and reports
false confidence.** `chunk-done`'s `domains-composed` field is deliberately *not* self-reported —
per `kernel.md`, it's written by re-running `select()` itself, specifically so a spawn's own
attention isn't the thing standing between "what was recorded" and "what's true." That's a real
improvement over Run 1's snapshot of the system. But it means the ledger has no cross-check against
what the spawn's own handoff says it actually loaded (`domains-loaded:`). This run's
`design-ui-surface` chunk shows it concretely: the handoff for `ui-library-init` honestly recorded
`domains-loaded: [color, surfaces-elevation, visual-hierarchy, motion, design-method,
spawn-integrity, interviewing]` (7 domains — what the phase file actually specifies and what the
spawn actually loaded), while the chunk ledger recorded `domains-composed:` as the full 11-domain
`select()` output for that unit-of-work name — because that's what `chunk-done` computed, not what
happened. `verify-chunks` then reports "every recorded `domains-composed` matches current
`select()`" — true, and useless, because both sides of that check are the same function call. The
mechanism built to catch composition drift is structurally blind to the one composition drift this
project already has, because it verifies internal self-consistency of `select()`, not fidelity
between `select()`'s output and a real spawn's actual load. This wasn't visible in Run 1 because the
chunk ledger didn't exist yet to make the claim "ground truth, not self-reported" — it only became
checkable by literally exercising the machinery this run.

**Real coding bugs, not corpora-process findings, but relevant to what "verification" needs to
mean.** Both were invisible to `tsc --noEmit` and `next build`, which passed cleanly the entire
time — only driving the actual submit flow in a real browser surfaced either:

1. Calling the Server Action through a manually-wrapped `startTransition` handler (rather than
   native `<form action={...}>` dispatch) meant `revalidatePath` ran server-side but the client
   never re-fetched the route's RSC payload — a successfully-posted comment silently never
   appeared. Fixed with an explicit `router.refresh()`.
2. `lib/comments.ts`'s in-memory store started as a plain module-scoped `Map`; in Next.js dev mode,
   the Server Action's compiled module graph and the page-render's compiled module graph obtained
   separate instances of it across Fast Refresh, so a "successful" (200, no thrown error) mutation
   vanished on the next read. Fixed by storing the singleton on `globalThis`.

This is the concrete version of what `kernel.md`'s "passing tools is not evidence" line already
argues for soft principles — extended here to functional correctness itself. `general-operation.md`
does not currently require live-driving a feature before ratifying a coder handoff, only that
verification commands (lint/check/build/test) pass; this run's own coder handoff would have ratified
cleanly on tooling alone, with a comment feature that silently didn't work.

### Net read on the split, after two runs

The process/judgment separation held up structurally across an entire restructuring: `kernel.md`,
`general-operation.md`, and `corpus.py` changed substantially between the two runs, and none of that
churn touched — or needed to touch — a single domain file's content, while every domain file edit
this run made (four new principles, one resolved open question) needed zero script changes to take
effect. That's the architecture working as intended. What a second *literal* run adds beyond
confirming Run 1's three findings unfixed is two sharper ones only visible by actually operating the
machinery: a process-layer side effect that reaches outside the project it runs for (new finding A),
and an anti-drift mechanism that verifies itself rather than the thing it was built to catch (new
finding B) — plus a reminder that "tooling passed" and "the feature works" are not the same claim,
for judgment content and for code alike.
