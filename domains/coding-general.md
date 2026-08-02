---
subject: coding
posture: guardrail
units-of-work: [implement-feature]
universal: false
---

# Domain: coding-general

Stack-agnostic coding judgment — applies in any language or framework, loaded by any
convergent coding spawn (always). Audit metadata lives in `domains/audit.md`, loaded only at
ratify/retrospective time.

Foundational, stable across every project shape this domain serves — held here in the preamble
rather than in `principles:`, since checking a `condition` and `reason` against these before every
task would be friction without benefit (provenance: `domains/audit.md`):

- **Explicit by Default** and **prefer the error-exposing form** are peer meta-conventions, both
  extending Crockford's heuristic ("if a feature is sometimes useful and sometimes dangerous and
  there is a better option, always use the better option"). Explicit by Default: don't make the
  reader reconstruct something you could have just stated — every shortcut bills a Reader Tax to
  whoever reads the code next. Error-exposing form: when two forms produce the same result but one
  has a silent failure mode, choose the form that exposes the error, even at the cost of verbosity.
  They overlap but neither subsumes the other — a verbose variable name satisfies Explicit by
  Default without touching error exposure; strict equality over loose equality is error-exposing
  without improving semantic recovery. When they conflict, error-exposing form wins: a silent
  failure leaves no signal anything went wrong, while a reader who has to reconstruct intent can at
  least see that something needs reconstructing.
- **No peer re-exports** — import from the authoritative module, not a peer that happens to
  re-export it. Barrel index files that explicitly aggregate a public surface are the only
  exception. Near-unconditional; needs no per-case condition-weighing.
- Keep scope tight: implement what was asked, nothing more. Before adding any new function, type,
  or abstraction, ask whether it needs to exist at all, whether the standard library covers it, and
  whether an already-installed dependency covers it — stop at the first rung that holds. When a
  task fits multiple framings, prefer the one with the smaller net addition; deletion is progress.
- Run the project's verification commands (lint, type-check, build — whatever `corpora/config.md`
  actually declares) before finishing.
- Report a `tradeoffs` block (design_element / cost / alternative / what_is_lost) for any spec or
  task where implementation cost clearly outweighs the value, rather than implementing or skipping
  silently.
- Design decisions (visual direction, layout, UX flows) are out of scope — flag them as a note to
  the orchestrator rather than deciding them.

```yaml
last-retrospective: 2026-06-20

principles:

- id: ask-before-architecture
  rule: "When a task involves a structural or DRY question with two reasonable approaches, name both and ask before implementing."
  condition: "When implementing a structural change where multiple approaches are plausible — class vs. function extraction, inline vs. extracted helper, etc."
  reason: "Architectural questions are cheap to clarify and expensive to implement wrong. One question saves a full round-trip correction and avoids a messy intermediate state the user has to redirect out of."

- id: verify-before-bulk-edit
  rule: "Before replace_all or any bulk find-and-replace, grep for all instances and read context around each match to confirm they are all conceptually equivalent."
  condition: "Whenever the same string or pattern appears in multiple places and a bulk replacement is tempting."
  reason: "Occurrences of the same string are not always the same thing. Bulk replacement without verification creates a syntactically correct but conceptually wrong intermediate state — worse than not having made the change."

- id: grep-subdirs-before-delete
  rule: "Before deleting a file flagged as a redundant duplicate, grep for all relative imports/references (including ../ and ../../ variants) across the entire directory subtree, not just sibling files."
  condition: "When deleting a file that other files in the same directory tree may reference via relative paths."
  reason: "Subdirectories have different relative path depths, so a grep limited to ./ will miss references in nested dirs. The build reveals them, but a wider grep at task start catches them in one pass."

- id: code-lives-at-consumer-level
  rule: "Code lives at the level of its narrowest consumer. Something used in one file stays in that file; something used in one module stays in that module. Once a second consumer appears, promote immediately — do not defer. Promote to the lowest common ancestor of its consumers, and place shared code beside the data type or concern it serves."
  condition: "When deciding where a function, type, or component should live — at initial placement and at the moment a second consumer appears."
  reason: "Premature extraction signals reuse that isn't real, obscures actual scope, and implies candidacy for import when it isn't. One module importing from another's internals creates a hidden peer dependency."

- id: generic-defers-to-consumer
  rule: "Generic components expose extension points (parameters, slots, options) and make no assumptions about their caller's context. Any concern specific to a particular use case belongs in the consumer that has that context."
  condition: "When building any reusable unit that will be composed into more specific ones. Test: could this serve two different contexts with different concerns? If yes, the generic must not bake in either."
  reason: "A generic unit's value is reusability across contexts. Every caller-specific assumption hardcoded into the generic narrows that reusability and hides the dependency from the call site."

- id: single-callsite-helper-scoped
  rule: "A function that computes a value and has exactly one callsite should not be extracted as a standalone function. Resolve it where it's used — as a local in the calling scope (preferred when the expression is long), or inlined directly when it's short."
  condition: "When a standalone helper has exactly one callsite. Does not apply to functions called from two or more places — those earn the extraction."
  reason: "A standalone function implies reuse. A single-callsite helper adds a named concept with no benefit. Keeping the resolution local is more honest about its scope."

- id: ceiling-comment-for-deliberate-shortcuts
  rule: "When deliberately accepting a known limitation — a naive algorithm, a linear scan, a global lock — mark it with one inline comment: the limitation and the specific condition under which upgrading becomes necessary. Form: `// [limitation]; upgrade to [alternative] when [condition]`. Treat that named condition as live, not archival: at the same structural-examination pass done before finishing (see structural-examination-at-working-checkpoint), check any ceiling comment in code touched this session against its condition, and upgrade or remove it if the condition now holds."
  condition: "When choosing a simpler or slower implementation that has a known ceiling on performance, correctness, or scalability; and, for existing ceiling comments, whenever the structural-examination checkpoint is reached in a session that touched the marked code."
  reason: "A silent shortcut looks like a gap. A ceiling comment distinguishes a deliberate tradeoff from an oversight and names the upgrade path so the next reader can act rather than guess. But a named condition with no scheduled re-check degrades to the same silent-drift risk as an unbounded comment — nobody proactively rereads old comments to test whether their condition has become true. Anchoring the re-check to the same checkpoint already used for other structural review gives the condition an actual chance to be evaluated instead of only sitting in prose indefinitely."
  see-also: tag-identity-dependencies-check-before-handoff

