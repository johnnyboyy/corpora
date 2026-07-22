# Corpora v3 — stance-composed lenses (Phases 0–3) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this
> plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collapse the kernel's "lens file + fixed declaration" role model into
stance-frame (convergent/divergent) + orchestrator-composed domain subset, per
`v3-redesign-proposal.md`'s locked decisions (2026-07-21). Scope: this repo only —
kernel.md, corpus.py, SKILL.md, bootstrap.md, README.md, and the web-frontend pack. The
FAMOUS/Blog/Meridian upgrade path (proposal phase 4) is explicitly out of scope here.

**Architecture:** `coder.md`, `ux-designer.md`, `ui-designer.md` stop existing as files with
their own prompts. `orchestrator.md`-equivalent (SKILL.md/bootstrap.md routing logic) and
`planner.md` stay fixed. Their persona/"law" prose migrates into domain preambles and
principles; their fixed domain declarations dissolve into an informal alias list
(`domains/role-aliases.md`) the orchestrator uses as routing shorthand only. `kernel.md`
gains: composed-declaration language, an affirmative fit-justification requirement at the
ratify gate, a domain-creation fork test, a `stance:`/`composition:` handoff schema (drops
`role:`), reworded retrospective signals #1/#4, `promoted:` retirement (folds into domain
preambles), and a new "spawn brief" schema section.

**Tech Stack:** Markdown corpus files (hand-authored prose + YAML-in-fences), `scripts/corpus.py`
(stdlib-only Python), `tests/test_corpus.py` (pytest, 33 existing tests must keep passing).

## Global Constraints

- Every edit must keep `python3 -m pytest tests/test_corpus.py -q` green (33 passed baseline).
- Do not touch `packs/web-frontend/domains/*` subject-matter content except where explicitly
  named below (coding-ts, coding-react, coding-nextjs, css, color, etc. keep their existing
  principles — only the *audit* promoted-section handling and preambles change).
- Do not touch FAMOUS, Blog, or Meridian — this plan is scoped to the `corpora` repo (the skill
  itself).
- `cmd_adopt` and its five existing tests are untouched (locked decision: keep `adopt` as-is).
- Every commit message states which proposal decision it implements, referencing
  `v3-redesign-proposal.md` section headers, so `git log` stays a legible trail of which locked
  decision produced which diff.
- Work happens in the current worktree (`worktree-v3-stance-composed-lenses`), not on `master`.

---

### Task 1: kernel.md — Roles section: stance + composed subset (replaces lens + declaration)

**Files:**
- Modify: `kernel.md` — "Roles: lens + declaration" section (currently lines ~117–176)

**Interfaces:**
- Produces: the canonical description later tasks (5, 6, 11, 12, 13) cross-reference — a spawn
  is `stance + orchestrator-composed domain subset`; declarations are inspectable via the
  handoff's `domains-loaded:` field, not a fixed file.

- [ ] **Step 1: Rewrite the section**

