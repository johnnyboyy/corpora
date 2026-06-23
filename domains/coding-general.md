# Domain: coding-general

Stack-agnostic coding judgment — applies in any language or framework. Declared by the **coder**
lens (always). Provenance, promotions, and per-kill audit detail live in `domains/audit.md` (this
layer), loaded only at ratify/retrospective time. See `kernel.md`, "Storage: working vs audit."

```yaml
last-retrospective: 2026-06-20

principles:

- id: ask-before-architecture
  rule: "When a task involves a structural or DRY question with two reasonable approaches, name both and ask before implementing."
  condition: "When implementing a structural change where multiple approaches are plausible — class vs. function extraction, inline vs. extracted helper, etc."
  reason: "Architectural questions are cheap to clarify and expensive to implement wrong. One question saves a full round-trip correction and avoids a messy intermediate state the user has to redirect out of."
  status: ratified

- id: verify-before-bulk-edit
  rule: "Before replace_all or any bulk find-and-replace, grep for all instances and read context around each match to confirm they are all conceptually equivalent."
  condition: "Whenever the same string or pattern appears in multiple places and a bulk replacement is tempting."
  reason: "Occurrences of the same string are not always the same thing. Bulk replacement without verification creates a syntactically correct but conceptually wrong intermediate state — worse than not having made the change."
  status: ratified

- id: grep-subdirs-before-delete
  rule: "Before deleting a file flagged as a redundant duplicate, grep for all relative imports/references (including ../ and ../../ variants) across the entire directory subtree, not just sibling files."
  condition: "When deleting a file that other files in the same directory tree may reference via relative paths."
  reason: "Subdirectories have different relative path depths, so a grep limited to ./ will miss references in nested dirs. The build reveals them, but a wider grep at task start catches them in one pass."
  status: ratified

- id: code-lives-at-consumer-level
  rule: "Code lives at the level of its narrowest consumer. Something used in one file stays in that file; something used in one module stays in that module. Once a second consumer appears, promote immediately — do not defer. Promote to the lowest common ancestor of its consumers, and place shared code beside the data type or concern it serves."
  condition: "When deciding where a function, type, or component should live — at initial placement and at the moment a second consumer appears."
  reason: "Premature extraction signals reuse that isn't real, obscures actual scope, and implies candidacy for import when it isn't. One module importing from another's internals creates a hidden peer dependency."
  status: ratified

- id: generic-defers-to-consumer
  rule: "Generic components expose extension points (parameters, slots, options) and make no assumptions about their caller's context. Any concern specific to a particular use case belongs in the consumer that has that context."
  condition: "When building any reusable unit that will be composed into more specific ones. Test: could this serve two different contexts with different concerns? If yes, the generic must not bake in either."
  reason: "A generic unit's value is reusability across contexts. Every caller-specific assumption hardcoded into the generic narrows that reusability and hides the dependency from the call site."
  status: ratified

- id: single-callsite-helper-scoped
  rule: "A function that computes a value and has exactly one callsite should not be extracted as a standalone function. Resolve it where it's used — as a local in the calling scope (preferred when the expression is long), or inlined directly when it's short."
  condition: "When a standalone helper has exactly one callsite. Does not apply to functions called from two or more places — those earn the extraction."
  reason: "A standalone function implies reuse. A single-callsite helper adds a named concept with no benefit. Keeping the resolution local is more honest about its scope."
  status: ratified

- id: ceiling-comment-for-deliberate-shortcuts
  rule: "When deliberately accepting a known limitation — a naive algorithm, a linear scan, a global lock — mark it with one inline comment: the limitation and the specific condition under which upgrading becomes necessary. Form: `// [limitation]; upgrade to [alternative] when [condition]`"
  condition: "When choosing a simpler or slower implementation that has a known ceiling on performance, correctness, or scalability."
  reason: "A silent shortcut looks like a gap. A ceiling comment distinguishes a deliberate tradeoff from an oversight and names the upgrade path so the next reader can act rather than guess."
  status: ratified

- id: two-approaches-then-decide
  rule: "When choosing between implementation approaches, evaluate at most two seriously. If still uncommitted after two, pick the simpler one and move forward. Re-deriving the same tradeoffs is not analysis — it's spinning."
  condition: "Any time an implementation decision has more than one plausible path and the first attempt was abandoned."
  reason: "Iteration is cheaper than deliberation past the second pass. The signal that more exploration is needed is new information, not re-examining the same constraints under a slightly different framing."
  status: ratified

- id: unified-representation-no-type-leakage
  rule: "Internal type distinctions (draft vs. entry, current vs. historical, variant A vs. B) must not escape into the consumer's data model. A unit that maintains parallel state for two variants should merge them into one unified collection before returning; a storage design where one of N items is 'active' should use an index into a flat list, not a separate slot or key."
  condition: "When a unit returns parallel outputs that differ only by an internal type distinction, or when designing state/storage for any system where one of N items is active."
  reason: "Leaking the internal distinction forces every consumer to replicate the branching logic. The unit already owns the data; it should own the routing too."
  status: ratified

- id: color-utility-over-guesswork
  rule: "When working with colors, use the project's color utility or script rather than guessing values. If none exists, ask for one or suggest building one before proceeding."
  condition: "When computing or selecting color values — perceptual variants, palette stops, opacity blends over a backdrop, or any case where color relationships need to be derived rather than chosen arbitrarily."
  reason: "LCH color relationships are not intuitive to reason about arithmetically. Guessing produces inaccurate results and burns many tokens iterating toward something correct. A small script does this exactly for near-zero token cost."
  status: ratified

killed:
```