- id: two-approaches-then-decide
  rule: "When choosing between implementation approaches, evaluate at most two seriously. If still uncommitted after two, pick the simpler one and move forward. Re-deriving the same tradeoffs is not analysis — it's spinning."
  condition: "Any time an implementation decision has more than one plausible path and the first attempt was abandoned."
  reason: "Iteration is cheaper than deliberation past the second pass. The signal that more exploration is needed is new information, not re-examining the same constraints under a slightly different framing."

- id: unified-representation-no-type-leakage
  rule: "Internal type distinctions (draft vs. entry, current vs. historical, variant A vs. B) must not escape into the consumer's data model. A unit that maintains parallel state for two variants should merge them into one unified collection before returning; a storage design where one of N items is 'active' should use an index into a flat list, not a separate slot or key."
  condition: "When a unit returns parallel outputs that differ only by an internal type distinction, or when designing state/storage for any system where one of N items is active."
  reason: "Leaking the internal distinction forces every consumer to replicate the branching logic. The unit already owns the data; it should own the routing too."

- id: utility-over-guesswork
  rule: "When work is deterministic, precision-sensitive, or disproportionately expensive to solve by inference — color/LCH math, date and timezone arithmetic, geometric layout, hashing, unit conversion, and similar — use the project's registered utility for it if one exists. If none exists, propose one as a deterministic shortcut candidate in the handoff rather than solving it by inference every time."
  condition: "When a task requires computing or verifying a value where getting it right by inference is unreliable, slow, or has recurred across sessions — not for one-off trivial arithmetic. Color is the canonical case: perceptual variants, palette stops, opacity blends over a backdrop, or any case where color relationships need to be derived rather than chosen arbitrarily. In React Native specifically, CSS custom properties are unavailable to component props at runtime (tintColor, tabBarActiveTintColor, inline style.color, etc.) — reference values from a JS token module rather than hardcoding hex literals there."
  reason: "Color/LCH relationships are the case that founded this principle: guessing produces inaccurate results and burns many tokens iterating toward something correct, while a small script computes the exact answer for near-zero cost. The same logic applies to any deterministic or repeatedly-recurring computation — the operator can deny a weak candidate cheaply; grinding it out by inference every session cannot be undone."

- id: scripts-over-hand-editing-structured-data
  rule: "When generating or modifying structured data files at scale, write a script that produces the output rather than editing the files directly. The script is the artifact; the output file is its build product."
  condition: "When a task involves adding, transforming, or regenerating structured data files with more than a handful of entries."
  reason: "Hand-editing large structured files is token-expensive, error-prone, and produces an unreviewed intermediate state. A script is idempotent (safe to re-run), captures the generation logic for future modification, and is cheaper to correct than a partially-edited JSON file."

