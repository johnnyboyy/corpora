# corpora

A system for accumulating learned judgment across agent sessions and projects. Judgment lives in **domains**, not roles — a **spawn** is a stance plus a domain subset the orchestrator composes fresh per task, so shared judgment is written once and never duplicated across role files.

The mechanics: judgment lives in **domains** (corpora scoped to a subject matter or decision class). A **spawn** is a *stance* (convergent or divergent — see `kernel.md`, "Generative stance") plus the domains the orchestrator composes for the task at hand — never a persistent named file with its own fixed declaration. The shared mechanism — schema, ratify gate, retrospective — is the **kernel**. Seed domains carry general principles earned from real work; a project adds its own same-named domains. Principles ratified in a project can promote upward to the seed domain when they generalize across projects, or fold into a domain's own preamble when they've stabilized into scene-setting that no longer needs per-task condition-checking. Rejected principles are kept with their reason and a `kill_type` — the kill log is often more instructive than the ratified list. Kernel and seed domains travel in this repo; project domains stay in the project.

Domains, not roles, own corpora — so shared judgment lives once and is available to any spawn whose stance and subject match (a `ui-design`- and a `ux-design`-composed spawn both load `recoverability`, for example, without either one "owning" it). Domain boundaries are discovered from accumulated tension (the fork signal in the retrospective), never declared up front from an org chart.

## Architecture

**One flat domain pool, one fixed process layer:**

- **The orchestrator** (`SKILL.md`, declares `orchestrator-routing` and `ratify-gate`) is the one fixed thing: a process layer that composes and routes spawns but never takes on a spawn's stance itself, so something occupies that position before any composition can happen. The **planner** is not fixed the same way — it's a seeded alias (`domains/lenses.md`, domains `planning` + `interviewing`) that composes like any other spawn. Every working spawn composes from `coding-general` at minimum; there is no fixed "base coder" file.
- **Domains** — stack-agnostic (`coding-general`, `orchestrator-routing`, `spawn-integrity`, ...) and stack-specific (`coding-react`, `css`, `color`, ...) domains live together in one flat `domains/`, not two separate layers. There's no "role pack" selected by a project-config field: each stack-specific domain states its own load condition directly against `corpora/config.md`'s shape fields (`language`, `framework`, `styling`, `has-ui`) in its own preamble — retired 2026-07-22, since a `role-pack:` field only ever bundled conditions the domains already carried individually, all-or-nothing.

`domains/lenses.md` names the recurring compositions (`coder`, `ux-design`, `ui-design`, `planner`) as routing shorthand, not a schema entity — domains available to an alias are not new fixed roles. One composed spawn per named alias runs at a time per project; a domain splits into scoped instances only when the retrospective surfaces a fork signal (conditions that partition the space and give opposing advice), never from an org chart.

**Domains (where judgment lives):**

- **Seed domain** — general principles, in the skill's flat `domains/`.
- **Project domain** — project-specific accumulated judgment at `corpora/domains/<domain>.md` in the target project. Never merged back here without abstraction.

For each domain a spawn's composition includes, both apply when it runs — seed first, then the same-named project domain. A project may also have domains with no seed counterpart (project-specific subjects, e.g. `spatial-metaphor`).

**Two load modes** (file granularity matches load granularity):

- **Working load** — a spawn's composed domains, *working files only* (`domains/<domain>.md`). Selective and inspectable; this is every new isolated spawn and inline segment.
- **Audit load** — the orchestrator reads domains broadly *including* `domains/audit.md` (provenance, kills) at ratify and retrospective time only.

**Spawn contexts.** Each spawn receives its stance frame plus every composed domain, and nothing from the other stance or an undeclared domain. The orchestrator decides whether to run inline, resume the agent owning the workstream, or start an isolated agent. Handoffs are checkpoints; operator testing and revisions return to the owning agent. See `SKILL.md`, "Inline, resume, or isolate," and LINEAGE.md, "Role isolation."

## Files

