---
name: corpora:architecture-scan
description: Proactively scan a managed project's codebase for architecture-deepening opportunities and surface them to the operator, agent-legible rather than visual. Run on operator command (architecture-scan [target]), never automatic.
---

# Architecture scan

**Trigger:** operator command, `architecture-scan [target]` (target is an optional module,
subsystem, or pain point). Never runs automatically — there is no mechanical trigger for it, the
same non-automatic posture `processes/retrospective.md` takes for scanning corpora's own corpus, applied
here to a scan of the target project's actual code (`domains/architecture-health.md`,
`ah-03`'s decision).

**Composition:** load `domains/architecture-health.md` (this process's own judgment) —
`corpus.py select --unit-of-work scan-architecture`, same as any other unit of work. Describe
candidates using deep-module vocabulary — module, interface, depth, seam, adapter, leverage,
locality — informally; corpora has no domain of its own for these terms yet (`domains/architecture-health.md`'s
preamble, `nys-01` in the queue that scoped this capability). Read `CONTEXT.md` (if it exists) for
domain vocabulary and any ADRs in scope before exploring.

## Procedure

1. **Scope.** If the operator named a target, scope the scan to it. Otherwise apply
   `domains/architecture-health.md`'s `scan-scope-by-recent-churn`: walk `git log --oneline` for a
   good stretch of history to find hot spots, and let those paths pull attention first. Widen the
   net if changes are too scattered to show a hot spot.

2. **Explore.** Use the Agent tool with `subagent_type=Explore` to walk the scoped codebase. Note
   friction: modules whose interface is nearly as complex as their implementation, concepts that
   require bouncing between many small modules to understand, tightly-coupled modules leaking
   across their seams, code that's hard to test through its current interface. Apply the deletion
   test — would deleting the module concentrate its complexity elsewhere, or just move it — to
   anything suspected shallow.

3. **Screen ADR conflicts.** For any candidate whose recommended change contradicts an existing
   ADR, apply `domains/architecture-health.md`'s `dont-relitigate-adr-without-real-friction` —
   include it only if the friction motivating it is real and specific, and mark the conflict
   explicitly when included.

4. **Write the report.** A plain-text file, saved to `corpora/architecture-scans/<date>-<slug>.md`
   (create the directory if absent). Agent-legible, not a visual artifact — one section per
   candidate:

   ```markdown
   ## <candidate name>

   **Files:** which files/modules are involved
   **Problem:** why the current shape is causing friction, in deep-module vocabulary (module,
   interface, depth, seam, adapter, leverage, locality)
   **Solution:** what would change, in plain English
   **Benefits:** in terms of leverage and locality, and how tests would improve
   **Tradeoffs/concerns:** cost, risk, or open questions this candidate raises
   **Recommendation strength:** Strong | Worth exploring | Speculative
   **ADR conflict:** only present if step 3 applies — which ADR, and the friction justifying reopening it
   ```

   End the report with a **Top recommendation** section: which candidate to tackle first and why.

5. **Surface to the operator.** Relay the full report verbatim (`kernel.md`'s "Surfaced" convention
   — never summarized or filtered). Offer, per candidate, to hand it to the planner as a fresh
   capability description (`processes/bootstrap.md`'s pattern for a feature request found at bootstrap
   time) — do not invoke the planner automatically. Stop and wait for the operator's choice: pursue
   a candidate (naming which), or take no action. A scan that surfaces nothing actionable is a
   valid outcome — report that plainly rather than manufacturing a weak candidate to fill the report.
