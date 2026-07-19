# corpora

A system for accumulating learned judgment across agent sessions and projects. Judgment lives in **domains**, not roles — roles are lenses that declare which domains they load, so shared judgment is written once and never duplicated across role files.

The mechanics: judgment lives in **domains** (corpora scoped to a subject matter or decision class), and a **role** is a *lens* (a domain prompt) plus a static declaration of the domains it loads. The shared mechanism — schema, ratify gate, retrospective — is the **kernel**. Seed domains carry general principles earned from real work; a project adds its own same-named domains. Principles ratified in a project can promote upward — to the seed domain when they generalize across projects, to the lens prompt itself when they stabilize into defaults. Rejected principles are kept with their reason and a `kill_type` — the kill log is often more instructive than the ratified list. Kernel, lenses, and seed domains travel in this repo; project domains stay in the project.

Domains, not roles, own corpora — so shared judgment lives once and is declared by every lens that needs it (the UI and UX designers both declare `recoverability`, for example). Domain boundaries are discovered from accumulated tension (the fork signal in the retrospective), never declared up front from an org chart.

## Architecture

**Two layers of lenses:**

- **Kernel** — stack-agnostic, always loaded. One orchestrator (`SKILL.md`, declares `orchestrator-routing` and `ratify-gate`) and one base coder (`coder.md`, declares `coding-general`). Every project starts here, even with no role pack.
- **Role pack** — stack-specific lens overlays and domains under `packs/<name>/`, loaded only when a project's `corpora/config.md` declares `role-pack: <name>`. The only pack here is `web-frontend` (coder overlay, UX designer, UI designer; coding + design domains).

A pack adds **depth to existing roles** — more domains on a lens's declaration — not new roles. There is one coder, one UX designer, one UI designer per project. Roles split into scoped instances only when the retrospective surfaces a fork signal (a domain whose conditions partition the space and give opposing advice), never from an org chart.

**Domains (where judgment lives):**

- **Seed domain** — general principles, in `domains/` (kernel) and `packs/<pack>/domains/` (pack).
- **Project domain** — project-specific accumulated judgment at `corpora/domains/<domain>.md` in the target project. Never merged back here without abstraction.

For each domain a lens declares, both apply when the role runs — seed first, then the same-named project domain. A project may also have domains with no seed counterpart (project-specific subjects, e.g. `spatial-metaphor`).

**Two load modes** (file granularity matches load granularity):

- **Working load** — a role's declared domains, *working files only* (`domains/<domain>.md`). Selective and inspectable; this is every new isolated role agent and inline role segment.
- **Audit load** — the orchestrator reads domains broadly *including* `domains/audit.md` (provenance, promotions, kills) at ratify and retrospective time only.

**Role contexts.** Each role receives its complete lens plus every domain it declares, and nothing from another lens or an undeclared domain. The orchestrator decides whether to run inline, resume the role agent owning the workstream, or start an isolated agent. Handoffs are checkpoints; operator testing and revisions return to the owning agent. See `SKILL.md`, "Inline, resume, or isolate," and LINEAGE.md, "Role isolation."

## Files

- `SKILL.md` — the shared orchestrator entrypoint for Claude Code (`/corpora`) and Codex (`$corpora`): routes workstreams, assembles complete role loads, relays handoffs, and drives the ratify gate.
- `coder.md` — base coder lens. Declares `coding-general`. Loaded for every project.
- `kernel.md` — the schema, lens+declaration model, ratify gate, write-back format, two load modes, retrospective signals, and role lifecycle. Reference document.
- `domains/` — kernel-seed domains: `coding-general.md`, `orchestrator-routing.md`, `ratify-gate.md`, `planning.md`, plus `audit.md` (provenance/promoted/kill detail for the layer, loaded only at ratify/retrospective time).
- `packs/web-frontend/` — the web-frontend pack: lens overlays (`coder.md`, `ux-designer.md`, `ui-designer.md`) and `domains/` (stack-specific coding + design domains, plus the layer `audit.md`). Loaded only when `role-pack: web-frontend`.
- `bootstrap.md` — one-time project setup. Phase 1 detects project shape and writes `corpora/config.md`. Phases 2 and 3 (UI projects only) generate `corpora/ui-library.md` (UI designer) then `corpora/ux-library.md` (UX designer) and propose seed design principles.
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

1. Invoke corpora on an unbootstrapped project. The orchestrator detects that `corpora/config.md` is absent and runs bootstrap: Phase 1 writes stable project shape, commands, and registered utilities; UI projects then route UI and UX bootstrap workstreams for their libraries.
2. On subsequent invocations, the orchestrator routes work inline, to an existing workstream agent, or to a new isolated role agent. A plan starts a new coder workstream; testing feedback and revisions return to its owning coder.
3. Handoffs surface proposals, violations, utility candidates, and other routing material. The operator ratifies corpus and direction changes.
4. `corpora/domains/<domain>.md` holds project-specific principles. The orchestrator creates a domain file on first ratification into it and assigns every ratified proposal a domain at the gate.

**Project files** (all under `corpora/` in the target project):

- `config.md` — stable project shape, registered deterministic utilities, library paths, and verification commands
- `ui-library.md` — design system documentation (generated by bootstrap, updated by designers)
- `ux-library.md` — experience patterns and flow documentation for UI projects
- `deferred-decisions.md` — non-blocking UI/UX questions waiting for a coherent designer workstream
- `utility-candidates.md` — persistent accepted, denied, and deferred utility observations
- `handoffs/` — unratified role checkpoints and their pending gate material
- `domains/<domain>.md` — per-domain accumulated judgment (working fields only)
- `domains/audit.md` — provenance, promotions, and per-kill detail for the project layer

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

## New stacks and role splitting

**New stack:** the kernel applies unchanged — every new project inherits the orchestrator and base coder for free. Add a role pack only when a body of stack-specific conventions has accumulated and is worth shipping across projects of that stack. Until then, project-earned specifics live in `corpora/domains/coding-general.md` (and project-specific domains). Do not pre-build packs speculatively.

**Domain and role splitting:** new judgment lands in the domain it's about (a new domain is born at the ratify gate when nothing fits). A *role* splits into scoped instances only when a domain it declares develops a genuine fork signal — conditions that partition the space and give opposing advice. Reach for this only when accumulated tension reveals the seam, not from an org chart.
