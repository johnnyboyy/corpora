# The Role Kernel

The kernel is the shared mechanism every role inherits. It is not code — it is a discipline made
of files plus a loop.

A **role** is a *lens* plus a *declaration*: a domain prompt (the mode of reasoning the agent
applies) and a static list of the **domain corpora** it loads. Roles do not own corpora. Judgment
lives in domains; a role is the lens through which one or more domains are applied to a task.

A **domain corpus** is a list of principles about one subject matter, context type, or decision
class — not a job title. Multiple roles may declare the same domain, so shared judgment lives
once. Domain boundaries are *discovered from accumulated tension* (the fork signal in the
retrospective), never declared up front from how a team would be organized.

---

## The principle schema

A domain corpus is a list of **principles**. Every principle has four required fields plus optional ones:

```yaml
principle:
  id: kebab-case-identifier
  rule: # WHAT. The judgment itself, stated as guidance.
  condition: # WHEN it applies. The scope. Be specific enough that two principles
             #   with overlapping conditions don't silently contradict each other.
  reason: # WHY. The justification that generalizes. This is the most important field —
          #   it lets the principle be weighed against the present case rather than
          #   obeyed mechanically. A rule without its reason is dogma.
  provenance: # WHERE it came from. Date, task, context. For audit and trust.
  see-also: # OPTIONAL. ids of related principles (same domain or another domain).
```

Notes on fields:

- **condition** is structurally the most important. When two ratified principles in a domain have
  conditions that partition the same space and give opposing advice, the corpus is telling you the
  domain has become two — a fork candidate.
- **reason** travels with the rule always. This is what lets the role think rather than pattern-match:
  "the reason was X; this task is Y, so the rule doesn't bind here."
- **provenance** is cheap to record and invaluable for trusting or retiring a principle later.
- A principle does not name its domain in a field — the domain is the *file* it lives in. Moving a
  principle to a better-fitting domain is a file move, recorded in the audit `history`.

### Storage: working vs audit

Working and audit metadata are split so a role's working context carries only the fields it weighs
during a task. **File granularity matches load granularity:** working files are per-domain because
the working load is *selective* (only declared domains); audit metadata is one file per layer
because the audit load is *broad* (the orchestrator pulls the whole layer at once).

- **Working file** (`domains/<domain>.md`) — one per domain. The active `principles:` with their
  `id / rule / condition / reason / see-also`, plus the `killed:` log. This is the only
  part loaded when a role works, inline or spawned.
- **Audit file** (`domains/audit.md`, one per layer — kernel-seed, each pack, and each project) —
  per-principle `provenance` keyed by `id` (each entry noting its `domain`), the `promoted:` block,
  and per-kill audit metadata. Loaded only at ratify and retrospective time, by the orchestrator —
  never in a role's working context. The audit file also carries the layer's **counters** — the
  mechanical signals that replace operator feel. **Never write or edit these by hand, including
  when creating a fresh audit file**: `scripts/corpus.py` alone creates them (`measure`) and
  updates them (`record-gate`), inside a marker-delimited block it owns. Shown here for
  reference only:

  ```yaml
  counters:
    - domain: coding-general
      since: 2026-06-20            # last retrospective
      ratified: 3                  # new principles since
      killed: 1
      gate-violations: 2           # violations flagged at ratify-gate audit passes
      working-file-tokens: 3100    # measured at the most recent gate
      baseline-tokens: 2100        # measured at the last retrospective (growth reference)
      principles-at-baseline: 12   # entry counts at the last retrospective — ground truth
      kills-at-baseline: 4         #   for `verify` (ledger must reconcile with the files)

  efficacy:                        # per-principle, incremented at each gate's audit pass
    - id: some-principle
      fired: 4                     # was relevant and the output followed it
      violated: 1                  # was relevant and the output contradicted it
      idle: 9                      # domain was loaded, principle never relevant

  library-drift:                   # project layer only, when has-ui: yes
    since-last-sync: 2             # gates where a handoff carried ui-drift: yes
  ```

  Efficacy counts must never enter a working file — a role that sees them will start writing
  principles that fire often instead of principles that are right. They are audit-layer signals,
  consumed only by the retrospective.

  The script (in the skill repo: `record-gate`, `measure`, `triggers`, `lint-handoff`,
  `lint-deferred`, `deferred`, `lint-utility-candidates`, `utility-candidates`,
  `record-utility-candidate`, `set-utility-status`, `retro-done`, `sync-done`) does all counting,
  measuring, validation, and threshold math. The model supplies
  judgments as arguments — fired/violated/idle classification, ratify counts — and never does the
  arithmetic or the YAML writing. Bookkeeping done by attention is bookkeeping that silently
  stops. Hand-written provenance, promotions, and per-kill detail live in the same file, outside
  the script's markers — that part of the audit file remains the model's to write.

  Completeness is enforced by **reconciliation**, not interception: `corpus.py verify` checks
  that each working file's entry counts equal its baseline plus the gates recorded since — an
  unrecorded gate (or any write that bypassed the gate) surfaces as a named discrepancy. A
  project-level SessionStart hook (`scripts/session-start.sh`) runs `verify` at every session
  start and announces the project as corpora-managed, so an omission at session end — where
  attention is weakest — is caught at the next session start, where it is strongest.

