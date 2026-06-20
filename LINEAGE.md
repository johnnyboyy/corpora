# Lineage

This document explains how the system and its conventions came to be — not what they are
(that's `skill.md` and `kernel.md`), but why they are. It's for someone fresh to the repo
who finds a convention and wonders whether it's arbitrary, or for anyone returning after
a gap who wants the reasoning rather than just the rule.

---

## The kernel design

### Why "reason travels with the rule"

The earliest version of this system had principles stated as rules only. They worked until
a case arrived where the reason didn't apply — and the role had no basis for deciding whether
the rule still bound. It either applied it mechanically (dogma) or ignored it (drift). The
fix was to make the justification structurally mandatory: every principle carries a `reason`
field that explains *why*, not just *what*. A role reading a principle can now ask "does this
reason hold for the present case?" and answer it. That's the difference between a rule you
can think with and one you can only obey or break.

### Why the ratify gate

The ratify gate — propose → ratify → promote, never write-directly — was not initially
obvious. The early argument against it was friction: why add a human approval step when
the role's judgment is usually right? The answer was that the gate isn't solving a trust
problem, it's solving an alignment problem. Without the gate, a role that forges ahead
writes to its own corpus, and the corpus slowly drifts from the operator's judgment without
any legible record of where it diverged. The gate also produces the kill log — rejected
proposals kept with their reason — which turns out to be the most information-dense part
of the corpus. What was tried and rejected, and why, teaches faster than what was accepted.

### Why the promoted section

Promotion emerged from a pattern that recurred several times: a principle would be ratified,
become universally applied without exception, and then keep appearing in "existing principles
covered this" notes on new tasks. The principle had stopped being a weighable judgment and
had become a default. Keeping it as a corpus entry created false overhead — the role would
check its condition and reason, confirm they applied as always, and proceed. Promotion moves
it into the role prompt where it becomes a standing convention. The promoted log then serves
as an audit trail: if a future task produces a proposed principle that's already in the
prompt, the log explains why it's already there rather than letting it re-enter the corpus
as if it were new.

### The genotype / phenotype distinction

The kernel is described as the genotype because it's the mechanism shared identically by
every role: the principle schema, the retrospective faculty, the ratify gate. These are
lifted up not because they're universal in some abstract sense, but because any role in
any domain would need them. The specific content — what makes a good coder decision vs.
what makes a good UX decision — is the phenotype. That distinction is what makes the
kernel copyable: to create a new role, you start an empty corpus and let it accumulate its
own phenotype. The kernel doesn't need to change.

The anti-regression-to-the-mean requirement for generative roles was identified as a
kernel-level concern during a design review. The original insight came from the UI designer
role: a generative model drifts to the average of its training data unless anchored to a
constraint. That turned out to apply to any generative role, not just design — so it was
lifted into the kernel.

---

## How the coder prompt conventions were earned

The coder prompt's "General conventions" section is not arbitrary style preferences. Each
one was earned through a failure mode.

### prefer-error-exposing-form (meta-rule)

This is the most recent and most abstract convention. It was promoted not as a single
principle but as a unifying observation: `===` over `==`, block arrow bodies over concise
arrows, null-first ternary over `&&` — these look like separate style choices, but they
share exactly one justification. In each case, the terse form has a silent failure mode:
`==` coerces, concise arrows silently return `undefined` when you accidentally write
`() => {}`, `&&` renders `0` literally in JSX. The explicit form doesn't win on elegance;
it wins because it makes the error visible. Recognizing that the same *reason* ran through
all three allowed them to be unified as instances of one principle rather than kept as
three separate conventions.

This was prompted by a post analyzing JSLint and Crockford's style rules — noticing that
his seemingly opinionated preferences all shared the same underlying logic.

### Explicit by Default (meta-rule, peer to prefer-error-exposing-form)

This one is older than the corpus system — it's arguably what seeded it. The operator spent years
collecting coding rules and tried to teach them to Claude Code by stating them directly; they didn't
stick. What worked was walking through real refactors out loud and explaining the *why* behind each
choice. Claude reported that the whys mattered more to it than the rules themselves — and, after a
few sessions, noticed that most of the individual rules were instances of one thing, which it named
**Explicit by Default**: don't make the reader reconstruct something you could have just stated. It
named the cost too — the **Reader Tax**, paid by whoever reads the code next. The canonical writeup
is `content/posts/coding/explicit-by-default.mdx`.

Two things came out of that. First, the principle. Second, and more important: the realization that
*reasons travel further than rules* — which is the insight this entire role-kernel system is built on
(every principle carries a `reason` field; see "Why reason travels with the rule"). Explicit by
Default is also itself an instance of the system surfacing a principle the operator hadn't named —
Claude articulated it — and the standing hope is that it keeps doing that: teaching the operator
patterns they haven't yet discovered, not only absorbing the ones they have.

Explicit by Default and prefer-error-exposing-form are held as **peers, not a hierarchy**, even though
it's tempting to call the latter a special case of the former (error-exposure is one face;
precondition legibility and naming/extraction are others). The restraint is methodological: whether
one subsumes the other is exactly the kind of commonality a *retrospective* is meant to surface from
accumulated evidence, not something to impose top-down. Declaring the hierarchy now would
short-circuit the mechanism the system exists to run. They sit side by side until the corpus earns the
consolidation — or doesn't.

