# The Corpora Kernel

The kernel is the shared mechanism every spawn inherits. It is not code — it is a discipline made
of files plus a loop.

A **spawn** is a *stance* plus a *composition*: a generative posture (the mode of reasoning the
agent applies) and the **domain corpora**, decided fresh by routing judgment each time, the
orchestrator applies to the task at hand. Spawns do not own corpora. Judgment lives in domains; a
composition is the momentary combination through which one or more domains are applied to a task.
See "Spawns: stance + composition," below.

A **domain corpus** is a list of principles about one subject matter, context type, or decision
class — not a job title. Multiple compositions may draw on the same domain, so shared judgment
lives once. Domain boundaries are *discovered from accumulated tension* (the fork signal in the
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
- **reason** travels with the rule always. This is what lets the spawn think rather than pattern-match:
  "the reason was X; this task is Y, so the rule doesn't bind here."
- **provenance** is cheap to record and invaluable for trusting or retiring a principle later.
- A principle does not name its domain in a field — the domain is the *file* it lives in. Moving a
  principle to a better-fitting domain is a file move, recorded in the audit `history`.

### Storage: working vs audit

Working and audit metadata are split so a spawn's working context carries only the fields it weighs
during a task. **File granularity matches load granularity:** working files are per-domain because
the working load is *selective* (only composed domains); audit metadata is one file per layer
because the audit load is *broad* (the orchestrator pulls the whole layer at once).

- **Working file** (`domains/<domain>.md`) — one per domain. The active `principles:` with their
  `id / rule / condition / reason / see-also`, the `conventions:` list (below), plus the `killed:`
  log. This is the only part loaded when a spawn works, inline or spawned.
- **Audit file** (`domains/audit.md`, one per layer — kernel-seed and each project) —
  per-principle `provenance` keyed by `id` (each entry noting its `domain`) and per-kill audit
  metadata. Loaded only at ratify and retrospective time, by the orchestrator —
  never in a spawn's working context. The audit file also carries the layer's **counters** — the
  mechanical signals that replace operator feel. **Never write or edit these by hand, including
  when creating a fresh audit file**: `scripts/corpus.py` alone creates them (`measure`) and
  updates them (`record-gate`), inside a marker-delimited block it owns. Shown here for
  reference only:

  ```yaml
  counters:
    - domain: coding-general
      origin: seed                 # seed | project — stronger than directory-inference
                                    #   alone; defaults from --domains-dir shape, overridable
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

  co-occurrence:                   # per unordered domain pair, incremented at each gate that
                                    #   loaded both — mechanical byproduct of record-gate's inputs
    - domains: [color, motion]
      count: 3

  library-drift:                   # project layer only, when has-ui: yes
    since-last-sync: 2             # gates where a handoff's ui-drift.screens or .components
                                    #   was non-empty
  ```

  Efficacy counts must never enter a working file — a spawn that sees them will start writing
  principles that fire often instead of principles that are right. They are audit-layer signals,
  consumed only by the retrospective.

  The script (in the skill repo: `record-gate`, `measure`, `triggers`, `lint-handoff`,
  `lint-deferred`, `deferred`, `lint-deterministic-shortcut-candidates`, `deterministic-shortcut-candidates`,
  `record-deterministic-shortcut-candidate`, `set-deterministic-shortcut-status`, `retro-done`, `sync-done`) does all counting,
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

The `killed:` log lives in the working file because it is active guidance — it tells the spawn what
has already been tried and rejected, prevents the same pattern from re-emerging, and opens new
directions by making the rejection reason visible. Provenance and promotions are audit metadata a
spawn does not weigh mid-task, so they stay in the audit file.

This is a *storage* split, not a *corpus* excerpt: every active principle and kill entry is still
passed in full with the fields a spawn reasons over. Working and audit are kept consistent by `id`:
every active `id` in a working file has a `provenance` entry in its layer's audit file, and vice versa.

---

## Spawns: stance + composition

A **spawn** is a stance (see "Generative stance," below) plus a **composition** — the domain subset
applied to the task at hand. The orchestrator's actual routing act is *composing directly*: reading
the task, deciding stance, and stating the domain subset it needs in the spawn brief (below), every
time — never through a cached, named intermediate layer. A spawn is never a persistent named file
carrying its own persona prompt and a fixed domain list; two fixed, universal stance frames exist —
convergent and divergent (below) — and everything else about "what this spawn is" comes from the
composed domains themselves, stated fresh in the brief.

A composition's domain subset is subject-separated — a spawn never mixes domains from different
subject families (coding and design never co-compose; see "The hard line," below). Stance is a
property of the spawn, not of a domain: a domain carries `posture: guardrail` (every domain in the
corpus today does — see "The hard line") and is available to any composition whose subject matches,
regardless of which stance the spawn runs under. `design-method`, for instance, is a convergent body
of correctness guardrails that loads into both convergent and divergent design spawns; a convergent
domain loading into a divergent spawn is the design working as intended, not a violation. Domains are
not "declared by" a composition the way principles used to be "declared by" a role.

**Recognizing that a task needs a *different* domain subset, not just one more domain, is itself
routing judgment.** A founding-a-library task (standing up a UI or UX library from nothing) needs a
narrower composition than ongoing design work on an established one. The same task-shape question
applies orthogonally to coding work: a task whose actual subject is dependency/version management,
not feature work, needs judgment (`dependency-management`, seeded 2026-07-22) that has no business
loading on every routine coding task just because it's also convergent, stack-agnostic prose. The
fix is composing `dependency-management` instead of `coding-general` for that task shape, not
folding task-specific judgment into `coding-general`'s always-loaded default — a domain composed
unconditionally into every coding spawn should earn that by actually applying to every task of that
shape, not by being convergent and general-sounding. Stack-shape (framework/styling/language)
already conditions which domains a coding composition includes (`coding-nextjs` only when
`framework: nextjs`, etc.); task-shape is the same kind of conditioning, checked against what the
task is actually about instead of what the project is built with.

**The composition is deterministic, not a self-selected runtime relevance call by the working
agent.** The orchestrator fixes which domains apply before the spawn runs; the choice is inspectable
after the fact via the handoff's `domains-loaded:` field (see "The handoff artifact"). The
orchestrator's composition choice is visible before the spawn runs the same way any other
orchestrator action is; see the spawn brief, below.

**The orchestrator does not compose domains for itself — every other spawn is what gets composed.**
The distinction is not fixedness; it is what kind of thing produces what. A composed spawn produces
a generative artifact *about a subject*: a spec, a plan, code. The orchestrator produces routing and
gating *decisions about spawns*, one level up: which stance and domains a task needs, whether a
proposal ratifies, when a retrospective fires. Something has to occupy that position before any
composition can happen — otherwise nothing decides what to compose for the orchestrator itself, and
the regress has no floor. `SKILL.md` states this precisely: the orchestrator is "a pure process
layer that composes and routes spawns but never takes on a spawn's stance itself."
`orchestrator-routing`, `ratify-gate`, and `principle-judgment` are its own domains, loaded into
`SKILL.md`'s own prompt rather than composed fresh per task — not because the orchestrator is
"fixed" in some special sense, but because a process layer has no subject to compose *for*; it has
only the process itself.

Multiple domains compose into one spawn whenever a task's coupling warrants it — a
gesture-transition task might load `motion` + `wizards-flows` + `ranking-evaluation` together in one
divergent spawn. There is no separately-named grouping to be "forced across"; the orchestrator
states whatever subset the task needs directly, every time (see LINEAGE.md, "Lenses retired").

### Two load modes

- **Working load** (generation): a spawn's composed domains, *working files only*. Lean and
  inspectable. This is every new isolated spawn and every inline spawn segment.
- **Audit load** (synthesis, human-gated): the orchestrator loads relevant domains *broadly,
  including audit and kill metadata*, at ratify and retrospective time. Breadth is safe here
  because it is not constrained generation and it is gated by the operator.

Composition enforces load boundaries: a coding-stance spawn loads coding domains and never design
domains. Whether two spawn segments may share a context is routing judgment, informed by stance,
prior exploration, evaluator independence, context length, and cost. A handoff captures proposals
and violations at a transition, but is a checkpoint rather than automatic agent termination. See
`SKILL.md`, "Inline, resume, or isolate," and LINEAGE.md, "Role isolation."

### Generative stance

Every spawn has a `stance:` — how it generates. There are two, and they are opposite:

- **convergent** — the value of the output comes from *matching a standard*: correctness, idiom,
  fit. Coding, UX-flow, planning, and orchestration work are convergent. For a convergent spawn,
  regression toward the training mean is frequently the *right* answer; there is no anti-mean anchor.
- **divergent** — the value comes from *differentiating from the standard*: a distinctive identity.
  Visual/UI-identity work is divergent. A divergent spawn carries an **anti-mean anchor**: before
  committing to a direction it must name at least one safe/expected default that should *not*
  apply, because a generative model otherwise drifts to the average of its training data — the
  forgettable answer. (History: LINEAGE.md.)

Stance is a property of the **spawn** (the generating agent, for this task), not of a domain.
Principles, by their nature — a weighable rule with a condition and a reason — overwhelmingly
encode *convergent* correctness; that is what crystallizes into a rule. The divergent element is a
generative *stance*, not a body of principles. So domains are mostly convergent guardrails,
consumed by spawns of either stance, and the anti-mean anchor lives on the divergent stance and
fires at the generative moment.

**The hard line:** a single domain must not bundle principles that demand *opposite* generative
stances to apply — a "resist the standard" instruction sitting beside "match the standard" rules is
incoherent, since the agent cannot hold both stances at once. In practice this means a domain
declares `posture: guardrail` (a convergent body of correctness rules, consumable by either stance)
or, hypothetically, `posture: generative` (a body that itself demands the anti-mean anchor). No
domain in this corpus is `posture: generative` today — the anti-mean anchor lives on the divergent
stance frame itself, not on any domain — so a proposal arriving with `posture: generative` is a
ratify-gate rejection on sight; it belongs on the stance frame, not a domain. This is a narrower
claim than stance-matching at the composition level: the hard line is about what a single domain is
allowed to bundle, not about which domains a given spawn may load together (that is subject
separation, above). The sharpest composition-level case is that coding judgment and
visual-aesthetic judgment never share a domain — coding-subject and design-subject domains never
co-compose. At the ratify gate, a proposal that wants a home in a domain whose principles pull the
opposite way is a signal the domain or the proposal is wrong — surface it (a fork candidate), do not
force the fit.

---

## The spawn brief

Before spawning, the orchestrator states its composition choice in a short, fixed-field brief —
the schema structures the envelope, not the thinking. No decision-procedure is baked into the
schema for *how* the orchestrator picks these values; that judgment stays as flexible as ever and
accumulates the normal way, through `domains/orchestrator-routing.md`'s own principles.

```yaml
stance: divergent
unit-of-work: design-ui-surface
domains: [color, visual-hierarchy, motion]
expected-output: "Design spec for the settings-panel color treatment."
```

This is visibility, not a pre-spawn approval gate — the orchestrator's routing choice (which
domains, why) is already visible before a spawn runs, the same way any other orchestrator action
is. The real gate stays exactly where it already is: the ratify gate, for anything proposing new
corpus content, never for the working composition itself. A genuinely novel subject with no
existing domain simply runs guardrail-light; the new-domain need surfaces through the spawn's own
proposal at the ratify gate as already designed, with no separate ephemeral-domain
pre-declaration step required.