The `killed:` log lives in the working file because it is active guidance — it tells the role what
has already been tried and rejected, prevents the same pattern from re-emerging, and opens new
directions by making the rejection reason visible. Provenance and promotions are audit metadata a
role does not weigh mid-task, so they stay in the audit file.

This is a *storage* split, not a *corpus* excerpt: every active principle and kill entry is still
passed in full with the fields a role reasons over. Working and audit are kept consistent by `id`:
every active `id` in a working file has a `provenance` entry in its layer's audit file, and vice versa.

---

## Roles: lens + declaration

A role file is a **lens** — a prompt establishing the mode of reasoning — followed by a static
declaration of the domains it loads:

```markdown
## domains
stance: convergent        # convergent | divergent — the lens's generative stance (see below)
- coding-general          # always
- coding-js               # when role-pack: web-frontend
- coding-react            # when role-pack: web-frontend
- css                     # when role-pack: web-frontend
```

The declaration is checked into the role file, not computed at runtime. Assembly is therefore a
deterministic, inspectable fact — read the lens, know exactly what loads. An agent never selects
its own constraints; there is no runtime relevance call on a working role's corpus. A domain may
be conditional on the project's `role-pack` (a pack adds domains to a role's declaration; it never
adds a new role).

### Two load modes

- **Working load** (generation): a role's declared domains, *working files only*. Lean and
  inspectable. This is every new isolated role agent and every inline role segment.
- **Audit load** (synthesis, human-gated): the orchestrator loads relevant domains *broadly,
  including audit and kill metadata*, at ratify and retrospective time. Breadth is safe here
  because it is not constrained generation and it is gated by the operator.

Declarations enforce load boundaries: the coder declares coding domains and never design domains.
Whether two role segments may share a context is routing judgment, informed by stance, prior
exploration, evaluator independence, context length, and cost. A handoff captures proposals and
violations at a transition, but is a checkpoint rather than automatic agent termination. See
`SKILL.md`, "Inline, resume, or isolate," and LINEAGE.md, "Role isolation."

### Generative stance

Each lens declares a `stance:` — how it generates. There are two, and they are opposite:

- **convergent** — the value of the output comes from *matching a standard*: correctness, idiom,
  fit. The coder, the UX designer, the planner, and the orchestrator are convergent. For a
  convergent lens, regression toward the training mean is frequently the *right* answer; there is
  no anti-mean anchor.
- **divergent** — the value comes from *differentiating from the standard*: a distinctive identity.
  The UI designer is divergent. A divergent lens carries an **anti-mean anchor**: before committing
  to a direction it must name at least one safe/expected default that should *not* apply, because a
  generative model otherwise drifts to the average of its training data — the forgettable answer.
  (History: LINEAGE.md.)

Stance is a property of the **lens** (the generating agent), not of a domain. Principles, by their
nature — a weighable rule with a condition and a reason — overwhelmingly encode *convergent*
correctness; that is what crystallizes into a rule. The divergent element is a generative *stance*,
not a body of principles. So domains are mostly convergent guardrails, consumed by lenses of either
stance, and the anti-mean anchor lives on the divergent lens and fires at the generative moment.

