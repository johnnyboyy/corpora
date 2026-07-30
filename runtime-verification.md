---
name: corpora:runtime-verification
description: Drive a real, running surface and observe the actual result before a coder-composed spawn's handoff with runtime-observable output can be considered complete. Mechanical — no composition, no stance; the judgment behind it lives in domains/testing.md.
---

# Runtime verification

**Trigger:** required, not suggested — a coder-composed spawn's work includes a
runtime-observable surface (not docs-only, types-only, or test-only) and is about to reach its own
terminal checkpoint (`general-operation.md`, Phase 4). This is part of what "the spawn's work is
done" means, the same way `kernel.md`'s "before writing it, re-read the output against the
composed domains" is — not a separate opt-in step.

**No composition, no stance.** Driving the app and observing what happens needs no design or code
judgment of its own — the judgment is in `domains/testing.md`
(`runtime-verification-required-not-static-checks-alone`,
`probe-one-adversarial-case-beyond-happy-path`), already loaded as part of the spawn's own
`implement-feature` composition. This file is the procedure, not a second spawn.

---

## Procedure

1. Use this project's `verify` skill (or a project-specific verifier under `.claude/skills/`) if
   one exists; otherwise drive the surface directly with whatever tooling the project actually has
   (a dev server plus browser automation, a CLI invocation, an HTTP call).
2. Drive the real surface — not import-and-call, not re-running tests or typecheck. For a change
   that only reorganizes existing wiring (a refactor, a hook consolidation, a mutation rewired
   through a different call shape), specifically exercise every interaction path whose call site or
   dependency ordering changed, not only the path that was the nominal point of the change.
3. Probe at least one adversarial or edge case beyond the happy path.
4. Report what was actually observed in the handoff's `Artifact` section, not just a pass/fail
   verdict — the steps taken and what happened at each one.

**If no way to drive the real surface is available this session** (no browser automation, no
reachable runtime), say so explicitly in the handoff's `Surfaced` section rather than silently
reporting the work complete on tooling alone — this is the same disclosure discipline
`screenshot-library-init.md`/`screenshot-library-sync.md` already use when no browser tool is
available for their own mechanical work.
