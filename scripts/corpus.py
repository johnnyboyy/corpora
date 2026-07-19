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
  lint-deferred                    validate the non-blocking UI/UX decision queue
  deferred                         list queued decisions grouped by owning role
  lint-utility-candidates          validate the persistent utility-candidate ledger
  utility-candidates               list candidates with status and sighting count
  record-utility-candidate [...]   append dated evidence to a candidate
  set-utility-status [...]         record the operator's candidate disposition
  retro-done --domain D            reset counters after a retrospective
  sync-done                        reset library-drift after a UI-library sync
  adopt --domain D                 locate D's seed/pack file and print it for curation into a
                                   project-local fork (fork-status: forked)

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
DEFERRED_ROLE_ENUM = {"ui-designer", "ux-designer"}
DEFERRED_STATUS_ENUM = {"queued", "resolved"}
UTILITY_STATUS_ENUM = {"open", "deferred", "denied", "accepted", "implemented"}
UTILITY_STATUS_REQUIRES_REASON = {"deferred", "denied"}


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
        self.deferred_path = os.path.join(root, "corpora", "deferred-decisions.md")
        self.utility_candidates_path = os.path.join(root, "corpora", "utility-candidates.md")
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
    prop_block = re.search(r"^proposals:\n((?:[ \t]+.*\n?)*)", front, re.MULTILINE)
    if prop_block and prop_block.group(1).strip() not in ("", "[]"):
        items = re.split(r"^\s*- ", prop_block.group(1), flags=re.MULTILINE)[1:]
        for position, item in enumerate(items, 1):
            for req in ("rule", "condition", "reason", "kind", "provenance"):
                if not re.search(rf"^\s*{req}:", "- " + item, re.MULTILINE):
                    problems.append(f"proposal {position}: missing {req}")
            km = re.search(r"^\s*kind:\s*(\S+)", "- " + item, re.MULTILINE)
            if km and km.group(1) not in KIND_ENUM:
                problems.append(f"proposal {position}: kind '{km.group(1)}' not in {sorted(KIND_ENUM)}")
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


def parse_deferred(path: str) -> list:
    """Parse the queue's deliberately flat YAML subset without a YAML dependency."""
    entries = []
    item = None
    in_decisions = False
    for raw in open(path):
        line = raw.rstrip()
        stripped = line.strip()
        if in_decisions and stripped == "```":
            break
        if stripped == "decisions:" or stripped == "decisions: []":
            in_decisions = True
            continue
        if not in_decisions or not stripped or stripped.startswith(("#", "```")):
            continue
        if re.match(r"^\s*-\s+id:\s*", line):
            item = {}
            entries.append(item)
            stripped = re.sub(r"^-\s+", "", stripped)
        if item is not None and ":" in stripped:
            key, _, value = stripped.partition(":")
            item[key.strip()] = value.strip().strip('"').strip("'")
    return entries


def deferred_problems(entries: list) -> list:
    required = ("id", "role", "domain", "question", "context", "source-workstream",
                "created", "blocking", "provisional-treatment", "status")
    problems = []
    seen = set()
    for index, entry in enumerate(entries, 1):
        label = entry.get("id") or f"entry {index}"
        for field in required:
            if not entry.get(field):
                problems.append(f"{label}: missing {field}")
        if entry.get("id") in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(entry.get("id"))
        if entry.get("role") not in DEFERRED_ROLE_ENUM:
            problems.append(f"{label}: role must be one of {sorted(DEFERRED_ROLE_ENUM)}")
        if entry.get("status") not in DEFERRED_STATUS_ENUM:
            problems.append(f"{label}: status must be one of {sorted(DEFERRED_STATUS_ENUM)}")
        if entry.get("blocking") != "no":
            problems.append(f"{label}: blocking must be 'no' — surface blockers immediately")
        created = entry.get("created", "")
        if created and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", created):
            problems.append(f"{label}: created must be YYYY-MM-DD")
    return problems


