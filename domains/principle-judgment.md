---
subject: process
posture: guardrail
units-of-work: [ratify]
universal: false
---

# Domain: principle-judgment

Judgment about whether a principle — proposed or already ratified — actually encodes earned
judgment, and whether it lives in the domain its real consumer needs it in. Distinct from
`ratify-gate`'s judgment about assembling and processing a spawn, and from `orchestrator-routing`'s
judgment about which composition to invoke: this is about the corpus's own content, at the moment a
proposal is judged and again, periodically, after ratification, since gate-time discipline can
lapse under session-context pressure and a principle ratified in error otherwise sits unexamined
indefinitely. Seeded 2026-07-22 from the criteria used in a full-corpus domain-and-principle audit
this session — see `LINEAGE.md` for the audit's own findings; this domain generalizes the method,
not the specific findings. Audit metadata lives in `domains/audit.md`, loaded only at
ratify/retrospective time.

The judgment below applies the same way regardless of who proposed the candidate — a spawn's
output, a mined transcript, an import, or the operator stating a rule they already hold directly.
Operator-direct authorship is a sanctioned entry point, not a bypass of this domain's tests
(`kernel.md`, "The ratify gate") — the fork test and knowledge-vs-judgment distinction below still
apply to an operator-authored candidate the same as any other.

```yaml
last-retrospective: 2026-07-30

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
  rule: "When a source documents a coherent, ordered workflow rather than independent decision points, don't atomize each step into a standalone principle. Extract only the mechanism-level gotchas that fire independent of the workflow's sequencing and ratify those as ordinary principles. Leave the sequencing itself unencoded — never force it into disconnected `rule`/`condition`/`reason` atoms."
  condition: "Mining a structured source (a skill file, tutorial, or runbook) for principle candidates, when several extracted candidates only make sense relative to each other in a fixed order."
  reason: "The principle schema asks 'does this decision recur under this condition' — it presupposes the content is a judgment call. A workflow isn't a judgment call at all, recurring or otherwise; its value is procedural, and an individual step is not worth stating in isolation the way a decision point is. Steps may contain principles, but steps are not principles in their own right; corpora has nowhere else to put the sequencing itself, so it stays unencoded rather than forced into atoms that misrepresent it."

- id: cost-of-discovery-is-not-judgment-evidence
  rule: "Do not treat how difficult, costly, or recent an insight was to acquire, or how many times its underlying problem has recurred, as evidence that the insight itself clears the judgment-call bar. A fact can be expensive to discover and still just be a fact."
  condition: "When a candidate principle's stated justification for ratification centers on the pain, time, or repetition involved in finding the underlying fix, rather than on a decision that recurs under a describable condition."
  reason: "Effort and repetition measure the cost of learning something, not whether what was learned is a repeatable decision under uncertainty. Every fix that resolves a real bug was effortful by definition — if cost-of-discovery alone justified ratification, every settled fact would qualify, and the corpus would fill with facts that already expired the moment their specific case stopped existing. The bar has to be whether the insight recurs, not what it cost to reach."

- id: strip-specifics-to-find-the-transferable-method
  rule: "When a candidate principle traces to a specific hard-won fix, restate its rule with the case's specific facts — names, files, exact values, the particular symptom — removed, and judge what's left. If nothing recurs-under-uncertainty remains, the candidate is knowledge and expires with the fix; do not ratify it. If a transferable diagnostic method, ordering-of-suspicion, or heuristic remains, ratify that method in place of the original fact."
  condition: "When judging a principle proposal whose provenance traces to a specific bug fix, debugging session, or incident, rather than a general project or design decision."
  reason: "The specific fact a fix resolves — which wire, which line, which config value — was never a judgment call; only how the fix was found might have been. Stripping the instance-level detail is the fastest way to separate the two: what remains is either nothing, meaning the case was pure knowledge dressed up by how hard it was to find, or a reusable method for the next unprecedented case in this domain, which is the actual judgment worth keeping."
  see-also: cost-of-discovery-is-not-judgment-evidence

- id: argument-density-precedes-full-read
  rule: "Before spending a full read on a candidate source, require it to make a specific, reasoned claim with a because — not merely be on-topic. A single sentence that argues a position with a reason qualifies; a listicle or a topic-matching summary with no argued claim does not."
  condition: "When filtering candidate sources (articles, posts, documentation) before reading them in full for principle extraction — a precondition check, prior to the genuine-judgment test that applies once a claim is actually extracted from a source that passed."
  reason: "Topic match alone screens for subject relevance, not for whether the source contains anything that could become a rule/condition/reason — reading a source in full is the expensive step, so the density check belongs before it, not after. A source can pass this and still fail the fork test once actually read; this filter only prevents spending the read on material that structurally cannot contain a claim worth extracting."

- id: mining-signal-precision-ranking
  rule: "When mining a session transcript for judgment that was exercised but never proposed, weight signals by precision, highest first: an operator correction (the operator overrides, redirects, or rewords a spawn's output) is the strongest evidence judgment was actually exercised; a retry chain (the same intent re-asked after an unsatisfying first pass, with the delta between attempts as the candidate's condition) is next; a revert (with why it was backed out as the candidate's reason) is next; an ungated inline tradeoff articulated but never brought to a ratify gate is the weakest and most inference-dependent signal. For any hit, reconstruct what was attempted, what marked it wrong, and what generalizes — emit nothing if nothing generalizes."
  condition: "Mining a transcript (a session, a chat log, any recorded working session) for candidate judgment not captured through the normal handoff/ratify-gate path."
  reason: "A transcript records what happened, not what should be extracted from it — signal precision matters because a correction is direct evidence the operator weighed and rejected something, while an ungated tradeoff is only the spawn's own account of its reasoning, with no external check that it was actually load-bearing. Ranking by precision keeps a mining pass from over-crediting weak signals just because they're more numerous — ungated tradeoffs are the most common shape in any transcript, and the least reliable."

- id: container-kill-hit-is-a-rehoming-candidate-not-a-rejection
  rule: "When a mined or newly-proposed candidate matches an existing killed entry, check the kill's kill_type before treating the match as settled. A quality kill means the match is already rejected — skip it, or surface it only if the transcript/new context shows the kill's reason_killed actually failing in practice. A container kill means the content was sound but filed wrong — surface the new candidate as a re-homing opportunity, not a duplicate to discard."
  condition: "Deduping a candidate (from any source — reading pipeline, session harvest, a fresh proposal) against a domain's killed: log."
  reason: "kill_type: container exists specifically to distinguish 'this was wrong' from 'this was right but misplaced' — collapsing both into a single dedupe check that always skips a match throws away the container case's whole point, which is that the same content deserves a second look at the right home, not permanent suppression."

killed:
```
