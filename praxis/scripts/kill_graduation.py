#!/usr/bin/env python3
"""kill_graduation — the two-phase retire-an-old-kill sequence, with the no-auto-graduate discipline.

Migrated from corpora `processes/kill-graduation.md`. The process is deliberately two-phase with a
JUDGMENT gate in the middle: `kill-report` lists candidates old enough to consider (a fact), the
retrospective judges whether the killed idea has actually stopped recurring (judgment —
`domains/retrospective.md`'s `kill-graduation-judged-not-assumed`), and only then does
`graduate-kill` demote a *specific* judged id.

The praxis-owned deterministic content, tested here:
  - `candidates` is read-only and lists; it never demotes anything;
  - `graduate` demotes exactly one explicitly-named id — it will not batch, and there is no "graduate
    all candidates" verb, because age is a precondition, not evidence. Praxis structurally refuses to
    turn the report into an action, which is what keeps the judgment gate from being skipped.
  - both verbs carry the domains-dir + audit pair through (the process notes these commands work on
    any pair — a project's `corpora/domains/` or the skill's own `domains/` — not a `--for-file`).

Commands:
  candidates --domains-dir D --audit A [--min-age-days N]   list, read-only (kill-report)
  graduate   --domains-dir D --audit A --domain X --id ID   demote one judged-safe id (graduate-kill)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402


def cmd_candidates(args) -> int:
    call = ["kill-report", "--domains-dir", args.domains_dir, "--audit", args.audit]
    if args.min_age_days is not None:
        call += ["--min-age-days", str(args.min_age_days)]
    r = engine.invoke(Path(args.corpus_py), call)
    engine.echo(r, "kill-report")
    return 0 if r.ok else (r.returncode or 1)


def cmd_graduate(args) -> int:
    # One id, explicitly named. No path here batches or reads the report back — the judgment that
    # this specific kill is safe to retire happened in the retrospective, out of band, on purpose.
    r = engine.invoke(Path(args.corpus_py),
                      ["graduate-kill", "--domains-dir", args.domains_dir, "--audit", args.audit,
                       "--domain", args.domain, "--id", args.id])
    engine.echo(r, "graduate-kill")
    return 0 if r.ok else (r.returncode or 1)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="kill_graduation", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus-py", default=str(engine.DEFAULT_CORPUS_PY),
                    help="the corpora engine CLI (in-repo binding; tests override)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("candidates", help="list graduation candidates (read-only)")
    c.add_argument("--domains-dir", required=True)
    c.add_argument("--audit", required=True)
    c.add_argument("--min-age-days", type=int, default=None)
    c.set_defaults(func=cmd_candidates)

    g = sub.add_parser("graduate", help="demote one explicitly-named, judged-safe killed entry")
    g.add_argument("--domains-dir", required=True)
    g.add_argument("--audit", required=True)
    g.add_argument("--domain", required=True)
    g.add_argument("--id", required=True)
    g.set_defaults(func=cmd_graduate)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
