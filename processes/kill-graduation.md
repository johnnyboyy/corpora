---
name: corpora:kill-graduation
description: The command sequence for retiring an old killed entry — listing graduation candidates whose rejected idea has stopped recurring, then demoting one out of a domain's working-file kill log. The kernel holds why a kill's guidance value decays; the judgment of whether a specific kill is safe to retire is the retrospective's.
---

# Kill graduation

The step-by-step operations for graduating a killed entry — removing it from a domain working
file's `killed:` log once it is no longer live guidance. Why a kill's value decays (it stops the
same rejected idea from being re-proposed; once nobody comes near re-proposing it, its continued
presence is a permanent reader-tax) lives in `kernel.md`, "Killed entries"; this file is the
*sequence*. Recording a *new* kill is a different operation, in `processes/ratify-write-back.md`.

**Invoked from:** `processes/retrospective.md` (the retrospective judges each candidate;
`domains/retrospective.md`'s `kill-graduation-judged-not-assumed` is the judgment).

## List graduation candidates

```
corpus.py kill-report --domains-dir <dir> --audit <audit-file>
```

Lists, per domain, two things:

- every killed entry with **no recorded `killed:` date** — a bookkeeping gap to fix (the date is
  required and is what enables graduation), not itself a graduation candidate.
- every killed entry **old enough** to be a graduation candidate (default 90 days; `--min-age-days`
  to override).

Age is a necessary precondition, not sufficient evidence. The retrospective still judges whether
anything resembling the killed idea has actually resurfaced before demoting it — see
`domains/retrospective.md`, `kill-graduation-judged-not-assumed`.

## Graduate a candidate

Once the retrospective judges a candidate safe to retire:

```
corpus.py graduate-kill --domains-dir <dir> --audit <audit-file> --domain <domain> --id <id>
```

Does the mechanical part: removes the entry from the working file's `killed:` log and stamps
`graduated: <date>` on its audit-file record.

## Which domains-dir

Both commands work on any `domains-dir` + `audit.md` pair — a project's `corpora/domains/` or this
skill's own `domains/` — since retrospective consolidation happens in this skill repo's own domain
pool too, not only in downstream projects. Pass the pair explicitly (these commands operate on a
`--domains-dir`/`--audit` override not tied to any one file, so `--for-file` does not apply).
