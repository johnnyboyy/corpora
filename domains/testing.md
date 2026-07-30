---
subject: coding
posture: guardrail
units-of-work: [implement-feature]
universal: false
---

# Domain: testing

Judgment about what's worth testing, at what layer, and what "verified" actually requires —
distinct from `coding-general`/stack-specific coding domains' implementation judgment. Seeded
2026-07-29 from a literal exercise run (`exercises/comment-section-process-vs-judgment.md`, Run 2)
that shipped two real runtime bugs — a stale RSC payload after a Server Action mutation, a
per-module-graph singleton split by Fast Refresh — with `tsc --noEmit` and `next build` passing
cleanly through both, caught only by driving the actual feature in a browser. Adapted from
`motors-and-controls/praxis/phases/`' testing-phase family into corpora's own process/judgment
split: this file is the judgment; `runtime-verification.md`, `test-writing-at-implementation.md`,
`integration-test-implementation.md`, and `test-coverage-audit.md` are the processes that apply it.
Audit metadata lives in `domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: none

principles:

- id: runtime-verification-required-not-static-checks-alone
  rule: "Passing lint/typecheck/build/test does not prove a code change with a runtime-observable surface actually works. Drive the real, rendered/running surface and observe the actual result before considering the work verified — never substitute re-running static checks or re-reading the diff."
  condition: "Any code change with a runtime-observable surface (not docs-only, types-only, or test-only) about to be reported complete — especially a refactor or consolidation pass that only reorganizes existing wiring (dependency reordering, hook consolidation, a mutation path rewired through a different call shape), which is exactly the class of change where static checks pass while the app breaks."
  reason: "Static checks verify shape and syntax, not behavior at runtime — a stale closure, a hook-execution-order change, a dropped dependency, or (the case that founded this principle) two independent module-graph instances of what should be one singleton are all invisible to typecheck/build/lint and only surface by actually exercising the path. The plausible alternative — trust green tooling as sufficient — was tried and failed twice in the same session that seeded this principle."

- id: probe-one-adversarial-case-beyond-happy-path
  rule: "When driving a real surface to verify a change, exercise at least one case beyond the primary intended flow — an error path, an edge input, a repeated action — not only the happy path."
  condition: "Any runtime verification pass on a change with a runtime-observable surface."
  reason: "The happy path is the path most likely to have already been exercised informally while building the feature. The adversarial/edge case is where an unverified assumption (an error state, a race, a boundary value) actually lives, and is disproportionately cheap to check while already driving the surface."

- id: feature-level-test-by-default
  rule: "Write tests for newly implemented user-facing behavior at the feature/end-to-end level by default — exercising the actual path a user or caller goes through, not the internal functions that implement it."
  condition: "A coder-composed spawn reaches its own terminal checkpoint on newly implemented user-facing behavior or a newly fixed bug."
  reason: "A feature-level test exercises the same integration points (routing, state wiring, the actual rendered/executed path) that a real usage would, and survives internal refactors that don't change observable behavior. A test written against internal functions instead couples to implementation shape that has no reason to stay fixed."

- id: unit-test-only-for-named-reasons
  rule: "Add a unit-level test only for one of two reasons, stated explicitly which applies: (a) it regresses a specific bug just found during this implementation pass, or (b) the logic is genuinely intricate pure computation where hitting every edge case through an end-to-end test would be slow and imprecise about which case broke. Never add unit tests as a general policy of covering every new function, argument, or branch touched."
  condition: "When deciding whether newly implemented logic needs a unit-level test in addition to (or instead of) feature-level coverage."
  reason: "A test that asserts on internal shape — an argument name, a helper's call signature, a mocked internal — raises the cost of the next harmless refactor without adding a proportionate signal. The two named exceptions are the cases where that cost is actually worth paying: a regression test pins down a real, previously-missed failure mode; intricate pure computation is genuinely hard to pinpoint a failing case for through an end-to-end test alone."
  see-also: feature-level-test-by-default

- id: test-shape-matches-what-a-lower-level-test-cannot-reproduce
  rule: "Choose a real, rendered/running-environment test for interactive-layer behavior that a lower-level or mocked test environment (a virtual DOM, a stubbed runtime) cannot faithfully reproduce — framework-internal registries, real layout/resize/focus behavior, an actual network or module-boundary interaction. Choose a component- or unit-level test only for logic genuinely reachable and representative without that real environment."
  condition: "When deciding what layer/shape of test to write for new behavior or to close a named coverage gap."
  reason: "A mocked or lower-level test environment approximates the real one; the approximation is exact for pure logic and unreliable for anything that depends on the real runtime's actual behavior. Choosing the lower-level shape for that second category produces a test that can pass while the real path is broken — the same failure mode `runtime-verification-required-not-static-checks-alone` names for verification, applied to test authoring itself."
  see-also: runtime-verification-required-not-static-checks-alone

- id: coverage-audit-by-layer-and-real-paths-not-location
  rule: "When assessing how well a test suite covers the application's actual behavior, inventory by the layer each test actually exercises (pure logic vs. the interactive/rendered layer) and check that against the real user-facing paths a person or caller actually takes — not by file location or test-runner category. Cite a concrete, dated instance of this project already having shipped a bug on a given path as stronger risk evidence than a hypothetical when prioritizing which gaps matter."
  condition: "When explicitly assessing test coverage (not routine test-writing alongside a feature, which `feature-level-test-by-default` already covers)."
  reason: "File location and test-runner category describe how tests are organized, not what they actually verify — two files in the same 'unit tests' folder can be exercising completely different layers of confidence. A dated, concrete prior incident is falsifiable evidence a hypothetical risk assessment isn't, and keeps prioritization from defaulting to whichever gap is easiest to imagine rather than the one that has actually bitten this project."

killed:
```
