---
name: corpora
description: "Corpora — a queryable judgment service and ratify-gate procedure for a design+coding system. Given a task or spawn description, it answers which stance and domain subset applies, and hands back that composed content. It has no initiative of its own: it does not decide when to ask this question, whether to spawn, whether to go inline vs. isolated, or how to sequence a session — that's process/timing judgment owned by whoever is driving (direct execution by default, or praxis's phase router when installed). One flat domain pool; each domain states its own load condition against the project's config (language, framework, styling, has-ui). Entry is always through a task description, not a bypass — stance and domains are derived fresh every time."
---

# Corpora

A queryable judgment service for a portable spawn-composition system. A **spawn** is a *stance*
(convergent or divergent) plus a **composition** — whoever is driving states stance and domain
subset directly from the task at hand, every time; judgment lives in domains, not fixed roles or a
cached naming layer between task and domains. `kernel.md` is the canonical reference: schema,
stance+composition model, generative stance, ratify gate, write-back, handoff artifact,
retrospective.

**Corpora has no initiative of its own, in any configuration.** It does not decide when to query
itself, whether a task warrants a spawn at all, whether to run inline vs. isolated, or how to
sequence a session — none of that is corpora's concern, standalone or alongside praxis. What it
does:

1. **Answers a composition query.** Given a task or spawn description, states which stance
   (convergent/divergent) and which domain subset apply, and hands back that composed content —
   the stance frame plus every composed domain's working file, in full.
2. **Runs the ratify-gate procedure, on request.** Audits a spawn's output against ratified
   principles, classifies each as fired/violated/idle, presents proposals for ratify/reject/edit,
   and writes ratified or killed principles back to the domain files plus the audit ledger.
3. **Maintains its own bookkeeping ledgers, on request.** Deferred UI/UX decisions,
   deterministic-shortcut candidates, the screenshot cache manifest, and UI-library sync.

Whatever is driving a session decides *when* to invoke 1, 2, or 3 — direct execution by default (an
agent working a task with no special apparatus), or praxis's phase router when praxis is installed,
per whichever phase's own `invocations` field names corpora. `orchestrator-routing` was corpora's
former domain for exactly this kind of judgment — retired 2026-07-28 once corpora stopped acting as
an active orchestrator; see `LINEAGE.md`, "Corpora stops being an active orchestrator," for the full
redistribution of that domain's content.

**One flat domain pool.** All seed domains — stack-agnostic (`coding-general`, `ratify-gate`,
`principle-judgment`, `planning`, `interviewing`, `spawn-integrity`) and stack-specific
(`coding-ts`, `coding-react`, `coding-nextjs`, `css`, and the design domains) alike — live together
in `domains/`, with one `domains/audit.md` for the layer. There is no separate "role pack" layer
selected by a project-config field: each stack-specific domain states its own load condition
directly against `corpora/config.md`'s existing shape fields in its own preamble (`coding-nextjs`
loads when `framework: nextjs`, `css` loads when `styling` is not `none`, and so on) — retired
2026-07-22, see `kernel.md`, "One flat seed layer," for why the old `role-pack:` field added an
indirection without adding information.

Corpora itself declares two standing domains, always loaded before it answers any query or runs the
ratify gate: **`ratify-gate`** (assembling a complete spawn and processing what it returns) and
**`principle-judgment`** (whether a proposed or ratified principle is genuine judgment and lives in
the right domain). Every other composition — coding, planning, design, dependency migration — is
composed the same way: stance plus whatever domain subset the task needs, decided fresh each time by
whoever is querying corpora — there is no fixed composition file for any recurring task shape. One
composed spawn per recurring task shape runs at a time per project; a domain splits into scoped
instances only when a retrospective surfaces a fork signal from a domain's own accumulated tension
(see `kernel.md`), never by importing an org chart up front.

There is no bare-spawn entry and no named arg that maps to a pre-built composition. Entry is always
through a task description: state stance + whichever domains that task shape needs (seed + same-named
project domains), the same way for every query.

**Step 0, every time corpora is queried or its ratify gate is run:** load corpora's own domains —
`domains/ratify-gate.md` and `domains/principle-judgment.md`, plus project counterparts if present.
Corpora is a spawn like any other; it does not get to skip the load-before-work rule it applies to
everyone else.