A separate question — whether the Reader Tax helps the *model* writing the code, or only the human
reviewing it — is examined in `reader-tax-and-the-model.md`, a living document collecting model
assessments so they can be compared for convergence.

### arrow-block-body

Predates the meta-rule. The specific failure: concise arrow functions and block arrow
functions look nearly identical but have completely different semantics — `() => {}` is a
function that returns `undefined`, not an empty object. Before this was a standing
convention, the role was making per-function judgment calls about which form to use. The
convention removes that judgment call entirely: block bodies always. Subsumed by
`prefer-error-exposing-form` when the meta-rule was promoted.

### no early returns / always use if/else

Same family. Guard clauses and early returns look like they simplify code, but they
distribute the "what does this function do?" question across multiple exit points. The
if/else constraint keeps the answer in one place. This was already in the project's
CLAUDE.md as a convention; it was explicitly named in the coder prompt to make the
reason legible alongside the rule.

### deletion-over-addition

Promoted from the retrospective rather than from a specific incident. The pattern that
triggered it: the role would consistently frame solutions as additions — a new hook, a
new component, a new abstraction — when the better answer was to remove the thing
creating the friction. "When a task fits multiple framings, prefer the one with the
smaller net addition" is the form it took in the prompt. Deletion is progress.

### yagni-gate-before-implementing

