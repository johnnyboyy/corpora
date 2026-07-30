---
name: corpora:test-writing-at-implementation
description: Write a test for newly implemented user-facing behavior or a newly fixed bug, at the checkpoint a coder-composed spawn already reaches. Composition is ordinary implement-feature — the judgment is domains/testing.md, already part of that composition.
---

# Test writing at implementation

**Trigger:** a coder-composed spawn reaches its own terminal checkpoint on newly implemented
user-facing behavior or a newly fixed bug — proactive by default, not only when the operator asks
for tests, but conservative in what it adds (see `domains/testing.md`).

**Composition:** same as `implement-feature` — no separate spawn, no separate unit-of-work. The
`testing` domain is already part of that composition; this file names when its judgment applies
during ordinary coding work, not a new task shape.

---

## Procedure

1. For the behavior just implemented, write a test at the feature/end-to-end level by default —
   `domains/testing.md`'s `feature-level-test-by-default`.
2. Add a unit-level test only for one of the two reasons `unit-test-only-for-named-reasons` names,
   stated explicitly which one applies. Do not add unit tests as general proactive coverage.
3. Choose the test's shape (real-environment vs. component vs. unit) per
   `test-shape-matches-what-a-lower-level-test-cannot-reproduce`.
4. Run the project's verification commands before considering the checkpoint reached.

**Surfaced:** any behavior from this implementation pass that couldn't reasonably be tested at the
feature/end-to-end level with current infrastructure — name it rather than silently skipping it, so
it becomes a candidate for a future `processes/test-coverage-audit.md` pass instead of disappearing.
