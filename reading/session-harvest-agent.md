# Session harvest agent

Mines past session transcripts for judgment that was exercised but never proposed — the layer
between what the reading pipeline imports and what the ratify gate captures. Self-contained — no
prior session context needed. Emits into the same `candidates.md` the reading agent uses; rides
the existing gate end to end.

With handoff artifacts in place, most proposals are captured at the source; this agent is the
backfill tool for the pre-handoff era and the safety net for exempted inline sessions. The
harvester finding little is the system working.

---

## Setup

1. Input: a project path and a transcript window (e.g. "sessions from the last 14 days", or
   "all sessions before <date>" for a backfill pass).
2. Claude Code transcripts live under `~/.claude/projects/<munged-project-path>/`, one JSONL
   file per session.
3. Read `reading/harvested.md`. Skip any session already listed — sessions are never re-mined.
4. Read the project's `corpora/config.md` for its shape (language, framework, styling, has-ui).

## For each unharvested session (one at a time, fresh context per session)

### 1. Compose the stance and domains

Determine the session's apparent subject (coding, UX, visual) and compose the matching stance plus
domains — same routing table as the reading agent (`reading-agent.md`, step 1). Reading a
transcript under a stance is what turns "the operator said no" into a candidate with a
`condition`. Load the domains' working files *including their kill logs* — the dedupe check below
depends on them.

### 2. Mine

Scan for four signals, in descending precision:

1. **Operator corrections** — the operator overrides, redirects, or rewords after a spawn's output
   ("no, actually…", an edit reversing the spawn's choice). The correction *is* the judgment; the
   candidate encodes what should have been weighed.
2. **Retry chains** — the same intent re-asked after an unsatisfying first pass. The delta
   between the failed and accepted attempts is the condition under which the first approach
   doesn't work.
3. **Reverts** — a committed change backed out (`git revert`, a manual undo visible in the
   transcript). Why it was backed out is a candidate `reason`.
4. **Ungated decisions** — a principle-shaped tradeoff articulated inline ("we chose X over Y
   because Z") in a session that never reached a ratify gate.

For each hit, reconstruct: what was attempted, what signal marked it wrong, what the corrected
form was, and what generalizes. If nothing generalizes — a one-off mistake, a typo-level fix, a
preference with no reason — emit nothing. Do not force candidates from weak material.

**Dedupe before emitting.** Check the candidate against the loaded domains' active principles and
their kill logs. Already covered → skip. Matches a killed principle → emit only if the transcript
shows the kill's `reason_killed` failing in practice, and say so in `gap`. Exception: `container`
kills are re-homing candidates by definition — surface those for re-filing.

**Cap candidates per session** (default 5, strongest signals first) so a backfill pass never
floods the gate. Run backfills in dated batches; each gate session should see a reviewable amount.

### 3. Emit

Append to `reading/candidates.md` inside the `candidates:` block, existing schema, with
session-shaped provenance:

```yaml
- id: [kebab-case-slug]
  rule: [the judgment, stated as guidance]
  condition: [when it applies — be specific]
  reason: [why — the justification that generalizes]
  domains: [domain names this belongs to]
  provenance:
    source: session:<project>/<session-id>
    signal: correction | retry-chain | revert | ungated-decision
    gap: [what was lost — e.g. "corrected twice, never proposed"]
    extracted: [YYYY-MM-DD]
  see-also: [ids of existing principles this relates to, if any]
```

Candidates encode the *judgment*, never transcript content beyond what `rule`/`condition`/`reason`
require — transcripts can hold secrets and personal context; provenance is a session pointer, not
an excerpt.

### 4. Mark harvested

Append to `reading/harvested.md`:

```yaml
- session: <project>/<session-id>
  harvested: [YYYY-MM-DD]
  candidates: [N]
```

## Commit and push

```bash
git add reading/harvested.md reading/candidates.md
git commit -m "harvest: [project]/[session-id] → [N] candidate(s)"
git push
```

## At the gate

Harvested candidates surface like any reading-pipeline candidate, marked with their source. One
difference the operator should weigh: unlike external reading, these were *earned in this
project's own work* — a ratified one skips the usual "provisional until tested in a second shape"
caution only if it also reads as general.
