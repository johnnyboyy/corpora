# Role aliases — routing shorthand, not a schema entity

Not a domain: no `principles:`, no ratify gate, no kill log. A recurring stance + domain-subset
composition the orchestrator has reused often enough to be worth naming, so a spawn brief (see
`kernel.md`, "The spawn brief") can write `composition: coder` instead of re-listing every domain.
Aliases accumulate the same way domains do — from repeated, observed composition, never declared
up front. Adding, renaming, or retiring an alias is an ordinary operator/orchestrator judgment
call, not a ratify-gate action (nothing here is a corpus proposal, and the `notes:` field below is
explicitly non-normative — task-mechanics reference, not weighable guidance).

Seeded 2026-07-21 (v3 lens-collapse migration, retiring `coder.md`, `packs/web-frontend/coder.md`,
`packs/web-frontend/ux-designer.md`, and `packs/web-frontend/ui-designer.md` as persistent lens
files):

```yaml
aliases:
  - name: coder
    stance: convergent
    domains: [coding-general]  # + coding-ts, coding-react, css, coding-nextjs (if framework:
                                #   nextjs) when role-pack: web-frontend
    notes: >
      Read corpora/config.md first for the project's registered utilities and verification
      commands; use a utility when its use-when condition matches. If the project declares a
      role-pack, load that pack's coder-overlay domains too. Read the task, explore the codebase,
      implement the change precisely. Run the project's verification commands (lint, type-check,
      build — whatever config actually declares) before finishing. Report a `tradeoffs` block
      (design_element / cost / alternative / what_is_lost) for any spec or task where
      implementation cost clearly outweighs the value, rather than implementing or skipping
      silently. Design decisions (visual direction, layout, UX flows) are out of scope — flag them
      as a note to the orchestrator rather than deciding them.

  - name: ux-design
    stance: convergent
    domains: [wizards-flows, ranking-evaluation, motion, validation-feedback, recoverability,
              lists-selection, forms-inputs, design-method]
    notes: >
      Read corpora/config.md first for the UX library location; halt and report if config is
      absent (Phase 1 of bootstrap must run first). Read the project's UX library — authoritative
      for current experience patterns; do not re-derive from code. If it doesn't exist yet, this
      spawn is in bootstrap: produce the flow spec, then create the library documenting the
      patterns it introduces. Output is a user flow spec: user and goal, current experience,
      proposed flow per step (what's seen, actions available, system response, error/empty/edge
      cases), clarity requirements, open questions only if genuinely unresolvable after trying to
      resolve them from the library, config, or reasonable inference. Describe what the user
      perceives and does — never visual layout, styling, colors, or typography (that's the
      `ui-design` composition's job). Most proposals from this composition are `kind: judgment`;
      a genuine direction question mid-work means `status: questions-pending`, not a silent
      assumption.

  - name: ui-design
    stance: divergent
    domains: [color, surfaces-elevation, visual-hierarchy, motion, validation-feedback,
              recoverability, lists-selection, forms-inputs, design-method]
    notes: >
      Read corpora/config.md first for the UI library location and registered utilities; halt and
      report if config is absent. Read the project's UI library — authoritative for color system,
      typography, spacing, component patterns, visual character; do not re-derive from
      screenshots. If a UX flow spec was provided, ground visual decisions in it. Read component
      documentation before speccing — do not spec a component without checking whether one already
      exists. Output is a design spec: current state, proposed design per UI state (elements,
      layout, hierarchy, interaction behavior, empty/loading/selected/error states), open
      questions only if genuinely unresolvable. Describe proportions in relative terms — no pixel
      values, no CSS class names, no component names; implementation is not this composition's
      concern. Most proposals from this composition are `kind: direction` (the gate files these
      into the UI library, not a domain) — a divergent spawn's output is an identity choice, not a
      weighable rule; set `ui-drift: yes` when the spec changes the rendered visual system.
```
