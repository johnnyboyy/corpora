# Domain: visual-hierarchy (web-frontend pack)

Emphasis, grouping, and legibility weight. Declared by the **ui-designer** lens. Provenance and
per-kill audit detail live in `packs/web-frontend/domains/audit.md`, loaded only at
ratify/retrospective time. See `kernel.md`, "Storage: working vs audit."

```yaml
last-retrospective: 2026-06-20

principles:

- id: hierarchy-through-scarcity
  rule: "Emphasis signals — differentiation, color, elevation — apply to one dominant element per section; using them on more than one or two cancels the effect. Subordinating non-dominant elements means withholding emphasis, not reducing legibility — informational elements remain fully readable."
  condition: "When composing any screen or section layout and deciding which elements receive visual weight through color, size, differentiation, or elevation."
  reason: "Hierarchy comes from elevating one element, not degrading the others. Dimming non-dominant elements destroys their communicative function without improving the dominant signal."
  status: ratified

- id: control-grouping-encodes-unity
  rule: "Visual grouping of controls — capsule, joined buttons, bordered cluster — signals that all segments operate on the same value or target (e.g. −/0/+ on a count, or 1/2/3 as states of a single selection). Apply a grouped form only when that relationship holds; keep controls visually separate when they are distinct actions, even if related or adjacent."
  condition: "Any interactive control group — steppers, toggles, segmented selectors, button rows."
  reason: "The shape of a control should encode the relationship of its options to each other. Visual grouping communicates 'these are all aspects of one thing.' Joining distinct actions into a group for visual tidiness creates false affordance."
  status: ratified

- id: redundant-badge-sublabel
  rule: "When a badge already communicates status, no sub-label repeating that status is needed. Badge alone."
  condition: "When a list item has both a badge and explanatory text that say the same thing."
  reason: "Redundancy adds visual weight without adding information."
  status: ratified

- id: responsive-text-by-viewport-distance
  rule: "Apply responsive text size bumps independently of density decisions. Mobile-primary density (airy spacing) does not imply mobile-primary text sizes — desktop users read at ~2x the viewing distance and need one size step up on any text that carries legibility weight."
  condition: "Any page with small text elements that carry data or instruction weight. Apply regardless of whether the project is mobile-primary or desktop-primary."
  reason: "Mobile density and mobile text size are independent concerns. Density governs spacing and touch-target sizing. Viewport distance governs text legibility."
  status: ratified

killed:
```