`unit-of-work` and `domains` are no longer independent assertions the orchestrator makes side by
side: the orchestrator states `stance` and `unit-of-work` from the task at hand — that part stays
judgment, same as ever — and `domains` is what `scripts/corpus.py select --unit-of-work
<unit-of-work>` returns for the project's current `corpora/config.md`, not a second freestanding
guess. The brief keeps all three fields because all three are worth seeing before the spawn runs,
but the third is now derived and inspectable (re-run `select` and compare) rather than merely
asserted.

---

## The ratify gate

Every cross-boundary change is **propose → ratify → promote**, never write-directly.

- A spawn proposes a principle as part of its output. It cannot write a corpus.
- The operator (or a ratifying spawn acting under standing rules) reviews and ratifies or rejects.
- **Operator-direct authorship is sanctioned**, not a bypass of this rule: the operator already
  knows a rule they hold — no spawn had to produce it as a proposal first. `corpus.py record-gate
  --ratified 1` runs standalone (no handoff required) with a hand-written provenance entry using
  the convention `"Operator-authored, <date>, based on observed <behavior>, root-caused and
  refined."` What "never write-directly" actually forbids is a *spawn* writing a corpus directly,
  skipping the gate's review — it was never a prohibition on the operator's own hand, which the
  gate exists to serve, not to route around.