def cmd_lint_deferred(project: Project, _args) -> None:
    if not os.path.exists(project.deferred_path):
        config = os.path.join(project.root, "corpora", "config.md")
        config_text = open(config).read() if os.path.exists(config) else ""
        if re.search(r"^has-ui:\s*yes\s*$", config_text, re.MULTILINE):
            fail("UI project has no corpora/deferred-decisions.md — create it from the kernel schema")
        print("no deferred-decision queue needed (project has no UI)")
        return
    entries = parse_deferred(project.deferred_path)
    problems = deferred_problems(entries)
    if problems:
        print(f"FAIL {project.deferred_path}")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    resolved = [entry["id"] for entry in entries if entry.get("status") == "resolved"]
    print(f"PASS {project.deferred_path} ({len(entries)} entries)")
    if resolved:
        print("  warning: resolved entries should be removed after ratification: " + ", ".join(resolved))


def cmd_deferred(project: Project, _args) -> None:
    if not os.path.exists(project.deferred_path):
        print("deferred decision queue: absent")
        return
    entries = parse_deferred(project.deferred_path)
    problems = deferred_problems(entries)
    if problems:
        print("deferred decision queue is invalid; run `lint-deferred`")
        sys.exit(1)
    queued = [entry for entry in entries if entry.get("status") == "queued"]
    if not queued:
        print("deferred decision queue: empty")
        return
    print("deferred non-blocking decisions:")
    for role in sorted(DEFERRED_ROLE_ENUM):
        owned = [entry for entry in queued if entry["role"] == role]
        if not owned:
            continue
        print(f"  {role} ({len(owned)}):")
        for entry in owned:
            print(f"    - {entry['id']}  domain={entry['domain']}  workstream={entry['source-workstream']}")
            print(f"      {entry['question']}")


def parse_utility_candidates(path: str) -> list:
    entries = []
    item = None
    evidence = None
    in_candidates = False
    in_evidence = False
    in_disposition = False
    for raw in open(path):
        line = raw.rstrip()
        stripped = line.strip()
        if in_candidates and stripped == "```":
            break
        if stripped in {"candidates:", "candidates: []"}:
            in_candidates = True
            continue
        if not in_candidates or not stripped or stripped.startswith(("#", "```")):
            continue
        if re.match(r"^\s{2}-\s+id:\s*", line):
            item = {"evidence": [], "disposition-reason": ""}
            entries.append(item)
            item["id"] = stripped.partition(":")[2].strip().strip('"').strip("'")
            in_evidence = False
            in_disposition = False
            continue
        if item is None:
            continue
        top = re.match(r"^\s{4}([a-z][a-z0-9-]*):\s*(.*)$", line)
        if top:
            key, value = top.groups()
            in_evidence = key == "evidence"
            in_disposition = key == "disposition"
            if in_evidence:
                evidence = None
                continue
            if in_disposition:
                continue
            item[key] = value.strip().strip('"').strip("'")
            continue
        if in_evidence and re.match(r"^\s{6}-\s+workstream:\s*\S+", line):
            # Legacy order is rejected by validation but parsed so the error is useful.
            evidence = {"workstream": stripped.partition(":")[2].strip().strip('"').strip("'")}
            item["evidence"].append(evidence)
        dated = re.match(r"^\s{6}-\s+date:\s*(.*)$", line)
        if in_evidence and dated:
            evidence = {"date": dated.group(1).strip().strip('"').strip("'")}
            item["evidence"].append(evidence)
            continue
        evidence_field = re.match(r"^\s{8}(workstream|burden):\s*(.*)$", line)
        if in_evidence and evidence is not None and evidence_field:
            key, value = evidence_field.groups()
            evidence[key] = value.strip().strip('"').strip("'")
        if in_disposition:
            reason = re.match(r"^\s{6}reason:\s*(.*)$", line)
            if reason:
                item["disposition-reason"] = reason.group(1).strip().strip('"').strip("'")
    return entries


