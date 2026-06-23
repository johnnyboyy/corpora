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
  status: # proposed | ratified. Only ratified principles guide work.
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
  `id / rule / condition / reason / status / see-also`, plus the `killed:` log. This is the only
  part loaded when a role works, inline or spawned.
- **Audit file** (`domains/audit.md`, one per layer — kernel-seed, each pack, and each project) —
  per-principle `provenance` keyed by `id` (each entry noting its `domain`), the `promoted:` block,
  and per-kill audit metadata. Loaded only at ratify and retrospective time, by the orchestrator —
  never in a role's working context.

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
- coding-js-react         # when role-pack: web-frontend
- css                     # when role-pack: web-frontend
```

The declaration is checked into the role file, not computed at runtime. Assembly is therefore a
deterministic, inspectable fact — read the lens, know exactly what loads. An agent never selects
its own constraints; there is no runtime relevance call on a working role's corpus. A domain may
be conditional on the project's `role-pack` (a pack adds domains to a role's declaration; it never
adds a new role).

### Two load modes

- **Working load** (generation, hard isolation): a role's declared domains, *working files only*.
  Lean and contamination-safe. This is every spawn and every inline role session.
- **Audit load** (synthesis, human-gated): the orchestrator loads relevant domains *broadly,
  including audit and kill metadata*, at ratify and retrospective time. Breadth is safe here
  because it is not constrained generation and it is gated by the operator.

Role isolation is enforced at this level: the coder declares coding domains and never design
domains, so design context cannot bleed into coding work. Two *design* lenses sharing a design
domain is allowed and intended — that is the point of domain-scoping. The seam that matters
(design decisions contaminating later coding) is preserved because no coding lens declares a
design domain. See LINEAGE.md, "Role isolation."

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
  This is the realization of the thinner kernel-level claim noted in LINEAGE ("a generative role
  must know whether its domain rewards convergence or divergence and anchor accordingly").

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

- A role proposes a principle (`status: proposed`) as part of its output. It cannot write a corpus.
- The operator (or a ratifying role acting under standing rules) reviews and ratifies or rejects.
- **Rejections are kept** with their reason. The kill log is the highest-signal training data.
- Structural changes (split a domain, fork a role, add an explorer, change a route) go through the
  same gate.

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
  status: ratified
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

Per-kill audit detail (`provenance`, `killed:` date) goes in the layer's audit file, keyed by `id`.

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
the project domain (if any) of the same name. A project may also have domains with no seed
counterpart (project-specific subjects, e.g. `spatial-metaphor`).

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

**Anti-overfitting (any domain whose principles were earned in a single project shape):** surface
which ratified principles should stay provisional — weighable, not promoted — until tested against
another shape. A principle pressure-tested in only one climate is a promotion risk, not a default.

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