## Spawn loads and context boundaries

Composition-level, unconditional: a spawn's assembled load is its stance frame (`kernel.md`,
"Generative stance") plus its composed domains — **nothing from another stance and no undeclared
domain**. A convergent implementation spawn loads coding domains and never design domains. Whether
that load enters a fresh or shared context — inline, resumed, or isolated — is process/timing
judgment owned by whoever is driving the session (direct execution's own judgment, or praxis's phase
router when installed); it is not corpora's decision to make. History lives in LINEAGE.md, "Role
isolation" and "Orchestrator as process."

Any switch from one composition to another — in either direction, between any two spawns — is a
load event in its own right, not satisfied by an earlier load in the same session. Reload the new
composition's stance frame + domains at the switch, every time, including the second, third, or Nth
switch.

## Project shape

Before composing any spawn, if `corpora/config.md` exists, run the bundled ledger check:
`python3 <skill-directory>/scripts/corpus.py --root <project-root> verify`. Resolve the skill
directory from this `SKILL.md`, not from the project working directory. Surface any discrepancy to
the operator and never repair or re-baseline it automatically; the check informs rather than
blocking unrelated work, but do not perform corpus write-back while its ledger is inconsistent.
For UI projects, also run `corpus.py lint-deferred` and `corpus.py deferred`; surface malformed
entries and consider the active queue when composing new work.
For every managed project, run `corpus.py lint-deterministic-shortcut-candidates` and
`corpus.py deterministic-shortcut-candidates`; malformed or recurring candidates must remain visible.

When running under Codex, if the managed project has no `AGENTS.md` instruction that activates
`$corpora`, include this single non-blocking line on entry: “Corpora can auto-activate here; ask me
to add its one-line opt-in to AGENTS.md.” Do not show the note under Claude Code or after the opt-in
exists. If asked to opt in, add: `Use the $corpora skill to compose judgment for coding, planning,
design, and review work in this project.`

Every spawn reads `corpora/config.md` at the start of its work. It carries:

- **Project shape** — language, framework, package manager, `has-ui`, styling. Each stack-specific
  domain checks these fields directly to decide whether it applies to this project; `has-ui`
  additionally governs whether the design domains are ever composed into a spawn at all.
- **Project utilities and commands** — project-owned deterministic tools that replace recurring
  inference, UI/UX library locations, and verification commands. Environment-owned capabilities
  such as browser automation, image generation, and agent delegation are discovered from the
  current runtime rather than persisted here.
- **`debug`** — optional, operator-set, defaults to no. Gates two audit-trail writes that otherwise
  don't happen: `compose-spawn-prompt`'s default saved copy under `corpora/session-prompts/`, and
  retaining a ratified handoff under `corpora/handoffs/archive/` instead of deleting it (`corpus.py
  handoff-done`). See `bootstrap.md`, "The config file," and `kernel.md`, "The handoff artifact."

If `corpora/config.md` does not exist, the project is not bootstrapped. Run bootstrap first — this
is the only fallback; no domain or composition carries other "if missing" logic:

- **Phase 1 (inline):** read the bundled `bootstrap.md` adjacent to this `SKILL.md`, then follow
  Phase 1 — read shape and verification commands from `praxis/config.md` if it already exists,
  otherwise detect the project's shape and commands from the applicable project agent instructions,
  package manifests, lockfiles, and codebase; detect existing project utilities directly either way;
  write `corpora/config.md`. Do not proceed until it exists.
- **What happens after Phase 1** is a routing decision — whether to run Phases 2/3 directly or via a
  planning/decomposition workstream — owned by whoever is driving, not by corpora itself; see
  `bootstrap.md`, "Routing after Phase 1," for the content those phases invoke either way.

Before any spawn work, for each domain the composition includes, load the seed working file
(`domains/<domain>.md` in the kernel or pack) then the project working file
(`corpora/domains/<domain>.md`) if it exists — apply seed + project principles together.

---

# Querying corpora: composing a spawn

Given a task description, state its `stance:` and `domains:` in a short, fixed-field brief
(`kernel.md`, "The spawn brief") — the schema structures the envelope, not the thinking; no
decision-procedure is baked into the schema for *how* these values are picked, that judgment
accumulates the normal way through the `ratify-gate` domain's own principles.