**The hard line:** a single domain must not bundle principles that demand *opposite* generative
stances to apply — a "resist the standard" instruction sitting beside "match the standard" rules is
incoherent, since the agent cannot hold both stances at once. The sharpest case is that coding
judgment and visual-aesthetic judgment never share a domain. At the ratify gate, a proposal that
wants a home in a domain whose principles pull the opposite way is a signal the domain or the
proposal is wrong — surface it (a fork candidate), do not force the fit.

---

## The ratify gate

Every cross-boundary change is **propose → ratify → promote**, never write-directly.

- A role proposes a principle as part of its output. It cannot write a corpus.
- The operator (or a ratifying role acting under standing rules) reviews and ratifies or rejects.
- **Rejections are kept** with their reason. The kill log is the highest-signal training data.
- Structural changes (split a domain, fork a role, add an explorer, change a route) go through the
  same gate.
- A proposal of `kind: direction` takes a **third route**: filed into the project's
  `ui-library.md` (provenance to the audit layer as usual) — never ratified into a domain, never
  killed, never a seed-promotion candidate. A direction is an identity decision, not a weighable
  rule; it carries no condition/reason obligation, and the library is the project's identity
  record. Processing a sound direction as a failed principle is a container-kill in new clothes.

### The genuine-fork test

Before ratifying a `judgment` proposal, ask: is there a plausible alternative choice — one a
competent role would actually reach for in the moment — that this principle rules out? If no
realistic version of "the wrong way" exists, the proposal isn't recording judgment; it's
decorating an outcome that was never at risk. Reject these by default, even when the rule is true
and harmless — a principle earns its permanent slot by guarding against a real wrong turn, not by
being correct. The common failure shape is generic good practice restated as project-specific
guidance: watch for a `reason` that names no specific failure mechanism and no plausible competing
choice, only a restatement of the rule itself. This is a different rejection than a `knowledge`
kill (which fires because the answer is derivable from training/docs regardless of whether a fork
exists) — the fork test asks whether a fork exists at all, prior to asking where the answer came
from.

### Domain assignment at the gate

A proposal arrives without a home. At the gate the orchestrator decides which domain it belongs to
and writes it there. If no existing domain fits, a **new domain is born here** — the orchestrator
creates `domains/<new-domain>.md` (+ audit) and adds it to the declarations of the roles that
should load it. This is the one point where domain assignment involves judgment, and it is
human-gated. A proposal that spans two domains is a signal the domain boundaries may be wrong —
surface it rather than fragmenting the principle across both.

### Write-back format

Ratified principle — append the working fields to the end of the target domain's `principles:`:

```yaml
- id: principle-id
  rule: "The guidance."
  condition: "When this applies."
  reason: "Why — the justification."
```

The proposal that surfaced the principle carries its `provenance` (captured at proposal time, not
ratification). On write-back, that `provenance` is filed by `id` in the layer's audit file, with
its `domain:` noted. The working file's principle carries no `provenance` field.

When a ratified principle is meaningfully reshaped — generalized, consolidated, split, or **moved
to another domain** — add an optional `history:` sub-list to its provenance entry. Each item
carries `date`, `type` (generalized / consolidated / split / moved), and `reason`:

```yaml
- id: some-principle
  provenance: "2026-01-01, original task."
  history:
    - date: 2026-06-20
      type: moved
      reason: "Re-homed from ui-designer corpus to the recoverability domain — it is shared with UX."
```

Promoted principle — when a corpus entry graduates to a lens prompt itself (becomes a baked-in
default rather than a weighable principle), move it from `principles:` to `promoted:` in the audit
file. Keep the entry so the audit trail is legible — a promoted principle that reappears as a
corpus proposal is a signal of regression, not new insight.

```yaml
- id: principle-id
  promoted_to: "<lens> prompt — <section name>"
  provenance: "Date, task, context. Note if it was subsumed by a meta-rule."
```

The trigger for promotion: a principle has been ratified long enough that checking its `condition`
and `reason` before every task is friction without benefit. Or: several principles share a common
root justification; the meta-rule that unifies them gets promoted, and the individual entries
become examples of it.