- **Rejections are kept** with their reason. The kill log is the highest-signal training data.
- Structural changes (split a domain, add an explorer, change a route) go through the
  same gate.
- A proposal of `kind: direction` takes a **third route**: filed into the project's
  `ui-library.md` — never ratified into a domain, never killed, never a seed-promotion candidate.
  A direction is an identity decision, not a weighable rule; it carries no condition/reason
  obligation, and the library is the project's identity record. Processing a sound direction as a
  failed principle is a container-kill in new clothes. **No parallel audit file exists for
  `ui-library.md`/`ux-library.md`, and none should be created.** The working/audit split above is
  real infrastructure built specifically for domain corpora (a per-domain working file plus one
  audit file per layer, both maintained by `corpus.py`) — it does not extend to the library docs by
  default, and "as usual" language here would wrongly imply it does. `ui-library.md` describes only
  current application state; git history is its complete audit trail, the same way it is for any
  other versioned source file — do not write "(direction, <date>, implemented)" tags,
  "supersedes..." lead-ins, or trailing "*Provenance*" paragraphs into the library itself. A spawn
  updating the library replaces superseded content outright rather than layering a correction on
  top of it.

### The genuine-fork test

Before ratifying a `judgment` proposal, ask: is there a plausible alternative choice — one a
competent spawn would actually reach for in the moment — that this principle rules out? If no
realistic version of "the wrong way" exists, the proposal isn't recording judgment; it's
decorating an outcome that was never at risk. Reject these by default, even when the rule is true
and harmless — a principle earns its permanent slot by guarding against a real wrong turn, not by
being correct. The common failure shape is generic good practice restated as project-specific
guidance: watch for a `reason` that names no specific failure mechanism and no plausible competing
choice, only a restatement of the rule itself. This is a different rejection than a `knowledge`
kill (which fires because the answer is derivable from training/docs regardless of whether a fork
exists) — the fork test asks whether a fork exists at all, prior to asking where the answer came
from.

The same test extends to domain **creation**, not only principle ratification: before a new
domain is born at the gate (see "Domain assignment," below), ask whether the proposal is actually
a different subject from every existing domain, not merely a proposal that would read a little
cleaner with its own file. Freer domain creation under the composed-subset model cuts both ways —
it removes the old incentive to force-fit content into an ill-fitting existing container, but
without this check it trades that failure for the opposite one: fragmentation into too many
narrow, single-principle domains. A new domain clears the bar only when an existing domain's
principles would have to bundle opposing generative stances, or a genuinely separate decision
class, to hold it — the same structural-kinship/fork evidence used for domain splits, applied at
creation time instead of split time.

### Domain assignment at the gate

A proposal arrives without a home. At the gate the orchestrator decides which domain it belongs to
and writes it there. If no existing domain fits, a **new domain is born here** — the orchestrator
creates `domains/<new-domain>.md` (+ audit); the domain becomes available to any spawn whose
stance and subject match — there is no composition declaration to add it to. This is the one point where
domain assignment involves judgment, and it is human-gated. A proposal that spans two domains is a
signal the domain boundaries may be wrong — surface it rather than fragmenting the principle
across both.