Replace the "## Roles: lens + declaration" heading and its body (from `A role file is a **lens**...`
through the end of "Generative stance" but keep "Generative stance" content mostly intact — it's
already the frame text per the proposal's "Decided 2026-07-21" note) with:

```markdown
## Spawns: stance + composed domain subset

A **spawn** is a stance (see "Generative stance," below) plus a domain subset the orchestrator
composes fresh for the task at hand — never a persistent named file carrying its own persona
prompt and a fixed domain list. Two fixed, universal frames exist: convergent and divergent
(below). Everything else about "what this spawn is" is assembled per task.

The orchestrator decides which domains a task needs and unions them into one working
declaration, same-stance domains only — the hard line below (no stance-mixing inside one spawn)
is the one invariant carried over unchanged from the earlier lens-file model. A domain is
available to any spawn whose stance and subject match; domains are not "declared by" a role.

**The declaration is still deterministic, not a self-selected runtime relevance call by the
working agent** — that invariant survives in spirit — but it changes shape: no longer inspectable
in advance by reading a fixed lens file, it is inspectable *after* spawn via the handoff's
`domains-loaded:` field (see "The handoff artifact"). The orchestrator's composition choice is
visible before the spawn runs the same way any other orchestrator action is; see the spawn brief,
below.

**Recurring domain-subsets get an informal alias.** `coder`, `ux-design`, and `ui-design` are the
first three seeded entries in `domains/role-aliases.md` — a label for a domain-subset +
stance combination the orchestrator reuses often enough to be worth naming as routing shorthand.
An alias is not a schema entity and not a file with its own prompt; it carries no persona text.
New aliases accumulate the same way domains do — from repeated, observed composition, never
declared up front.

**The orchestrator and the planner are excluded from this collapse.** They are the fixed,
named entities doing the composing, not domain-consuming working roles — `SKILL.md`'s routing
logic and `planner.md` keep their own prompts and stay as they are.

Multiple domain-subsets can compose into one spawn when a task's coupling warrants it (a
gesture-transition task might load `motion` + `wizards-flows` + `ranking-evaluation` together in
one divergent spawn, rather than being forced across two separately-named roles).

### Two load modes

- **Working load** (generation): a spawn's composed domains, *working files only*. Lean and
  inspectable. This is every new isolated spawn and every inline role segment.
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
incoherent, since the agent cannot hold both stances at once. The sharpest case is that coding
judgment and visual-aesthetic judgment never share a domain. At the ratify gate, a proposal that
wants a home in a domain whose principles pull the opposite way is a signal the domain or the
proposal is wrong — surface it (a fork candidate), do not force the fit.
```

- [ ] **Step 2: Verify no dangling references to "lens" as a per-role file concept remain in this section**

Run: `grep -n "lens file\|role file\|declared domains\|## domains" kernel.md`

Expected: only hits inside sections not yet rewritten by this task (later tasks fix those) — note
which lines still say "lens file" so Tasks 12/13 can find them; do not fix outside kernel.md here.

- [ ] **Step 3: Run the test suite (no code touched, sanity check nothing else broke)**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed`

- [ ] **Step 4: Commit**

```bash
git add kernel.md
git commit -m "kernel: collapse lens+declaration into stance+composed domain subset

Implements v3-redesign-proposal.md phase 1, 'Kernel model changes' and the
alias-list / orchestrator-and-planner-excluded decisions locked 2026-07-21."
```

---

### Task 2: kernel.md — ratify gate: affirmative fit-justification + domain-creation fork test

**Files:**
- Modify: `kernel.md` — "Domain assignment at the gate" subsection, and "The genuine-fork test"
  subsection

**Interfaces:**
- Consumes: nothing new from Task 1.
- Produces: gate language later referenced by Task 11 (when migrating lens prose into domains) —
  every migrated principle must pass this fit test.

- [ ] **Step 1: Add affirmative fit-justification to "Domain assignment at the gate"**

Insert as a new paragraph immediately after the existing first paragraph of that subsection
(which ends "...surface it rather than fragmenting the principle across both."):

```markdown
A proposal must cite specifically how it matches an existing domain's stated subject — not just
"plausibly fits." This is a cheap, one-line justification the proposer states at write-back time,
not a new tier or gate: it exists to stop content being filed into a domain because the container
looked plausible and was already open, rather than because it is actually the right home — the
exact failure mode a persistent named lens file used to invite (see LINEAGE.md, the v3 transition
entry).
```

- [ ] **Step 2: Extend the genuine-fork test to domain creation**

At the end of "### The genuine-fork test" subsection, append:

```markdown
The same test extends to domain **creation**, not only principle ratification: before a new
domain is born at the gate (see "Domain assignment," above), ask whether the proposal is actually
a different subject from every existing domain, not merely a proposal that would read a little
cleaner with its own file. Freer domain creation under the composed-subset model cuts both ways —
it removes the old incentive to force-fit content into an ill-fitting existing container, but
without this check it trades that failure for the opposite one: fragmentation into too many
narrow, single-principle domains. A new domain clears the bar only when an existing domain's
principles would have to bundle opposing generative stances, or a genuinely separate decision
class, to hold it — the same structural-kinship/fork evidence used for domain splits, applied at
creation time instead of split time.
```

- [ ] **Step 3: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed`

- [ ] **Step 4: Commit**

```bash
git add kernel.md
git commit -m "kernel: add affirmative fit-justification and domain-creation fork test

Implements v3-redesign-proposal.md phase 1 bullet on domain-assignment ceremony,
and the 'freer domain creation cuts both ways' gap surfaced on review."
```

---

### Task 3: kernel.md — handoff schema: `stance:`/`composition:` replace `role:`

**Files:**
- Modify: `kernel.md` — "The handoff artifact" section (YAML schema block and field notes)

**Interfaces:**
- Consumes: Task 1's "Generative stance" terminology (`stance: convergent | divergent`).
- Produces: schema fields `stance:` and `composition:` that Task 13 (bootstrap.md) and Task 11
  (retired lens files) must not contradict.

- [ ] **Step 1: Edit the YAML schema block**

In the fenced schema block under "## The handoff artifact", change:

```yaml
role: ux-designer            # which lens produced this
workstream: checkout-redesign # stable across checkpoints and revisions
```

to:

```yaml
stance: convergent           # convergent | divergent — which stance this spawn ran under
composition: ux-design       # OPTIONAL — the alias name, if the spawn used one, for fast
                              #   scanning only; never authoritative. Omit for ad hoc composition.
workstream: checkout-redesign # stable across checkpoints and revisions
```

- [ ] **Step 2: Update field notes**

In the "Field notes" bullet list immediately below the schema, add a new bullet right before the
`workstream` bullet:

```markdown
- **`stance`** reports what actually ran, not a claim about what a role generally does — immune to
  declaration drift by construction. **`composition`** is a fast-scan label only; the gate never
  treats it as authoritative, and a spawn with no matching alias simply omits it. Together they
  replace the old `role:` field: `domains-loaded:` (already on this schema) plus `stance:` report
  exactly what was applied for *this* spawn, more precisely than a role name did.
```

- [ ] **Step 3: Check for other `role:` handoff-schema references in kernel.md**

Run: `grep -n "role: ux-designer\|role: ui-designer\|which lens produced" kernel.md`
Expected: no matches (Task 7 handles the separate `deferred-decisions.md` schema's `role:` enum).

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed`

- [ ] **Step 5: Commit**

```bash
git add kernel.md
git commit -m "kernel: handoff schema — stance/composition replace role field

Implements the locked 2026-07-21 decision: drop the handoff role: enum (and its
pre-approval implication), report stance + optional composition label instead."
```

---

### Task 4: kernel.md — reword retrospective signals #1 and #4 for composition

**Files:**
- Modify: `kernel.md` — "The retrospective" section, "Backward (periodic)" numbered list

**Interfaces:**
- Consumes: Task 1's composition terminology.

- [ ] **Step 1: Reword signal #1**

Change:

```markdown
1. **Contamination detected** — attention was spent on a domain outside the task's mode. Fix the
   routing or the declaration.
```

to:

```markdown
1. **Contamination detected** — attention was spent on a domain outside the task's mode. Fix the
   routing or the composition.
```

- [ ] **Step 2: Reword signal #4**

Change:

```markdown
4. **Declaration drift** — a role declares a domain it never draws from, or repeatedly reaches for a
   domain it doesn't declare. Proposal: fix the declaration.
```

to:

```markdown
4. **Composition drift** — a spawn's composed domain-subset consistently excludes a domain the work
   actually needed, or includes one it never draws from. Proposal: fix the composition (or, if this
   recurs on the same task shape, propose the pattern as a new or revised alias). Maps directly onto
   the co-occurrence tally `corpus.py record-gate` maintains (see "Storage: working vs audit") and
   the handoff's `Surfaced` field.
```

- [ ] **Step 3: Grep the rest of kernel.md for any other reference relying on "declaration drift already covers this"**

Run: `grep -n "declaration drift\|Declaration drift" kernel.md`
Expected: only the signal-#4 heading itself (now "Composition drift"); if any other prose still
says "declaration drift" as a safety-net justification, update it to "composition drift" too —
this dependency was flagged explicitly in the proposal ("Retrospective signals that reference
'the declaration'").

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed`

- [ ] **Step 5: Commit**

```bash
git add kernel.md
git commit -m "kernel: reword retrospective signals 1 and 4 for a role-less-declaration world

Implements v3-redesign-proposal.md's flagged dependency: the applies-to: tagging
and other mitigations leaned on 'declaration drift already catches this' — that
safety net doesn't hold until these signals are reworded for composition."
```

---

### Task 5: kernel.md — retire `promoted:` as an audit-file section

**Files:**
- Modify: `kernel.md` — "Storage: working vs audit" (audit file description + example YAML),
  "The ratify gate" → "Write-back format" (the "Promoted principle" subsection)

**Interfaces:**
- Produces: the audit-file shape Task 8 (`corpus.py`) and Task 11 (migrating `coder.md`'s
  General Conventions into `coding-general.md`) must match — no `promoted:` block, promoted
  content instead lives as domain-preamble prose.

- [ ] **Step 1: Remove `promoted:` from the "Storage: working vs audit" description**

In the bullet describing the audit file (`domains/audit.md`, one per layer...), change:

```markdown
  per-principle `provenance` keyed by `id` (each entry noting its `domain`), the `promoted:` block,
  and per-kill audit metadata. Loaded only at ratify and retrospective time, by the orchestrator —
```

to:

```markdown
  per-principle `provenance` keyed by `id` (each entry noting its `domain`) and per-kill audit
  metadata. Loaded only at ratify and retrospective time, by the orchestrator —
```

- [ ] **Step 2: Rewrite the "Promoted principle" write-back subsection**

Replace the block starting `Promoted principle — when a corpus entry graduates to a lens prompt
itself...` through the end of "Promotion restraint" paragraph with:

```markdown
Retired principle — folded into scene-setting: when a principle has been ratified long enough that
checking its `condition` and `reason` before every task is friction without benefit, it does not
graduate to a separate authority tier. Move its substance into the domain's own **preamble** — the
scene-setting prose read before the working file's `principles:` list — and remove the entry from
`principles:`. A preamble doesn't read as more authoritative than a principle; it's just the frame
read first. Add a `history:` entry (`type: folded-to-preamble`) to the principle's audit-layer
`provenance` record so the trail stays legible — a principle that reappears as a corpus proposal
after being folded is a signal of regression, not new insight, exactly as the old `promoted:` log
was for.

The other job `promoted:` used to do — "this principle has outgrown its narrow domain, belongs
somewhere more general or deserves a new domain" — is not a distinct mechanism either: it is
exactly what the structural-kinship/condensation signal (see "The retrospective," below) and the
gate's ordinary domain-reassignment judgment already catch. No parallel "laws vs. rules" split is
introduced — an entry exempt from condition-checking is *more* dangerous, not more trustworthy,
and a separate authority tier would reintroduce the same ossification risk a persistent lens
file's baked prompt text had.

**Promotion restraint** still applies to the fold-to-preamble case: before folding, ask whether the
role would still need to reconsider this when the project context changes. Fold only if the
judgment is stable *across the kinds of projects the domain serves* — or is so foundational that
contestability has genuinely become noise — not merely because it has repeated inside one project
family. When in doubt, leave it in `principles:` where its `condition` and `reason` can still be
checked against an unfamiliar case.
```

- [ ] **Step 3: Update the audit-file YAML example**

In the fenced `counters:` / `efficacy:` / `library-drift:` example under "Storage: working vs
audit", it does not currently show a `promoted:` key — confirm this with a grep and leave it
unchanged if so:

Run: `grep -n "promoted:" kernel.md`
Expected after this task: zero matches remaining in `kernel.md` (Task 7 handles
`deferred-decisions.md`'s unrelated `role:` field, not `promoted:`).

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed` (kernel.md prose changes don't affect corpus.py behavior yet — Task 8 does).

- [ ] **Step 5: Commit**

```bash
git add kernel.md
git commit -m "kernel: retire promoted: as an audit-file section

Implements the locked 2026-07-21 decision: fold 'stable, friction-free' principles
into the domain's own preamble instead of a separate authority tier; the
outgrown-domain case is already covered by the structural-kinship signal."
```

---

### Task 6: kernel.md — add "The spawn brief" section

**Files:**
- Modify: `kernel.md` — insert a new section after "### Generative stance" and before "## The
  ratify gate"

**Interfaces:**
- Produces: `stance:`, `domains:`, `expected-output:` fields Task 12 (SKILL.md) references when
  describing what the orchestrator writes before spawning.

- [ ] **Step 1: Insert the new section**

```markdown
---

## The spawn brief

Before spawning, the orchestrator states its composition choice in a short, fixed-field brief —
the schema structures the envelope, not the thinking. No decision-procedure is baked into the
schema for *how* the orchestrator picks these values; that judgment stays as flexible as ever and
accumulates the normal way, through `domains/orchestrator-routing.md`'s own principles.

```yaml
stance: divergent
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
```

- [ ] **Step 2: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed`

- [ ] **Step 3: Commit**

```bash
git add kernel.md
git commit -m "kernel: add the spawn brief — thin stance/domains/expected-output envelope

Implements the locked 2026-07-21 decision: a spawn brief structured like the
handoff, no new pre-approval gate, judgment stays in orchestrator-routing.md."
```

---

### Task 7: kernel.md — fix `deferred-decisions.md`'s `role:` enum

**Files:**
- Modify: `kernel.md` — "## Deferred UI/UX decisions" section (schema block and prose)

**Interfaces:**
- Consumes: Task 1's stance terminology.

- [ ] **Step 1: Edit the schema block**

Change:

```yaml
  - id: results-empty-state
    role: ux-designer
    domain: validation-feedback
```

to:

```yaml
  - id: results-empty-state
    stance: convergent
    domain: validation-feedback
```

- [ ] **Step 2: Edit the prose line below the schema**

Change:

```markdown
The schema is deliberately flat so `scripts/corpus.py lint-deferred` can validate it without a YAML
dependency. `role` is `ui-designer` or `ux-designer`; `status` is `queued` or `resolved`; `blocking`
must always be `no`. Group items by owning role and related surface, not count alone.
```

to:

```markdown
The schema is deliberately flat so `scripts/corpus.py lint-deferred` can validate it without a YAML
dependency. `stance` is `convergent` or `divergent`; `status` is `queued` or `resolved`; `blocking`
must always be `no`. Group items by stance and related surface, not count alone.
```

- [ ] **Step 3: Run tests — expect a failure, this is intentional at this step**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: any test asserting `DEFERRED_ROLE_ENUM` behavior against `role: ui-designer` fixtures
may now be testing stale fixture data only — check the failure output before assuming corpus.py
itself needs a code change; this task only edits documentation. If a test fails because it
constructs a fixture using `role:`, that fixture is exercising `corpus.py`'s parser, which Task 9
below updates — note the failing test name and confirm Task 9 covers it, do not silently `xfail`.

- [ ] **Step 4: Commit**

```bash
git add kernel.md
git commit -m "kernel: deferred-decisions schema — stance replaces the role: ui-designer|ux-designer enum

Same role-less-declaration problem the handoff schema had, just buried in a
section that doesn't obviously look role-related at first glance."
```

---

### Task 8: `corpus.py` — retire `DEFERRED_ROLE_ENUM`, add `DEFERRED_STANCE_ENUM`

**Files:**
- Modify: `scripts/corpus.py` (constant + wherever it validates `role:` in a deferred-decision
  entry)
- Test: `tests/test_corpus.py`

**Interfaces:**
- Consumes: Task 7's schema change (`stance:` field replaces `role:` in deferred-decisions.md).
- Produces: `DEFERRED_STANCE_ENUM = {"convergent", "divergent"}` other tasks/tests reference.

- [ ] **Step 1: Find current usage**

Run: `grep -n "DEFERRED_ROLE_ENUM\|role.*ui-designer\|role.*ux-designer" scripts/corpus.py tests/test_corpus.py`

Read every matched line before editing — this constant is checked in `lint-deferred`'s validation
path; know the exact call site before changing it.

- [ ] **Step 2: Write/adjust the failing test first**

Find the existing test(s) that build a deferred-decisions fixture with `role: ux-designer` (or
similar) and assert `lint-deferred` accepts/rejects it. Update the fixture to use
`stance: convergent` / `stance: divergent`, and add one new test asserting an invalid stance value
(e.g. `stance: sideways`) is rejected the same way an invalid `role:` used to be. Name it
`test_lint_deferred_rejects_invalid_stance`.

- [ ] **Step 3: Run the new/updated test to confirm it fails**

Run: `python3 -m pytest tests/test_corpus.py -k deferred -v`
Expected: FAIL — either `KeyError`/`AssertionError` from the stale `role:` field name, or the new
invalid-stance test failing because nothing rejects it yet.

- [ ] **Step 4: Implement**

In `scripts/corpus.py`, rename the constant and update its one call site:

```python
DEFERRED_STANCE_ENUM = {"convergent", "divergent"}
```

(Replaces `DEFERRED_ROLE_ENUM = {"ui-designer", "ux-designer"}`.) Update the validation code that
reads `entry.get("role")` to read `entry.get("stance")` and check membership in
`DEFERRED_STANCE_ENUM` instead of `DEFERRED_ROLE_ENUM`, keeping the same error-message shape
(field name in the message changes from `role` to `stance`).

- [ ] **Step 5: Run tests to confirm they pass**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed` or more (the new test adds one, so `34 passed` if no other tests were
removed).

- [ ] **Step 6: Commit**

```bash
git add scripts/corpus.py tests/test_corpus.py
git commit -m "corpus.py: deferred-decisions validates stance, not the role enum

Matches kernel.md's deferred-decisions schema update (Task 7)."
```

---

### Task 9: `corpus.py` — retire `promoted:` section parsing, fold audit entries into preambles

**Files:**
- Modify: `scripts/corpus.py` (`parse_audit_entries`, `annotate_graduated`)
- Modify: `domains/audit.md` (kernel-seed layer) — remove `promoted:` block, fold each entry
- Modify: `domains/coding-general.md` — add/extend the preamble with folded content
- Modify: `packs/web-frontend/domains/audit.md` — remove `promoted:` block, fold each entry
- Modify: `packs/web-frontend/domains/coding-ts.md` or the relevant pack domain — add/extend
  preamble (check each entry's `domain:` field first; do not assume all pack promotions are
  coding-ts)
- Test: `tests/test_corpus.py`

**Interfaces:**
- Consumes: Task 5's kernel.md rule (fold to preamble, add `history: type: folded-to-preamble`).
- Produces: audit files with zero `promoted:` sections, matching what `parse_audit_entries` and
  `annotate_graduated` now expect (no special-cased section boundary).

- [ ] **Step 1: Read both current `promoted:` blocks in full**

Run: `sed -n '/^promoted:/,$p' domains/audit.md`
Run: `sed -n '/^promoted:/,$p' packs/web-frontend/domains/audit.md`

For each entry, note: `id`, `domain`, `promoted_to` (which lens/section it named), and
`provenance`. This is the exact content that must appear, reworded as scene-setting prose, in the
preamble of the domain named in each entry's `domain:` field.

- [ ] **Step 2: Update `parse_audit_entries` and `annotate_graduated` in `scripts/corpus.py`**

Both functions currently use `re.fullmatch(r"promoted:", stripped)` as a section-boundary marker
that ends `in_provenance`. Since `promoted:` will no longer exist in any audit file, the boundary
must instead be end-of-file (or, if a future top-level key is added, that key) — remove the
`promoted:` check entirely; `in_provenance` simply stays `True` from the `provenance:` line to
EOF. Concretely, in both functions delete the block:

```python
        if re.fullmatch(r"promoted:", stripped):
            in_provenance = False
            current = None
            continue
```

(In `annotate_graduated`, delete the corresponding two-line `if re.fullmatch(r"promoted:", stripped): in_provenance = False` — check the exact surrounding lines before deleting, the two functions are structured slightly differently per the earlier Read output.)

- [ ] **Step 3: Write a test proving `parse_audit_entries` no longer needs a `promoted:` boundary**

Add a test that writes a minimal audit fixture with a `provenance:` list and NO `promoted:` key,
containing entries both before and after where a stale implementation might have stopped parsing,
and asserts every entry is returned by `parse_audit_entries`. Name it
`test_parse_audit_entries_no_promoted_section`.

- [ ] **Step 4: Run the new test to confirm current behavior (should already pass — this is a
  regression-guard, not a bugfix)**

Run: `python3 -m pytest tests/test_corpus.py -k no_promoted -v`
Expected: PASS once Step 2's deletion is in place; if it fails before Step 2, that confirms the
old code depended on the `promoted:` marker in a way that would have broken parsing once the
marker is removed from real files — proceed to Step 2 if not already done, then re-run.

- [ ] **Step 5: Fold `domains/audit.md`'s `promoted:` entries into `domains/coding-general.md`'s preamble**

For each entry found in Step 1 whose `domain:` is `coding-general`, add one sentence to
`domains/coding-general.md`'s preamble (the prose above its `principles:` list) capturing the
substance the old `promoted_to` field pointed at — e.g. "No peer re-exports: import from the
authoritative module, not a peer that happens to re-export it (barrel index files that explicitly
aggregate a public surface are the only exception)" for `no-re-export-from-peer-module`. Then
delete the `promoted:` block from `domains/audit.md` entirely, and add a `history:` entry to each
folded principle's `provenance` record in the same file:

```yaml
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-general's own preamble."
```

- [ ] **Step 6: Repeat Step 5 for `packs/web-frontend/domains/audit.md`**

Check each entry's `domain:` field individually — do not assume they all belong to `coding-ts`;
fold each into the preamble of whichever pack domain file it actually names.

- [ ] **Step 7: Run the full test suite**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all pass, count = baseline + 2 (the two new tests from Task 8 Step 2 and this task's
Step 3).

- [ ] **Step 8: Verify no `promoted:` string remains anywhere in the repo's audit files**

Run: `grep -rn "^promoted:" domains/ packs/`
Expected: no matches.

- [ ] **Step 9: Commit**

```bash
git add scripts/corpus.py tests/test_corpus.py domains/audit.md domains/coding-general.md \
        packs/web-frontend/domains/audit.md packs/web-frontend/domains/coding-ts.md \
        packs/web-frontend/domains/coding-react.md packs/web-frontend/domains/css.md
git commit -m "corpus.py + audit files: retire promoted: sections, fold into domain preambles

Implements the locked 2026-07-21 decision. parse_audit_entries/annotate_graduated
no longer treat 'promoted:' as a section boundary; kernel-seed and web-frontend
pack audit files carry their formerly-promoted entries as preamble prose instead,
with a folded-to-preamble history entry each."
```

(Adjust the file list in the commit to whichever pack domain files actually received folded
content, per Step 6's per-entry check.)

---

### Task 10: `corpus.py` — domain co-occurrence tally on `record-gate`

**Files:**
- Modify: `scripts/corpus.py` (`record-gate` command implementation, state-block schema)
- Test: `tests/test_corpus.py`

**Interfaces:**
- Consumes: nothing new.
- Produces: a `co-occurrence:` list in the audit-layer state block — read `record-gate`'s current
  argument parsing (likely accepts `--domain D` possibly repeated) before designing the tally
  shape; find the exact current signature first.

- [ ] **Step 1: Read the current `record-gate` implementation and its existing tests**

Run: `grep -n "record-gate\|record_gate\|def cmd_record_gate" scripts/corpus.py`
Read the full function body and its `add_parser` argument definitions before writing anything.
Read every existing test whose name contains `record_gate` in `tests/test_corpus.py` to learn the
current state-block write format (`counters:`, `efficacy:` list shapes already established).

- [ ] **Step 2: Design the co-occurrence shape to match existing state-block conventions**

Model it as a flat list keyed by an unordered domain pair, incremented once per gate that loaded
both domains in the same spawn:

```yaml
co-occurrence:
  - domains: [color, motion]
    count: 3
```

`record-gate` already receives the set of domains loaded for the gate it's recording (this is
what populates the existing per-domain `counters:` entries) — reuse that same input rather than
adding a new CLI flag; when more than one domain is passed to a single `record-gate` invocation,
increment `count` for every unordered pair among them (for 3 domains, that's 3 pairs). If only one
domain was loaded, no pair exists — write nothing for that gate.

- [ ] **Step 3: Write the failing test first**

```python
def test_record_gate_tallies_domain_co_occurrence(tmp_path):
    project = make_test_project(tmp_path, domains=["color", "motion"])
    run_corpus_cli(["record-gate", "--domain", "color", "--domain", "motion",
                     "--ratified", "0", "--killed", "0", "--gate-violations", "0",
                     "--root", str(project)])
    state = read_state_block(project / "corpora" / "domains" / "audit.md")
    assert {"domains": ["color", "motion"], "count": 1} in state["co-occurrence"]
```

Adapt the exact fixture/helper names (`make_test_project`, `run_corpus_cli`, `read_state_block`)
to whatever helpers `tests/test_corpus.py` already defines for the existing `record-gate` tests —
read those tests first (Step 1) and reuse the same setup pattern rather than inventing new
helpers.

- [ ] **Step 4: Run to confirm it fails**

Run: `python3 -m pytest tests/test_corpus.py -k co_occurrence -v`
Expected: FAIL — `KeyError: 'co-occurrence'` or similar, since the field doesn't exist yet.

- [ ] **Step 5: Implement**

Add `co-occurrence` parsing to `empty_state()`, the state-block reader, and the state-block
writer (the same three places every other state-block field is threaded through — follow the
existing pattern for `counters:` exactly). In `cmd_record_gate`, after updating per-domain
counters, compute all unordered pairs from the gate's domain list with `itertools.combinations`
and increment (or create with `count: 1`) each pair's entry in `co-occurrence`.

- [ ] **Step 6: Run to confirm it passes**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all pass, baseline + 3 (Task 8's test + Task 9's test + this one).

- [ ] **Step 7: Add a second test for the two-gate accumulation case**

```python
def test_record_gate_co_occurrence_accumulates_across_gates(tmp_path):
    project = make_test_project(tmp_path, domains=["color", "motion"])
    for _ in range(2):
        run_corpus_cli(["record-gate", "--domain", "color", "--domain", "motion",
                         "--ratified", "0", "--killed", "0", "--gate-violations", "0",
                         "--root", str(project)])
    state = read_state_block(project / "corpora" / "domains" / "audit.md")
    assert {"domains": ["color", "motion"], "count": 2} in state["co-occurrence"]
```

- [ ] **Step 8: Run full suite**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all pass, baseline + 4.

- [ ] **Step 9: Update kernel.md's audit-file example block to show the new field**

In `kernel.md`, "Storage: working vs audit," add `co-occurrence:` to the fenced YAML example
(after the `efficacy:` block, before `library-drift:`):

```yaml
  co-occurrence:                   # per unordered domain pair, incremented at each gate that
                                    #   loaded both — mechanical byproduct of record-gate's inputs
    - domains: [color, motion]
      count: 3
```

- [ ] **Step 10: Commit**

```bash
git add scripts/corpus.py tests/test_corpus.py kernel.md
git commit -m "corpus.py: tally domain co-occurrence per spawn on record-gate

Implements v3-redesign-proposal.md phase 2: mechanical byproduct of what
record-gate already receives, no new operator ceremony. Feeds the reworded
composition-drift retrospective signal (kernel.md task 4)."
```

---

### Task 11: `corpus.py` — origin-layer tag (seed / pack / project)

**Files:**
- Modify: `scripts/corpus.py`
- Test: `tests/test_corpus.py`

**Interfaces:**
- Consumes: nothing new.
- Produces: an `origin:` field on audit entries, values `seed | pack | project`.

- [ ] **Step 1: Read how audit entries currently get their layer identity**

Run: `grep -n "def cmd_adopt\|fork-status\|forked-from\|domains_dir" scripts/corpus.py`
Confirm layer is currently inferred purely from *which directory* `--domains-dir`/`--audit`
point at (kernel `domains/`, pack `packs/<pack>/domains/`, or project `corpora/domains/`) — the
proposal calls this "directory-inference alone" and asks for something stronger recorded on the
entry itself.

- [ ] **Step 2: Write the failing test**

```python
def test_record_gate_stamps_origin_layer(tmp_path):
    project = make_test_project(tmp_path, domains=["color"])
    run_corpus_cli(["record-gate", "--domain", "color", "--origin", "project",
                     "--ratified", "1", "--killed", "0", "--gate-violations", "0",
                     "--root", str(project)])
    entries = parse_audit_entries(str(project / "corpora" / "domains" / "audit.md"))
    # origin is stamped per-domain in counters, not per-principle-id — see Step 3 for exact shape
```

Before finalizing this test, decide (Step 3) whether `origin` is a per-domain counter field or a
per-principle provenance field, then write the assertion against that actual shape — do not guess
the shape and write a test around a guess.

- [ ] **Step 3: Decide the shape and implement**

`origin` is a property of a *domain*, not of an individual principle (a whole domain file lives at
one layer) — add it to the per-domain `counters:` entry in the state block, alongside `since`,
`ratified`, `killed`, etc.:

```yaml
counters:
  - domain: color
    origin: pack              # seed | pack | project — stronger than directory-inference alone
    since: 2026-07-21
    ...
```

Default it by inferring from `--domains-dir` path shape when `--origin` is not explicitly passed
(kernel `domains/` → `seed`, `packs/*/domains/` → `pack`, `corpora/domains/` → `project`) so
existing callers of `record-gate` that don't pass `--origin` keep working — add an `--origin`
optional CLI argument that overrides the inference when the operator wants it explicit.

- [ ] **Step 4: Run the test to confirm it fails, then passes after implementation**

Run: `python3 -m pytest tests/test_corpus.py -k origin -v`
Expected: FAIL before the CLI argument and state-block field exist, PASS after.

- [ ] **Step 5: Add a test for the default-inference path (no `--origin` passed)**

```python
def test_record_gate_infers_origin_from_domains_dir(tmp_path):
    project = make_test_project(tmp_path, domains=["color"])
    run_corpus_cli(["record-gate", "--domain", "color",
                     "--ratified", "0", "--killed", "0", "--gate-violations", "0",
                     "--root", str(project)])
    state = read_state_block(project / "corpora" / "domains" / "audit.md")
    assert next(c for c in state["counters"] if c["domain"] == "color")["origin"] == "project"
```

- [ ] **Step 6: Run full suite**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all pass, baseline + 6.

- [ ] **Step 7: Update kernel.md's audit-file example to show `origin`**

Add `origin: pack` to the `counters:` example entry in "Storage: working vs audit" (already shown
above with `domain: coding-general`).

- [ ] **Step 8: Commit**

```bash
git add scripts/corpus.py tests/test_corpus.py kernel.md
git commit -m "corpus.py: stamp origin-layer (seed/pack/project) on domain counters

Implements v3-redesign-proposal.md phase 2: stronger than directory-inference
alone, so legibility and seed-promotion signals keep working as project-specific
domains multiply more freely under composed spawns."
```

---

### Task 12: Retire `coder.md`, `ux-designer.md`, `ui-designer.md`; create `domains/role-aliases.md`

**Files:**
- Delete: `coder.md`, `packs/web-frontend/coder.md`, `packs/web-frontend/ux-designer.md`,
  `packs/web-frontend/ui-designer.md`
- Create: `domains/role-aliases.md`
- Modify: `domains/coding-general.md` (fold coder.md's General Conventions + What-you-do
  judgment prose)
- Modify: `packs/web-frontend/domains/coding-ts.md`, `coding-react.md`, `css.md` (fold
  pack-coder.md's block-arrow-bodies / no-early-returns conventions)
- Modify: `packs/web-frontend/domains/design-method.md` (fold ux-designer.md's/ui-designer.md's
  process judgment — flow-before-visual sequencing, library-authority rules, spec-before-code)
- Modify: `packs/web-frontend/domains/motion.md`, `recoverability.md`, `lists-selection.md`,
  `forms-inputs.md`, `validation-feedback.md`, `color.md`, `surfaces-elevation.md`,
  `visual-hierarchy.md`, `wizards-flows.md`, `ranking-evaluation.md` — only if content read in
  Step 1 actually belongs there per the fit-justification test from Task 2; do not force-fit.

**Interfaces:**
- Consumes: Task 1's stance/composition model, Task 2's fit-justification requirement, Task 5's
  fold-to-preamble convention.
- Produces: `domains/role-aliases.md` — the file Task 13/14 (SKILL.md, bootstrap.md) reference
  when describing routing shorthand.

This task is content judgment, not mechanical find-replace — read the full text of all four files
being deleted (already read once in this session; re-read to work from, not from memory) before
writing anything.

- [ ] **Step 1: Catalogue what's in each of the four files, sorted into three buckets**

For `coder.md`, `packs/web-frontend/coder.md`, `packs/web-frontend/ux-designer.md`, and
`packs/web-frontend/ui-designer.md`, sort every paragraph/bullet into:

  - **(a) Stance/identity prose** — already covered by kernel.md's "Generative stance" section
    (Task 1). Discard; do not duplicate. Example: ui-designer.md's "Generative stance — divergent"
    section.
  - **(b) Judgment prose that passes the fit-justification test against an existing domain** —
    migrate into that domain's preamble or as a new `principles:` entry with full
    `id/rule/condition/reason/provenance` (provenance: `"2026-07-21, v3 lens-collapse migration
    from <old file>."`). Example: coder.md's "Explicit by Default" / "Prefer the error-exposing
    form" meta-conventions clearly belong in `coding-general.md`'s preamble (they're already
    partially there per Task 9's fold — check for duplication before adding); pack coder.md's
    "Block arrow bodies always" and "No early returns" belong in `coding-react.md` or
    `coding-ts.md` (read both files' current preambles first to place correctly, per-language).
  - **(c) Task-mechanics prose that is neither stance nor domain judgment** — output format
    instructions ("produce a user flow spec structured as: 1. User and goal... 2. Current
    experience..."), "what you do" procedural checklists (read config first, read the library
    first), "what you don't do" scope boundaries. This has no domain home — it describes how to
    execute a composed spawn of this shape, not a weighable rule. Route to `domains/role-aliases.md`
    (Step 2) as the alias's `notes:` field — kept as operational reference for the orchestrator
    composing that alias, explicitly NOT weighable, NOT ratified, NOT a principle.

Do not skip reading; the exact placement of each paragraph is the actual work of this task. Where
a paragraph could pass the fit test for more than one domain, or for none, surface it as a comment
in the commit message rather than guessing — this is exactly the kind of call the plan says stays
human-judged.

- [ ] **Step 2: Create `domains/role-aliases.md`**

```markdown
# Role aliases — routing shorthand, not a schema entity

Not a domain: no `principles:`, no ratify gate, no kill log. A recurring stance + domain-subset
composition the orchestrator has reused often enough to be worth naming, so a spawn brief (see
`kernel.md`, "The spawn brief") can write `composition: coder` instead of re-listing every domain.
Aliases accumulate the same way domains do — from repeated, observed composition, never declared
up front. Adding, renaming, or retiring an alias is an ordinary operator/orchestrator judgment
call, not a ratify-gate action (nothing here is a corpus proposal).

Seeded from the kernel-seed and web-frontend pack layers, 2026-07-21 (v3 lens-collapse migration):

```yaml
aliases:
  - name: coder
    stance: convergent
    domains: [coding-general]        # + coding-ts, coding-react, css when role-pack: web-frontend
    notes: >
      Read corpora/config.md first for registered utilities and verification commands. Read the
      task, explore the codebase, implement precisely. Run the project's verification commands
      before finishing. Report a tradeoffs block for any spec/task where implementation cost
      clearly outweighs the value, rather than implementing or skipping silently.

  - name: ux-design
    stance: convergent
    domains: [wizards-flows, ranking-evaluation, motion, validation-feedback, recoverability,
              lists-selection, forms-inputs, design-method]
    notes: >
      Read the project's UX library first; it is authoritative for current experience patterns.
      Output is a user flow spec: user and goal, current experience, proposed flow per step
      (what's seen, actions available, system response, error/empty/edge cases), clarity
      requirements, open questions only if genuinely unresolvable. Describe what the user
      perceives and does, never visual layout or styling.

  - name: ui-design
    stance: divergent
    domains: [color, surfaces-elevation, visual-hierarchy, motion, validation-feedback,
              recoverability, lists-selection, forms-inputs, design-method]
    notes: >
      Read the project's UI library first; it is authoritative for the color system, typography,
      spacing, component patterns, and visual character. Output is a design spec: current state,
      proposed design per UI state (elements, layout, hierarchy, interaction behavior, empty/
      loading/selected/error states), open questions only if genuinely unresolvable. Describe
      proportions in relative terms — no pixel values, no CSS class names, no component names.
```
```

Fill the `domains:` lists and `notes:` fields from what Step 1 actually catalogued, not from this
sketch verbatim — this text is a starting shape, not the final content; reconcile it against the
real source files before writing the file.

- [ ] **Step 3: Migrate bucket-(b) content into domain files**

For each item sorted into bucket (b) in Step 1, add it to the target domain's preamble (if it's
foundational/stable framing) or as a full `principles:` entry (if it's a conditional judgment
call with a real fork alternative — apply Task 2's genuine-fork test before adding as a
principle). Record provenance in the layer's `audit.md` for any new `principles:` entry.

- [ ] **Step 4: Delete the four lens files**

```bash
git rm coder.md packs/web-frontend/coder.md packs/web-frontend/ux-designer.md packs/web-frontend/ui-designer.md
```

- [ ] **Step 5: Grep the repo for any remaining reference to the deleted files**

Run: `grep -rln "coder\.md\|ux-designer\.md\|ui-designer\.md" --include="*.md" .`
Expected: hits only in files Tasks 13/14 will fix (`SKILL.md`, `bootstrap.md`, `README.md`,
`LINEAGE.md` — LINEAGE.md's historical mentions stay, per the proposal's phase-5 exception for
comparative/historical framing). List every hit here so those tasks have a checklist.

- [ ] **Step 6: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all still pass — this task touches no Python.

- [ ] **Step 7: Commit**

```bash
git add domains/role-aliases.md domains/coding-general.md packs/web-frontend/domains/
git commit -m "retire coder.md, ux-designer.md, ui-designer.md into domain content + role-aliases.md

Implements v3-redesign-proposal.md's core lens-collapse: persona/stance prose was
already covered by kernel.md's Generative stance section; judgment prose migrated
into domain preambles/principles per-domain with the fit-justification test;
task-mechanics prose (spec format, read-this-first checklists) has no domain home
and moves to role-aliases.md's notes field, explicitly non-normative."
```

---

### Task 13: SKILL.md — describe composition routing, drop fixed-lens references

**Files:**
- Modify: `SKILL.md`

**Interfaces:**
- Consumes: Task 12's `domains/role-aliases.md`, Task 6's spawn brief, Task 1's stance/composition
  terms.

- [ ] **Step 1: Read the full current `SKILL.md` and mark every line matching Task 12 Step 5's
  grep list**

Read the file top to bottom. For each place it says "route to the coder," "spawn the UX
designer," "the UI designer's lens," etc., rewrite it to describe composing a spawn: state the
stance and which domains (or which alias from `domains/role-aliases.md`) the orchestrator loads
for that task shape, referencing the spawn brief (Task 6) as the mechanism.

- [ ] **Step 2: Update the bootstrap-phase routing table/prose (Phase 2/Phase 3 references to
  "UI designer"/"UX designer" as named roles)**

Where `SKILL.md` currently says something like "route a UI designer workstream," change to "route
a divergent workstream composed from the `ui-design` alias (`color`, `surfaces-elevation`,
`visual-hierarchy` + shared domains — see `domains/role-aliases.md`)" — concrete enough that a
reader unfamiliar with the old model still knows exactly what loads.

- [ ] **Step 3: Grep for leftover stale terms**

Run: `grep -n "lens file\|declared domains\|role file\|the coder$\|the UX designer\|the UI designer" SKILL.md`
Fix any remaining hits — "the coder"/"the UX designer" as a bare noun phrase should become "a
coder-composed spawn" or similar, consistent with Task 12's terminology.

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all pass (no Python touched).

- [ ] **Step 5: Commit**

```bash
git add SKILL.md
git commit -m "SKILL.md: describe stance-composed spawn routing instead of fixed lenses

Implements v3-redesign-proposal.md phase 3, sized correctly per the file-impact
correction: this is a conceptual rewrite of the role-listing/routing prose, not
a rename."
```

---

### Task 14: bootstrap.md — same treatment as SKILL.md

**Files:**
- Modify: `bootstrap.md`

**Interfaces:**
- Consumes: same as Task 13.

- [ ] **Step 1: Read the full current `bootstrap.md`**

Same process as Task 13 Step 1 — mark every fixed-lens reference, rewrite to composition
language, reference `domains/role-aliases.md` for the `ux-design`/`ui-design`/`coder`
compositions the bootstrap phases use.

- [ ] **Step 2: Grep for leftover stale terms**

Run: `grep -n "lens file\|declared domains\|role file\|the coder$\|the UX designer\|the UI designer" bootstrap.md`
Fix any remaining hits.

- [ ] **Step 3: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add bootstrap.md
git commit -m "bootstrap.md: describe stance-composed spawn routing instead of fixed lenses

Companion to the SKILL.md rewrite (Task 13), same v3-redesign-proposal.md phase 3 scope."
```

---

### Task 15: README.md — role-listing prose

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: same as Tasks 13/14.

- [ ] **Step 1: Read the full current `README.md`, find the role-listing section**

Rewrite the section describing the system's roles (likely lists "coder, UX designer, UI
designer, planner, orchestrator" as fixed roles) to describe: two fixed entities (orchestrator,
planner) plus composed spawns using the `domains/role-aliases.md` shorthand, per the proposal's
explicit note that this needed "a fresh impact pass... this is more than a rename."

- [ ] **Step 2: Grep for leftover stale terms**

Run: `grep -n "lens file\|declared domains\|role file" README.md`

- [ ] **Step 3: Run tests**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: all pass.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "README.md: describe the stance-composed spawn model

Completes v3-redesign-proposal.md phase 3's content-rewrite scope for this repo
(kernel.md, corpus.py, SKILL.md, bootstrap.md, README.md, web-frontend pack)."
```

---

### Task 16: Full-repo consistency sweep and LINEAGE.md entry

**Files:**
- Modify: `LINEAGE.md` (new entry)
- Modify: any file surfaced by the final grep sweep below

**Interfaces:**
- Consumes: everything above.

- [ ] **Step 1: Repo-wide grep for stale terms**

```bash
grep -rn "role: ux-designer\|role: ui-designer\|declared domains\|lens file\|role file\b" \
  --include="*.md" . | grep -v "^./LINEAGE.md"
```

Expected: no matches outside `LINEAGE.md` (whose historical framing is explicitly preserved per
the proposal's phase-5 note — comparative/historical framing belongs there).

- [ ] **Step 2: Confirm `v1-alpha` and `v2-domain-scoped` tags both exist**

Run: `git tag -l -n1`
Expected: both tags listed (Phase 0 already completed this session, before this plan was
written).

- [ ] **Step 3: Add the LINEAGE.md entry for the v3 transition**

Append a new dated section to `LINEAGE.md` summarizing: what changed (lens-collapse to
stance+composition), why (convenience-container mis-filing, the slider-puzzle-adjacent
observation that named lenses invite the shortcut), what was explicitly kept (`adopt`, the
orchestrator/planner as fixed entities), what was retired (`promoted:` as a section, the `role:`
enum in two schemas, three lens files), and the tag markers (`v1-alpha`, `v2-domain-scoped`) a
future reader can diff against. Reference `v3-redesign-proposal.md` by name as the reasoning
document this session ratified from.

- [ ] **Step 4: Run the full test suite one final time**

Run: `python3 -m pytest tests/test_corpus.py -q`
Expected: `33 passed` + however many tests Tasks 8/9/10/11 added — confirm the exact final count
and state it in this task's commit message.

- [ ] **Step 5: Commit**

```bash
git add LINEAGE.md
git commit -m "LINEAGE.md: v3 stance-composed-lenses transition entry

Closes out v3-redesign-proposal.md phases 0-3 for this repo. FAMOUS/Blog/Meridian
upgrade path (proposal phase 4) intentionally not started here."
```

---

## Self-Review Notes (from plan authoring)

- **Spec coverage:** Phases 0 (done pre-plan), 1 (Tasks 1–7), 2 (Tasks 8–11), 3 (Tasks 12–16) all
  have tasks. Phases 4 (upgrade path) and 5 (old-framing cleanup pass) are explicitly out of
  scope per the operator's chosen scope this session.
- **Known judgment-heavy step:** Task 12 cannot be fully pre-specified — placing each paragraph of
  four prose-heavy files into the right domain is exactly the kind of call the proposal reserves
  for the ratify gate's human judgment. The task gives the sorting method (three buckets + the
  fit-justification test) rather than the final placement of every sentence.
- **Type/name consistency check:** `DEFERRED_STANCE_ENUM` (Task 8), `co-occurrence:` (Task 10),
  `origin:` (Task 11), `domains/role-aliases.md` (Task 12) are each introduced once and referenced
  consistently by later tasks under the same name.
