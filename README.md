# corpora

### A system for accumulating learned judgment across agent sessions and projects

Instead of an agent re-deriving the same correction every session, or a project's conventions living
only in one person's head, judgment gets written down once, weighed against new cases, and kept or
killed based on whether it actually holds up.

## Why this exists (I wrote this)

AI agents, really Claude Code in particular, is a new kind of tool. I felt I needed to learn how to
use it as much as it needed work to be geat. This is a colleciton (probably not exhaustive) of all
those lessons I've learned along the way. Including the ones Claude Code taught me about my own
rules and principles from my time as a software engineer.

- **Reason and condition over hard instructions.** This grew from having hard instrstructions to
  force my own rules onto Claude Code. I had very good reasons for it, but I couldn't be sure they
  were *the best rules ever*. It would struggle to follow them anyways; or over apply them. Until
  one day I asked it why it was doing what it was doing. I dont't remember the answer. The point was
  I broke down each rule with it's reason, and it said the reason was doing much more work than the
  rule on it's own. Not only that, it was able to find a meta-principle that all my rules were
  pointing towards: The Reader Tax (Explicit by Default). It taught me something new and interesting
  about my own thinking. I wanted it to do that more, and that's when this project started.
- **Some Agents hate to read.** (Codex). I could not get Codex to cooperate with the system. The
  whole *full corpus on spawn* thing was meant to be a guard against pointing to a file and hoping
  that the agent would not just skim it or skip it altogether. If it was in the spawn prompt, it
  was at least guaranteed to be in the context. But even then it seemed to be skimming or ignoring
  the reading. I wasn't able to get it to use the rules the way Claude Code does.
- **Convergent vs. divergent stance.** I noticed that doing design work followed by implementation
  in the same context window was incredibly painful. It's married to the design it creates, and the
  "stances" as I've taken to calling them (Claude's name) do NOT mix well. Convergent is correctness.
  You want your code to be correct. Divergent is creative. You do not want your code to be creative.
- **Overstuffed context.** You can notice it when Claude Code starts answering in long, drawn out
  responses. I assume this is it's way of trying to keep attention on the current ask, and the sheer
  size of the context before it means it needs a lot more bulk just to stay on track. This also means
  that principles loaded will get less notice, and not be followed. So there's a principle that watches
  for these symptoms, suggest the agent find a good place to stop work, and ask for a fresh spawn to
  continue where it left off.
- **Making a script is a good option.** Codified in the `utility-candidates.md` mechanism. Anything
  you can move out of Inference into something Deterministic is a good thing. For one, you're saving
  tokens. But also, you're saving time and getting better results. This came from asking Claude Code
  to give me three colors from one - a warmer and cooler variant. It was spinning like crazy on that
  task and the colors is made were awful. When probed, it said it had to "guess a warmer color, then
  check if it actually was," and essentially loop that until it thought it had something. A quick
  color utility script later and I had 9 full color scheme options for a 10th of the cost. And they
  didn't suck!
- **It can review it's own plan.** Typically, I ask it to make a high-level plan, and then do a pass
  for any gaps or improvements. It's never come back without something. That's codified in a planning
  principle.
- **Propose → ratify.** Claude does not always propse good things. Sometimes, it even does
  bad or ugly things. The Operator (you) is the standing guard against a bad corpus.
- **Rejections are kept, with their reason.** This might get cut or eventually moved fully to the
  auditing section. I've been told it's both useful and not useful, and I haven't had enough data
  to really tell. There's a new system in place to track how long they sit and if they matter in a
  task. After so many sessions, they move out to the audit anyways. If that's the consistent pattern,
  then that can become the default.

If you don't want to take the system as a whole, I hope you can at least take something from these
lessons. I've always wanted to meaningfully contribute something to the field of software. I hope
this can go at least a small way towards that.

## The system (Everything below is Claude Code)