A proposal must cite specifically how it matches an existing domain's stated subject — not just
"plausibly fits." This is a cheap, one-line justification the proposer states at write-back time,
not a new tier or gate: it exists to stop content being filed into a domain because the container
looked plausible and was already open, rather than because it is actually the right home. (History:
LINEAGE.md, the v3 transition entry.)

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

Retired principle — graduated to a convention: when a principle has been ratified long enough that
checking its `condition` before every task is friction without benefit, move it from `principles:`
to the working file's `conventions:` list, dropping `condition` and keeping its `id`, `rule`, and
`reason`:

```yaml
- id: convention-id
  rule: "The guidance."
  reason: "Why — the justification, unchanged from the principle it graduated from."
  # no condition — unconditioned by definition, applies whenever this domain loads
```

This is not a separate authority tier: a convention doesn't read as more authoritative than a
principle, it is simply unconditioned — checked whenever the domain loads, with no per-case
condition-weighing left to do. Unlike the old fold-to-preamble mechanic, a convention keeps its
`id`: it stays addressable, killable (a convention can still move to `killed:` if it turns out
wrong), and graduatable in the other direction (see "Promotion restraint," below) — dissolving a
principle into unstructured preamble prose loses all three. Add a `history:` entry (`type:
graduated-to-convention`) to the principle's audit-layer `provenance` record so the trail stays
legible — a principle that reappears as a corpus proposal after graduating is a signal of
regression, not new insight.

A principle that has outgrown its narrow domain — belongs somewhere more general, or warrants a
new domain of its own — is handled by the same mechanism as any other domain reassignment: the
structural-kinship/condensation signal (see "The retrospective," below) and the gate's ordinary
domain-reassignment judgment. No parallel "laws vs. rules" split exists here — an entry exempt
from condition-checking is *more* dangerous, not more trustworthy, and a separate authority tier
would carry an ossification risk not worth taking on.

**Promotion restraint** applies to graduation into `conventions:`: before graduating, ask whether
the spawn would still need to reconsider this when the project context changes. Graduate only if
the judgment is stable *across the kinds of projects the domain serves* — or is so foundational
that contestability has genuinely become noise — not merely because it has repeated inside one
project family. When in doubt, leave it in `principles:` where its `condition` and `reason` can
still be checked against an unfamiliar case.

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
every future spawn session for a risk that has stopped materializing. `scripts/corpus.py kill-report
--domains-dir <dir> --audit <audit-file>` lists, per domain, every killed entry with no recorded
`killed:` date (a bookkeeping gap to fix) and every one old enough (default 90 days, `--min-age-days`
to override) to be a graduation candidate. The operator/retrospective judges whether it is actually
safe — has anything resembling it resurfaced — then `corpus.py graduate-kill --domains-dir <dir>
--audit <audit-file> --domain <domain> --id <id>` does the mechanical part: removes the entry from
the working file's `killed:` log and stamps `graduated:` on its audit-file record. Works on any
domains-dir + audit.md pair — a project's `corpora/domains/` or the kernel-seed `domains/` — since
retrospective consolidation happens in the skill repo's own seed corpus too, not only in downstream
projects.

---

## The handoff artifact

A spawn's terminal output is a **handoff artifact**: one file per spawn session, written by the
spawn as its final act, at `corpora/handoffs/<date>-<composition>-<slug>.md`. The orchestrator
relays this file — never raw transcript — and the ratify gate reads proposals from its fields
instead of parsing prose. The schema structures the *envelope* (what the gate and relay
mechanically consume), not the *thinking*: the artifact body stays freeform in the spawn's own
form.

**One unit-of-work is one spawn is one handoff — a corpora-owned rule, unconditional, never
inferred.** A queue of several units of work is several spawns, each producing its own handoff, even
when nothing goes wrong and no domain-tension gap ever surfaces. This is stated as a hard rule and
not left to a process layer's own gap-detection because gap-triggered routing has already been
observed to silently drop it: when corpora ceded per-task routing to a gap-triggered process layer,
a five-task queue with nothing going wrong never re-fired a spawn, and all five tasks executed
inline in one continuous context with only the outermost planner's handoff surviving — see
LINEAGE.md, "Orchestrator-removal reverted," for the evidence. A queue-task boundary, or a chunk boundary (see
"Chunk chaining," below), is *itself* a mandatory new-spawn trigger — not a fact that must first be
inferred from a surfaced gap. Lighter-weight bookkeeping between chunks (below) is for ground-truth
ledger data, never a substitute for this per-unit-of-work isolation.

**Before writing it, re-read the output against the composed domains.** Re-read the deliverable
against the ratified principles in every domain the composition included and revise any violation
found — this is part of what producing a valid handoff requires, not a domain judgment call, so it
lives here rather than in a domain's `principles:` list. Passing tools (lint, typecheck, tests) is
not evidence this happened: tooling only catches what produces a hard error and is structurally
blind to soft principles (comment discipline, naming, structural conventions) that have no
mechanical enforcement — green tooling means "no hard errors," not "checked." Catching a violation
here is cheaper than the external ratify gate finding it after the fact.

