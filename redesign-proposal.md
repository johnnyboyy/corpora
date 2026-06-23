# Corpora Skill Redesign

> Supersedes `redesign-proposal.v1.md`. The v1 problem statement still holds; this
> version resolves the open questions v1 left (assembly mechanism, UI/UX disposition)
> and grounds the diagnosis in concrete evidence from the FAMOUS project corpus.

## The thesis

The role construct currently welds together two things that should be separable:

1. **A reasoning lens** — the mode of judgment an agent applies (think like a coder, think
   like a UX designer, think about visual specification).
2. **A corpus container** — where the learned judgment that lens produces is stored.

Because storage is welded to the lens, every principle must be owned by exactly one role.
That single-ownership constraint is the source of the system's worst failures. It forces
principles that belong to two lenses to be fragmented or killed for the wrong reason; it
makes the corpus organization reflect role topology instead of the conditions that actually
surface decisions; and — most relevant to the operator's stated frustration — it means the
UI/UX seam, kept for a *reasoning* reason, drags a *storage* fragmentation along with it that
the operator never wanted.

**The redesign unwelds them.** Lenses stay (a role is still a prompt that supplies a mode of
reasoning). Storage moves to domain-scoped corpora that any lens can draw from. The operator
keeps the UX/UI distinction as a reasoning lens — to push design thinking toward abstraction —
while it stops being a corpus-ownership boundary that orphans cross-domain judgment.

---

## The evidence this is real, not theoretical

Three artifacts from the FAMOUS project corpus make the problem concrete.

**A coherent cluster split across roles.** The keyboard-grid design produced three principles
that explicitly depend on each other: `discovery-grid-as-landscape` (the UX frame),
`grounded-hover-reads-as-emergence` and `depth-signals-tier-in-discovery-grid` (the UI
constraints derived from that frame). The third cross-references the other two *in its own
condition field*. They are one body of judgment about one design idea — yet single-ownership
forced the frame into the UX corpus and the constraints into the UI corpus. The
cross-references became cross-role pointers the loaded path can't follow.

**Container kills — the smoking gun.** Three killed UI-designer principles share a kill reason
that is not a quality judgment at all:

- `empty-state-must-offer-one-exit` — *"Role boundary… Lives in the UX corpus."*
- `pinned-escape-above-search-input` — *"Role boundary… Lives in the UX corpus."*
- `search-complexity-threshold` — *"Role boundary… Lives in the UX corpus."*

These principles were surfaced in an inline orchestrator+coder session with no UX designer
present. The kill reason is a *redirect*, not a rejection — and there is no mechanism in the
current system to complete the redirect. The judgment is sound; it just has nowhere to go.
Under domain-scoping these three are never killed: they file by domain regardless of which
session produced them. This kill category disappears structurally.

**Attribution-noise kills — the system failing silently.** The three keyboard-grid principles,
some of the strongest-conditioned entries in the corpus, ended up in the UI designer's `killed`
section — not because they were wrong, but because a backwards pass over a very long,
multi-domain context window degraded enough to mishandle them. The current kill log cannot
distinguish "killed because wrong" from "killed because context noise." Those are opposite
epistemic events recorded identically.

Together these show the container is wrong: it forces good judgment to be fragmented (cluster),
orphaned (container kills), or lost (attribution-noise kills).

---

## What changes

### 1. Corpora are domain-scoped, not role-scoped

A corpus covers a subject matter / decision class — a *what is this about*, not a *whose job is
this*. This applies at both layers:

- **Seed corpora** (travel with the skill across projects) — organized by domain.
- **Project corpora** — organized by domain.

Multiple roles draw from the same corpus; shared judgment lives once. Domain boundaries are
**discovered from corpus tension** (the existing fork signal in the retrospective), never
declared upfront from how a team would be organized — the same discipline the lineage applies
to roles ("roles are discovered, not org-charted") now applies to domains. A domain split is
warranted only when accumulated principles within a domain develop conditions that partition
the same space and give opposing advice.

