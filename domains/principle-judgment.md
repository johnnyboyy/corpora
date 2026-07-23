# Domain: principle-judgment

Judgment about whether a principle — proposed or already ratified — actually encodes earned
judgment, and whether it lives in the domain its real consumer needs it in. Distinct from
`ratify-gate`'s judgment about assembling and processing a spawn, and from `orchestrator-routing`'s
judgment about which lens to invoke: this is about the corpus's own content, at the moment a
proposal is judged and again, periodically, after ratification, since gate-time discipline can
lapse under session-context pressure and a principle ratified in error otherwise sits unexamined
indefinitely. Declared by the **orchestrator** lens, alongside `orchestrator-routing` and
`ratify-gate`. Seeded 2026-07-22 from the criteria used in a full-corpus domain-and-principle audit
this session — see `LINEAGE.md` for the audit's own findings; this domain generalizes the method,
not the specific findings. Audit metadata lives in `domains/audit.md`, loaded only at
ratify/retrospective time.

```yaml
last-retrospective: none

principles:

- id: reaudit-ratified-principles-against-genuine-fork-test
  rule: "Periodically re-apply the genuine-fork test (`kernel.md`) and the knowledge/judgment distinction to already-ratified principles, not only to new proposals at the gate. A principle's own audit provenance already recording `kind: knowledge` at ratification time is a lapsed-gate signal in itself, not evidence the principle is fine — it means the check existed and was bypassed, not that it never applied."
  condition: "During any retrospective or dedicated principle audit, for every active (non-killed) principle in the domains under review — not only principles flagged by some other signal first."
  reason: "Concrete evidence, not a hypothetical: this session's audit found css.md's grid-for-layout-flexbox-for-flow and color.md's semantic-token-names-by-role-not-value both tagged `kind: knowledge` in their own audit provenance at ratification time, yet both were ratified into `principles:` anyway. Assuming ratification-time discipline is sufficient and a retrospective re-check would be redundant is a plausible, tempting shortcut this session's audit directly disproved."

- id: reading-pipeline-provenance-flags-knowledge-risk
  rule: "When a principle's provenance cites a reading-pipeline source (an article, documentation, a training-data-adjacent secondary source) rather than an earned project mistake or an observed session correction, weight the knowledge-vs-judgment question harder before treating its `kind` as settled — a rule 'surfaced from reading pipeline' is more likely to be derivable doctrine than earned judgment, even when it was ratified as `kind: judgment`."
  condition: "When auditing or ratifying a principle whose provenance names a reading-pipeline source or secondary documentation rather than a specific incident, task, or operator correction."
  reason: "Every knowledge-kill from this session's audit (css.md's two, color.md's two) originated from reading-pipeline provenance — a real, non-coincidental correlation between source type and knowledge-not-judgment risk, worth naming directly rather than re-discovering it fresh on every future audit."

- id: check-principle-against-consuming-lens-not-just-domain-topic
  rule: "When auditing a domain's principles, check each one against which lens actually needs and applies it — not only whether it plausibly fits the domain's stated topic. A principle can read as on-topic for its domain while actually encoding a different lens's job entirely (e.g., framework-specific implementation mechanics sitting in a design domain no coder composition ever loads)."
  condition: "During a principle audit or retrospective, for any domain loaded by more than one lens, or whose principles reference an implementation-specific mechanism (a named library, hook, framework API, or file format)."
  reason: "`kernel.md`'s domain-tension retrospective signal only catches principles that give *opposing* advice under partitioned conditions — it structurally cannot see a principle that is simply misplaced without contradicting anything. This session found three such cases (`optimistic-ui-for-high-confidence-mutations` and its pair sitting in `recoverability` though no design alias's notes ever claimed implementation as their concern; `progressive-disclosure-for-primary-advanced-split` sitting in `design-method` though it's a substantive interaction pattern, not a process rule) with zero textual contradiction to trigger the existing signal. This test fills that structural gap: check consumption, not only topical fit."

- id: lead-with-the-nonobvious-half-when-refining
  rule: "When a principle survives the genuine-judgment test overall but its stated rule foregrounds a well-known default alongside a genuinely earned, non-obvious insight, restructure the rule and reason to lead with the non-obvious part. The familiar half becomes a corollary, not the headline."
  condition: "When refining (not killing) a principle whose `rule` bundles common-knowledge framing ahead of its actually-earned insight."
  reason: "`visual-hierarchy.md`'s `hierarchy-through-scarcity` originally led with 'apply emphasis to one dominant element' — design-101, close to textbook knowledge — and buried the actually-earned insight ('subordinating means withholding emphasis, never degrading legibility to fake contrast') as an afterthought. A principle that reads as mostly-obvious on its face keeps getting flagged, or silently discounted, on every future audit even when it has a real kernel worth keeping; restructuring to foreground the earned half fixes the audit signal without losing the corollary."

killed:
```