- `SKILL.md` — the shared orchestrator entrypoint for Claude Code (`/corpora`) and Codex (`$corpora`): routes workstreams, assembles complete spawn loads, relays handoffs, and drives the ratify gate.
- `kernel.md` — the schema, stance+composition model, ratify gate, write-back format, two load modes, retrospective signals, and domain lifecycle. Reference document.
- `domains/` — every seed domain, flat: stack-agnostic (`coding-general.md`, `orchestrator-routing.md`, `ratify-gate.md`, `planning.md`, `interviewing.md`, `spawn-integrity.md`) and stack-specific (`coding-ts.md`, `coding-react.md`, `coding-nextjs.md`, `css.md`, and the design domains `color.md`/`motion.md`/`recoverability.md`/etc.) alike, each stating its own load condition in its own preamble. Plus `lenses.md` (routing shorthand, not a domain, seeds `coder`/`ux-design`/`ui-design`/`planner`) and `audit.md` (provenance/kill detail for the layer, loaded only at ratify/retrospective time).
- `bootstrap.md` — one-time project setup. Phase 1 detects project shape and writes `corpora/config.md`. Phases 2 and 3 (UI projects only) generate `corpora/ui-library.md` (`ui-design`-composed, divergent) then `corpora/ux-library.md` (`ux-design`-composed, convergent) and propose seed design principles.
- `LINEAGE.md` — intellectual history: why conventions became law, key kills, design decisions.
- `reader-tax-and-the-model.md` — a living, multi-model assessment of whether Explicit by Default helps the model itself, not only the human reviewer.

## Installation

Clone this repository once, then symlink the same working copy into either or both skill directories:

```bash
ln -s /absolute/path/to/corpora ~/.claude/skills/corpora
ln -s /absolute/path/to/corpora ~/.codex/skills/corpora
```

Claude Code invokes it as `/corpora`. Codex invokes it as `$corpora` and may also activate it implicitly. A managed project's `AGENTS.md` can opt into automatic Codex activation with the one-line instruction offered by the skill.

## Using in a project

1. Invoke corpora on an unbootstrapped project. The orchestrator detects that `corpora/config.md` is absent and runs bootstrap: Phase 1 writes stable project shape, commands, and registered utilities; UI projects then route `ui-design`- and `ux-design`-composed bootstrap workstreams for their libraries.
2. On subsequent invocations, the orchestrator routes work inline, to an existing workstream agent, or to a new isolated spawn. A plan starts a new coder-composed workstream; testing feedback and revisions return to its owning agent.
3. Handoffs surface proposals, violations, utility candidates, and other routing material. The operator ratifies corpus and direction changes.
4. `corpora/domains/<domain>.md` holds project-specific principles. The orchestrator creates a domain file on first ratification into it and assigns every ratified proposal a domain at the gate.

**Project files** (all under `corpora/` in the target project):

- `config.md` — stable project shape, registered deterministic utilities, library paths, and verification commands
- `ui-library.md` — design system documentation (generated by bootstrap, updated by designers)
- `ux-library.md` — experience patterns and flow documentation for UI projects
- `deferred-decisions.md` — non-blocking UI/UX questions waiting for a coherent designer workstream
- `utility-candidates.md` — persistent accepted, denied, and deferred utility observations
- `handoffs/` — unratified spawn checkpoints and their pending gate material
- `domains/<domain>.md` — per-domain accumulated judgment (working fields only)
- `domains/audit.md` — provenance and per-kill detail for the project layer

See `kernel.md` for the full principle schema and write-back format.

## Validation

Run the dependency-free regression suite with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## Cross-project learning

When a principle in a project domain is general — its condition doesn't reference the project's stack or specifics — it's a candidate for promotion to the seed domain of the same name here. The project domain is where principles are earned; this repo is where they graduate.

The retrospective is the natural trigger: when a project-level principle has held across enough tasks that it reads as general rather than project-specific, the retrospective surfaces it as a seed promotion candidate. The exact process for that promotion is not yet spelled out.

The seed domains here have been through a retrospective pass (2026-06-20): scoping misplaced principles, flagging single-project principles as provisional, and killing redundant entries. A provisional flag means the principle was earned in one project context and hasn't been stress-tested against a second.

## New stacks and domain splitting

**New stack:** the kernel applies unchanged — every new project inherits the orchestrator, the planner, and `coding-general` for free. Add stack-specific seed domains (with their own load conditions against `language`/`framework`/`styling`) only once a body of stack-specific conventions has accumulated and is worth shipping across projects of that stack. Until then, project-earned specifics live in `corpora/domains/coding-general.md` (and project-specific domains). Do not pre-build stack-specific domains speculatively.

**Domain splitting:** new judgment lands in the domain it's about (a new domain is born at the ratify gate when nothing fits, after clearing the genuine-fork test — see `kernel.md`, "The genuine-fork test"). A domain splits into scoped instances only when it develops a genuine fork signal — conditions that partition the space and give opposing advice. Reach for this only when accumulated tension reveals the seam, not from an org chart.
