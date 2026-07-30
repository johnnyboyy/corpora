#!/usr/bin/env python3
"""corpus.py — deterministic bookkeeping for a corpora project.

Judgment stays with the model; arithmetic and verification live here. The model
supplies its judgments (ratify counts, fired/violated/idle classifications) as
arguments; this script does all measuring, counting, threshold math, and writing.

Runs from a project root (the directory containing `corpora/`), or pass --root.
State lives in a script-owned block inside `corpora/domains/audit.md`, delimited
by markers — the script never touches anything outside its markers.

Commands:
  measure [--domains-dir --audit]  update working-file-tokens for every domain (defaults to the
                                   project layer; override to measure any domains-dir + audit.md
                                   pair — e.g. the kernel-seed layer, same as kill-report)
  verify [--domains-dir --audit]   reconcile ledger against working files (detects
                                   unrecorded gates and gate-bypassing writes)
  record-gate --domain D [...]     record a ratify gate's outcomes (same --domains-dir/--audit
                                   override)
  triggers                         evaluate thresholds; print what fires
  lint-handoff FILE                validate a handoff artifact's envelope
  handoffs                         list lingering handoff files with age
  handoff-done FILE                close a ratified handoff: delete it, or archive it under
                                   corpora/handoffs/archive/ when corpora/config.md sets debug: yes
  lint-deferred                    validate the non-blocking UI/UX decision queue
  deferred                         list queued decisions grouped by owning composition
  lint-deterministic-shortcut-candidates          validate the persistent deterministic-shortcut-candidate ledger
  deterministic-shortcut-candidates               list candidates with status and sighting count
  record-deterministic-shortcut-candidate [...]   append dated evidence to a candidate
  set-deterministic-shortcut-status [...]         record the operator's candidate disposition
  retro-done --domain D [...]       reset counters after a retrospective (same --domains-dir/--audit
                                   override)
  sync-done [...]                  reset library-drift after a UI-library sync (same
                                   --domains-dir/--audit override)
  compose-spawn-prompt [...]       mechanically assemble a spawn-ready prompt: stance frame +
                                   full domain files (this project's own corpora/domains/, or
                                   --domains-dir) + handoff schema + task, no summarization step;
                                   saves a copy under corpora/session-prompts/ only with --output
                                   or when corpora/config.md sets debug: yes
  screenshot-record [...]          register/update a captured screen variant in the manifest
  screenshot-mark-stale [...]      invalidate screens by direct id or shared-component ripple
  screenshot-status                list current/stale screens in the manifest
  screenshot-lookup --component C  which screens already show component C, and where
  lint-screenshots                 validate the screenshot manifest structurally
  lint-domains --domains-dir D     validate domain frontmatter (subject/posture/applies-when/
                                   units-of-work) — works on any domains-dir, same as kill-report
  manifest [--json]                emit the machine-readable domain index for this project's own
                                   corpora/domains/ (or --domains-dir): every domain's subject/
                                   posture/applies-when/units-of-work plus its principles' id+
                                   condition and conventions' ids — never rule/reason
  select --unit-of-work U [...]    deterministic domain selection for a unit-of-work, evaluated
                                   against corpora/config.md's project-shape — no model in the loop
  import-list --source D           browse a source domains-dir's principles+conventions, flagging
                                   ids already present in the target; read-only, proposes nothing
  import-candidate --source D [...] propose one principle/convention from a source domains-dir as
                                   a candidate (corpora/import-candidates.md), imported-from
                                   provenance, optional --as-domain/--as-id retargeting/rename
  import-default-pool [...]        propose every principle+convention whose applies-when already
                                   matches this project's shape, from every domain in the source
                                   (defaults to this skill's own domains/) — the bootstrap fast path
  check-composition --domains [...] fail (exit 2) if a domain list mixes subjects (coding/design)
                                   or includes a posture: generative domain
  chunk-start --workstream --unit-of-work   print the deterministic composition; writes nothing
  chunk-done --workstream --unit-of-work --stance --handoff [--next]
                                   close a chunk in corpora/chunks/<workstream>.md; fails unless
                                   --handoff names a real handoff for the same workstream — a
                                   chunk record never substitutes for the handoff it points at
  lint-chunks                     validate every corpora/chunks/*.md ledger structurally
  close-workstream --workstream   read-only summary of a workstream's completed chunks
  verify-chunks                    Stop-hook check: recompute select() for every recorded chunk
                                   and compare against its stored domains-composed

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
DEFERRED_STANCE_ENUM = {"convergent", "divergent"}
DEFERRED_STATUS_ENUM = {"queued", "resolved"}
SHORTCUT_STATUS_ENUM = {"open", "deferred", "denied", "accepted", "implemented"}
SHORTCUT_STATUS_REQUIRES_REASON = {"deferred", "denied"}
SCREENSHOT_STATUS_ENUM = {"current", "stale"}
DOMAIN_SUBJECT_ENUM = {"coding", "design", "process"}
DOMAIN_POSTURE_ENUM = {"guardrail", "generative"}
CONFIG_SHAPE_FIELDS = {"language", "framework", "styling", "has-ui", "package-manager"}


def today() -> str:
    return datetime.date.today().isoformat()


def est_tokens(path: str) -> int:
    return os.path.getsize(path) // 4


def fail(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)


def project_debug(project: "Project") -> bool:
    """corpora/config.md's `debug: yes` opt-in — gates audit-trail writes that have no
    functional role otherwise (saved session-prompt copies, retained ratified handoffs)."""
    if not os.path.exists(project.config_path):
        return False
    text = open(project.config_path).read()
    return re.search(r"^debug:\s*(yes|true)\s*$", text, re.MULTILINE | re.IGNORECASE) is not None


# ── project layout ──────────────────────────────────────────────────────────

class Project:
    def __init__(self, root: str, domains_dir: str = "", audit_path: str = ""):
        self.root = root
        self.domains_dir = domains_dir or os.path.join(root, "corpora", "domains")
        self.audit_path = audit_path or os.path.join(self.domains_dir, "audit.md")
        self.handoffs_dir = os.path.join(root, "corpora", "handoffs")
        self.handoffs_archive_dir = os.path.join(self.handoffs_dir, "archive")
        self.config_path = os.path.join(root, "corpora", "config.md")
        self.deferred_path = os.path.join(root, "corpora", "deferred-decisions.md")
        self.deterministic_shortcut_candidates_path = os.path.join(root, "corpora", "deterministic-shortcut-candidates.md")
        self.screenshots_dir = os.path.join(root, "corpora", "screenshots")
        self.screenshot_manifest_path = os.path.join(self.screenshots_dir, "manifest.md")
        self.chunks_dir = os.path.join(root, "corpora", "chunks")
        self.queue_path = os.path.join(root, "corpora", "queue.md")
        self.import_candidates_path = os.path.join(root, "corpora", "import-candidates.md")
        # No existence check here: `corpora/domains/` only ever holds *ratified* project
        # principles, so a freshly-bootstrapped project with nothing ratified yet legitimately
        # has no such directory. A command that only reads (select, manifest, chunk-start/-done,
        # compose-spawn-prompt) must work against a project with zero project-level domains —
        # domain_files() below returns {} rather than raising. A command that writes into this
        # layer (record-gate, retro-done, sync-done, via save()) creates the directory lazily on
        # first write instead. A command whose result is meaningless without it (e.g. record-gate
        # for a specific domain) still fails, but with a message naming what's actually missing,
        # not a blanket precondition every command pays for.

    def domain_files(self) -> dict:
        out = {}
        if not os.path.isdir(self.domains_dir):
            return out
        audit_name = os.path.basename(self.audit_path)
        for name in sorted(os.listdir(self.domains_dir)):
            if name.endswith(".md") and name != audit_name:
                out[name[:-3]] = os.path.join(self.domains_dir, name)
        return out


# ── state block: parse / render ─────────────────────────────────────────────
# The block is flat, fixed-schema YAML the script alone writes, so a purpose-
# built parser is safe. Structure:
#   counters:      list of per-domain dicts
#   efficacy:      list of per-principle dicts
#   library-drift: one dict

ORIGIN_ENUM = {"seed", "project"}


def empty_state() -> dict:
    return {"counters": [], "efficacy": [], "co-occurrence": [], "library-drift": {"since-last-sync": 0}}


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
            section = key if key in ("counters", "efficacy", "co-occurrence", "library-drift") else None
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
            k = k.strip()
            v = v.strip()
            if k == "domains" and v.startswith("[") and v.endswith("]"):
                val = [d.strip() for d in v[1:-1].split(",") if d.strip()]
            else:
                val = int(v) if re.fullmatch(r"-?\d+", v) else v
            if section == "library-drift":
                state[section][k] = val
            elif item is not None:
                item[k] = val
    return state


COUNTER_FIELDS = ["domain", "origin", "since", "ratified", "killed", "graduated", "gate-violations",
                  "working-file-tokens", "baseline-tokens",
                  "principles-at-baseline", "kills-at-baseline", "conventions-at-baseline"]
COOCCURRENCE_FIELDS = ["domains", "count"]


def count_entries(path: str) -> tuple:
    """Count convention, principle, and kill entries in a domain working file.

    Ground truth for `verify`: entries are appended under `conventions:`, `principles:`, and
    `killed:` keys; each entry opens with `- id:`. Tolerant of indentation and
    of the keys appearing inside a yaml fence.
    """
    conventions = principles = kills = 0
    section = None
    for raw in open(path):
        line = raw.strip()
        if re.fullmatch(r"conventions:\s*", line):
            section = "c"
        elif re.fullmatch(r"principles:\s*", line):
            section = "p"
        elif re.fullmatch(r"killed:\s*", line):
            section = "k"
        elif re.match(r"-\s*id:", line):
            if section == "c":
                conventions += 1
            elif section == "p":
                principles += 1
            elif section == "k":
                kills += 1
    return principles, kills, conventions


EFFICACY_FIELDS = ["id", "fired", "violated", "idle"]


def render_state(state: dict) -> str:
    lines = ["```yaml", "counters:"]
    for c in state["counters"]:
        prefix = "  - "
        for f in COUNTER_FIELDS:
            default = "project" if f == "origin" else 0
            lines.append(f"{prefix}{f}: {c.get(f, default)}")
            prefix = "    "
    lines.append("efficacy:")
    for e in state["efficacy"]:
        prefix = "  - "
        for f in EFFICACY_FIELDS:
            lines.append(f"{prefix}{f}: {e.get(f, 0)}")
            prefix = "    "
    lines.append("co-occurrence:")
    for pair in state["co-occurrence"]:
        prefix = "  - "
        for f in COOCCURRENCE_FIELDS:
            if f == "domains":
                lines.append(f"{prefix}domains: [{', '.join(pair.get('domains', []))}]")
            else:
                lines.append(f"{prefix}{f}: {pair.get(f, 0)}")
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
    os.makedirs(os.path.dirname(project.audit_path), exist_ok=True)
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


def counter_for(state: dict, domain: str, tokens: int, path: str = "", origin: str = "project") -> dict:
    for c in state["counters"]:
        if c.get("domain") == domain:
            c.setdefault("graduated", 0)
            c.setdefault("conventions-at-baseline", 0)
            return c
    p, k, conv = count_entries(path) if path else (0, 0, 0)
    c = {"domain": domain, "origin": origin, "since": today(), "ratified": 0, "killed": 0,
         "graduated": 0, "gate-violations": 0, "working-file-tokens": tokens, "baseline-tokens": tokens,
         "principles-at-baseline": p, "kills-at-baseline": k, "conventions-at-baseline": conv}
    state["counters"].append(c)
    return c


def co_occurrence_for(state: dict, domain_a: str, domain_b: str) -> dict:
    pair = sorted([domain_a, domain_b])
    for entry in state["co-occurrence"]:
        if sorted(entry.get("domains", [])) == pair:
            return entry
    entry = {"domains": pair, "count": 0}
    state["co-occurrence"].append(entry)
    return entry


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
        actual_p, actual_k, actual_conv = count_entries(path)
        expect_p = c.get("principles-at-baseline", 0) + c.get("ratified", 0) - c.get("graduated", 0)
        expect_k = c.get("kills-at-baseline", 0) + c.get("killed", 0)
        expect_conv = c.get("conventions-at-baseline", 0) + c.get("graduated", 0)
        if actual_p != expect_p:
            what = "UNRECORDED ratification(s)" if actual_p > expect_p else "entries REMOVED outside a retrospective"
            problems.append(f"{domain}: {abs(actual_p - expect_p)} {what} "
                            f"(file has {actual_p} principles; ledger accounts for {expect_p})")
        if actual_k != expect_k:
            what = "UNRECORDED kill(s)" if actual_k > expect_k else "kill entries REMOVED outside a retrospective"
            problems.append(f"{domain}: {abs(actual_k - expect_k)} {what} "
                            f"(file has {actual_k} kills; ledger accounts for {expect_k})")
        if actual_conv != expect_conv:
            what = "UNRECORDED graduation(s) to convention" if actual_conv > expect_conv else "convention entries REMOVED outside a retrospective"
            problems.append(f"{domain}: {abs(actual_conv - expect_conv)} {what} "
                            f"(file has {actual_conv} conventions; ledger accounts for {expect_conv})")
    if problems:
        print("LEDGER RECONCILIATION FAILED — corpus changed off the books:")
        for p in problems:
            print(f"  - {p}")
        print("Fix: run `record-gate` retroactively for the unrecorded gate(s), or `measure`/`retro-done` to re-baseline knowingly.")
        sys.exit(1)
    print("ledger reconciled: every corpus entry is accounted for by a recorded gate")


def _ids(arg: str) -> list:
    return [s.strip() for s in (arg or "").split(",") if s.strip()]


def cmd_record_gate(project: Project, args) -> None:
    state = load(project)
    files = project.domain_files()
    if args.domain not in files:
        fail(f"unknown domain '{args.domain}' — have: {', '.join(files) or 'none'}")
    tokens = est_tokens(files[args.domain])
    existed = any(c.get("domain") == args.domain for c in state["counters"])
    c = counter_for(state, args.domain, tokens, files[args.domain], origin=args.origin)
    if args.origin != c.get("origin", "project"):
        c["origin"] = args.origin
    if not existed:
        # First registration during a gate: the file already contains the entries
        # this gate ratified/killed/graduated (write-back precedes record-gate), so exclude
        # them from the baseline or verify would double-count them.
        c["principles-at-baseline"] = max(0, c["principles-at-baseline"] - args.ratified + args.graduated)
        c["kills-at-baseline"] = max(0, c["kills-at-baseline"] - args.killed)
        c["conventions-at-baseline"] = max(0, c["conventions-at-baseline"] - args.graduated)
    c["working-file-tokens"] = tokens
    c["ratified"] += args.ratified
    c["killed"] += args.killed
    c["graduated"] += args.graduated
    c["gate-violations"] += args.violations
    for pid in _ids(args.fired):
        efficacy_for(state, pid)["fired"] += 1
    for pid in _ids(args.violated):
        efficacy_for(state, pid)["violated"] += 1
    for pid in _ids(args.idle):
        efficacy_for(state, pid)["idle"] += 1
    if args.ui_drift:
        state["library-drift"]["since-last-sync"] = state["library-drift"].get("since-last-sync", 0) + 1
    for other in _ids(args.co_occurs_with):
        co_occurrence_for(state, args.domain, other)["count"] += 1
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


def parse_ui_drift(front: str) -> dict:
    """Extract the nested `ui-drift: {screens: [...], components: [...]}` field from a
    handoff's frontmatter. Returns only the sub-fields that are present and shaped as a
    bracketed list — the old flat `ui-drift: yes|no` shape yields an empty dict, since
    neither sub-field parses out of it.
    """
    m = re.search(r"^ui-drift:\s*\n((?:[ \t]+\S.*\n?)*)", front, re.MULTILINE)
    if not m:
        return {}
    block = m.group(1)
    result = {}
    for key in ("screens", "components"):
        km = re.search(rf"^\s*{key}:\s*(\[.*?\])\s*$", block, re.MULTILINE)
        if km:
            result[key] = km.group(1)
    return result


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
        fm = re.search(rf"^{name}:[ \t]*(.*)$", front, re.MULTILINE)
        return fm.group(1).strip() if fm else ""

    def field_present(name: str) -> bool:
        return re.search(rf"^{name}:[ \t]*.*$", front, re.MULTILINE) is not None

    stance = field("stance")
    if stance not in ("convergent", "divergent"):
        problems.append(f"frontmatter: stance '{stance}' not in ['convergent', 'divergent']")
    if field_present("composition") and not field("composition"):
        problems.append("frontmatter: composition present but empty")
    status = field("status")
    if status not in STATUS_ENUM:
        problems.append(f"frontmatter: status '{status}' not in {sorted(STATUS_ENUM)}")
    drift = parse_ui_drift(front)
    for key in ("screens", "components"):
        if key not in drift:
            problems.append(f"frontmatter: ui-drift.{key} missing or not a list")
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


def cmd_handoff_done(project: Project, args) -> None:
    """Close a ratified handoff: delete it, or archive it under corpora/handoffs/archive/ when
    corpora/config.md sets debug: yes. The archive is never part of the pending backlog
    `handoffs` reports — it holds only handoffs whose proposals are already written back."""
    path = os.path.abspath(args.file)
    if not os.path.exists(path):
        fail(f"no such file: {args.file}")
    if os.path.dirname(path) != os.path.abspath(project.handoffs_dir):
        fail(f"{args.file} is not directly inside {project.handoffs_dir}")
    if project_debug(project):
        os.makedirs(project.handoffs_archive_dir, exist_ok=True)
        dest = os.path.join(project.handoffs_archive_dir, os.path.basename(path))
        os.replace(path, dest)
        print(f"archived to {dest}")
    else:
        os.remove(path)
        print(f"deleted {path}")


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
    required = ("id", "stance", "domain", "question", "context", "source-workstream",
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
        if entry.get("stance") not in DEFERRED_STANCE_ENUM:
            problems.append(f"{label}: stance must be one of {sorted(DEFERRED_STANCE_ENUM)}")
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
    for stance in sorted(DEFERRED_STANCE_ENUM):
        owned = [entry for entry in queued if entry["stance"] == stance]
        if not owned:
            continue
        print(f"  {stance} ({len(owned)}):")
        for entry in owned:
            print(f"    - {entry['id']}  domain={entry['domain']}  workstream={entry['source-workstream']}")
            print(f"      {entry['question']}")


def parse_deterministic_shortcut_candidates(path: str) -> list:
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


def deterministic_shortcut_candidate_problems(entries: list) -> list:
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
        if entry.get("status") not in SHORTCUT_STATUS_ENUM:
            problems.append(f"{label}: status must be one of {sorted(SHORTCUT_STATUS_ENUM)}")
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
        if entry.get("status") in SHORTCUT_STATUS_REQUIRES_REASON and not entry.get("disposition-reason"):
            problems.append(f"{label}: {entry.get('status')} status requires disposition reason")
    return problems


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def save_deterministic_shortcut_candidates(path: str, entries: list) -> None:
    lines = ["# Deterministic shortcut candidates", "", "```yaml"]
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


def cmd_lint_deterministic_shortcut_candidates(project: Project, _args) -> None:
    path = project.deterministic_shortcut_candidates_path
    if not os.path.exists(path):
        fail("no corpora/deterministic-shortcut-candidates.md — create it from the kernel schema")
    entries = parse_deterministic_shortcut_candidates(path)
    problems = deterministic_shortcut_candidate_problems(entries)
    if problems:
        print(f"FAIL {path}")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    print(f"PASS {path} ({len(entries)} entries)")


def cmd_deterministic_shortcut_candidates(project: Project, _args) -> None:
    path = project.deterministic_shortcut_candidates_path
    if not os.path.exists(path):
        print("deterministic shortcut candidate ledger: absent")
        return
    entries = parse_deterministic_shortcut_candidates(path)
    if deterministic_shortcut_candidate_problems(entries):
        print("deterministic shortcut candidate ledger is invalid; run `lint-deterministic-shortcut-candidates`")
        sys.exit(1)
    if not entries:
        print("deterministic shortcut candidate ledger: empty")
        return
    print("deterministic shortcut candidates:")
    for entry in entries:
        dates = [evidence["date"] for evidence in entry["evidence"]]
        print(f"  - {entry['id']}  status={entry['status']}  sightings={len(dates)}  "
              f"first={min(dates)}  last={max(dates)}")
        print(f"    {entry['operation-shape']}")


def cmd_record_deterministic_shortcut_candidate(project: Project, args) -> None:
    path = project.deterministic_shortcut_candidates_path
    if not os.path.exists(path):
        fail("no corpora/deterministic-shortcut-candidates.md — create it from the kernel schema")
    entries = parse_deterministic_shortcut_candidates(path)
    problems = deterministic_shortcut_candidate_problems(entries)
    if problems:
        fail("deterministic shortcut candidate ledger is invalid — run `lint-deterministic-shortcut-candidates`")
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
        print(f"deterministic shortcut candidate {args.id}: identical evidence already recorded")
        return
    entry["evidence"].append(evidence)
    save_deterministic_shortcut_candidates(path, entries)
    sightings = len(entry["evidence"])
    print(f"deterministic shortcut candidate {args.id}: recorded sighting {sightings}")
    if sightings > 1 or entry["status"] in {"deferred", "denied"}:
        print(f"RESURFACE {args.id}: status={entry['status']} with {sightings} sightings")


def cmd_set_deterministic_shortcut_status(project: Project, args) -> None:
    path = project.deterministic_shortcut_candidates_path
    if not os.path.exists(path):
        fail("no corpora/deterministic-shortcut-candidates.md — create it from the kernel schema")
    entries = parse_deterministic_shortcut_candidates(path)
    problems = deterministic_shortcut_candidate_problems(entries)
    if problems:
        fail("deterministic shortcut candidate ledger is invalid — run `lint-deterministic-shortcut-candidates`")
    entry = next((candidate for candidate in entries if candidate["id"] == args.id), None)
    if entry is None:
        fail(f"unknown deterministic shortcut candidate '{args.id}'")
    if args.status in SHORTCUT_STATUS_REQUIRES_REASON and not args.reason:
        fail(f"status '{args.status}' requires --reason")
    entry["status"] = args.status
    entry["disposition-reason"] = args.reason or ""
    save_deterministic_shortcut_candidates(path, entries)
    print(f"deterministic shortcut candidate {args.id}: status={args.status}")


# ── screenshot cache: manifest parse / render / commands ────────────────────
# `screens: [{..., variants: [{...}]}]` is two levels of nested lists — same depth as
# `candidates: [{..., evidence: [{...}]}]`, so the parser is modeled on
# `parse_deterministic_shortcut_candidates`, not the flat `parse_state`, which cannot represent it.

def parse_screenshot_manifest(path: str) -> list:
    entries = []
    item = None
    variant = None
    in_screens = False
    in_variants = False
    for raw in open(path):
        line = raw.rstrip()
        stripped = line.strip()
        if in_screens and stripped == "```":
            break
        if stripped in {"screens:", "screens: []"}:
            in_screens = True
            continue
        if not in_screens or not stripped or stripped.startswith(("#", "```")):
            continue
        if re.match(r"^\s{2}-\s+id:\s*", line):
            item = {"components": [], "variants": []}
            entries.append(item)
            item["id"] = stripped.partition(":")[2].strip().strip('"').strip("'")
            in_variants = False
            continue
        if item is None:
            continue
        top = re.match(r"^\s{4}([a-z][a-z0-9-]*):\s*(.*)$", line)
        if top:
            key, value = top.groups()
            in_variants = key == "variants"
            if in_variants:
                variant = None
                continue
            if key == "components":
                value = value.strip()
                if value.startswith("[") and value.endswith("]"):
                    item["components"] = [c.strip() for c in value[1:-1].split(",") if c.strip()]
                else:
                    item["components"] = []
                continue
            item[key] = value.strip().strip('"').strip("'")
            continue
        label_m = re.match(r"^\s{6}-\s+label:\s*(.*)$", line)
        if in_variants and label_m:
            variant = {"label": label_m.group(1).strip().strip('"').strip("'")}
            item["variants"].append(variant)
            continue
        field_m = re.match(r"^\s{8}(path|captured):\s*(.*)$", line)
        if in_variants and variant is not None and field_m:
            key, value = field_m.groups()
            variant[key] = value.strip().strip('"').strip("'")
    return entries


def screenshot_manifest_problems(entries: list, screenshots_dir: str) -> list:
    problems = []
    seen = set()
    referenced = set()
    for index, entry in enumerate(entries, 1):
        label = entry.get("id") or f"entry {index}"
        if not entry.get("id"):
            problems.append(f"{label}: missing id")
        if entry.get("id") in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(entry.get("id"))
        if entry.get("status") not in SCREENSHOT_STATUS_ENUM:
            problems.append(f"{label}: status must be one of {sorted(SCREENSHOT_STATUS_ENUM)}")
        if not entry.get("last-touched"):
            problems.append(f"{label}: missing last-touched")
        if not entry.get("variants"):
            problems.append(f"{label}: requires at least one variant")
        for vindex, variant in enumerate(entry.get("variants", []), 1):
            vlabel = f"{label} variant {vindex}"
            if not variant.get("label"):
                problems.append(f"{vlabel}: missing label")
            path = variant.get("path", "")
            if not path:
                problems.append(f"{vlabel}: missing path")
            else:
                referenced.add(path)
                if not os.path.exists(os.path.join(screenshots_dir, path)):
                    problems.append(f"{vlabel}: path '{path}' does not exist on disk")
            captured = variant.get("captured", "")
            if not captured:
                problems.append(f"{vlabel}: missing captured date")
            else:
                try:
                    datetime.date.fromisoformat(captured)
                except ValueError:
                    problems.append(f"{vlabel}: captured must be valid YYYY-MM-DD")
    if os.path.isdir(screenshots_dir):
        for root, _dirs, files in os.walk(screenshots_dir):
            for name in files:
                if not name.endswith(".png"):
                    continue
                rel = os.path.relpath(os.path.join(root, name), screenshots_dir)
                if rel not in referenced:
                    problems.append(f"orphaned image not in manifest: {rel}")
    return problems


def save_screenshot_manifest(path: str, entries: list) -> None:
    lines = ["# Screenshot manifest", "", "```yaml"]
    if not entries:
        lines.append("screens: []")
    else:
        lines.append("screens:")
        for entry in entries:
            lines.extend([
                f"  - id: {entry['id']}",
                f"    components: [{', '.join(entry.get('components', []))}]",
                f"    status: {entry['status']}",
                f"    last-touched: {entry['last-touched']}",
                "    variants:",
            ])
            for variant in entry["variants"]:
                lines.extend([
                    f"      - label: {variant['label']}",
                    f"        path: {variant['path']}",
                    f"        captured: {variant['captured']}",
                ])
    lines.extend(["```", ""])
    open(path, "w").write("\n".join(lines))


def cmd_lint_screenshots(project: Project, _args) -> None:
    path = project.screenshot_manifest_path
    if not os.path.exists(path):
        fail("no corpora/screenshots/manifest.md — create it (e.g. via bootstrap Phase 2's "
             "seeding step) before linting")
    entries = parse_screenshot_manifest(path)
    problems = screenshot_manifest_problems(entries, project.screenshots_dir)
    if problems:
        print(f"FAIL {path}")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    print(f"PASS {path} ({len(entries)} screens)")


def cmd_screenshot_status(project: Project, _args) -> None:
    path = project.screenshot_manifest_path
    if not os.path.exists(path):
        print("screenshot manifest: absent")
        return
    entries = parse_screenshot_manifest(path)
    if screenshot_manifest_problems(entries, project.screenshots_dir):
        print("screenshot manifest is invalid; run `lint-screenshots`")
        sys.exit(1)
    if not entries:
        print("screenshot manifest: empty")
        return
    current = sorted((e for e in entries if e.get("status") == "current"), key=lambda e: e["id"])
    stale = sorted((e for e in entries if e.get("status") == "stale"), key=lambda e: e["id"])
    print(f"screenshot manifest: {len(current)} current, {len(stale)} stale")
    if current:
        print("  current:")
        for entry in current:
            print(f"    - {entry['id']}  components=[{', '.join(entry.get('components', []))}]")
    if stale:
        print("  stale:")
        for entry in stale:
            print(f"    - {entry['id']}  components=[{', '.join(entry.get('components', []))}]")


def cmd_screenshot_lookup(project: Project, args) -> None:
    path = project.screenshot_manifest_path
    if not os.path.exists(path):
        print("screenshot manifest: absent")
        return
    entries = parse_screenshot_manifest(path)
    if screenshot_manifest_problems(entries, project.screenshots_dir):
        print("screenshot manifest is invalid; run `lint-screenshots`")
        sys.exit(1)
    matches = [e for e in entries if args.component in e.get("components", [])]
    if not matches:
        print(f"no screens tagged with component '{args.component}'")
        return
    print(f"screens showing '{args.component}':")
    for entry in matches:
        for variant in entry.get("variants", []):
            print(f"  - {entry['id']} ({variant['label']}): {variant['path']}  status={entry['status']}")


def cmd_screenshot_record(project: Project, args) -> None:
    path = project.screenshot_manifest_path
    entries = parse_screenshot_manifest(path) if os.path.exists(path) else []
    entry = next((e for e in entries if e["id"] == args.screen), None)
    if entry is None:
        entry = {"id": args.screen, "components": [], "status": "current",
                  "last-touched": today(), "variants": []}
        entries.append(entry)
    entry["components"] = _ids(args.components)
    entry["status"] = "current"
    entry["last-touched"] = today()
    variant = next((v for v in entry["variants"] if v["label"] == args.variant), None)
    if variant is None:
        entry["variants"].append({"label": args.variant, "path": args.path, "captured": today()})
    else:
        variant["path"] = args.path
        variant["captured"] = today()
    os.makedirs(project.screenshots_dir, exist_ok=True)
    save_screenshot_manifest(path, entries)
    print(f"screenshot recorded: {args.screen}/{args.variant} -> {args.path} "
          f"(status=current, components=[{', '.join(entry['components'])}])")


def cmd_screenshot_mark_stale(project: Project, args) -> None:
    path = project.screenshot_manifest_path
    if not os.path.exists(path):
        print("screenshot manifest: absent — nothing to mark stale")
        return
    entries = parse_screenshot_manifest(path)
    if screenshot_manifest_problems(entries, project.screenshots_dir):
        fail("screenshot manifest is invalid — run `lint-screenshots`")
    direct = set(_ids(args.screens))
    ripple_components = set(_ids(args.components))
    invalidated = []
    for entry in entries:
        rippled = bool(ripple_components & set(entry.get("components", [])))
        if entry["id"] in direct or rippled:
            if entry.get("status") != "stale":
                invalidated.append(entry["id"])
            entry["status"] = "stale"
    save_screenshot_manifest(path, entries)
    print(f"marked stale: {', '.join(invalidated) if invalidated else 'none'}")


def cmd_retro_done(project: Project, args) -> None:
    state = load(project)
    for c in state["counters"]:
        if c["domain"] == args.domain:
            files = project.domain_files()
            if args.domain in files:
                tokens = est_tokens(files[args.domain])
                p, k, conv = count_entries(files[args.domain])
            else:
                tokens = c["working-file-tokens"]
                p, k, conv = (c.get("principles-at-baseline", 0), c.get("kills-at-baseline", 0),
                               c.get("conventions-at-baseline", 0))
            c.update({"since": today(), "ratified": 0, "killed": 0, "graduated": 0, "gate-violations": 0,
                      "working-file-tokens": tokens, "baseline-tokens": tokens,
                      "principles-at-baseline": p, "kills-at-baseline": k, "conventions-at-baseline": conv})
            save(project, state)
            print(f"reset counters for {args.domain}; baseline-tokens={tokens}, principles={p}, kills={k}")
            return
    fail(f"no counters for domain '{args.domain}'")


def cmd_sync_done(project: Project, _args) -> None:
    state = load(project)
    state["library-drift"]["since-last-sync"] = 0
    save(project, state)
    print("library-drift reset to 0")


def skill_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── domain selection API: frontmatter, manifest, select, check-composition ──────────────────
#
# An external process layer selects domains by querying data instead of reading
# preambles — see `kernel.md`, "Spawns: stance + composition." Every load condition previously
# stated in prose is machine-evaluable already; this section is the seam.

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _parse_inline_list(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [x.strip() for x in inner.split(",")] if inner else []
    return [value] if value else []


def parse_domain_frontmatter(path: str):
    """Parse a domain file's frontmatter block. Returns None if the file has none (not yet
    migrated to the schema in `kernel.md`, "Spawns: stance + composition")."""
    text = open(path).read()
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    data = {"subject": None, "posture": None, "applies-when": [], "units-of-work": [], "universal": False}
    lines = m.group(1).split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("subject:"):
            data["subject"] = line.split(":", 1)[1].strip()
        elif line.startswith("posture:"):
            data["posture"] = line.split(":", 1)[1].strip()
        elif line.startswith("universal:"):
            data["universal"] = line.split(":", 1)[1].strip().lower() == "true"
        elif line.startswith("units-of-work:"):
            data["units-of-work"] = _parse_inline_list(line.split(":", 1)[1])
        elif re.fullmatch(r"applies-when:\s*", line):
            i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                key, _, val = lines[i][4:].partition(":")
                data["applies-when"].append((key.strip(), _parse_inline_list(val)
                                              if val.strip().startswith("[") else val.strip()))
                i += 1
            continue
        i += 1
    return data


def parse_domain_conditions(path: str) -> list:
    """Extract `id` + `condition` (only — never `rule`/`reason`) for every active principle, so a
    routing layer can see when a principle applies without seeing what it says."""
    text = open(path).read()
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    section = None
    current_id = None
    conditions = []
    for raw in body.split("\n"):
        stripped = raw.strip()
        if re.fullmatch(r"conventions:", stripped):
            section = "c"
            continue
        if re.fullmatch(r"principles:", stripped):
            section = "p"
            continue
        if re.fullmatch(r"killed:", stripped):
            section = "k"
            continue
        if section != "p":
            continue
        m_id = re.match(r"-\s*id:\s*(\S+)", stripped)
        if m_id:
            current_id = m_id.group(1)
            continue
        m_cond = re.match(r'condition:\s*"(.*)"\s*$', stripped)
        if m_cond and current_id:
            conditions.append({"id": current_id, "condition": m_cond.group(1)})
            current_id = None
    return conditions


def parse_domain_conventions(path: str) -> list:
    """Extract every `conventions:` entry's `id` plus which of `rule`/`reason`/`condition` are
    present, for `lint-domains`'s shape check and `manifest`'s id listing. A convention is
    unconditioned by definition (kernel.md, 'Retired principle — graduated to a convention') — a
    `condition` field here is a shape error, not a valid variant of the schema."""
    text = open(path).read()
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    section = None
    current = None
    entries = []
    for raw in body.split("\n"):
        stripped = raw.strip()
        if re.fullmatch(r"conventions:", stripped):
            section = "c"
            current = None
            continue
        if re.fullmatch(r"principles:", stripped):
            section = "p"
            current = None
            continue
        if re.fullmatch(r"killed:", stripped):
            section = "k"
            current = None
            continue
        if section != "c":
            continue
        m_id = re.match(r"-\s*id:\s*(\S+)", stripped)
        if m_id:
            current = {"id": m_id.group(1), "rule": False, "reason": False, "condition": False}
            entries.append(current)
            continue
        if current is None:
            continue
        for field in ("rule", "reason", "condition"):
            if re.match(rf"{field}:\s*\S", stripped):
                current[field] = True
    return entries


def domain_lint_problems(domains_dir: str) -> list:
    problems = []
    for name in sorted(os.listdir(domains_dir)):
        if not name.endswith(".md") or name == "audit.md":
            continue
        domain = name[:-3]
        fm = parse_domain_frontmatter(os.path.join(domains_dir, name))
        if fm is None:
            problems.append(f"{domain}: no frontmatter block")
            continue
        if fm["subject"] not in DOMAIN_SUBJECT_ENUM:
            problems.append(f"{domain}: subject '{fm['subject']}' not in {sorted(DOMAIN_SUBJECT_ENUM)}")
        if fm["posture"] not in DOMAIN_POSTURE_ENUM:
            problems.append(f"{domain}: posture '{fm['posture']}' not in {sorted(DOMAIN_POSTURE_ENUM)}")
        if not fm["universal"] and not fm["units-of-work"]:
            problems.append(f"{domain}: units-of-work is empty and universal is not true")
        for key, _ in fm["applies-when"]:
            if key not in CONFIG_SHAPE_FIELDS:
                problems.append(f"{domain}: applies-when references unknown config field '{key}'")
        for conv in parse_domain_conventions(os.path.join(domains_dir, name)):
            label = conv["id"] or "(no id)"
            if not conv["rule"]:
                problems.append(f"{domain}: convention '{label}' missing rule")
            if not conv["reason"]:
                problems.append(f"{domain}: convention '{label}' missing reason")
            if conv["condition"]:
                problems.append(f"{domain}: convention '{label}' has a condition — "
                                 "conventions are unconditioned by definition")
    return problems


def cmd_lint_domains(args) -> None:
    problems = domain_lint_problems(args.domains_dir)
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        sys.exit(2)
    print(f"lint-domains: ok ({args.domains_dir})")


def parse_config_shape(config_path: str) -> dict:
    if not os.path.exists(config_path):
        return {}
    text = open(config_path).read()
    m = re.search(r"^## project-shape\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL | re.MULTILINE)
    if not m:
        return {}
    shape = {}
    for line in m.group(1).split("\n"):
        line = line.strip()
        if not line or line.startswith("<!--") or line.startswith("see:"):
            continue
        mm = re.match(r"([\w-]+):\s*(.*)$", line)
        if mm:
            shape[mm.group(1)] = mm.group(2).strip()
    return shape


def _normalize_shape_value(v: str) -> str:
    return re.sub(r"[^a-z0-9]", "", v.lower())


def applies_when_matches(applies_when: list, shape: dict) -> bool:
    for key, val in applies_when:
        actual = _normalize_shape_value(shape.get(key, ""))
        if val == "not-none":
            if actual in ("", "none"):
                return False
            continue
        options = val if isinstance(val, list) else [val]
        if actual not in {_normalize_shape_value(o) for o in options}:
            return False
    return True


def select_domains(sources: dict, shape: dict, unit_of_work: str) -> list:
    selected = []
    for name, path in sources.items():
        fm = parse_domain_frontmatter(path)
        if fm is None:
            continue
        if fm["universal"]:
            selected.append(name)
            continue
        if unit_of_work not in fm["units-of-work"]:
            continue
        if not applies_when_matches(fm["applies-when"], shape):
            continue
        selected.append(name)
    return sorted(selected)


def cmd_select(project: "Project", args) -> None:
    config_path = args.config or project.config_path
    shape = parse_config_shape(config_path)
    sources = project.domain_files()
    selected = select_domains(sources, shape, args.unit_of_work)
    if args.json:
        import json
        print(json.dumps({"unit-of-work": args.unit_of_work, "domains": selected}))
    else:
        print(", ".join(selected) if selected else "(no domains selected)")


def cmd_manifest(project: "Project", args) -> None:
    sources = project.domain_files()
    entries = []
    for name in sorted(sources):
        path = sources[name]
        fm = parse_domain_frontmatter(path)
        if fm is None:
            continue
        entries.append({
            "name": name,
            "subject": fm["subject"],
            "posture": fm["posture"],
            "applies_when": [{k: v} for k, v in fm["applies-when"]],
            "units_of_work": fm["units-of-work"],
            "universal": fm["universal"],
            "conditions": parse_domain_conditions(path),
            "conventions": [c["id"] for c in parse_domain_conventions(path)],
        })
    if args.json:
        import json
        print(json.dumps({"domains": entries}, indent=2))
    else:
        for e in entries:
            print(f"{e['name']}: subject={e['subject']} posture={e['posture']} "
                  f"units-of-work={e['units_of_work']} universal={e['universal']}")


def check_composition_problems(named_frontmatter: list) -> list:
    """named_frontmatter: list of (name, frontmatter-or-None). Fails on any `posture: generative`
    domain (kernel.md, 'The hard line' — no legitimate instance exists today) and on mixed
    coding/design subjects in one composition (subject separation), ignoring universal domains. A
    domain with no frontmatter (e.g. a project-only domain born fresh at the ratify gate, not yet
    carrying the schema) is not itself an error here — it contributes no subject and is skipped;
    `lint-domains` is the place that flags missing frontmatter as a structural problem."""
    problems = []
    subjects = set()
    for name, fm in named_frontmatter:
        if fm is None:
            continue
        if fm["posture"] == "generative":
            problems.append(f"{name}: posture 'generative' is a ratify-gate rejection, not a "
                             "valid domain to compose (kernel.md, 'The hard line')")
        if not fm["universal"]:
            subjects.add(fm["subject"])
    if len(subjects - {None}) > 1:
        problems.append(f"mixed subjects in one composition: {sorted(subjects - {None})}")
    return problems


def cmd_check_composition(project: "Project", args) -> None:
    domains = _ids(args.domains)
    if not domains:
        fail("--domains requires at least one comma-separated domain name")
    sources = project.domain_files()
    named = [(d, parse_domain_frontmatter(sources[d]) if d in sources else None) for d in domains]
    problems = check_composition_problems(named)
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        sys.exit(2)
    print(f"check-composition: ok ({', '.join(domains)})")


# ── import: propose principles/conventions from another domains-dir as candidates ────────────
#
# kernel.md, "Project corpora"/proposals/domain-repo-import.md §3: an import is a new *producer*
# of candidates, structurally the same relationship discovery-agent.md/session-harvest-agent.md
# already have to a candidates file and the gate — the operator still browses and picks, per
# principle, and the gate still ratifies. This never writes into a domain working file directly.

def collect_domain_ids(path: str) -> set:
    """Every id already present in a domain working file — conventions, principles, and killed
    entries alike — so import-candidate can refuse a collision regardless of which section an id
    already occupies."""
    ids = set()
    for raw in open(path):
        m = re.match(r"\s*-\s*id:\s*(\S+)", raw)
        if m:
            ids.add(m.group(1))
    return ids


def parse_domain_section_full(path: str, section_name: str) -> dict:
    """Extract every entry's full `rule`/`condition`/`reason` (whichever are present) from one
    section (`principles` or `conventions`) of a domain working file, keyed by `id` — the same
    tolerant flat-scan style as `parse_domain_conditions`/`parse_domain_conventions`, extended to
    capture `rule`/`reason` too since import-candidate needs the whole entry, not just its id."""
    text = open(path).read()
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    section = None
    current = None
    entries = {}
    for raw in body.split("\n"):
        stripped = raw.strip()
        if re.fullmatch(r"conventions:", stripped):
            section, current = "conventions", None
            continue
        if re.fullmatch(r"principles:", stripped):
            section, current = "principles", None
            continue
        if re.fullmatch(r"killed:", stripped):
            section, current = "killed", None
            continue
        if section != section_name:
            continue
        m_id = re.match(r"-\s*id:\s*(\S+)", stripped)
        if m_id:
            current = m_id.group(1)
            entries[current] = {}
            continue
        if current is None:
            continue
        for field in ("rule", "condition", "reason"):
            fm_field = re.match(rf'{field}:\s*"(.*)"\s*$', stripped)
            if fm_field:
                entries[current][field] = fm_field.group(1)
        m_see_also = re.match(r"see-also:\s*(\S.*)$", stripped)
        if m_see_also:
            entries[current]["see-also"] = m_see_also.group(1).strip()
    return entries


def find_import_entry(source_dir: str, domain: str, entry_id: str) -> tuple:
    """Locate `entry_id` in `source_dir/<domain>.md`, principles first then conventions. Returns
    (kind, fields) where kind is "principle" or "convention", or fails if not found in either."""
    path = os.path.join(source_dir, f"{domain}.md")
    if not os.path.exists(path):
        fail(f"no domain '{domain}' under {source_dir}")
    principles = parse_domain_section_full(path, "principles")
    if entry_id in principles:
        return "principle", principles[entry_id]
    conventions = parse_domain_section_full(path, "conventions")
    if entry_id in conventions:
        return "convention", conventions[entry_id]
    fail(f"no principle or convention '{entry_id}' in {path}")


def source_originally_ratified(source_dir: str, entry_id: str) -> str:
    """Best-effort: the source's own audit.md provenance date for this id, if the source layer has
    one. Returns "" when unavailable — never fabricated."""
    audit_path = os.path.join(source_dir, "audit.md")
    if not os.path.exists(audit_path):
        return ""
    entries = parse_audit_entries(audit_path)
    entry = entries.get(entry_id)
    return entry.get("provenance", "").strip('"') if entry else ""


def append_import_candidate(target_path: str, fields: dict) -> None:
    lines = []
    lines.append(f"- id: {fields['id']}")
    lines.append(f"  rule: {yaml_quote(fields['rule'])}")
    if "condition" in fields:
        lines.append(f"  condition: {yaml_quote(fields['condition'])}")
    lines.append(f"  reason: {yaml_quote(fields['reason'])}")
    lines.append(f"  domains: [{fields['domain']}]")
    lines.append("  kind: judgment")
    lines.append("  provenance:")
    lines.append("    imported-from:")
    lines.append(f"      source: {yaml_quote(fields['source'])}")
    lines.append(f"      domain: {fields['source-domain']}")
    if fields.get("source-id") and fields["source-id"] != fields["id"]:
        lines.append(f"      id: {fields['source-id']}")
    if fields.get("originally-ratified"):
        lines.append(f"      originally-ratified: {yaml_quote(fields['originally-ratified'])}")
    lines.append(f"    extracted: {today()}")
    block = "\n".join(lines) + "\n"

    if os.path.exists(target_path):
        text = open(target_path).read()
    else:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        text = "# Import candidates\n\nProposed at the ratify gate like any other candidate " \
               "(kernel.md, \"Domain assignment at the gate\") — the operator still browses and " \
               "picks the destination domain per entry.\n\n```yaml\ncandidates:\n```\n"
    if "```yaml" not in text or "candidates:" not in text:
        fail(f"{target_path} does not have a recognizable 'candidates:' block — fix by hand")
    before, _, rest = text.partition("```yaml")
    fence_body, _, after = rest.partition("\n```")
    if fence_body.rstrip().endswith("candidates: []"):
        fence_body = fence_body.rstrip()[: -len("candidates: []")] + "candidates:\n" + block.rstrip("\n")
    else:
        fence_body = fence_body.rstrip("\n") + "\n" + block.rstrip("\n")
    text = before + "```yaml" + fence_body + "\n```" + after
    open(target_path, "w").write(text)


def cmd_import_list(project: "Project", args) -> None:
    target_domains_dir = args.target_domains_dir or project.domains_dir
    target_ids = set()
    if os.path.isdir(target_domains_dir):
        for name in os.listdir(target_domains_dir):
            if name.endswith(".md") and name != "audit.md":
                target_ids |= collect_domain_ids(os.path.join(target_domains_dir, name))
    printed = 0
    for name in sorted(os.listdir(args.source)):
        if not name.endswith(".md") or name == "audit.md":
            continue
        domain = name[:-3]
        path = os.path.join(args.source, name)
        for kind, section in (("principle", "principles"), ("convention", "conventions")):
            for entry_id, fields in sorted(parse_domain_section_full(path, section).items()):
                already = entry_id in target_ids
                rule = fields.get("rule", "")
                flag = " [already present]" if already else ""
                print(f"{domain}/{entry_id} ({kind}){flag}: {rule}")
                printed += 1
    if not printed:
        print(f"no principles or conventions found under {args.source}")


def cmd_import_candidate(project: "Project", args) -> None:
    kind, fields = find_import_entry(args.source, args.domain, args.id)
    dest_domain = args.as_domain or args.domain
    dest_id = args.as_id or args.id
    target_domains_dir = args.target_domains_dir or project.domains_dir
    existing = set()
    dest_path = os.path.join(target_domains_dir, f"{dest_domain}.md")
    if os.path.exists(dest_path):
        existing = collect_domain_ids(dest_path)
    if dest_id in existing:
        fail(f"'{dest_id}' already exists in {dest_path} — pass --as-id to import under a "
             "different id")
    entry = {
        "id": dest_id, "rule": fields.get("rule", ""), "reason": fields.get("reason", ""),
        "domain": dest_domain, "source": args.source, "source-domain": args.domain,
        "source-id": args.id if args.id != dest_id else "",
        "originally-ratified": source_originally_ratified(args.source, args.id),
    }
    if kind == "principle" and "condition" in fields:
        entry["condition"] = fields["condition"]
    target = args.output or project.import_candidates_path
    append_import_candidate(target, entry)
    print(f"proposed {kind} '{args.id}' from {args.source}/{args.domain} as candidate "
          f"'{dest_id}' -> {dest_domain} in {target}")


def default_pool_domains(source_dir: str, shape: dict) -> list:
    """Every domain in `source_dir` whose `applies-when` already matches this project's shape (or
    is universal) — the day-one bulk-import pool, independent of any one unit-of-work (kernel.md,
    'Project corpora')."""
    selected = []
    for name in sorted(os.listdir(source_dir)):
        if not name.endswith(".md") or name == "audit.md":
            continue
        fm = parse_domain_frontmatter(os.path.join(source_dir, name))
        if fm is None:
            continue
        if fm["universal"] or applies_when_matches(fm["applies-when"], shape):
            selected.append(name[:-3])
    return selected


def cmd_import_default_pool(project: "Project", args) -> None:
    source_dir = args.source or os.path.join(skill_root(), "domains")
    config_path = args.config or project.config_path
    shape = parse_config_shape(config_path)
    target_domains_dir = args.target_domains_dir or project.domains_dir
    target = args.output or project.import_candidates_path
    proposed = 0
    for domain in default_pool_domains(source_dir, shape):
        existing = set()
        dest_path = os.path.join(target_domains_dir, f"{domain}.md")
        if os.path.exists(dest_path):
            existing = collect_domain_ids(dest_path)
        source_path = os.path.join(source_dir, f"{domain}.md")
        for kind, section in (("principle", "principles"), ("convention", "conventions")):
            for entry_id, fields in sorted(parse_domain_section_full(source_path, section).items()):
                if entry_id in existing:
                    continue
                entry = {
                    "id": entry_id, "rule": fields.get("rule", ""), "reason": fields.get("reason", ""),
                    "domain": domain, "source": source_dir, "source-domain": domain, "source-id": "",
                    "originally-ratified": source_originally_ratified(source_dir, entry_id),
                }
                if kind == "principle" and "condition" in fields:
                    entry["condition"] = fields["condition"]
                append_import_candidate(target, entry)
                proposed += 1
    print(f"proposed {proposed} candidate(s) from {source_dir}'s default pool -> {target}")


# ── migration: materialize a pre-dissolution project's live-merged view once ─────────────────
#
# processes/domain-repo-migration.md: a project bootstrapped under the old live seed/project merge
# writes what was previously computed live into its own corpora/domains/, once, so nothing it
# already relied on silently disappears when the merge stops. This bypasses the candidate/gate
# pipeline deliberately — it isn't proposing new judgment, it's making already-active judgment
# explicit; write-back's ordinary review would ask the operator to re-approve content the project
# was already running on. Scoped to `principles:`/`conventions:` only — the active guidance a spawn
# actually loads; a domain's `killed:` log is not migrated (documented gap, `processes/
# domain-repo-migration.md`; a re-proposed already-killed idea is a low-cost, self-correcting
# failure mode, not silent content loss).

def render_migrated_domain(domain: str, frontmatter: str, last_retrospective: str,
                            conventions: dict, principles: dict) -> str:
    lines = ["```yaml", f"last-retrospective: {last_retrospective}", "", "conventions:", ""]
    for entry_id, fields in conventions.items():
        lines.append(f"- id: {entry_id}")
        lines.append(f"  rule: {yaml_quote(fields.get('rule', ''))}")
        lines.append(f"  reason: {yaml_quote(fields.get('reason', ''))}")
        if fields.get("see-also"):
            lines.append(f"  see-also: {fields['see-also']}")
        lines.append("")
    lines += ["principles:", ""]
    for entry_id, fields in principles.items():
        lines.append(f"- id: {entry_id}")
        lines.append(f"  rule: {yaml_quote(fields.get('rule', ''))}")
        lines.append(f"  condition: {yaml_quote(fields.get('condition', ''))}")
        lines.append(f"  reason: {yaml_quote(fields.get('reason', ''))}")
        if fields.get("see-also"):
            lines.append(f"  see-also: {fields['see-also']}")
        lines.append("")
    lines += ["killed:", "```"]
    body = "\n".join(lines) + "\n"
    header = frontmatter if frontmatter else ""
    return f"{header}\n# Domain: {domain}\n\n{body}"


def append_migration_provenance(audit_path: str, domain: str, ids: list) -> None:
    if not ids:
        return
    lines = []
    for entry_id in ids:
        lines.append(f"- id: {entry_id}")
        lines.append(f"  domain: {domain}")
        lines.append(f"  provenance: \"Migrated from seed, {today()}.\"")
        lines.append("  history:")
        lines.append(f"    - date: {today()}")
        lines.append("      type: migrated-from-seed")
        lines.append(f"      reason: \"processes/domain-repo-migration.md: materialized from what "
                     f"the pre-dissolution live seed/project merge was already applying.\"")
        lines.append("")
    block = "\n".join(lines)
    if os.path.exists(audit_path):
        text = open(audit_path).read()
    else:
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        text = "# Audit — project layer\n\n```yaml\nprovenance:\n```\n"
    if "```yaml" not in text or "provenance:" not in text:
        fail(f"{audit_path} does not have a recognizable 'provenance:' block — fix by hand")
    before, _, rest = text.partition("```yaml")
    fence_body, _, after = rest.partition("\n```")
    fence_body = fence_body.rstrip("\n") + "\n" + block.rstrip("\n")
    text = before + "```yaml" + fence_body + "\n```" + after
    open(audit_path, "w").write(text)


def cmd_migrate_domains(project: "Project", args) -> None:
    source_dir = args.source or os.path.join(skill_root(), "domains")
    config_path = args.config or project.config_path
    shape = parse_config_shape(config_path)
    domains = sorted(set(_ids(args.domains) or default_pool_domains(source_dir, shape))
                      | set(project.domain_files().keys()))
    os.makedirs(project.domains_dir, exist_ok=True)
    migrated = []
    for domain in domains:
        seed_path = os.path.join(source_dir, f"{domain}.md")
        project_path = os.path.join(project.domains_dir, f"{domain}.md")
        has_seed = os.path.exists(seed_path)
        has_project = os.path.exists(project_path)
        if not has_seed and not has_project:
            continue
        frontmatter = ""
        for candidate_path in (project_path if has_project else None, seed_path if has_seed else None):
            if candidate_path:
                m = FRONTMATTER_RE.match(open(candidate_path).read())
                if m:
                    frontmatter = m.group(0)
                    break
        last_retrospective = "none"
        for candidate_path in (project_path if has_project else None, seed_path if has_seed else None):
            if candidate_path:
                m = re.search(r"^last-retrospective:\s*(\S+)", open(candidate_path).read(), re.MULTILINE)
                if m:
                    last_retrospective = m.group(1)
                    break
        newly_migrated_ids = []
        merged = {}
        for section in ("conventions", "principles"):
            entries = parse_domain_section_full(project_path, section) if has_project else {}
            if has_seed:
                for entry_id, fields in parse_domain_section_full(seed_path, section).items():
                    if entry_id not in entries:
                        entries[entry_id] = fields
                        newly_migrated_ids.append(entry_id)
            merged[section] = entries
        if not merged["conventions"] and not merged["principles"]:
            continue
        open(project_path, "w").write(render_migrated_domain(
            domain, frontmatter, last_retrospective, merged["conventions"], merged["principles"]))
        if newly_migrated_ids:
            append_migration_provenance(project.audit_path, domain, newly_migrated_ids)
            migrated.append(f"{domain}: +{len(newly_migrated_ids)} entries from seed")
    if migrated:
        print("migrated:")
        for line in migrated:
            print(f"  - {line}")
    else:
        print("nothing to migrate — every matching domain already fully materialized")
    print("Next: run `corpus.py measure` then `corpus.py verify` to register the new baseline "
          "(processes/domain-repo-migration.md, step 4).")


# ── chunk chaining: ground-truth ledger for a workstream's units of work ────────────────────
#
# kernel.md, "Chunk chaining": this ledger records what already happened — it never replaces the
# per-unit-of-work spawn+handoff rule (kernel.md, "The handoff artifact"). `chunk-done` requires a
# real handoff to exist for the unit-of-work it closes, the same way `record-gate` requires a real
# gate to have run; `domains-composed` comes from the same `select` call that composed the spawn,
# never self-reported.

def chunks_path(project: "Project", workstream: str) -> str:
    return os.path.join(project.chunks_dir, f"{workstream}.md")


def parse_chunks(path: str) -> tuple:
    """Deliberately flat parser, same style as `parse_deferred`. Returns (workstream, entries)."""
    workstream = ""
    entries = []
    item = None
    in_chunks = False
    for raw in open(path):
        line = raw.rstrip()
        stripped = line.strip()
        if in_chunks and stripped == "```":
            break
        if not in_chunks and stripped.startswith("workstream:"):
            workstream = stripped.split(":", 1)[1].strip()
            continue
        if stripped in ("chunks:", "chunks: []"):
            in_chunks = True
            continue
        if not in_chunks or not stripped or stripped.startswith(("#", "```")):
            continue
        if re.match(r"^\s*-\s+unit-of-work:\s*", line):
            item = {}
            entries.append(item)
            stripped = re.sub(r"^-\s+", "", stripped)
        if item is not None and ":" in stripped:
            key, _, value = stripped.partition(":")
            item[key.strip()] = value.strip()
    for item in entries:
        if "domains-composed" in item:
            item["domains-composed"] = _parse_inline_list(item["domains-composed"])
    return workstream, entries


def render_chunks(workstream: str, entries: list) -> str:
    lines = ["# Chunks", "", f"workstream: {workstream}", "", "```yaml", "chunks:", ""]
    for e in entries:
        lines.append(f"  - unit-of-work: {e['unit-of-work']}")
        lines.append(f"    domains-composed: [{', '.join(e['domains-composed'])}]")
        lines.append(f"    stance: {e['stance']}")
        lines.append(f"    handoff: {e['handoff']}")
        lines.append(f"    completed: {e['completed']}")
        if e.get("next"):
            lines.append(f"    next: {e['next']}")
        lines.append("")
    lines.append("```")
    return "\n".join(lines) + "\n"


def handoff_field(path: str, name: str) -> str:
    text = open(path).read()
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return ""
    fm = re.search(rf"^{name}:[ \t]*(.*)$", m.group(1), re.MULTILINE)
    return fm.group(1).strip() if fm else ""


def cmd_chunk_start(project: "Project", args) -> None:
    """Informational: runs the same deterministic `select` a `chunk-done` call will use, so the
    composition is known before the spawn starts. Writes nothing — the ledger is append-only and
    is only ever written once a real handoff exists to point at."""
    shape = parse_config_shape(project.config_path)
    sources = project.domain_files()
    selected = select_domains(sources, shape, args.unit_of_work)
    print(f"workstream={args.workstream} unit-of-work={args.unit_of_work} "
          f"domains-composed=[{', '.join(selected)}]")


def cmd_chunk_done(project: "Project", args) -> None:
    if not os.path.exists(args.handoff):
        fail(f"no such handoff file: {args.handoff}")
    handoff_workstream = handoff_field(args.handoff, "workstream")
    if handoff_workstream and handoff_workstream != args.workstream:
        fail(f"handoff's workstream '{handoff_workstream}' does not match --workstream '{args.workstream}' — "
             "a chunk can only be closed by the handoff it actually produced")
    shape = parse_config_shape(project.config_path)
    sources = project.domain_files()
    domains_composed = select_domains(sources, shape, args.unit_of_work)
    # Ground-truth check, not self-report: domains-composed comes from select(), never from the
    # handoff — but that only proves select() is self-consistent unless it's also reconciled
    # against what the spawn's own handoff says it actually loaded. A mismatch means either the
    # composing process (e.g. a phase file's own hard-coded domain list) diverged from select()'s
    # frontmatter-driven answer, or the spawn didn't load what its composition specified — either
    # way, closing the chunk over it would record a false "reconciled" claim (see LINEAGE.md-worthy
    # finding from running this exercise literally: verify-chunks reported clean while the ledger
    # and the handoff disagreed about what actually loaded).
    domains_loaded_raw = handoff_field(args.handoff, "domains-loaded")
    if domains_loaded_raw:
        domains_loaded = sorted(_parse_inline_list(domains_loaded_raw))
        expected = sorted(domains_composed)
        if domains_loaded != expected:
            only_composed = sorted(set(expected) - set(domains_loaded))
            only_loaded = sorted(set(domains_loaded) - set(expected))
            fail(
                "handoff's domains-loaded does not match select()'s domains-composed for "
                f"unit-of-work '{args.unit_of_work}' — refusing to close the chunk.\n"
                f"  select() only: {only_composed or '(none)'}\n"
                f"  handoff only: {only_loaded or '(none)'}\n"
                "Either the composing process diverged from select() (fix the composition to use "
                "select(), per processes/general-operation.md's spawn-brief step), or the spawn didn't load "
                "what its composition specified (fix the spawn). Do not paper over this by editing "
                "the ledger by hand."
            )
    path = chunks_path(project, args.workstream)
    if os.path.exists(path):
        _, entries = parse_chunks(path)
    else:
        entries = []
    entries.append({
        "unit-of-work": args.unit_of_work,
        "domains-composed": domains_composed,
        "stance": args.stance,
        "handoff": args.handoff,
        "completed": today(),
        "next": args.next,
    })
    os.makedirs(project.chunks_dir, exist_ok=True)
    open(path, "w").write(render_chunks(args.workstream, entries))
    print(f"chunk closed: {args.workstream}/{args.unit_of_work} -> {path}")


def chunk_lint_problems(path: str) -> list:
    problems = []
    workstream, entries = parse_chunks(path)
    if not workstream:
        problems.append(f"{path}: missing top-level workstream:")
    for i, e in enumerate(entries, 1):
        label = f"{path} chunk {i}"
        for field in ("unit-of-work", "stance", "handoff", "completed"):
            if not e.get(field):
                problems.append(f"{label}: missing {field}")
        if e.get("stance") not in DEFERRED_STANCE_ENUM:
            problems.append(f"{label}: stance must be one of {sorted(DEFERRED_STANCE_ENUM)}")
        if not e.get("domains-composed"):
            problems.append(f"{label}: domains-composed is empty")
    return problems


def cmd_lint_chunks(project: "Project", _args) -> None:
    if not os.path.isdir(project.chunks_dir):
        print("no corpora/chunks/ directory — nothing to lint")
        return
    problems = []
    for name in sorted(os.listdir(project.chunks_dir)):
        if name.endswith(".md"):
            problems += chunk_lint_problems(os.path.join(project.chunks_dir, name))
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        sys.exit(2)
    print("lint-chunks: ok")


def cmd_close_workstream(project: "Project", args) -> None:
    """Read-only summary once every chunk in a workstream is done — aggregates the ledger for the
    retrospective. Never folds multiple chunks' handoffs into one; each chunk's own handoff already
    went through the normal ratify gate."""
    path = chunks_path(project, args.workstream)
    if not os.path.exists(path):
        fail(f"no chunk ledger for workstream '{args.workstream}' at {path}")
    workstream, entries = parse_chunks(path)
    print(f"workstream: {workstream}")
    print(f"chunks: {len(entries)}")
    for e in entries:
        print(f"  - {e['unit-of-work']} ({e['stance']}, completed {e['completed']}): "
              f"{', '.join(e['domains-composed'])}")


def cmd_verify_chunks(project: "Project", _args) -> None:
    """Best-effort `Stop`-hook check (`scripts/stop-check.sh`): recompute `select` for every
    recorded chunk and compare against its stored `domains-composed`. This cannot see whether a
    spawn actually re-read its composed domains before writing (kernel.md, 'The handoff artifact'
    — that is an instruction, not something Stop-hook input exposes); it catches the narrower,
    mechanically-checkable case of composition drift — config.md or a domain's frontmatter changed
    after the chunk closed, or the ledger was hand-edited."""
    if not os.path.isdir(project.chunks_dir):
        print("no corpora/chunks/ directory — nothing to verify")
        return
    shape = parse_config_shape(project.config_path)
    sources = project.domain_files()
    problems = []
    for name in sorted(os.listdir(project.chunks_dir)):
        if not name.endswith(".md"):
            continue
        workstream, entries = parse_chunks(os.path.join(project.chunks_dir, name))
        for e in entries:
            expected = select_domains(sources, shape, e["unit-of-work"])
            recorded = sorted(e.get("domains-composed", []))
            if expected != recorded:
                problems.append(f"{workstream}/{e['unit-of-work']}: recorded domains-composed "
                                 f"{recorded} no longer matches current select() result {expected}")
    if problems:
        print("CHUNK COMPOSITION DRIFT:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("chunk composition reconciled: every recorded domains-composed matches current select()")


# ── queue: mechanical status transitions for corpora/queue.md ────────────────────────────────
# Same reasoning as the chunk ledger (kernel.md, "bookkeeping done by attention is bookkeeping
# that silently stops"): `planning.md`'s queue schema states the orchestrator updates `status` on
# tasks and `resolved`/`answer` on questions "in-place," but nothing scripted ever did that
# in-place update — it was hand-edited, the same failure class the chunk ledger was built to
# close for domains-composed. This closes it for corpora/queue.md.

TASK_STATUS_ENUM = {"pending", "in-progress", "complete", "blocked"}
QUEUE_LIST_FIELDS = {"blocked-by", "blocks"}
QUEUE_TASK_FIELDS = ("id", "title", "description", "context", "status", "blocked-by",
                     "parallel-ok", "concern", "judgment", "notes")
QUEUE_QUESTION_FIELDS = ("id", "question", "blocks", "resolved", "answer")
QUEUE_HEADER_FIELDS = ("capability", "area", "status", "created", "updated")


def parse_queue(path: str) -> tuple:
    """Deliberately flat parser, same style as parse_deferred/parse_chunks. Returns
    (header, tasks, questions) — header is the top-level scalar fields; tasks/questions are lists
    of dicts, with blocked-by/blocks parsed into real lists via _parse_inline_list."""
    header = {}
    tasks = []
    questions = []
    section = None
    item = None
    for raw in open(path):
        line = raw.rstrip()
        stripped = line.strip()
        if stripped == "```":
            if section is not None:
                break
            continue
        if stripped in ("tasks:", "tasks: []"):
            section, item = "tasks", None
            continue
        if stripped in ("open-questions:", "open-questions: []"):
            section, item = "open-questions", None
            continue
        if not stripped or stripped.startswith(("#", "```yaml")):
            continue
        if section is None:
            if ":" in stripped:
                key, _, value = stripped.partition(":")
                header[key.strip()] = value.strip()
            continue
        if re.match(r"^\s*-\s+id:\s*", line):
            item = {}
            (tasks if section == "tasks" else questions).append(item)
            stripped = re.sub(r"^-\s+", "", stripped)
        if item is not None and ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            item[key] = _parse_inline_list(value) if key in QUEUE_LIST_FIELDS else value
    return header, tasks, questions


def render_queue(header: dict, tasks: list, questions: list) -> str:
    lines = ["```yaml"]
    for key in QUEUE_HEADER_FIELDS:
        lines.append(f"{key}: {header.get(key, '')}")
    lines += ["", "tasks:"]
    for t in tasks:
        lines.append(f"  - id: {t.get('id', '')}")
        for key in QUEUE_TASK_FIELDS[1:]:
            value = t.get(key, "")
            if key in QUEUE_LIST_FIELDS:
                value = f"[{', '.join(value)}]" if isinstance(value, list) else (value or "[]")
            lines.append(f"    {key}: {value}")
        lines.append("")
    lines.append("open-questions:")
    for q in questions:
        lines.append(f"  - id: {q.get('id', '')}")
        for key in QUEUE_QUESTION_FIELDS[1:]:
            value = q.get(key, "")
            if key in QUEUE_LIST_FIELDS:
                value = f"[{', '.join(value)}]" if isinstance(value, list) else (value or "[]")
            lines.append(f"    {key}: {value}")
        lines.append("")
    lines.append("```")
    return "\n".join(lines) + "\n"


def queue_lint_problems(path: str) -> list:
    problems = []
    header, tasks, questions = parse_queue(path)
    for field in ("capability", "area", "status"):
        if not header.get(field):
            problems.append(f"{path}: missing header field {field}")
    task_ids = set()
    for t in tasks:
        label = f"{path} task {t.get('id') or '(no id)'}"
        if not t.get("id"):
            problems.append(f"{label}: missing id")
        elif t["id"] in task_ids:
            problems.append(f"{label}: duplicate task id")
        task_ids.add(t.get("id"))
        if t.get("status") not in TASK_STATUS_ENUM:
            problems.append(f"{label}: status must be one of {sorted(TASK_STATUS_ENUM)}")
        for dep in t.get("blocked-by", []):
            if dep and dep not in {t2.get("id") for t2 in tasks}:
                problems.append(f"{label}: blocked-by references unknown task id '{dep}'")
    question_ids = set()
    for q in questions:
        label = f"{path} question {q.get('id') or '(no id)'}"
        if not q.get("id"):
            problems.append(f"{label}: missing id")
        elif q["id"] in question_ids:
            problems.append(f"{label}: duplicate question id")
        question_ids.add(q.get("id"))
        if q.get("resolved") not in ("true", "false"):
            problems.append(f"{label}: resolved must be true or false")
        for blocked in q.get("blocks", []):
            if blocked and blocked not in task_ids:
                problems.append(f"{label}: blocks references unknown task id '{blocked}'")
    return problems


def cmd_lint_queue(project: "Project", _args) -> None:
    if not os.path.exists(project.queue_path):
        print("no corpora/queue.md — nothing to lint")
        return
    problems = queue_lint_problems(project.queue_path)
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        sys.exit(2)
    print("lint-queue: ok")


def _task_startable(task: dict, tasks_by_id: dict, questions_by_id: dict) -> tuple:
    """Returns (startable, blockers) — blockers names every unresolved question and
    incomplete task still standing between this task and being routable."""
    blockers = []
    for dep_id in task.get("blocked-by", []):
        dep = tasks_by_id.get(dep_id)
        if dep and dep.get("status") != "complete":
            blockers.append(f"task {dep_id} ({dep.get('status')})")
    for q in questions_by_id.values():
        if task.get("id") in q.get("blocks", []) and q.get("resolved") != "true":
            blockers.append(f"question {q.get('id')} (unresolved)")
    return (not blockers, blockers)


def cmd_queue_status(project: "Project", _args) -> None:
    if not os.path.exists(project.queue_path):
        print("no corpora/queue.md")
        return
    header, tasks, questions = parse_queue(project.queue_path)
    tasks_by_id = {t.get("id"): t for t in tasks}
    questions_by_id = {q.get("id"): q for q in questions}
    print(f"capability: {header.get('capability', '')}")
    print(f"status: {header.get('status', '')}")
    for t in tasks:
        startable, blockers = _task_startable(t, tasks_by_id, questions_by_id)
        note = "" if t.get("status") == "complete" else (
            " — startable now" if startable else f" — blocked by: {', '.join(blockers)}")
        print(f"  {t.get('id')}: {t.get('status')}{note}")
    for q in questions:
        if q.get("resolved") != "true":
            print(f"  {q.get('id')}: unresolved — blocks {', '.join(q.get('blocks', [])) or '(nothing)'}")


def _save_queue(project: "Project", header: dict, tasks: list, questions: list) -> None:
    header["updated"] = today()
    if tasks and questions is not None:
        all_tasks_complete = all(t.get("status") == "complete" for t in tasks)
        all_questions_resolved = all(q.get("resolved") == "true" for q in questions)
        if all_tasks_complete and all_questions_resolved:
            header["status"] = "complete"
    text = open(project.queue_path).read()
    block = render_queue(header, tasks, questions)
    if "```yaml" in text and "```" in text:
        before = text.split("```yaml", 1)[0]
        after = text.split("```yaml", 1)[1].split("```", 1)[1] if "```" in text.split("```yaml", 1)[1] else ""
        open(project.queue_path, "w").write(before + block + after)
    else:
        open(project.queue_path, "w").write(block)


def cmd_queue_set_status(project: "Project", args) -> None:
    if not os.path.exists(project.queue_path):
        fail(f"no queue at {project.queue_path}")
    if args.status not in TASK_STATUS_ENUM:
        fail(f"status must be one of {sorted(TASK_STATUS_ENUM)}")
    header, tasks, questions = parse_queue(project.queue_path)
    task = next((t for t in tasks if t.get("id") == args.id), None)
    if task is None:
        fail(f"unknown task id '{args.id}' — have: {', '.join(t.get('id', '') for t in tasks) or 'none'}")
    task["status"] = args.status
    _save_queue(project, header, tasks, questions)
    tasks_by_id = {t.get("id"): t for t in tasks}
    unblocked = [t.get("id") for t in tasks
                 if t.get("id") != args.id and t.get("status") == "pending"
                 and args.id in t.get("blocked-by", [])
                 and _task_startable(t, tasks_by_id, {q.get("id"): q for q in questions})[0]]
    print(f"{args.id}: status -> {args.status}")
    if unblocked:
        print(f"now startable: {', '.join(unblocked)}")


def cmd_queue_resolve_question(project: "Project", args) -> None:
    if not os.path.exists(project.queue_path):
        fail(f"no queue at {project.queue_path}")
    header, tasks, questions = parse_queue(project.queue_path)
    question = next((q for q in questions if q.get("id") == args.id), None)
    if question is None:
        fail(f"unknown question id '{args.id}' — have: {', '.join(q.get('id', '') for q in questions) or 'none'}")
    question["resolved"] = "true"
    question["answer"] = args.answer
    _save_queue(project, header, tasks, questions)
    tasks_by_id = {t.get("id"): t for t in tasks}
    unblocked = [t.get("id") for t in tasks
                 if t.get("id") in question.get("blocks", []) and t.get("status") == "pending"
                 and _task_startable(t, tasks_by_id, {q.get("id"): q for q in questions})[0]]
    print(f"{args.id}: resolved")
    if unblocked:
        print(f"now startable: {', '.join(unblocked)}")


# ── compose-spawn-prompt: mechanical, no-summarization spawn-prompt assembly ─────────────────
#
# Fix for the exercise's most serious finding: hand-assembled spawn prompts drifted toward
# summarizing or truncating inlined domain content as a session went on. This command removes the
# judgment call by concatenating full working files byte-for-byte — nothing here decides what's
# relevant, so there is nowhere for compression to sneak in.

def extract_section(text: str, heading_pattern: str, source: str) -> str:
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if re.match(heading_pattern, line):
            start = i
            break
    if start is None:
        fail(f"could not find a section matching {heading_pattern!r} in {source}")
    end = len(lines)
    in_fence = False
    for i in range(start + 1, len(lines)):
        if lines[i].strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            # A bare "---" (e.g. a YAML document separator) inside a fenced
            # code block is section content, not a boundary marker — only a
            # heading or "---" outside any fence ends the section.
            continue
        if re.match(r"^#{1,6}\s", lines[i]) or lines[i].strip() == "---":
            end = i
            break
    return "\n".join(lines[start:end]).rstrip("\n")


def cmd_compose_spawn_prompt(project: Project, args) -> None:
    domains = _ids(args.domains)
    if not domains:
        fail("--domains requires at least one comma-separated domain name")
    if not os.path.exists(args.task_file):
        fail(f"no such file: {args.task_file}")

    sources = project.domain_files()
    named = [(d, parse_domain_frontmatter(sources[d]) if d in sources else None) for d in domains]
    composition_problems = check_composition_problems(named)
    if composition_problems:
        for p in composition_problems:
            print(f"error: {p}", file=sys.stderr)
        fail("composition check failed — a spawn never mixes domains from different subject "
             "families or composes a posture: generative domain (kernel.md, 'The hard line')")

    kernel_path = os.path.join(skill_root(), "kernel.md")
    kernel_text = open(kernel_path).read()
    stance_frame = extract_section(kernel_text, r"^### Generative stance\s*$", "kernel.md")
    handoff_schema = extract_section(kernel_text, r"^## The handoff artifact\s*$", "kernel.md")

    parts = [f"stance: {args.stance}", "", stance_frame, "", "## Domains"]
    for domain in domains:
        if domain not in sources:
            fail(f"domain '{domain}' not found in {project.domains_dir} — nothing to compose")
        parts.append(f"\n### Domain: {domain}\n")
        parts.append(open(sources[domain]).read().rstrip("\n"))
    parts.append("\n" + handoff_schema)
    parts.append("\n## Task\n")
    parts.append(open(args.task_file).read().rstrip("\n"))
    prompt = "\n".join(parts).strip() + "\n"

    if args.output:
        out_path = args.output
    elif project_debug(project):
        slug = args.composition or "-".join(domains)
        out_path = os.path.join(project.root, "corpora", "session-prompts", f"{today()}-{slug}.md")
    else:
        out_path = ""

    print(prompt)
    if out_path:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        open(out_path, "w").write(prompt)
        print(f"--- wrote {out_path} ---", file=sys.stderr)
    else:
        print("--- debug not enabled (corpora/config.md) — session prompt not saved to disk; "
              "pass --output to save explicitly ---", file=sys.stderr)


# ── kill-log graduation: age out killed entries with a recorded, stale kill date ─────────────
#
# Works on any domains-dir + its audit.md pair — project layer (<root>/corpora/domains) or the
# kernel-seed layer (domains/) — not only project layers, since retrospective consolidation
# happens in the skill repo's own seed corpus too.

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
    reads just enough structure for kill-age accounting, not a general YAML parser. The
    `provenance:` list runs to end of file — there is no `promoted:` section to bound it against
    (retired per v3-redesign-proposal.md; formerly-promoted principles now live as preamble prose
    in their domain's working file instead of a separate audit-file tier).
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
    layer_help = "override to work on any domains-dir + audit.md pair — a project's own " \
                 "corpora/domains or the kernel-seed domains/ — not only a project's own corpora"
    m = sub.add_parser("measure")
    m.add_argument("--domains-dir", default="", help=layer_help)
    m.add_argument("--audit", default="", help=layer_help)
    v = sub.add_parser("verify")
    v.add_argument("--domains-dir", default="", help=layer_help)
    v.add_argument("--audit", default="", help=layer_help)
    g = sub.add_parser("record-gate")
    g.add_argument("--domains-dir", default="", help=layer_help)
    g.add_argument("--audit", default="", help=layer_help)
    g.add_argument("--domain", required=True)
    g.add_argument("--ratified", type=int, default=0)
    g.add_argument("--killed", type=int, default=0)
    g.add_argument("--graduated", type=int, default=0,
                   help="principles moved from principles: to conventions: this gate")
    g.add_argument("--violations", type=int, default=0)
    g.add_argument("--ui-drift", action="store_true")
    g.add_argument("--fired", default="", help="comma-separated principle ids")
    g.add_argument("--violated", default="", help="comma-separated principle ids")
    g.add_argument("--idle", default="", help="comma-separated principle ids")
    g.add_argument("--origin", choices=sorted(ORIGIN_ENUM), default="project",
                   help="seed | project — stronger than directory-inference alone")
    g.add_argument("--co-occurs-with", default="",
                   help="comma-separated domain names loaded alongside --domain in the same spawn")
    sub.add_parser("triggers")
    lh = sub.add_parser("lint-handoff")
    lh.add_argument("file")
    sub.add_parser("handoffs")
    hd = sub.add_parser("handoff-done",
                         help="close a ratified handoff: delete it, or archive it under "
                              "corpora/handoffs/archive/ when corpora/config.md sets debug: yes")
    hd.add_argument("file")
    sub.add_parser("lint-deferred")
    sub.add_parser("deferred")
    sub.add_parser("lint-deterministic-shortcut-candidates")
    sub.add_parser("deterministic-shortcut-candidates")
    uc = sub.add_parser("record-deterministic-shortcut-candidate")
    uc.add_argument("--id", required=True)
    uc.add_argument("--operation-shape", required=True)
    uc.add_argument("--workstream", required=True)
    uc.add_argument("--burden", required=True)
    uc.add_argument("--date", default="", help="YYYY-MM-DD; defaults to today")
    us = sub.add_parser("set-deterministic-shortcut-status")
    us.add_argument("--id", required=True)
    us.add_argument("--status", required=True, choices=sorted(SHORTCUT_STATUS_ENUM))
    us.add_argument("--reason", default="")
    r = sub.add_parser("retro-done")
    r.add_argument("--domain", required=True)
    r.add_argument("--domains-dir", default="", help=layer_help)
    r.add_argument("--audit", default="", help=layer_help)
    sd = sub.add_parser("sync-done")
    sd.add_argument("--domains-dir", default="", help=layer_help)
    sd.add_argument("--audit", default="", help=layer_help)
    cp = sub.add_parser("compose-spawn-prompt",
                        help="mechanically concatenate a composition's full domain files, the "
                             "stance frame, and the handoff schema into one spawn-ready prompt file")
    cp.add_argument("--stance", required=True, choices=sorted(DEFERRED_STANCE_ENUM))
    cp.add_argument("--domains", required=True, help="comma-separated domain names")
    cp.add_argument("--task-file", required=True, help="path to a file containing the task description")
    cp.add_argument("--composition", default="", help="descriptive label, for the output filename only")
    cp.add_argument("--output", default="", help="output path; defaults under corpora/session-prompts/")
    cp.add_argument("--domains-dir", default="", help=layer_help)
    sr = sub.add_parser("screenshot-record")
    sr.add_argument("--screen", required=True)
    sr.add_argument("--variant", required=True)
    sr.add_argument("--path", required=True)
    sr.add_argument("--components", default="", help="comma-separated component names")
    sm = sub.add_parser("screenshot-mark-stale")
    sm.add_argument("--screens", default="", help="comma-separated screen ids touched directly")
    sm.add_argument("--components", default="", help="comma-separated shared components changed")
    sub.add_parser("screenshot-status")
    sl = sub.add_parser("screenshot-lookup")
    sl.add_argument("--component", required=True)
    sub.add_parser("lint-screenshots")
    kr = sub.add_parser("kill-report", help="works on any domains-dir + audit.md pair, not only a project's corpora/domains")
    kr.add_argument("--domains-dir", required=True)
    kr.add_argument("--audit", required=True)
    kr.add_argument("--min-age-days", type=int, default=KILL_GRADUATION_DAYS)
    gk = sub.add_parser("graduate-kill", help="works on any domains-dir + audit.md pair, not only a project's corpora/domains")
    gk.add_argument("--domains-dir", required=True)
    gk.add_argument("--audit", required=True)
    gk.add_argument("--domain", required=True)
    gk.add_argument("--id", required=True)
    ld = sub.add_parser("lint-domains", help="works on any domains-dir, not only a project's corpora/domains — "
                                              "validates frontmatter (subject/posture/applies-when/units-of-work)")
    ld.add_argument("--domains-dir", required=True)
    mf = sub.add_parser("manifest", help="emit the machine-readable domain index for this project's own "
                                          "corpora/domains/ (or --domains-dir), for a process layer to "
                                          "select against without reading prose")
    mf.add_argument("--json", action="store_true")
    mf.add_argument("--domains-dir", default="", help=layer_help)
    sel = sub.add_parser("select", help="deterministic domain selection for a unit-of-work, evaluated "
                                         "against corpora/config.md — no model in the loop")
    sel.add_argument("--unit-of-work", required=True)
    sel.add_argument("--config", default="", help="defaults to corpora/config.md under --root")
    sel.add_argument("--json", action="store_true")
    sel.add_argument("--domains-dir", default="", help=layer_help)
    cc = sub.add_parser("check-composition", help="fail if a domain list mixes subjects or includes "
                                                    "a posture: generative domain (kernel.md, 'The hard line')")
    cc.add_argument("--domains", required=True, help="comma-separated domain names")
    cc.add_argument("--domains-dir", default="", help=layer_help)
    il = sub.add_parser("import-list", help="browse a source domains-dir's principles+conventions, "
                                              "flagging which ids already exist in the target — "
                                              "read-only, proposes nothing")
    il.add_argument("--source", required=True, help="path to the source domains-dir")
    il.add_argument("--target-domains-dir", default="", help="defaults to this project's own corpora/domains")
    ic = sub.add_parser("import-candidate", help="propose one principle or convention from a source "
                                                   "domains-dir as a candidate, with imported-from provenance")
    ic.add_argument("--source", required=True, help="path to the source domains-dir")
    ic.add_argument("--domain", required=True, help="the entry's domain in the source")
    ic.add_argument("--id", required=True, help="the entry's id in the source")
    ic.add_argument("--as-domain", default="", help="propose into a different destination domain")
    ic.add_argument("--as-id", default="", help="propose under a different id (e.g. on collision)")
    ic.add_argument("--target-domains-dir", default="", help="defaults to this project's own corpora/domains")
    ic.add_argument("--output", default="", help="candidates file; defaults to corpora/import-candidates.md")
    idp = sub.add_parser("import-default-pool", help="propose every principle+convention from every "
                                                       "domain in the source whose applies-when already "
                                                       "matches this project's shape — the bootstrap fast path")
    idp.add_argument("--source", default="", help="defaults to this skill's own domains/")
    idp.add_argument("--config", default="", help="defaults to corpora/config.md under --root")
    idp.add_argument("--target-domains-dir", default="", help="defaults to this project's own corpora/domains")
    idp.add_argument("--output", default="", help="candidates file; defaults to corpora/import-candidates.md")
    md = sub.add_parser("migrate-domains", help="one-time: materialize a pre-dissolution project's "
                                                  "live seed/project merge into its own corpora/domains/ "
                                                  "(processes/domain-repo-migration.md)")
    md.add_argument("--source", default="", help="defaults to this skill's own domains/")
    md.add_argument("--config", default="", help="defaults to corpora/config.md under --root")
    md.add_argument("--domains", default="", help="comma-separated domain names; defaults to the "
                                                    "default-pool match plus every domain the project already has")
    cs = sub.add_parser("chunk-start", help="print the deterministic composition for a unit-of-work; writes nothing")
    cs.add_argument("--workstream", required=True)
    cs.add_argument("--unit-of-work", required=True)
    cs.add_argument("--domains-dir", default="", help=layer_help)
    cd = sub.add_parser("chunk-done", help="close a chunk in corpora/chunks/<workstream>.md — requires "
                                            "the handoff that unit-of-work actually produced")
    cd.add_argument("--workstream", required=True)
    cd.add_argument("--unit-of-work", required=True)
    cd.add_argument("--stance", required=True, choices=sorted(DEFERRED_STANCE_ENUM))
    cd.add_argument("--handoff", required=True)
    cd.add_argument("--next", default="")
    cd.add_argument("--domains-dir", default="", help=layer_help)
    sub.add_parser("lint-chunks")
    clw = sub.add_parser("close-workstream", help="read-only summary of a workstream's completed chunks")
    clw.add_argument("--workstream", required=True)
    sub.add_parser("verify-chunks", help="Stop-hook check: recompute select() for every recorded "
                                          "chunk and compare against its stored domains-composed")
    sub.add_parser("lint-queue", help="validate corpora/queue.md structurally")
    sub.add_parser("queue-status", help="read-only: each task's status and startability, each "
                                         "question's resolution state")
    qss = sub.add_parser("queue-set-status", help="set a task's status in-place — the mechanical "
                                                   "half of planning.md's 'orchestrator updates "
                                                   "status in-place' rule")
    qss.add_argument("--id", required=True)
    qss.add_argument("--status", required=True, choices=sorted(TASK_STATUS_ENUM))
    qrq = sub.add_parser("queue-resolve-question", help="resolve an open question in-place")
    qrq.add_argument("--id", required=True)
    qrq.add_argument("--answer", required=True)
    args = ap.parse_args()

    no_project = {"kill-report": cmd_kill_report, "graduate-kill": cmd_graduate_kill,
                  "lint-domains": cmd_lint_domains}
    if args.cmd in no_project:
        no_project[args.cmd](args)
        return

    project = Project(os.path.abspath(args.root),
                      domains_dir=getattr(args, "domains_dir", "") or "",
                      audit_path=getattr(args, "audit", "") or "")
    {"measure": cmd_measure, "verify": cmd_verify, "record-gate": cmd_record_gate, "triggers": cmd_triggers,
     "lint-handoff": cmd_lint_handoff, "handoffs": cmd_handoffs, "handoff-done": cmd_handoff_done,
     "lint-deferred": cmd_lint_deferred, "deferred": cmd_deferred,
     "lint-deterministic-shortcut-candidates": cmd_lint_deterministic_shortcut_candidates,
     "deterministic-shortcut-candidates": cmd_deterministic_shortcut_candidates,
     "record-deterministic-shortcut-candidate": cmd_record_deterministic_shortcut_candidate,
     "set-deterministic-shortcut-status": cmd_set_deterministic_shortcut_status,
     "retro-done": cmd_retro_done, "sync-done": cmd_sync_done,
     "compose-spawn-prompt": cmd_compose_spawn_prompt,
     "screenshot-record": cmd_screenshot_record,
     "screenshot-mark-stale": cmd_screenshot_mark_stale,
     "screenshot-status": cmd_screenshot_status,
     "screenshot-lookup": cmd_screenshot_lookup,
     "lint-screenshots": cmd_lint_screenshots,
     "manifest": cmd_manifest, "select": cmd_select,
     "check-composition": cmd_check_composition,
     "import-list": cmd_import_list, "import-candidate": cmd_import_candidate,
     "import-default-pool": cmd_import_default_pool, "migrate-domains": cmd_migrate_domains,
     "chunk-start": cmd_chunk_start, "chunk-done": cmd_chunk_done,
     "lint-chunks": cmd_lint_chunks, "close-workstream": cmd_close_workstream,
     "verify-chunks": cmd_verify_chunks,
     "lint-queue": cmd_lint_queue, "queue-status": cmd_queue_status,
     "queue-set-status": cmd_queue_set_status,
     "queue-resolve-question": cmd_queue_resolve_question}[args.cmd](project, args)


if __name__ == "__main__":
    main()
