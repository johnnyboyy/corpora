# The Reader Tax, From the Model's Side

*Explicit by Default* — don't make the reader reconstruct something you could have just stated —
was distilled from years of human code review, and its cost, the **Reader Tax**, is obviously paid
by humans. But this system increasingly has a *model* as the next reader and editor of the code it
writes. So there is a prior question worth interrogating directly, because the whole skill implicitly
bets on the answer: does explicitness help the **model**, mechanically — or only the human who
reviews afterward?

This document collects model assessments of that question so they can be compared. The interesting
signal is not any single answer; it is whether independent models, asked the same thing, **converge**.
If several give the same account of *why* explicitness helps them, that is evidence the account is
real rather than a plausible-sounding confabulation. If they merely rhyme, that is weaker but still
informative. If they diverge, the principle's model-side justification is shakier than its human-side
one — and worth leaning on less.

The canonical statement of the principle is the post `content/posts/coding/explicit-by-default.mdx`
in the Blog project. Read it first; the assessments below assume it.

**On method and epistemics.** These are introspective and architectural assessments, not
measurements. No model has privileged access to its own weights or decoding; each is reasoning from
how the transformer architecture is known to work, plus the chain-of-thought literature, plus
observed behavior. Treat them as well-grounded models of the mechanism, not as data. The actual test
is empirical, and this system will run a version of it over time: hold two corpora — one carrying
reasons, one rules-only — and compare downstream code quality.

---

## Assessment — Claude Opus 4.8 (2026-06-19)

Short answer: yes, low Reader Tax helps the model, but the mechanism differs from the human one, and
the difference sharpens the principle rather than just restating it.

**1. Explicitness offloads reconstruction onto the context — the same move chain-of-thought makes.**
When a model generates or reads code, every token is conditioned on a single forward pass over what
is already there. Anything *implicit* — `&&`'s falsy semantics, an early-return precondition, a
parameter named for its caller instead of its purpose — has to be *recomputed* inside that forward
pass, under fixed compute, every time it becomes relevant. Anything *explicit* is simply present in
the context to be attended to. Writing the precondition into the indentation, or the intent into the
name, is the code-level equivalent of "show your work": it moves reasoning out of the activations and
onto the page, where it is cheap and reliable. The chain-of-thought literature is the strongest
available evidence that externalizing intermediate state into tokens improves a model's accuracy, and
explicit code is externalized state.

**2. The writer is also the reader, continuously — so implicitness derails generation itself, not
just later review.** A human pays the Reader Tax later, and usually someone else pays it. When a model
writes a misleading name early in a function, it then conditions *the rest of that same generation* on
that name's implied semantics — so the implicitness can corrupt the code it is about to write, not
only confuse a downstream reviewer. Ambiguous forms raise the model's own error rate at write time.
`() => {}` is the clean example: it is genuinely ambiguous in the token stream (empty body vs. intent
to return `{}`), so a model can resolve it the wrong way exactly as a human can. Error-exposing forms
reduce the *model's* mistakes, not only the human's.

**3. Names and locality are the highest-leverage cases.** Identifier names are very high-signal
tokens; a model leans on them as semantic anchors far more than it traces data flow to verify them, so
a good name does real work and a misleading one actively pulls generation toward wrong continuations.
Locality matters because long-range, multi-hop attention is where models get unreliable (the classic
"needle in a haystack" / multi-hop degradation). Keeping a fact next to its use shortens the
dependency chain the model must resolve. Both map directly onto the post's hook-naming and
precondition examples.

**4. The tax is on ambiguity and implicitness, not on brevity — and this is where the model and human
cases diverge.** A terse but highly *idiomatic* one-liner (`items.filter(x => x.active)`) is *low*
entropy for a model: seen a million times, easy to continue. Verbosity is not free either — more
tokens means more context consumed and more individual points at which generation can diverge. So
"explicit even at the cost of verbosity," stated baldly, is not strictly a model-positive. The win
comes specifically from removing *ambiguity, silent failure modes, and invisible preconditions* — not
from adding words. For the model-as-reader, the operative form of the principle is closer to
**"minimize ambiguity and implicit preconditions"** than "prefer the longer form." This is a candidate
refinement the corpus could surface in a future retrospective.

**5. The instruction level is the cleanest existing evidence.** The operator found that giving Claude
the rules *with their whys* worked where bare rules did not. That is the Reader Tax applied to
instructions rather than code: the reason was implicit in the rule, the model reconstructed it badly,
and stating it explicitly fixed that. The entire "reason travels with the rule" architecture is the
same bet at the meta level, and it paid off observably. The experiment has, in effect, already been
run once.

**6. The stakes are rising: the next editor is increasingly a model.** The intuition that the Reader
Tax is "really" a courtesy to a future human is becoming outdated. In workflows like this one, the
next reader and editor of the code is often an LLM. Optimizing code for model-readability is shifting
from a secondary nicety to a first-order concern.

**Bottom line.** Explicit by Default helps the model for partly different reasons than it helps the
human — externalized reasoning, names as anchors, shorter dependency chains, fewer ambiguous forks —
with the important caveat that the operative target is *ambiguity*, not *length*. Even if the
model-side benefit were zero, human review would justify the principle; but my assessment is that the
benefit is real and, for an LLM-in-the-loop codebase, growing. The honest limit: I cannot measure my
own decoding, so this is a grounded model of the mechanism, not a fact about it.

---

## Other model assessments

To add one: a different model reads this document and the post, then appends a dated, attributed
section below — ideally responding to the numbered claims above (agree / disagree / refine) so
convergence and divergence are legible at a glance. Independent agreement on the *mechanism* is the
signal worth collecting; bare agreement on the conclusion is not.

```
## Assessment — <model name> (<date>)

<short answer>

On claim 1 (offloading / CoT): <agree | disagree | refine> — <why>
On claim 2 (writer-is-reader): ...
On claim 3 (names & locality): ...
On claim 4 (ambiguity not brevity): ...
On claim 5 (instruction-level evidence): ...
On claim 6 (rising stakes): ...

<anything the claims above missed>
```
