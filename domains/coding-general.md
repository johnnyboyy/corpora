# Domain: coding-general

Stack-agnostic coding judgment — applies in any language or framework, loaded by any
convergent coding spawn (always). Audit metadata lives in `domains/audit.md`, loaded only at
ratify/retrospective time.

Foundational, stable across every project shape this domain serves — folded here from the
audit layer's retired `promoted:` section (v3-redesign-proposal.md, 2026-07-21) rather than kept
as a separate authority tier:

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
  rule: "When deliberately accepting a known limitation — a naive algorithm, a linear scan, a global lock — mark it with one inline comment: the limitation and the specific condition under which upgrading becomes necessary. Form: `// [limitation]; upgrade to [alternative] when [condition]`. Treat that named condition as live, not archival: at the same structural-examination pass done before writing the handoff artifact (see structural-examination-at-working-checkpoint), check any ceiling comment in code touched this session against its condition, and upgrade or remove it if the condition now holds."
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
  rule: "When work is deterministic, precision-sensitive, or disproportionately expensive to solve by inference — color/LCH math, date and timezone arithmetic, geometric layout, hashing, unit conversion, and similar — use the project's registered utility for it if one exists. If none exists, propose one as a utility candidate in the handoff rather than solving it by inference every time."
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
  rule: "Before writing the handoff artifact for a working implementation, do a one-pass structural examination. Look for: (1) implicit coupling via string selectors or attribute names used as DOM contracts, (2) thin wrappers whose only job is bundling two things with no identity of their own, (3) logic blocks with a clear purpose but no explicit name — candidates for extraction to a named hook or function, (4) emergent groupings — types, functions, and hooks that belong together but ended up separated during implementation."
  condition: "After any multi-file or multi-component implementation reaches a working state (feature correct, typecheck and lint pass) — at the coder's own terminal checkpoint, immediately before writing the handoff artifact (or, for a trivial inline session with no handoff file, before reporting the work as done)."
  reason: "Running code reveals structural seams that planning cannot predict. The implementation session surfaces what talks to what and via what contract. Examining now costs minutes; the same issues discovered later cost full context reconstruction. Thin wrappers and implicit string contracts are especially invisible during planning — they emerge from solving the problem, not from designing the solution. Anchored to the handoff artifact rather than 'the commit': when or whether a commit happens isn't reliably this session's own event, but writing the handoff artifact always is — it's a checkpoint every session actually reaches."

- id: tag-identity-dependencies-check-before-handoff
  rule: "When writing code that depends on an object's identity or reference persisting across a sequence of states — an animated element, a memoized value, a reference-keyed cache entry, an instance-bound subscription — mark it inline at the point of writing with a one-line, session-scoped tag: `// [depends-on-identity]: <what must stay the same, and why>`. Before writing the handoff artifact, grep for the tag, verify each one against the code that now owns that object's lifecycle, and remove it — it is a todo for this session's own review, not a permanent comment. If the dependency is significant enough to need protection past this session, replace the tag with an assertion or a test asserting the invariant instead of leaving prose behind."
  condition: "Any coder session creating a dependency on referential/identity persistence over time. Tag at creation; resolve — verify-and-delete, or upgrade to an assertion/test — before writing the handoff artifact. Never leave the tag in shipped code past that point."
  reason: "A comment has no compiler and can drift from the code it describes; the same risk applies to any inline marker, including one with a named resolution condition (see ceiling-comment-for-deliberate-shortcuts), if nothing schedules an active check of that condition. This tag pairs the marker with an explicit, structurally-guaranteed checkpoint — immediately before writing the handoff artifact, the coder's own terminal act — so the condition actually gets evaluated rather than only sitting in prose. Its lifetime is bounded to one session: it is deleted once verified, never trusted at a distance past that point. What it doesn't solve: a dependency needing protection across later sessions needs a real check — an assertion or a test — because nothing enforces a comment's truth, resolved or not, once the session that wrote it ends. Two locally-correct pieces of code can still break when combined if one depends on identity/reference persistence and the other manages that object's lifecycle without knowing the dependency exists (first found as a CSS transition broken by a render function that rebuilt every element from scratch each render); this tag exists to make that class of dependency visible to both sides before it ships."
  see-also: ceiling-comment-for-deliberate-shortcuts, structural-examination-at-working-checkpoint

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

killed:
```
