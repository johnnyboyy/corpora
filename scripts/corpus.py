#!/usr/bin/env python3
"""corpus.py — deterministic bookkeeping for a corpora project.

Judgment stays with the model; arithmetic and verification live here. The model
supplies its judgments (ratify counts, fired/violated/idle classifications) as
arguments; this script does all measuring, counting, threshold math, and writing.

Runs from a project root (the directory containing `corpora/`), or pass --root.
State lives in a script-owned block inside `corpora/domains/audit.md`, delimited
by markers — the script never touches anything outside its markers.

Commands:
  measure                          update working-file-tokens for every domain
  verify                           reconcile ledger against working files (detects
                                   unrecorded gates and gate-bypassing writes)
  record-gate --domain D [...]     record a ratify gate's outcomes
  triggers                         evaluate thresholds; print what fires
  lint-handoff FILE                validate a handoff artifact's envelope
  handoffs                         list lingering handoff files with age
  retro-done --domain D            reset counters after a retrospective
  sync-done                        reset library-drift after a UI-library sync

Thresholds (kernel.md, "The retrospective"): retrospective when ratified >= 6,
or tokens grew >= 50% over baseline, or gate-violations >= 3; library sync when
since-last-sync >= 3.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import sys

MARK_BEGIN = "<!-- corpus-script:begin — maintained by scripts/corpus.py; do not edit by hand -->"
MARK_END = "<!-- corpus-script:end -->"

RETRO_RATIFIED = 6
RETRO_TOKEN_GROWTH = 0.5
RETRO_VIOLATIONS = 3
SYNC_DRIFT = 3

STATUS_ENUM = {"complete", "tradeoffs-pending", "questions-pending", "blocked"}
KIND_ENUM = {"judgment", "knowledge", "direction"}


def today() -> str:
    return datetime.date.today().isoformat()


def est_tokens(path: str) -> int:
    return os.path.getsize(path) // 4


def fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


# ── project layout ──────────────────────────────────────────────────────────

class Project:
    def __init__(self, root: str):
        self.root = root
        self.domains_dir = os.path.join(root, "corpora", "domains")
        self.audit_path = os.path.join(self.domains_dir, "audit.md")
        self.handoffs_dir = os.path.join(root, "corpora", "handoffs")
        if not os.path.isdir(self.domains_dir):
            fail(f"no corpora/domains under {root} — run from a bootstrapped project root, or pass --root")

    def domain_files(self) -> dict:
        out = {}
        for name in sorted(os.listdir(self.domains_dir)):
            if name.endswith(".md") and name != "audit.md":
                out[name[:-3]] = os.path.join(self.domains_dir, name)
        return out


# ── state block: parse / render ─────────────────────────────────────────────
# The block is flat, fixed-schema YAML the script alone writes, so a purpose-
# built parser is safe. Structure:
#   counters:      list of per-domain dicts
#   efficacy:      list of per-principle dicts
#   library-drift: one dict

def empty_state() -> dict:
    return {"counters": [], "efficacy": [], "library-drift": {"since-last-sync": 0}}


def parse_state(text: str) -> dict:
    state = empty_state()
    section = None
    item = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#") or line.strip().startswith("```"):
            continue
        if not line.startswith(" "):
            key = line.rstrip(":")
            section = key if key in ("counters", "efficacy", "library-drift") else None
            item = None
            continue
        if section is None:
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            item = {}
            state[section].append(item)
            stripped = stripped[2:]
        if ":" in stripped:
            k, _, v = stripped.partition(":")
            v = v.strip()
            val = int(v) if re.fullmatch(r"-?\d+", v) else v
            if section == "library-drift":
                state[section][k.strip()] = val
            elif item is not None:
                item[k.strip()] = val
    return state


COUNTER_FIELDS = ["domain", "since", "ratified", "killed", "gate-violations",
                  "working-file-tokens", "baseline-tokens",
                  "principles-at-baseline", "kills-at-baseline"]


def count_entries(path: str) -> tuple:
    """Count principle and kill entries in a domain working file.

    Ground truth for `verify`: entries are appended under `principles:` and
    `killed:` keys; each entry opens with `- id:`. Tolerant of indentation and
    of the keys appearing inside a yaml fence.
    """
    principles = kills = 0
    section = None
    for raw in open(path):
        line = raw.strip()
        if re.fullmatch(r"principles:\s*", line):
            section = "p"
        elif re.fullmatch(r"killed:\s*", line):
            section = "k"
        elif re.match(r"-\s*id:", line):
            if section == "p":
                principles += 1
            elif section == "k":
                kills += 1
    return principles, kills
EFFICACY_FIELDS = ["id", "fired", "violated", "idle"]


def render_state(state: dict) -> str:
    lines = ["```yaml", "counters:"]
    for c in state["counters"]:
        prefix = "  - "
        for f in COUNTER_FIELDS:
            lines.append(f"{prefix}{f}: {c.get(f, 0)}")
            prefix = "    "
    lines.append("efficacy:")
    for e in state["efficacy"]:
        prefix = "  - "
        for f in EFFICACY_FIELDS:
            lines.append(f"{prefix}{f}: {e.get(f, 0)}")
            prefix = "    "
    lines.append("library-drift:")
    lines.append(f"  since-last-sync: {state['library-drift'].get('since-last-sync', 0)}")
    lines.append("```")
    return "\n".join(lines)


def load(project: Project) -> dict:
    if not os.path.exists(project.audit_path):
        return empty_state()
    text = open(project.audit_path).read()
    if MARK_BEGIN not in text:
        return empty_state()
    block = text.split(MARK_BEGIN, 1)[1].split(MARK_END, 1)[0]
    return parse_state(block)


def save(project: Project, state: dict) -> None:
    block = f"{MARK_BEGIN}\n\n## counters (script-maintained)\n\n{render_state(state)}\n\n{MARK_END}"
    if os.path.exists(project.audit_path):
        text = open(project.audit_path).read()
    else:
        text = "# Audit — project layer\n"
    if MARK_BEGIN in text:
        head = text.split(MARK_BEGIN, 1)[0]
        tail = text.split(MARK_END, 1)[1] if MARK_END in text else "\n"
        text = head + block + tail
    else:
        text = text.rstrip("\n") + "\n\n" + block + "\n"
    open(project.audit_path, "w").write(text)


def counter_for(state: dict, domain: str, tokens: int, path: str = "") -> dict:
    for c in state["counters"]:
        if c.get("domain") == domain:
            return c
    p, k = count_entries(path) if path else (0, 0)
    c = {"domain": domain, "since": today(), "ratified": 0, "killed": 0,
         "gate-violations": 0, "working-file-tokens": tokens, "baseline-tokens": tokens,
         "principles-at-baseline": p, "kills-at-baseline": k}
    state["counters"].append(c)
    return c


def efficacy_for(state: dict, pid: str) -> dict:
    for e in state["efficacy"]:
        if e.get("id") == pid:
            return e
    e = {"id": pid, "fired": 0, "violated": 0, "idle": 0}
    state["efficacy"].append(e)
    return e


# ── commands ────────────────────────────────────────────────────────────────

def cmd_measure(project: Project, _args) -> None:
    state = load(project)
    for domain, path in project.domain_files().items():
        tokens = est_tokens(path)
        c = counter_for(state, domain, tokens, path)
        c["working-file-tokens"] = tokens
        print(f"{domain}: ~{tokens} tokens (baseline {c['baseline-tokens']})")
    save(project, state)


def cmd_verify(project: Project, _args) -> None:
    """Reconcile the ledger against the working files (the ground truth).

    Invariant: entries in each working file == entries at baseline + entries
    recorded since. A surplus means a gate ran off the books (or a write
    bypassed the gate entirely); a deficit means entries were removed without
    a retrospective reset. Read-and-report only — the operator decides.
    """
    state = load(project)
    known = {c.get("domain"): c for c in state["counters"]}
    problems = []
    for domain, path in project.domain_files().items():
        c = known.get(domain)
        if c is None:
            problems.append(f"{domain}: not in ledger — run `measure` to register it")
            continue
        actual_p, actual_k = count_entries(path)
        expect_p = c.get("principles-at-baseline", 0) + c.get("ratified", 0)
        expect_k = c.get("kills-at-baseline", 0) + c.get("killed", 0)
        if actual_p != expect_p:
            what = "UNRECORDED ratification(s)" if actual_p > expect_p else "entries REMOVED outside a retrospective"
            problems.append(f"{domain}: {abs(actual_p - expect_p)} {what} "
                            f"(file has {actual_p} principles; ledger accounts for {expect_p})")
        if actual_k != expect_k:
            what = "UNRECORDED kill(s)" if actual_k > expect_k else "kill entries REMOVED outside a retrospective"
            problems.append(f"{domain}: {abs(actual_k - expect_k)} {what} "
                            f"(file has {actual_k} kills; ledger accounts for {expect_k})")
    if problems:
        print("LEDGER RECONCILIATION FAILED — corpus changed off the books:")
        for p in problems:
            print(f"  - {p}")
        print("Fix: run `record-gate` retroactively for the unrecorded gate(s), or `measure`/`retro-done` to re-baseline knowingly.")
        sys.exit(1)
    print("ledger reconciled: every corpus entry is accounted for by a recorded gate")


def _ids(arg: str) -> list:
    return [s for s in (arg or "").split(",") if s.strip()]


def cmd_record_gate(project: Project, args) -> None:
    state = load(project)
    files = project.domain_files()
    if args.domain not in files:
        fail(f"unknown domain '{args.domain}' — have: {', '.join(files) or 'none'}")
    tokens = est_tokens(files[args.domain])
    existed = any(c.get("domain") == args.domain for c in state["counters"])
    c = counter_for(state, args.domain, tokens, files[args.domain])
    if not existed:
        # First registration during a gate: the file already contains the entries
        # this gate ratified/killed (write-back precedes record-gate), so exclude
        # them from the baseline or verify would double-count them.
        c["principles-at-baseline"] = max(0, c["principles-at-baseline"] - args.ratified)
        c["kills-at-baseline"] = max(0, c["kills-at-baseline"] - args.killed)
    c["working-file-tokens"] = tokens
    c["ratified"] += args.ratified
    c["killed"] += args.killed
    c["gate-violations"] += args.violations
    for pid in _ids(args.fired):
        efficacy_for(state, pid)["fired"] += 1
    for pid in _ids(args.violated):
        efficacy_for(state, pid)["violated"] += 1
    for pid in _ids(args.idle):
        efficacy_for(state, pid)["idle"] += 1
    if args.ui_drift:
        state["library-drift"]["since-last-sync"] = state["library-drift"].get("since-last-sync", 0) + 1
    save(project, state)
    print(f"recorded gate for {args.domain}: +{args.ratified} ratified, +{args.killed} killed, "
          f"+{args.violations} violations, drift={'+1' if args.ui_drift else 'no'}")
    cmd_triggers(project, None)


def cmd_triggers(project: Project, _args) -> None:
    state = load(project)
    fired = []
    for c in state["counters"]:
        reasons = []
        if c.get("ratified", 0) >= RETRO_RATIFIED:
            reasons.append(f"ratified {c['ratified']} >= {RETRO_RATIFIED}")
        base = c.get("baseline-tokens", 0)
        cur = c.get("working-file-tokens", 0)
        if base and cur >= base * (1 + RETRO_TOKEN_GROWTH):
            reasons.append(f"tokens {cur} grew >= {int(RETRO_TOKEN_GROWTH*100)}% over baseline {base}")
        if c.get("gate-violations", 0) >= RETRO_VIOLATIONS:
            reasons.append(f"violations {c['gate-violations']} >= {RETRO_VIOLATIONS}")
        if reasons:
            fired.append(f"retrospective {c['domain']} — " + "; ".join(reasons))
    drift = state["library-drift"].get("since-last-sync", 0)
    if drift >= SYNC_DRIFT:
        fired.append(f"ui-library sync — drift {drift} >= {SYNC_DRIFT}")
    if fired:
        print("TRIGGERS FIRED (suggest to operator — never automatic):")
        for f in fired:
            print(f"  - {f}")
    else:
        print("triggers: none")


def cmd_lint_handoff(_project: Project, args) -> None:
    path = args.file
    if not os.path.exists(path):
        fail(f"no such file: {path}")
    text = open(path).read()
    problems = []
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        problems.append("missing YAML frontmatter (--- ... ---)")
        front = ""
    else:
        front = m.group(1)

    def field(name: str) -> str:
        fm = re.search(rf"^{name}:\s*(.*)$", front, re.MULTILINE)
        return fm.group(1).strip() if fm else ""

    if not field("role"):
        problems.append("frontmatter: missing role")
    status = field("status")
    if status not in STATUS_ENUM:
        problems.append(f"frontmatter: status '{status}' not in {sorted(STATUS_ENUM)}")
    drift = field("ui-drift")
    if drift and drift.split("#")[0].strip() not in {"yes", "no"}:
        problems.append(f"frontmatter: ui-drift '{drift}' must be yes|no")
    # proposals: each item needs rule/condition/reason/kind/provenance; kind in enum
    prop_block = re.search(r"^proposals:\n((?:[ \t]+.*\n?)*)", front, re.MULTILINE)
    if prop_block and prop_block.group(1).strip() not in ("", "[]"):
        items = re.split(r"^\s*- ", prop_block.group(1), flags=re.MULTILINE)[1:]
        for i, item in enumerate(items, 1):
            for req in ("rule", "condition", "reason", "kind", "provenance"):
                if not re.search(rf"^\s*{req}:", "- " + item, re.MULTILINE):
                    problems.append(f"proposal {i}: missing {req}")
            km = re.search(r"^\s*kind:\s*(\S+)", "- " + item, re.MULTILINE)
            if km and km.group(1) not in KIND_ENUM:
                problems.append(f"proposal {i}: kind '{km.group(1)}' not in {sorted(KIND_ENUM)}")
    if not re.search(r"^## Artifact\s*$", text, re.MULTILINE):
        problems.append("missing '## Artifact' section")
    if not re.search(r"^## Surfaced\s*$", text, re.MULTILINE):
        problems.append("missing '## Surfaced' section (always present; empty is a statement)")
    if status == "questions-pending" and re.search(r"^## Surfaced\s*\n+\s*(\Z|##)", text, re.MULTILINE):
        problems.append("status is questions-pending but Surfaced is empty")

    if problems:
        print(f"FAIL {path}")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"PASS {path}")


def cmd_handoffs(project: Project, _args) -> None:
    if not os.path.isdir(project.handoffs_dir):
        print("no corpora/handoffs directory — no backlog")
        return
    entries = sorted(f for f in os.listdir(project.handoffs_dir) if f.endswith(".md"))
    if not entries:
        print("handoff backlog: empty")
        return
    now = datetime.datetime.now()
    print("handoff backlog (unratified — each is a pending gate):")
    for name in entries:
        path = os.path.join(project.handoffs_dir, name)
        age = (now - datetime.datetime.fromtimestamp(os.path.getmtime(path))).days
        front = open(path).read(2000)
        sm = re.search(r"^status:\s*(\S+)", front, re.MULTILINE)
        print(f"  - {name}  status={sm.group(1) if sm else '?'}  age={age}d")


def cmd_retro_done(project: Project, args) -> None:
    state = load(project)
    for c in state["counters"]:
        if c["domain"] == args.domain:
            files = project.domain_files()
            if args.domain in files:
                tokens = est_tokens(files[args.domain])
                p, k = count_entries(files[args.domain])
            else:
                tokens, p, k = c["working-file-tokens"], c.get("principles-at-baseline", 0), c.get("kills-at-baseline", 0)
            c.update({"since": today(), "ratified": 0, "killed": 0, "gate-violations": 0,
                      "working-file-tokens": tokens, "baseline-tokens": tokens,
                      "principles-at-baseline": p, "kills-at-baseline": k})
            save(project, state)
            print(f"reset counters for {args.domain}; baseline-tokens={tokens}, principles={p}, kills={k}")
            return
    fail(f"no counters for domain '{args.domain}'")


def cmd_sync_done(project: Project, _args) -> None:
    state = load(project)
    state["library-drift"]["since-last-sync"] = 0
    save(project, state)
    print("library-drift reset to 0")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="project root (contains corpora/)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("measure")
    sub.add_parser("verify")
    g = sub.add_parser("record-gate")
    g.add_argument("--domain", required=True)
    g.add_argument("--ratified", type=int, default=0)
    g.add_argument("--killed", type=int, default=0)
    g.add_argument("--violations", type=int, default=0)
    g.add_argument("--ui-drift", action="store_true")
    g.add_argument("--fired", default="", help="comma-separated principle ids")
    g.add_argument("--violated", default="", help="comma-separated principle ids")
    g.add_argument("--idle", default="", help="comma-separated principle ids")
    sub.add_parser("triggers")
    lh = sub.add_parser("lint-handoff")
    lh.add_argument("file")
    sub.add_parser("handoffs")
    r = sub.add_parser("retro-done")
    r.add_argument("--domain", required=True)
    sub.add_parser("sync-done")
    args = ap.parse_args()
    project = Project(os.path.abspath(args.root))
    {"measure": cmd_measure, "verify": cmd_verify, "record-gate": cmd_record_gate, "triggers": cmd_triggers,
     "lint-handoff": cmd_lint_handoff, "handoffs": cmd_handoffs,
     "retro-done": cmd_retro_done, "sync-done": cmd_sync_done}[args.cmd](project, args)


if __name__ == "__main__":
    main()
