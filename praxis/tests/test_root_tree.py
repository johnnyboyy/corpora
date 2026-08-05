"""Tests for root_tree. Run with: python3 -m unittest discover -s praxis/tests -v"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import root_tree as rt  # noqa: E402


def mkroot(base: Path, rel: str, marker: str = "corpora/config.md", name: str | None = None) -> Path:
    """Create a root dir at base/rel with a marker file, optionally carrying a `name:`."""
    d = base / rel
    (d / Path(marker).parent).mkdir(parents=True, exist_ok=True)
    body = "## project-shape\n"
    if name:
        body += f"name: {name}\n"
    (d / marker).write_text(body)
    return d


class RootTreeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_nesting_makes_parent_child(self):
        mkroot(self.tmp, "app")
        mkroot(self.tmp, "app/admin")
        nodes = rt.build_tree(rt.find_roots(self.tmp, rt.DEFAULT_MARKERS), rt.DEFAULT_MARKERS)
        app = nodes[str((self.tmp / "app").resolve())]
        admin = nodes[str((self.tmp / "app/admin").resolve())]
        self.assertIsNone(app["parent"])
        self.assertEqual(admin["parent"], app["path"])
        self.assertIn(admin["path"], app["children"])

    def test_sibling_roots_flag_missing_interop(self):
        mkroot(self.tmp, "apps/circuit-builder")
        mkroot(self.tmp, "apps/marketing")
        nodes = rt.build_tree(rt.find_roots(self.tmp, rt.DEFAULT_MARKERS), rt.DEFAULT_MARKERS)
        groups = rt.orphan_sibling_groups(nodes)
        self.assertEqual(len(groups), 1)
        self.assertEqual(sorted(groups[0]["members"]), ["circuit-builder", "marketing"])

    def test_a_real_parent_root_suppresses_the_flag(self):
        mkroot(self.tmp, ".", name="interop")
        mkroot(self.tmp, "apps/circuit-builder")
        mkroot(self.tmp, "apps/marketing")
        nodes = rt.build_tree(rt.find_roots(self.tmp, rt.DEFAULT_MARKERS), rt.DEFAULT_MARKERS)
        self.assertEqual(rt.orphan_sibling_groups(nodes), [])

    def test_name_from_config_else_basename(self):
        mkroot(self.tmp, "svc", name="billing")
        mkroot(self.tmp, "other")
        self.assertEqual(rt.root_name((self.tmp / "svc"), rt.DEFAULT_MARKERS), "billing")
        self.assertEqual(rt.root_name((self.tmp / "other"), rt.DEFAULT_MARKERS), "other")

    def test_nearest_root_wins(self):
        mkroot(self.tmp, "app")
        mkroot(self.tmp, "app/admin")
        roots = rt.find_roots(self.tmp, rt.DEFAULT_MARKERS)
        self.assertEqual(rt.nearest_root(self.tmp / "app/admin/src/x.ts", roots),
                         (self.tmp / "app/admin").resolve())
        self.assertEqual(rt.nearest_root(self.tmp / "app/src/y.ts", roots),
                         (self.tmp / "app").resolve())

    def test_corpora_and_praxis_markers_both_recognized(self):
        mkroot(self.tmp, "a", marker="corpora/config.md")
        mkroot(self.tmp, "b", marker="praxis/config.md")
        roots = rt.find_roots(self.tmp, rt.DEFAULT_MARKERS)
        engines = {rt.root_name(r, rt.DEFAULT_MARKERS): rt.which_marker(r, rt.DEFAULT_MARKERS)
                   for r in roots}
        self.assertEqual(engines, {"a": "corpora", "b": "praxis"})

    def test_node_modules_pruned(self):
        mkroot(self.tmp, "app")
        mkroot(self.tmp, "app/node_modules/somepkg")
        roots = rt.find_roots(self.tmp, rt.DEFAULT_MARKERS)
        self.assertEqual([r.name for r in roots], ["app"])


if __name__ == "__main__":
    unittest.main()
