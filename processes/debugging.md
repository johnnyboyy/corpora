---
name: corpora:debugging
description: The four-phase sequence for investigating a bug, test failure, or unexpected behavior before proposing a fix. Mechanical — no composition, no stance; the judgment behind each phase lives in domains/debugging.md.
---

# Debugging

**Trigger:** any bug, test failure, or unexpected behavior, before proposing or applying a fix —
part of `debug-issue`'s own composition, not a separate opt-in step.

**No composition, no stance of its own.** The sequencing here is mechanical; the judgment at each
phase is in `domains/debugging.md`, already loaded as part of the spawn's `debug-issue`
composition. This file is the procedure, not a second spawn.

---

## Procedure

1. **Root cause investigation.** Reproduce the issue, read the full error/stack trace, check what
   recently changed, and — for a multi-component system — gather evidence at each component
   boundary before investigating any single component in depth. See
   `root-cause-before-fix`.

2. **Pattern analysis.** Find a working example similar to the broken case; if a reference
   implementation exists, read it in full and enumerate every difference rather than adapting a
   skimmed pattern. See `compare-against-complete-reference`.

3. **Hypothesis and testing.** State one specific hypothesis, make the smallest change that tests
   it, and verify before continuing. A failed test reforms the hypothesis rather than stacking a
   second change on the unresolved first. After three failed attempts sharing a pattern, stop and
   raise whether the architecture itself is sound instead of attempting a fourth fix. See
   `single-hypothesis-minimal-test-reform-on-failure`, `repeated-fix-failure-questions-architecture`.

4. **Implementation.** Create the smallest failing test (or one-off reproduction) before writing
   the fix. Implement the fix at the root cause, not the symptom. Once fixed, validate at every
   layer the bad data or state actually passes through, not only the one checkpoint the fix
   touches. Verify the fix resolves the issue without breaking other tests. See
   `reproduce-as-failing-test-before-fixing`, `fix-at-source-not-symptom`,
   `validate-at-every-layer-after-root-cause`.

**If at any point the actual cause isn't clear**, say so explicitly rather than proceeding on a
plausible-sounding guess — see `state-uncertainty-instead-of-plausible-guess`.

Report what was actually investigated and found in the handoff's `Artifact` section — the
hypothesis tested, the evidence, the fix and where it lands in the call chain — not just a
pass/fail verdict.