An instruction is a thing that sometimes doesn't happen — the reason this is stated as a rule here
rather than trusted as a norm. `scripts/stop-check.sh` (a `Stop` hook) checks the one part of this
mechanically verifiable from outside the spawn: that every chunk recorded in `corpora/chunks/*.md`
(see "Chunk chaining," below) still matches what `corpus.py select` would compose today, blocking
termination on a mismatch. It cannot see whether the re-read itself happened — `Stop`-hook input
does not carry the originating spawn prompt, and it is unverified whether `SubagentStart`'s does
either — so it is a narrower, honest check (composition drift), not a substitute for the instruction
above.

The same "an instruction sometimes doesn't happen" gap applies to a spawn noticing its own task has
drifted from its original scope mid-work, not just at the terminal act — `scripts/scope-checkpoint.sh`
(a `PostToolUse` hook) fires an external reminder every `INTERVAL` tool calls (default 20, per
session, cheap: no interpreter startup on the common silent path) rather than relying on the spawn
to spontaneously remember to check. It carries no judgment of its own — `spawn-integrity`'s
`periodic-scope-and-integrity-checkpoint` is what the spawn does when it fires.

**The spawn's own final conversational turn is not a second copy of the artifact.** Once the
handoff file is written, the spawn's actual return to the orchestrator (its last message) states
only that the file exists and where — a path and a one-line status, never a restatement of the
`Artifact`/`Surfaced` content or the proposals. The orchestrator retrieves the handoff by reading
the file directly, the same way it already reads domain files, never from the spawn's own return
text. Paying full generation cost for the same content twice — once into the file, once again into
the conversational turn that hands control back — is the same waste
`artifact-points-to-persisted-file-not-full-reproduction` already rules out one level up (a
deliverable that already has a persisted home does not get reproduced in full); this is that same
principle applied to the handoff file itself, not only to what the handoff points at.

```yaml
---
stance: <convergent|divergent>  # which stance this spawn ran under
workstream: <stable-workstream-id> # stable across checkpoints and revisions — not this spawn's
                              #   composition or task name; substitute a real identifier, never
                              #   leave this example value in place
agent-continuity: new        # new | continued | replacement
status: complete             # complete | tradeoffs-pending | questions-pending | blocked
domains-loaded: [<domain-a>, <domain-b>, ...] # every domain this spawn's composition actually loaded
proposals:                   # principle proposals, provenance attached at proposal time
  - id: proposed-slug
    rule: "..."
    condition: "..."
    reason: "..."
    kind: judgment           # judgment | knowledge | direction
    provenance: "date, task, context"
deterministic-shortcut-candidates: []       # plausible deterministic shortcuts observed during work
violations-noted: []         # existing principles this work knowingly deviated from, with why
ui-drift:                    # both invalidation signals — a spawn names only what it touched
  screens: []                 #   screen ids directly worked on, if any
  components: []               #   shared component names changed, if any (matches
                                #   ui-library.md's own component vocabulary headings)
token-usage: "..."           # per spawn-token-summary
delegated-workers: []        # worker scopes, if this spawn delegated execution
---

## Artifact

[The spec / audit / tradeoff block — freeform, in the spawn's own form.]

## Surfaced

[Anything that fits no field above: a gap noticed, a domain tension, a tooling problem.
Relayed to the operator verbatim. Expected empty most sessions — resolve what you can from
available material first, and never manufacture content to fill it. The section header is
always present; an empty section is a statement, a missing one is a schema violation.]
```

Field notes:

- **`stance`** reports what actually ran, not a claim about what a composition generally does —
  immune to declaration drift by construction. Together with `domains-loaded:` (already on this
  schema), it replaces the old `role:` field: the two report exactly what was applied for *this*
  spawn, more precisely than a role name did.
- **`workstream`** stays stable across implementation, operator testing, and revisions. A new plan
  or unrelated intended outcome receives a new identifier. **`agent-continuity`** makes a context
  discontinuity visible: `new` starts the workstream, `continued` resumes its owning agent, and
  `replacement` reconstructs from the complete composition load and structured artifacts because the
  prior agent could not continue.
- **`kind`** is captured when the spawn knows it from the inside, not reconstructed at the gate.
  `judgment` = a decision made under uncertainty where context and tradeoffs shaped the outcome;
  `knowledge` = derivable from documentation or training; `direction` = a project design-direction
  choice — an identity decision, not a weighable rule. The stance model predicts `direction`: a
  divergent spawn's output is a choice, so most UI-identity proposals are direction, not principle.
- **`deterministic-shortcut-candidates`** is deliberately liberal. Each entry names an observed inference burden
  and concrete deterministic operation shape; it need not prove recurrence or specify a finished
  CLI. The orchestrator transfers it to the persistent project ledger before closing the handoff
  (`corpus.py handoff-done`).
- **`status: questions-pending`** — the spawn hit a genuine direction question mid-work: it stops,
  puts the questions in `Surfaced` (each with what has been established so far and what turns on
  the answer), and the orchestrator relays them and resumes the same workstream agent with the
  operator's answers when available, so working context survives the exchange. If continuation is
  unavailable, use the structured replacement protocol in
  `SKILL.md`; never rebuild from raw transcript. Same bar as
  gap-closing dialogue: only questions whose answers would produce materially different outputs.
