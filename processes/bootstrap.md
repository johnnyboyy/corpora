---
name: corpora:bootstrap
description: Bootstrap a project's config, UI library, screenshot cache, and UX library. Run once, before any feature design work. Outputs corpora/config.md always; for has-ui projects, via a direct designer sequence or a planner-produced queue depending on whether a concrete feature accompanied the bootstrap request, also a UI library, a seeded screenshot manifest, a UX library, and proposed design principles ratified into the project's design domains. The library documents themselves stay text-only — no screenshots or image exports embedded (see LINEAGE.md for why).
---

# Project Bootstrap

Reference for the orchestrator's bootstrap sequence, run when `corpora/config.md` is absent — Phase
1 (below) always runs inline and is corpora's own: it is what makes corpora itself routable, the
one fallback corpora needs regardless of what else is installed. Not a standalone skill.

**Sequencing is a fixed pipeline with one real fork.** Phase 1 always runs first. Phase 2 (UI
library) always runs before Phase 3 (screenshot seed) and Phase 4 (UX library) — both are a content
dependency, not an arbitrary process choice: the UX library cites the UI library's tokens and
components, and the screenshot phase reads the screens and components Phase 2 named. Phase 3 and
Phase 4 are independent of *each other* — both are blocked-by Phase 2 only, and may run in either
order, exactly as `planning.md`'s `sequence-by-output-dependency` principle would decompose them.

- **Phase 1 — always, run inline, corpora's own.** Always ensures **`corpora/config.md`** exists
  (schema below: shape — language, framework, package manager, `has-ui`, styling; project
  resources — registered utilities, UI library location, verification commands) — this flips the
  project to "bootstrapped" and runs for every project type. Corpora detects the shape, commands,
  and existing project utilities that go into it directly, every time.
- **Phase 2 — only when `has-ui: yes`.** Bootstrap the design system: see `processes/ui-library-init.md` for
  the full composition, task, and output format.
- **Phase 3 — only when `has-ui: yes`, after Phase 2.** Seed the screenshot cache: see
  `processes/screenshot-library-init.md`. Mechanical — no composition, no stance, no handoff of its own.
- **Phase 4 — only when `has-ui: yes`, after Phase 2.** Bootstrap the experience reference: see
  `processes/ux-library-init.md` for the full composition, task, and output format.

The library and corpus are text-only. See LINEAGE.md for why text outperforms design artifacts
for this purpose.

---

## Routing after Phase 1

Once `corpora/config.md` exists, decide whether a concrete operator feature request accompanied
this bootstrap (the request that triggered `corpora:bootstrap` named something to build, not just
"set this project up"). This is the same judgment the orchestrator always applies before spawning —
`orchestrator-routing.md`'s `spawn-threshold-is-spec-scope` — applied to the case where bootstrapping
itself is part of the scope being weighed.

- **No concrete feature request.** Nothing exists yet to scope a design system against, and the
  remaining work (stand up the UI library, seed the screenshot cache, stand up the UX library) has
  no real decomposition or sequencing ambiguity beyond the fork already stated above — it's not a
  planning problem. Run Phase 2, then Phase 3 and Phase 4 (either order), directly, exactly as
  above. Skip the planner — it would add a hop with nothing to decompose. (`has-ui: no` with no
  feature request: Phase 1 was already the whole job, per Phase 1 above.)