def utility_candidate_problems(entries: list) -> list:
    required = ("id", "operation-shape", "status")
    problems = []
    seen = set()
    for index, entry in enumerate(entries, 1):
        label = entry.get("id") or f"entry {index}"
        for field in required:
            if not entry.get(field):
                problems.append(f"{label}: missing {field}")
        if entry.get("id") in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(entry.get("id"))
        if entry.get("status") not in UTILITY_STATUS_ENUM:
            problems.append(f"{label}: status must be one of {sorted(UTILITY_STATUS_ENUM)}")
        evidence_seen = set()
        if not entry.get("evidence"):
            problems.append(f"{label}: requires at least one evidence record")
        for evidence_index, evidence in enumerate(entry.get("evidence", []), 1):
            for field in ("date", "workstream", "burden"):
                if not evidence.get(field):
                    problems.append(f"{label}: evidence {evidence_index} missing {field}")
            value = evidence.get("date", "")
            try:
                datetime.date.fromisoformat(value)
            except ValueError:
                if value:
                    problems.append(f"{label}: evidence {evidence_index} date must be valid YYYY-MM-DD")
            signature = tuple(evidence.get(field, "") for field in ("date", "workstream", "burden"))
            if signature in evidence_seen:
                problems.append(f"{label}: duplicate evidence record {evidence_index}")
            evidence_seen.add(signature)
        if entry.get("status") in UTILITY_STATUS_REQUIRES_REASON and not entry.get("disposition-reason"):
            problems.append(f"{label}: {entry.get('status')} status requires disposition reason")
    return problems


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def save_utility_candidates(path: str, entries: list) -> None:
    lines = ["# Utility candidates", "", "```yaml"]
    if not entries:
        lines.append("candidates: []")
    else:
        lines.append("candidates:")
        for entry in entries:
            lines.extend([
                f"  - id: {entry['id']}",
                f"    operation-shape: {yaml_quote(entry['operation-shape'])}",
                f"    status: {entry['status']}",
                "    evidence:",
            ])
            for evidence in entry["evidence"]:
                lines.extend([
                    f"      - date: {evidence['date']}",
                    f"        workstream: {evidence['workstream']}",
                    f"        burden: {yaml_quote(evidence['burden'])}",
                ])
            reason = entry.get("disposition-reason", "")
            if reason:
                lines.extend(["    disposition:", f"      reason: {yaml_quote(reason)}"])
    lines.extend(["```", ""])
    open(path, "w").write("\n".join(lines))


def cmd_lint_utility_candidates(project: Project, _args) -> None:
    path = project.utility_candidates_path
    if not os.path.exists(path):
        fail("no corpora/utility-candidates.md — create it from the kernel schema")
    entries = parse_utility_candidates(path)
    problems = utility_candidate_problems(entries)
    if problems:
        print(f"FAIL {path}")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    print(f"PASS {path} ({len(entries)} entries)")


def cmd_utility_candidates(project: Project, _args) -> None:
    path = project.utility_candidates_path
    if not os.path.exists(path):
        print("utility candidate ledger: absent")
        return
    entries = parse_utility_candidates(path)
    if utility_candidate_problems(entries):
        print("utility candidate ledger is invalid; run `lint-utility-candidates`")
        sys.exit(1)
    if not entries:
        print("utility candidate ledger: empty")
        return
    print("utility candidates:")
    for entry in entries:
        dates = [evidence["date"] for evidence in entry["evidence"]]
        print(f"  - {entry['id']}  status={entry['status']}  sightings={len(dates)}  "
              f"first={min(dates)}  last={max(dates)}")
        print(f"    {entry['operation-shape']}")


def cmd_record_utility_candidate(project: Project, args) -> None:
    path = project.utility_candidates_path
    if not os.path.exists(path):
        fail("no corpora/utility-candidates.md — create it from the kernel schema")
    entries = parse_utility_candidates(path)
    problems = utility_candidate_problems(entries)
    if problems:
        fail("utility candidate ledger is invalid — run `lint-utility-candidates`")
    entry = next((candidate for candidate in entries if candidate["id"] == args.id), None)
    if entry is None:
        entry = {"id": args.id, "operation-shape": args.operation_shape, "status": "open",
                 "evidence": [], "disposition-reason": ""}
        entries.append(entry)
    elif entry["operation-shape"] != args.operation_shape:
        fail(f"candidate '{args.id}' has a different operation-shape")
    evidence_date = args.date or today()
    try:
        datetime.date.fromisoformat(evidence_date)
    except ValueError:
        fail("--date must be a valid YYYY-MM-DD date")
    evidence = {"date": evidence_date, "workstream": args.workstream, "burden": args.burden}
    if evidence in entry["evidence"]:
        print(f"utility candidate {args.id}: identical evidence already recorded")
        return
    entry["evidence"].append(evidence)
    save_utility_candidates(path, entries)
    sightings = len(entry["evidence"])
    print(f"utility candidate {args.id}: recorded sighting {sightings}")
    if sightings > 1 or entry["status"] in {"deferred", "denied"}:
        print(f"RESURFACE {args.id}: status={entry['status']} with {sightings} sightings")