```yaml
stance: divergent
domains: [color, visual-hierarchy, motion]
expected-output: "Design spec for the settings-panel color treatment."
```

For each domain in the composition, read the seed working file plus the project's
`corpora/domains/<domain>.md`. Starting without the full composition is a bug — the spawn starts
with missing judgment. The spawn reads `corpora/config.md` itself; if absent, surface that the
project needs `corpora:bootstrap` rather than starting into a vacuum.

**Assembling the prompt:** [`kernel.md`'s "Generative stance" section for the composed stance] +
`## Domains` + [each composed domain's seed + project working content] + [kernel.md's "The
handoff artifact" section, inlined] + `## Task` + task description + relevant context. Build this
with `scripts/corpus.py compose-spawn-prompt --stance <s> --domains <d1,d2,...> --task-file <path>`
rather than hand-assembling it: the command concatenates each piece byte-for-byte with no
generative or summarization step, so there is no place for compression to sneak in as a session's
context accumulates. It always prints the composed prompt to stdout; read that output and paste its
content into the spawn — do not point the spawn at a file, for the same reason domains are inlined
rather than referenced: a spawn told to read a file it thinks it knows may shortcut the read and
pattern-match a near-miss envelope. Passing `--output <path>` also saves a copy to that path,
always. With no `--output`, the command additionally saves its default copy under
`corpora/session-prompts/` only when `corpora/config.md` sets `debug: yes` — otherwise nothing is
written to disk, since the saved copy is a pure audit trail with no role after the paste. Full
injection is a load-completeness guarantee (`full-corpus-on-spawn`, `ratify-gate`); its duplicate
token cost is tolerated, not desired, and must not be treated as corpus-size control — govern corpus
growth separately.

Append the token usage summary request to every new isolated spawn (`spawn-token-summary` in
`ratify-gate`): "At the end of your output, add a `### token usage` section listing: every file you
read and its approximate line count, how many corpus principles you referenced, and your estimate
of the single heaviest cost item."

**Delegation within a spawn:** A spawn may autonomously create scope-bounded workers within its
assigned task and stance. Work results return to the parent. Questions, tradeoffs, proposals,
violations, and routing requests belong to whoever is driving the session: the worker sends that
orchestration envelope directly when the runtime permits, otherwise the parent relays it verbatim
under `Delegated handoffs`. The parent may synthesize work results but never filter, ratify, or
silently resolve that envelope. Its handoff records the worker scopes. A worker does not delegate
again, and a spawn does not instantiate another corpora spawn.

**Processing a completed spawn's output:**

- Read the handoff from the file the spawn wrote (`kernel.md`, "The handoff artifact"); do not
  expect or rely on the spawn's own final conversational turn to restate the content — that turn is
  a terse pointer only, by design, so the content is never generated twice.
- If `status: questions-pending`: relay the questions verbatim, collect answers, and **continue the
  same agent** so working context survives. This is the direction-question channel: any composed
  spawn can ask, when the question is real.
- If the artifact carries a `tradeoffs` block: relay it to whoever can decide — implement as
  specced, accept an alternative, or send back to the upstream spawn.
- Relay the handoff's `Artifact` section for approval before passing to the next spawn, and the
  `Surfaced` section verbatim, always — never filtered or summarized.

---

# The ratify-gate procedure

Invoked after spawn work, whenever whoever is driving decides to run it. If the project runs praxis,
its `phases/ratify-checkpoint.md` may batch this procedure across multiple spawns' proposals into
one gate pass instead of running it immediately after each spawn — sequencing is praxis's job when
the project runs it. The procedure below stays exactly the same either way; only its trigger timing
changes. Absent any process layer sequencing it, run it immediately after each spawn, the same
default it has always had.

1. **Audit the output against existing principles.** Read the spawn's output against each ratified
   principle in the domains it declared; flag violations (output contradicts a rule under its
   stated condition) to the operator. Do not silently correct — the operator decides whether to
   send back or accept the deviation. Classify each audited principle now (fired / violated / idle);
   lint the handoff with the bundled `scripts/corpus.py`, resolving it from this skill's directory
   rather than the project working directory: `python3 <skill-directory>/scripts/corpus.py
   lint-handoff <file>`. Resolve every shortened `corpus.py` command below to that same bundled
   script. The counts are recorded by the script *after write-back* (step 6), once the ratify
   numbers exist: `corpus.py record-gate --domain <d> --ratified N --killed N --violations N
   [--ui-drift] --fired <ids> --violated <ids> --idle <ids>`. Never write the counters block by
   hand — not even when creating a fresh audit file (`kernel.md`, "Storage: working vs audit").
2. **Check reading candidates.** If `reading/candidates.md` in the corpora skill repo has entries
   whose `domains` match a domain this project declares, surface them alongside session proposals,
   marked `[reading pipeline: <source URL>]`. Same ratify/kill decision; ratified or killed
   entries are removed from `candidates.md`. Also check `reading/queue.md` for any `status:
   fetch-failed` entries — surface each to the operator verbatim: the source URL, `error:`, and the
   exact expected save path (`reading/saved/<id>.html`, per `reading/saved/README.md`) so they know
   precisely where to drop a copy with no further status edit needed. This is the reading agent's
   hard-stop-on-fetch-failure guard reaching the operator, not a routine status to skip past.
3. **Persist deterministic shortcut candidates.** For every `deterministic-shortcut-candidates`
   entry, match by operation shape against `corpora/deterministic-shortcut-candidates.md`, then
   call `corpus.py record-deterministic-shortcut-candidate` before closing the handoff (`corpus.py
   handoff-done`). Surface it to the operator for accept / deny / defer and persist that judgment
   with `corpus.py set-deterministic-shortcut-status`. The script derives counts and dates and
   identifies recurrence. Acceptance authorizes a scoped implementation workstream, not config
   registration; register it only after implementation and tests prove useful.
4. Present proposals from the handoff envelope's `proposals` field (rule, condition, reason,
   provenance, kind). Surface the `kind` the spawn captured — do not re-evaluate it. `judgment` =
   decision under uncertainty; `knowledge` = derivable from documentation or training (see
   `ratify-gate-judgment-vs-knowledge`); `direction` = a project design-direction choice (third
   route, next step). If a proposal's provenance names a reading-pipeline source rather than an
   earned incident, flag that alongside it — a real correlation with knowledge-not-judgment risk
   (`reading-pipeline-provenance-flags-knowledge-risk` in `principle-judgment`). Ask: ratify / reject / edit.
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
6. **Write-back** per `kernel.md`. Ratified → working fields (`rule`/`condition`/`reason`/`status`)
   to the end of `principles:` in the target domain working file; the proposal's `provenance`
   (with its `domain:`) to that layer's `domains/audit.md`. Rejected → append to the domain
   working file's `killed:` log with an `id`, `kill_type` (`quality` | `container` |
   `attribution-noise`), and `reason_killed`; per-kill provenance to the audit file. Edited →
   ratify operator's version.
