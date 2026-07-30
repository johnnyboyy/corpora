---
name: corpora:ui-library-init
description: Found a project's UI library from nothing. Runs once, as bootstrap.md's Phase 2, only when has-ui yes. Produces corpora/ui-library.md, proposed design principles/directions, and identifies the components and screens that screenshot-library-init.md will capture next.
---

# UI library init

**Trigger:** `has-ui: yes`, no `ui-library.md` exists yet. Runs once, as bootstrap.md's Phase 2 —
see `bootstrap.md` for what precedes and follows this phase in the bootstrap sequence.

**Composition:** divergent stance, `unit-of-work: bootstrap-ui-surface` — run `scripts/corpus.py
select --unit-of-work bootstrap-ui-surface` rather than asserting the set freehand, same as any
other spawn brief. Narrower than ongoing `ui-design` work (`design-ui-surface`, which also composes
`forms-inputs`/`lists-selection`/`recoverability`/`validation-feedback`), since founding a library
from nothing doesn't have concrete components/screens for every domain to attach to yet — that
narrowing lives in each contributing domain's own `units-of-work` frontmatter, not in this file's
prose.

**Execution:** this is one spawn — after composing, follow `general-operation.md`'s Phase 3
onward (spawn brief, execution, relay, ratify gate) exactly as any other unit of work. Everything
below is this spawn's task content.

---

## Task

When this task arrived via a planner-produced queue (`bootstrap.md`, "Routing after Phase 1"), it
names a concrete feature to scope against — cover the sections below only to the depth that
feature actually needs, same restraint `ux-library-init.md` applies: do not invent aspirational
components, sub-systems, or states the feature doesn't touch. A greenfield project gets a short
library that grows with the work, not a fully speculative one authored sight-unseen. When there is
no feature to scope against (the direct, no-planner path), cover the sections at the depth needed
for a foundational first pass.

The orchestrator should pass any of the following that exist; work with what's provided and ask for
what's missing only if it blocks a foundational decision:

- Existing design documentation (brand guidelines, style guides, Figma exports as text)
- Token or variable files from an existing codebase (`tokens.css`, design tokens JSON, etc.)
- Aesthetic references (described or linked — e.g., "like Linear", "like Notion", "like a Bloomberg terminal")
- Audience and use context (from applicable project context or operator description)

If none of this was provided, ask the operator two questions before proceeding — no more than two
(stack is already known from `corpora/config.md`):

1. **Audience and context** — who uses this product and in what setting? (Office desk,
   field mobile, developer tooling, consumer app?)
2. **Aesthetic direction** — one reference or a few adjectives. If the operator has
   nothing, offer three distinct directions with a one-line description each and ask
   them to pick or redirect. (See defaults below.)

After those answers, proceed. Do not ask more questions until you have a draft.

The library sections below assume a CSS-based styling layer (web or Electron), which is the
context this phase runs in. Express values in the project's actual styling vocabulary as found in
`corpora/config.md` — CSS custom properties, Tailwind utilities, or plain CSS.

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

This section is `screenshot-library-init.md`'s own input: every component and screen named here is
what that phase captures and registers next, after this handoff ratifies. Name them precisely
enough to identify as a distinct screen or shared component — this phase does not run any capture
itself.

### 5. Visual character

A short paragraph (not a list) describing the overall aesthetic register. This is the
generative anchor the designer uses when making novel choices — it should be specific
enough to rule things out. Avoid generic words like "clean" or "modern" without
qualification. Instead: "Low saturation throughout. Motion is used sparingly and only
to mark state changes. No decorative elements. Data reads as the hero; chrome recedes."

### 6. Project utilities

Use existing registered utilities when their `use-when` conditions match. Do not invent utilities
during this phase or search for named categories. If this work itself exposes a deterministic,
precision-sensitive, or disproportionately token-expensive operation, surface it as a utility
candidate using the handoff schema. Color math is one example: a project may register a script for
OKLCH adjustment or alpha compositing because exact computation is cheaper than repeated inference.
The observed burden earns the proposal; the category does not.

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

## Findings — bugs and gaps are not proposals

Documenting an existing project will surface defects: treatments that contradict the system's own
evident intent (three border radii where the system clearly wants one), states with no defined
behavior, broken or missing affordances. These are **findings, not principles** — a defect
observation is not earned judgment, and proposing it pollutes the handoff's `proposals` field with
entries the gate can only kill.

Route findings to the handoff's `Surfaced` section, one line each: what was observed, where, and
why it reads as unintended rather than chosen. The orchestrator relays `Surfaced` verbatim; the
operator triages — fix now, queue as coder work, or declare it intended (at which point it may
become a direction).

The library records the **intended** pattern, not the defect: where the dominant convention is
clear, document that and note the deviation as a deviation. Documenting a bug as if it were a
convention re-teaches it to every future session.

---

## Output format

### corpora/ui-library.md

Structure the document with a section per topic above, in `bootstrap.md`'s library document format
(narrative prose, concrete named values, never the domain-corpus `principles:` shape). Every value
that a designer or coder will need to use should be named — not "a dark background" but "the page
background: `--background` (gray-950 in dark mode)."

Include a short intro paragraph explaining: what this document is, who reads it, and
that it is text-based because text descriptions are more token-efficient and precise
than design artifacts (one sentence on the why is enough).

### Proposed design principles

Distill the significant decisions made in this session into principles in the standard schema, and
surface them in the handoff's `proposals` field. A foundational color system choice, a density
decision, a typography role assignment — these are worth encoding with conditions and reasons, so
future designer sessions can weigh them rather than re-derive them. You propose the judgment; the
orchestrator assigns each ratified principle to a design domain at the gate (e.g. a color decision
to `color`, a documentation rule to `design-method`) and writes it to `corpora/domains/<domain>.md`.

There is no target count — propose what the work genuinely surfaced, and none is a valid
outcome when the library captured everything as direction. Most foundational choices are
`kind: direction` (identity decisions; the gate files them into the library itself). A
*principle* needs a real tradeoff whose reason will bind future weighing — do not dress a
direction up as one to fill a quota, and do not encode every detail of the library.

### Handoff

End by writing the handoff artifact per `kernel.md`, "The handoff artifact": the library goes in
the `Artifact` section; foundational design decisions go in `proposals` with `kind` set from the
inside (a mix of `judgment` and `direction`, provenance `"Bootstrap session, [date], [project
name]."`). Leave `ui-drift.screens`/`.components` empty — this phase names its screens and
components in the library document itself, which `screenshot-library-init.md` reads directly; it
does not use the drift-invalidation channel, which is reserved for a change to an *existing*
capture, not an initial one.
