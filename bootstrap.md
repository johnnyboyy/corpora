---
name: corpora:bootstrap
description: Bootstrap a project's config, UI library, and UX library. Run once, before any feature design work. Works from existing design documentation, brand guidelines, aesthetic references, or from scratch with operator guidance. Outputs corpora/config.md (project shape, commands, and registered utilities), corpora/ui-library.md, corpora/ux-library.md, and proposed design principles ratified into the project's design domains. Text-only — no screenshots or image exports (see LINEAGE.md for why).
---

# Project Bootstrap

Reference for the orchestrator's bootstrap flow, run when `corpora/config.md` is absent — Phase 1
inline, Phase 2 by routing the UI designer with the Phase 2 section as the task, Phase 3 by routing
the UX designer with the Phase 3 section. Not a standalone skill.

- **Phase 1 — always, run inline.** Detect the project's shape, commands, and existing utilities; write
  **`corpora/config.md`** (schema below: shape — language, framework, package manager, `has-ui`,
  styling, `role-pack`; project resources — registered utilities, UI library location, verification
  commands). This flips the project to "bootstrapped" and runs for
  every project type.
- **Phase 2 — only when `has-ui: yes`, UI designer workstream.** Bootstrap the design system:
  **`corpora/ui-library.md`** (or the project's chosen path — the living design system reference)
  plus **proposed design principles** distilled from the foundational decisions and surfaced in
  the standard proposed-principles block; the orchestrator ratifies them into the project's design
  domains (`corpora/domains/<domain>.md`), assigning each a domain at the gate. This is the UI
  designer's foundational work — get it right and every subsequent designer session starts with
  real constraints; get it wrong and every session invents in a vacuum.
- **Phase 3 — only when `has-ui: yes`, UX designer workstream, after Phase 2.** Bootstrap the
  experience reference: **`corpora/ux-library.md`** plus proposed principles/directions, same
  gate. UI runs first deliberately — the divergent lens sets identity before the convergent lens
  documents constraints (see LINEAGE.md, "UI/UX seam settled").

The library and corpus are text-only. See LINEAGE.md for why text outperforms design artifacts
for this purpose.

---

## Phase 1 — Project shape and config (always)

Detect the project's shape before anything else. Read the platform's applicable project agent
instructions (`AGENTS.md` under Codex; `CLAUDE.md` under Claude Code), package manifest
(`package.json`, `pyproject.toml`, `Cargo.go`, `go.mod`, etc.), lockfiles, and relevant codebase
structure. If both agent-instruction files exist, read both; use the current platform's native file
for runtime-specific instructions and surface any substantive conflict in project requirements.
A project README is optional supporting evidence when present and useful, never a required or
authoritative instruction source. Determine, and ask the operator only for what you cannot infer:

- **Language(s)** — typescript, python, rust, go, etc.
- **Framework** — next.js, astro, electron, fastapi, none, etc.
- **Package manager** — pnpm, npm, bun, uv, cargo, go, etc.
- **`has-ui`** — does this project render a user interface a person looks at? A web app, an
  Electron app, a TUI → yes. A CLI that prints text, a library, a backend service → no. This
  single field decides whether Phases 2 and 3 run.
- **Styling approach** — tailwind, css-modules, vanilla-css, none, etc. (`none` is correct for
  non-UI projects.)
- **`role-pack`** — which role pack the project's roles should overlay. A web/Electron UI on a
  JS/TS stack → `web-frontend`. Anything this repo has no pack for → `none` (the project runs on
  the kernel alone; that is a valid, complete configuration).
- **Verification commands** — the project's lint, type-check, build, and/or test commands. Run
  what the project actually has; not every ecosystem separates these, and some have none.

Record existing project-owned utilities and exact verification commands using the schema below.
Do not search for predetermined utility categories or persist environment-owned capabilities; the
runtime already exposes browser automation, image generation, delegation, and similar tools. Then
**write `corpora/config.md`**. Detect, don't assume: an incorrect role pack, command, or utility is
worse than `none` because a role will try to use something that is not there.

**If `has-ui: no`, Phase 1 is the whole job.** Write `corpora/config.md` and stop — no UI library,
no design principles, no designer roles for this project. Note to the operator that design-phase
roles are inactive and the project runs on the kernel (orchestrator + base coder).

**If `has-ui: yes`, continue to Phases 2 and 3.**

For a UI project, also create `corpora/deferred-decisions.md` from `kernel.md`, "Deferred UI/UX
decisions," with an empty `decisions: []` list. This queue is project working state, not corpus.
For every project, create `corpora/utility-candidates.md` from `kernel.md`, "Project utilities,"
with an empty `candidates: []` list.

---

## Phase 2 — UI library (only when `has-ui: yes`)

You are now the UI designer bootstrapping a design system for a project that has none yet. The
orchestrator should pass any of the following that exist; work with what's provided and ask for
what's missing only if it blocks a foundational decision:

- Existing design documentation (brand guidelines, style guides, Figma exports as text)
- Token or variable files from an existing codebase (`tokens.css`, design tokens JSON, etc.)
- Aesthetic references (described or linked — e.g., "like Linear", "like Notion", "like a Bloomberg terminal")
- Audience and use context (from applicable project context or operator description)

If none of this was provided, ask the operator two questions before proceeding — no more than two
(stack is already known from Phase 1):

1. **Audience and context** — who uses this product and in what setting? (Office desk,
   field mobile, developer tooling, consumer app?)
2. **Aesthetic direction** — one reference or a few adjectives. If the operator has
   nothing, offer three distinct directions with a one-line description each and ask
   them to pick or redirect. (See defaults below.)

After those answers, proceed. Do not ask more questions until you have a draft.

The library sections below assume a CSS-based styling layer (web or Electron), which is the
context Phase 2 runs in. Express values in the project's actual styling vocabulary as found in
Phase 1 — CSS custom properties, Tailwind utilities, or plain CSS.

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

### 6. Project utilities

Use existing registered utilities when their `use-when` conditions match. Do not invent utilities
during bootstrap or search for named categories. If this work itself exposes a deterministic,
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

## The config file (`corpora/config.md`)

The file every role reads to learn stable project facts — without it the project is "not
bootstrapped." It records **project shape**, **project-owned utilities**, library locations, and
verification commands. Runtime-owned capabilities are discovered each session and never persisted.
When updating a legacy config, remove browser/image runtime entries and migrate any project-owned
color or other deterministic script into the general utility registry.

- **Utilities** — deterministic project-owned tools that replace recurring inference. Record their
  purpose, triggering condition, exact invocation, operations, and output shape. An empty registry
  is normal; do not speculate during bootstrap.
- **UI library** — where does the design system reference live? Default `corpora/ui-library.md`;
  only note a path here if it's non-standard. `none` for projects with no UI.
- **Verification commands** — the project's lint, type-check, build, and/or test commands. Record
  only what the project actually has.

### Schema

Human-readable and edited by hand as the project changes; machine-read by every role at session
start. Keep it terse because it loads on every role invocation. Project-shape and command values
are concrete or `none`; utilities are an explicit list or `utilities: []`.

```markdown
# Config

Read this file at the start of any role session. It declares the project's shape, registered
project utilities, libraries, and verification commands. Generated by `corpora:bootstrap`; edit by
hand as the project changes. Discover environment-owned capabilities from the current runtime.

## project-shape
language: <e.g. typescript, python, rust, go>
framework: <e.g. next.js, astro, electron, fastapi, none>
package-manager: <e.g. pnpm, npm, bun, uv, cargo, go>
has-ui: <yes | no>
styling: <e.g. tailwind, css-modules, vanilla-css, none>
role-pack: <e.g. web-frontend, or none>

## utilities
utilities:
  - id: <e.g. color-math>
    purpose: <the deterministic inference burden it replaces>
    use-when: <condition under which a role should invoke it>
    invoke: <exact command form>
    operations: [<supported operations>]
    output: <paste-ready or machine-readable output shape>
    provenance: <workstream and date that demonstrated its value>

Use `utilities: []` when the project has none.

## ui-library
path: corpora/ui-library.md

## verification-commands
lint: <the project's lint command, or none>
check: <static analysis or type-check command, or none>
build: <the project's build command, or none>
test: <the project's test command, or none>
```

## Output format

### corpora/config.md

Write the config file using the schema above (detect, don't assume — see Phase 1).

### corpora/deferred-decisions.md

For `has-ui: yes`, create the queue with its explanatory heading and an empty YAML list:

````markdown
# Deferred decisions

Only non-blocking UI/UX questions belong here. Blocking questions are surfaced immediately.

```yaml
decisions: []
```
````

For `has-ui: no`, do not create a queue.

### corpora/utility-candidates.md

Create the persistent candidate ledger for every project:

````markdown
# Utility candidates

```yaml
candidates: []
```
````

### corpora/ui-library.md

Structure the document with a section per topic above. Use concrete, precise language.
Every value that a designer or coder will need to use should be named — not "a dark
background" but "the page background: `--background` (gray-950 in dark mode)."

Include a short intro paragraph explaining: what this document is, who reads it, and
that it is text-based because text descriptions are more token-efficient and precise
than design artifacts (one sentence on the why is enough).

### Proposed design principles

Distill the significant decisions made in this session into principles in the standard schema, and
surface them in the proposed-principles block below. A foundational color system choice, a density
decision, a typography role assignment — these are worth encoding with conditions and reasons, so
future designer sessions can weigh them rather than re-derive them. You propose the judgment; the
orchestrator assigns each ratified principle to a design domain at the gate (e.g. a color decision
to `color`, a documentation rule to `design-method`) and writes it to `corpora/domains/<domain>.md`.

There is no target count — propose what the work genuinely surfaced, and none is a valid
outcome when the library captured everything as direction. Most foundational choices are
`kind: direction` (identity decisions; the gate files them into the library itself). A
*principle* needs a real tradeoff whose reason will bind future weighing — do not dress a
direction up as one to fill a quota, and do not encode every detail of the library.

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

## Phase 3 — UX library (only when `has-ui: yes`, after Phase 2)

You are now the UX designer bootstrapping the project's experience reference. The UI designer has
already run — identity is set; your job is convergent documentation of how the product *works* as
an experience, so future UX sessions weigh established patterns instead of re-deriving them.

Write `corpora/ux-library.md` (or the path config names under `ux-library`) covering, as they
exist in the project:

- **Navigation model** — how users move between surfaces; what is global vs contextual
- **Flow inventory** — the primary user journeys, each in a few lines: entry, steps, exit,
  what state persists
- **Interaction conventions** — selection, editing, confirmation, dismissal; where the project
  asks vs acts
- **State and feedback patterns** — loading, empty, error, success; how progress and failure
  are communicated
- **Recoverability conventions** — which actions are undoable, where recovery surfaces live

Document what exists or was decided — from the codebase, the UI library's behavioral notes, and
any operator-provided product documentation. Do not invent aspirational patterns; a greenfield
project gets a short library that grows with the work. The same restraint as Phase 2 applies to
proposals: no target count, most foundational choices are `kind: direction`.

---

## Findings — bugs and gaps are not proposals

Applies to Phases 2 and 3. Documenting an existing project will surface defects: treatments that
contradict the system's own evident intent (three border radii where the system clearly wants
one), states with no defined behavior, broken or missing affordances. These are **findings, not
principles** — a defect observation is not earned judgment, and proposing it pollutes the
handoff's `proposals` field with entries the gate can only kill.

Route findings to the handoff's `Surfaced` section, one line each: what was observed, where, and
why it reads as unintended rather than chosen. The orchestrator relays `Surfaced` verbatim; the
operator triages — fix now, queue as coder work, or declare it intended (at which point it may
become a direction).

The library records the **intended** pattern, not the defect: where the dominant convention is
clear, document that and note the deviation as a deviation. Documenting a bug as if it were a
convention re-teaches it to every future session.

---

## Proposed principles output

Applies to Phases 2 and 3. End by writing your **handoff artifact** per `kernel.md`, "The handoff
artifact": the library goes in the `Artifact` section (Phase 2 sets `ui-drift: yes` — it defines
the rendered visual system; Phase 3 documents experience and does not);
foundational design decisions go in the envelope's `proposals` field with `kind` set from the
inside. Expect a mix: seed *principles* (weighable rules — `kind: judgment`) and *directions*
(identity choices the gate files into the library itself rather than a domain — `kind:
direction`). Provenance: `"Bootstrap session, [date], [project name]."` The orchestrator
ratifies principles into the project's design domains (`corpora/domains/<domain>.md`), assigning
each a domain at the gate, after operator review.
