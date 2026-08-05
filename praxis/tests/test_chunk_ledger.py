"""Tests for chunk_ledger — the load-bearing close ordering. Run: python3 -m unittest discover -s praxis/tests"""

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
from _stub_engine import write_stub, read_log  # noqa: E402


class ChunkLedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.stub = write_stub(self.tmp)
        self.log = self.tmp / "log.txt"
        os.environ["STUB_LOG"] = str(self.log)
        os.environ.pop("STUB_FAIL", None)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("STUB_LOG", None)
        os.environ.pop("STUB_FAIL", None)

    def _handoff(self) -> Path:
        h = self.tmp / "handoff.md"
        h.write_text("---\nworkstream: w\n---\n")
        return h

    def test_close_runs_chunk_done_then_handoff_done_in_order(self):
        h = self._handoff()
        rc = chunk_ledger.close(self.stub, "w", "u", "convergent", str(h), None)
        self.assertEqual(rc, 0)
        calls = [c[0] for c in read_log(self.log)]
        self.assertEqual(calls, ["chunk-done", "handoff-done"])  # order is load-bearing

    def test_missing_handoff_is_a_precondition_stop_before_engine(self):
        rc = chunk_ledger.close(self.stub, "w", "u", "convergent", str(self.tmp / "nope.md"), None)
        self.assertEqual(rc, 1)
        self.assertEqual(read_log(self.log), [])  # engine never touched

    def test_handoff_done_never_runs_if_chunk_done_fails(self):
        os.environ["STUB_FAIL"] = "chunk-done"
        h = self._handoff()
        rc = chunk_ledger.close(self.stub, "w", "u", "convergent", str(h), None)
        self.assertNotEqual(rc, 0)
        calls = [c[0] for c in read_log(self.log)]
        self.assertEqual(calls, ["chunk-done"])  # the gate held: handoff-done was NOT run

    def test_next_flag_is_passed_through(self):
        h = self._handoff()
        chunk_ledger.close(self.stub, "w", "u", "convergent", str(h), "next-uow")
        chunk_call = read_log(self.log)[0]
        self.assertIn("--next", chunk_call)
        self.assertIn("next-uow", chunk_call)


if __name__ == "__main__":
    unittest.main()