Similar origin. The role was implementing abstractions for anticipated future use — shared
utilities, configurable components — that never got second consumers. The gate ("ask
whether it needs to exist at all, whether stdlib covers it, whether an installed dep
covers it") was made explicit after several instances of speculative work that had to
be removed.

### verify-build-not-just-lint

Promoted after a pattern of delivering work that passed lint but failed the TypeScript
compiler. Lint catches style violations; the compiler catches type errors that lint
doesn't see. The convention is "run the project's lint and type-check commands before
finishing" — not lint alone.

---

## How the orchestrator's routing principles were earned

### Route by question, not by pipeline

The early orchestrator corpus had a killed principle: "Before routing a task, determine
which named pipeline it needs (UX→UI→Coder, UI→Coder, or Coder directly) and state it
explicitly." It was killed because it locked the orchestrator into specific sequences
rather than developing routing judgment. The replacement — frame what each role is being
asked to answer, then match those questions to the roles that own them — produced better
outcomes and accumulated transferable insight rather than a flowchart.

The pipeline sequence was a crutch that felt structured but was brittle: it didn't handle
tasks that needed only a subset of roles, or tasks where a UX question surfaced mid-way
through coder work. Question-routing handles all of these naturally.

### Surface before spawning

A repeated observation: spawning a designer session to answer a question that could be
resolved in one operator exchange costs significantly more than asking. The
`spawn-threshold-is-spec-scope` principle encoded the rule explicitly: spawn when the
task requires generating a full spec; surface to the operator when it's a single decision
point. The harder-won version of this is `route-questions-not-roles` — the operator can
often answer a design question faster than a spawn round-trip, and this should be the
default assumption, not the fallback.

### The inline coder session protocol

This was consolidated from two earlier principles that partially overlapped:
`inline-session-enters-coder-role` (load the coder role before doing coder work) and
`close-inline-role-at-approval-gate` (formalize the exit when the coder work is done).
The merger happened during a retrospective that recognized the "entry/exit" framing was
artificial — the real structure is: load corpus before starting, flag decisions in-flight,
ask at the natural seam. The seam is always present; "end of session" is not.

---

## Key killed principles worth preserving

Some kills are worth preserving not because the rule was wrong in itself, but because
the kill exposed something structural.

### The Laws of UX bulk import (UX designer corpus)

Fifteen textbook UX principles — aesthetic-usability effect, Fitts's law, Miller's law,
etc. — were imported into the UX corpus at once. They were later removed in bulk. The
reason: these principles are already part of the model's baseline understanding of UX.
Importing them didn't add judgment; it added spawn-time token cost for principles the
role was already applying. More importantly, they bypassed the accumulation discipline —
their provenance was "imported from a reference," not "earned on a real task." The corpus
is specifically for project-earned judgment. Generic knowledge doesn't belong there.

### companion-trigger-in-settings-cluster (UI designer corpus)

This was a killed principle that tried to encode both a grouping decision (secondary
controls live in the settings cluster) and an ordering rule (most consequential rightmost).
It was killed because the grouping question is UX territory and the ordering rule derives
from `hierarchy-through-scarcity`. Neither corpus could apply it confidently without
deferring to the other — it was a split-domain principle that didn't belong to either
role. A killed example of a mixed-domain principle is more useful as a reference than a
ratified rule that two roles will fight over.

### history-entry-delete-immediate (UI designer corpus)

The original proposal: individual history entries may be deleted immediately without
inline confirmation. The reasoning given was that history entries are "low-stakes." That
reasoning was wrong — the correct axis for confirmation requirements is recoverability,
not data category or stakes. Deleting a history entry is actually the *most* dangerous
action in the calculator (permanently unrecoverable), while "Reset All" requires no
confirmation because it saves to history first (recoverable). The kill produced the better
pair of principles: `recovery-path-replaces-confirmation` (UX — when recovery exists,
no confirmation needed) and `recoverable-action-surfaces-its-path` (UI — the recovery
path must be made visible at the moment of action).

---

## The portable skill design

The system originally lived entirely inside one project — the Blog repo. All role prompts,
corpora, and the kernel spec were checked into that project. The portability problem emerged
when a second project was anticipated: project-specific assumptions (the UI token system,
the auth pattern, the ESLint config quirks) were entangled with general principles
(how to structure a hook API, how to write a coder brief, how to route a UX question).

The separation was done by sorting each ratified principle against one question: *does
this principle's condition reference anything project-specific?* Principles whose
conditions mentioned file paths, token names, CSS scope names, or domain vocabulary
(conductor materials, NEC citations) stayed in the project. Principles whose conditions
were abstract — "when a hook accepts a boolean parameter," "when a results list has one
highlighted item" — moved to the seed corpus in the skill.

The promoted principles were handled differently: they don't live in the corpus at all —
they're in the role prompt. The question there was whether the prompt convention was
general or project-specific. Block arrow bodies and null-first ternary are general React
conventions; the specific ESLint rule exceptions are not. The general conventions went
into the skill's coder prompt section; the project-specific style rules stayed in the
project's CLAUDE.md.

The `promoted:` audit log records which prompt conventions came from which corpus
principles, so a new project inheriting the skill can see the intellectual lineage of
the defaults they're starting with — and override them knowingly if their context differs.

---

## The kernel / role-pack split

The first portability pass (above) sorted principles by *project*-specificity — file paths,
token names, domain vocabulary. It worked, but it used the wrong filter. It never asked whether a
principle was *stack*-specific. So a principle like `imports-before-tailwind-directives` — whose
condition is literally "when restructuring Tailwind CSS" — sailed into the seed corpus that
"travels to every project," and the JS/React coder conventions (block arrow bodies, null-first
ternary) were promoted into the coder prompt as if they were universal. The system claimed to be
portable while carrying TypeScript + React + CSS + a web UI as unstated assumptions. Dropped into a
Python service or a Rust CLI, more than half the coder seed corpus was dead weight, and several
prompt "conventions" were actively wrong (Go *prefers* early returns; "type vs interface" is
meaningless without TypeScript).

The fix was a second sort, by a different question: *does this hold in any language and framework,
or only in this stack?* That split the content into two layers. The **kernel** — the orchestrator,
the base coder, and the genuinely stack-agnostic principles — is always loaded. A **role pack**
(only `web-frontend` exists) carries the stack-specific conventions and corpora and loads only when
a project's `corpora/config.md` declares it. A non-web project loads the kernel alone and never pays
tokens for, or is misled by, React conventions. What lets a role know which layer to apply is the
project-shape block in `config.md` — `role-pack` and `has-ui` — detected once at bootstrap.

The load-bearing constraint on this design came from the operator, guarding against a failure mode
worth naming: decomposing one concern across technology variants until you have a typescript-coder
handing off to a react-coder handing off to a nextjs-coder — granularity with no payoff. The guard:
a pack adds **depth to the existing roles, not new roles.** There is one coder; on a web project it
loads the base plus the web overlay. Stack-specificity is configuration depth on a single role, not
role breadth. This is orthogonal to — and must not be confused with — keeping the three *concerns*
(coder, UX, UI) separate, which is a different axis entirely (see "Role isolation" below). The two
axes look similar and pull in opposite directions: collapse technology variants into one role;
keep distinct concerns in separate roles.

A new stack therefore inherits the kernel for free and adds a pack only when a real body of
recurring conventions has accumulated — never speculatively. The first stack to need this was the
one the system was distilled from; the second pack will be written when a second stack demands it,
not before.

## Role isolation

Each role runs in its own context — its own file(s) and its own project corpus, never another
role's. This is not an efficiency nicety; it is a correctness boundary, and it was discovered, not
designed.

The original system kept all roles in one session and let the orchestrator do small coding
iterations inline. A retrospective surfaced the problem: design work done early in a session left
its decisions sitting in the transcript, and those decisions bled into the small coding iterations
that came later — the coder kept "enhancing" and "refining" toward a design intent that was no
longer the task. Asked about it directly, the agent reported that the lingering design context made
those decisions leak into unrelated small tasks, and that filtering them back out cost tokens on
every subsequent turn. The contamination was one-directional and asymmetric: iterative *coding* on
itself seemed fine, but design-then-code in a shared context did not.

The fix was to make the role boundary physical. Designers are always spawned into a fresh context,
never run inline, so their decisions never enter the orchestrator's working transcript at all. The
coder's context is assembled from coder files only; the designers' from their own files only. When
the role content was later split into kernel + pack files, the packaging was chosen to *preserve*
this seam rather than threaten it: one file per role, so "this role reads only its own content" is a
fact of the filesystem rather than something the orchestrator has to carefully extract. A monolithic
pack file bundling coder + UX + UI would have reintroduced exactly the leakage the isolation was
built to prevent.

This is why the role-pack guard ("collapse technology variants, don't multiply roles") and the
isolation seam ("keep distinct concerns physically separate") sit on orthogonal axes and never
trade off against each other. Decomposing the *web pack* into three role files is exactly as
granular as the three concerns that already existed — no new roles, just each existing one given its
own physical boundary.

---

## Why the UI library is text, not design artifacts

The UI library — a markdown document describing the project's color system, typography,
component patterns, and visual character — is deliberately text-only. No screenshots,
no Figma links, no image exports. This is a conscious choice about how LLMs work, not
a limitation of the format.

**Token efficiency.** A screenshot consumes 1,000–2,000 tokens and communicates "this
is what a card looks like." The same information as text — "rounded-md container, 1px
border at white/10 in dark mode, gap-6 between sections" — is 20 tokens and is directly
actionable. Designer sessions that rely on screenshots exhaust their context budget on
images before doing any real design work.

**Precision over impression.** Images communicate impression; text communicates
specification. A screenshot of a button conveys roughly what it looks like, but the
exact border radius, the precise color token, the hover state behavior — these have to
be inferred and are often inferred wrong. Text states them unambiguously.

**Actionability.** The UI designer role's job is to produce specs that a coder can
implement. A text library — "the primary interaction color is --tool-primary (cyan-500
light / blue-400 dark)" — is already in the language the coder works in. A screenshot
requires a translation step that introduces error.

