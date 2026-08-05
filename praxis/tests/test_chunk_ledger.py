"""Tests for chunk_ledger — now praxis-NATIVE unit-of-work accounting. Praxis reads/writes the
ledger itself; the only engine touch is `compose` (driven against the stub). Covers: the native
ledger round-trip + corpora-format compatibility, the load-bearing chunk-done-before-handoff-close
ordering gate, the handoff-exists precondition, and both reconciliation failures.
Run: python3 -m unittest discover -s praxis/tests"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import chunk_ledger  # noqa: E402
from _stub_engine import write_stub  # noqa: E402


class LedgerFormatTests(unittest.TestCase):
    """Native round-trip, and byte-compatibility with a hand-written corpora-format ledger."""

    def test_render_then_parse_round_trips(self):
        entries = [{
            "unit-of-work": "implement-feature", "domains-composed": ["coding-general", "security"],
            "stance": "convergent", "handoff": "h.md", "completed": "2026-08-04", "next": "next-uow",
        }]
        text = chunk_ledger.render_chunks("ws-1", entries)
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "ws-1.md"
            p.write_text(text)
            workstream, got = chunk_ledger.parse_chunks(p)
            self.assertEqual(workstream, "ws-1")
            self.assertEqual(got[0]["domains-composed"], ["coding-general", "security"])
            self.assertEqual(got[0]["stance"], "convergent")
            self.assertEqual(got[0]["next"], "next-uow")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_reads_a_handwritten_corpora_format_ledger(self):
        # Exactly the shape corpora's render_chunks emits — proving praxis parses corpora's files.
        sample = (
            "# Chunks\n\nworkstream: legacy\n\n```yaml\nchunks:\n\n"
            "  - unit-of-work: fix-bug\n"
            "    domains-composed: [coding-general, debugging]\n"
            "    stance: convergent\n"
            "    handoff: corpora/handoffs/fix-bug.md\n"
            "    completed: 2026-07-30\n\n"
            "```\n"
        )
        tmp = Path(tempfile.mkdtemp())
        try:
            p = tmp / "legacy.md"
            p.write_text(sample)
            workstream, entries = chunk_ledger.parse_chunks(p)
            self.assertEqual(workstream, "legacy")
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["unit-of-work"], "fix-bug")
            self.assertEqual(entries[0]["domains-composed"], ["coding-general", "debugging"])
            # And praxis re-renders it byte-identically.
            self.assertEqual(chunk_ledger.render_chunks(workstream, entries), sample)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class CloseSequenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "proj"
        self.handoffs = self.root / "corpora" / "handoffs"
        self.handoffs.mkdir(parents=True)
        (self.root / "corpora" / "chunks").mkdir(parents=True)
        self.stub = write_stub(self.tmp)
        self.log = self.tmp / "log.txt"
        os.environ["STUB_LOG"] = str(self.log)
        os.environ.pop("STUB_FAIL", None)
        os.environ.pop("STUB_DOMAINS", None)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        for k in ("STUB_LOG", "STUB_FAIL", "STUB_DOMAINS"):
            os.environ.pop(k, None)

    def _handoff(self, body: str = "workstream: w\n") -> Path:
        h = self.handoffs / "h.md"
        h.write_text(f"---\n{body}---\n")
        return h

    def _ledger(self) -> Path:
        return self.root / "corpora" / "chunks" / "w.md"

    def test_close_writes_ledger_then_removes_handoff(self):
        h = self._handoff()  # no domains-loaded → reconciliation (b) skipped
        rc = chunk_ledger.close(self.stub, str(self.root), "w", "u", "convergent", str(h), None)
        self.assertEqual(rc, 0)
        # chunk-done ran (ledger written) BEFORE handoff-close (handoff removed): both effects present.
        self.assertTrue(self._ledger().is_file())
        _, entries = chunk_ledger.parse_chunks(self._ledger())
        self.assertEqual(entries[0]["unit-of-work"], "u")
        self.assertFalse(h.exists())  # handoff closed (debug off → deleted)

    def test_missing_handoff_is_a_precondition_stop_before_anything(self):
        rc = chunk_ledger.close(self.stub, str(self.root), "w", "u", "convergent",
                                str(self.handoffs / "nope.md"), None)
        self.assertEqual(rc, 1)
        self.assertFalse(self._ledger().exists())  # nothing written

    def test_handoff_survives_when_chunk_done_fails_workstream_mismatch(self):
        h = self._handoff("workstream: other\n")  # (a) mismatch → chunk-done fails
        rc = chunk_ledger.close(self.stub, str(self.root), "w", "u", "convergent", str(h), None)
        self.assertNotEqual(rc, 0)
        self.assertFalse(self._ledger().exists())  # ledger never written
        self.assertTrue(h.exists())                # gate held: handoff NOT closed

    def test_domains_loaded_mismatch_fails_and_leaves_handoff(self):
        os.environ["STUB_DOMAINS"] = "coding-general"       # compose returns [coding-general]
        h = self._handoff("workstream: w\ndomains-loaded: [coding-general, security]\n")
        rc = chunk_ledger.close(self.stub, str(self.root), "w", "u", "convergent", str(h), None)
        self.assertNotEqual(rc, 0)
        self.assertFalse(self._ledger().exists())
        self.assertTrue(h.exists())

    def test_domains_loaded_match_closes_cleanly(self):
        os.environ["STUB_DOMAINS"] = "coding-general,security"
        h = self._handoff("workstream: w\ndomains-loaded: [coding-general, security]\n")
        rc = chunk_ledger.close(self.stub, str(self.root), "w", "u", "convergent", str(h), None)
        self.assertEqual(rc, 0)
        _, entries = chunk_ledger.parse_chunks(self._ledger())
        self.assertEqual(entries[0]["domains-composed"], ["coding-general", "security"])
        self.assertFalse(h.exists())

    def test_chunk_done_records_composed_domains_from_compose(self):
        os.environ["STUB_DOMAINS"] = "a,b,c"
        h = self._handoff()  # no domains-loaded, so compose result is recorded unreconciled
        chunk_ledger.close(self.stub, str(self.root), "w", "u", "divergent", str(h), "nxt")
        _, entries = chunk_ledger.parse_chunks(self._ledger())
        self.assertEqual(entries[0]["domains-composed"], ["a", "b", "c"])
        self.assertEqual(entries[0]["next"], "nxt")


class SummaryTests(unittest.TestCase):
    def test_summary_reads_native_ledger(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            cdir = tmp / "corpora" / "chunks"
            cdir.mkdir(parents=True)
            entries = [{"unit-of-work": "u", "domains-composed": ["d1"], "stance": "convergent",
                        "handoff": "h.md", "completed": "2026-08-04", "next": None}]
            (cdir / "w.md").write_text(chunk_ledger.render_chunks("w", entries))

            class A:
                root = str(tmp)
                workstream = "w"
            self.assertEqual(chunk_ledger.cmd_summary(A()), 0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_summary_missing_ledger_returns_1(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            class A:
                root = str(tmp)
                workstream = "nope"
            self.assertEqual(chunk_ledger.cmd_summary(A()), 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