7. If the operator defers review, the unratified handoff file *is* the queue — leave it in
   `corpora/handoffs/`; a directory of lingering handoffs is a visible backlog. Once a handoff's
   proposals are ratified/killed and written back, close it: `corpus.py handoff-done <file>`. By
   default this deletes it; when `corpora/config.md` sets `debug: yes`, it archives the file to
   `corpora/handoffs/archive/` instead so the operator can audit past handoffs — the archive is not
   part of the pending backlog.
8. **Check triggers.** `record-gate` prints fired triggers automatically (or run `corpus.py
   triggers`). Relay any that fire as suggestions to the operator. Suggestions only.
9. Commit the corpus — domain working files and the audit file together — alongside the code
   change so they don't drift. Run `corpus.py verify` first; a discrepancy means a gate went
   unrecorded — heal it with a retroactive `record-gate` before committing.

---

# Bookkeeping ledgers

Corpora maintains the following ledgers as a service, when asked to — none of them are triggered on
corpora's own initiative; whoever is driving decides when a spawn's output warrants updating one.

**Deferred UI/UX decisions (`corpora/deferred-decisions.md`).** Only queue a UI/UX question when
implementation can proceed with an explicit, narrow, reversible provisional treatment
(`defer-only-nonblocking-design-decisions`, `ratify-gate`). Surface blockers immediately instead.
Group queued items by stance and related surface — not count alone — so a later designer workstream
resolves a coherent surface rather than a grab-bag of unrelated questions. Pass the relevant entries
to whichever spawn eventually resolves them. After the operator ratifies that spawn's handoff,
remove resolved items; do not let the queue become the durable record of a design decision — durable
direction lives in the UI/UX libraries and corpora's own domains.

