#!/usr/bin/env python3
"""chunk_ledger — the deterministic close sequence for a workstream's chunk ledger.

Migrated from corpora `processes/chunk-accounting.md`. That process's judgment content is nil; its
value is a **load-bearing ordering constraint**: `chunk-done` must run *before* `handoff-done`,
never after, because `chunk-done` fails if the handoff file it points at is already gone, and
`handoff-done` is what removes it. Ordering a sequence of engine calls and refusing to advance past
a failed step is exactly the orchestration praxis owns — so it is a praxis script, testable against
a stub engine, not prose a reader has to obey by hand.

What praxis enforces here (deterministic, tested):
  - the handoff file exists before anything is attempted (a praxis precondition — the handoff is a
    praxis primitive, so praxis checks its presence directly, no engine needed);
  - `chunk-done` runs first;
  - `handoff-done` runs ONLY if `chunk-done` succeeded — the ordering is a hard gate, not a hint.

Each verb is an engine call through the single `engine.invoke` binding; the ledger schema, the
`domains-composed` recomputation, and the fidelity checks all live in corpora and are not
re-derived here.

Commands:
  close   --workstream W --unit-of-work U --stance S --handoff FILE [--next U2]
            chunk-done then (only on success) handoff-done, in that order.
  preview --workstream W --unit-of-work U          chunk-start: print a composition, write nothing.
  summary --workstream W                           close-workstream: read-only ledger summary.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402


def close(corpus_py: Path, workstream: str, unit_of_work: str, stance: str, handoff: str,
          nxt: str | None) -> int:
    """Run the close sequence with the load-bearing ordering gate. Returns a process exit code."""
    handoff_path = Path(handoff)
    if not handoff_path.is_file():
        # Praxis precondition, before the engine is ever touched: chunk-done would fail on a missing
        # handoff anyway, but praxis owns the handoff primitive and says so in its own voice.
        sys.stdout.write(f"[precondition] FAILED — handoff file does not exist: {handoff}\n")
        sys.stdout.write("  chunk-done points at a handoff that must still be on disk; nothing run.\n")
        return 1

    args = ["chunk-done", "--workstream", workstream, "--unit-of-work", unit_of_work,
            "--stance", stance, "--handoff", str(handoff_path)]
    if nxt:
        args += ["--next", nxt]
    chunk = engine.invoke(corpus_py, args)
    engine.echo(chunk, "chunk-done")
    if not chunk.ok:
        # The gate: never close (delete/archive) the handoff a failed chunk-done still needs.
        sys.stdout.write("[handoff-done] not run — chunk-done did not succeed; handoff left in place "
                         "so the close can be retried in the correct order.\n")
        return chunk.returncode or 1

    done = engine.invoke(corpus_py, ["handoff-done", str(handoff_path)])
    engine.echo(done, "handoff-done")
    return 0 if done.ok else (done.returncode or 1)


def cmd_close(args) -> int:
    return close(Path(args.corpus_py), args.workstream, args.unit_of_work, args.stance,
                 args.handoff, args.next or None)


def cmd_preview(args) -> int:
    r = engine.invoke(Path(args.corpus_py),
                      ["chunk-start", "--workstream", args.workstream,
                       "--unit-of-work", args.unit_of_work])
    engine.echo(r, "chunk-start")
    return 0 if r.ok else (r.returncode or 1)


def cmd_summary(args) -> int:
    r = engine.invoke(Path(args.corpus_py), ["close-workstream", "--workstream", args.workstream])
    engine.echo(r, "close-workstream")
    return 0 if r.ok else (r.returncode or 1)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="chunk_ledger", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus-py", default=str(engine.DEFAULT_CORPUS_PY),
                    help="the corpora engine CLI (in-repo binding; tests override)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("close", help="chunk-done then handoff-done, in that load-bearing order")
    c.add_argument("--workstream", required=True)
    c.add_argument("--unit-of-work", required=True)
    c.add_argument("--stance", required=True)
    c.add_argument("--handoff", required=True)
    c.add_argument("--next", default="")
    c.set_defaults(func=cmd_close)

    p = sub.add_parser("preview", help="chunk-start: print composition, write nothing")
    p.add_argument("--workstream", required=True)
    p.add_argument("--unit-of-work", required=True)
    p.set_defaults(func=cmd_preview)

    s = sub.add_parser("summary", help="close-workstream: read-only ledger summary")
    s.add_argument("--workstream", required=True)
    s.set_defaults(func=cmd_summary)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
