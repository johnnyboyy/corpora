# Role aliases — routing shorthand, not a schema entity

Not a domain: no `principles:`, no ratify gate, no kill log. A recurring stance + domain-subset
composition the orchestrator has reused often enough to be worth naming, so a spawn brief (see
`kernel.md`, "The spawn brief") can write `composition: coder` instead of re-listing every domain.
Aliases accumulate the same way domains do — from repeated, observed composition, never declared
up front. Adding, renaming, or retiring an alias is an ordinary operator/orchestrator judgment
call, not a ratify-gate action (nothing here is a corpus proposal, and the `notes:` field below is
explicitly non-normative — task-mechanics reference, not weighable guidance).

Current seeded aliases:

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
      patterns it introduces. The library is `bootstrap.md`'s narrative format — navigation model,
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
    domains: [planning, interviewing]
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
      task's `concern` to the character of the work (from what orientation found, not a role name)
      and `judgment` to `settled` or `uncertain`. Sequence by real output dependency, never assumed
      role order; mark tasks with no blockers between them as parallelizable. Self-check every task
      description against the `planning` domain before writing — the most common failure is naming
      files, functions, or data paths instead of the observable output and its acceptance
      condition. Write or update `corpora/queue.md` per the `planning` domain's schema; if a queue
      already exists for a different capability, surface the conflict to the operator rather than
      overwriting. Out of scope: assigning tasks to specific spawns, prescribing implementation
      approach or design direction, re-planning work already in progress or complete, ratifying its
      own proposals, or any routing/orchestration work — output the queue and stop.

  - name: ui-design
    stance: divergent
    domains: [color, surfaces-elevation, visual-hierarchy, motion, validation-feedback,
              recoverability, lists-selection, forms-inputs, design-method]
    notes: >
      Read corpora/config.md first for the UI library location and registered utilities; halt and
      report if config is absent. Read the project's UI library — authoritative for color system,
      typography, spacing, component patterns, visual character; do not re-derive from
      screenshots. The library is `bootstrap.md`'s narrative format — concrete named values in
      prose sections, never the domain-corpus `principles:` YAML shape (`id`/`rule`/`condition`/
      `reason`); that shape belongs to `corpora/domains/<domain>.md`, a different file entirely. If
      a UX flow spec was provided, ground visual decisions in it. Read component
      documentation before speccing — do not spec a component without checking whether one already
      exists. Output is a design spec: current state, proposed design per UI state (elements,
      layout, hierarchy, interaction behavior, empty/loading/selected/error states), open
      questions only if genuinely unresolvable. Describe proportions in relative terms — no pixel
      values, no CSS class names, no component names; implementation is not this composition's
      concern. Most proposals from this composition are `kind: direction` (the gate files these
      into the UI library, not a domain) — a divergent spawn's output is an identity choice, not a
      weighable rule; name every screen this spec changes in `ui-drift.screens` and every shared
      component it changes in `ui-drift.components`.
```
