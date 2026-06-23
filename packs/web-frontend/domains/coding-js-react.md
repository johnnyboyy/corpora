# Domain: coding-js-react (web-frontend pack)

JS/TS/React code patterns. Declared by the coder lens when `role-pack: web-frontend`. Provenance,
promotions, and per-kill audit detail live in `packs/web-frontend/domains/audit.md`, loaded only at
ratify/retrospective time. See `kernel.md`, "Storage: working vs audit."

```yaml
last-retrospective: 2026-06-18

principles:

- id: undefined-check-by-source
  rule: "Match the equality operator to the source of the value: optional props (T | undefined) use === undefined / !== undefined; array element access and Array.find() also use !== undefined. Never == null for either."
  condition: "When guarding any value that may be absent — optional props, array element access, or Array.find() results."
  reason: "Strict equality is a common codebase convention. Both sources yield undefined (not null), but distinguishing them by name keeps intent clear. A loose == null silently absorbs both, hiding contract violations."
  status: ratified

- id: null-first-ternary
  rule: "Use null-first ternary (`condition ? null : <Component />`) for conditional rendering; never `condition && <Component />`."
  condition: "Any JSX conditional rendering expression."
  reason: "`&&` returns whichever operand it lands on, not a boolean. A legitimate `0` (e.g. a numeric state value) renders as the literal number 0 on the page instead of rendering nothing. The null-first ternary asks the actual question — is this condition met — rather than whether something is falsy."
  status: ratified

- id: css-var-over-mapped-class-for-dynamic-color
  rule: "When a component's fill color must track a CSS custom property that changes based on an ancestor's data attribute, use an inline style (`background: rgb(var(--token))`) rather than a Record mapping prop values to utility class names. Remove the prop entirely once it's no longer needed."
  condition: "Any component with a Record<SomeProp, string> mapping prop values to color utility classes, where those colors are meant to track a CSS custom property set on an ancestor."
  reason: "Utility class names are static strings resolved at build time; inline styles read the computed CSS variable at paint time, so the component correctly responds to ancestor scope changes."
  status: ratified

- id: font-mono-at-element-not-container
  rule: "Apply font-mono to the individual element containing code-register data — not to a wrapper div. A container-wide font-mono forces every child into mono regardless of semantic role, requiring special overrides to correct."
  condition: "Any time font-mono is being placed on a wrapper div rather than on specific text elements inside it."
  reason: "Each element should declare its own register. Container-wide mono is an implicit contract that must be opted out of rather than opted into — the opposite of intentional."
  status: ratified

- id: hook-params-named-for-hook-concern
  rule: "Hook parameters should be named for what the hook does with them, not for the caller's state variable. The mapping from caller concept to hook concept is documentation in the code itself."
  condition: "When a hook accepts a parameter whose name implies the caller's concept but the hook uses it for a different purpose."
  reason: "A param named for the caller's concept is opaque at the callsite — a reader sees useX(isOpen) and has to look inside the hook to understand why open-ness controls data loading. A param named for the hook's concern makes the contract legible without reading the implementation."
  see-also: hook-options-object-for-named-args
  status: ratified

- id: hook-options-object-for-named-args
  rule: "Wrap hook boolean (and other ambiguous primitive) parameters in a single options object so the callsite reads as named arguments."
  condition: "When a hook accepts a boolean or other primitive whose meaning isn't self-evident at the callsite."
  reason: "A bare boolean arg is opaque: useX(true) forces the reader to count positional args. An options object makes the mapping explicit at the callsite: useX({ shouldRefresh: isOpen })."
  see-also: hook-params-named-for-hook-concern
  status: ratified

- id: wizard-callbacks-unconditional
  rule: "When the same screen is reachable via both linear (Next/Back) and non-linear (tab) navigation, wire all core callbacks (onGoToStep, onEdit) unconditionally. Never make a callback conditional on which navigation path was taken."
  condition: "When implementing a wizard where a summary or output screen is reachable via multiple navigation paths."
  reason: "Conditional wiring produces two different capability levels for the same screen. Users who navigate non-linearly should never see a degraded experience compared to those who stepped through sequentially."
  see-also: wizard-output-consistent-regardless-of-path
  status: ratified

- id: frequent-state-in-callback-deps-triggers-cascade
  rule: "Before including a state value in a useCallback or useMemo dependency array, check whether that value is updated by the same interactions the callback serves. If it is, prefer a ref or functional updater to remove the dep — or confirm that every effect listing this callback as a dep should re-fire on each state change."
  condition: "When a useCallback or useMemo dependency array includes state that is also mutated during the interactions or events the component handles."
  reason: "A dep that changes on each interaction recreates the callback each time. Any useEffect listing this callback as a dep re-fires with it — including effects whose purpose is unrelated to the changed value. The cascade is silent: types are correct, the effect appears to fire correctly, but it fires more often than intended."
  status: proposed

- id: no-read-after-set-in-same-scope
  rule: "Never read a state value (via getter, selector, or derived hook) in the same synchronous scope as the setter call that changes it."
  condition: "When a state setter and a state read of the same value appear in the same event handler or callback — including when the read is wrapped in a memoized function that closes over the same state."
  reason: "React's setState is asynchronous — the update is enqueued, not applied. A read that immediately follows a setter cannot observe the new value and will silently compute against stale data, producing wrong output with no error signal."
  status: proposed

- id: timer-handles-in-refs-not-state
  rule: "Store setTimeout/setInterval return values in refs (useRef), not state (useState). Never include a timer ID in a useCallback or useMemo dependency array."
  condition: "When a component or hook needs to clear or track a pending timer."
  reason: "A timer ID in state causes a re-render on every timer start or clear. Any useCallback that captures the ID must include it in deps, which recreates the callback each time — propagating recreation to every hook and effect that depends on it, potentially re-firing effects that should not have run."
  status: proposed

- id: stable-id-not-position-for-deferred-ops
  rule: "When recording state for a deferred operation (undo, redo, queue, bookmark), store the item's stable identity (e.g. ID, slug), never its current position in a filtered, sorted, or paginated view."
  condition: "Any undo, redo, or queued action that references an item by how it was found rather than what it is."
  reason: "Position in a derived collection is only valid while the collection's filter/sort/pagination is unchanged. A stable ID remains correct across any view change; a position silently references a different item or crashes on out-of-bounds access with no warning."
  status: proposed

killed:
```