**Promotion restraint.** Before promoting, ask: would the role still need to reconsider this when
the project context changes? Promote only if the judgment is stable *across the kinds of projects
the role serves* — or is so foundational that contestability has genuinely become noise — not
merely because it has repeated inside one project family. When in doubt, leave it in `principles:`
where its `condition` and `reason` can still be checked against an unfamiliar case.

### Killed entries

Append to the `killed:` log in the domain's **working file**. Kills carry a stable `id` (so they
are referenceable via `see-also`, queryable at the gate, and traceable if the judgment recurs) and
a `kill_type`:

```yaml
- id: rejected-rule-id
  rule: "The rejected rule."
  kill_type: # quality | container | attribution-noise
  reason_killed: "Operator's reason."
```

- **quality** — the principle was wrong, too narrow, misframed, or already covered. The kill log
  working correctly; highest signal, because it pushes against a model default.
- **container** — the principle was sound but "belonged to another role." Under domain-scoping this
  is no longer a valid reason to kill: such a proposal is *filed in the right domain*, not killed.
  The value is reserved for tagging legacy kills that need re-homing.
- **attribution-noise** — killed by context degradation (e.g. a long multi-domain session), not on
  merit. A *false* kill. The retrospective should surface `container` and `attribution-noise` kills
  for re-examination rather than treating them as settled.

Per-kill audit detail goes in the layer's audit file, keyed by `id`, alongside its `provenance`:

```yaml
- id: rejected-rule-id
  domain: the-domain
  provenance: "Where this principle came from, before it was killed."
  killed: 2026-07-18     # the date this kill was recorded — required; enables graduation, below
  graduated: 2026-10-20  # OPTIONAL — set only once graduate-kill has demoted this entry
```

**Graduation.** A kill's job is to stop the same rejected idea from being re-proposed. That value
decays: a kill nobody has come near re-proposing across several retrospectives is no longer live
guidance, and its continued presence in the working file is a small, permanent reader-tax paid by
every future role session for a risk that has stopped materializing. `scripts/corpus.py kill-report
--domains-dir <dir> --audit <audit-file>` lists, per domain, every killed entry with no recorded
`killed:` date (a bookkeeping gap to fix) and every one old enough (default 90 days, `--min-age-days`
to override) to be a graduation candidate. The operator/retrospective judges whether it is actually
safe — has anything resembling it resurfaced — then `corpus.py graduate-kill --domains-dir <dir>
--audit <audit-file> --domain <domain> --id <id>` does the mechanical part: removes the entry from
the working file's `killed:` log and stamps `graduated:` on its audit-file record. Works on any
domains-dir + audit.md pair — a project's `corpora/domains/`, the kernel-seed `domains/`, or a pack's
`packs/<pack>/domains/` — since retrospective consolidation happens in the skill repo's own seed and
pack corpora too, not only in downstream projects.

---

## The handoff artifact

A role's terminal output is a **handoff artifact**: one file per role session, written by the role
as its final act, at `corpora/handoffs/<date>-<role>-<slug>.md`. The orchestrator relays this file
— never raw transcript — and the ratify gate reads proposals from its fields instead of parsing
prose. The schema structures the *envelope* (what the gate and relay mechanically consume), not the
*thinking*: the artifact body stays freeform in the lens's own form.

```yaml
---
role: ux-designer            # which lens produced this
workstream: checkout-redesign # stable across checkpoints and revisions
agent-continuity: new        # new | continued | replacement
status: complete             # complete | tradeoffs-pending | questions-pending | blocked
domains-loaded: [ux-design, recoverability]
proposals:                   # principle proposals, provenance attached at proposal time
  - id: proposed-slug
    rule: "..."
    condition: "..."
    reason: "..."
    kind: judgment           # judgment | knowledge | direction
    provenance: "date, task, context"
utility-candidates: []       # plausible deterministic shortcuts observed during work
violations-noted: []         # existing principles this work knowingly deviated from, with why
ui-drift: no                 # yes | no — did this work change the rendered visual system
                             #   (new component, changed treatment, retired pattern)
token-usage: "..."           # per spawn-token-summary
delegated-workers: []        # worker scopes, if this role delegated execution
---

## Artifact

[The spec / audit / tradeoff block — freeform, in the lens's own form.]

## Surfaced

[Anything that fits no field above: a gap noticed, a domain tension, a tooling problem.
Relayed to the operator verbatim. Expected empty most sessions — resolve what you can from
available material first, and never manufacture content to fill it. The section header is
always present; an empty section is a statement, a missing one is a schema violation.]
```