- **A concrete feature request exists.** Hand off to the planner with a capability description
  combining both needs — e.g. *"Bootstrap this project's design system (has-ui: yes) and
  implement: \<operator's request, verbatim\>."* This is passed as direct input, not sourced from a
  `ROADMAP.md` (none exists yet for a fresh project). The planner treats it like any other
  capability: no changes to `domains/planning.md` are needed — it orients (finds `corpora/
  config.md` but no `ui-library.md`, `ux-library.md`, screenshot manifest, or existing code),
  decomposes into tasks (`bootstrap-ui-library`, `bootstrap-screenshot-library`,
  `bootstrap-ux-library` when `has-ui: yes`, plus the feature's own task(s)), and sequences by real
  output dependency: `bootstrap-screenshot-library` and `bootstrap-ux-library` are each blocked-by
  `bootstrap-ui-library` only, independent of each other; the feature task is blocked-by
  `bootstrap-ui-library` and `bootstrap-ux-library` (it needs their output), not by
  `bootstrap-screenshot-library`, which produces no output the feature consumes. Scoping each
  design-system task to what the feature actually needs — rather than a fully speculative library —
  is exactly the outcome this routing is for: `processes/ui-library-init.md` and `processes/ux-library-init.md` both
  already state this restraint for a planner-produced task.

  **One boundary to hold:** the planner's dialogue step must not ask the audience/aesthetic-direction
  questions that open `processes/ui-library-init.md` — those are that phase's own divergent
  judgment call, asked when its task actually runs, not decomposition-shaping ambiguity the
  planner should resolve upfront. `domains/planning.md`'s own preamble
  already states this general rule ("do not anticipate the direction questions downstream
  spawns will face mid-work"); this is that rule's bootstrap instance, named here because it's easy
  to blur in practice.

  Once the queue is written, the orchestrator executes it per `processes/general-operation.md`'s normal
  routing and ratify-gate judgment, task by task.

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
  single field decides whether Phases 2, 3, and 4 run.
- **Styling approach** — tailwind, css-modules, vanilla-css, none, etc. (`none` is correct for
  non-UI projects.) Together with `language` and `framework`, this is what each stack-specific
  domain's `applies-when` frontmatter checks to decide whether it loads for this project — there is
  no separate role-pack field to set; a project stack simply is or isn't what a given domain's
  condition names.
- **Verification commands** — the project's lint, type-check, build, and/or test commands. Run
  what the project actually has; not every ecosystem separates these, and some have none.

Record existing project-owned utilities and exact verification commands using the schema below.
Do not search for predetermined utility categories or persist environment-owned capabilities; the
runtime already exposes browser automation, image generation, delegation, and similar tools. Then
**write `corpora/config.md`**. Detect, don't assume: an incorrect command or utility is worse than
`none` because a spawn will try to use something that is not there.

**If `has-ui: no` and no concrete feature request accompanied this bootstrap, Phase 1 is the whole
job.** Write `corpora/config.md` and stop — no UI library, no design principles, no design spawns
for this project. Note to the operator that divergent/visual-identity domains are inactive and the
project runs on the kernel layer (the orchestrator, the planner, and coder-composed spawns only).
(If `has-ui: no` but a feature request *was* given, see "Routing after Phase 1" — the planner
still decomposes the feature into coder tasks, just with no design-system tasks in the queue.)

**If `has-ui: yes`, see "Routing after Phase 1" above** to decide whether Phases 2–4 run directly
or via a planner-produced queue.

For a UI project, also create `corpora/deferred-decisions.md` from `kernel.md`, "Deferred UI/UX
decisions," with an empty `decisions: []` list. This queue is project working state, not corpus.
For every project, create `corpora/deterministic-shortcut-candidates.md` from `kernel.md`, "Project utilities,"
with an empty `candidates: []` list.

---

## The config file (`corpora/config.md`)

The file every spawn reads to learn stable project facts — without it the project is "not
bootstrapped." It records **project shape**, **project-owned utilities**, library locations, and
verification commands. Runtime-owned capabilities are discovered each session and never persisted.
When updating a legacy config, remove browser/image runtime entries and migrate any project-owned
color or other deterministic script into the general utility registry. Also drop a legacy
`role-pack:` line if present — retired 2026-07-22; the fields already here (`language`, `framework`,
`styling`) are what each stack-specific domain now checks directly.

- **Project shape and verification commands** — write `## project-shape` and `##
  verification-commands` with the detected values in full.
- **Utilities** — deterministic project-owned tools that replace recurring inference. Record their
  purpose, triggering condition, exact invocation, operations, and output shape. An empty registry
  is normal; do not speculate during bootstrap.
- **UI library** — where does the design system reference live? If an external artifact-location
  registry already exists for this project (a file recording where UI/UX libraries and screenshot
  caches are placed, maintained outside corpora's own state), that registry's path wins — corpora
  doesn't decide this unilaterally when something else already owns artifact placement. Otherwise,
  default `corpora/ui-library.md`; only note a path here if it's non-standard. `none` for projects
  with no UI.
- **Verification commands** — the project's lint, type-check, build, and/or test commands. Record
  only what the project actually has.
- **`debug`** — not detected during bootstrap; leave `no` (or omit) unless the operator asks for it.
  When `yes`, `compose-spawn-prompt` saves its default session-prompt file (`kernel.md`, "The spawn
  brief") and a ratified handoff is archived under `corpora/handoffs/archive/` instead of deleted
  (`kernel.md`, "The handoff artifact"). Both are audit trails with no functional role otherwise —
  the gate exists so a project only pays that disk/history cost when someone actually wants to
  inspect past spawn prompts and handoffs, not by default.

### Schema

Human-readable and edited by hand as the project changes; machine-read by every spawn at session
start. Keep it terse because it loads on every spawn invocation. Project-shape and command values
are concrete or `none`; utilities are an explicit list or `utilities: []`.

```markdown
# Config

Read this file at the start of any spawn's session. It declares the project's shape, registered
project utilities, libraries, and verification commands. Generated by `corpora:bootstrap`; edit by
hand as the project changes. Discover environment-owned capabilities from the current runtime.

## project-shape
language: <e.g. typescript, python, rust, go>
framework: <e.g. next.js, astro, electron, fastapi, none>
package-manager: <e.g. pnpm, npm, bun, uv, cargo, go>
has-ui: <yes | no>
styling: <e.g. tailwind, css-modules, vanilla-css, none>

## utilities
utilities:
  - id: <e.g. color-math>
    purpose: <the deterministic inference burden it replaces>
    use-when: <condition under which a spawn should invoke it>
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

## debug
debug: <yes | no>  # optional; omit or leave "no" unless the operator asks. See "The config file" above.
```

---

## Library document format

`corpora/ui-library.md` and `corpora/ux-library.md` share one convention, whichever phase or sync
process is writing to them: narrative prose with concrete named values, never the domain-corpus
`principles:` YAML shape (id/rule/condition/reason) — `domains/spawn-integrity.md`'s
`library-is-narrative-not-corpus-shape` principle is what enforces this for any spawn reading or
writing either file.

Structure the document with a section per topic the writing phase defines. Use concrete, precise
language. Every value that a designer or coder will need to use should be named — not "a dark
background" but "the page background: `--background` (gray-950 in dark mode)."

Include a short intro paragraph explaining: what this document is, who reads it, and that it is
text-based because text descriptions are more token-efficient and precise than design artifacts
(one sentence on the why is enough).

---

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

### corpora/deterministic-shortcut-candidates.md

Create the persistent candidate ledger for every project:

````markdown
# Deterministic shortcut candidates

```yaml
candidates: []
```
````

---

**Checkpoint — reapply the orchestrator, between every phase.** Each of Phase 2, Phase 3, and
Phase 4 produces its own handoff (Phase 3 produces none — it is mechanical, see
`processes/screenshot-library-init.md`), and a handoff is not a finished write-back: it needs the ratify gate
(`processes/general-operation.md`, Phase 6) before the next phase can rely on its output. Drop that phase's
composition, run the gate, then route into whichever phase is next per the sequencing fork stated
above. Bootstrap is complete once every applicable phase has run — resume as the orchestrator for
everything from here forward, routing, further spawn work, all of it.
