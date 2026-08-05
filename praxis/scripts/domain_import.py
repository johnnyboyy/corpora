#!/usr/bin/env python3
"""domain_import — the browse -> file -> ratify import sequence for pulling ratified content in.

Migrated from corpora `processes/domain-import.md`. No composition of its own; the one judgment
point (which destination domain a picked entry belongs to) is the ratify gate's existing
`domain-assignment-at-ratify-gate` judgment, reused. The praxis-owned deterministic content is the
**ordering discipline**: browse first and propose nothing (`import-list` is read-only), then file
candidates one at a time or in a shape-matched batch, then ratify each individually. The verbs are
corpora's; the "browse before you propose" separation is the orchestration praxis keeps intact by
giving `browse` no side effects and never folding it into `file`.

Commands:
  browse     --source DIR                                   import-list (read-only, proposes nothing)
  file       --source DIR --domain X --id ID [--as-domain D2] [--as-id ID2]   one candidate
  file-pool  [--source DIR]                                 import-default-pool (shape-matched batch)
  ratify     --id ID [--as-domain D2] [--as-id ID2]         ratify-import-candidate (per entry)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import engine  # noqa: E402


def cmd_browse(args) -> int:
    r = engine.invoke(Path(args.corpus_py), ["import-list", "--source", args.source])
    engine.echo(r, "import-list")
    return 0 if r.ok else (r.returncode or 1)


def cmd_file(args) -> int:
    call = ["import-candidate", "--source", args.source, "--domain", args.domain, "--id", args.id]
    if args.as_domain:
        call += ["--as-domain", args.as_domain]
    if args.as_id:
        call += ["--as-id", args.as_id]
    r = engine.invoke(Path(args.corpus_py), call)
    engine.echo(r, "import-candidate")
    return 0 if r.ok else (r.returncode or 1)


def cmd_file_pool(args) -> int:
    call = ["import-default-pool"] + (["--source", args.source] if args.source else [])
    r = engine.invoke(Path(args.corpus_py), call)
    engine.echo(r, "import-default-pool")
    return 0 if r.ok else (r.returncode or 1)


def cmd_ratify(args) -> int:
    call = ["ratify-import-candidate", "--id", args.id]
    if args.as_domain:
        call += ["--as-domain", args.as_domain]
    if args.as_id:
        call += ["--as-id", args.as_id]
    r = engine.invoke(Path(args.corpus_py), call)
    engine.echo(r, "ratify-import-candidate")
    return 0 if r.ok else (r.returncode or 1)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="domain_import", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus-py", default=str(engine.DEFAULT_CORPUS_PY),
                    help="the corpora engine CLI (in-repo binding; tests override)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("browse", help="import-list: read-only, proposes nothing")
    b.add_argument("--source", required=True)
    b.set_defaults(func=cmd_browse)

    f = sub.add_parser("file", help="import-candidate: file one entry as a candidate")
    f.add_argument("--source", required=True)
    f.add_argument("--domain", required=True)
    f.add_argument("--id", required=True)
    f.add_argument("--as-domain", default="")
    f.add_argument("--as-id", default="")
    f.set_defaults(func=cmd_file)

    fp = sub.add_parser("file-pool", help="import-default-pool: shape-matched bulk candidate file")
    fp.add_argument("--source", default="")
    fp.set_defaults(func=cmd_file_pool)

    r = sub.add_parser("ratify", help="ratify-import-candidate: write one ratified entry back")
    r.add_argument("--id", required=True)
    r.add_argument("--as-domain", default="")
    r.add_argument("--as-id", default="")
    r.set_defaults(func=cmd_ratify)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