Field notes:

- **`workstream`** stays stable across implementation, operator testing, and revisions. A new plan
  or unrelated intended outcome receives a new identifier. **`agent-continuity`** makes a context
  discontinuity visible: `new` starts the workstream, `continued` resumes its owning agent, and
  `replacement` reconstructs from the complete role load and structured artifacts because the
  prior agent could not continue.
- **`kind`** is captured when the role knows it from the inside, not reconstructed at the gate.
  `judgment` = a decision made under uncertainty where context and tradeoffs shaped the outcome;
  `knowledge` = derivable from documentation or training; `direction` = a project design-direction
  choice — an identity decision, not a weighable rule. The stance model predicts `direction`: a
  divergent lens's output is a choice, so most UI-designer proposals are direction, not principle.
- **`utility-candidates`** is deliberately liberal. Each entry names an observed inference burden
  and concrete deterministic operation shape; it need not prove recurrence or specify a finished
  CLI. The orchestrator transfers it to the persistent project ledger before deleting the handoff.
- **`status: questions-pending`** — the role hit a genuine direction question mid-work: it stops,
  puts the questions in `Surfaced` (each with what has been established so far and what turns on
  the answer), and the orchestrator relays them and resumes the same workstream agent with the
  operator's answers when available, so working context survives the exchange. If continuation is
  unavailable, use the structured replacement protocol in
  `SKILL.md`; never rebuild from raw transcript. Same bar as
  gap-closing dialogue: only questions whose answers would produce materially different outputs.
- **`ui-drift`** is the mechanical staleness signal for the project's UI library, self-reported
  while the role's context is fresh. It is *counted at the ratify gate* (see the `library-drift`
  counter below), so experimental work that is discarded never reaches a gate and never triggers
  a library sync.
- **`Surfaced`** is the schema's escape valve: the envelope can under-fit but cannot suppress.
  Recurring traffic of the same *kind* in `Surfaced` is a retrospective signal that the schema
  needs a field — schema evolution from accumulated tension, through the gate, never speculative.
- **`delegated-workers`** lists each worker scope. When direct worker-to-orchestrator relay is not
  available, append a `## Delegated handoffs` section containing every worker's questions,
  tradeoffs, proposals, violations, and routing requests verbatim; the parent may not filter or
  ratify them.

Lifecycle: handoff files are working state, not corpus. Once the gate has ratified, killed, or
filed each proposal and written back, the file is deleted; the audit layer holds the durable
record. An unratified handoff file *is* the deferred-proposal queue — a directory of lingering
handoffs is a visible backlog. Inline sessions producing zero proposals, zero tradeoffs, and no
drift may skip the file; the session-harvest pipeline is the backstop for what that exemption
misses.

---

## Deferred UI/UX decisions

`corpora/deferred-decisions.md` is a project working queue for unresolved design questions that do
not block current implementation. It is not a substitute for a handoff or a place to hide blockers.
Every queued item names a narrow reversible provisional treatment so the coder can proceed without
turning that treatment into settled direction.

````markdown
# Deferred decisions

Only non-blocking UI/UX questions belong here. Blocking questions are surfaced immediately.

```yaml
decisions:
  - id: results-empty-state
    role: ux-designer
    domain: validation-feedback
    question: "Should an empty filtered result preserve filters or offer a reset action?"
    context: "Results panel introduced by the search workstream."
    source-workstream: search
    created: 2026-07-14
    blocking: no
    provisional-treatment: "Preserve filters; add no reset action yet."
    related-files: [src/components/results.tsx]
    status: queued
```
````

