---
name: corpora:retrospective
description: The periodic, backward-looking counterpart to per-task routing — reads a domain's accumulated corpus and gate history for fork, convergence, drift, promotion, condensation, and kill-graduation signals. Suggested by mechanical triggers, run on operator command (retrospective <domain>), never automatic.
---

# Retrospective

**Trigger:** on operator command, `retrospective <domain>` (or `retrospective <composition-name>`,
covering every domain that composition loads). `record-gate` prints fired triggers automatically
at every ratify gate (or run `corpus.py triggers`) as a suggestion only — since the last
retrospective, `ratified ≥ 6`, or `working-file-tokens` grew by ≥ 50%, or `gate-violations ≥ 3`.
Thresholds are operator-tunable and deliberately coarse: the trigger replaces "am I watching
carefully enough," not the retrospective's own judgment. These are *triggers, not caps* —
accumulation is the point; the bet is that meta-principles condense out of accumulated specific
ones, and a fired trigger means "there is enough new material that condensation is worth
attempting."

**Composition:** convergent stance. This is an **audit-mode load**, not a composed spawn's working
load (`kernel.md`, "Two load modes") — load the full working file plus `domains/audit.md` for every
domain under review, and `domains/retrospective.md` (this domain's own judgment for reading what
the history means) unconditionally, the same way `orchestrator-routing`/`ratify-gate`/
`principle-judgment` load unconditionally rather than through `scripts/corpus.py select`.

---

## Procedure

1. For each domain under review, read its working file's `last-retrospective:` date, its
   `principles:` and `killed:` entries, and its `domains/audit.md` counters, efficacy, and
   co-occurrence blocks.
2. Apply `domains/retrospective.md`'s principles to what you read — contamination, domain-tension
   splits, convergence, composition drift, complementary-principle abstraction candidates,
   structural kinship, anti-overfitting, efficacy interpretation, and co-firing. Every signal that
   fires is a **proposal to the operator**, never automatic — advisory only, same as any other
   proposal at the ratify gate.
3. **Kill graduation, as its own pass:** run it per `processes/kill-graduation.md` — list the
   candidates (`kill-report`), judge each per `domains/retrospective.md`'s
   `kill-graduation-judged-not-assumed`, then demote the safe ones (`graduate-kill`). That file has
   the commands and which `domains-dir`/`audit` pair to pass.
4. Present every signal and every graduation judgment to the operator: ratify, reject, or edit,
   same as any proposal.
5. **If a domain-tension split is approved:** this is the one signal whose execution is not
   mechanical. Working with the operator, decide the new domain names and boundaries (see
   `domains/audit.md`, "The coding-ts / coding-react split," for the shape of a real precedent —
   `coding-js-react` split into a TS/JS-general domain, a React-specific domain, and had its
   stack-agnostic remainder land in `coding-general`). Create the new working file(s), move each
   affected principle to its new home, and add a `history:` entry (`type: moved` or `type: split`)
   to that principle's audit-file record (`processes/ratify-write-back.md`, "Reshape a ratified
   principle"; the `history:` schema is `kernel.md`, "Write-back format"). There is no `corpus.py`
   command for this step — it stays a live conversation deliberately, the same way domain assignment
   at the ratify gate is the one point in that procedure requiring judgment rather than a script.
6. When the retrospective completes, run `corpus.py retro-done --domain <d>` (resets counters,
   re-baselines tokens) for each domain reviewed; after a UI-library sync specifically,
   `corpus.py sync-done`.
