# corpora

A portable role-kernel system — a multi-role design+coding discipline that accumulates judgment
across projects without carrying project-specific assumptions along.

## How it works

**Two layers of corpus:**

- **Seed corpus** — general principles distilled from real project work. Lives in this repo,
  travels to every project. Lives inside `skill.md` alongside each role's prompt.
- **Project corpus** — project-specific accumulated judgment. Lives in the project at `corpora/<role>.md`.
  Extends the seed; never merged back here without abstraction.

Both layers are always applied when a role runs. The skill loads the seed; the orchestrator
reads the project corpus file and includes it in the role context.

## Files

- `skill.md` — the main skill. Orchestrator entry point with all roles embedded. Invoke via
  the Claude Code skill system. Pass a role name as an arg for direct role invocation.
- `kernel.md` — the schema, ratify gate, and write-back format. Reference document.

## Using in a project

1. Install this repo as a Claude Code plugin.
2. Invoke the skill: `/corpora` for orchestrator mode, or `/corpora coder` etc. for direct role entry.
3. The skill will look for `corpora/<role>.md` in the current project root.
4. Create that file (empty is fine) when the first project-specific principle is ratified.

## Project corpus format

`corpora/coder.md`, `corpora/orchestrator.md`, `corpora/ux-designer.md`, `corpora/ui-designer.md`

Each follows the schema in `kernel.md`:

```yaml
last-retrospective: YYYY-MM-DD

principles:

- id: principle-id
  rule: "The guidance."
  condition: "When this applies."
  reason: "Why."
  provenance: "Date, task, context."
  status: ratified

killed:
```

## Cross-project learning

When a principle in a project corpus proves general — its condition doesn't reference the
project's specific stack or domain — propose promoting it to the seed corpus here via a PR.
The project corpus is where principles are earned; this repo is where they graduate.

## Role splitting

For large projects that need domain-split roles (frontend/backend, or by feature area),
create additional corpus files: `corpora/frontend-coder.md`, `corpora/dashboard-ux.md`, etc.
The orchestrator loads the appropriate one based on the task being routed. No changes to
this skill are needed — the split lives entirely in the project.
