# UI Designer audit record (web-frontend pack)

Provenance and promotions for `ui-designer.md`. Loaded only at ratify/retrospective time — never
in the UI designer's working context. Keyed by principle `id`. See `kernel.md`, "Storage: working
vs audit." (The kill log lives in `ui-designer.md` so it is available in the working context.)

```yaml
provenance:

- id: one-highlight-per-result-set
  provenance: "2026-06-13, load calculator full visual audit."

- id: color-palette-inspiration
  provenance: "2026-06-02, operator-provided. Clarified 2026-06-13."

- id: accent-color-for-distinction-not-data
  provenance: "2026-06-02, Box Selector visual spec."

- id: warning-colocated-with-resolution
  provenance: "2026-06-02, Box Selector visual spec."

- id: redundant-badge-sublabel
  provenance: "2026-06-02, Box Selector visual spec."

- id: palette-chromatic-depth
  provenance: "2026-06-03, taste training session."

- id: control-grouping-encodes-unity
  provenance: "2026-06-03, taste training session (originally as capsule-encodes-same-value)."
  history:
    - date: 2026-06-20
      type: generalized
      reason: "Original rule prescribed capsule as the specific pattern — 'join into a capsule when segments share a value.' This directed the designer to a single implementation rather than stating the underlying principle. The insight is that any form of visual grouping (capsule, joined buttons, bordered cluster) encodes semantic unity; the specific form is a design decision the rule should inform, not resolve. Rule rewritten to state the general principle with capsule as one named example. Id renamed from capsule-encodes-same-value to reflect the broader concept."

- id: hierarchy-through-scarcity
  provenance: "2026-06-04, retrospective consolidation."

- id: motion-as-accent
  provenance: "2026-06-03, taste training session."

- id: responsive-text-by-viewport-distance
  provenance: "2026-06-09, Box Selector desktop text legibility audit."

- id: document-visual-sub-systems
  provenance: "2026-06-12, full site visual audit."

- id: disclosure-panel-vs-modal
  provenance: "2026-06-14, load calculator history panel design spec."

- id: dark-floating-surface-fill
  provenance: "2026-06-19, nav background depth session."

- id: scroll-fade-gradient-surface-match
  provenance: "2026-06-19, nav background depth session."

promoted:
```
