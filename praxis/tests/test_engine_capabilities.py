"""Tests for the engine capability resolver — the plugin-declared invocation contract.

The sequence scripts no longer name corpora verbs; they name CAPABILITIES, which resolve to verbs +
argv through the corpora manifest (praxis/engine/plugins/corpora.json). These tests pin the resolver
itself: manifest loads, argv is built in the right shape (globals before the verb, positionals bare,
booleans as a lone flag, required params enforced), and an undeclared capability is praxis's own
error rather than a silent engine call. Run: python3 -m unittest discover -s praxis/tests
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import engine  # noqa: E402
from _stub_engine import write_stub, read_log  # noqa: E402


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.m = engine.load_manifest()

    def test_manifest_is_the_corpora_plugin(self):
        self.assertEqual(self.m["plugin"], "corpora")

    def test_declares_the_capabilities_the_scripts_use(self):
        for cap in ("compose", "principle-add", "import-ratify", "kill-report", "kill-graduate",
                    "domain-import-list", "domain-migrate", "domain-verify", "lint-domains",
                    "gate-record", "triggers"):
            self.assertIn(cap, self.m["capabilities"], cap)

    def test_native_ledger_verbs_are_no_longer_engine_capabilities(self):
        # chunk_ledger + handoff-close went praxis-native; praxis stops invoking them on the engine.
        for cap in ("chunk-start", "chunk-close", "handoff-close", "close-workstream"):
            self.assertNotIn(cap, self.m["capabilities"], cap)


class BuildArgvTests(unittest.TestCase):
    def setUp(self):
        self.m = engine.load_manifest()

    def test_flag_value_pairs_follow_the_verb(self):
        argv = engine.build_argv(self.m, "principle-add", {
            "domain": "d", "id": "p1", "rule": "r", "condition": "c", "reason": "y",
            "provenance": "prov"})
        self.assertEqual(argv[0], "add-principle")  # capability -> verb
        self.assertIn("--domain", argv)
        self.assertIn("d", argv)

    def test_optional_absent_param_is_omitted(self):
        argv = engine.build_argv(self.m, "principle-add", {
            "domain": "d", "id": "p1", "rule": "r", "condition": "c", "reason": "y",
            "provenance": "prov", "kind": ""})
        self.assertNotIn("--kind", argv)  # empty optional dropped

    def test_positional_emits_value_alone(self):
        # No live capability uses a positional after the native-ledger removal; a synthetic manifest
        # still pins build_argv's positional path (a positional emits the value with no flag).
        synth = {"plugin": "x", "capabilities": {"p": {
            "capability": "p", "verb": "vp", "args": [{"param": "file", "positional": True, "required": True}]}}}
        self.assertEqual(engine.build_argv(synth, "p", {"file": "h.md"}), ["vp", "h.md"])

    def test_global_option_precedes_the_verb(self):
        argv = engine.build_argv(self.m, "domain-migrate", {"root": "/proj", "source": "/seed"})
        self.assertEqual(argv[:2], ["--root", "/proj"])  # global goes BEFORE the subcommand
        self.assertEqual(argv[2], "migrate-domains")
        self.assertIn("--source", argv[3:])

    def test_boolean_emits_a_lone_flag(self):
        argv = engine.build_argv(self.m, "compose",
                                 {"root": "/r", "unit_of_work": "u", "json": True})
        self.assertIn("--json", argv)
        # the flag is not followed by a value
        self.assertEqual(argv[-1], "--json")

    def test_missing_required_param_raises_before_engine(self):
        with self.assertRaises(engine.CapabilityError):
            engine.build_argv(self.m, "chunk-close", {"workstream": "w"})  # no unit_of_work/stance/handoff

    def test_unknown_capability_raises(self):
        with self.assertRaises(engine.CapabilityError):
            engine.build_argv(self.m, "no-such-capability", {})


class ResolveAgainstStubTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.stub = write_stub(self.tmp)
        self.log = self.tmp / "log.txt"
        os.environ["STUB_LOG"] = str(self.log)
        os.environ.pop("STUB_FAIL", None)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        os.environ.pop("STUB_LOG", None)

    def test_resolve_runs_the_resolved_verb(self):
        res = engine.resolve(self.stub, "kill-report", {"domains_dir": "d", "audit": "a"})
        self.assertTrue(res.ok)
        self.assertEqual(read_log(self.log)[0][0], "kill-report")

    def test_resolve_degrades_when_engine_absent(self):
        res = engine.resolve(self.tmp / "nonexistent.py", "triggers", {})
        self.assertFalse(res.ran)  # praxis reports, does not crash


if __name__ == "__main__":
    unittest.main()