The schema is deliberately flat so `scripts/corpus.py lint-deferred` can validate it without a YAML
dependency. `role` is `ui-designer` or `ux-designer`; `status` is `queued` or `resolved`; `blocking`
must always be `no`. Group items by owning role and related surface, not count alone. Route a role
workstream when several items need coherent judgment, an item becomes blocking, provisional work
would create material rework, or the operator requests it. Pass the relevant entries to the role.
Mark them `resolved` only after the operator ratifies the role's handoff, then remove them; durable
direction and judgment live in the UI/UX libraries and corpora, not this queue.

---

## Project utilities

Active utilities live tersely in the `utilities` section of `corpora/config.md` because every role
may need them. They are project-owned deterministic tools that replace recurring, precision-sensitive,
or disproportionately token-expensive inference. Environment-owned tools are discovered from the
current runtime instead.

Candidates live separately in `corpora/utility-candidates.md` so cheap denials and recurrence
evidence survive handoff deletion without taxing every role load:

````markdown
# Utility candidates

```yaml
candidates:
  - id: color-math
    operation-shape: "Deterministic perceptual color transformation and compositing."
    status: denied
    evidence:
      - date: 2026-07-14
        workstream: settings-redesign
        burden: "Several rounds of manual color derivation."
    disposition:
      reason: "Not enough expected reuse yet."
```
````

Surface a plausible candidate whenever denial is cheap. Before recording it, check the standard
library, installed dependencies, current runtime tools, and active project utilities. The operator
accepts, denies, or defers it. Record evidence with `corpus.py record-utility-candidate`; the script
derives sighting count and first/last dates and resurfaces recurrence or a prior denial. Record the
operator's disposition with `corpus.py set-utility-status`. Only an accepted utility that is
implemented and tested enters config. Denied candidates remain historical memory; retrospectives
may consolidate duplicates or obsolete entries. Candidate status is `open`, `deferred`, `denied`,
`accepted`, or `implemented`.

---

## Project corpora

In any project using this system, project-specific accumulated judgment lives under
`<project-root>/corpora/domains/`, one working file per domain (`<domain>.md`) plus a single
`corpora/domains/audit.md` for the project layer, same schema as the seed domains. The kernel is the mechanism (schema, ratify gate, retrospective,
lifecycle) and is indifferent to how many domains exist.

Seed domain = general judgment that travels across projects (lives in the skill: kernel-level
`domains/` and pack-level `packs/<pack>/domains/`).
Project domain = judgment earned in this specific project.
Both apply when a role runs: for each domain the role declares, load the seed domain (if any) then
the project domain (if any) of the same name — unless the project domain file's preamble declares
`fork-status: forked`, in which case load only the project file; the seed is no longer consulted
for that domain. A project may also have domains with no seed counterpart (project-specific
subjects, e.g. `spatial-metaphor`).

### Forking a domain

A project can adopt a seed or pack domain instead of always merging live with it — useful once a
domain has diverged enough, or has principles that don't fit the project, that the live merge is
more noise than signal. Run `corpus.py adopt --domain <domain>` (skill-repo script, project root as
`--root`): it locates the domain's seed or pack file and prints its principles — mechanics only, no
judgment. From there: propose which principles are project-relevant vs. droppable with a reason
each, get operator approval, then write the curated result to `corpora/domains/<domain>.md` —
merged by `id` with any principles already there — with `fork-status: forked`, `forked-from: <seed
path>`, and `forked-date: <date>` in its preamble. Forking is one-way: it stops the live merge for
that domain going forward. Re-syncing a fork against later seed changes is not yet supported.

Two layers supply the seed: a stack-agnostic kernel layer (orchestrator + base coder + their
domains) always present, and an optional role pack selected by `corpora/config.md` (`role-pack:`)
that overlays stack-specific lenses and domains. A pack adds depth — more domains on existing
roles — never new roles. A project with no UI runs on the kernel layer alone, designer lenses
inactive.

---

## The retrospective

Run at two cadences. Same faculty, different direction.

**Forward (per-task):** Route the task to the right lens(es) and assemble the right domains. Guard
against contamination — is the working context holding domains from another mode?

**Backward (periodic):** Surface signals as proposals for the operator:

1. **Contamination detected** — attention was spent on a domain outside the task's mode. Fix the
   routing or the declaration.
