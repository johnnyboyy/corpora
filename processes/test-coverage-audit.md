---
name: corpora:test-coverage-audit
description: Assess how well the test suite covers the application's actual, observable behavior. Produces a list of gaps, not tests — see processes/integration-test-implementation.md for execution. Composition is ordinary implement-feature — the judgment is domains/testing.md.
---

# Test coverage audit

**Trigger:** either (a) the operator explicitly requests an assessment of how well the test suite
covers the application's actual behavior, or (b) a runtime-verification or debugging pass surfaces
that a real, user-facing bug shipped with no test that would have caught it. Does not fire on
routine test-writing alongside a feature — that's `processes/test-writing-at-implementation.md`'s concern.

**Composition:** same as `implement-feature` — no separate spawn, no separate unit-of-work. Judging
whether a given path is adequately covered, and what test shape would close a gap, is the same
`testing`-domain judgment as any other coding work; this phase supplies the *when* and the
*comparison target* (the app's real behavior), not new judgment of its own.

---

## Procedure

1. Inventory the existing test suite by the layer it actually exercises (pure logic vs. the
   interactive/rendered layer), not by file location or test-runner category —
   `domains/testing.md`'s `coverage-audit-by-layer-and-real-paths-not-location`.
2. Enumerate the application's real user-facing paths — the things a user or caller actually does —
   and check each against the inventory: is this path exercised by any test that would fail if the
   path broke?
3. For every gap found, name the specific behavior, cite whether this project has already shipped a
   bug on that path (a concrete, dated instance is stronger evidence than a hypothetical), and
   propose a test shape per `test-shape-matches-what-a-lower-level-test-cannot-reproduce`.
4. Do not write the tests in this phase — an audit that also implements blurs "what's missing" with
   "here's the fix" and skips the operator's own prioritization of which gaps matter most. Hand the
   list to `processes/integration-test-implementation.md`.

**Surfaced:** any path where the risk/value judgment was ambiguous (worth covering now vs.
deferring), and any infrastructure gap discovered that would block writing the candidate tests
(no browser-automation test runner wired in, no component-test harness) — named explicitly rather
than assumed away.
