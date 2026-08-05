#!/usr/bin/env python3
"""frame — the deterministic fact bundle for a task, gathered before any judgment acts.

Part of praxis. Given a task's candidate target (a path and/or a set of files) and its unit-of-work,
emit the facts the `framing` phase sizes and routes on:

  - which root governs the task, and whether it spans several roots (→ decompose: one unit of work per
    root, handed to each; a single agent never straddles two roots)
  - the composition (domain set) for the unit-of-work

Determinism + decoupling:
  - Root facts are pure filesystem (via root_tree) — they cannot be wrong.
  - Composition is the ENGINE's job, not praxis's. Praxis *invokes* it and relays the fact; it never
    re-derives a composition and never learns the engine's schema (what a "domain" or "applies-when"
    is). corpora is the engine for now, and the ONE binding — locating and calling
    `corpus.py select --json` — is isolated in engine_compose() below, overridable with --corpus-py.
    When praxis is lifted out, that single function becomes an engine registry; nothing else changes.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import root_tree as rt  # noqa: E402
import engine  # noqa: E402

# In-repo binding: praxis lives at <corpora-root>/praxis/, so the corpora engine's CLI is two levels up.
# This is the only place praxis knows where corpora is; --corpus-py overrides it (and tests use that).
DEFAULT_CORPUS_PY = Path(__file__).resolve().parents[2] / "scripts" / "corpus.py"


def engine_compose(root: Path, unit_of_work: str, corpus_py: Path) -> tuple[list[str] | None, str]:
    """Invoke the judgment engine for the `compose` capability: the domain set for a unit-of-work.

    `compose` is just another declared capability now — its argv is built from the same corpora
    manifest every write verb uses (`engine.resolve`), so frame no longer hardcodes the `select`
    verb or its flags. Frame still owns *interpreting* the result (composition is a JSON payload,
    not a pass/fail), which is why it reads `.stdout` rather than only branching on `.ok`.

    Returns (domains, note). domains is None when the engine is unavailable or errored — praxis still
    reports the root facts in that case rather than failing, since it does not depend on the engine.
    """
    if not Path(corpus_py).is_file():
        return None, f"engine not found at {corpus_py} — composition unavailable"
    res = engine.resolve(Path(corpus_py), "compose",
                         {"root": str(root), "unit_of_work": unit_of_work, "json": True}, timeout=30)
    if not res.ran:
        return None, res.note()
    if res.returncode != 0:
        return None, f"engine returned {res.returncode}: {res.stderr.strip()[:200]}"
    try:
        return json.loads(res.stdout)["domains"], "ok"
    except (json.JSONDecodeError, KeyError) as e:
        return None, f"engine output not understood: {e}"


def build_frame(base: Path, target: str | None, files: list[str], unit_of_work: str | None,
                corpus_py: Path) -> dict:
    markers = rt.DEFAULT_MARKERS
    roots = rt.find_roots(base, markers)

    # Resolve the target(s) to their governing root(s).
    targets: list[Path] = []
    if target:
        p = Path(target)
        targets.append(p if p.is_absolute() else base / p)
    for f in files:
        p = Path(f)
        targets.append(p if p.is_absolute() else base / p)

    governing: dict[str, dict] = {}
    unrouted: list[str] = []
    for t in targets:
        r = rt.nearest_root(t, roots)
        if r is None:
            unrouted.append(str(t))
        else:
            governing.setdefault(str(r), {
                "name": rt.root_name(r, markers), "engine": rt.which_marker(r, markers),
                "path": str(r), "targets": [],
            })["targets"].append(str(t))

    spans = len(governing) > 1
    frame: dict = {
        "base": str(base),
        "unit_of_work": unit_of_work,
        "roots": list(governing.values()),
        "spans_multiple_roots": spans,
        "unrouted_targets": unrouted,
    }

    if spans:
        info = rt.interop_root(targets, roots)
        frame["verdict"] = "decompose"
        frame["composition"] = None
        if info["entry"] is not None:
            entry = info["entry"]
            frame["interop_root"] = {"name": rt.root_name(entry, markers), "path": str(entry)}
            frame["define_interop_at"] = None
            frame["note"] = (f"spans {len(governing)} roots: enter at interop root "
                             f"'{rt.root_name(entry, markers)}', which defines each in-scope piece and "
                             f"passes it off to the child root for execution in its own context.")
        else:
            frame["interop_root"] = None
            frame["define_interop_at"] = info["define_at"]
            frame["note"] = (f"spans {len(governing)} roots with NO common-ancestor root to enter at — "
                             f"define an interop root at {info['define_at']} before this can proceed.")
        return frame

    frame["verdict"] = "single-root" if governing else "no-root"
    # Composition is a fact only once the unit-of-work is decided (a routing judgment upstream).
    if governing and unit_of_work:
        root = Path(next(iter(governing)))
        domains, note = engine_compose(root, unit_of_work, corpus_py)
        frame["composition"] = domains
        frame["composition_note"] = note
    else:
        frame["composition"] = None
        frame["composition_note"] = "unit-of-work not given — decide it (routing judgment) then re-run"
    return frame


def print_frame(f: dict) -> None:
    print(f"frame · unit-of-work: {f['unit_of_work'] or '(undecided)'}\n")
    if f["spans_multiple_roots"]:
        print(f"⚠ {f['note']}\n")
        if f.get("interop_root"):
            print(f"enter at: {f['interop_root']['name']}  {f['interop_root']['path']}")
        elif f.get("define_interop_at"):
            print(f"define an interop root at: {f['define_interop_at']}")
        print("pieces:")
        for r in f["roots"]:
            print(f"  • {r['name']} [{r['engine']}]")
            for t in r["targets"]:
                print(f"      {t}")
        return
    if not f["roots"]:
        print("no root governs this target.")
        if f["unrouted_targets"]:
            for t in f["unrouted_targets"]:
                print(f"  {t}")
        return
    r = f["roots"][0]
    print(f"root: {r['name']} [{r['engine']}]  {r['path']}")
    comp = f["composition"]
    if comp is None:
        print(f"composition: — ({f['composition_note']})")
    else:
        print(f"composition ({len(comp)} domains): {', '.join(comp)}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="frame", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", help="a candidate path the task touches")
    ap.add_argument("--files", default="", help="comma-separated candidate files")
    ap.add_argument("--unit-of-work", default="", help="the task's unit-of-work (decided upstream)")
    ap.add_argument("--from", dest="frm", default=".", help="search base for root discovery (default cwd)")
    ap.add_argument("--corpus-py", default=str(DEFAULT_CORPUS_PY),
                    help="the corpora engine CLI to invoke for composition (in-repo binding)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not args.target and not args.files:
        ap.error("give --target and/or --files")
    base = Path(args.frm).resolve()
    files = [f.strip() for f in args.files.split(",") if f.strip()]
    frame = build_frame(base, args.target, files, args.unit_of_work or None, Path(args.corpus_py))
    if args.json:
        print(json.dumps(frame, indent=2))
    else:
        print_frame(frame)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