def cmd_set_utility_status(project: Project, args) -> None:
    path = project.utility_candidates_path
    if not os.path.exists(path):
        fail("no corpora/utility-candidates.md — create it from the kernel schema")
    entries = parse_utility_candidates(path)
    problems = utility_candidate_problems(entries)
    if problems:
        fail("utility candidate ledger is invalid — run `lint-utility-candidates`")
    entry = next((candidate for candidate in entries if candidate["id"] == args.id), None)
    if entry is None:
        fail(f"unknown utility candidate '{args.id}'")
    if args.status in UTILITY_STATUS_REQUIRES_REASON and not args.reason:
        fail(f"status '{args.status}' requires --reason")
    entry["status"] = args.status
    entry["disposition-reason"] = args.reason or ""
    save_utility_candidates(path, entries)
    print(f"utility candidate {args.id}: status={args.status}")


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


# ── adopt: fork a seed/pack domain into the project layer ──────────────────

def skill_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_role_pack(project: Project) -> str:
    config_path = os.path.join(project.root, "corpora", "config.md")
    if not os.path.exists(config_path):
        return "none"
    for raw in open(config_path):
        m = re.match(r"role-pack:\s*(\S+)", raw.strip())
        if m:
            return m.group(1)
    return "none"


def seed_domain_path(project: Project, domain: str) -> str:
    if domain == "audit":
        return ""
    root = skill_root()
    kernel_path = os.path.join(root, "domains", f"{domain}.md")
    if os.path.exists(kernel_path):
        return kernel_path
    pack = read_role_pack(project)
    if pack != "none":
        pack_path = os.path.join(root, "packs", pack, "domains", f"{domain}.md")
        if os.path.exists(pack_path):
            return pack_path
    return ""


def fork_info(path: str) -> dict:
    info = {}
    for raw in open(path):
        line = raw.strip()
        if re.fullmatch(r"principles:\s*", line):
            break
        m = re.match(r"(fork-status|forked-from|forked-date):\s*(.+)", line)
        if m:
            info[m.group(1)] = m.group(2).strip()
    return info


def cmd_adopt(project: Project, args) -> None:
    domain = args.domain
    seed_path = seed_domain_path(project, domain)
    if not seed_path:
        fail(f"no seed or pack file for domain '{domain}' — nothing to fork from")
    project_path = os.path.join(project.domains_dir, f"{domain}.md")
    if os.path.exists(project_path):
        info = fork_info(project_path)
        if info.get("fork-status") == "forked":
            fail(f"'{domain}' is already forked (forked-from {info.get('forked-from', '?')}) "
                 "— adopt is one-way, not a resync")
    print(f"seed file for '{domain}': {seed_path}\n")
    print(open(seed_path).read())
    rel_seed = os.path.relpath(seed_path, skill_root())
    print(f"---\nPropose which principles above are project-relevant vs. droppable (with a reason "
          f"each). After operator approval, write the curated result to {project_path} — merged by "
          f"`id` with any principles already there — with this preamble:\n"
          f"  fork-status: forked\n  forked-from: {rel_seed}\n  forked-date: {today()}\n"
          "From then on this domain loads only the project file; the seed is no longer consulted.")


# ── kill-log graduation: age out killed entries with a recorded, stale kill date ─────────────
#
# Works on any domains-dir + its audit.md pair — project layer (<root>/corpora/domains), the
# kernel-seed layer (domains/), or a pack layer (packs/<pack>/domains/) — not only project layers,
# since retrospective consolidation happens in the skill repo's own seed/pack corpora too.

