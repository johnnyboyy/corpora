# Domain: coding-js-react (web-frontend pack)

JS/TS/React code patterns. Declared by the coder lens when `role-pack: web-frontend`. Provenance,
promotions, and per-kill audit detail live in `packs/web-frontend/domains/audit.md`, loaded only at
ratify/retrospective time. See `kernel.md`, "Storage: working vs audit."

```yaml
last-retrospective: 2026-06-29

principles:

- id: undefined-check-by-source
  rule: "Match the equality operator to the source of the value: optional props (T | undefined) use === undefined / !== undefined; array element access and Array.find() also use !== undefined. Never == null for either."
  condition: "When guarding any value that may be absent — optional props, array element access, or Array.find() results."
  reason: "Strict equality is a common codebase convention. Both sources yield undefined (not null), but distinguishing them by name keeps intent clear. A loose == null silently absorbs both, hiding contract violations."

- id: null-first-ternary
  rule: "Use null-first ternary (`condition ? null : <Component />`) for conditional rendering; never `condition && <Component />`."
  condition: "Any JSX conditional rendering expression."
  reason: "`&&` returns whichever operand it lands on, not a boolean. A legitimate `0` (e.g. a numeric state value) renders as the literal number 0 on the page instead of rendering nothing. The null-first ternary asks the actual question — is this condition met — rather than whether something is falsy."

- id: css-var-over-mapped-class-for-dynamic-color
  rule: "When a component's fill color must track a CSS custom property that changes based on an ancestor's data attribute, use an inline style (`background: rgb(var(--token))`) rather than a Record mapping prop values to utility class names. Remove the prop entirely once it's no longer needed."
  condition: "Any component with a Record<SomeProp, string> mapping prop values to color utility classes, where those colors are meant to track a CSS custom property set on an ancestor."
  reason: "Utility class names are static strings resolved at build time; inline styles read the computed CSS variable at paint time, so the component correctly responds to ancestor scope changes."

- id: font-mono-at-element-not-container
  rule: "Apply font-mono to the individual element containing code-register data — not to a wrapper div. A container-wide font-mono forces every child into mono regardless of semantic role, requiring special overrides to correct."
  condition: "Any time font-mono is being placed on a wrapper div rather than on specific text elements inside it."
  reason: "Each element should declare its own register. Container-wide mono is an implicit contract that must be opted out of rather than opted into — the opposite of intentional."

- id: hook-params-named-for-hook-concern
  rule: "Hook parameters should be named for what the hook does with them, not for the caller's state variable. The mapping from caller concept to hook concept is documentation in the code itself."
  condition: "When a hook accepts a parameter whose name implies the caller's concept but the hook uses it for a different purpose."
  reason: "A param named for the caller's concept is opaque at the callsite — a reader sees useX(isOpen) and has to look inside the hook to understand why open-ness controls data loading. A param named for the hook's concern makes the contract legible without reading the implementation."
  see-also: hook-options-object-for-named-args

- id: hook-options-object-for-named-args
  rule: "Wrap hook boolean (and other ambiguous primitive) parameters in a single options object so the callsite reads as named arguments."
  condition: "When a hook accepts a boolean or other primitive whose meaning isn't self-evident at the callsite."
  reason: "A bare boolean arg is opaque: useX(true) forces the reader to count positional args. An options object makes the mapping explicit at the callsite: useX({ shouldRefresh: isOpen })."
  see-also: hook-params-named-for-hook-concern

- id: wizard-callbacks-unconditional
  rule: "When the same screen is reachable via both linear (Next/Back) and non-linear (tab) navigation, wire all core callbacks (onGoToStep, onEdit) unconditionally. Never make a callback conditional on which navigation path was taken."
  condition: "When implementing a wizard where a summary or output screen is reachable via multiple navigation paths."
  reason: "Conditional wiring produces two different capability levels for the same screen. Users who navigate non-linearly should never see a degraded experience compared to those who stepped through sequentially."
  see-also: wizard-output-consistent-regardless-of-path

- id: frequent-state-in-callback-deps-triggers-cascade
  rule: "Before including a state value in a useCallback or useMemo dependency array, check whether that value is updated by the same interactions the callback serves. If it is, prefer a ref or functional updater to remove the dep — or confirm that every effect listing this callback as a dep should re-fire on each state change."
  condition: "When a useCallback or useMemo dependency array includes state that is also mutated during the interactions or events the component handles."
  reason: "A dep that changes on each interaction recreates the callback each time. Any useEffect listing this callback as a dep re-fires with it — including effects whose purpose is unrelated to the changed value. The cascade is silent: types are correct, the effect appears to fire correctly, but it fires more often than intended."

- id: no-read-after-set-in-same-scope
  rule: "Never read a state value (via getter, selector, or derived hook) in the same synchronous scope as the setter call that changes it."
  condition: "When a state setter and a state read of the same value appear in the same event handler or callback — including when the read is wrapped in a memoized function that closes over the same state."
  reason: "React's setState is asynchronous — the update is enqueued, not applied. A read that immediately follows a setter cannot observe the new value and will silently compute against stale data, producing wrong output with no error signal."

- id: timer-handles-in-refs-not-state
  rule: "Store setTimeout/setInterval return values in refs (useRef), not state (useState). Never include a timer ID in a useCallback or useMemo dependency array."
  condition: "When a component or hook needs to clear or track a pending timer."
  reason: "A timer ID in state causes a re-render on every timer start or clear. Any useCallback that captures the ID must include it in deps, which recreates the callback each time — propagating recreation to every hook and effect that depends on it, potentially re-firing effects that should not have run."

- id: stable-id-not-position-for-deferred-ops
  rule: "When recording state for a deferred operation (undo, redo, queue, bookmark), store the item's stable identity (e.g. ID, slug), never its current position in a filtered, sorted, or paginated view."
  condition: "Any undo, redo, or queued action that references an item by how it was found rather than what it is."
  reason: "Position in a derived collection is only valid while the collection's filter/sort/pagination is unchanged. A stable ID remains correct across any view change; a position silently references a different item or crashes on out-of-bounds access with no warning."

- id: coordinated-setters-signal-reducer
  rule: "When a hook has 4+ state variables that consistently update together in the same handlers — where multiple setters always fire as a group — replace them with useReducer. Name the action types explicitly; they are the state machine's transitions."
  condition: "When reviewing a hook's event handlers and finding that 3+ setters always fire together, especially when the groups represent named transitions (answer submitted, question advanced, item loaded)."
  reason: "Scattered setters in a handler are a decomposed state machine — the transitions exist but aren't named. useReducer makes them explicit, consolidates mutation to one place, and lets a reader understand all valid state changes from a single function."

- id: same-state-same-name
  rule: "When two sibling types have states that produce the same visual output, unify the state vocabulary before extracting a shared renderer. A naming mismatch signals the same concept split across two types — rename first, then the shared function compiles without casting."
  condition: "When two types have parallel state fields that map to identical visual output, differing only in the name of the base/default state."
  reason: "Separate names for the same visual concept force either a translation layer or casts at the merge point. Renaming removes the impedance mismatch and makes the subset relationship structurally visible to TypeScript — the narrower type becomes assignable to the wider one without casting."

- id: stable-ref-for-document-listeners
  rule: "When a document-level event handler (visibilitychange, blur, beforeunload) must read current React state, shadow each reactive value with a ref updated on every render. The handler reads the ref, not the closure. Do not add the state to the effect's deps array as a workaround."
  condition: "When a useEffect registers a document-level listener that needs to observe current React state — and re-registering on every state change is incorrect or undesirable."
  reason: "React closures capture state at the time the effect ran. A document-level listener registered once sees stale state. Adding state to deps fixes the staleness but re-registers the listener on every change — often wrong for events like visibilitychange. A ref updated each render is always current without forcing re-registration."
  see-also: timer-handles-in-refs-not-state

- id: behavior-flags-in-refs
  rule: "Ephemeral boolean flags that control behavior but don't affect rendering — mount guards, pending-write trackers, round-error flags, any 'did-X-happen-in-this-session' bit — belong in refs, not useState."
  condition: "When adding a boolean flag whose only purpose is gating a side-effect or skipping an operation, and changing it should not trigger a re-render."
  reason: "A flag in state causes a re-render when toggled and includes the flag in the dependency surface of any memo or callback that reads it. A ref has zero rendering cost and zero dep-cascade cost. The test: would the UI look different if this flag changed? If no, it belongs in a ref."
  see-also: timer-handles-in-refs-not-state

- id: extract-named-concern-into-custom-hook
  rule: "When hook calls in a component manage a single named concern, extract them into
    a custom hook named for that concern. The component body should read as a list of
    named concerns, not a sequence of hook mechanics."
  condition: "When a component body contains any hook call or group of related hook calls
    whose purpose can be given a domain name (useOnOff, useInput, usePagination,
    useDocumentTitle). Does NOT apply when hooks are genuinely unrelated concerns that
    happen to sit near each other."
  reason: "Inline hook calls interleave multiple concerns at the component level and
    force the reader to reconstruct concern boundaries from proximity and naming alone.
    A named custom hook makes each concern boundary structural and explicit. The hook
    name replaces a comment; the component body becomes declarative."
  see-also: coordinated-setters-signal-reducer

- id: hook-returns-own-handlers
  rule: "A custom hook that owns state should return the mutation functions (handlers,
    dispatchers, setters) for that state as part of its return value. The consuming
    component should not define event handlers for state it does not own."
  condition: "When building or revisiting a custom hook that manages state and has
    associated event handlers or mutation operations — including existing hooks that
    currently return only state and leave handler definition to the consumer."
  reason: "A hook that owns state but requires consumers to write handlers breaks
    encapsulation: the consumer must understand internal state structure to mutate it
    correctly. Returning handlers keeps mutation logic co-located with the state,
    lets the implementation change without consumer edits, and makes the hook's
    interface complete."


killed:
```
