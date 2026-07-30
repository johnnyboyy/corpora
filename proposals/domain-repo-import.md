# Proposal: domain schema, seed/project dissolution, and cross-repo import

**Status: implemented 2026-07-30 (§1–§5).** `corpus.py`, `kernel.md`, `general-operation.md`,
`bootstrap.md`, `SKILL.md`, `README.md`, `domains/principle-judgment.md`, `domains/coding-ts.md`,
and `domains/audit.md` all changed for this proposal; `processes/domain-repo-migration.md` is new.
The two related proposals below (principle elicitation through operator dialogue; monorepo support)
remain draft, not implemented — out of scope for this pass. Downstream projects (Blog, FAMOUS, etc.)
still need to actually run `migrate-domains` against their own repos before their next corpora
session under this model — that migration could not be run from this repo, since those projects
live elsewhere.

---

## 1. The domain schema

Every domain file — seed or project, this skill's own or any other corpora installation's —
becomes one uniform shape:

```yaml
---
subject: <coding|design|process>
posture: <guardrail|generative>
applies-when: [...]
units-of-work: [...]
universal: <bool>
---

# Domain: <name>

<minimal framing prose — what this domain is about, kept to what a reader needs before the
entries below, not restated rule-by-rule>

last-retrospective: <date|none>

conventions:
  - id: <slug>
    rule: "..."
    reason: "..."
    # no condition — unconditioned by definition, applies whenever this domain loads

principles:
  - id: <slug>
    rule: "..."
    condition: "..."
    reason: "..."
    see-also: [...]

killed:
  - id: <slug>
    rule: "..."
    kill_type: <quality|container|attribution-noise>
    reason_killed: "..."
```

**What's new:** `conventions:`, a structured home for what `kernel.md`'s write-back format
currently calls "folded to preamble" — a principle whose `condition` has become friction-without-
benefit to keep checking. Today, folding turns a structured, `id`-addressable entry into
unstructured prose: no `id`, not killable, not graduatable, not selectively importable by anyone.
`coding-ts.md`'s "no early returns" and "block arrow bodies always" are the current live examples
of content this would formalize. A principle graduates from `principles:` to `conventions:` by
dropping `condition`, keeping its `id` and audit trail — not by dissolving into prose.

`lint-domains` gets a `conventions:` shape check (same as `principles:`/`killed:` today); `manifest`
lists convention ids alongside principle ids; the audit file's per-`id` provenance keying is
unaffected — `conventions:` entries key into `domains/audit.md` exactly like `principles:` entries
do now.

## 2. Dissolving seed/project

Today: `domains/<name>.md` in this skill's own repo (seed) and `corpora/domains/<name>.md` in a
project (project) concatenate live, unconditionally, every load. `project_domain_sources()` in
`corpus.py` merges `{name: {"seed": path, "project": path}}` and every load-bearing command
(`select`, `compose-spawn-prompt`, `manifest`) reads through that merge.

Proposed: no more automatic merge. A project's `corpora/domains/` is the whole domain set for that
project. This skill's own `domains/` stops being structurally privileged and becomes an ordinary
import source — the *default* one, with a bootstrap-time bulk-import convenience (below), but not a
live-concatenated layer. Every corpora-managed location — this skill's repo, any bootstrapped
project — becomes symmetric: a place with a `domains/` + `audit.md`, importable from and exportable
to, using the same mechanism either direction.

This is mostly a simplification, not just a behavior change: `corpus.py`'s `--domains-dir`/`--audit`
override already treats "any domains-dir + audit.md pair" generically (`kill-report`,
`graduate-kill`, `lint-domains`, `measure`, `record-gate` all already operate on this skill's own
`domains/` today, via that override). Dropping the seed/project merge removes a layer of
special-casing from `select`/`compose-spawn-prompt`/`domain_files()` rather than adding one.

**Retrospective signal #5 (seed-promotion candidate) becomes the export direction of the same
mechanism.** "Promote to seed" is "import this principle into the skill's own domain repo" —
symmetric with importing the other way, not a separate concept. `domains/retrospective.md`'s
`seed-promotion-candidate` principle's *judgment* (when a principle reads as general enough to
travel) doesn't change; only the mechanical act of promoting it does.

## 3. Import — interactive, per-principle, redirectable