- **`ui-drift`** is the mechanical staleness signal for the project's UI library and its
  screenshot cache (`corpora/screenshots/manifest.md`), self-reported while the spawn's context is
  fresh. `screens:` names what was worked on directly; `components:` names shared components that
  changed. Empty on both means no drift. A spawn never has to enumerate which *other* screens a
  changed shared component appears on — at the ratify gate, `screenshot-mark-stale` expands
  `components:` into every screen the manifest's own tags already show it on, mechanically. It is
  also *counted at the ratify gate* (see the `library-drift` counter below), so experimental work
  that is discarded never reaches a gate and never triggers a library sync.
- **`Surfaced`** is the schema's escape valve: the envelope can under-fit but cannot suppress.
  Recurring traffic of the same *kind* in `Surfaced` is a retrospective signal that the schema
  needs a field — schema evolution from accumulated tension, through the gate, never speculative.
- **`delegated-workers`** lists each worker scope. When direct worker-to-orchestrator relay is not
  available, append a `## Delegated handoffs` section containing every worker's questions,
  tradeoffs, proposals, violations, and routing requests verbatim; the parent may not filter or
  ratify them.

Lifecycle: handoff files are working state, not corpus. Once the gate has ratified, killed, or
filed each proposal and written back, close it with `corpus.py handoff-done <file>`: the audit
layer already holds the durable record, so by default (`corpora/config.md` has no `debug: yes`)
the script deletes the file. When `debug: yes`, it archives the file to
`corpora/handoffs/archive/` instead — never deleted there, kept purely so a project that wants to
audit past spawn output can. An unratified handoff file *is* the deferred-proposal queue — a
directory of lingering handoffs is a visible backlog; the archive directory is not part of that
backlog and is never read for it, since it holds only already-ratified handoffs. Inline sessions
producing zero proposals, zero tradeoffs, and no drift may skip the file; the session-harvest
pipeline is the backstop for what that exemption misses.

---

## Chunk chaining

A **chunk** is one unit-of-work's worth of a workstream: the composition it drew (see `scripts/
corpus.py select`), the stance it ran under, and the handoff it produced. `corpora/chunks/
<workstream>.md` is an append-only ledger, one entry per chunk, keyed by `workstream` (stable across
checkpoints and revisions the same way the handoff's `workstream` field already is):

```yaml
workstream: <stable-workstream-id>
chunks:
  - unit-of-work: design-ux-flow
    domains-composed: [wizards-flows, recoverability, design-method, interviewing]
    stance: convergent
    handoff: corpora/handoffs/2026-07-29-uxdesign-settings-flow.md
    completed: 2026-07-29
    next: design-ui-surface        # or omitted
