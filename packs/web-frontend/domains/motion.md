# Domain: motion (web-frontend pack)

Animation and motion as signal. Declared by the **ui-designer** and **ux-designer** lenses.
Provenance and per-kill audit detail live in `packs/web-frontend/domains/audit.md`, loaded only at
ratify/retrospective time. See `kernel.md`, "Storage: working vs audit."

```yaml
last-retrospective: 2026-06-20

principles:

- id: motion-as-accent
  rule: "Use motion sparingly and purposefully when a state change benefits from a moment of legibility — a result appearing, a row being removed, a success state landing. Do not use motion decoratively or as a default on all interactive elements."
  condition: "Any state change or element transition in UI. Richer motion only when explicitly requested."
  reason: "Motion means something when used sparingly; it becomes noise when used everywhere. New motion should feel native to the existing register, not expressive for its own sake."
  status: ratified

- id: scrollytelling-must-always-react
  rule: "In a scrollytelling section where scroll input drives animation, the experience must provide visible feedback that input is being received at all times — not only at major action moments. Between set-pieces, a subtle continuous effect must make clear that scrolling is doing something."
  condition: "Any section that intercepts scroll to drive a narrative animation — sticky full-viewport sections, scroll-driven SVG animations, parallax-driven reveals."
  reason: "When scroll is the primary input and nothing visibly reacts, users lose their mental model of control. They don't know if they've scrolled far enough, if something is broken, or if they should try something else."
  status: ratified

killed:
```