2. **Domain tension → split / fork** — two ratified principles in one domain have conditions that
   partition the same space and give *opposing* advice. Proposal: split the domain (and, if the
   split tracks a role seam, fork the role). Advisory only — the operator judges whether the
   partition is real. *What counts:* one cluster of principles clearly governs one decision class
   and another governs a different one, and they repeatedly give opposing advice under their
   conditions. *What doesn't:* two principles on different topics are simply different subjects, not
   a partition. The seam is discovered here, from tension — never assumed up front.
3. **Convergence → explorer** — a domain has stopped changing, corrections rare. Proposal: pair the
   roles that use it with an explorer to prevent calcification.
4. **Declaration drift** — a role declares a domain it never draws from, or repeatedly reaches for a
   domain it doesn't declare. Proposal: fix the declaration.
5. **Seed promotion candidate** — a project domain principle whose condition makes no reference to
   this project's stack, domain, or specifics, and has held across enough tasks to read as general.
   Surface it as a candidate for promotion to the seed domain of the same name in the skill repo.
6. **Structural kinship → condensation candidate** — active principles that state the same
   underlying test in different words, evidenced by existing `see-also` links or found by reading a
   domain's principles side by side rather than sequentially. Proposal: state the shared test once
   as an umbrella, with the specific cases named as instances — the shape `coder.md`'s General
   Conventions already uses for its own meta-conventions. Complementary to co-firing, below: kinship
   is visible from the text alone and doesn't need firing history to accumulate first, so it can
   surface a candidate before co-firing ever would.
7. **Kill graduation** — a killed entry old enough with no sign of recurrence is paying reader-tax
   for a risk that has stopped materializing. Mechanically surfaced by `corpus.py kill-report`
   (see "Killed entries," above); the retrospective judges whether it is actually safe to demote,
   then `corpus.py graduate-kill` does the removal and audit annotation.

**Anti-overfitting (any domain whose principles were earned in a single project shape):** surface
which ratified principles should stay provisional — weighable, not promoted — until tested against
another shape. A principle pressure-tested in only one climate is a promotion risk, not a default.
Sharpened by efficacy counts: a provisional principle with real `fired` counts under a *second*
project shape has earned its promotion case; one that has only ever fired in its birth project
stays provisional.

**Triggers (mechanical, checked by the orchestrator at every ratify gate; always a suggestion,
never automatic):** suggest `retrospective <domain>` when, since the last one, `ratified ≥ 6`, or
`working-file-tokens` grew by ≥ 50%, or `gate-violations ≥ 3`. Suggest a **UI-library sync** when
`library-drift.since-last-sync ≥ 3`, or immediately when a drifting change *retired* something the
library still teaches — a stale-but-wrong library is worse than an incomplete one. Thresholds are
operator-tunable and deliberately coarse: the trigger replaces "am I watching carefully enough,"
not the retrospective's judgment. These are *triggers, not caps* — accumulation is the point; the
bet is that meta-principles condense out of accumulated specific ones, and a fired trigger means
"there is enough new material that condensation is worth attempting."

**Efficacy readings (inputs to the signals above):** `idle` dominant across many gates →
retirement candidate, or the condition is scoped to situations the project never produces.
`violated` recurring → the principle is load-bearing (it keeps catching real drift) *or* badly
conditioned — the counts cannot distinguish these; the retrospective can, which is why counts feed
the retrospective instead of acting alone. A cluster that always `fired` together → meta-principle
candidate: co-firing is the empirical trace of a shared root justification — see structural kinship,
above, for the same candidate found from the text alone rather than firing counts.

Each domain working file carries `last-retrospective: <date>` at the top to make convergence measurable.

---

## Role lifecycle

```
spawn (lens + declared seed domains)
  → accumulate (work + retrospective surface principles; operator ratifies into domains)
  → [retrospective may propose SPLIT if a domain develops tension, FORK if the split tracks a role seam]
  → converge / lock (domains stabilize, corrections rare)
  → [retrospective proposes pairing with an EXPLORER]
```

Growth is differentiation under accumulated tension — never promotion up a ladder, never an org
chart imposed in advance.