This subsumes, rather than conflicts with, the kernel/pack split. A stack overlay is just
conditional domain layering: `coding-general` (stack-agnostic) always loads; `coding-web-frontend`
(the web overlay) is declared only when `config.md` says `role-pack: web-frontend`. A pack still
adds depth to a role's declaration, never a new role.

**This is a storage reorganization, not a relevance filter.** Every principle in a declared
domain loads in full — `full-corpus-on-spawn` is preserved. The leanness comes from domain
boundaries (a coder session loads coding domains, not design domains), never from excerpting a
corpus by relevance. This distinction must be written into the design so a future maintainer
doesn't "optimize" domain-scoping into semantic excerpting.

### 2. Roles become a lens plus a static corpus declaration

A role is (a) a domain prompt — the reasoning lens — and (b) a **statically declared set of
domain corpora** it consumes. The declaration is checked into the role definition, not computed
at runtime.

This is the resolution to v1's central open question ("corpus assembly trust"). The trust
problem largely dissolves: there is **no runtime relevance judgment about a working agent's
constraint set.** Assembly is deterministic and inspectable — read the role file, know exactly
what loads. An agent never selects its own constraints; the constraint set is the same kind of
structural fact it is today, moved one level of indirection (from "the role's own file" to "the
role's declared domains").

Why static over the alternatives v1 floated:
- *Full injection of all active corpora* — token cost, and it reintroduces contamination
  (design principles loaded into a coder session).
- *Semantic retrieval* — an agent making a relevance call with a stake in the outcome; the exact
  trust problem, now load-bearing at working time.
- *Static declaration* — neither cost: the boundary is explicit, shared (many roles → one
  domain), and drift-proof.

### 3. Two load modes: working (lean, isolated) and audit (broad, human-gated)

This generalizes the existing working/audit file split from per-role to per-domain.

- **Working load** (hard isolation, generation): the role's statically declared domains,
  *working files only*. No kills, no provenance, no audit metadata. Lean and contamination-safe.
- **Audit load** (ratify, retrospective, backwards pass): the orchestrator may load relevant
  domains *broadly, including audit and kill logs*, because it is doing synthesis and
  ratify-prep — not constrained generation — and it is human-gated. Breadth is safe here for the
  same reason it is unsafe at working time.

The orchestrator's runtime judgment is therefore confined to (a) routing — which lens to invoke,
unchanged from today's route-by-question — and (b) ratify-time consultation — which domains to
read while reviewing a proposal. Neither silently shapes a working agent's constraints without
human involvement.

### 4. New domains are born at the ratify gate

The one place domain-scoping needs runtime judgment is when a session surfaces a principle in a
domain no role yet declares. That judgment lives at the **ratify gate**, where it is already
human-gated: the operator decides the principle's domain (creating a new domain corpus if the
tension warrants one) and updates the relevant role declarations to consume it. There is no
"homeless principle" problem — there is a single, legible, human-signed-off point where domain
assignment and declaration updates happen together.

### 5. Killed entries get stable ids and a kill taxonomy

Killed entries gain an `id` (consistent with ratified principles), making them referenceable via
`see-also`, queryable at ratify time, and traceable across sessions. A new proposal resembling a
killed entry surfaces the prior kill for operator review before ratification proceeds. The
`asymmetric-grid-encodes-entry-point` kill — *"underlying idea may resurface with better
framing"* — becomes an actual handle instead of a dead comment: when editorial-variation
judgment recurs, the prior attempt and its failure mode surface automatically.

Kills are not all the same epistemic event, and the redesign should make the difference legible:

- **Quality kill** — the principle was wrong, too narrow, misframed, or already covered
  (`ledger-form-in-discovery`, `asymmetric-grid`). The kill log working correctly. Highest
  signal — it pushes against model defaults.
- **Container kill** — "belongs to another role." Under domain-scoping this reason is no longer
  valid; these become filing decisions, not kills. The three FAMOUS `Role boundary` kills are
  the worked example.