- id: no-single-char-names
  rule: "Never use single-character variable names. Name what the variable holds: `index` not `i`, `xCoord` not `x`, `error` not `e`. Exception: abbreviations whose meaning is fully determined by universal convention and carries no ambiguity (e.g. two-letter state codes)."
  condition: "When naming any variable, parameter, loop counter, catch binding, or destructured value — in any language."
  reason: "Single-character names force every reader to reconstruct what the variable holds from surrounding context — the Reader Tax on every read. The convention originated as a program-size constraint that no longer exists; the tradeoff that justified it is gone. Descriptive names also make bulk rename safe; a single-character name appears in unrelated contexts and cannot be safely replaced."

- id: sibling-config-over-consumer-branch
  rule: "When N siblings share the same shape — the same set of methods or properties, varying only in their values and logic — model them as an array of config records, each carrying its own logic as functions. The consumer maps over the array; it does not branch on index or type."
  condition: "When a consumer has or would have a switch/if-chain over sibling cases (steps, sections, tabs), and each case's logic is self-contained."
  reason: "A consumer switch grows linearly with siblings and must be updated in two places (the data and the branch) when a sibling is added or changed. A config record concentrates each sibling's identity and logic in one object; the consumer stays fixed. Adding a sibling is a single-site edit: append to the array."

- id: structural-examination-at-working-checkpoint
  rule: "Before finishing a working implementation, do a one-pass structural examination. Look for: (1) implicit coupling via stringly-typed contracts — magic keys, selector strings, attribute names — standing in for an explicit interface, (2) thin wrappers whose only job is bundling two things with no identity of their own, (3) logic blocks with a clear purpose but no explicit name — candidates for extraction into a named function, (4) emergent groupings — types and functions that belong together but ended up separated during implementation."
  condition: "After any multi-file or multi-unit implementation reaches a working state (feature correct, checks passing) — at your own terminal checkpoint, immediately before considering the work done."
  reason: "Running code reveals structural seams planning can't predict — what talks to what, and via what contract. Thin wrappers and implicit stringly-typed contracts are especially invisible at design time; they emerge from solving the problem, not from designing the solution. Anchor to your own terminal checkpoint rather than 'the commit': whether or when a commit happens isn't reliably part of every session, but reaching a working, reportable state is."

- id: tag-identity-dependencies-check-before-handoff
  rule: "When writing code that depends on an object's identity or reference persisting across a sequence of states — an animated element, a memoized value, a reference-keyed cache entry, an instance-bound subscription — tag it inline at the point of writing: `// [depends-on-identity]: <what must stay the same, and why>`. Before finishing, grep for the tag, verify each one against the code that now owns that object's lifecycle, then resolve it: delete the tag once verified, or replace it with an assertion or test if the invariant needs protection past this session."
  condition: "Any implementation session creating a dependency on referential/identity persistence over time. Tag at creation; resolve before considering the work done. Never leave the tag in shipped code past that point."
  reason: "A comment has no compiler and can silently drift from the code it describes — a named upgrade condition (see ceiling-comment-for-deliberate-shortcuts) doesn't help if nothing schedules an actual check of it. This tag pairs the marker with your own terminal checkpoint — the point immediately before you finish — so the condition actually gets evaluated instead of only sitting in prose. Its lifetime is bounded to one session: verified and deleted, never trusted at a distance."
  see-also: ceiling-comment-for-deliberate-shortcuts, structural-examination-at-working-checkpoint

- id: minimize-comments-prefer-self-documenting-code
  rule: "Default to no comments; precise naming and clear structure should communicate intent. Add a comment only to explain a genuinely non-obvious constraint, invariant, or deliberate workaround that isn't recoverable by reading the code itself — never to describe what the code does, and never to document UI/UX look, layout reasoning, or behavior."
  condition: "When writing or editing any code, inline or via a spawned implementation agent."
  reason: "Comments drift out of sync with the code they describe — one earned instance required fixing three stale ones in a single session, each describing behavior or symmetry that had since changed or been deleted. Needing a comment to explain what code does is itself a sign the code isn't clear enough. UI/UX documentation has a dedicated home in this system — `ui-library.md`/`ux-library.md` — with its own staleness-detection (the ratify gate's sync trigger); inline comments duplicating that have no equivalent mechanism keeping them honest."
  see-also: ceiling-comment-for-deliberate-shortcuts

