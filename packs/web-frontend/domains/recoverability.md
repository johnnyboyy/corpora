# Domain: recoverability (web-frontend pack)

Destructive actions, confirmation, undo, and recovery. The canonical cross-role domain — declared by
both the **ux-designer** and **ui-designer** lenses (the UX flow and the visible recovery affordance
are one concern). Audit metadata lives in `packs/web-frontend/domains/audit.md`, loaded only at
ratify/retrospective time.

```yaml
last-retrospective: 2026-06-20

principles:

- id: recovery-path-replaces-confirmation
  rule: "When a destructive action has a recoverable path (undo, saved history, restore), no confirmation dialog is required — the recovery path is the safety gate and must be made visible at the moment of action: an undo toast, a restore link, or a clear indicator that the action can be reversed. Confirmation dialogs are reserved for permanently irreversible actions with no recovery path."
  condition: "When designing any destructive action where a recovery mechanism exists or can be built."
  reason: "Confirmation dialogs add friction to every user — including confident ones acting intentionally. An undo mechanism only costs the user who made a mistake, and only if they need it. A recoverable action that doesn't communicate its recoverability produces the same anxiety as an unrecoverable one — the design must close the gap between 'this is recoverable' and 'the user knows it's recoverable.'"

- id: destructive-global-actions-require-confirmation
  rule: "Any action that clears all user-entered state requires either a confirmation step or an immediate undo mechanism. The trigger button carries no destructive visual styling; the confirmation or undo is the safety gate."
  condition: "When a single action irreversibly discards more than can be re-entered in under 30 seconds."
  reason: "Accidental state loss after significant data entry is a trust-breaking failure. A confirmation gate or undo toast costs minimal friction; accidental reset costs all entered data."
  see-also: recovery-path-replaces-confirmation

- id: destructive-inline-confirmation
  rule: "Low-stakes destructive actions (remove an item) use an inline row transformation to confirm — not a modal. The row shows the confirmation prompt with confirm and cancel in place of normal content."
  condition: "When designing remove/delete actions on list items."
  reason: "Modals interrupt flow and feel heavy for reversible, low-consequence actions. Inline confirmation keeps the user in context."

killed:
```
