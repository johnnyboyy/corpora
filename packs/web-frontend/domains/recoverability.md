# Domain: recoverability (web-frontend pack)

Destructive actions, confirmation, undo, and recovery. The canonical cross-role domain — declared by
both the **ux-designer** and **ui-designer** lenses (the UX flow and the visible recovery affordance
are one concern). Audit metadata lives in `packs/web-frontend/domains/audit.md`, loaded only at
ratify/retrospective time.

```yaml
last-retrospective: 2026-06-20

principles:

- id: recovery-path-replaces-confirmation
  rule: "A destructive action that would cost meaningful re-entry to undo (roughly 30+ seconds of work) needs either a recovery path (undo, saved history, restore) or a confirmation step — never neither, and the trigger button's styling doesn't count as the gate. A visible recovery path (undo toast, restore link) replaces confirmation; confirmation is for actions with no recovery path. Trivial actions below that bar need neither."
  condition: "When designing a destructive action that discards user-entered state worth roughly 30+ seconds to re-enter, or where a recovery mechanism already exists or could be built."
  reason: "Confirmation adds friction for every user; an undo mechanism only costs the one who errs. An ungated loss of substantial work breaks trust, and a recovery path that isn't visible produces the same anxiety as no recovery at all."

- id: destructive-inline-confirmation
  rule: "Low-stakes destructive actions (remove an item) use an inline row transformation to confirm — not a modal. The row shows the confirmation prompt with confirm and cancel in place of normal content."
  condition: "When designing remove/delete actions on list items."
  reason: "Modals interrupt flow and feel heavy for reversible, low-consequence actions. Inline confirmation keeps the user in context."

- id: optimistic-ui-for-high-confidence-mutations
  rule: "Apply optimistic UI (show assumed-success state immediately) only for mutations where server failure is rare and a visible rollback carries low cost — toggles, likes, reorders, non-destructive inline updates. Do not use optimistic UI for destructive actions, payment flows, or any mutation whose failure would require significant user re-entry."
  condition: "When deciding whether to apply optimistic state patterns (React 19 `useOptimistic`, or manual optimistic state) to a user-triggered server mutation."
  reason: "Optimistic UI trades accuracy for perceived speed. The pattern earns its keep when the assumed-success is almost always correct — the rare rollback is a minor correction. When failure is plausible (a payment that might decline, a delete that might conflict), a visible rollback is disorienting: the user briefly sees success, then it reverses. Worse, a user who misreads the rollback as success stops retrying. The optimistic assumption must be safe to make."
  see-also: recovery-path-replaces-confirmation, optimistic-rollback-requires-explicit-error

- id: optimistic-rollback-requires-explicit-error
  rule: "When an optimistic UI mutation fails and state rolls back to its pre-action value, always surface an explicit error message. Never let the visual rollback be the sole signal of failure."
  condition: "When implementing any optimistic state pattern — including React 19 `useOptimistic` — where the state reverts on a failed async action."
  reason: "A state rollback with no error message is experienced as a mysterious 'snap-back': the UI briefly showed the new state, then silently returned to the old one. The user doesn't know if the action failed, is still pending, or partially succeeded — and whether they should retry. An explicit error closes the gap between what happened internally and what the user knows happened, and makes retry decisions possible."
  see-also: recovery-path-replaces-confirmation, optimistic-ui-for-high-confidence-mutations

killed:

- id: destructive-global-actions-require-confirmation
  rule: "Any action that clears all user-entered state requires either a confirmation step or an immediate undo mechanism. The trigger button carries no destructive visual styling; the confirmation or undo is the safety gate."
  kill_type: quality
  reason_killed: "Merged into recovery-path-replaces-confirmation. Both were the same recovery-or-confirmation test — this one just named a concrete severity bar (~30s of re-entry) for when the gate becomes mandatory. Absorbed as that threshold, stated directly in the general principle's rule and reason."
```
