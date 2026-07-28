# Domain: principle-judgment

Judgment about whether a principle — proposed or already ratified — actually encodes earned
judgment, and whether it lives in the domain its real consumer needs it in. Distinct from
`ratify-gate`'s judgment about assembling and processing a spawn: this is about the corpus's own
content, at the moment a proposal is judged and again, periodically, after ratification, since
gate-time discipline can lapse under session-context pressure and a principle ratified in error
otherwise sits unexamined indefinitely. One of corpora's two standing domains, alongside
`ratify-gate` — corpora's process/timing judgment (which composition to invoke, when to spawn vs.
surface vs. defer) is not a domain here at all; it lived in `orchestrator-routing` until that
domain was retired 2026-07-28 and its judgment moved to praxis, the process driver whenever it's
installed (`LINEAGE.md`, "Corpora stops being an active orchestrator"). Seeded 2026-07-22 from the
criteria used in a full-corpus domain-and-principle audit this session — see `LINEAGE.md` for the
audit's own findings; this domain generalizes the method, not the specific findings. Audit metadata
lives in `domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: none

principles:

- id: reaudit-ratified-principles-against-genuine-fork-test
  rule: "Periodically re-apply the genuine-fork test (`kernel.md`) and the knowledge/judgment distinction to already-ratified principles, not only to new proposals at the gate. A principle's own audit provenance already recording `kind: knowledge` at ratification time is a lapsed-gate signal in itself, not evidence the principle is fine — it means the check existed and was bypassed, not that it never applied."
  condition: "During any retrospective or dedicated principle audit, for every active (non-killed) principle in the domains under review — not only principles flagged by some other signal first."
  reason: "A principle's own audit provenance recording `kind: knowledge` at ratification time means the check existed and was bypassed at the moment it mattered most — nothing about the passage of time since then makes that judgment more reliable. Assuming ratification-time discipline is sufficient on its own, with no periodic re-check, treats a single gate pass as infallible when the gate is exactly the thing shown capable of lapsing under session-context pressure."

- id: reading-pipeline-provenance-flags-knowledge-risk
  rule: "When a principle's provenance cites a reading-pipeline source (an article, documentation, a training-data-adjacent secondary source) rather than an earned project mistake or an observed session correction, weight the knowledge-vs-judgment question harder before treating its `kind` as settled — a rule 'surfaced from reading pipeline' is more likely to be derivable doctrine than earned judgment, even when it was ratified as `kind: judgment`."
  condition: "When auditing or ratifying a principle whose provenance names a reading-pipeline source or secondary documentation rather than a specific incident, task, or operator correction."
  reason: "A reading-pipeline source is selected and written to explain or persuade, not to record a mistake actually made — so its claims arrive pre-packaged as generally-applicable doctrine regardless of whether they encode a real decision under uncertainty. That framing is easy to mistake for earned judgment precisely because it reads as confident and well-argued; the correlation between source type and knowledge-not-judgment risk is worth checking explicitly rather than assuming the `kind` tag alone settles it."

- id: check-principle-against-consuming-lens-not-just-domain-topic
  rule: "When auditing a domain's principles, check each one against which composition actually needs and applies it — not only whether it plausibly fits the domain's stated topic. A principle can read as on-topic for its domain while actually encoding a different composition's job entirely (e.g., framework-specific implementation mechanics sitting in a design domain no convergent implementation composition ever loads)."
  condition: "During a principle audit or retrospective, for any domain loaded by more than one composition, or whose principles reference an implementation-specific mechanism (a named library, hook, framework API, or file format)."
  reason: "`kernel.md`'s domain-tension retrospective signal only catches principles that give *opposing* advice under partitioned conditions — it structurally cannot see a principle that is simply misplaced without contradicting anything else in its domain. A principle can read as topically on-theme while actually encoding a different composition's job entirely, and no amount of re-reading it against its own domain's stated subject will surface that, because the mismatch isn't a contradiction — it's a mismatch between what the content is and who would ever load it."

- id: lead-with-the-nonobvious-half-when-refining
  rule: "When a principle survives the genuine-judgment test overall but its stated rule foregrounds a well-known default alongside a genuinely earned, non-obvious insight, restructure the rule and reason to lead with the non-obvious part. The familiar half becomes a corollary, not the headline."
  condition: "When refining (not killing) a principle whose `rule` bundles common-knowledge framing ahead of its actually-earned insight."
  reason: "A principle that leads with a well-known default and buries its actually-earned insight as an afterthought reads as mostly-obvious on its face — inviting it to be flagged, or silently discounted, on every future audit even when it has a real kernel worth keeping. Restructuring to foreground the earned half fixes that audit signal without losing the corollary; the familiar half is still true, it's just not the reason the principle is worth keeping."

- id: consuming-lens-includes-agent-vs-human-gap
  rule: "When judging whether a candidate clears the genuine-judgment bar, check whether the mistake it guards against is one the system's actual consumer — an AI agent — would make, not one a human developer would make from habit or forgetfulness. A reason citing framework muscle-memory, habit-transfer from a prior stack, or 'just remember to do X' framing is a human-consumer signal, not evidence of agent-relevant risk."
  condition: "Ratifying or auditing any principle, especially one mined from documentation or a skill file, whose `reason` describes a lapse of memory or a carried-over habit rather than a mechanism that fails silently or produces a hard-to-attribute symptom."
  reason: "A habit-transfer or 'remember to' framing describes a lapse specific to human working memory and cross-project carryover — an agent reads the current project's actual state fresh each time rather than accumulating carried-over habits, so a principle guarding against that lapse changes nothing about agent behavior even when ratified. This is `check-principle-against-consuming-lens-not-just-domain-topic` applied prospectively at ratify time, to the specific case of the audience itself, not only retrospectively once a domain is already populated."
  see-also: check-principle-against-consuming-lens-not-just-domain-topic

- id: mined-workflow-stays-a-workflow
  rule: "When a source documents a coherent, ordered workflow rather than independent decision points, don't atomize each step into a standalone principle. Extract only the mechanism-level gotchas that fire independent of the workflow's sequencing and ratify those as ordinary principles. Route the sequencing itself to praxis, if the project runs it, as a phase or phase pool — never force it into disconnected `rule`/`condition`/`reason` atoms, and never discard it outright now that it has a home."
  condition: "Mining a structured source (a skill file, tutorial, or runbook) for principle candidates, when several extracted candidates only make sense relative to each other in a fixed order."
  reason: "The principle schema asks 'does this decision recur under this condition' — it presupposes the content is a judgment call. A workflow isn't a judgment call at all, recurring or otherwise; its value is procedural, and an individual step is not worth stating in isolation the way a decision point is. Steps may contain principles, but steps are not principles in their own right. Originally this meant leaving the sequencing unencoded — corpora had nowhere else to put it. Praxis now exists as the peer skill for exactly this content (`praxis/kernel.md`, \"What praxis is\"), so 'unencoded' is no longer the correct default: a real workflow found in a mined source is praxis's phase-discovery input, not corpora's to drop. A project not running praxis still drops it, since corpora alone has nowhere to route it."

- id: cost-of-discovery-is-not-judgment-evidence
  rule: "Do not treat how difficult, costly, or recent an insight was to acquire, or how many times its underlying problem has recurred, as evidence that the insight itself clears the judgment-call bar. A fact can be expensive to discover and still just be a fact."
  condition: "When a candidate principle's stated justification for ratification centers on the pain, time, or repetition involved in finding the underlying fix, rather than on a decision that recurs under a describable condition."
  reason: "Effort and repetition measure the cost of learning something, not whether what was learned is a repeatable decision under uncertainty. Every fix that resolves a real bug was effortful by definition — if cost-of-discovery alone justified ratification, every settled fact would qualify, and the corpus would fill with facts that already expired the moment their specific case stopped existing. The bar has to be whether the insight recurs, not what it cost to reach."

- id: strip-specifics-to-find-the-transferable-method
  rule: "When a candidate principle traces to a specific hard-won fix, restate its rule with the case's specific facts — names, files, exact values, the particular symptom — removed, and judge what's left. If nothing recurs-under-uncertainty remains, the candidate is knowledge and expires with the fix; do not ratify it. If a transferable diagnostic method, ordering-of-suspicion, or heuristic remains, ratify that method in place of the original fact."
  condition: "When judging a principle proposal whose provenance traces to a specific bug fix, debugging session, or incident, rather than a general project or design decision."
  reason: "The specific fact a fix resolves — which wire, which line, which config value — was never a judgment call; only how the fix was found might have been. Stripping the instance-level detail is the fastest way to separate the two: what remains is either nothing, meaning the case was pure knowledge dressed up by how hard it was to find, or a reusable method for the next unprecedented case in this domain, which is the actual judgment worth keeping."
  see-also: cost-of-discovery-is-not-judgment-evidence

killed:
```