Decided: interactive per-*principle*, not a flat batch, and not per-domain. Browsing a source and
picking individual principles (or conventions) lets the operator scope a picked entry to a
*different* destination domain than the one it came from in the source — the same domain-
assignment judgment already exercised at the ordinary ratify gate (`kernel.md`, "Domain assignment
at the gate"), applied to an imported entry instead of a freshly-proposed one.

Mechanically, this reuses the existing candidate/gate pipeline rather than inventing a parallel one:
an import pass is a new *producer* of candidates, structurally the same relationship
`discovery-agent.md`/`session-harvest-agent.md` already have to `reading/candidates.md` and the
gate. The difference is what's being proposed: not a freshly-mined judgment call, but an
*already-ratified* principle from another corpus, re-proposed here with provenance recording where
it actually came from and when it was first ratified there — `kind: judgment` by default (it
already cleared this exact bar once), the fork test still available if the operator wants to
re-examine it rather than rubber-stamp it.

Candidate shape for an import (extends the existing candidate schema with an `imported-from` block
rather than replacing it):

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

**Default-pool bulk-import convenience, decided as an ordinary use of the same mechanism, not a
separate code path:** bootstrap can still offer "import everything applicable from this skill's
default pool" as a fast path — a project shouldn't have to hand-pick 50+ principles across a dozen
domains just to get `coding-general`/`coding-ts`/etc. on day one. That fast path is exactly
"select every principle+convention from every domain whose `applies-when`/`units-of-work` already
matches this project's config, propose all of them as import candidates in one batch, ratify in
bulk" — the same interactive-per-principle mechanism, just with the operator's answer defaulted to
"yes to all" instead of asked one at a time.

## 4. Operator-direct authorship (the smaller, related ask)

No new mechanism needed — already possible today via `record-gate --ratified 1` run standalone
(no handoff required) plus a hand-written provenance entry. The gap is that nothing currently *says*
this is sanctioned; `kernel.md`'s "propose → ratify → promote, never write-directly" reads as
forbidding it, when what it actually forbids is a *spawn* writing directly. Fix is documentation,
not code: add an explicit provenance convention —
`"Operator-authored, <date>, based on observed <behavior>, root-caused and refined."` — to
`kernel.md`'s write-back section and `domains/principle-judgment.md`.

## 5. Migration — as its own process file, not a one-off script

Per operator direction: this ships as a real corpora process (trigger/procedure, matching
`ui-library-init.md`/`retrospective.md`'s shape), not a bare `corpus.py` command with no documented
procedure around it. Working name: `domain-repo-migration.md`.

- **Trigger:** a project bootstrapped under the old seed/project model is about to run corpora
  under the new no-merge model for the first time. One-time per project.
- **Procedure (sketch, to be written properly at implementation time):**
  1. Compute the project's current *effective* domain set exactly as it loads today — every seed
     domain the project's `applies-when`/`units-of-work` would match, concatenated with whatever
     already exists in `corpora/domains/<name>.md`.
  2. Materialize that effective set into the project's own `corpora/domains/` — one working file per
     domain, seed content and project content merged into a single file, principles/conventions/
     killed all preserved with their existing `id`s and audit history intact (this is a
     write operation on the project's *own* files only; the skill's own `domains/` and
     `domains/audit.md` are never touched by a project's migration).
  3. Record migration provenance per domain (something like `history: type: migrated-from-seed,
     date: <date>`) so a later reader can see this content arrived via migration, not fresh import.
  4. Only after materialization succeeds and is verified (`corpus.py verify` clean against the
     newly-populated `corpora/domains/`) does the project stop reading the live seed layer.
- **Rollback:** since this only writes to the project's own `corpora/domains/` and never touches the
  skill's own `domains/`, the migration is safe to re-run or abandon — the project's prior
  (pre-migration) state is whatever was in `corpora/domains/` before step 2, recoverable via git the
  same way any other working-tree change is.

## 6. Open questions for implementation time (not resolved by this draft)

- Exact `corpus.py` command surface for import (`import-list --source <path>`, `import-candidate
  --source <path> --domain <d> --id <id> [--as-domain <d2>] [--as-id <id2>]`?) — sketched above in
  spirit, not finalized.
- Whether `conventions:` entries participate in `record-gate`'s `--fired`/`--violated`/`--idle`
  audit classification the same way `principles:` do, or are exempt (per `kernel.md`'s existing
  "an entry exempt from condition-checking is more dangerous, not more trustworthy" stance on a
  separate authority tier — probably *not* exempt, but worth confirming against that existing
  principle rather than assuming).
- Whether a project can import from another *project* (not just this skill's repo) without that
  other project granting any special access — i.e. is "any project running corpora is a domain
  repo" purely about file-format compatibility (any `corpora/domains/` is readable by anyone with
  filesystem/repo access), or does it need an explicit opt-in/publish step. Current lean: pure
  file-format compatibility, no publish step — matches "corpora doesn't decide artifact placement
  unilaterally" reasoning already used elsewhere (`bootstrap.md`, "The config file").
- Whether to dogfood this the same way the process/judgment split was dogfaded today — build against
  a throwaway demo project first (mirroring `corpora-exercise-blog`), not the first real project it
  touches.

---

# Related proposal: principle elicitation through operator dialogue

**Status: draft, not implemented.**

Every existing way a principle enters corpora starts from an *event*: a spawn does work and
proposes something, a session gets mined after the fact, a source gets read, a domain repo gets
imported from. None of them start from the operator simply *knowing* a rule they already hold and
stating it. That path already exists — it's how corpora itself began. `README.md`'s own account:
personal rules, described with their reasons, refined through dialogue until "the reason was doing
much more work than the rule on its own," and a meta-principle (Explicit by Default / the Reader
Tax) condensed out of the specific ones. That process happened once, informally, and produced the
whole system. It has never been written down as something that runs again.

**Trigger:** operator-initiated — most naturally offered as an optional step during bootstrap
("besides what gets detected, do you have standing rules of your own?"), but not limited to
bootstrap; the operator should be able to invoke it any time they have an opinion to formalize.

**Composition:** convergent stance, composing `interviewing` + `principle-judgment` — no new domain
judgment needed; both already contain exactly what this requires; this is a new *process* applying
existing domains in a context neither was written for yet (a dialogue whose subject is the
operator's own stated belief, not a spawn's work output or a mined transcript).

**Procedure (sketch):**
1. The operator states a rule as they'd say it naturally — a habit, a pet peeve, "I always/never do
   X."
2. Ask one question at a time (`interviewing.md`) to draw out the *reason* — not "because it's
   better," but the specific mechanism or incident the rule actually guards against — and the
   *condition* — is this universal, or scoped to something narrower than the operator's first
   phrasing implies?
3. Apply `principle-judgment.md`'s tests to what's drawn out, the same as any other candidate —
   `consuming-lens-includes-agent-vs-human-gap` matters most here specifically: a personal rule is
   disproportionately likely to be a human-memory or habit-transfer reminder ("I always forget to
   X") rather than something an agent — which doesn't forget, doesn't get tired, reads the current
   project state fresh every time — actually needs stated. Surface that distinction to the operator
   directly rather than silently ratifying a rule that would change nothing about agent behavior.
4. Restate the drawn-out rule/condition/reason back for confirmation — `name-clear-direction-
   dont-manufacture-choice`, not a menu of options where the operator already gave one clear answer.
5. Route through the ordinary ratify gate and domain assignment — this is a different way of
   *arriving* at a well-formed proposal, not a bypass of how proposals get written back.

**Open question:** whether repeated use of this process on the same operator's rules is itself a
retrospective-worthy signal — a cluster of personal rules that keep resolving to the same underlying
test is exactly what `structural-kinship-condensation-candidate` (`domains/retrospective.md`)
already looks for, and is how the founding session actually produced a meta-principle rather than a
pile of unrelated ones. Worth naming explicitly rather than assuming it'll be noticed.

---

# Related proposal: monorepo — multiple corpora directories scoped to individual apps

**Status: partially implemented 2026-07-30.** Directory resolution (the first bullet below) shipped
as `corpus.py resolve-root`/`check-root-boundary` (`kernel.md`, "Monorepo root resolution") once a
real second root (FAMOUS's `admin/`) existed to build and test it against. The other two bullets —
bootstrapping a new sibling app's import-source ordering, and explicitly sanctioning a root-level
app-less `corpora/` — remain draft.

Today corpora assumes one `corpora/` at a project root. A monorepo (`apps/web/corpora/`,
`apps/mobile/corpora/`, `packages/shared/corpora/`, or a shared root-level `corpora/` with no app of
its own) needs more than one, and something needs to decide which one governs a given task.

This turns out to be a narrower gap than it first looks, mostly because of two things already true:
`corpus.py` already parameterizes every command by `--root` — nothing in it assumes a single
repo-root instance — and the domain-repo import mechanism above already gives sibling apps (or a
shared root) a way to share judgment without a live seed-style merge. What's actually missing is
orchestrator-level routing judgment, not new mechanism.

**What needs deciding at implementation time:**
- **Directory resolution — IMPLEMENTED.** `corpus.py resolve-root --file <path>` resolves by
  nearest-ancestor walk from a file up toward the filesystem root, stopping at the first
  `corpora/config.md` found (the same resolution model `tsconfig.json`/`package.json` already use).
  `corpus.py check-root-boundary --files <f1,f2,...>` is the mechanical split signal for a task
  spanning two apps' corpora roots — fails (exit 2), naming each root's files, rather than letting a
  single spawn straddle both; the operator/planner splits it into one unit of work per root from
  there. Automatic resolution only (no manual `sibling-corpora:` declaration) — decided over a
  declaration-based alternative specifically so the check can't go stale.
- **Bootstrapping a new sibling app.** Same `bootstrap.md` flow, but should offer to import from a
  sibling or shared-root `corpora/domains/` (via the mechanism in the main proposal above) as the
  first import source considered, ahead of this skill's own default pool — a monorepo's own
  accumulated judgment (a company-wide `coding-general` refinement, a shared design system) is
  usually more relevant to a new sibling app than the skill's generic seed pool is.
- **A root-level, app-less `corpora/`.** Worth explicitly sanctioning as a valid pattern: a
  monorepo-root `corpora/domains/` with no `corpora/config.md`-driven project of its own, existing
  purely as a shared import source every sibling app's `corpora/` can pull from and export back to —
  a natural, even encouraged use of "any corpora location is a domain repo," not a special case that
  needs its own mechanism.
