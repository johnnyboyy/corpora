# Domain: coding-js (web-frontend pack)

Framework-agnostic JS/TS code patterns — language and module-system judgment that holds regardless
of which UI framework the project uses. Declared by the coder lens when `role-pack: web-frontend`.
Audit metadata lives in `packs/web-frontend/domains/audit.md`, loaded only at ratify/retrospective
time.

```yaml
last-retrospective: 2026-07-18

principles:

- id: named-exports-over-default
  rule: "Prefer named exports over export default. Export a binding under the name it's defined with, and import it by that same name."
  condition: "When adding or refactoring a JS/TS module's exports."
  reason: "A default export lets every importer choose its own local name for the same binding, so the same value can appear under different names across the codebase, and find-references / auto-import tooling has no canonical name to anchor on. Named exports fix the name at the source, so grep and IDE find-references locate every consumer reliably."

- id: same-state-same-name
  rule: "When two sibling types have states that produce the same visual output, unify the state vocabulary before extracting a shared renderer. A naming mismatch signals the same concept split across two types — rename first, then the shared function compiles without casting."
  condition: "When two types have parallel state fields that map to identical visual output, differing only in the name of the base/default state."
  reason: "Separate names for the same visual concept force either a translation layer or casts at the merge point. Renaming removes the impedance mismatch and makes the subset relationship structurally visible to TypeScript — the narrower type becomes assignable to the wider one without casting."

- id: nan-serializes-to-null-in-json
  rule: "Never store NaN in state that will be JSON-serialized. Use undefined for 'not yet entered' — JSON.stringify omits it; NaN becomes null and silently corrupts reads. The ?? operator does not catch NaN (NaN is not null/undefined)."
  condition: "Any controlled numeric input whose onChange handler parses with parseFloat or parseInt, or any state that is JSON.stringify'd to a serialization boundary."
  reason: "JSON.stringify(NaN) === 'null'. An input cleared to '' → parseFloat('') → NaN → ??(default) still evaluates to NaN. That NaN reaches localStorage as null, breaking any consumer that assumes the TypeScript number type."
  see-also: numeric-inputs-start-empty-not-zero

killed:

- id: stable-id-not-position-for-deferred-ops
  rule: "When recording state for a deferred operation (undo, redo, queue, bookmark), store the item's stable identity, never its current position in a filtered, sorted, or paginated view."
  kill_type: quality
  reason_killed: "Zero fires across Blog and FAMOUS. Condition (undo/redo/queue/bookmark) has not appeared in either project. A principle that never fires is ambient noise."

- id: font-mono-at-element-not-container
  rule: "Apply font-mono to the individual element containing code-register data — not to a wrapper div."
  kill_type: quality
  reason_killed: "Fired once (Blog FixedBottomResultsBar, 2026-06-13). Has not recurred in FAMOUS. A correct choice a coder makes from first principles when they see the symptom."
```