```

**This ledger records what already happened; it does not replace it.** "One unit-of-work is one
spawn is one handoff" (above) still holds for every chunk — `chunk-done` requires a real handoff
file to exist for the unit-of-work it closes, the same way `record-gate` requires a real gate to
have run. `domains-composed` is written by `corpus.py`, from the same `select` call that composed
the spawn, not self-reported by the spawn — `domains-loaded:` in a handoff has always been
self-report, and self-report done by attention is exactly what LINEAGE.md's "Orchestrator-removal
reverted" entry shows silently stops happening under no-news-is-good-news conditions. Making it a
script byproduct instead gives the co-occurrence and composition-drift signals (`corpus.py
record-gate --co-occurs-with`) ground truth to reconcile against, without asking the ledger to carry
any of the weight of deciding whether to spawn.

`corpus.py chunk-start --workstream W --unit-of-work U` runs the same `select` call the spawn brief
already made and prints the composition — a preview, writing nothing; the ledger is append-only and
only ever written once a real handoff exists to point at, so there is no in-progress entry to
record before the spawn starts. `chunk-done --workstream W --unit-of-work U --stance S --handoff
<path> [--next U]` is the operative half — it re-runs `select` itself (so `domains-composed` is
never self-reported) and appends the entry, failing if the handoff file does not exist or does not
name the same `workstream`. That existence check makes ordering load-bearing: `chunk-done` must run
*before* `handoff-done` closes (deletes or archives) the handoff file it points at, never after —
see `processes/general-operation.md`, Phase 6's chunk-close step. `close-workstream W` is a
read-only summary once every chunk in a workstream is done — it aggregates the ledger for the
retrospective, it does not fold multiple chunks' handoffs into one.

`chunk-done` also reconciles against the handoff's own `domains-loaded:` field, when present, and
refuses to close the chunk if the two disagree. Recomputing `select()` proves it's self-consistent,
not that it matches what actually happened — a composing process that hard-lists a domain set in
prose instead of calling `select()` (the exact shape of drift `processes/bootstrap.md`'s Phase 2/3 composition
had before it was fixed) can silently diverge from `select()`'s answer, and `verify-chunks` alone
cannot see that: it only recomputes the same function it's checking against itself. The
`domains-loaded:` cross-check is the actual fidelity check; a handoff written before this schema
field existed (or by a process that doesn't yet self-report it) skips the check rather than failing
retroactively.

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
    stance: convergent
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
dependency. `stance` is `convergent` or `divergent`; `status` is `queued` or `resolved`; `blocking`
must always be `no`. Group items by stance and related surface, not count alone. Route a spawn
workstream when several items need coherent judgment, an item becomes blocking, provisional work
would create material rework, or the operator requests it. Pass the relevant entries to the spawn.
Mark them `resolved` only after the operator ratifies the spawn's handoff, then remove them; durable
direction and judgment live in the UI/UX libraries and corpora, not this queue.

---

## Project utilities

Active utilities live tersely in the `utilities` section of `corpora/config.md` because every spawn
may need them. They are project-owned deterministic tools that replace recurring, precision-sensitive,
or disproportionately token-expensive inference. Environment-owned tools are discovered from the
current runtime instead.

Candidates live separately in `corpora/deterministic-shortcut-candidates.md` so cheap denials and recurrence
evidence survive handoff deletion without taxing every spawn's load:

````markdown
# Deterministic shortcut candidates

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
accepts, denies, or defers it. Record evidence with `corpus.py record-deterministic-shortcut-candidate`; the script
derives sighting count and first/last dates and resurfaces recurrence or a prior denial. Record the
operator's disposition with `corpus.py set-deterministic-shortcut-status`. Only an accepted utility that is
implemented and tested enters config. Denied candidates remain historical memory; retrospectives
may consolidate duplicates or obsolete entries. Candidate status is `open`, `deferred`, `denied`,
`accepted`, or `implemented`.

---

## Project corpora

In any project using this system, project-specific accumulated judgment lives under
`<project-root>/corpora/domains/`, one working file per domain (`<domain>.md`) plus a single
`corpora/domains/audit.md` for the project layer, same schema as any other layer. The kernel is the
mechanism (schema, ratify gate, retrospective, lifecycle) and is indifferent to how many domains
exist or which repository holds them.

A project's own `corpora/domains/` is the whole domain set that project's spawns compose from —
`select`, `compose-spawn-prompt`, and `manifest` all read only it (or an explicit `--domains-dir`
override). There is no live, automatic merge with this skill's own `domains/` or with any other
project's corpora: every corpora-managed location is symmetric — a `domains/` + `audit.md` pair,
readable and importable the same way regardless of which repository holds it. This skill's own
`domains/` is not structurally privileged; it is the **default import source**, the pool bootstrap
offers to pull from on day one (see "Import," below), and nothing more.

A freshly-bootstrapped project therefore starts with an empty `corpora/domains/` and imports what
it needs — either the default-pool bulk import bootstrap offers, or picking individual principles
and conventions from any domains-dir later (`corpus.py import-list` / `import-candidate`). A
project bootstrapped under the older, live-merge model migrates once via
`processes/domain-repo-migration.md` before its first session under this model — that process
materializes its previously-live seed content into its own `corpora/domains/` so nothing it already
relied on silently disappears.

A project that wants to track this skill's own domain content as it evolves, rather than
snapshotting it once at import time, re-runs the default-pool import periodically (or per updated
principle) — the same mechanism, not a separate sync feature. This replaces the older per-domain
fork mechanism (`corpus.py adopt`), retired 2026-07-22 for never having been exercised by a real
project and for solving a problem — merge-time conflict — that live concatenation never actually
created; see `LINEAGE.md`.

### Import

An import never writes a domain working file directly — it is a new *producer* of candidates,
structurally the same relationship `reading/discovery-agent.md`/`reading/session-harvest-agent.md`
already have to a candidates file and the ratify gate. The difference is what's being proposed: not
a freshly-mined judgment call, but an *already-ratified* principle or convention from another
corpus, re-proposed here with provenance recording where it actually came from. It goes through the
same gate as any other candidate — the operator (or the gate-running orchestrator) still browses,
picks a destination domain per entry (not necessarily the source's own domain name — the same
domain-assignment judgment as "Domain assignment at the gate," above, applied to an imported entry
instead of a freshly-proposed one), and ratifies or rejects it individually.

- `corpus.py import-list --source <domains-dir>` — read-only. Lists every principle and convention
  under `<domains-dir>`, flagging which ids already exist anywhere in the target project's own
  `corpora/domains/`. Proposes nothing; for browsing before picking.
- `corpus.py import-candidate --source <domains-dir> --domain <d> --id <id> [--as-domain <d2>]
  [--as-id <id2>]` — proposes one entry as a candidate, appended to
  `corpora/import-candidates.md` (created on first use), with an `imported-from` provenance block:

  ```yaml
  - id: [kebab-case-slug]                 # may be renamed at import time if it collides
    rule: [...]
    condition: [...]                      # omitted for a convention import
    reason: [...]
    domains: [proposed destination domain — operator's choice, not necessarily the source's]
    kind: judgment
    provenance:
      imported-from:
        source: [path to the source domains-dir]
        domain: [source domain name]
        id: [source id, if renamed on import]
        originally-ratified: [source's own provenance date, if available]
      extracted: [YYYY-MM-DD]
  ```

  `kind: judgment` by default — the entry already cleared the fork test once, in its source corpus;
  the fork test (`domains/principle-judgment.md`) is still available if the operator wants to
  re-examine it rather than rubber-stamp it.
- `corpus.py import-default-pool [--source <domains-dir>]` — the bootstrap fast path: proposes
  every principle and convention from every domain in the source (this skill's own `domains/` by
  default) whose `applies-when` already matches the project's `corpora/config.md` shape, or is
  `universal`, skipping anything the project already has by id. One batch, still individually
  ratifiable — not a bypass of the gate, just the operator's answer defaulted to "yes to all"
  instead of asked one at a time.

Write-back from `corpora/import-candidates.md` follows the ordinary write-back format, above — the
`imported-from` block is additional provenance, not a different write path.

### Monorepo root resolution

A monorepo may have more than one `corpora/config.md` — an app-scoped one (`admin/corpora/`) and a
root-level one, or several sibling apps each with their own. `scripts/corpus.py` resolves which
root governs a given file by nearest-ancestor walk from the file up toward the filesystem root,
stopping at the first `corpora/config.md` found — the same model `tsconfig.json`/`package.json`
resolution already use. This resolves automatically; there is no manual `sibling-corpora:`
declaration to keep in sync, deliberately, so the check can't go stale the way a hand-maintained
list would.

**`--for-file <path>` is the standard way to invoke `corpus.py`** for any real task, in place of
computing and passing `--root` by hand: pass any file the task touches (a target file, or the
first one named in the task description) and every command resolves the right root itself before
doing anything else — no session, orchestrator, or project needs to work out which root governs a
task as a separate step. `--root` still exists for the cases `--for-file` can't cover: bootstrapping
a brand-new nested root (nothing to resolve to yet, since its `corpora/config.md` doesn't exist
until that bootstrap writes it), or operating on a `--domains-dir`/`--audit` override that isn't
tied to any one file (`kill-report`, `graduate-kill`, working the kernel-seed layer directly).

`corpus.py resolve-root --file <path>` and `corpus.py check-root-boundary --files <f1,f2,...>`
remain available directly for the narrower cases `--for-file` doesn't cover on its own: inspecting
which root a file would resolve to without running a command against it, and — the one still-manual
step — checking whether a task's *several* touched files all resolve to the *same* root before
composing a single spawn. `--for-file` only resolves one path; a task spanning multiple files still
needs `check-root-boundary` to catch the case those files disagree about which root governs them,
since a spawn's composition can only ever be one root's domains (`select`/`compose-spawn-prompt`
take one `--root`). This is the same shape as subject separation (`check-composition` — a spawn
never mixes coding and design domains), just on a different axis: a task spanning two corpora roots
is two units of work, one per root, sequenced by whichever the planner judges dependent — not a
single spawn straddling both.

### One flat seed layer

The skill's `domains/` is one flat pool — no separate "role pack" layer selected by a project-config
field. A stack-agnostic domain (`coding-general`, `orchestrator-routing`, `spawn-integrity`, ...)
and a stack-specific one (`coding-react`, `css`, `color`, ...) live side by side; each states its own
load condition as `applies-when` frontmatter against `corpora/config.md`'s existing project-shape
fields (`language`, `framework`, `styling`, `has-ui`) — `coding-nextjs` loads when `framework:
nextjs`, `css` loads when `styling` is not `none`, and so on; `scripts/corpus.py select` evaluates
these mechanically rather than a reader checking prose (see "Spawns: stance + composition," and
`scripts/corpus.py`'s `select`/`manifest` commands). Retired 2026-07-22: an earlier `role-pack:`
field bundled a stack's domains behind one coarse flag, gating them all-or-nothing; since every
domain already carried its own precise condition, the field added an indirection without adding
information, and it couldn't express a project needing some but not all of a stack's domains. A
project with no UI simply never composes divergent visual-identity domains into a spawn — nothing
gates that on a config field at all, since nothing routes work into them.

That original reasoning was specific to who was consuming the condition: true while the only
consumer was a reader checking prose before a spawn, since a coarse `role-pack:` flag genuinely
added nothing over precise per-domain prose read the same way either form. It stopped being the
whole story once a process layer needs to select domains without reading prose at all (2026-07-29,
"Promote load conditions to frontmatter") — at that point the condition has to exist in a
machine-evaluable form regardless, and `applies-when` frontmatter is that form. This isn't a
reversal of the `role-pack:` retirement — a coarse all-or-nothing flag would still be strictly worse
information than per-domain `applies-when` predicates — it's the same conclusion holding for a new
reason once the requirement changed. See `LINEAGE.md` for both entries.

---

## The retrospective

Run at two cadences. Same faculty, different direction.

**Forward (per-task):** Route the task to the right stance and compose the right domains. Guard
against contamination — is the working context holding domains from another mode?

**Backward (periodic):** surfaces signals as proposals for the operator — contamination, domain
tension, convergence, composition drift, seed-promotion candidates, structural kinship, kill
graduation, anti-overfitting, and efficacy interpretation. See `processes/retrospective.md` for the trigger
and procedure, and `domains/retrospective.md` for the judgment behind each signal — what counts,
what doesn't, and why. Two adjacent signals (a misplaced principle, and a ratified principle whose
gate-time discipline may have lapsed) are judged by `principle-judgment` instead, since they're
about one principle's own fitness rather than a pattern read across a domain's history.

Each domain working file carries `last-retrospective: <date>` at the top to make convergence measurable.

---

## Domain lifecycle

```
spawn (stance + composition)
  → accumulate (work + retrospective surface principles; operator ratifies into domains)
  → [retrospective may propose SPLIT if a domain develops tension, FORK if the split tracks a
     project-local seam]
  → converge / lock (domains stabilize, corrections rare)
  → [retrospective proposes pairing with an EXPLORER]
```

Growth is differentiation under accumulated tension — never promotion up a ladder, never an org
chart imposed in advance.
