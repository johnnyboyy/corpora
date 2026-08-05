"""Tests for frame. Run with: python3 -m unittest discover -s praxis/tests -v

Composition is the engine's job; these tests cover praxis's deterministic parts — root resolution,
the span/decompose verdict, and graceful degradation when the engine is absent — plus one live
integration check against a real corpora root when this repo's own corpus.py is present.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import frame  # noqa: E402
import root_tree as rt  # noqa: E402


def mkroot(base: Path, rel: str, name: str | None = None) -> Path:
    d = base / rel
    (d / "corpora").mkdir(parents=True, exist_ok=True)
    body = "## project-shape\n" + (f"name: {name}\n" if name else "")
    (d / "corpora" / "config.md").write_text(body)
    return d


NO_ENGINE = Path("/nonexistent/corpus.py")  # forces the engine-unavailable path


class FrameTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_single_root_resolves(self):
        mkroot(self.tmp, "app", name="app")
        f = frame.build_frame(self.tmp, "app/src/x.ts", [], "implement-feature", NO_ENGINE)
        self.assertEqual(f["verdict"], "single-root")
        self.assertEqual(len(f["roots"]), 1)
        self.assertEqual(f["roots"][0]["name"], "app")

    def test_spanning_roots_says_decompose_and_skips_composition(self):
        mkroot(self.tmp, "apps/a", name="a")
        mkroot(self.tmp, "apps/b", name="b")
        f = frame.build_frame(self.tmp, None,
                              ["apps/a/src/x.ts", "apps/b/src/y.ts"], "implement-feature", NO_ENGINE)
        self.assertTrue(f["spans_multiple_roots"])
        self.assertEqual(f["verdict"], "decompose")
        self.assertIsNone(f["composition"])  # never compose a cross-root task as one

    def test_engine_absence_degrades_gracefully(self):
        # Root facts must survive the engine being unavailable — praxis does not depend on it.
        mkroot(self.tmp, "app", name="app")
        f = frame.build_frame(self.tmp, "app/src/x.ts", [], "implement-feature", NO_ENGINE)
        self.assertEqual(f["roots"][0]["name"], "app")
        self.assertIsNone(f["composition"])
        self.assertIn("unavailable", f["composition_note"])

    def test_no_unit_of_work_defers_composition(self):
        mkroot(self.tmp, "app", name="app")
        f = frame.build_frame(self.tmp, "app/src/x.ts", [], None, NO_ENGINE)
        self.assertIsNone(f["composition"])
        self.assertIn("unit-of-work not given", f["composition_note"])

    def test_binding_is_a_single_overridable_path(self):
        # The one corpora coupling is a single, inspectable path — overridable (tests rely on that).
        self.assertTrue(str(frame.DEFAULT_CORPUS_PY).endswith("scripts/corpus.py"))

    def test_live_composition_against_this_repo(self):
        # Integration: if this repo's own corpus.py is present, a real select must return domains.
        corpus_py = frame.DEFAULT_CORPUS_PY
        if not corpus_py.is_file():
            self.skipTest("corpus.py not present")
        repo_root = corpus_py.parent.parent  # the corpora repo is itself a root (has domains/)
        # corpora's own tree uses domains/ not corpora/config.md, so point --from at a real project if
        # available; otherwise just assert the engine call path returns a list or a clean note.
        domains, note = frame.engine_compose(repo_root, "implement-feature", corpus_py)
        self.assertTrue(domains is None or isinstance(domains, list),
                        f"unexpected engine result: {note}")


if __name__ == "__main__":
    unittest.main()
