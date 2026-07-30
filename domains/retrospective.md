---
subject: process
posture: guardrail
units-of-work: [retrospect]
universal: false
---

# Domain: retrospective

Judgment about reading a domain's accumulated corpus and gate history for what it's telling you —
which signal is real, which is noise, and what to propose from it. Distinct from `principle-judgment`
(whether one proposed or ratified principle is genuine, and lives in the right domain) and from
`ratify-gate`/`orchestrator-routing` (assembling and routing a single spawn): this domain's
principles apply at the retrospective's periodic, backward-looking pass across a domain's history,
not at any single spawn's forward-looking gate. Loaded explicitly by `retrospective.md`'s own
procedure as part of the audit-mode bundle (the domains under review, plus `domains/audit.md`) —
not selected via `scripts/corpus.py select` the way a composed spawn's working domains are, the
same way `orchestrator-routing`/`ratify-gate`/`principle-judgment` are loaded unconditionally rather
than composed. Two signals that read as retrospective triggers — a misplaced principle, and a
ratified principle whose gate-time discipline may have lapsed — are already homed in
`principle-judgment` (`check-principle-against-consuming-lens-not-just-domain-topic` and
`reaudit-ratified-principles-against-genuine-fork-test`); they are not duplicated here. Audit
metadata lives in `domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: none

principles:

- id: contamination-detected-fix-routing-or-composition
  rule: "When retrospective review finds attention was spent on a domain outside a task's actual mode during a session, treat it as a routing or composition defect and propose a fix to the routing judgment or the composition rule itself — not a one-off correction to that session's output."
  condition: "During a retrospective, when a composed spawn's actual working attention (visible in its output or a handoff's Surfaced notes) touched a domain its composition did not include, or a domain outside its declared stance."
  reason: "A single contaminated session is a symptom; the routing or composition rule that let it happen is the disease. Fixing only the output leaves the same misrouting free to recur on the next similar task."

- id: domain-tension-partition-signals-split
  rule: "Propose splitting a domain when two ratified principles within it have conditions that partition the same decision space and give opposing advice under their respective conditions — never when they simply address different topics. Advisory only; the operator judges whether the partition is real, and execution of an approved split is a live conversation with the operator about naming and boundaries, not a scripted step (`domains/audit.md`, \"The coding-ts / coding-react split,\" is the precedent to weigh a new one against)."
  condition: "During a retrospective, reviewing a domain's active principles for conditions that repeatedly produce contradictory guidance rather than merely covering different subjects."
  reason: "The seam between two domains is only real once tension is observed, not assumed from how a team would organize the same subject. Two principles on different topics are just different subjects; the partition test is repeated, condition-triggered opposing advice, which is the only evidence a single container has actually become two decision classes."

- id: convergence-signals-explorer-pairing
  rule: "When a domain's principles have stopped changing and corrections have become rare, propose pairing every composition that loads it with an explorer, to prevent the domain calcifying around its current state."
  condition: "During a retrospective, for a domain whose ratify counts and corrections have been low across several recent gates."
  reason: "A domain that never gets corrected is either genuinely settled or has stopped being questioned — the two look identical from counters alone. An explorer reintroduces active challenge before settledness curdles into an unexamined default."

- id: composition-drift-fix-going-forward
  rule: "When a spawn's composed domain-subset consistently excludes a domain the work actually needed, or includes one it never draws from, propose correcting the composition rule itself, not just the affected task."
  condition: "During a retrospective, reading the co-occurrence tally `record-gate` maintains and any handoff `Surfaced` notes naming a gap between what was composed and what the work actually needed."
  reason: "A single spawn missing a relevant domain is a routing accident; a *pattern* of the same domain being consistently excluded or consistently idle for a given unit-of-work is evidence the composition rule itself is wrong, and only a retrospective's aggregated view across sessions can tell the two apart from a one-off."

- id: seed-promotion-candidate
  rule: "Surface a project-domain principle as a seed-promotion candidate when its condition makes no reference to this project's stack, domain, or specifics, and it has held across enough tasks to read as general rather than provisional."
  condition: "During a retrospective, reviewing a project domain's active principles for ones whose condition would bind identically in an unrelated project."
  reason: "A principle earned in one project only proves it generalizes once its condition is stack/project-agnostic and it has survived repeated application — promoting on stack-agnostic wording alone, before it has actually been re-tested, risks promoting a principle that only happened to never hit its edge case yet."
  see-also: single-project-shape-principle-stays-provisional

- id: structural-kinship-condensation-candidate
  rule: "When several active principles state the same underlying test in different words — visible from existing see-also links or from reading a domain's principles side by side rather than sequentially — propose condensing them into one umbrella statement with the specific cases named as instances, rather than leaving the shared test implicit across separate entries."
  condition: "During a retrospective, or when a domain's principle list has grown large enough that side-by-side reading becomes practical."
  reason: "Kinship is visible from the text alone and doesn't need firing history to accumulate first — it can surface a condensation candidate earlier than co-firing would. Leaving the shared test implicit across several worded-differently entries pays a reader tax every session that has to re-derive that they're the same test."
  see-also: co-firing-cluster-signals-meta-principle

- id: kill-graduation-judged-not-assumed
  rule: "When `corpus.py kill-report` surfaces a killed entry old enough with no sign of recurrence, judge specifically whether anything resembling it has actually resurfaced since — not merely whether enough time has passed — before running `graduate-kill` to demote it."
  condition: "During a retrospective, for every `kill-report` candidate in a domain under review."
  reason: "A kill's job is to stop the same rejected idea from being re-proposed; its value decays once nobody has come near re-proposing it, but 'old enough' is a necessary precondition age can measure, not sufficient evidence recurrence has genuinely stopped — that judgment is what the retrospective adds on top of the mechanical age filter."

- id: single-project-shape-principle-stays-provisional
  rule: "Surface which ratified principles were earned in a single project shape and mark them as candidates that should stay provisional — weighable, not promoted — until tested against a second shape. A provisional principle with real `fired` counts under a second project shape has earned its promotion case; one that has only ever fired in its birth project stays provisional."
  condition: "During a retrospective, for any domain whose active principles all trace to one project's provenance."
  reason: "A principle pressure-tested in only one climate is a promotion risk, not a default — the condition it states may happen to hold everywhere in that one project's shape without actually generalizing, and there's no way to tell the difference without a second shape's evidence."
  see-also: seed-promotion-candidate

- id: interpret-efficacy-counts-dont-act-on-them-raw
  rule: "Read idle-dominant efficacy counts across many gates as a retirement candidate or a too-narrowly-scoped condition; read recurring violated counts as either a load-bearing principle (still catching real drift) or a badly-conditioned one — the counts alone cannot distinguish either pair, so treat them as a question the retrospective must answer, never as evidence to act on directly."
  condition: "During a retrospective, reading a domain's efficacy block (fired/violated/idle counts) for any principle."
  reason: "Counts are inputs to judgment, not verdicts — that's why they're recorded at the audit layer instead of consumed automatically. A principle that is idle because nobody needs it and one that is idle because its condition never fires look identical in the counter; a violated principle that's badly conditioned and one that's correctly catching real drift look identical too. Only the retrospective's read of the actual instances can resolve either ambiguity."

- id: co-firing-cluster-signals-meta-principle
  rule: "When a cluster of principles consistently fire together across gates, propose a shared meta-principle, treating the co-firing as the empirical trace of one underlying justification the individual principles only state as separate instances."
  condition: "During a retrospective, reading the co-occurrence/efficacy data for principles that repeatedly fire in the same gates."
  reason: "Co-firing is the empirical, counted trace of the same shared-test pattern `structural-kinship-condensation-candidate` finds from reading the text alone — the two are complementary detection paths for the same underlying condensation opportunity, one needing accumulated firing history first and one visible immediately from the prose."
  see-also: structural-kinship-condensation-candidate

killed:
```