Judgment lives in **domains** — corpora scoped to one subject matter or decision class. A
**spawn** is a *stance* (convergent or divergent — `kernel.md`, "Generative stance") plus whatever
domain subset the orchestrator composes fresh for the task at hand, stated directly in a spawn
brief every time. The shared mechanism — schema, ratify gate, retrospective — is the **kernel**.
Seed domains carry general principles earned from real work; a project adds its own same-named
domains. Principles ratified in a project can promote upward to the seed domain when they
generalize across projects, or fold into a domain's own preamble once they've stabilized into
scene-setting that no longer needs per-task condition-checking. Rejected principles are kept with
their reason and a `kill_type`. Kernel and seed domains travel in this repo; project domains stay
in the project.

Domains own corpora, so shared judgment lives once and is available to any spawn whose stance and
subject match (a divergent UI-composed spawn and a convergent UX-composed spawn both load
`recoverability`, for example, without either one "owning" it). Domain boundaries are discovered
from accumulated tension — the fork signal in the retrospective.

### Architecture

**One flat domain pool, one fixed process layer:**

- **The orchestrator** (`SKILL.md`, declares `orchestrator-routing`, `ratify-gate`, and
  `principle-judgment`) is the one fixed thing: a process layer that composes and routes spawns
  without taking on a spawn's stance itself, so something occupies that position before any
  composition can happen. The **planner** composes `planning` + `interviewing` like any other
  spawn, decided fresh by routing judgment. Every working spawn composes from `coding-general` at
  minimum.
- **Domains** — stack-agnostic (`coding-general`, `orchestrator-routing`, `spawn-integrity`, ...)
  and stack-specific (`coding-react`, `css`, `color`, ...) domains live together in one flat
  `domains/`. Each stack-specific domain states its own load condition directly against
  `corpora/config.md`'s shape fields (`language`, `framework`, `styling`, `has-ui`) in its own
  preamble.

The orchestrator states a stance and domain subset directly in the spawn brief for every task.
`coder`, `ux-design`, `ui-design`, and `planner` name recurring task shapes in prose (see
`LINEAGE.md` for history). One composed spawn per recurring task shape runs at a time per project;
a domain splits into scoped instances when the retrospective surfaces a fork signal — conditions
that partition the space and give opposing advice.

**Domains (where judgment lives):**

- **Seed domain** — general principles, in the skill's flat `domains/`.
- **Project domain** — project-specific accumulated judgment at `corpora/domains/<domain>.md` in
  the target project. Merges back here once it generalizes beyond the project's specifics.

For each domain a spawn's composition includes, both apply when it runs — seed first, then the
same-named project domain. A project may also have domains with no seed counterpart
(project-specific subjects, e.g. `spatial-metaphor`).

**Two load modes** (file granularity matches load granularity):

- **Working load** — a spawn's composed domains, *working files only* (`domains/<domain>.md`).
  Selective and inspectable; this is every new isolated spawn and inline segment.
- **Audit load** — the orchestrator reads domains broadly *including* `domains/audit.md`
  (provenance, kills) at ratify and retrospective time.

**Spawn contexts.** Each spawn receives its stance frame plus every composed domain. The
orchestrator decides whether to run inline, resume the agent owning the workstream, or start an
isolated agent. Handoffs are checkpoints; operator testing and revisions return to the owning
agent. See `SKILL.md`, "Inline, resume, or isolate," and `LINEAGE.md`, "Role isolation."

### Files

- `SKILL.md` — the shared orchestrator entrypoint for Claude Code (`/corpora`) and Codex
  (`$corpora`): routes workstreams, assembles complete spawn loads, relays handoffs, and drives the
  ratify gate.
- `kernel.md` — the schema, stance+composition model, ratify gate, write-back format, two load
  modes, retrospective signals, and domain lifecycle. Reference document.
- `domains/` — every seed domain, flat: stack-agnostic (`coding-general.md`,
  `orchestrator-routing.md`, `ratify-gate.md`, `principle-judgment.md`, `planning.md`,
  `interviewing.md`, `spawn-integrity.md`) and stack-specific (`coding-ts.md`, `coding-react.md`,
  `coding-nextjs.md`, `css.md`, and the design domains `color.md`/`motion.md`/`recoverability.md`/
  etc.) alike, each stating its own load condition in its own preamble. Plus `audit.md`
  (provenance/kill detail for the layer, loaded only at ratify/retrospective time).
