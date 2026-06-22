# UX Designer audit record (web-frontend pack)

Provenance and promotions for `ux-designer.md`. Loaded only at ratify/retrospective time — never
in the UX designer's working context. Keyed by principle `id`. See `kernel.md`, "Storage: working
vs audit." (The kill log lives in `ux-designer.md` so it is available in the working context.)

```yaml
provenance:

- id: triage-and-ranking-are-independent-signals
  provenance: "Merged from intake-and-ranking-are-separate-activities + elo-as-independent-ranking-signal, 2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a comparative ranking/evaluation tool (Taste Trainer). Condition is narrow — tools that mix quick triage with deliberate ranking. Plausible general principle but untested against a second project with a ranking or evaluation feature. Do not promote until confirmed in a second context."

- id: category-scope-is-visible-on-ranked-items
  provenance: "2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a per-category ranking tool (Box Selector). Condition presupposes category-scoped rankings — a pattern that may not recur in other web-frontend projects. Do not promote until confirmed in a second context."

- id: choice-prompt-anchors-on-usefulness-not-preference
  provenance: "2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a reference-building tool (Taste Trainer). Condition is narrow — tools whose output is meant to inform future decisions, not record taste. Do not promote until confirmed in a second context."

- id: callout-label-describes-property-not-judgment
  provenance: "2026-06-02, Box Selector UX review."

- id: out-of-order-callout-requires-sort-explanation
  provenance: "2026-06-02, Box Selector UX review."

- id: zero-count-orphan-rows
  provenance: "2026-06-02, Box Selector UX review."

- id: warning-banner-must-locate-its-fix
  provenance: "2026-06-02, Box Selector UX review."

- id: filter-side-effects-are-surfaced
  provenance: "2026-06-02, Box Selector UX review."

- id: scrollytelling-must-always-react
  provenance: "2026-06-13, homepage journey audit."

- id: origin-step-marked-visited-on-navigation
  provenance: "2026-06-14, load-calculator UX audit."

- id: destructive-global-actions-require-confirmation
  provenance: "2026-06-14, load-calculator UX audit."

- id: wizard-output-consistent-regardless-of-path
  provenance: "2026-06-14, load-calculator UX audit."

- id: optional-step-must-be-labeled-optional
  provenance: "2026-06-14, load-calculator UX audit."

- id: numeric-inputs-start-empty-not-zero
  provenance: "2026-06-14, load-calculator UX audit."

- id: recovery-path-replaces-confirmation
  provenance: "2026-06-14, load-calculator audit."
  history:
    - date: 2026-06-20
      type: consolidated
      reason: "Absorbed recoverable-action-surfaces-its-path (originated ui-designer seed 2026-06-14, moved to ux-designer seed 2026-06-20). Both principles shared identical conditions and formed one complete thought: skip confirmation when recovery exists, and surface that recovery path. Separated, a designer could apply one without the other and get incomplete guidance. Merged rule absorbs both: recovery path is the gate AND must be made visible. Merged reason combines both justifications."

- id: unified-field-over-derived-dual-fields
  provenance: "2026-06-14, load-calculator appliance row overhaul."

- id: persistent-controls-not-conditional
  provenance: "2026-06-14, load-calculator appliance row overhaul."

- id: section-level-explanation-not-row-level
  provenance: "2026-06-14, load-calculator appliance row overhaul."

- id: indicator-weight-matches-job
  provenance: "2026-06-16, load calculator history redesign."

- id: active-row-is-inert
  provenance: "2026-06-16, load calculator history redesign."

- id: destructive-inline-confirmation
  provenance: "2026-06-02 (originated in ui-designer seed corpus)."
  history:
    - date: 2026-06-20
      type: moved
      reason: "Principle describes interaction behavior (inline row transformation, confirm/cancel affordance), not visual design. Moved from UI designer seed to UX designer seed."

- id: clarity-over-polish
  provenance: "2026-06-22, extracted from UX designer 'Project context' instruction."

- id: documentation-before-screenshots
  provenance: "2026-06-22, extracted from UX designer 'What you do' screenshots bullet."

promoted:
```
