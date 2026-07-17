# Lineage

This document explains how the system and its conventions came to be — not what they are
(that's `SKILL.md` and `kernel.md`), but why they are. It's for someone fresh to the repo
who finds a convention and wonders whether it's arbitrary, or for anyone returning after
a gap who wants the reasoning rather than just the rule.

Because it is a history, it records *decisions and their reasoning as dated events* — the
form of claim that stays true even after the code moves on. It is deliberately not the
authority on current state: where an entry explains why something was decided, whether that
decision still holds is answered by `kernel.md`/`SKILL.md`, not here. A present-tense state
claim ("X is in the kernel") is a defect in this document — it rots silently the moment the
code diverges. The durable form is "on `<date>`, we reasoned toward X, because…": verifiable,
and immune to staleness when the code later moves on.

*Dating convention.* The original body was authored 2026-06-19 (`951273f`); each section below
opens with an italic anchor giving the date and commit of the *decision it records*, which is
not the same as when these words were written. Events that predate this repo originated in the
**Blog** project, from which this system was distilled — they carry no commit here and are
marked as pre-repo. This document was dated and scoped in a pass on 2026-06-22, before the v1
snapshot, so the anchors reflect git history up to that tag.

---

## The kernel design

*Founding mechanisms, materialized at this repo's first commit (2026-06-19, `2ca7f6e`); the
promoted section (`d669829`) and the working/audit split (`8c22959`) landed the same day. The
"reason travels with the rule" bet has roots that predate this repo — see Explicit by Default
below. The anti-mean note was corrected in the 2026-06-22 pass and carries its own inline date.*

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

### Why the corpus splits into working and audit files

A cost analysis of role invocation surfaced that the coder's corpus carried roughly a quarter
of its tokens as material the coder never weighs while working: `provenance` (where a rule came
from), the `promoted:` audit trail, and the `killed:` log. The kernel already says as much —
`condition` and `reason` are what a role reasons over; `provenance` is "for audit and trust,"
a retrospective-time concern. So those fields were moved out of the loaded path into a sibling
`<role>.audit.md`, loaded only when the orchestrator ratifies or runs a retrospective.

The tempting alternative — have the orchestrator strip the fields at spawn time — was rejected
because the coder also runs *inline* (the orchestrator loads `coder.md` itself), where no spawn
step exists to do the stripping; a file-level split makes the leanness structural and identical
for both paths, with no runtime YAML surgery. The split was scoped to the coder: the designers'
provenance is already one-liners and they have no `promoted:` section, so their audit volume
(~6–7%) didn't justify a second file.

The one real hazard is that this looks like a violation of `full-corpus-on-spawn` (the principle
that bars excerpting the corpus by relevance). It isn't: the split drops no *principle* and makes
no relevance judgment — every active rule/condition/reason still loads in full; only uniform
audit metadata moves. That distinction is written into both `full-corpus-on-spawn` and the
kernel's "working vs audit" note so a future orchestrator doesn't "correct" the split back into
one file. The residual cost — `promoted:`/`killed:` are the guard against re-proposing an
already-decided principle, and the working coder no longer sees them — is borne by the
orchestrator, which retains the audit file and screens proposals at the ratify gate.

### The genotype / phenotype distinction

The kernel is described as the genotype because it's the mechanism shared identically by
every role: the principle schema, the retrospective faculty, the ratify gate. These are
lifted up not because they're universal in some abstract sense, but because any role in
any domain would need them. The specific content — what makes a good coder decision vs.
what makes a good UX decision — is the phenotype. That distinction is what makes the
kernel copyable: to create a new role, you start an empty corpus and let it accumulate its
own phenotype. The kernel doesn't need to change.

During a design review, the anti-regression-to-the-mean requirement was reasoned about as a
possible *kernel-level* concern. The original insight came from the UI designer role — a
generative model drifts to the average of its training data unless anchored to a constraint —
and the argument was that this generalizes to any generative role, not just design.

That generalization was asserted but never executed in the code. As of 2026-06-22 the
constraint lives as a single principle in the web-frontend UI designer pack
(`packs/web-frontend/ui-designer.md`), extracted there from the role's prompt — its real
motion has been *toward* domain-specificity, not into the kernel. The redesign argues that is
correct: anti-mean anchoring is load-bearing for *divergent* domains (design, where the value
is differentiation from the expected) and actively wrong for *convergent* ones (coding, where
the training mean is often the right answer — see `reader-tax-and-the-model.md` on idiomatic
brevity being low-cost). What might be genuinely kernel-level is only the thinner meta-claim —
that a generative role must know whether its domain rewards convergence or divergence and
anchor accordingly — and that abstraction is not worth writing until a second divergent domain
demands it. Verify against `kernel.md` for current state; do not infer from this paragraph
that anything lives in the kernel.

*Update, later 2026-06-22.* The thinner meta-claim did get written — see `kernel.md`, "Generative
stance," and "Domain-scoped corpora — the lens / corpus split" below. And the home sharpened once
more: anti-mean is a property of the divergent **lens** (the UI designer), not a divergent
*domain*. It is a generative *stance*, not a weighable principle — principles overwhelmingly encode
*convergent* correctness, because that is what crystallizes into a rule. So `reject-safe-defaults`
was promoted off the design-method corpus and onto the UI designer lens as its stance anchor. This
partly supersedes the "divergent-domain" framing in this paragraph: read it as divergent-*lens*.

### Roles are discovered, not org-charted

The early instinct was to model the system on a human team: a project manager coordinating a
coder, a designer, and so on — the org chart you would draw for people doing this work. That
instinct was wrong, and recognizing why sharpened the whole design. An LLM-mediated system does
not have the constraints a human org is structured around (limited working memory, communication
overhead, individual specialization, calendars). Importing the org chart drags those assumptions in
as dead weight and invents role boundaries that the work itself never asked for.

So the system inverts it: roles and their boundaries are *discovered from accumulated tension*, not
assumed up front. A role starts as a discipline guess (coder, UX, UI). Whether it is really one role
or two is then revealed by the corpus — when its ratified principles develop conditions that partition
the same space and give opposing advice, the *fork signal* surfaces a candidate seam (see kernel.md's
retrospective). The operator judges whether the partition is real. This is why "a second coder" is not
gated on "separate codebases" or on what a human team would look like, but on whether the role's own
accumulated judgment has split. Growth is differentiation under tension — never promotion up a ladder,
and never an org chart imposed in advance. It is a new frontier; the point is to discover its native
structure, not to make an old one work.

---

## How the coder prompt conventions were earned

*Most of these conventions were earned in the Blog project before this repo and captured here
2026-06-19. Explicit by Default predates the corpus system entirely (its canonical post is dated
2026-06-17 in Blog). In-repo landmarks: the real why for no-early-returns (`9ff2f52`), EbD
captured as a peer meta-convention (`40f9942`) and distinguished from the error-exposing form
(`3629582`), all 2026-06-19; the deferred EbD-vs-error-exposing tension was resolved 2026-06-20
(`f5695aa`).*

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

*Captured 2026-06-19. The inline-session design-question gate was made to work in inline coder
sessions the same day (`137dec4`); the `route-questions-not-roles` sharpening and the
fork-discovered-seam framing came from the external-review pass (`6fd9c39`, 2026-06-19).*

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

### Why the orchestrator inlines domain content rather than passing file paths

*Surfaced 2026-06-23, first full planner session on FAMOUS. No commit — a design rationale
confirmed in production use, not introduced by a code change.*

The kernel instructs the orchestrator to read each role's declared domain files and include
their content inline in the spawn prompt. The obvious alternative — pass file paths and let
the spawned agent read its own context — would reduce orchestrator token cost. It was
considered and rejected, for a reason worth recording.

A spawned agent told to read files before beginning will shortcut when the file name sounds
familiar, when the task context already feels rich, when the file is long and the first
section answered the obvious question, or when the agent has pattern-matched the file type
against training knowledge and assumed coverage. The failure is not random — it happens
precisely on the principles that feel obvious enough to skip. And the cost of underfetching
is not "the role missed some principles evenly" but "the role missed the one principle that
would have prevented the mistake it then made," which is the hardest failure to detect after
the fact.

The inline approach makes this underfetch impossible. The spawned agent cannot choose not to
have read a domain because the domain content is already in its context window.

A secondary effect emerged from the same session: inlining has a direct cost the orchestrator
feels, which enforces tight domain management. If the orchestrator pays tokens to relay every
domain it spawns with, bloated domains raise the cost of every spawn immediately and visibly.
Letting the agent read its own files diffuses that cost and removes the forcing function — the
feedback signal that tells you the domains are getting heavy.

---

## Key killed principles worth preserving

*These kills occurred in the Blog project (the calculator references predate this repo) and were
recorded here 2026-06-19. The Laws-of-UX bulk assessment and related seed-corpus scope fixes
were revisited in the 2026-06-20 corpus audit and retrospectives (`f23215b`, `dd0eac9`).*

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

*The first portability pass, authored 2026-06-19. Its filter (project-specificity) was found
insufficient the same day and superseded in framing by the stack-specificity sort in the next
section — read the two in order; this one is kept because the kill is instructive, not because
its filter is still the operative one.*

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

*Decided 2026-06-19 (`108d9ca`), building on the `config.md` project surface introduced the same
day (`85cb290`). "Only `web-frontend` exists" was current as of 2026-06-22; verify the pack list
against `packs/` for later state.*

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

*The contamination was discovered in the Blog single-session era (pre-repo); the physical-isolation
fix and this account were recorded 2026-06-19 (`108d9ca`). The "one file per role" arrangement
described below is the pre-redesign state as of 2026-06-22 — the redesign proposal revisits where
corpora live while deliberately preserving this isolation seam.*

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

## Domain-scoped corpora — the lens / corpus split

*Decided and executed 2026-06-22, across the skill and both projects (Blog, FAMOUS), in one pass.
The pre-redesign system is preserved at git tag `v1-alpha`; `redesign-proposal.md` (and
`redesign-proposal.v1.md`) hold the reasoning at length. Verify the current shape against
`kernel.md`, `SKILL.md`, and the `domains/` directories — this entry records why the move was made,
not a guarantee of present state.*

The original system welded two things into the **role**: a *reasoning lens* (how an agent thinks)
and a *corpus container* (where its learned judgment is stored). Because storage was welded to the
lens, every principle had to be owned by exactly one role — and that single-ownership constraint was
the source of the system's worst failures. Judgment that belonged to two roles was either fragmented
across both or killed for "role boundary" reasons rather than because it was wrong. Three concrete
symptoms, all visible in the corpora at the time:

- `documentation-before-screenshots` existed **byte-for-byte identical** in both the UI and UX seed
  corpora — shared judgment stored twice because the role was the container.
- FAMOUS killed three sound principles (`empty-state-must-offer-one-exit`,
  `pinned-escape-above-search-input`, `search-complexity-threshold`) as "lives in the UX corpus"
  while they were *alive* in the UX corpus — a redirect with nowhere to land, not a quality rejection.
- The keyboard-grid cluster (`discovery-grid-as-landscape`, `grounded-hover-reads-as-emergence`,
  `depth-signals-tier-in-discovery-grid`, plus the coder's 3D-implementation principles) was split
  across UX, UI, and coder corpora, with two of its design principles ending up in a *killed* section
  through attribution noise in a long multi-domain session.

The fix unwelds the two. A **domain** is a corpus scoped to a subject (color, recoverability,
spatial-metaphor), not a job title; judgment lives there. A **role** becomes a *lens* plus a *static
declaration* of the domains it loads. Multiple lenses may declare the same domain, so shared judgment
lives once (the UI and UX designers both declare `recoverability`, `validation-feedback`, and the
rest). The container-kill category disappears: a proposal that surfaces in any session is *filed in
the right domain* rather than killed for belonging to the "wrong" role.

Two design choices kept this from eroding what came before:

- **Static declaration, not runtime retrieval.** The lens names its domains in a checked-in
  `## domains` block (project-only domains are declared in `corpora/config.md`). Assembly stays a
  deterministic, inspectable filesystem fact — no agent makes a per-task relevance call on its own
  constraints. This is what let domain-scoping coexist with `full-corpus-on-spawn`: loading only the
  declared domains is a fixed contract, not a relevance judgment.
- **Role isolation preserved at the declaration level.** The coder declares coding domains and never
  design domains, so the design→code contamination the seam was built to prevent still cannot
  happen. Two *design* lenses sharing a *design* domain is allowed and intended — a different axis.
  Where a subject genuinely spanned the coder/design seam (FAMOUS's `spatial-metaphor`), the design
  principles and the coder's implementation principles were kept in separate same-subject domains
  (`spatial-metaphor` and `css`) linked by `see-also`, rather than merged — coherence by subject
  without breaking the hard seam.

The anti-regression-to-the-mean constraint found its honest home in this move: it lives in the
`design-method` domain (declared by both designers), confirming the earlier finding that it is a
divergent-design concern, not a kernel universal (see "The genotype / phenotype distinction").

What was deliberately *not* settled: whether the UI and UX lenses are really one role or two. The
redesign reorganizes their corpora into shared domains and leaves the fork signal to answer the
question from accumulated tension — if a shared design domain develops UI-vs-UX conditions that
partition the same space with opposing advice, that is the seam, surfaced by a retrospective rather
than assumed. The storage was unwelded from the lens precisely so that question could be answered by
evidence later instead of by convention now.

### Generative stance — the correctness/creative line

*Added later the same day (2026-06-22), in the same session, once the domain split was in place.*

The operator pressed on whether the correctness/creative split was "a hard line domains should never
cross." Working it through sharpened the whole model. The split is real — it is the convergent /
divergent mechanism from `reader-tax-and-the-model.md` — but it lives on the **lens**, not the
domain. A *convergent* lens (coder, UX designer, orchestrator) generates by matching a standard;
regression to the training mean is often the right answer. A *divergent* lens (the UI designer)
generates by differentiating, and carries an anti-mean anchor. The reason it is a lens property and
not a domain one: a principle — rule + condition + reason, weighable — almost always encodes
convergent correctness, because that is what crystallizes into a rule. The divergent element never
becomes a body of principles; it is a stance taken at the generative moment. Domains are therefore
mostly convergent guardrails, consumed by lenses of either stance.

This immediately repaid itself by exposing a flaw in the just-built taxonomy: `design-method` had
bundled `reject-safe-defaults` (a divergent-stance instruction — "resist the standard") beside
`clarity-over-polish` and the documentation rules (convergent — "prefer the clear/standard answer").
One domain telling the agent to hold two opposite stances at once. The fix was the hard line stated
precisely: a domain must not bundle principles that demand opposite generative stances. So
`reject-safe-defaults` left the domain and became the UI designer lens's stance anchor, and
`design-method` settled into a clean convergent process domain.

A bonus fell out, and it closed a long-standing puzzle. The operator had tried, on the prior system,
to make the *UI* more interesting by having design lead with *UX* — and it kept producing safe,
boring results. The stance model explains why mechanically: UX is the **convergent** lens. Leading
visual work with a convergent stance pulls it toward the default — the opposite of the intended
effect. The way to get a more divergent UI is to let the divergent lens lead, not to anchor it to
the convergent one. The role split the operator had felt was "both real and arbitrary" was a proxy
for the stance axis all along; the stance axis is the principled version of it.

### UI/UX seam settled — stance as the answer

*Settled 2026-06-22, closing the open question recorded at the end of "Domain-scoped corpora" above.*

The earlier note deferred the question of whether UI and UX are really one role or two, leaving it
for accumulated tension to answer. The stance model settled it without requiring a further
retrospective: the seam is the stance axis itself.

The **UX designer** is convergent — it aims for correctness. Usability, flow, and navigability have
better and worse answers; the lens generates by matching against those standards. The **UI designer**
is divergent — it aims for creative differentiation. Visual expression does not converge on a single
right answer; the lens generates by resisting the mean. These are not two specializations of the
same activity; they are opposite generative modes applied to adjacent subject matter.

This means the fork signal (a shared domain developing opposing conditions that partition the space)
is not what resolved it. The seam was visible the moment stance became a first-class lens property:
one lens is convergent, the other is divergent, and no future convergence of their domain corpora
would collapse that difference. The question is closed.

The practical consequence: a session that leads visual work with the UX lens — the convergent one —
will pull toward the mean before the UI lens has a chance to differentiate. The roles must be
sequenced so the divergent lens does its work before the convergent lens constrains it, or run
independently on separate concerns.

---

## Orchestrator as process — context-state routing

*Decided 2026-06-22, same session as the planner role and UI/UX seam entries above.*

The original system encoded the contamination finding (see "Role isolation" above) as fixed
per-role assignments: designers always spawn, coder always inline. The finding was correct; the
encoding was over-specified. The assignment was determined by which role was being invoked, not by
whether the session actually held incompatible context. That distinction matters because it makes
the system brittle: the rule cannot accommodate a new role (the planner) cleanly, and it prevents
the coder from spawning even when spawning would be cleaner.

The fix separates two things that were conflated:

1. **The orchestrator is a pure process layer.** It routes, spawns, relays, ratifies, writes back.
   It does not take on a role lens. In the original system the orchestrator "assumed the coder
   lens" for coding tasks — making it simultaneously a process and an actor. That dual role
   introduced its own contamination risk: the orchestrator session accumulated coder domain context,
   which could leak into subsequent routing decisions or relayed output. A pure process layer
   accumulates only `orchestrator-routing` context and structured artifacts — never role-domain
   content.

2. **Inline vs. spawn is a session-state decision, not a per-role rule.** The contamination
   finding holds — design context in a coding session contaminates. But the rule is: spawn when the
   session holds incompatible context; inline when it doesn't. A coder may run inline in a clean
   session. A designer must be spawned if the session has prior coder work. A planner may run
   inline or spawned depending on what the session already holds. The per-role assignments were a
   conservative approximation of this rule, not the rule itself.

The practical consequence: the inline path is available to any role when session state permits.
Divergent lenses (UI designer) should still be spawned in almost all cases — a divergent lens in
a convergent-context session is the most dangerous contamination direction — but the reason is
session state, not role identity. The rule is derivable from principle, not from a lookup table.

---

## Why the UI library is text, not design artifacts

*Rationale recorded 2026-06-19 (`660172b`). A design rationale about how LLMs consume reference
material, not a state claim — durable as written.*

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

*The utility was built in the Blog project (pre-repo); the skill's decision to ship a *spec*
rather than a reference implementation was recorded 2026-06-19 (`aabb436`).*

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

---

## Planner behavior and knowledge boundary

*Decided 2026-06-23 (pre-commit, same session as the planner role's introduction). Verify
current state against `planner.md` and `domains/planning.md`.*

The first real use of the planner role surfaced three failure modes in one session: it
proposed principles without the kernel schema (a vague placeholder instead of
`id / rule / condition / reason / provenance / status`), it pre-classified each proposal as
"judgment" or "knowledge" — work that belongs to the orchestrator at the ratify gate, not
to the role at proposal time — and it did orchestration work (routing decisions) after
writing the queue instead of stopping.

The first two were output format defects, fixed by making the principle schema explicit in
`planner.md` and adding a prohibition matching the coder's existing output block. The third
was a contamination effect: the planner ran inline, the orchestrator's context (including its
routing behaviors) was still live in the session, and the planner had no explicit instruction
to stop at the queue. The fix added the prohibition directly to the planner lens.

The question of whether to spawn the planner by default — as designers are spawned — was
raised and rejected. The dominant use pattern is inline coder iteration, not planning; making
the planner always-spawn would add isolation overhead to every invocation of a role that is
itself occasional. The explicit prohibition is the lighter and sufficient fix for a lens that
runs rarely and has a well-defined output boundary.

---

## Open questions in designer specs — from required to conditional

*Decided 2026-06-23 (same session). Verify current state against
`packs/web-frontend/ui-designer.md` and `packs/web-frontend/ux-designer.md`.*

Both designer lenses had "Open questions" as a required section in the spec format — a
structural slot that created pressure to fill even when there was nothing genuinely
unresolved. In practice this produced two failure modes: questions the designer could have
resolved from available material (the library, existing patterns, the UX spec), and
manufactured questions where none existed.

The UX designer already carried a softener ("keep this short; resolve most questions
yourself"), but it was still a required section. The fix made the section conditional in
both lenses: omit it entirely if there are none, try to resolve from available material
first, only surface what genuinely cannot be resolved. The resolution sources are named
explicitly so the designer knows what to check before surfacing: the UI library, existing
components, config, and the UX spec (if provided) for the UI designer; the UX library,
existing patterns, config, and inference from the user's goal for the UX designer.

---

## Planner signals: concern and judgment

*Decided 2026-06-23 (same session). Verify current state against `domains/planning.md`
(queue schema) and `planner.md` (decompose step).*

The queue schema needed a signal to help the orchestrator decide routing and spawn path
without the planner knowing which roles exist. The first attempt introduced `role-hint`
with values naming the current roles (`coder | ux-designer | ui-designer | planner`).
This was wrong on two counts: role assignment is orchestrator territory, and coupling the
field values to the current role taxonomy means a new role requires updating the planner —
the wrong dependency direction.

The replacement separates two things the planner can actually assess during orientation:

- **`concern`** — the character of the work, named from what orientation found (`visual`,
  `interaction`, `implementation`, or whatever the task actually involves). Open-ended
  and role-agnostic: the orchestrator knows which role handles `visual` work; the planner
  does not need to.
- **`judgment`** — `settled | uncertain` — whether established project patterns already
  cover this work, or genuine novel territory where judgment under uncertainty is required.
  Assessable from orientation: if the library covers the patterns, `settled`; if not,
  `uncertain`.

These two signals together give the orchestrator what it actually needs for routing and
spawn-threshold decisions, without the planner knowing the role taxonomy. A future role
added to the system slots in without touching the planner or the queue schema.

---

## Design spawn cost and the lighter path

*Decided 2026-06-23 (same session). The triggering case: a UI designer spawn for a page
that followed an already-documented subsystem. Verify the proposed principle against
`domains/orchestrator-routing.md` (`design-pattern-application-lighter-path`).*

A post-mortem on a designer spawn that cost roughly 20k tokens surfaced the pattern: a
full designer session loading the lens, all declared domains, and running the ratify gate
is justified when there is genuine visual judgment under uncertainty. It is not justified
when the work is applying documented vocabulary from the library to a new surface. In that
case the useful output — which tokens go where, resolving a pending library item — was
reachable without a spawn. The session produced three proposed principles that were killed
immediately as format violations, with their substance going to the library directly.

The `design-pattern-application-lighter-path` principle encodes the rule: when a design
task has `judgment: settled`, prefer reading the library, identifying gaps, and surfacing
them as targeted questions to the operator, rather than spawning the full designer. Spawn
only if the operator's answers reveal actual design judgment is needed. The principle is
currently `proposed` — the case was clear enough to earn the rule, but one instance in one
project is not yet ratification evidence.

The existing `spawn-threshold-is-spec-scope` and `route-questions-not-roles` principles
already pointed toward this, but neither covered the case where the orchestrator could
handle the gap-identification work itself rather than routing to a role or the operator.
The new principle names that third path explicitly.

---

## Planner scope expansion and the coder orientation gap

*Decided 2026-06-23, from a cross-model experiment comparing four implementations of the
same app. Verify current state against `domains/planning.md` (queue schema, `context` field;
`surface-shared-concept-before-implementation` principle) and
`packs/web-frontend/domains/coding-js-react.md` (four proposed principles).*

A comparison of four Pokemon Tinder implementations — three by Sonnet (one without the skill,
one with an early version, one without) and one by Haiku with the current skill including
the planner — surfaced two related findings.

**The planner expands scope and narrows coder orientation.** The Sonnet implementation using
the early skill (no planner) produced fewer features but higher correctness. The Haiku
implementation with the planner produced more features but several confirmed runtime state
bugs. The planner was working correctly: it decomposed a richer capability into actionable
tasks. The failure was structural. A coder working from a vague prompt must do its own
orientation — reading the codebase, understanding what exists, building the full state picture
itself. That process naturally surfaces interaction surfaces between features. A coder working
from a plan gets pre-digested context and may skip orientation, trusting the plan to have
captured what matters. The plan is a lossy summary: it records what exists and what to build,
but not what multiple tasks will share at runtime.

**The fix has two parts.** First, a new planning principle (`surface-shared-concept-before-implementation`)
requires the planner to detect when two or more tasks will operate on the same runtime concept
and surface it as a blocked open question before implementation begins. Second, the `context`
field description in the queue schema was updated to make explicit that the planner must
populate not just "what exists" but also "what this task shares with other tasks in this
capability" — so the executing role starts with the interaction surface visible.

**A domain gap in `coding-js-react` also contributed.** The confirmed bugs fell into three
categories with no ratified principles covering them: reading state in the same synchronous
scope as its setter (stale read), storing timer handles in state rather than refs (dep cascade),
and recording position rather than stable identity for deferred operations (undo/filter
interaction). A fourth, more general principle about frequent state in callback dep arrays
was added to cover the class. All four are proposed in `coding-js-react`; the planning
principle is proposed in `planning`. None were ratified outright — one project, one experiment.

**The model-specificity finding.** The planner increasing scope is correct behavior; the
domain corpus not having kept up with the failure modes that expanded scope introduces is
where the gap lived. The principle additions are the corpus catching up, not a constraint on
scope. Whether these principles hold across a second project is the condition for ratification.

---

## The empirical-signal pass — handoffs, counters, harvest, and stance as the seam

*Decided 2026-07-05, executed 2026-07-06, pre-commit. Provoked by a comparison against two
external systems: microsoft/SkillOpt (validation-gated skill-document optimization) and
uditgoenka/autoresearch (bounded metric-loop iteration). The four `*-proposal.md` files at the
repo root hold the reasoning at length; they follow the `redesign-proposal.md` convention and are
removed once resolved. Verify current state against `kernel.md` and `SKILL.md`.*

SkillOpt's thesis is a standing critique of this system: self-revision without an empirical gate
does not reliably improve over its starting point. The ratify gate filters what *enters* the
corpus; nothing measured what a principle did *after* it entered, and the decision of when to run
a retrospective rested on the operator manually watching token counts. The pass adopted the
critique's spirit under this system's constraint — judgment calls cannot be scored on a held-out
benchmark, but one can *count* whether a principle ever does work, and let the still-human-gated
retrospective act on counts instead of memory. Four changes landed together:

**The handoff artifact.** A role's terminal output became a file with a fixed envelope: what the
gate and relay mechanically consume (status, proposals with proposal-time provenance and a
role-assigned `kind`, violations, `ui-drift`) plus a freeform artifact body. The relay rule
("structured artifact, not raw transcript") had been an instruction the orchestrator interpreted;
the file made it a mechanism. The operator's worry — that a rigid schema might suppress what it
didn't anticipate — became the central design decision: a mandatory `Surfaced` section, relayed
verbatim, so the schema can under-fit but cannot suppress; recurring traffic of one kind in
`Surfaced` is itself the signal that the schema needs a field — evolution from accumulated
tension, like domain boundaries. The 2026-06-23 lesson ("Open questions — from required to
conditional") shaped its discipline: the section is always present but *expected empty*, never
filled from weak material. The unratified handoff also subsumed the deferred-proposals queue —
a lingering handoff file is a visible backlog. One prior decision was knowingly reversed: the
2026-06-23 planner entry had made "classify judgment vs knowledge" gate-time work, forbidding
roles from pre-classifying. The gate's own instruction had always admitted the tension — "the
role knows this from the inside — surface the distinction; do not evaluate it" — and the envelope
resolved it: the role *captures* `kind` at proposal time (when it knows), while evaluation and
ratification stay at the gate. The 2026-06-23 prohibition was aimed at the planner doing the
gate's job; the envelope keeps that boundary while moving the capture to where the knowledge is.

**Counters and the retrospective trigger.** Per-domain counters (ratified / killed /
gate-violations / working-file tokens since last retrospective) and per-principle efficacy counts
(fired / violated / idle), recorded as a byproduct of the gate's existing audit pass, in the audit
layer only. Thresholds *suggest* retrospectives; they never cap ratification — accumulation is
deliberate, because meta-principles condense out of piled-up specific ones (Explicit by Default
itself condensed that way). Co-firing clusters are meta-principle candidates detected from data
rather than noticed by luck; idle-dominant principles become retirement candidates instead of
invisible token cost. One hard line: efficacy counts never enter a working file, or roles would
learn to write principles that fire often instead of principles that are right.

**The `direction` route and mechanical library upkeep.** The gate had two exits — ratify into a
domain, or kill — and the stance model predicts a third category it couldn't file: a divergent
lens's output is an identity *choice*, not a weighable rule. The evidence was already in the
FAMOUS audit log (the RecencyBadge kill: "Component specification, not a principle… Substance
documented in UI library" — a sound direction processed as a failed principle, the library update
done as a workaround inside a kill reason; the container-kill pattern one level up). `kind:
direction` now files into the project's UI library at the gate. Coder-side library staleness got
its mechanical signal the same way: handoffs self-report `ui-drift`, counted only at gate time —
so experimental work that is discarded never reaches a gate and never triggers a sync, resolving
the tension between keeping the library current and not disturbing exploratory sessions. The
FAMOUS `design-queue.md` and Blog's pre-redesign `proposal-queue.md` were removed as subsumed.

**Stance became the session seam.** "Contamination" had bundled three harms. Untangling them:
(1) *stance corruption* — divergent anchoring is toxic to convergent generation and vice versa;
categorical, and now the hard seam (the UI designer always spawns). (2) *attribution degradation*
— the attribution-noise kill class arose in an all-*convergent* long session, so stance theory
alone would have called that session clean; the guard is per-transition handoffs (the gate reads
envelopes captured while each role's context was fresh, never a backward pass over accumulated
transcript) plus a mechanical length trigger. (3) *evaluator independence* — the reviewer's spawn
rule was never about contamination; a judge must not share a brain with the defendant. A residual
fourth — provisional-content bleed, an inline role resurrecting a predecessor's
considered-and-rejected option — is why spawn kept the heavier weight and "when in doubt, spawn"
survived as tiebreaker. This completes the trajectory begun in "Orchestrator as process": that
entry had already moved from per-role assignments to session-state routing but left "incompatible
context" underspecified; stance is the rule it was reaching for. The practical loosening:
convergent chains (planner → ux-designer → coder) became inline-eligible under the handoff and
length conditions. The length trigger's initial value (80k total session context) was not guessed
— it was derived 2026-07-06 from the transcript record of 91 FAMOUS and Blog sessions: baseline
load measured ~24–28k, a single role segment ~20–30k (the two corpus-recorded work units agree),
median session growth 59–106k beyond baseline, and sessions saturating at the ~166k compaction
ceiling — the zone the attribution-noise kills came from. 80k stops chaining early enough that
the incoming role's segment plus the gate's audit pass complete before that zone; roughly half of
the measured sessions would have been forced to spawn mid-way, which is the intended
conservatism. Verify the operative value against `SKILL.md` — this records only how the first
number was chosen.

**The engagement channel — the planner's flaw named.** The operator's real reason for preferring
inline was never token economy: it was the ability to engage a role about direction mid-work,
where a spawned role was fire-and-forget. The planner was the first attempt at this, and its flaw
became nameable: it moved dialogue *before* the work into a *different lens*, so it could only ask
decomposition-shaped questions, while the questions that matter arise inside the executing role's
lens mid-work. The fix is a channel, not co-location: `status: questions-pending` — a spawned role
stops, puts its direction questions in `Surfaced`, the orchestrator relays them verbatim, and the
*same agent is continued* with the answers. This extends `route-questions-not-roles` from
route-time to mid-work. The planner survives, rescoped to its own subject: gap-closing on the
capability description.

**Session harvest.** A third source for the reading pipeline: mining the project's own past
transcripts for judgment exercised but never proposed (operator corrections, retry chains,
reverts, ungated inline decisions), adapted from SkillOpt-Sleep's finding that correction chains
are the highest-precision failure signal available without an evaluator. It passes the
Laws-of-UX-kill test that bulk imports failed — harvested candidates are earned in real work, not
imported knowledge — and dedupes against active principles *and* kill logs before emitting. With
handoffs capturing proposals at the source, the harvester's steady state is backfill over the
pre-handoff era; the harvester finding little is the system working.

**What was deliberately not taken** from the comparison: autoresearch's thin-router token
architecture (the working/audit split already solves that problem, with the added property that
the orchestrator *feels* domain weight — see "Why the orchestrator inlines domain content"), and
SkillOpt's opaque single-document optimization, which trades away exactly the inspectability the
principle schema exists to provide. The falsifier for the loosened seam is named in the proposal:
a rise in `attribution-noise` kills or misfiled proposals from stance-clean inline chains — which
the new counters would surface — tightens the length threshold before the old seam returns.

---

## Bookkeeping moved to a script — and why this shipped an implementation, not a spec

*Decided 2026-07-06, same day as the empirical-signal pass it hardens. Verify current state
against `scripts/corpus.py`, `kernel.md` "Storage: working vs audit," and the gate steps in
`SKILL.md`.*

The counters and efficacy counts landed as instructions to the orchestrator — a model
incrementing integers and rewriting YAML at gate time. The evaluation that same day named the
flaw: the counters existed to replace fallible operator attention but were *maintained* by
fallible orchestrator attention, in a system whose own lineage documents that models shortcut
under context pressure. Bookkeeping done by attention is bookkeeping that silently stops — and a
counter that silently stops is worse than no counter, because it looks like evidence.

The fix drew the line at judgment vs arithmetic: the model classifies (fired/violated/idle,
ratify decisions) and passes its judgments as arguments; `scripts/corpus.py` does all counting,
token measurement, threshold evaluation, envelope linting, and writing, inside a
marker-delimited block of the audit file it alone owns. This also picked up a schema refinement
the thresholds forced: token *growth* needs a reference point, so `baseline-tokens` (measured at
the last retrospective) joined the counters block.

One precedent had to be consciously distinguished rather than followed. The color utility
shipped as a *spec* in `bootstrap.md`, not an implementation — because its output was
project-specific (Tailwind values vs CSS custom properties vs hex). The bookkeeping script is
the opposite case: the counters schema is kernel-defined and identical in every project, so a
reference implementation in the skill repo is correct and a per-project spec would just be N
copies of the same code drifting apart. The rule of thumb the pair suggests: ship a spec when
the *output* varies by project; ship an implementation when the *schema* is the kernel's.

*Extended later the same day (2026-07-06): reconciliation over interception.* The script
guaranteed the ledger was *accurate* but not *complete* — nothing forced `record-gate` to run,
and in this system a silently stale counter is worse than none, because low activity reads as
convergence: absence mimics the healthiest signal the retrospective knows. The considered fix —
a Stop hook blocking session end until the gate was recorded — was rejected because it would
put judgment ("did this session need a gate?") into the one component whose value is having
none. The adopted fix exploits the corpus files being append-only ledgers themselves: `verify`
counts entries per working file and requires them to equal baseline-plus-recorded, so an
unrecorded gate — or any write bypassing the gate, including a hand-edit — surfaces as a named
discrepancy. The check runs from a SessionStart hook rather than at session end, deliberately:
session end is where discipline dies (fullest context), session start is where attention peaks
— you can forget to record a gate, but you cannot start the next session without being told.
The same hook announces the project as corpora-managed, closing a second gap: skill activation
itself had been operator-remembered, so a coding session begun without `/corpora` loaded no
lens and no domains. The hook cannot force the load, but it makes the instruction deterministic
and present in every session's opening context. This is the system's first executable
enforcement — the deterministic shell around the probabilistic core.

---

## Cross-runtime portability — separating invariants from old tool constraints

*Decided and executed 2026-07-14 (`edf8b29`), while adapting the skill to run from the same
repository under Claude Code and Codex. Verify current state against `SKILL.md`, `kernel.md`,
`domains/orchestrator-routing.md`, and `scripts/corpus.py`; this entry records why the earlier
spawn and tool-surface conclusions changed.*

The portability review exposed a recurring category error in the system's history: a real concern
had become fused to the only mechanism the tooling offered at the time. Fresh spawning served
three purposes — keeping incompatible reasoning out of a role context, forcing the complete lens
and domains into the spawned prompt, and making corpus growth expensive because the orchestrator
paid to read and transmit it. Only the second is still a hard construction guarantee. Full role
content is still assembled and injected because a file path is not proof that an agent absorbed
the file. But paying twice was a necessary cost, never a desirable corpus budget; corpus size must
be measured and governed directly. The earlier lineage claim that duplicate load was a useful
forcing function remains historically true, but no longer states the design goal.

Agent continuation made the handoff boundary similarly visible as an implementation artifact.
A handoff is now a checkpoint, not agent death. A role agent persists through implementation,
operator testing, and small revisions inside one recognizable workstream; a new plan, unrelated
outcome, role change, unsafe context, or failed continuation starts a new instance. This preserves
the engagement channel without making the orchestrator absorb follow-up coding inline. Stance
interference, provisional-content bleed, evaluator bias, and context length remain routing evidence,
but none is an unconditional per-role spawn table. They live as weighable judgment in
`orchestrator-routing` and can harden into a kernel invariant later only if repeated evidence earns
that promotion. This supersedes the hard-seam and mechanical 80k conclusions in "The
empirical-signal pass" as operative policy, not as observations about the sessions that produced
them.

Delegation changed for the same reason. The old prohibition on a role spawning workers protected
the orchestrator from losing a child's handoff through parent summarization. The failure was relay,
not decomposition. Roles may now create same-stance scoped workers autonomously; implementation
results return to the parent, while questions, tradeoffs, proposals, violations, and routing
requests reach the orchestrator directly or verbatim through a `Delegated handoffs` envelope.
Cross-role and deeper delegation still return to the orchestrator because they change ownership.

The project config also stopped pretending to be a catalog of the runtime. Browser automation,
image generation, and delegation belong to the current environment and are discovered there.
Config now records stable project facts and project-owned deterministic utilities: small programs
that replace recurring precision-sensitive or disproportionately expensive inference. The color
utility was the motivating case, not a privileged category. Utility proposals deliberately have a
low surfacing threshold and a higher build threshold; accepted, denied, and deferred candidates
persist in `corpora/utility-candidates.md`, so a deleted handoff does not make recurrence depend on
operator memory. Non-blocking UI/UX questions gained the parallel
`corpora/deferred-decisions.md` queue: provisional treatments must be explicit and reversible,
while blockers still surface immediately. Both ledgers are validated by the deterministic script,
extending the judgment-versus-bookkeeping boundary established on 2026-07-06.

Finally, runtime portability became structural rather than forked: `SKILL.md`, relative bundled
resources, platform-appropriate project instructions at bootstrap, shared role files, and one
repository symlinked into both skill directories. Platform differences stay at activation and
runtime capability discovery; accumulated judgment stays singular.

*Extended the same day: derived recurrence, not attention-maintained counters.* The first utility
ledger schema stored `sightings`, `first-seen`, and `last-seen` beside its evidence, recreating the
bookkeeping defect this pass claimed to avoid: a missed increment looked like no recurrence. Those
fields were removed. The model still judges candidate identity and operator disposition;
`record-utility-candidate` appends evidence, while the script derives counts and dates and signals
when prior denial or recurrence should be resurfaced.

---

## Cutting the standing reviewer role

*Decided 2026-07-17, `0122c5d`. Verify current state against `SKILL.md`, `README.md`, and
`domains/orchestrator-routing.md`; this entry records why the base and pack-overlay reviewer
lenses were removed, not that a reviewer role is absent — check those files directly.*

The base `reviewer.md` and its `packs/web-frontend/reviewer.md` overlay were removed, along with
the ratify gate's "offer the reviewer" step. Two observations converged, surfaced in a Meridian
project retrospective conversation: the standing role was rarely invoked — the offer at the ratify
gate went declined often enough that its ongoing cost (a lens plus `coding-general` kept in step
with the coder's) wasn't earning its keep — and on the occasions review actually mattered, the
operator found a fresh, independent *coder* instance did the job better than the dedicated
reviewer lens. The dedicated lens added a name and a file without adding distinct judgment: the
evaluator-independence value that motivated it in the first place (see "Stance became the session
seam," above) comes from a fresh context evaluating producer work, not from that fresh context
running a reviewer-specific prompt. `prefer-independent-evaluation` in `orchestrator-routing` now
states the mechanism directly — spawn a fresh coder agent scoped to the review — rather than
pointing at a role that no longer exists. This is a narrower claim than deleting review itself:
the capability is intact, routed through the coder lens instead of a parallel one.
