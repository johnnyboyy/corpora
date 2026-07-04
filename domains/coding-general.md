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
  rule: "When deliberately accepting a known limitation — a naive algorithm, a linear scan, a global lock — mark it with one inline comment: the limitation and the specific condition under which upgrading becomes necessary. Form: `// [limitation]; upgrade to [alternative] when [condition]`"
  condition: "When choosing a simpler or slower implementation that has a known ceiling on performance, correctness, or scalability."
  reason: "A silent shortcut looks like a gap. A ceiling comment distinguishes a deliberate tradeoff from an oversight and names the upgrade path so the next reader can act rather than guess."

- id: two-approaches-then-decide
  rule: "When choosing between implementation approaches, evaluate at most two seriously. If still uncommitted after two, pick the simpler one and move forward. Re-deriving the same tradeoffs is not analysis — it's spinning."
  condition: "Any time an implementation decision has more than one plausible path and the first attempt was abandoned."
  reason: "Iteration is cheaper than deliberation past the second pass. The signal that more exploration is needed is new information, not re-examining the same constraints under a slightly different framing."

- id: unified-representation-no-type-leakage
  rule: "Internal type distinctions (draft vs. entry, current vs. historical, variant A vs. B) must not escape into the consumer's data model. A unit that maintains parallel state for two variants should merge them into one unified collection before returning; a storage design where one of N items is 'active' should use an index into a flat list, not a separate slot or key."
  condition: "When a unit returns parallel outputs that differ only by an internal type distinction, or when designing state/storage for any system where one of N items is active."
  reason: "Leaking the internal distinction forces every consumer to replicate the branching logic. The unit already owns the data; it should own the routing too."

- id: color-utility-over-guesswork
  rule: "When working with colors, use the project's color utility or script rather than guessing values. If none exists, ask for one or suggest building one before proceeding."
  condition: "When computing or selecting color values — perceptual variants, palette stops, opacity blends over a backdrop, or any case where color relationships need to be derived rather than chosen arbitrarily."
  reason: "LCH color relationships are not intuitive to reason about arithmetically. Guessing produces inaccurate results and burns many tokens iterating toward something correct. A small script does this exactly for near-zero token cost."

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

killed:
```
