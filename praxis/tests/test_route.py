"""Tests for route.py — the GO-2 routing fact-sheet. Two layers:

  - the execution-shape signals against the fixture project as REAL subprocesses (frame-derived
    facts: single-root new work vs. a spanning task that must isolate), mirroring test_e2e; and
  - the resume-vs-new ledger signal against the stub engine, where the read-only `close-workstream`
    capability's outcome is what routing reads to tell a resume candidate from new work.

Run: python3 -m unittest discover -s praxis/tests
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PRAXIS = Path(__file__).resolve().parent.parent
ROUTE = PRAXIS / "scripts" / "route.py"
CORPUS_PY = PRAXIS.parent / "scripts" / "corpus.py"

SCRIPTS = PRAXIS / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import route  # noqa: E402
from _stub_engine import write_stub  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, timeout=60)


def mkroot(base: Path, rel: str, name: str, universal_domain: bool = False) -> Path:
    d = base / rel
    dom = d / "corpora" / "domains"
    dom.mkdir(parents=True, exist_ok=True)
    (d / "corpora" / "config.md").write_text(
        f"## project-shape\nname: {name}\nlanguage: typescript\nframework: none\nhas-ui: no\nstyling: none\n")
    if universal_domain:
        (dom / "coding-general.md").write_text(
            "---\nsubject: coding\nposture: guardrail\nunits-of-work: [implement-feature]\nuniversal: true\n---\n"
            "# Domain: coding-general\n\n```yaml\nprinciples:\n- id: p\n  rule: r\n  condition: c\n  reason: y\nkilled:\n```\n")
    return d


class RouteShapeE2E(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        mkroot(self.tmp, ".", "platform")
        mkroot(self.tmp, "app", "app", universal_domain=True)
        mkroot(self.tmp, "admin", "admin")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_single_root_new_work_shape(self):
        r = run(str(ROUTE), "--from", str(self.tmp), "--target", "app/src/x.ts",
                "--unit-of-work", "implement-feature", "--corpus-py", str(CORPUS_PY), "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        es = d["execution_shape"]
        self.assertEqual(es["verdict"], "single-root")
        self.assertFalse(es["isolate_per_root"])       # one root → not isolate
        self.assertFalse(es["resume_candidate"])       # no workstream named → new
        self.assertEqual(es["ledger"], "unknown")
        if CORPUS_PY.is_file():
            self.assertTrue(es["composition_available"])

    def test_spanning_task_routes_to_isolate(self):
        r = run(str(ROUTE), "--from", str(self.tmp), "--files", "app/x.ts,admin/y.ts",
                "--unit-of-work", "implement-feature", "--corpus-py", str(CORPUS_PY), "--json")
        d = json.loads(r.stdout)
        es = d["execution_shape"]
        self.assertEqual(es["verdict"], "decompose")
        self.assertTrue(es["isolate_per_root"])        # spanning → isolate per root
        self.assertTrue(any("isolate" in s for s in d["signals"]))


class RouteLedgerNative(unittest.TestCase):
    """resume-vs-new is now a NATIVE ledger-file lookup — the ledger is a praxis-owned file
    (<root>/corpora/chunks/<workstream>.md), so routing reads it directly, no engine call."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.stub = write_stub(self.tmp)
        os.environ.pop("STUB_LOG", None)
        self.root = mkroot(self.tmp, "proj", "proj", universal_domain=True)
        self.target = "proj/src/x.ts"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("STUB_LOG", None)

    def _route(self, workstream):
        return route.build_route(self.tmp, self.target, [], "implement-feature", workstream, self.stub)

    def _make_ledger(self, workstream):
        cdir = self.root / "corpora" / "chunks"
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / f"{workstream}.md").write_text(
            f"# Chunks\n\nworkstream: {workstream}\n\n```yaml\nchunks:\n```\n")

    def test_named_workstream_with_ledger_is_resume(self):
        self._make_ledger("ws-1")           # native ledger file present → resume candidate
        es = self._route("ws-1")["execution_shape"]
        self.assertEqual(es["ledger"], "exists")
        self.assertTrue(es["resume_candidate"])

    def test_named_workstream_without_ledger_is_new(self):
        es = self._route("ws-1")["execution_shape"]   # no ledger file → new
        self.assertEqual(es["ledger"], "absent")
        self.assertFalse(es["resume_candidate"])

    def test_no_workstream_is_unknown_and_new(self):
        es = self._route(None)["execution_shape"]
        self.assertEqual(es["ledger"], "unknown")
        self.assertFalse(es["resume_candidate"])

    def test_engine_absent_still_reports_native_ledger_and_root_facts(self):
        # The ledger lookup no longer depends on the engine, so it stands even when compose can't run.
        self._make_ledger("ws-1")
        d = route.build_route(self.tmp, self.target, [], "implement-feature", "ws-1",
                              self.tmp / "nonexistent.py")
        es = d["execution_shape"]
        self.assertEqual(es["ledger"], "exists")               # native lookup, engine-independent
        self.assertEqual(d["frame"]["roots"][0]["name"], "proj")  # root fact still stands


if __name__ == "__main__":
    unittest.main()