KILL_GRADUATION_DAYS = 90


def list_killed_ids(domain_path: str) -> list:
    ids = []
    section = None
    for raw in open(domain_path):
        line = raw.strip()
        if re.fullmatch(r"principles:\s*", line):
            section = "p"
        elif re.fullmatch(r"killed:\s*", line):
            section = "k"
        elif section == "k":
            m = re.match(r"-\s*id:\s*(\S+)", line)
            if m:
                ids.append(m.group(1))
    return ids


def parse_audit_entries(audit_path: str) -> dict:
    """Tolerant parser for the hand-maintained `provenance:` list in a layer's audit.md.

    Extracts only top-level (2-space-indented) scalar fields per entry — id, domain, killed,
    graduated. Nested `history:` sub-blocks (4-space indented) are deliberately not parsed; this
    reads just enough structure for kill-age accounting, not a general YAML parser.
    """
    entries = {}
    current = None
    in_provenance = False
    for raw in open(audit_path):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if re.fullmatch(r"provenance:", stripped):
            in_provenance = True
            continue
        if re.fullmatch(r"promoted:", stripped):
            in_provenance = False
            current = None
            continue
        if not in_provenance:
            continue
        m_id = re.match(r"-\s*id:\s*(\S+)", stripped)
        if m_id:
            current = m_id.group(1)
            entries[current] = {"id": current}
            continue
        if current is None or not stripped:
            continue
        if line.startswith("  ") and not line.startswith("    "):
            m_field = re.match(r"([\w-]+):\s*(.*)$", stripped)
            if m_field:
                entries[current][m_field.group(1)] = m_field.group(2).strip()
    return entries


def cmd_kill_report(args) -> None:
    threshold = args.min_age_days
    entries = parse_audit_entries(args.audit)
    reported = False
    for name in sorted(os.listdir(args.domains_dir)):
        if not name.endswith(".md") or name == "audit.md":
            continue
        domain = name[:-3]
        killed_ids = list_killed_ids(os.path.join(args.domains_dir, name))
        missing, candidates = [], []
        for kid in killed_ids:
            entry = entries.get(kid)
            if entry is None or "killed" not in entry:
                missing.append(kid)
                continue
            if "graduated" in entry:
                continue
            try:
                killed_date = datetime.date.fromisoformat(entry["killed"])
            except ValueError:
                missing.append(kid)
                continue
            age = (datetime.date.today() - killed_date).days
            if age >= threshold:
                candidates.append((kid, age))
        if missing:
            reported = True
            print(f"{domain}: missing killed-date for: {', '.join(missing)}")
        for kid, age in candidates:
            reported = True
            print(f"{domain}: '{kid}' killed {age}d ago (>= {threshold}) — graduation candidate")
    if not reported:
        print("no kills missing a date, and none old enough to graduate")


def remove_killed_entry(domain_path: str, kill_id: str) -> bool:
    text = open(domain_path).read()
    if "\nkilled:" not in text and not text.startswith("killed:"):
        return False
    head, tail = text.split("killed:", 1)
    fence_idx = tail.find("```", 0)
    body = tail[:fence_idx] if fence_idx != -1 else tail
    footer = tail[fence_idx:] if fence_idx != -1 else ""
    blocks = re.split(r"\n\s*\n", body)
    kept = []
    removed = False
    for block in blocks:
        if re.search(rf"^\s*-\s*id:\s*{re.escape(kill_id)}\s*$", block, re.MULTILINE):
            removed = True
            continue
        kept.append(block)
    if not removed:
        return False
    new_body = "\n\n".join(b for b in kept if b.strip())
    new_tail = ("\n" + new_body + "\n" if new_body.strip() else "\n") + footer
    open(domain_path, "w").write(head + "killed:" + new_tail)
    return True


