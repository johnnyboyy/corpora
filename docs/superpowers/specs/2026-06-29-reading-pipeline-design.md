# Reading Pipeline Design

**Date:** 2026-06-29

A two-stage autonomous pipeline that accumulates principle candidates from external sources into
the corpora skill repo, feeding the existing ratify gate.

---

## Data flow

```
reading/config.md (feeds, author list)
corpus domain files (gap derivation)
        ↓
  discovery agent (Fridays 8 AM PST)
        ↓ quality filter
  reading/queue.md
        ↓ (triggered by new entries, weeknights 2 AM PST)
  reading agent → lens + declared domains, fresh context
        ↓
  reading/candidates.md
        ↓
  ratify gate (surfaced alongside session proposals)
```

---

## File structure

```
reading/
  config.md        # feeds, author list (manually tuned)
  queue.md         # sources queued by discovery, not yet read
  candidates.md    # extracted candidates, awaiting ratify gate
```

`config.md` is the only file edited directly. `queue.md` and `candidates.md` are written by agents.

`config.md` ships pre-populated with: TL;DR, Bytes, Hacker News as feeds; Crockford and Henney
as the starting author list (noted as stale-prone). The Shevlin use-encapsulation piece and the
export-default article seed `queue.md` as the first entries.

---

## Discovery agent

Runs Fridays at 8 AM PST. Inputs: `reading/config.md` and current domain working files.

Gap derivation reads domain files for thin areas (few principles, narrow conditions) and
contested kills (rejected without resolution). Produces 3–5 search queries per run, checked
against configured feeds and web search.

**Quality filter — both must pass:**
1. Topic match — addresses a gap in current domains
2. Argument density — makes a specific, reasoned claim (a tweet qualifies; a listicle doesn't)

Author list entries bypass topic-match and go straight to argument-density check. One citation
hop from a listed author gets the same treatment.

Each entry written to `queue.md` includes: source URL or reference, domain tag(s), gap addressed.

---

## Reading agent

Triggered when discovery adds entries to `queue.md`. Runs one source at a time in a fresh
context — no shared state with the discovery agent or prior reading runs.

Loads the lens declared for the tagged domain(s), fetches the source, reads through that lens.
Extracted candidates are written to `reading/candidates.md` in the standard principle schema
(`rule`, `condition`, `reason`) with `provenance` noting the source URL and gap addressed.

If the source yields nothing principled, the entry is marked read in `queue.md` with a note;
no candidate is written.

Text sources only. Screenshots and visual-only sources are not supported — the designer lenses
reason through written argument.

---

## Ratify gate integration

No change to the existing ratify gate flow. The orchestrator gains one addition: before
presenting session proposals, it checks `reading/candidates.md` for entries whose domain tags
match the current project's declared domains and surfaces them alongside session proposals.

Candidates are marked with their source so they're distinguishable from work-earned proposals.
They go through the same ratify/kill decision. On ratification, the candidate enters the project
domain file with its original provenance intact. On kill, it moves to the kill log. Either way,
it is removed from `reading/candidates.md`.

---

## Tuning

`reading/config.md` is the tuning interface for feeds and author list. The author list is
acknowledged as stale-prone — the primary discovery signal is gap derivation from the corpus,
which self-updates as principles are ratified. Updating the corpus tunes discovery; the author
list needs periodic manual attention.
