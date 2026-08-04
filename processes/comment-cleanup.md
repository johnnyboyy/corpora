---
name: corpora:comment-cleanup
description: Sweep a managed project's code comments against coding-general's comment-shape principles — delete what's redundant, version-pin what's a real framework quirk, and queue everything else for a concrete non-comment fix (regression test, named constant, or type/assertion). Run on operator command (comment-cleanup [target]), never automatic.
---

# Comment cleanup

**Trigger:** operator command, `comment-cleanup [target]` (target is an optional directory or file
list; defaults to the whole source tree, excluding tests). Never runs automatically — same
standalone posture as `processes/architecture-scan.md`: this scans the target project's actual code,
not corpora's own corpus, so there is no mechanical trigger for it.

**Composition:** `corpus.py select --unit-of-work cleanup-comments` — pulls in `coding-general`
(this process's own governing principles: `minimize-comments-prefer-self-documenting-code` as the
umbrella, plus its five comment-shape siblings — `framework-quirk-comment-needs-version-pin`,
`magic-number-domain-fact-becomes-a-constant-name`, `ceiling-comment-for-deliberate-shortcuts`,
`past-bug-comment-belongs-in-a-test-not-prose`, `unverifiable-invariant-comment-encode-dont-narrate`)
plus `testing` (what counts as an adequate regression test for the past-bug redirect) and any other
domain whose frontmatter opts into this unit of work. Stack-specific domains (`coding-ts`,
`coding-react`, ...) are deliberately not pulled in by default — this process is about the *comment*,
not the surrounding code style; a project can add `cleanup-comments` to a domain's own
`units-of-work` if that domain's judgment genuinely bears on this pass.

## The test

Every comment gets exactly one of three outcomes. There is no "leave it, it seems fine" outcome —
the five sibling principles above each name a shape a load-bearing comment might take, and every one
of them redirects somewhere:

1. **Delete now** — the comment restates what the code already says, is a decorative divider, is a
   past-bug/tradeoff narration with no live guard (see below), or is stale/actively wrong (verify
   against the current code before trusting an old comment's claim).
2. **Rewrite now** — the comment is a genuine framework/library quirk workaround but doesn't name
   the exact package and version it's true of. Add the pin by checking `package.json` (or the
   project's actual manifest) for the installed version. This is the only case that survives as a
   permanent comment, and only once version-pinned.
3. **Queue for follow-up** — the comment is load-bearing but the fix is a real code change, not a
   comment edit: write a missing regression test, extract a magic number into a named constant, or
   encode an invariant as a type/assertion. Do not attempt the restructuring inline during this
   pass — queue it (`corpora/comment-cleanup-queue.md`, create if absent) with the concrete action
   required, not just "load-bearing." A queue entry that just says "keep" has failed this process;
   every entry must name what would make the comment unnecessary.

## Procedure

1. **Scope.** If the operator named a target, scope to it. Otherwise walk the whole source tree
   (exclude test files and directories — a test's own comments are a much smaller, different
   surface and not this process's concern). Batch by directory for parallel review if the tree is
   large; keep each batch's file list disjoint so parallel agents never edit the same file.

2. **Per comment, apply the relevant sibling principle:**
   - Restates the code, or is a decorative divider → **delete**
     (`minimize-comments-prefer-self-documenting-code`).
   - Explains a past bug/regression → grep the project's test suite for a test that actually
     guards the described behavior (by filename, ticket/error id cited in the comment, or
     described symptom). Found one → **delete** the comment (the test is the guard now). Found
     none → **queue**: "write a regression test for `<what the comment describes>`, then delete
     this comment" — do not write the test as part of this pass; that's real implementation work
     with its own verification burden, not a comment edit
     (`past-bug-comment-belongs-in-a-test-not-prose`).
   - Explains a framework/library quirk → **rewrite** to name the exact package(s) and pinned
     version(s) (check the manifest/lockfile), if not already present. Already pinned and still
     accurate → leave as-is (this is the one case where "leave as-is" is a valid outcome, and only
     after the version-pin check confirms it's actually pinned)
     (`framework-quirk-comment-needs-version-pin`).
   - States a domain/hardware fact behind a magic number or literal → **queue**: "extract into a
     named constant, e.g. `<suggested name>`, then delete this comment." Do not perform the
     extraction inline (`magic-number-domain-fact-becomes-a-constant-name`).
   - Narrates a deliberate tradeoff → is there a stated, live upgrade condition (the
     `ceiling-comment-for-deliberate-shortcuts` shape: "upgrade to X when Y")? If yes, leave it —
     that's the one tradeoff shape this principle already treats as legitimate. If no (it's just
     "we considered X and Y, picked Y" with nothing to re-check later) → **delete**; that belongs
     in the commit message, not the source.
   - Asserts a non-obvious invariant → **queue**: "encode as `<a type / a runtime assertion / a
     test>`, then delete this comment." Do not perform the encoding inline
     (`unverifiable-invariant-comment-encode-dont-narrate`).
   - Is a functional pragma (`eslint-disable`, `@ts-expect-error`, `@vitest-environment`, or any
     other directive a tool reads) → leave completely alone, don't even log it.

3. **Absolutely no behavior changes** in steps 1-2 beyond the comment edits themselves (delete a
   comment line, or rewrite one to add a version pin) — no renames, no extractions, no logic
   changes. That's what step 4 queues for separately.

4. **Write/update the queue file** at `corpora/comment-cleanup-queue.md`: one entry per queued
   comment, `file:line — required action — one-line why`. If the file already exists from a prior
   pass, reconcile rather than duplicate — an entry whose comment no longer exists (deleted, or the
   surrounding code changed) gets removed; a new entry gets appended.

5. **Verify.** Run the project's typecheck/lint/test commands (`corpora/config.md`'s
   `verification-commands`). Comment-only edits (deletions and version-pin rewrites) should never
   break any of these — a failure means a step 1-2 edit touched something it shouldn't have; fix it
   before reporting done.

6. **Report to the operator**: counts (deleted / rewritten / queued) per batch and in total, any
   comment found to be actively stale/wrong (corrected in step 1, called out explicitly since that's
   a real defect, not routine cleanup), and the queue file's current size. Relay verbatim — this is
   a `Surfaced`-style report, not a summary that hides the queue's actual size behind a favorable
   framing.
