# The Role Kernel

The kernel is the shared mechanism every role inherits. A role is `kernel + seed corpus + domain prompt`.
The kernel is not code — it is a discipline made of files plus a loop.

---

## The principle schema

A corpus is a list of **principles**. Every principle has four required fields plus optional ones:

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
  see-also: # OPTIONAL. ids of related principles (same corpus or another role's).
```

Notes on fields:

- **condition** is structurally the most important. When two ratified principles have conditions
  that partition the same space, the corpus is telling you it has become two domains — a fork candidate.
- **reason** travels with the rule always. This is what lets the role think rather than pattern-match:
  "the reason was X; this task is Y, so the rule doesn't bind here."
- **provenance** is cheap to record and invaluable for trusting or retiring a principle later.

---

## The ratify gate

Every cross-boundary change is **propose → ratify → promote**, never write-directly.

- A role proposes a principle (`status: proposed`) as part of its output. It cannot write its own corpus.
- The operator (or a ratifying role acting under standing rules) reviews and ratifies or rejects.
- **Rejections are kept** with their reason. The kill log is the highest-signal training data.
- Structural changes (fork a role, add an explorer, change a route) go through the same gate.

### Write-back format

Ratified principle — append before the `promoted:` line:

```yaml
- id: principle-id
  rule: "The guidance."
  condition: "When this applies."
  reason: "Why — the justification."
  provenance: "Date, task, context."
  status: ratified
```

Promoted principle — when a corpus entry graduates to the role prompt itself (becomes a baked-in
default rather than a weighable principle), move it from `principles:` to `promoted:`. Keep the
entry so the audit trail is legible — a promoted principle that reappears as a corpus proposal
is a signal of regression, not new insight.

```yaml
- id: principle-id
  promoted_to: "<role> role prompt — <section name>"
  provenance: "Date, task, context. Note if it was subsumed by a meta-rule."
```

The trigger for promotion: a principle has been ratified long enough that checking its
`condition` and `reason` before every task is friction without benefit — the judgment has
become the default. Or: several principles share a common root justification; the meta-rule
that unifies them gets promoted, and the individual entries become examples of it.

**Promotion restraint.** Before promoting, ask: would the role still need to reconsider this when
the project context changes? Promote only if the judgment is stable *across the kinds of projects
the role serves* — or is so foundational that contestability has genuinely become noise — not merely
because it has repeated inside one project family. A principle earned only in (say) web work may feel
universal while still drawing its truth from the current climate; promoting it bakes that overfitting
into the prompt, where it stops being weighable. When in doubt, leave it in `principles:` where its
`condition` and `reason` can still be checked against an unfamiliar case.

Killed entry — append at end of file:

```yaml
- rule: "The rejected rule."
  reason_killed: "Operator's reason."
  provenance: "Date, task, context."
```

---

## Project corpora

In any project using this system, project-specific accumulated judgment lives at:

```
<project-root>/corpora/
  coder.md
  orchestrator.md
  ux-designer.md
  ui-designer.md
```

These files use the same schema and extend the seed corpus in the skill.
Seed corpus = general principles that travel across projects.
Project corpus = principles earned in this specific project.
Both apply when a role runs — seed first, then project.

The four-role set is the default configuration, not a law of the kernel. The kernel itself is
the mechanism (schema, ratify gate, retrospective, lifecycle) and is indifferent to which roles
exist. Two layers instantiate the roles: a stack-agnostic kernel layer (orchestrator + base coder)
that is always present, and an optional role pack selected by the project's `corpora/config.md`
(`role-pack:`) that overlays stack-specific conventions and corpus onto those roles. A pack adds
depth to existing roles, not new roles — and a project with no UI runs on the kernel layer alone,
with the designer roles simply inactive. Each role runs in isolation: its context is its own
file(s) and its own project corpus, never another role's (see LINEAGE.md, "Role isolation").

---

## The retrospective

Run at two cadences. Same faculty, different direction.

**Forward (per-task):** Route the task to the right role(s). Guard against contamination — is the
working context holding concerns from another mode?

**Backward (periodic):** Surface three signals as proposals for the operator:

1. **Contamination detected** — attention was spent on concerns outside the task's mode. Fix routing.
2. **Corpus tension → fork** — two ratified principles have conditions that partition the same space.
   Proposal: fork the role into two. Advisory only — operator judges whether the partition is a real seam.
   *What counts:* one cluster of coder principles clearly governs UI component work and another governs
   backend data workflows, and they repeatedly give *opposing* advice under their respective conditions —
   that is a seam. *What doesn't:* one principle about helper extraction and another about verification
   commands are simply different topics, not a partition. The seam is discovered here, from accumulated
   tension — never assumed up front from how a human team would be organized.
3. **Convergence → explorer** — corpus has stopped changing, corrections rare. Proposal: pair with an
   explorer to prevent calcification.

**Anti-overfitting (coder, and any role whose work has been single-context):** surface which ratified
principles were earned only in one project shape (e.g. UI/web work) and should stay provisional —
weighable, not promoted — until tested against another shape. A principle that has only ever been
pressure-tested in one climate is a promotion risk, not a settled default.

Each corpus carries `last-retrospective: <date>` at the top to make convergence measurable.

---

## Role lifecycle

```
spawn (seed corpus from skill)
  → accumulate (work + retrospective surface principles, operator ratifies)
  → [retrospective may propose FORK if corpus tension appears]
  → converge / lock (corpus stabilizes, corrections rare)
  → [retrospective proposes pairing with an EXPLORER]
```

Growth is differentiation under accumulated tension — never promotion up a ladder.
