---
name: corpora:general-operation
description: The orchestrator's session and per-spawn procedure, in order — session entry, routing, spawn composition, execution, relay, the ratify gate, post-gate maintenance, the retrospective, and the architecture scan. Read at the start of every session and followed exactly.
---

# General operation

This is the sequence. `SKILL.md` states what the orchestrator is and the judgment it applies;
this file states the order in which it does things. `kernel.md` is the schema and mechanism
reference each phase below points into.

---

## Phase 1 — Session entry

Every session, before bootstrap checks or routing: load the orchestrator's own domains —
`domains/orchestrator-routing.md`, `domains/ratify-gate.md`, and `domains/principle-judgment.md`
(`SKILL.md`, "## domains"), plus project counterparts if present. The orchestrator is a spawn like
any other; it does not get to skip the load-before-work rule it applies to everyone else.

A monorepo may have more than one `corpora/config.md` (an app-scoped root, or a shared root-level
one). Every `corpus.py` invocation below should pass `--for-file <a file the task touches>` instead
of a hand-picked `--root` — it resolves the governing root itself, nearest-ancestor walk, same
model `tsconfig.json`/`package.json` resolution already use (`kernel.md`, "Monorepo root
resolution"). This is not an extra step to remember: it's just how `corpus.py` gets invoked. The one
case that still needs an explicit check: if a task touches files under more than one root, run
`corpus.py check-root-boundary --files <f1,f2,...>` before composing — `--for-file` only resolves
one path, so a multi-file task can silently pick whichever file happened to be passed first unless
this runs. A spanning task fails there and routes as two units of work, one per root, rather than
one spawn straddling both. `--root` stays available for the one thing `--for-file` structurally
can't do: bootstrapping a brand-new nested root, whose `corpora/config.md` doesn't exist yet to
resolve to.

If `corpora/config.md` exists, run the bundled ledger check before routing spawn work:
`python3 <skill-directory>/scripts/corpus.py --for-file <touched-file> verify`. Resolve the skill
directory from `SKILL.md`, not from the project working directory. Surface any discrepancy to the
operator and never repair or re-baseline it automatically; the check informs rather than blocking
unrelated work, but do not perform corpus write-back while its ledger is inconsistent.

For UI projects, also run `corpus.py lint-deferred` and `corpus.py deferred`; surface malformed
entries and consider the active queue during routing. For every managed project, run `corpus.py
lint-deterministic-shortcut-candidates` and `corpus.py deterministic-shortcut-candidates`;
malformed or recurring candidates must remain visible.

When running under Codex, if the managed project has no `AGENTS.md` instruction that activates
`$corpora`, include this single non-blocking line on entry: "Corpora can auto-activate here; ask me
to add its one-line opt-in to AGENTS.md." Do not show the note under Claude Code or after the
opt-in exists. If asked to opt in, add: `Use the $corpora skill for coding, planning, design, and
review work in this project.`

If `corpora/config.md` does not exist, the project is not bootstrapped. Run bootstrap first — this
is the only fallback; no domain or composition carries other "if missing" logic:

- **Phase 1 (inline):** read the bundled `processes/bootstrap.md`, then follow its
  own Phase 1 — detect the project's shape and commands from the applicable project agent
  instructions, package manifests, lockfiles, and codebase, and detect existing project utilities
  directly; write `corpora/config.md`. Do not proceed until it exists.
- **Routing after Phase 1:** see `processes/bootstrap.md`, "Routing after Phase 1," for the full branch —
  summarized here. If no concrete operator feature request accompanied the bootstrap, route
  `processes/bootstrap.md`'s Phase 2 (only if `has-ui: yes`: `processes/ui-library-init.md`'s composition, divergent
  stance) then Phase 3 and Phase 4 (only if `has-ui: yes`, after Phase 2, order-independent of
  each other: `processes/screenshot-library-init.md`, mechanical, and `processes/ux-library-init.md`'s composition,
  convergent stance) directly, exactly as any other spawn workstream — ratify each as usual
  through Phase 6, below. If `has-ui: no` and no feature request, Phase 1 was the whole job. If a
  concrete feature request *did* accompany the bootstrap, skip the direct Phase 2–4 spawns and
  instead route a **planner** workstream with a capability description combining the bootstrap
  need and the feature request; execute the resulting queue (which may include
  `bootstrap-ui-library`/`bootstrap-screenshot-library`/`bootstrap-ux-library` tasks using
  `processes/ui-library-init.md`/`processes/screenshot-library-init.md`/`processes/ux-library-init.md` as their task content,
  sequenced ahead of the feature's own tasks) per Phase 2 onward, task by task.

---

## Phase 2 — Routing

For every unit of work, before spawning: decide `stance`, `unit-of-work`, and whether to run it
inline, resume an existing agent, or start an isolated spawn. This decision is judgment, not
process — `SKILL.md`'s "What you do" and the `orchestrator-routing` domain state how to weigh it.
What this phase requires mechanically is only the shape of the output: a routing decision must
produce a `stance`, a `unit-of-work` value, and an inline/resume/isolate choice before Phase 3 can
start.

Frame what the spawn is being asked to answer before spawning; if that framing reveals ambiguity,
ask one clarifying question first.

---

## Phase 3 — Spawn brief and composition

0. When spawning multiple agents that will each need to understand the same codebase structure, run
   codebase discovery (file listings, key greps) once and paste the findings directly into each
   agent's prompt — this is orchestrator procedure, not domain judgment, so it isn't gated behind any
   composed domain. Each agent starts cold and would otherwise pay discovery tokens independently.
1. Write the spawn brief (`kernel.md`, "The spawn brief"): `stance:` and `unit-of-work:` from
   Phase 2's routing decision, then `domains:` — run `scripts/corpus.py select --unit-of-work <u>`
   rather than asserting the subset freehand; it evaluates every domain's frontmatter against the
   project's `corpora/config.md` and returns the composed set, plus `expected-output:`. For each
   domain in the composition, load its working file (`corpora/domains/<domain>.md`) — a project's
   own `corpora/domains/` is the whole domain set; there is no separate seed layer to also load
   (`kernel.md`, "Project corpora"). Starting without the full composition is a bug — the spawn
   starts with missing judgment. The spawn reads `corpora/config.md` itself; if absent, surface
   that the project needs `corpora:bootstrap` rather than starting into a vacuum. Hold on to this
   `unit-of-work:` value and the workstream id — Phase 6's chunk-close step needs both, and neither
   is recoverable from the handoff alone (the handoff carries `stance:` and `workstream:`, not
   `unit-of-work:`).
2. Prompt structure: [`kernel.md`'s "Generative stance" section for the composed stance] +
   `## Domains` + [each composed domain's full working content] + [kernel.md's "The
   handoff artifact" section, inlined] + `## Task` + task description + relevant context. Build
   this with `scripts/corpus.py compose-spawn-prompt --stance <s> --domains <d1,d2,...>
   --task-file <path>` rather than hand-assembling it: the command
   concatenates each piece byte-for-byte with no generative or summarization step, so there is no
   place for compression to sneak in as a session's context accumulates. It always prints the
   composed prompt to stdout; read that output yourself and paste its content into the spawn — do
   not point the spawn at a file, for the same reason domains are inlined rather than referenced: a
   spawn told to read a file it thinks it knows may shortcut the read and pattern-match a near-miss
   envelope. Passing `--output <path>` also saves a copy to that path, always. With no `--output`,
   the command additionally saves its default copy under `corpora/session-prompts/` only when
   `corpora/config.md` sets `debug: yes` — otherwise nothing is written to disk, since the saved
   copy is a pure audit trail with no role after the paste. Include prior spawn output as its structured
   artifact, not raw transcript, appended after the task. Never include the other stance's frame or
   an undeclared domain — the seam is enforced here. Full injection is a load-completeness
   guarantee. Its duplicate token cost is tolerated, not desired, and must not be treated as
   corpus-size control; govern corpus growth separately.
3. Append the token usage summary request to every new isolated spawn (`spawn-token-summary` in
   `ratify-gate`).

**Inline spawn work** takes the same brief without the prompt-composition mechanics: load the
composed stance frame, every domain in the composition (seed + `corpora/domains/<domain>.md` if it
exists), and kernel.md's "The handoff artifact" section into the current session before starting.
State what was loaded in one line before starting (`Loaded: <stance>, <domains>`) — a silent load
is unverifiable; the spawn brief is the check.

---

## Phase 4 — Execution

The composed spawn does the work under its stance and domains. A spawn may autonomously create
scope-bounded workers within its assigned task and stance; work results return to the parent.
Questions, tradeoffs, proposals, violations, and routing requests belong to the orchestrator: the
worker sends that orchestration envelope directly when the runtime permits, otherwise the parent
relays it verbatim under `Delegated handoffs`. The parent may synthesize work results but never
filter, ratify, or silently resolve that envelope. Its handoff records the worker scopes. A worker
does not delegate again, and a spawn does not instantiate another corpora spawn; route
cross-composition or deeper delegation requests to the orchestrator.

Before writing its handoff, the spawn re-reads its output against the composed domains and revises
any violation found (`kernel.md`, "The handoff artifact"). Passing tools (lint, typecheck, tests)
is not evidence this happened — tooling only catches hard errors, not soft principles with no
mechanical enforcement.

If the work includes a runtime-observable surface, this checkpoint also requires
`processes/runtime-verification.md` — driving the real surface and observing the actual result, not
re-running the same static checks. Passing tools is not evidence of runtime correctness either;
`domains/testing.md` exists because that distinction shipped two real bugs in one session before it
did.

The spawn's terminal output is the handoff artifact: one file per spawn session, written at
`corpora/handoffs/<date>-<composition>-<slug>.md` per the schema in `kernel.md`, "The handoff
artifact." The spawn's own final conversational turn is not a second copy of it — a path and a
one-line status only.

---

## Phase 5 — Relay

4. Relay the handoff artifact — the `Artifact` section for approval before passing to the next
   spawn, and the `Surfaced` section to the operator **verbatim**, always. Read the handoff from the
   file the spawn wrote (`kernel.md`, "The handoff artifact"); do not expect or rely on the spawn's
   own final conversational turn to restate the content — that turn is a terse pointer only, by
   design, so the content is never generated twice.
5. If `status: questions-pending`: relay the questions verbatim, collect the operator's answers,
   and **continue the same agent** so working context survives — this returns control to Phase 4,
   not to Phase 2. This is the direction-question channel: any composed spawn can ask, when the
   question is real.
6. If the artifact carries a `tradeoffs` block: relay to operator — implement as specced, accept
   alternative, or send back to the relevant upstream spawn.
7. If `status: blocked` and `Surfaced` names scope divergence — the task grew to cover materially
   different or additional concerns than originally scoped, not merely a context-pressure tell or a
   genuine open question (`spawn-integrity`'s `periodic-scope-and-integrity-checkpoint`) — decide
   between two responses, using judgment: route the remaining work to a planner for
   re-decomposition when its shape is still unclear or spans multiple further unknowns, or refile
   the remaining scope directly as one or more fresh, narrowly-scoped coder tasks when the split is
   already obvious from the spawn's own account. Never simply resume the same spawn, or a
   replacement, on the full original scope as if nothing changed — that re-attempts the exact
   bundling mistake that caused the stop.

---

## Phase 6 — Ratify gate

Runs immediately after each spawn, by default.

1. **Audit the output against existing principles.** Read the spawn's output against each ratified
   principle in the domains it declared; flag violations (output contradicts a rule under its
   stated condition) to the operator. Do not silently correct — the operator decides whether to
   send back or accept the deviation. Classify each audited principle now (fired / violated /
   idle); lint the handoff with the bundled `scripts/corpus.py`, resolving it from this skill's
   directory rather than the project working directory: `python3 <skill-directory>/scripts/corpus.py
   lint-handoff <file>`. Resolve every shortened `corpus.py` command below to that same bundled
   script. Each ratified proposal's write-back (step 6, below) already records its own `ratified`
   count as part of that same write — after every proposal in the gate has been processed, one
   closing call folds in whatever write-back didn't cover: `corpus.py record-gate --domain <d>
   --ratified 0 --killed N --violations N [--ui-drift] --fired <ids> --violated <ids> --idle
   <ids>`. Never write the counters block by
   hand — not even when creating a fresh audit file (`kernel.md`, "Storage: working vs audit").
   Also re-apply `principle-judgment`'s genuine-fork test and knowledge-vs-judgment distinction to
   each proposal yourself here, even though `spawn-integrity`'s `proposal-self-cleanup-before-including`
   already asked the spawn to do this — that self-cleanup is not guaranteed to fire correctly every
   time. Fix rule/condition/reason field-bleed directly rather than presenting it broken; flag
   (don't silently reject) anything that fails the fork test outright, with your own assessment when
   asked. This is a named step here, not left implicit, because `principle-judgment` being loaded
   every session does not guarantee it gets applied under session momentum.
2. **Check reading candidates.** If `reading/candidates.md` in the corpora skill repo has entries
   whose `domains` match a domain this project declares, surface them alongside session proposals,
   marked `[reading pipeline: <source URL>]`. Same ratify/kill decision; ratified or killed
   entries are removed from `candidates.md`. Also check `reading/queue.md` for any `status:
   fetch-failed` entries — surface each to the operator verbatim: the source URL, `error:`, and the
   exact expected save path (`reading/saved/<id>.html`, per `reading/saved/README.md`) so they know
   precisely where to drop a copy with no further status edit needed. This is the reading agent's
   hard-stop-on-fetch-failure guard reaching the operator, not a routine status to skip past.
   `candidates.md` and `queue.md` are populated by three separate, self-contained agents this gate
   step never runs itself: `reading/discovery-agent.md` (scheduled, finds sources),
   `reading/reading-agent.md` (scheduled, extracts candidates from queued sources), and
   `reading/session-harvest-agent.md` (operator-triggered, mines past session transcripts for
   judgment that was exercised but never proposed) — this step only consumes what they produce.
3. **Persist deterministic shortcut candidates.** For every `deterministic-shortcut-candidates` entry, match by operation shape
   against `corpora/deterministic-shortcut-candidates.md`, then call `corpus.py record-deterministic-shortcut-candidate` before
   closing the handoff (`corpus.py handoff-done`). Surface it to the operator for accept / deny / defer and persist that
   judgment with `corpus.py set-deterministic-shortcut-status`. The script derives counts and dates and identifies
   recurrence. Acceptance authorizes a scoped coder
   workstream, not config registration; register it only after implementation and tests prove useful.
4. Present proposals from the handoff envelope's `proposals` field (rule, condition, reason,
   provenance, kind). Surface the `kind` the spawn captured — do not re-evaluate it. `judgment` =
   decision under uncertainty; `knowledge` = derivable from documentation or training (see
   `ratify-gate-judgment-vs-knowledge`); `direction` = a project design-direction choice (third
   route, next step). If a proposal's provenance names a reading-pipeline source rather than an
   earned incident, flag that alongside it — a real correlation with knowledge-not-judgment risk
   (`reading-pipeline-provenance-flags-knowledge-risk` in `principle-judgment`). Ask: ratify / reject / edit
   — **per proposal, every time, no exceptions.** Do not write a proposal back to a domain file,
   write its provenance to the audit file, or call `record-gate` for it until the operator has given
   an explicit answer for that specific proposal in this specific gate. A prior gate's approval —
   in this session or any other — is never implicit approval for a new proposal, even one that looks
   obviously fine: "ask once" scopes to that one proposal, not to the rest of the session.
5. **Assign a home.** A `direction` proposal is filed into the project's `ui-library.md`, describing
   only current state — never into a domain, never killed, never a seed candidate, and never with
   an inline provenance/history note (git history is the library's audit trail; no parallel
   audit file exists for it) (`kernel.md`, "The ratify gate"). For each ratified *principle*, decide its domain — citing
   specifically how it matches that domain's stated subject (`kernel.md`, "Domain assignment at
   the gate") — and write it there; if none fits, create a new domain working file
   (`corpora/domains/<new>.md`, or a seed domain if general). The domain becomes available to any
   spawn whose stance and subject match — there is no composition declaration to add it to. A proposal
   spanning two domains is a possible domain-boundary problem — surface it rather than
   fragmenting. See `domain-assignment-at-ratify-gate`.
6. **Write-back** per `kernel.md`, "Write-back format." Ratified (or edited — write the operator's
   edited version) → `corpus.py add-principle --domain <d> --id <id> --rule ... --condition ...
   --reason ... --provenance ... [--kind ...]` for a freshly-authored or mined proposal, or
   `corpus.py ratify-import-candidate --id <id> --as-domain <d> [--as-id ...]` for one sourced from
   `reading/candidates.md`/`corpora/import-candidates.md` — either writes the working fields into
   the target domain, files the provenance in that layer's `domains/audit.md`, and records the
   proposal's own `ratified` count, atomically; no hand edit to either file. Rejected → append to
   the domain working file's `killed:` log by hand with an `id`, `kill_type` (`quality` |
   `container` | `attribution-noise`), and `reason_killed`; per-kill provenance to the audit file —
   this path has no script yet.
7. **Resolve deferred decisions.** For any `corpora/deferred-decisions.md` entry this handoff's
   ratified write-back settles, mark it `status: resolved` and remove it — this is the step the
   ratification in steps 4–6 actually authorizes; a proposal presented but rejected or edited away
   from what the deferred question needed does not resolve it. Run `corpus.py lint-deferred` after
   editing. Durable direction and judgment live in the UI/UX libraries and corpora now, not this
   queue — do not let a resolved item linger here as if the queue were the record.
8. If the operator defers review, the unratified handoff file *is* the queue — leave it in
   `corpora/handoffs/`; a directory of lingering handoffs is a visible backlog. Once a handoff's
   proposals are ratified/killed and written back, **close its chunk before closing the handoff
   file** (`kernel.md`, "Chunk chaining"): `corpus.py chunk-done --workstream <w> --unit-of-work <u>
   --stance <s> --handoff <file> [--next <u>]`, using the handoff's own `workstream:`/`stance:`
   fields and the `unit-of-work:` held from Phase 3, step 1 — `chunk-done` fails if the handoff file
   no longer exists, so this order is load-bearing, not stylistic. It also fails if the handoff's
   `domains-loaded:` doesn't match what `select()` recomputes for `<u>` — a real discrepancy to
   investigate (fix the composing process or the spawn), never a mismatch to paper over by hand-
   editing the ledger (`kernel.md`, "Chunk chaining"). Only then close the handoff:
   `corpus.py handoff-done <file>`. By
   default this deletes it; when `corpora/config.md` sets `debug: yes`, it archives the file to
   `corpora/handoffs/archive/` instead so the operator can audit past handoffs — the archive is not
   part of the pending backlog. A unit-of-work whose inline session produced no handoff at all (the
   zero-proposals/zero-tradeoffs/no-drift exemption, `kernel.md`, "The handoff artifact") has
   nothing for `chunk-done` to point at either — it stays unchunked, same as it stays
   un-handed-off, and the session-harvest pipeline is the backstop for both.
9. **Check triggers.** `record-gate` prints fired triggers automatically (or run `corpus.py
   triggers`). Relay any that fire as suggestions to the operator. Suggestions only.
10. Commit the corpus — domain working files and the audit file together — alongside the code
    change so they don't drift. Run `corpus.py verify` first; a discrepancy means a gate went
    unrecorded — heal it with a retroactive `record-gate` before committing.

Loop: return to Phase 2 for the next unit of work.

---

## Phase 7 — Post-gate maintenance

Three sync processes trigger from within Phase 6 and may themselves open a new workstream — an
edge back to Phase 2, not a continuation of the gate that produced them. Each is its own file;
this phase is only the trigger point they share.

**`processes/ui-library-sync.md`** — direction filings already update `ui-library.md` directly at the gate
(Phase 6, step 5); this is for the coder-side drift a single filing doesn't close.
`library-drift.since-last-sync ≥ 3`, or a drifting change that retired something the library still
teaches, suggests running it.

**`processes/screenshot-library-sync.md`** — right after processing any handoff whose `ui-drift.screens` or
`.components` is non-empty, not on a threshold. Mechanical; never spawns a design composition.

**`processes/ux-library-sync.md`** — has no mechanical trigger today; see that file for why, and for the
judgment-based trigger it runs on in the meantime.

---

## Phase 8 — Retrospective

See `processes/retrospective.md` for the full trigger, composition, and procedure. This phase runs on its
own periodic trigger, not as part of the per-unit-of-work loop above — `retrospective <domain>` (or
`retrospective <composition-name>`, covering every domain that composition loads) is an operator
command, not something Phase 6 ever routes into automatically.

---

## Phase 9 — Architecture scan

See `processes/architecture-scan.md` for the full trigger, composition, and procedure. Same standalone
posture as Phase 8: `architecture-scan [target]` is an operator command, never a mechanical trigger
— it scans the managed project's own code rather than corpora's corpus, so the case for staying
non-automatic is at least as strong as retrospective's.