- **Attribution-noise kill** — killed by context degradation, not merit. A *false* kill. These
  should be re-auditable: the retrospective should surface non-quality kills for re-examination
  rather than treating them as settled.

---

## The UI/UX disposition

The operator's torn feeling is itself diagnostic. The seam is enforced hard — but for a
*reasoning* reason (a UX-first abstract framing was hoped to push the UI designer toward more
interesting, less code-shaped designs), while the *storage* fragmentation it drags along
(rampant cross-domain leakage, the three container kills, the split cluster) is unwanted. The
weld is the whole problem: the operator wants the lens and is paying for it in corpus damage.

Unwelding resolves the tension without forcing a premature call:

1. **Reorganize the corpora by domain now.** This is safe (storage-only) and it is the system's
   own mechanism for answering the role question: merge the UX and UI project corpora into domain
   corpora and let fork signals reveal whether a real UX/UI partition exists. If domain tension
   surfaces — opposing advice about the same decision class — there is evidence for a seam. If it
   doesn't, the split was convention. Either way assumption is replaced by evidence.
2. **Keep the lenses as invocation modes, decoupled from storage.** Two lenses can draw from
   overlapping domain corpora. The operator keeps the UX-framing invocation where it's cheap (a
   prompt), and it stops dictating where judgment lives.
3. **Stop asking the seam to fix "safe and boring."** Regression-to-the-mean is a kernel-level
   concern for generative roles, and process architecture (UX→UI handoff) was never the right
   tool for it. The right tool is accumulated anti-mean principles with conditions and reasons,
   earned on real work. The lens can frame; only the corpus can constrain.

So: do not pre-merge into one designer role, and do not keep the two-role split as load-bearing.
Domain-scope the corpora, run the retrospective, and let the fork signal make the call.

---

## What stays the same

- The principle schema (`id / rule / condition / reason / status / see-also`).
- The ratify gate (propose → ratify → write-back, human sign-off required).
- The working/audit split — now generalized from per-role to per-domain.
- **Role isolation.** Designers still spawn into fresh contexts; the one-directional design→code
  transcript contamination this prevents is untouched. Domain-scoping changes *what* loads into
  an isolated context (declared domains instead of a role's own file), never *whether* it is
  isolated. This is the point the lineage is most emphatic about, and the redesign preserves it
  deliberately.
- The retrospective and its signals; the kernel lifecycle (spawn, accumulate, fork, converge).
- Killed entries injected at runtime as active guidance.

---

## Explicit non-goals

- **Backwards-pass redesign.** The observation that a single end-of-session backwards pass may
  beat per-turn surfacing — and that it currently has to be manually triggered over long
  multi-domain windows — is real but out of scope here. Domain-scoping happens to position the
  orchestrator-as-router to run such a pass naturally (it already spans domains at audit time),
  but designing the trigger is a separate, interaction-pattern concern. Noted, not solved.
- **Checkpoint detection in iterative sessions.** The "Great, now let's…" seam detector failing
  in long multi-concern sessions is an interaction-mode problem, not a corpus-organization one.
  Out of scope.

---

## Open questions

- **Corpus proliferation and budget.** Domain-scoped corpora could multiply. The fork-signal
  discipline bounds *creation* (no domain without earned tension), and static declaration bounds
  *per-invocation load* (a role loads only its declared domains, not all active ones) — but a
  hard budget ceiling per invocation is still an implementation decision.
- **Declaration audit.** Role declarations can go stale or over-broad. The retrospective should
  probably gain a check ("is this role declaring a domain it never draws from?"), but the
  mechanism isn't designed here.
- **Migration order.** Reorganizing existing project corpora into domains, re-auditing the
  non-quality kills, and rewriting role files into lens+declaration form is a sequenced
  migration. The order — and whether to do FAMOUS first as the proving ground — needs a plan of
  its own.
