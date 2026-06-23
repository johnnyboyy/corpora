# Corpora Skill Redesign

## Problem

The current system conflates two distinct concerns inside the role construct:

1. **Judgment accumulation** — collecting, scoping, ratifying, and retrieving learned decisions
2. **Role boundary enforcement** — isolating concerns, preventing context contamination, routing tasks

When these live in the same structure, each degrades the other. Role boundaries must be stable
enough to enforce, which resists the revision that good judgment accumulation requires. Corpus
organization ends up shaped by role topology rather than by what conditions actually surface
interesting decisions. A judgment that belongs to two roles either lives in both (fragmented) or
gets killed for "role boundary" reasons rather than because it was wrong.

The same problem exists at the repo layer. Seed corpora (general judgment that travels with a role
across projects) are currently organized by role for the same reason project corpora are — the role
is the container. But the container is wrong at both layers.

A secondary problem: killed entries are already injected at runtime as active guidance, not just
consulted at retrospective time. But they carry no `id`, making them unsearchable,
unreferenceable, and invisible to `see-also`. A killed entry that resurfaces as a new proposal
should be identifiable as a recurrence, not treated as new signal. More importantly, killed entries
with clear reasons are often stronger signal than ratified principles — they push against model
defaults rather than confirming them. A corpus that only ratifies what a model already tends toward
isn't accumulating judgment; it's laundering model defaults with provenance. The killed list is
what keeps that honest.

---

## What changes

### 1. Corpora are domain-scoped, not role-scoped

A corpus covers a subject matter, context type, or decision class — not a job title. This applies
at both layers:

- **Repo (seed) corpora** — general judgment organized by domain, not by which role "owns" it
- **Project corpora** — accumulated project judgment organized by domain, not by role

Multiple roles can draw from the same corpus. Shared judgment lives once. Domain boundaries are
discovered from corpus tension (the existing fork signal in the retrospective), never declared
upfront from how a team would be organized.

This is a reorganization of the corpus layer only. The principle schema, ratify gate, working/audit
file split, and write-back format are unchanged.

### 2. Roles become thin consumers of corpora

A role is a domain prompt (the lens the agent applies) plus a declared set of corpora to load.
Roles do not own corpora. The orchestrator assembles the right corpora for each invocation; the
role supplies the mode of reasoning to apply to them.

Role isolation — spawning designers into fresh contexts to prevent transcript bleed — is unchanged.
That is a context contamination mechanism, not a corpus organization mechanism. The seam stays;
what changes is that the seam no longer determines where judgment lives.

### 3. The orchestrator becomes a judgment router

The orchestrator's job is corpus assembly: given a task, which domains are relevant, and which
role's lens applies? This is already close to what the orchestrator does — its existing corpus
encodes judgment about when and how to route. Making it explicit lets that corpus grow in the right
direction rather than being constrained by role identity.

The trust problem this creates (an agent selecting its own constraints) is partially load-bearing
at write time: only ratified principles are injectable, and ratification requires human sign-off.
The assembly call is less fraught when what it assembles from has already been vetted.

### 4. Killed entries get stable ids

Killed entries gain an `id` field, consistent with ratified principles. This makes them:

- Referenceable via `see-also` from ratified or other killed entries
- Queryable at ratify time — a new proposal that resembles a killed entry surfaces the kill reason
  for operator review before ratification proceeds
- Traceable if the same judgment recurs across sessions or projects

The killed list remains in the working file and continues to be injected at runtime alongside
ratified principles. The id is additive — no other schema changes to killed entries.

---

## What stays the same

- The principle schema (`id / rule / condition / reason / status / see-also`)
- The ratify gate (propose → ratify → write-back, human sign-off required)
- The working/audit file split (provenance in the audit file, not loaded at runtime)
- Role isolation (designers spawn into fresh contexts)
- The retrospective and its three signals
- The kernel lifecycle (spawn, accumulate, fork, converge)
- Killed entries injected at runtime as active guidance

---

## Open questions

**Corpus assembly trust.** The orchestrator selecting which corpora to inject is an agent making a
retrieval call with some stake in the outcome. The ratify gate provides the primary control, but
the assembly mechanism itself — how the orchestrator decides what's relevant — needs a design.
Options range from full injection of all active corpora, to semantic retrieval, to a lightweight
separate routing call. Not resolved here.

**UI/UX role boundary.** The current split was assumed from convention, not discovered from corpus
tension. Whether this becomes one designer role consuming different corpus sets by task, or remains
two roles with reorganized corpora, should be decided after the corpus reorganization makes the
actual seams visible.

**Corpus proliferation and context budget.** Domain-scoped corpora could grow unbounded. What
bounds the number of active corpora per invocation, and how context budget is allocated across
them, is an implementation decision not resolved here.