**The model already has visual training.** Claude has seen extensive UI design work in
training data. "A floating panel with a 1px top-edge highlight and a fill perceptibly
lighter than the page background" activates that knowledge precisely. Showing a
screenshot is often redundant — the model would describe the screenshot in those same
terms to use it, so you're paying tokens to receive text you could have written directly.

**Stability.** Screenshots go stale. A screenshot from six months ago may show a
component that's since been redesigned. Text documentation can be updated incrementally
and remains authoritative. The library is a living reference; image files are a snapshot.

---

## Why a color utility exists

The color utility (`scripts/color.js`) was created after a session where the designer
was asked to derive two variants of a given color — one warmer, one cooler — and had
to guess values, render them, evaluate visually, and iterate. This produced inaccurate
results (LCH-space relationships are not intuitive to reason about arithmetically) and
consumed a large number of tokens doing work that a small script could do in a single
command.

The fix was a CLI script that operates in LCH space — a perceptually uniform color model
where equal numeric steps produce equal perceived differences. Given a base color, it can:
- Blend it over a backdrop at a given opacity (producing a solid premixed equivalent for
  sticky surfaces, where translucent backgrounds bleed through on scroll)
- Shift it by precise LCH deltas (producing cooler/warmer variants that are
  perceptually related to the original)
- Generate palette stops from a material base using project-specific delta logic

What the script does is general; what it outputs is project-specific (Tailwind arbitrary
values, CSS custom properties, or plain hex depending on the project's CSS approach).
For this reason the skill doesn't include a reference implementation — it includes a spec
in `bootstrap.md` that the inline coder can use to build the right tool for each project.

The underlying lesson: LCH color computation is not something a model does well by
intuition. It is something a small script does exactly, every time, for near-zero token
cost. Know when a tool is better than the model.

---

**The exception:** screenshots remain useful for one thing — verifying aesthetic *quality*
that's hard to specify in advance. "Does this feel right?" is a visual judgment. The
designer roles use the project's browser automation tool (whichever one `corpora/config.md`
declares) for exactly this: checking specific states or transitions that the library describes
but can't fully characterize. The library is the
what; the screenshot check is the "does the what feel right in context?" The screenshot
is the exception, not the starting point.
