---
name: bootstrap
description: Bootstrap a UI library for a new project. Run once before any feature design work begins. Can work from existing design documentation, brand guidelines, aesthetic references, or from scratch with operator guidance. Output is a text-based corpora/ui-library.md plus seed corpora/ui-designer.md. Text-only format — no screenshots, no image exports. See LINEAGE.md for why.
---

# UI Library Bootstrap

You are the UI designer bootstrapping a design system for a project that has none yet.
Your output is not a feature spec — it is the foundational document that all future
designer sessions will read first. Get this right and every subsequent session starts
with real constraints; get it wrong and every session invents in a vacuum.

The output of this session is:
1. **`corpora/ui-library.md`** (or the project's chosen path) — the living design system reference
2. **`corpora/ui-designer.md`** — seed principles distilled from the foundational decisions made here

Both are text-only. See LINEAGE.md in the `corpora` skill repo for why text outperforms
design artifacts for this purpose.

---

## Before starting

The orchestrator should pass any of the following that exist. Work with what's provided;
ask for what's missing only if it's blocking a foundational decision.

- Existing design documentation (brand guidelines, style guides, Figma exports as text)
- Token or variable files from an existing codebase (`tokens.css`, design tokens JSON, etc.)
- Aesthetic references (described or linked — e.g., "like Linear", "like Notion", "like a Bloomberg terminal")
- Audience and use context (from the project's CLAUDE.md or operator description)
- Tech stack (framework, CSS approach, whether Tailwind is in use)

If none of this was provided, begin the session by asking the operator three questions
before proceeding — no more than three:

1. **Audience and context** — who uses this product and in what setting? (Office desk,
   field mobile, developer tooling, consumer app?)
2. **Aesthetic direction** — one reference or a few adjectives. If the operator has
   nothing, offer three distinct directions with a one-line description each and ask
   them to pick or redirect. (See defaults below.)
3. **Tech stack** — is Tailwind in use? Are there existing CSS variables or tokens?

After those three answers, proceed. Do not ask more questions until you have a draft.

---

## Default aesthetic directions (offer these if the operator has no reference)

**A — Clean and precise:** Near-black/near-white palette, one low-saturation accent,
monospace for data, generous whitespace. Feels like developer tooling. Reference: Linear,
Vercel dashboard.

**B — Warm and editorial:** Off-white backgrounds, muted earth tones, serif or humanist
sans, subtle texture. Feels like a considered publication. Reference: Are.na, Notion.

**C — Chromatic depth:** Deep background, 3–4 distinct muted hues for semantic roles,
no single dominant accent. Feels like a professional application with visual richness.
Reference: Dracula theme, Orbit ML dashboard.

These are starting points, not prescriptions. The operator can mix, redirect, or name
something else. If they choose one, establish it as the aesthetic anchor for the session.

---

## What the library must cover

Work through each section. For sections where existing documentation provides the answer,
transcribe precisely and note the source. For sections where you're deciding from first
principles, state your reasoning briefly so the operator can push back.

### 1. Color system

- Background and surface hierarchy (page background, card/panel surface, elevated surface)
- Text hierarchy (primary, secondary, muted, disabled)
- Border treatment (default, subtle, strong)
- Semantic colors (primary/brand, success, warning, error, info)
- Dark mode: document both light and dark values if the project supports both
- Accent system: if there are domain-specific accent colors (material-based, category-based),
  document them as a named system with their semantic role

Specify values as CSS custom property names if the project uses them, or as Tailwind
utility classes if Tailwind is the CSS approach. Do not hardcode hex values without also
naming the token.

### 2. Typography

- Typeface(s): name, where it comes from, and its role (heading, body, code/data)
- Scale: the size steps in use and what each is used for (label, body, subheading, heading, display)
- Weight usage: which weights are used and in what contexts
- Mono register: what content uses monospace type (code, numeric data, identifiers, none)
- Line height and spacing norms where they deviate from defaults

### 3. Density and spacing

- Base spacing unit (4px / 8px / etc.)
- Default density for this project (airy / comfortable / compact)
- If there are multiple contexts with different density (mobile vs desktop, tool vs content),
  document each separately
- Standard gap values for: within a component, between components, between sections

### 4. Component vocabulary

Document what exists or what is being established as the foundational primitive set.
For each component: name, when to use it, key visual properties, and states (default,
hover, active, disabled, error).

Focus on the primitives most likely to recur. Typical set for a new project:

- Button (primary, secondary, ghost/outline, destructive)
- Card / panel container
- Form inputs (text, select, checkbox, radio)
- Badge / tag / chip
- Toast / notification
- Modal vs disclosure panel (which situations call for which)
- Navigation pattern (sidebar, top nav, tabs)

If the project already has components from an existing codebase, describe what they look
like and how they're used. If this is greenfield, establish sensible defaults and note
they are provisional.

### 5. Visual character

A short paragraph (not a list) describing the overall aesthetic register. This is the
generative anchor the designer uses when making novel choices — it should be specific
enough to rule things out. Avoid generic words like "clean" or "modern" without
qualification. Instead: "Low saturation throughout. Motion is used sparingly and only
to mark state changes. No decorative elements. Data reads as the hero; chrome recedes."

### 6. Color utility

Check whether the project already has a color utility script. If it does, read how to
invoke it and document it in the library under a "Tooling" section.

If it doesn't, assess whether one is worth building. It is worth building when:
- The design uses material-based, category-based, or temperature-graded color palettes
  where multiple related tints need to be derived from a single base color
- The project has sticky or elevated surfaces where translucent tints bleed through on
  scroll and need premixed solid equivalents
- Palette derivation will recur across multiple design sessions

If it's worth building, use the inline coder to implement it now. Provide the following
spec to the coder:

---

**Color utility spec**

A small CLI script that computes perceptual color relationships precisely, so the designer
and coder aren't guessing at LCH-space values.

Core operations needed:

1. **adjust** — given an input color and LCH deltas (hue rotation, chroma shift,
   lightness shift), output the resulting color. This is how you derive a "cooler" or
   "warmer" variant of a base color without guessing: LCH is a perceptually uniform space
   where equal numeric steps produce equal perceived differences.

2. **blend** — given an input color, an opacity, and the project's backdrop color(s),
   output the premixed solid equivalent. This is needed whenever a translucent tint is
   used on a sticky or elevated surface: translucent backgrounds let page content bleed
   through on scroll.

3. **palette** (optional, add if the project derives palettes from base colors) — given
   a base color, output a set of variants using predefined LCH deltas appropriate to the
   project's palette logic. What "a set of variants" means is project-specific: temperature
   stops, lightness scale, semantic tints, etc.

Output format must match the project's CSS approach. For Tailwind: arbitrary-value class
strings. For CSS custom properties: the computed RGB values and a suggested variable name.
For plain CSS: hex values. The utility is only useful if its output is directly pasteable.

Recommended library: `chroma-js` for full LCH support in Node.js. For modern projects
preferring native CSS OKLCH, the utility may not be needed at all — OKLCH arithmetic
can happen directly in the stylesheet.

Wire it to a named package.json script (e.g., `pnpm color adjust "205 127 50" --hue -8`)
and document the commands in CLAUDE.md so future designer and coder sessions can find it
without reading the role prompts.

---

If building the utility is out of scope for this bootstrap session, note it as a
recommended follow-up and describe the project's palette derivation approach manually
in the library so designers can at least document the intended relationships, even if
they can't compute them precisely yet.

### 7. Interaction and motion

- Default transition duration and easing for state changes
- Whether animations are used at all and in what contexts (functional only, or expressive)
- Touch target minimums if mobile is a context

### 8. Sub-systems (if applicable)

If the project has sections with a distinct visual language (a marketing homepage vs.
an app dashboard, a documentation section vs. a tools section), document each as a
named sub-system with a one-paragraph boundary note describing what's different and
where to find the canonical reference.

---

## Output format

### corpora/ui-library.md

Structure the document with a section per topic above. Use concrete, precise language.
Every value that a designer or coder will need to use should be named — not "a dark
background" but "the page background: `--background` (gray-950 in dark mode)."

Include a short intro paragraph explaining: what this document is, who reads it, and
that it is text-based because text descriptions are more token-efficient and precise
than design artifacts (one sentence on the why is enough).

### corpora/ui-designer.md

Distill the significant decisions made in this session into seed principles in the standard
corpus schema. A foundational color system choice, a density decision, a typography role
assignment — these are worth encoding as ratified principles with conditions and reasons,
so future designer sessions can weigh them rather than re-derive them.

Aim for 5–10 principles. Do not encode every detail of the library — only the decisions
that involve real tradeoffs and where the reason matters for future work.

---

## If existing documentation was provided

When the operator provides existing brand guidelines, a token file, or a Figma export
as text:

- Treat it as authoritative for the decisions it covers
- Note explicitly what the source document established vs. what you're deciding fresh
- If the source document and the Tailwind/CSS approach conflict (e.g., brand specifies
  hex values but the project uses semantic tokens), resolve toward the project's token
  system and note the mapping

When substantial existing documentation is provided, the library section can be shorter —
transcribe the relevant values and add the sections the source document missed
(often: motion, density, sub-system boundaries, and the visual character paragraph).

---

## Proposed principles output

End your output with the standard proposed principles block:

```yaml
# Foundational design decisions proposed as seed principles.
# These will be written to corpora/ui-designer.md after operator review.
#
# - id: kebab-case-identifier
#   rule: "The guidance."
#   condition: "When this applies — be specific."
#   reason: "Why — the justification that makes this weighable."
#   provenance: "Bootstrap session, [date], [project name]."
#   status: proposed
```