- `bootstrap.md` — one-time project setup. Phase 1 detects project shape and writes
  `corpora/config.md`. Phases 2 and 3 (UI projects only) generate `corpora/ui-library.md`
  (divergent) then `corpora/ux-library.md` (convergent) and propose seed design principles.
- `LINEAGE.md` — intellectual history: why conventions became law, key kills, design decisions.
- `reader-tax-and-the-model.md` — a living, multi-model assessment of whether Explicit by Default
  helps the model itself, not only the human reviewer.

### Installation

Clone this repository once, then symlink the same working copy into either or both skill directories:

```bash
ln -s /absolute/path/to/corpora ~/.claude/skills/corpora
ln -s /absolute/path/to/corpora ~/.codex/skills/corpora
```

Claude Code invokes it as `/corpora`. Codex invokes it as `$corpora` and may also activate it
implicitly. A managed project's `AGENTS.md` can opt into automatic Codex activation with the
one-line instruction offered by the skill.

**Diverging from the shared skill.** A project that wants its own frozen copy of the seed domains,
deliberately not tracking future changes to this repo, copies it instead of symlinking. That's a
whole-skill decision made once, at install time; re-copy later to pick up upstream changes on your
own schedule. A project's own `corpora/domains/<domain>.md` always merges with the seed by
concatenation, live — there's no per-domain opt-out (`kernel.md`, "Project corpora").

### Using in a project

1. Invoke corpora on an unbootstrapped project. The orchestrator detects that `corpora/config.md`
   is absent and runs bootstrap: Phase 1 writes stable project shape, commands, and registered
   utilities; UI projects then route divergent- and convergent-composed bootstrap workstreams for
   their libraries.
2. On subsequent invocations, the orchestrator routes work inline, to an existing workstream agent,
   or to a new isolated spawn. A plan starts a new coder-composed workstream; testing feedback and
   revisions return to its owning agent.
3. Handoffs surface proposals, violations, utility candidates, and other routing material. The
   operator ratifies corpus and direction changes.
4. `corpora/domains/<domain>.md` holds project-specific principles. The orchestrator creates a
   domain file on first ratification into it and assigns every ratified proposal a domain at the
   gate.

**Project files** (all under `corpora/` in the target project):

- `config.md` — stable project shape, registered deterministic utilities, library paths, and
  verification commands
- `ui-library.md` — design system documentation (generated by bootstrap, updated by designers)
- `ux-library.md` — experience patterns and flow documentation for UI projects
- `deferred-decisions.md` — non-blocking UI/UX questions waiting for a coherent designer workstream
- `utility-candidates.md` — persistent accepted, denied, and deferred utility observations
- `handoffs/` — unratified spawn checkpoints and their pending gate material
- `domains/<domain>.md` — per-domain accumulated judgment (working fields only)
- `domains/audit.md` — provenance and per-kill detail for the project layer

See `kernel.md` for the full principle schema and write-back format.

### Validation

Run the dependency-free regression suite with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

### Cross-project learning

When a principle in a project domain is general — its condition doesn't reference the project's
stack or specifics — it's a candidate for promotion to the seed domain of the same name here. The
project domain is where principles are earned; this repo is where they graduate.

The retrospective is the natural trigger: when a project-level principle has held across enough
tasks that it reads as general, the retrospective surfaces it as a seed promotion candidate. The
exact process for that promotion is not yet spelled out.

### New stacks and domain splitting

**New stack:** the kernel applies unchanged — every new project inherits the orchestrator, the
planner, and `coding-general` for free. Add stack-specific seed domains (with their own load
conditions against `language`/`framework`/`styling`) once a body of stack-specific conventions has
accumulated and is worth shipping across projects of that stack. Until then, project-earned
specifics live in `corpora/domains/coding-general.md` (and project-specific domains). Do not
pre-build stack-specific domains speculatively.

**Domain splitting:** new judgment lands in the domain it's about (a new domain is born at the
ratify gate when nothing fits, after clearing the genuine-fork test — see `kernel.md`, "The
genuine-fork test"). A domain splits into scoped instances when it develops a genuine fork signal —
conditions that partition the space and give opposing advice. Reach for this when accumulated
tension reveals the seam.

## License

MIT — see `LICENSE`.
