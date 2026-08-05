# Phase: framing

The universal front door. Every task passes through framing before anything acts on it — but the
step's *output scales to the task*, so a one-property change costs one line and a vague goal earns a
full disambiguation. This is the phase that makes proportionality real and that surfaces the
assumptions being made before they're realized.

**Entry condition:** every task, before acting. Not skippable. (What *is* proportional is the depth of
what framing produces — see Proportionality.)

**Stance:** none for the deterministic facts; light convergent judgment for sizing and assumption
statement. Not generative.

**Invocations:** the judgment engine (corpora, for now) — invoked **only when sizing lands above
trivial** and genuine judgment remains: a disambiguation dialogue when the ask is ambiguous, or a
composed spawn when a real spec/decision is warranted. A trivial task invokes nothing.

## Deterministic facts — run these first, always (they can't be wrong)

Gather them in one call:

```
praxis/scripts/frame.py --from <search-base> --target <path> [--files a,b] --unit-of-work <uow>
```

It returns, as fact:

1. **Which root governs this task** — and if the candidate files span more than one root, the verdict
   is **decompose**: it is N units of work, one handed to each root, and it is *not composed or acted
   on as one task*. A single agent never straddles two roots. Stop here and hand off per root.
2. **Composition** — the domain set for the task's unit-of-work, obtained by invoking the judgment
   engine (corpora composes; praxis relays). Composition is a fact only once the unit-of-work is
   decided — that decision is routing judgment (below); everything after it is fact.

If the engine is unavailable the root facts still stand — praxis does not depend on it. Only what
remains after these facts is judgment.

## Proportionality — the frame scales to the task

The step always runs; its *volume* is proportional to real ambiguity. Three sizes, decided by the
judgment on top of the facts above:

- **Trivial / unambiguous** — one property, one file, matches a pattern the library already
  documents. State the single assumption inline — *"changing the primary login button's background
  token from `X` to `Y`; say so if you meant a different button or property"* — then execute
  directly. No spawn, no questions, no plan. The assumption-relay **is** the disambiguation here.
- **Bounded but ambiguous** — one or two targeted questions (framed for a cheap answer; state a clear
  direction rather than manufacturing a false choice), then execute or a single composed spawn.
- **Vague / multi-part** — full disambiguation → planning → decomposition. This is the shape that has
  been working well; framing just makes it the *earned* path, not the default one.

The failure to avoid in both directions: ballooning "change the button color" into a UI/UX →
implementation pipeline, and jumping into a vague goal without surfacing what was assumed.

## Assumptions are always surfaced

Whatever the size, framing states the assumptions it is acting on **before** acting, so they can be
redirected before they're realized. This is the floor of the step — even the trivial case surfaces
its one assumption. Non-blocking for trivial (state and proceed, interruptible); blocking for larger
(state and wait).

**Artifact:** a *frame* — the governing root, the assumptions stated for redirection, the size
verdict, and the route taken. For a trivial task the frame is one or two inline lines proceeded past;
for a vague task it is the entry into disambiguation/planning.

**Surfaced/lacking:** if the *size itself* is unclear — the request is ambiguous enough that you'd
have to assume its shape to size it — that is the signal to invoke disambiguation, not to guess a
size. Record any shape-assumption made to size the task as the first thing to confirm.
