# Domain: color (web-frontend pack)

Palette and hue judgment. Declared by the **ui-designer** lens. Audit metadata lives in
`packs/web-frontend/domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: 2026-06-20

principles:

- id: color-palette-inspiration
  rule: "When a color reference or taste palette informs a design direction, extract what it embodies — hue relationships, saturation register, warmth or coolness, depth contrast — rather than sourcing values from it directly."
  condition: "When making a color decision where a reference palette or taste example has been provided. Does not apply when selecting an existing project token by name."
  reason: "A palette submitted as a taste example encodes relationships and sensibilities, not prescriptions. Pulling hex values directly overfits — the example encodes what worked in that context, not a color system."

- id: palette-chromatic-depth
  rule: "Ensure the color system has at least 3–4 distinct hues available for semantic roles. Each hue should occupy its own corner of the wheel at controlled saturation — no two semantic colors should be close enough in hue to be confused. Avoid single-accent-on-monochrome schemes."
  condition: "Any UI with more than two distinct semantic roles (interaction, reference, state feedback, etc.)."
  reason: "A binary palette (background + one accent) flattens hierarchy — everything that isn't the accent reads as the same undifferentiated surface. Chromatic variety at low saturation lets each element carry meaning through color relationships rather than relying solely on light/dark contrast."

- id: semantic-tokens-required-for-theme-switching
  rule: "Any color token system that must support dark mode or theme switching needs at least two tiers: a primitive tier (raw values, e.g. `--color-blue-500: oklch(...)`) and a semantic tier (role-named aliases, e.g. `--color-action-primary: var(--color-blue-500)`). Theme switching redefines only semantic token values. Components reference only semantic tokens."
  condition: "When building or refactoring a token system where the same component must display correctly across two or more color themes (light/dark, brand variants)."
  reason: "If components reference primitive tokens directly, switching themes requires updating every component that uses any color. A semantic layer decouples 'what role does this color serve?' from 'what is the value for that role in this theme?' — theme switching becomes a single redefinition of the semantic tier, with no component changes needed."
  see-also: semantic-token-names-by-role-not-value

- id: semantic-token-names-by-role-not-value
  rule: "Semantic token names must describe the color's role or purpose, never its visual appearance. Use `--color-text-danger`, `--color-surface-interactive`, `--color-border-subtle` — never `--color-red-text`, `--color-light-gray-bg`."
  condition: "When naming any token in the semantic tier of a design token system — tokens that map a purpose to a value, as opposed to primitive tokens that simply name a raw value."
  reason: "A name like `--color-red-text` encodes both the role and the current value. If the brand's danger color changes from red to orange, every reference to the token is now semantically wrong — the name claims 'red' but it isn't. A role-based name like `--color-text-danger` remains correct regardless of what value it maps to. Role names also survive dark-mode redefinition: the purpose is stable; only the value changes."
  see-also: semantic-tokens-required-for-theme-switching

killed:
```