**Deterministic shortcut candidates.** Surface liberally whenever a spawn's own reasoning trace
shows it narrating its way step-by-step through an exact, deterministic, checkable procedure
instead of simply invoking one; denial is cheap. A candidate needs a concrete operation shape and
the observed narration, not proof of recurrence or a finished CLI design — this is not the same
signal as ordinary code duplication (two files reliably implementing the same low-complexity logic
with no inference being avoided is a code-reuse/promotion matter, not a candidate here). Before
proposing, check the standard library, installed dependencies, current runtime tools, and
registered project utilities. Transfer every candidate from the handoff to
`corpora/deterministic-shortcut-candidates.md` before closing the handoff (`corpus.py
handoff-done`). Record accept, deny, or defer. When the same operation returns, use `corpus.py
record-deterministic-shortcut-candidate` to append evidence and derive its dates and sighting
count; the command reports when it must be resurfaced. Record operator disposition with `corpus.py
set-deterministic-shortcut-status`. Only an accepted, implemented, and tested utility enters
`corpora/config.md`.

**UI library upkeep:** `direction` filings update the library directly at the gate — write the
entry as a standing description of current state, not a copy of the spawn's own narrated
reasoning. A spawn's handoff Artifact legitimately explains its thinking (that's what a freeform
Artifact is for); the library entry written from it is a different, more restricted document that
never inherits that narration — no "(direction, <date>, implemented)" tags, no "supersedes the prior
X" lead-ins, no dates, no naming what was rejected or why. When a direction replaces an existing
entry, overwrite it outright rather than layering the correction on top; the library should never
require reading two versions to know the current one. Implementation-side drift is mechanical:
handoffs self-report `ui-drift`, the gate counts it, and the `library-drift` threshold — or any
change that *retired* something the library still teaches — triggers a sync suggestion:
documentation work against the rendered state, run as a divergent visual-identity spawn. A stale
library silently re-teaches retired decisions; discarded experimental work never reaches a gate, so
exploration never triggers a sync.

**Screenshot cache upkeep:** right after processing a handoff whose `ui-drift.screens` or
`.components` is non-empty, run `corpus.py screenshot-mark-stale --screens <ids> --components
<names>` — it expands `.components` into every screen the manifest's own tags already show it on,
so a spawn never has to enumerate the ripple itself. For each screen the command reports as
invalidated, recapture immediately using the project's browser automation tool and register the
result with `corpus.py screenshot-record`, still inline in the same gate pass — this needs no
design judgment, so it never spawns a design composition (a project running praxis runs this as its
`screenshot-recapture` phase instead; see that phase's Provenance section). If no browser automation
tool is available this session, leave the invalidated screens marked stale; capture is deferred until
a session with the tool processes them.

---

## Retrospective

On `retrospective <domain>` (or `retrospective <composition-name>`, covering its composed domains),
surface domain-tension fork candidates, composition drift, and convergence signals as proposals —
never automatic. This is an **audit-mode load**: the relevant domain working files plus the layer
`domains/audit.md`. See `kernel.md` for the signals. When it completes, run
`corpus.py retro-done --domain <d>` (resets counters, re-baselines tokens); after a UI-library
sync, `corpus.py sync-done`.

---

## domains

stance: convergent

Corpora declares two standing domains of its own: **`ratify-gate`** (assembling a complete spawn
and processing what it returns) and **`principle-judgment`** (whether a proposed or already-ratified
principle is genuine judgment and lives in the right domain) — `domains/ratify-gate.md` and
`domains/principle-judgment.md`, plus each one's `corpora/domains/<name>.md` project counterpart
when it exists. `orchestrator-routing` — corpora's former domain for that process/timing judgment —
was retired 2026-07-28 for the same reason; that judgment now lives with whoever drives a session,
praxis's kernel when it's installed. See `LINEAGE.md`, "Corpora stops being an active orchestrator."
Audit detail loads only at ratify/retrospective time — see `kernel.md`, "Storage: working vs audit."
