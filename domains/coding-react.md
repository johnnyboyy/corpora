# Domain: coding-react

React-specific code patterns — JSX, hooks, refs, and component prop-typing. Declared by the coder
lens when `framework` is React-based (react, next.js, react native, expo, etc.). Split from
`coding-js-react` 2026-07-18 once the domain's
framework-agnostic JS/TS principles were carved into their own `coding-ts` domain — see
`domains/audit.md` for the migration note. Audit metadata lives in
`domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: 2026-07-18

principles:

- id: null-first-ternary
  rule: "Use null-first ternary (`condition ? null : <Component />`) for conditional rendering; never `condition && <Component />`."
  condition: "Any JSX conditional rendering expression."
  reason: "`&&` returns whichever operand it lands on, not a boolean. A legitimate `0` (e.g. a numeric state value) renders as the literal number 0 on the page instead of rendering nothing. The null-first ternary asks the actual question — is this condition met — rather than whether something is falsy."

- id: wizard-callbacks-unconditional
  rule: "When the same screen is reachable via both linear (Next/Back) and non-linear (tab) navigation, wire all core callbacks (onGoToStep, onEdit) unconditionally. Never make a callback conditional on which navigation path was taken."
  condition: "When implementing a wizard where a summary or output screen is reachable via multiple navigation paths."
  reason: "Conditional wiring produces two different capability levels for the same screen. Users who navigate non-linearly should never see a degraded experience compared to those who stepped through sequentially."
  see-also: wizard-output-consistent-regardless-of-path

- id: coordinated-setters-signal-reducer
  rule: "When a hook has 4+ state variables that consistently update together in the same handlers — where multiple setters always fire as a group — replace them with useReducer. Name the action types explicitly; they are the state machine's transitions."
  condition: "When reviewing a hook's event handlers and finding that 3+ setters always fire together, especially when the groups represent named transitions (answer submitted, question advanced, item loaded)."
  reason: "Scattered setters in a handler are a decomposed state machine — the transitions exist but aren't named. useReducer makes them explicit, consolidates mutation to one place, and lets a reader understand all valid state changes from a single function."

- id: nested-conditional-signals-sub-component
  rule: "When a render contains a nested conditional (A ? (B ? X : Y) : Z), treat the inner
    conditional as a strong signal that branches X and Y have a narrower consumer than the outer
    condition — extract them into a sub-component that owns that decision. Exception: short,
    self-evident inner branches that add no reader overhead."
  condition: "When reviewing JSX where a ternary's truthy or falsy branch is itself a ternary."
  reason: "A nested conditional encodes two distinct concerns at the same level. The outer condition
    gates access to the inner one, which means the inner branches have a narrower scope. Extracting
    the inner decision to a sub-component makes each layer's responsibility legible and prevents the
    parent from accumulating branching logic that belongs to its children. The test is reader overhead:
    if the nesting costs the reader nothing to parse, extraction is optional."

- id: prefers-reduced-motion-requires-js-hook
  rule: "For JS-driven animations, detect `prefers-reduced-motion` via a custom hook reading `window.matchMedia('(prefers-reduced-motion: reduce)')` and subscribing to its `change` event. Apply the result to conditionally set duration to zero or skip the animation call. Do not rely on CSS media query overrides alone."
  condition: "When implementing any animation whose parameters — duration, keyframes, or whether it fires at all — are configured in JavaScript, including use of Framer Motion, React Spring, GSAP, Reanimated, or manual Web Animations API calls."
  reason: "CSS `@media (prefers-reduced-motion: reduce)` only overrides CSS animation and transition properties. JS animation libraries read configuration from JS objects at runtime; no CSS rule can reach those values. A hook reading `window.matchMedia` is the only way to honor the OS preference for JS-controlled animations. Subscribing to the `change` event rather than reading once at mount ensures the preference stays current if the user toggles the OS setting during the session."
  see-also: reduced-motion-instant-not-absent

- id: discriminated-union-for-mutually-exclusive-props
  rule: "When a component has N variants whose prop sets are mutually exclusive, model the prop type as a discriminated union, not a flat interface with optional fields. Each union member carries the discriminant field and the props that are required — not optional — for that variant."
  condition: "When designing or refactoring the TypeScript prop interface of a component that has two or more distinct usage modes, each requiring different props, where mixing props from two modes should be a compile-time error."
  reason: "A flat interface with all variant props marked optional allows every combination, including impossible ones (icon and label together, or neither). TypeScript cannot flag these because all props are optional. A discriminated union narrows props at every discriminant check site, makes each variant's required fields explicit, and forces call sites to handle a new variant when one is added — exhaustiveness checks surface missing cases at compile time, not at runtime."
  see-also: unified-representation-no-type-leakage

- id: behavior-flags-in-refs
  rule: "Ephemeral values that control behavior but don't affect rendering — boolean flags (mount guards, pending-write trackers, round-error bits), timer handles (setTimeout/setInterval return values), any 'did-X-happen-in-this-session' value, or a mirror of current state read only by an external handler (a document-level listener, an imperative ref method) — belong in refs, not useState. Never include timer IDs or behavioral flags in a useCallback or useMemo dependency array. For a document-level event handler (visibilitychange, blur, beforeunload) that must read current React state, shadow the reactive value with a ref updated on every render and have the handler read the ref — not the closure — rather than adding the state to the effect's dependency array as a workaround."
  condition: "When adding any value whose purpose is gating or tracking a side-effect rather than driving rendered output — including a ref that exists only so an external listener or imperative method can read current state without a stale closure. Test: would the UI look different if this value changed? If no, it belongs in a ref."
  reason: "A value in state causes a re-render when changed and enters the dependency surface of any memo or callback. A ref has zero rendering cost and zero dep-cascade cost. Timer IDs especially: they change on every start/clear, so a dep array that includes one recreates the callback each time — propagating recreation to every hook and effect that depends on it, potentially re-firing effects that should not have run. The same test explains document-level listeners: registering one with reactive state in its dependency array re-registers it on every change, which is often wrong for events like visibilitychange, while a closure captured once goes stale if it isn't. Mirroring the state into a ref read by the handler avoids both failure modes, because the mirrored value never drives a render and therefore never needs to appear in a dependency array."

- id: hook-callsite-legibility
  rule: "Hook parameters should be named for what the hook does with them, not the caller's state variable. Wrap boolean and other ambiguous primitive params in a single options object so the callsite reads as named arguments: useX({ shouldRefresh: isOpen }) not useX(isOpen)."
  condition: "When a hook accepts a parameter whose name implies the caller's concept rather than the hook's concern, or a bare boolean/primitive whose meaning isn't self-evident at the callsite."
  reason: "A param named for the caller's concept is opaque at the callsite — a reader sees useX(isOpen) and must look inside the hook to understand why openness controls loading. An options object makes the mapping explicit without reading the implementation. Both failures read identically at the callsite: a renamed param and a bare boolean each force a lookup that an explicit name or options object removes."

- id: custom-hook-owns-its-concern
  rule: "When a group of hook calls in a component manages a single nameable concern, extract them into a custom hook named for that concern. The hook should return the mutation functions (handlers, dispatchers) for the state it owns — the component should not define event handlers for state it doesn't own."
  condition: "When a component body contains hook calls whose purpose can be given a domain name (useOnOff, usePagination, useDocumentTitle), or when a hook manages state but leaves handler definition to consumers."
  reason: "Inline hook mechanics interleave concerns at the component level, forcing the reader to reconstruct concern boundaries from proximity and naming. A named custom hook makes each boundary structural. A hook that owns state but requires consumers to write handlers breaks encapsulation: consumers must understand internal state structure to mutate it correctly. Returning handlers keeps mutation logic co-located with the state and lets the implementation change without consumer edits."
  see-also: coordinated-setters-signal-reducer

- id: effect-only-derived-state-belongs-in-render
  rule: "When a useEffect's entire body only computes or adjusts local state from a prop or another piece of state's current value — no subscription, timer, listener, fetch, or other external interaction — do the comparison and setState call directly in the render body (a ref holding the 'previous value' is fine to mutate there), not inside useEffect."
  condition: "When reviewing a useEffect whose body contains zero external interaction and whose only effect is one or more setState calls gated by a dependency-array change."
  reason: "The effect only defers a derivable computation to a second render pass for no benefit — an extra render plus an unneeded node in the effect dependency graph. Confirmed as a recurring miss, not a one-off: found independently in FAMOUS (PlayerBarContent's track-change scrubber reset) and Blog (ResultBar's useResultFlash throttled counter), both effects existing purely to adjust local state with no external interaction."

- id: optimistic-ui-for-high-confidence-mutations
  rule: "Apply optimistic UI (show assumed-success state immediately) only for mutations where server failure is rare and a visible rollback carries low cost — toggles, likes, reorders, non-destructive inline updates. Do not use optimistic UI for destructive actions, payment flows, or any mutation whose failure would require significant user re-entry."
  condition: "When deciding whether to apply optimistic state patterns (React 19 `useOptimistic`, or manual optimistic state) to a user-triggered server mutation."
  reason: "Optimistic UI trades accuracy for perceived speed. The pattern earns its keep when the assumed-success is almost always correct — the rare rollback is a minor correction. When failure is plausible (a payment that might decline, a delete that might conflict), a visible rollback is disorienting: the user briefly sees success, then it reverses. Worse, a user who misreads the rollback as success stops retrying. The optimistic assumption must be safe to make."
  see-also: optimistic-rollback-requires-explicit-error, recovery-path-replaces-confirmation

- id: optimistic-rollback-requires-explicit-error
  rule: "When an optimistic UI mutation fails and state rolls back to its pre-action value, always surface an explicit error message. Never let the visual rollback be the sole signal of failure."
  condition: "When implementing any optimistic state pattern — including React 19 `useOptimistic` — where the state reverts on a failed async action."
  reason: "A state rollback with no error message is experienced as a mysterious 'snap-back': the UI briefly showed the new state, then silently returned to the old one. The user doesn't know if the action failed, is still pending, or partially succeeded — and whether they should retry. An explicit error closes the gap between what happened internally and what the user knows happened, and makes retry decisions possible."
  see-also: optimistic-ui-for-high-confidence-mutations, recovery-path-replaces-confirmation

killed:

- id: hook-params-named-for-hook-concern
  rule: "Hook parameters should be named for what the hook does with them, not for the caller's state variable."
  kill_type: quality
  reason_killed: "Merged into hook-callsite-legibility alongside hook-options-object-for-named-args. Both were two facets of the same concern — legible hook callsite — always proposed together from the same session. The merged principle states both forms in one entry."

- id: hook-options-object-for-named-args
  rule: "Wrap hook boolean (and other ambiguous primitive) parameters in a single options object so the callsite reads as named arguments."
  kill_type: quality
  reason_killed: "Merged into hook-callsite-legibility alongside hook-params-named-for-hook-concern. See that entry."

- id: stable-ref-for-document-listeners
  rule: "When a document-level event handler (visibilitychange, blur, beforeunload) must read current React state, shadow each reactive value with a ref updated on every render. The handler reads the ref, not the closure. Do not add the state to the effect's deps array as a workaround."
  kill_type: quality
  reason_killed: "Merged into behavior-flags-in-refs (structural-kinship retrospective signal, 2026-07-18). Both answered the same test — does this value drive rendered output; if not, it belongs in a ref, not state — this one is the document-listener instance of it. Absorbed as a named case in the general principle's rule and reason rather than kept as a separate entry."

- id: extract-named-concern-into-custom-hook
  rule: "When hook calls in a component manage a single named concern, extract them into a custom hook named for that concern."
  kill_type: quality
  reason_killed: "Merged into custom-hook-owns-its-concern alongside hook-returns-own-handlers. Extraction and interface completeness are co-decisions — separated they invite partial application."

- id: hook-returns-own-handlers
  rule: "A custom hook that owns state should return the mutation functions (handlers, dispatchers, setters) for that state as part of its return value."
  kill_type: quality
  reason_killed: "Merged into custom-hook-owns-its-concern alongside extract-named-concern-into-custom-hook. See that entry."

- id: timer-handles-in-refs-not-state
  rule: "Store setTimeout/setInterval return values in refs (useRef), not state (useState). Never include a timer ID in a useCallback or useMemo dependency array."
  kill_type: quality
  reason_killed: "Absorbed into behavior-flags-in-refs, which is the general form. Timer IDs are behavioral flags — they gate logic without affecting rendered output. The dep-cascade concern is now part of that principle's reason."

- id: no-read-after-set-in-same-scope
  rule: "Never read a state value in the same synchronous scope as the setter call that changes it."
  kill_type: knowledge
  reason_killed: "React's setState is async/enqueued is a first-day React fact derivable from training data. No project-specific judgment encoded — same class as preserve-3d-on-every-ancestor. A coder who needs the reminder will find it in the React docs."

- id: css-var-over-mapped-class-for-dynamic-color
  rule: "When a component's fill color must track a CSS custom property that changes based on an ancestor's data attribute, use an inline style rather than a Record mapping prop values to utility class names."
  kill_type: quality
  reason_killed: "Fired once (Blog WireCircle, 2026-06-13). Condition requires ancestor data-attribute scoping plus static class-map — not recurred in FAMOUS. Too narrow for a seed principle after two projects."

- id: frequent-state-in-callback-deps-triggers-cascade
  rule: "Before including a state value in a useCallback or useMemo dependency array, check whether that value is updated by the same interactions the callback serves."
  kill_type: quality
  reason_killed: "No project-domain instance across Blog or FAMOUS. Idle across two projects. The cascade concern now lives in the updated behavior-flags-in-refs reason (timer IDs in dep arrays as the canonical example)."
```
