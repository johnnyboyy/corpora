---
name: corpora:integration-test-implementation
description: Write and wire up the specific tests test-coverage-audit.md (or an explicit operator request) already identified. Composition is ordinary implement-feature — the judgment is domains/testing.md, already part of that composition.
---

# Integration test implementation

**Trigger:** `test-coverage-audit.md` (or an explicit operator request naming specific paths
directly) has identified concrete candidate paths to cover, and the task is now to write and wire
up those tests — not to identify more gaps.

**Composition:** same as `implement-feature` — no separate spawn, no separate unit-of-work.
Writing the test itself (fixture setup, assertions, any new test infrastructure) is ordinary coding
judgment once the target path is named.

---

## Procedure

1. For each candidate path from the audit, write a test that exercises it the way it's actually
   reached — a real rendered/running environment for anything the audit flagged as needing one, per
   `domains/testing.md`'s `test-shape-matches-what-a-lower-level-test-cannot-reproduce`, rather than
   substituting a lower-level test that wouldn't catch the same class of bug.
2. Stand up whatever infrastructure the chosen test shape needs (a browser-automation test runner,
   a component-rendering harness) if the project doesn't already have it — this is new
   infrastructure, not just new test files; a deterministic-shortcut-candidate-style judgment call
   about whether it's worth the addition, same care as any other dependency addition.
3. Run the full verification suite after each new test is added, not only at the end — a new test
   that passes by accident (asserting something trivially true) is caught fastest by checking it
   fails against the bug it's meant to guard, when that's feasible to reproduce.
4. Do not backfill unit tests for every function touched along the way — this phase implements the
   specific paths the audit named; broader proactive unit coverage is
   `test-writing-at-implementation.md`'s concern, scoped narrowly there.

**Surfaced:** any candidate path from the audit that turned out infeasible to test at its intended
layer (and why — flaky automation, no reliable way to reach the state, infrastructure out of scope
for this pass), and any flakiness observed in the new tests themselves.
