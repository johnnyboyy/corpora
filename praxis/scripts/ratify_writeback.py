#!/usr/bin/env python3
# corpora-plugin script — corpora-specific orchestration (verbs resolved through the corpora engine
# manifest), distinct from praxis-core (root_tree, frame, handoff, engine).
"""ratify_writeback — the principle write-back verbs, dispatching scripted paths and flagging manual ones.

Migrated from corpora `processes/ratify-write-back.md`. The deterministic fact praxis carries here is
**which lifecycle operations corpora actually scripts vs which are hand-edit-only**, and never
pretending the latter are automated:

  - `add`    (a freshly-authored/mined ratified proposal) -> `add-principle`         [scripted]
  - `import` (a proposal sourced from an import candidate) -> `ratify-import-candidate` [scripted]
  - `reject` (into the kill log)                           -> no engine command       [manual]
  - `reshape` (history entry on an already-ratified one)   -> no engine command       [manual]
  - `graduate-convention` (principle -> convention)        -> no engine command       [manual]

The scripted verbs go through the single `engine.invoke` binding. The manual verbs invoke nothing
and print the exact hand-edit steps (working file + audit file) the process specifies — so a caller
is told plainly "this one has no script, here is the shape," rather than a wrapper implying a write
happened. That honesty is the point of migrating this as a script instead of dropping it: the
map of scripted-vs-manual is itself the deterministic surface.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402


def cmd_add(args) -> int:
    r = engine.resolve(Path(args.corpus_py), "principle-add", {
        "domain": args.domain, "id": args.id, "rule": args.rule, "condition": args.condition,
        "reason": args.reason, "provenance": args.provenance, "kind": args.kind,
        "see_also": args.see_also, "domains_dir": args.domains_dir, "audit": args.audit})
    engine.echo(r, "add-principle")
    return 0 if r.ok else (r.returncode or 1)


def cmd_import(args) -> int:
    r = engine.resolve(Path(args.corpus_py), "import-ratify",
                       {"id": args.id, "as_domain": args.as_domain, "as_id": args.as_id})
    engine.echo(r, "ratify-import-candidate")
    return 0 if r.ok else (r.returncode or 1)


MANUAL = {
    "reject": (
        "reject -> kill log (no engine command; hand-edit):\n"
        "  1. append to the domain WORKING file's `killed:` an entry with a stable `id`, a\n"
        "     `kill_type` (quality | container | attribution-noise), and `reason_killed`.\n"
        "  2. add per-kill audit detail keyed by the same id: its `provenance` and a required\n"
        "     `killed: <YYYY-MM-DD>` date (the date is what later enables kill graduation)."),
    "reshape": (
        "reshape -> history (no engine command; hand-edit):\n"
        "  add a `history:` item to the principle's audit-file `provenance` entry, each carrying\n"
        "  `date`, `type` (generalized | consolidated | split | moved), and `reason`. Moving a\n"
        "  principle to a better-fitting domain is a file move plus a `type: moved` history item."),
    "graduate-convention": (
        "graduate-convention -> conventions (no engine command; hand-edit, retrospective-time):\n"
        "  0. apply promotion restraint FIRST (the one judgment call): graduate only if the\n"
        "     judgment is stable across the kinds of projects the domain serves; when in doubt,\n"
        "     leave it in `principles:`.\n"
        "  1. move the entry from `principles:` to `conventions:` in the same working file,\n"
        "     dropping its `condition`, keeping `id`/`rule`/`reason`.\n"
        "  2. add a `type: graduated-to-convention` history item to its audit `provenance`."),
}


def cmd_manual(args) -> int:
    sys.stdout.write(f"[{args.cmd}] no engine command exists for this path — manual write-back:\n")
    sys.stdout.write(MANUAL[args.cmd] + "\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="ratify_writeback", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus-py", default=str(engine.DEFAULT_CORPUS_PY),
                    help="the corpora engine CLI (in-repo binding; tests override)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="add-principle: write a ratified freshly-authored/mined principle")
    a.add_argument("--domain", required=True)
    a.add_argument("--id", required=True)
    a.add_argument("--rule", required=True)
    a.add_argument("--condition", required=True)
    a.add_argument("--reason", required=True)
    a.add_argument("--provenance", required=True)
    a.add_argument("--kind", default="", choices=["", "judgment", "knowledge"])
    a.add_argument("--see-also", default="")
    a.add_argument("--domains-dir", default="")
    a.add_argument("--audit", default="")
    a.set_defaults(func=cmd_add)

    i = sub.add_parser("import", help="ratify-import-candidate: write a ratified imported entry")
    i.add_argument("--id", required=True)
    i.add_argument("--as-domain", default="")
    i.add_argument("--as-id", default="")
    i.set_defaults(func=cmd_import)

    for name in MANUAL:
        m = sub.add_parser(name, help="manual write-back (no engine command) — prints the exact steps")
        m.set_defaults(func=cmd_manual)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
