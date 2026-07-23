# Lenses — routing shorthand, not a schema entity

A **lens** is a stance + domain-subset composition (`kernel.md`, "Spawns: stance + lens") the
orchestrator checks first before composing anything ad hoc, and has reused often enough to be worth
naming, so a spawn brief (see
`kernel.md`, "The spawn brief") can write `composition: coder` instead of re-listing every domain.
Not a domain: no `principles:`, no ratify gate, no kill log. Lenses accumulate the same way domains
do — from repeated, observed composition, never declared up front. Adding, renaming, or retiring a
lens is an ordinary operator/orchestrator judgment call, not a ratify-gate action (nothing here is
a corpus proposal, and the `notes:` field below is explicitly non-normative — task-mechanics
reference, not weighable guidance). Renamed 2026-07-22 from "role aliases" — see LINEAGE.md — since
the working vocabulary should name what these actually are, not the fixed-role model they replaced.

Current seeded lenses:

```yaml
lenses:
  - name: coder
    stance: convergent
    domains: [coding-general, spawn-integrity]  # + coding-ts (language is js/ts), coding-react
                                #   (framework is React-based), css (styling is not none),
                                #   coding-nextjs (framework: nextjs), coding-expo (framework is
                                #   Expo/React Native via Expo) — each conditionally, per its own
                                #   preamble's stated condition against corpora/config.md
    notes: >
      Read corpora/config.md first for the project's registered utilities and verification
      commands; use a utility when its use-when condition matches. Load whichever stack-specific
      domains this project's shape actually matches (see the domains list above). Read the task,
      explore the codebase,
      implement the change precisely. Run the project's verification commands (lint, type-check,
      build — whatever config actually declares) before finishing. Report a `tradeoffs` block
      (design_element / cost / alternative / what_is_lost) for any spec or task where
      implementation cost clearly outweighs the value, rather than implementing or skipping
      silently. Design decisions (visual direction, layout, UX flows) are out of scope — flag them
      as a note to the orchestrator rather than deciding them.

  - name: dependency-management
    stance: convergent
    domains: [dependency-management, spawn-integrity]  # + coding-ts (language is js/ts),
                                #   coding-react (framework is React-based), css (styling is not
                                #   none), coding-nextjs (framework: nextjs), coding-expo (framework
                                #   is Expo/React Native via Expo) — each conditionally, per its own
                                #   preamble's stated condition against corpora/config.md
    notes: >
      For tasks whose actual subject is upgrading, migrating, or managing dependencies — not
      feature work that happens to touch a dependency in passing. Route here instead of `coder`
      when the task is framed as an upgrade/migration itself (a major framework bump, adopting a
      newly-mandatory architecture ahead of its deadline, auditing for silently-dropped transitive
      dependencies after an upgrade). Read corpora/config.md first for the project's registered
      utilities and verification commands. Load whichever stack-specific domains this project's
      shape actually matches, same as `coder`. Run the project's verification commands before
      finishing. Report a `tradeoffs` block for any migration step where cost clearly outweighs
      value rather than proceeding or skipping silently.

  - name: ux-design
    stance: convergent
    domains: [wizards-flows, ranking-evaluation, motion, validation-feedback, recoverability,
              lists-selection, forms-inputs, design-method, spawn-integrity]
    notes: >
      Read corpora/config.md first for the UX library location; halt and report if config is
      absent (Phase 1 of bootstrap must run first). Read the project's UX library — authoritative
      for current experience patterns; do not re-derive from code. If it doesn't exist yet, the
      project needs the `bootstrap-ux` alias's founding pass first, not this composition — route
      there instead of proceeding. The library is `bootstrap.md`'s narrative format — navigation model,
      flow inventory, interaction conventions, state/feedback patterns, recoverability conventions,
      each a prose section — never the domain-corpus `principles:` YAML shape (`id`/`rule`/
      `condition`/`reason`); that shape belongs to `corpora/domains/<domain>.md`, a different file
      entirely. Output is a user flow spec: user and goal, current experience,
      proposed flow per step (what's seen, actions available, system response, error/empty/edge
      cases), clarity requirements, open questions only if genuinely unresolvable after trying to
      resolve them from the library, config, or reasonable inference. Describe what the user
      perceives and does — never visual layout, styling, colors, or typography (that's the
      `ui-design` composition's job). Most proposals from this composition are `kind: judgment`;
      a genuine direction question mid-work means `status: questions-pending`, not a silent
      assumption.

  - name: planner
    stance: convergent
    domains: [planning, interviewing, spawn-integrity]
    notes: >
      A disambiguator, not a solver: reduce a capability's ambiguity to the point where other
      spawns can act, then decompose what remains into a sequenced, actionable task list. Read
      corpora/config.md, corpora/queue.md (if it exists, to avoid re-queuing work already in
      progress), and whatever planning artifact the operator references (ROADMAP.md, a feature
      spec, a user story, prose) — whichever form the capability description arrives in. Dialogue
      is scoped to the capability description, its own subject: do not try to anticipate the
      direction questions downstream spawns will face mid-work — those belong to the executing
      spawn, in its own lens, at the moment they arise, via the `questions-pending` handoff channel
      (`kernel.md`, "The handoff artifact"). Orient by reading the relevant source and project
      context — current state, what's missing, where this
      capability's edges are — recording findings for each task's `context` field so the executing
      spawn does not have to re-derive them. Settle what dialogue and orientation didn't: resolve
      from available information where possible; anything that can't resolve becomes an explicit
      open question, never a silent assumption. Decompose into atomic, concrete tasks — specific
      enough to route and act on without further planning, not trivial sub-steps — setting each
      task's `concern` to the character of the work (from what orientation found, not a lens name)
      and `judgment` to `settled` or `uncertain`. Sequence by real output dependency, never assumed
      lens order; mark tasks with no blockers between them as parallelizable. The most common
      self-check failure (see `spawn-integrity`) is naming files, functions, or data paths instead
      of the observable output and its acceptance condition. Write or update `corpora/queue.md` per
      the `planning` domain's schema; if a queue
      already exists for a different capability, surface the conflict to the operator rather than
      overwriting. Out of scope: assigning tasks to specific spawns, prescribing implementation
      approach or design direction, re-planning work already in progress or complete, ratifying its
      own proposals, or any routing/orchestration work — output the queue and stop.

  - name: ui-design
    stance: divergent
    domains: [color, surfaces-elevation, visual-hierarchy, motion, validation-feedback,
              recoverability, lists-selection, forms-inputs, design-method, spawn-integrity,
              interviewing]
    notes: >
      Read corpora/config.md first for the UI library location and registered utilities; halt and
      report if config is absent. Read the project's UI library — authoritative for color system,
      typography, spacing, component patterns, visual character; do not re-derive from
      screenshots. The library is `bootstrap.md`'s narrative format — concrete named values in
      prose sections, never the domain-corpus `principles:` YAML shape (`id`/`rule`/`condition`/
      `reason`); that shape belongs to `corpora/domains/<domain>.md`, a different file entirely. If
      a UX flow spec was provided, ground visual decisions in it. Output is a design spec: current state, proposed design per UI state (elements,
      layout, hierarchy, interaction behavior, empty/loading/selected/error states), open
      questions only if genuinely unresolvable. Describe proportions in relative terms — no pixel
      values, no CSS class names, no component names; implementation is not this composition's
      concern. Most proposals from this composition are `kind: direction` (the gate files these
      into the UI library, not a domain) — a divergent spawn's output is an identity choice, not a
      weighable rule; name every screen this spec changes in `ui-drift.screens` and every shared
      component it changes in `ui-drift.components`.

  - name: bootstrap-ui
    stance: divergent
    domains: [color, surfaces-elevation, visual-hierarchy, motion, design-method, spawn-integrity,
              interviewing]
    notes: >
      `bootstrap.md` Phase 2: founds a project's `corpora/ui-library.md` from nothing. Read
      whatever existing design documentation, token files, or aesthetic references the orchestrator
      provides; if none, ask at most two questions (audience/context, aesthetic direction) and offer
      the three default directions if the operator has nothing, per `bootstrap.md`. Cover color
      system, typography, density/spacing, component vocabulary, visual character, motion, and
      sub-systems as they apply — scope depth to what a feature actually needs when arriving via a
      planner-produced task, or to a foundational first pass otherwise; a greenfield project gets a
      short library that grows with the work, not a fully speculative one. Seed the screenshot cache
      (one canonical shot per identified screen) as you go. Most proposals are `kind: direction`;
      a genuine tradeoff worth encoding as a weighable principle is `kind: judgment`, not the
      default.

  - name: bootstrap-ux
    stance: convergent
    domains: [recoverability, validation-feedback, lists-selection, forms-inputs, design-method,
              spawn-integrity, interviewing]
    notes: >
      `bootstrap.md` Phase 3: founds a project's `corpora/ux-library.md` from nothing, after
      `bootstrap-ui` has run. Cover navigation model, flow inventory, interaction conventions,
      state/feedback patterns, and recoverability conventions, documenting what exists or was
      decided from the codebase, the UI library's behavioral notes, and any operator-provided
      product documentation. Do not invent aspirational patterns; a greenfield project gets a short
      library that grows with the work. Most proposals are `kind: direction`, same restraint as
      `bootstrap-ui`.
```
