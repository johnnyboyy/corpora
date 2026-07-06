# corpora

A system for accumulating learned judgment across agent sessions and projects. Judgment lives in **domains**, not roles — roles are lenses that declare which domains they load, so shared judgment is written once and never duplicated across role files.

The mechanics: judgment lives in **domains** (corpora scoped to a subject matter or decision class), and a **role** is a *lens* (a domain prompt) plus a static declaration of the domains it loads. The shared mechanism — schema, ratify gate, retrospective — is the **kernel**. Seed domains carry general principles earned from real work; a project adds its own same-named domains. Principles ratified in a project can promote upward — to the seed domain when they generalize across projects, to the lens prompt itself when they stabilize into defaults. Rejected principles are kept with their reason and a `kill_type` — the kill log is often more instructive than the ratified list. Kernel, lenses, and seed domains travel in this repo; project domains stay in the project.

Domains, not roles, own corpora — so shared judgment lives once and is declared by every lens that needs it (the UI and UX designers both declare `recoverability`, for example). Domain boundaries are discovered from accumulated tension (the fork signal in the retrospective), never declared up front from an org chart.

## Architecture

**Two layers of lenses:**

- **Kernel** — stack-agnostic, always loaded. One orchestrator (`skill.md`, declares `orchestrator-routing`) and one base coder (`coder.md`, declares `coding-general`). Every project starts here, even with no role pack.
- **Role pack** — stack-specific lens overlays and domains under `packs/<name>/`, loaded only when a project's `corpora/config.md` declares `role-pack: <name>`. The only pack here is `web-frontend` (coder overlay, UX designer, UI designer; coding + design domains).

A pack adds **depth to existing roles** — more domains on a lens's declaration — not new roles. There is one coder, one UX designer, one UI designer per project. Roles split into scoped instances only when the retrospective surfaces a fork signal (a domain whose conditions partition the space and give opposing advice), never from an org chart.

**Domains (where judgment lives):**

- **Seed domain** — general principles, in `domains/` (kernel) and `packs/<pack>/domains/` (pack).
- **Project domain** — project-specific accumulated judgment at `corpora/domains/<domain>.md` in the target project. Never merged back here without abstraction.

For each domain a lens declares, both apply when the role runs — seed first, then the same-named project domain. A project may also have domains with no seed counterpart (project-specific subjects, e.g. `spatial-metaphor`).

**Two load modes** (file granularity matches load granularity):

- **Working load** — a role's declared domains, *working files only* (`domains/<domain>.md`). Selective and contamination-safe; this is every spawn and inline session.
- **Audit load** — the orchestrator reads domains broadly *including* `domains/audit.md` (provenance, promotions, kills) at ratify and retrospective time only.

**Role isolation.** Each role runs in its own context: its lens plus the domains it declares, and nothing from another lens or an undeclared domain. The coder declares coding domains and never design domains, so design context cannot bleed into coding. Two *design* lenses sharing a design domain is allowed and intended. Designers always spawn into a fresh context; the coder runs inline. See LINEAGE.md, "Role isolation."

## Files

- `skill.md` — the orchestrator lens: routes tasks, spawns designers, drives the ratify gate (incl. domain assignment). Entry point for the Claude Code skill system (`/corpora`).
- `coder.md` — base coder lens. Declares `coding-general`. Loaded for every project.
- `reviewer.md` — base reviewer lens. Declares `coding-general`. Invoked at operator-defined checkpoints (commit diff, explicit audit) to evaluate code against principles and meta-rules. Surfaces violations of existing principles and proposes new ones. Spawn when session holds prior coder work; inline when context is clean.
- `kernel.md` — the schema, lens+declaration model, ratify gate, write-back format, two load modes, retrospective signals, and role lifecycle. Reference document.
- `domains/` — kernel-seed domains: `coding-general.md`, `orchestrator-routing.md`, plus `audit.md` (provenance/promoted/kill detail for the layer, loaded only at ratify/retrospective time).
- `packs/web-frontend/` — the web-frontend pack: lens overlays (`coder.md`, `reviewer.md`, `ux-designer.md`, `ui-designer.md`) and `domains/` (stack-specific coding + design domains, plus the layer `audit.md`). Loaded only when `role-pack: web-frontend`.
- `bootstrap.md` — one-time project setup. Phase 1 detects project shape and writes `corpora/config.md`. Phases 2 and 3 (UI projects only) generate `corpora/ui-library.md` (UI designer) then `corpora/ux-library.md` (UX designer) and propose seed design principles.
- `LINEAGE.md` — intellectual history: why conventions became law, key kills, design decisions.
- `reader-tax-and-the-model.md` — a living, multi-model assessment of whether Explicit by Default helps the model itself, not only the human reviewer.

## Using in a project

1. Symlink or clone into `~/.claude/skills/corpora` to install as a Claude Code skill.
2. Invoke `/corpora` on an unbootstrapped project. The orchestrator detects that `corpora/config.md` is absent and runs bootstrap automatically — Phase 1 inline (detects project shape, writes `corpora/config.md`), then if `has-ui: yes`, Phase 2 spawns the UI designer (`corpora/ui-library.md`) and Phase 3 spawns the UX designer (`corpora/ux-library.md`), each proposing seed design principles.
3. On any subsequent invocation, `/corpora` enters orchestrator mode. The orchestrator routes tasks, runs inline coder work, spawns designers when needed, and drives the ratify gate after any session that produces ratifiable decisions.
4. `corpora/domains/<domain>.md` in the project holds project-specific principles. The orchestrator creates a domain file on first ratification into it, and assigns each proposal a domain at the gate.

**Project files** (all under `corpora/` in the target project):

- `config.md` — project shape and tool surface, read by every role at session start (generated by bootstrap)
- `ui-library.md` — design system documentation (generated by bootstrap, updated by designers)
- `domains/<domain>.md` — per-domain accumulated judgment (working fields only)
- `domains/audit.md` — provenance, promotions, and per-kill detail for the project layer

See `kernel.md` for the full principle schema and write-back format.

## Cross-project learning

When a principle in a project domain is general — its condition doesn't reference the project's stack or specifics — it's a candidate for promotion to the seed domain of the same name here. The project domain is where principles are earned; this repo is where they graduate.

The retrospective is the natural trigger: when a project-level principle has held across enough tasks that it reads as general rather than project-specific, the retrospective surfaces it as a seed promotion candidate. The exact process for that promotion is not yet spelled out.

The seed domains here have been through a retrospective pass (2026-06-20): scoping misplaced principles, flagging single-project principles as provisional, and killing redundant entries. A provisional flag means the principle was earned in one project context and hasn't been stress-tested against a second.

## New stacks and role splitting

**New stack:** the kernel applies unchanged — every new project inherits the orchestrator and base coder for free. Add a role pack only when a body of stack-specific conventions has accumulated and is worth shipping across projects of that stack. Until then, project-earned specifics live in `corpora/domains/coding-general.md` (and project-specific domains). Do not pre-build packs speculatively.

**Domain and role splitting:** new judgment lands in the domain it's about (a new domain is born at the ratify gate when nothing fits). A *role* splits into scoped instances only when a domain it declares develops a genuine fork signal — conditions that partition the space and give opposing advice. Reach for this only when accumulated tension reveals the seam, not from an org chart.
