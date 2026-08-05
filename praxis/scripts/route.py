#!/usr/bin/env python3
"""route — the deterministic fact-sheet a GO-2 routing judgment consumes. Facts only, no decision.

Part of praxis (the routing spine). `frame` already produces the facts *prior* to routing — the
governing root, the span→decompose verdict, and the composition. Routing (GO-2, the "I am the
orchestrator" decision that is moving from corpora to praxis) needs a little more before a human/
engine can pick the unit-of-work, the stance, and the execution shape (inline / resume / isolate).
`route` bundles that: it runs `frame` for the root+span+composition facts and adds the deterministic
*execution-shape signals* on top —

  - **span → isolate**: a task whose files span multiple roots is `decompose` (frame's verdict); it
    is N units of work, one isolated per root, never routed as one. This is a hard fact, not a call.
  - **resume vs new**: if a workstream id is named, a ledger lookup says whether prior chunks for it
    already exist (a *resume* candidate) or not (*new*). The ledger is a praxis-owned file
    (`<root>/corpora/chunks/<workstream>.md`), so this is a native filesystem check — no engine call.
  - **composition availability**: whether the engine actually returned a domain set for the unit.

Everything here is fact. The *decision* — which unit-of-work, which stance, inline/resume/isolate —
is `phases/routing.md`, the judgment on top. Like `frame`, `route` degrades rather than crashes when
the engine or ledger is absent: it reports what it could not learn (`ledger: unknown`) and still
carries every root fact, because praxis does not depend on the engine to route.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frame as fr  # noqa: E402
import chunk_ledger as cl  # noqa: E402  the praxis-owned ledger this reads natively


def workstream_ledger_state(root_path: str | None, workstream: str | None) -> tuple[str, str]:
    """Native resume-vs-new signal. Returns (state, note) where state is one of:
    'exists' (a ledger file for this workstream is present → resume candidate),
    'absent' (a governing root is known but has no such ledger → new),
    'unknown' (no workstream named, or no single governing root → cannot tell, defaults to new).

    The ledger is a praxis-owned file (`chunk_ledger.chunks_path`), so this is a pure filesystem
    check — no engine call. (Previously the read-only `close-workstream` engine capability; that verb
    is now native praxis work, so the lookup came home too.)
    """
    if not workstream:
        return "unknown", "no workstream named — treated as new work"
    if not root_path:
        return "unknown", "no single governing root — cannot locate a ledger"
    if cl.chunks_path(root_path, workstream).is_file():
        return "exists", "a chunk ledger for this workstream exists — resume candidate"
    return "absent", "no ledger for this workstream — new work"


def build_route(base: Path, target: str | None, files: list[str], unit_of_work: str | None,
                workstream: str | None, corpus_py: Path) -> dict:
    frame = fr.build_frame(base, target, files, unit_of_work, corpus_py)

    spans = frame["spans_multiple_roots"]
    # A single governing root owns the ledger; a spanning/no-root task has no one ledger to resume.
    root_path = frame["roots"][0]["path"] if (frame.get("roots") and not spans) else None
    ledger_state, ledger_note = workstream_ledger_state(root_path, workstream)
    resume_candidate = ledger_state == "exists"
    composition_available = frame.get("composition") is not None

    # Execution-shape signals are facts; the shape *choice* is the judgment in routing.md.
    signals: list[str] = []
    if spans:
        signals.append("spans multiple roots → isolate: one unit of work per root, never routed as one")
    if resume_candidate:
        signals.append(f"workstream '{workstream}' has a ledger → resume candidate")
    elif workstream and ledger_state == "absent":
        signals.append(f"workstream '{workstream}' named but no ledger → new")
    if not unit_of_work:
        signals.append("unit-of-work not decided — the core routing judgment; composition follows it")
    if unit_of_work and not composition_available and not spans:
        signals.append(f"composition unavailable ({frame.get('composition_note')})")

    return {
        "base": str(base),
        "unit_of_work": unit_of_work,
        "frame": frame,
        "execution_shape": {
            "verdict": frame["verdict"],
            "spans_multiple_roots": spans,
            "isolate_per_root": spans,
            "workstream": workstream,
            "ledger": ledger_state,
            "ledger_note": ledger_note,
            "resume_candidate": resume_candidate,
            "composition_available": composition_available,
        },
        "signals": signals,
    }


def print_route(r: dict) -> None:
    es = r["execution_shape"]
    print(f"route · unit-of-work: {r['unit_of_work'] or '(undecided)'}\n")
    f = r["frame"]
    if es["spans_multiple_roots"]:
        print(f"shape: ISOLATE (decompose) — {f.get('note','')}")
    else:
        if not f["roots"]:
            print("shape: no root governs this target (see frame)")
        else:
            rr = f["roots"][0]
            comp = f["composition"]
            comp_s = f"{len(comp)} domains" if comp is not None else f"— ({f.get('composition_note')})"
            print(f"root: {rr['name']} [{rr['engine']}]   composition: {comp_s}")
    print(f"workstream: {es['workstream'] or '(none)'}   ledger: {es['ledger']}   "
          f"resume-candidate: {es['resume_candidate']}")
    if r["signals"]:
        print("\nsignals (facts for the routing judgment):")
        for s in r["signals"]:
            print(f"  • {s}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="route", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", help="a candidate path the task touches")
    ap.add_argument("--files", default="", help="comma-separated candidate files")
    ap.add_argument("--unit-of-work", default="", help="the task's unit-of-work (decided in routing)")
    ap.add_argument("--workstream", default="", help="an existing workstream id to test for resume")
    ap.add_argument("--from", dest="frm", default=".", help="search base for root discovery (default cwd)")
    ap.add_argument("--corpus-py", default=str(fr.DEFAULT_CORPUS_PY),
                    help="the corpora engine CLI (in-repo binding; tests override)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not args.target and not args.files:
        ap.error("give --target and/or --files")
    base = Path(args.frm).resolve()
    files = [f.strip() for f in args.files.split(",") if f.strip()]
    route = build_route(base, args.target, files, args.unit_of_work or None,
                        args.workstream or None, Path(args.corpus_py))
    if args.json:
        print(json.dumps(route, indent=2))
    else:
        print_route(route)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