def annotate_graduated(audit_path: str, kill_id: str) -> bool:
    lines = open(audit_path).read().split("\n")
    out = []
    current = None
    in_provenance = False
    annotated = False
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"provenance:", stripped):
            in_provenance = True
        if re.fullmatch(r"promoted:", stripped):
            in_provenance = False
        if in_provenance:
            m = re.match(r"-\s*id:\s*(\S+)", stripped)
            if m:
                current = m.group(1)
        out.append(line)
        if in_provenance and current == kill_id and re.match(r"killed:\s*\S+", stripped):
            out.append(f"  graduated: {today()}")
            annotated = True
    if annotated:
        open(audit_path, "w").write("\n".join(out))
    return annotated


def cmd_graduate_kill(args) -> None:
    domain_path = os.path.join(args.domains_dir, f"{args.domain}.md")
    if not os.path.exists(domain_path):
        fail(f"no domain file '{args.domain}' under {args.domains_dir}")
    entries = parse_audit_entries(args.audit)
    entry = entries.get(args.id)
    if entry is None or "killed" not in entry:
        fail(f"'{args.id}' has no recorded killed-date in {args.audit} — record one before "
             "graduating (kill-report lists entries missing it)")
    if "graduated" in entry:
        fail(f"'{args.id}' was already graduated on {entry['graduated']}")
    if not remove_killed_entry(domain_path, args.id):
        fail(f"no killed entry '{args.id}' found in {domain_path}")
    if not annotate_graduated(args.audit, args.id):
        fail(f"removed '{args.id}' from {domain_path} but could not annotate {args.audit} — fix by hand")
    print(f"graduated '{args.id}': removed from {domain_path}'s killed log, annotated in {args.audit}")


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
    sub.add_parser("lint-deferred")
    sub.add_parser("deferred")
    sub.add_parser("lint-utility-candidates")
    sub.add_parser("utility-candidates")
    uc = sub.add_parser("record-utility-candidate")
    uc.add_argument("--id", required=True)
    uc.add_argument("--operation-shape", required=True)
    uc.add_argument("--workstream", required=True)
    uc.add_argument("--burden", required=True)
    uc.add_argument("--date", default="", help="YYYY-MM-DD; defaults to today")
    us = sub.add_parser("set-utility-status")
    us.add_argument("--id", required=True)
    us.add_argument("--status", required=True, choices=sorted(UTILITY_STATUS_ENUM))
    us.add_argument("--reason", default="")
    r = sub.add_parser("retro-done")
    r.add_argument("--domain", required=True)
    sub.add_parser("sync-done")
    ad = sub.add_parser("adopt")
    ad.add_argument("--domain", required=True)
    kr = sub.add_parser("kill-report", help="works on any domains-dir + audit.md pair, not only a project's corpora/domains")
    kr.add_argument("--domains-dir", required=True)
    kr.add_argument("--audit", required=True)
    kr.add_argument("--min-age-days", type=int, default=KILL_GRADUATION_DAYS)
    gk = sub.add_parser("graduate-kill", help="works on any domains-dir + audit.md pair, not only a project's corpora/domains")
    gk.add_argument("--domains-dir", required=True)
    gk.add_argument("--audit", required=True)
    gk.add_argument("--domain", required=True)
    gk.add_argument("--id", required=True)
    args = ap.parse_args()

    no_project = {"kill-report": cmd_kill_report, "graduate-kill": cmd_graduate_kill}
    if args.cmd in no_project:
        no_project[args.cmd](args)
        return

    project = Project(os.path.abspath(args.root))
    {"measure": cmd_measure, "verify": cmd_verify, "record-gate": cmd_record_gate, "triggers": cmd_triggers,
     "lint-handoff": cmd_lint_handoff, "handoffs": cmd_handoffs,
     "lint-deferred": cmd_lint_deferred, "deferred": cmd_deferred,
     "lint-utility-candidates": cmd_lint_utility_candidates,
     "utility-candidates": cmd_utility_candidates,
     "record-utility-candidate": cmd_record_utility_candidate,
     "set-utility-status": cmd_set_utility_status,
     "retro-done": cmd_retro_done, "sync-done": cmd_sync_done,
     "adopt": cmd_adopt}[args.cmd](project, args)


if __name__ == "__main__":
    main()