- id: derivable-arithmetic-is-not-a-hidden-constraint
  rule: "Don't justify a numeric or config literal with a comment that only restates arithmetic performed on values already visible at the call site — a ratio, percentage, or unit conversion against a library default or a neighboring literal. That derivation is recoverable by any reader in the time it takes to compute it, so it fails minimize-comments-prefer-self-documenting-code's 'not recoverable by reading the code itself' bar. A literal earns a comment only when it encodes information from outside the code that reading the value can't reveal — a spec, a hardware limit, a prior incident, a compatibility requirement."
  condition: "When about to write a comment justifying a numeric or config literal, especially one framed as a derivation from a library default or another value already present nearby."
  reason: "Being able to show your work computing where a number came from feels like satisfying 'non-obvious constraint,' but the test is whether the reader gains information they couldn't already reconstruct from what's on screen — not whether the author can narrate a derivation. `minZoom={0.4}` commented as '0.5 / 0.4 = 1.25, ~25% more canvas' restates the literal in different notation; it survived one round of self-review (which correctly cut a different, narrative sentence naming the bug report that prompted the change) before a second challenge exposed that the remaining arithmetic sentence had the same defect. The self-review only checked for reasoning-leak, not for whether the surviving justification met the actual originating principle's bar."
  see-also: minimize-comments-prefer-self-documenting-code

- id: module-boundaries-precede-deployment-separation
  rule: "Before splitting code into separately-deployed services or packages, verify that the equivalent module boundaries are already clean in the existing codebase — no cycles, no cross-module access to internals. Deploy the boundary only after the code already respects it."
  condition: "When planning a migration from a monolith to microservices, separate repositories, or separately-deployed packages — at the point of deciding whether the split is ready to make."
  reason: "Deployment separation enforces physical isolation; it cannot create logical isolation. If module A depends on module B's internal functions rather than its exported API, the same entanglement persists after separation as a network call or inter-package import. The coupling is not resolved — it is made harder to refactor. Physical separation of clean logical boundaries is a deployment decision; separation of entangled code instantiates the coupling as a distributed-systems dependency."
  see-also: dependency-graph-over-architecture-diagrams

- id: dependency-graph-over-architecture-diagrams
  rule: "When auditing or enforcing architectural boundaries, derive them from the actual import/dependency graph of the code, not from architectural diagrams or intent statements."
  condition: "When verifying that two modules are genuinely isolated — before any structural separation such as package extraction, service split, or repository division — or when a stated architecture diverges from observed runtime or import behavior."
  reason: "An architecture diagram captures intent, not implementation. Two modules can be depicted as isolated boxes with a single interface arrow while one has twelve files importing from eight internal files of the other. The dependency graph is always current; a diagram is only current until the next unreviewed commit. If clean boundaries are the goal, the test is the dependency graph — a diagram that agrees with it is a summary, not evidence."
  see-also: module-boundaries-precede-deployment-separation, code-lives-at-consumer-level

- id: co-derive-coupled-values-in-one-place
  rule: "When two or more values are derived from the same input conditions and must always change together, derive them from a single computation with one branch per input case — never from separate independent conditionals or lookups that happen to key off the same condition."
  condition: "Whenever a state/condition maps to more than one dependent output that must stay consistent with each other — a label and the action it describes, a color and the icon that must match it, an error code and its message — and computing them separately risks one being edited without the other."
  reason: "Separate conditionals over the same input have no structural link between them; nothing stops one from being edited while the other is missed. Keeping one branch per case, in one place, makes the coupling visible at the point of edit instead of relying on the editor's memory to update both sites."
  see-also: single-callsite-helper-scoped

- id: throwaway-prototype-capture-decision-not-code
  rule: "When building throwaway code to answer a design or logic question — does this state model feel right, what should this UI look like — rather than to ship, keep it visibly marked as throwaway and out of the production path. Once the question is answered, capture the verdict and the question it settled as prose (in the handoff, a commit, or the deciding artifact) rather than folding the prototype code itself into the real implementation."
  condition: "When a coder- or design-composed spawn builds exploratory code specifically to answer a design or logic question before implementing for real, distinct from ordinary feature implementation."
  reason: "Throwaway code optimized for learning fast (no tests, no error handling, no abstractions) is exactly the code most likely to get folded into production once the question is answered and it already 'works' — which then ships the shortcuts that were fine for a one-off spike but aren't fine for the real feature. Capturing the verdict as text, separately from the prototype code, keeps the decision durable without also inheriting quality debt that was never meant to survive."

killed:

- id: immutable-by-default
  rule: "Declare variables, parameters, and data structures in their immutable form by default. Reach for const, readonly, and frozen or value types before their mutable counterparts; only use a mutable form when the variable or structure genuinely needs to change."
  kill_type: knowledge
  reason_killed: "Reading-pipeline sourced (kevlinhenney.medium.com) and close to universal, linter-enforced JS/TS doctrine — the knowledge-risk correlation principle-judgment's reading-pipeline-provenance-flags-knowledge-risk names directly. Also redundant with judgment already captured: the domain's own preamble already states prefer-error-exposing-form as a meta-convention (\"when two forms produce the same result but one has a silent failure mode, choose the form that exposes the error\") — an unintended reassignment is exactly that silent failure mode this candidate would have re-described as a new standalone principle."
```
