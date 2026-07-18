import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "corpus.py"


class CorpusCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "corpora" / "domains").mkdir(parents=True)

    def tearDown(self):
        self.tempdir.cleanup()

    def write_config(self, has_ui="yes"):
        (self.root / "corpora" / "config.md").write_text(
            f"# Config\n\nhas-ui: {has_ui}\n"
        )

    def write_queue(self, entries="decisions: []"):
        (self.root / "corpora" / "deferred-decisions.md").write_text(
            "# Deferred decisions\n\n```yaml\n" + textwrap.dedent(entries).strip() + "\n```\n"
        )

    def write_candidates(self, entries="candidates: []"):
        (self.root / "corpora" / "utility-candidates.md").write_text(
            "# Utility candidates\n\n```yaml\n"
            + textwrap.dedent(entries).strip()
            + "\n```\n"
        )

    def run_command(self, command):
        command = [command] if isinstance(command, str) else command
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *command],
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def entry(identifier="empty-state", role="ux-designer", status="queued", blocking="no"):
        return f"""
        decisions:
          - id: {identifier}
            role: {role}
            domain: validation-feedback
            question: "Should empty results offer a reset action?"
            context: "Search results workstream."
            source-workstream: search
            created: 2026-07-14
            blocking: {blocking}
            provisional-treatment: "Preserve filters."
            related-files: [src/results.tsx]
            status: {status}
        """

    @staticmethod
    def candidate(identifier="color-math", status="open", reason="", second_evidence=False):
        disposition = (
            f'\n            disposition:\n              reason: "{reason}"' if reason else ""
        )
        return f"""
        candidates:
          - id: {identifier}
            operation-shape: "Deterministic perceptual color transformation."
            status: {status}
            evidence:
              - date: 2026-07-14
                workstream: settings-redesign
                burden: "Repeated manual color derivation."{'\n              - date: 2026-08-03\n                workstream: reporting-redesign\n                burden: "Manual compositing recurred."' if second_evidence else ''}{disposition}
        """

class DeferredAndUtilityCommandsTest(CorpusCommandTestCase):
    def test_valid_queue_passes(self):
        self.write_config()
        self.write_queue(self.entry())

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS", result.stdout)
        self.assertIn("1 entries", result.stdout)

    def test_empty_queue_passes(self):
        self.write_config()
        self.write_queue()

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("0 entries", result.stdout)

    def test_blocking_decision_fails(self):
        self.write_config()
        self.write_queue(self.entry(blocking="yes"))

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 1)
        self.assertIn("surface blockers immediately", result.stdout)

    def test_missing_required_fields_fail(self):
        self.write_config()
        self.write_queue("decisions:\n  - id: incomplete")

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing role", result.stdout)
        self.assertIn("missing provisional-treatment", result.stdout)

    def test_invalid_role_status_and_date_fail(self):
        self.write_config()
        entry = self.entry(role="coder", status="waiting").replace(
            "created: 2026-07-14", "created: today"
        )
        self.write_queue(entry)

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 1)
        self.assertIn("role must be", result.stdout)
        self.assertIn("status must be", result.stdout)
        self.assertIn("created must be YYYY-MM-DD", result.stdout)

    def test_duplicate_ids_fail(self):
        self.write_config()
        first = textwrap.dedent(self.entry()).strip()
        second_item = textwrap.dedent(self.entry()).strip().removeprefix("decisions:\n")
        self.write_queue(first + "\n" + second_item)

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate id", result.stdout)

    def test_resolved_entry_warns(self):
        self.write_config()
        self.write_queue(self.entry(status="resolved"))

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("resolved entries should be removed", result.stdout)

    def test_deferred_groups_active_items_by_role(self):
        self.write_config()
        ux = textwrap.dedent(self.entry(identifier="ux-choice")).strip()
        ui_item = textwrap.dedent(
            self.entry(identifier="ui-choice", role="ui-designer")
        ).strip().removeprefix("decisions:\n")
        self.write_queue(ux + "\n" + ui_item)

        result = self.run_command("deferred")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("ui-designer (1)", result.stdout)
        self.assertIn("ux-designer (1)", result.stdout)
        self.assertIn("ui-choice", result.stdout)
        self.assertIn("ux-choice", result.stdout)

    def test_non_ui_project_does_not_require_queue(self):
        self.write_config(has_ui="no")

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("no deferred-decision queue needed", result.stdout)

    def test_ui_project_requires_queue(self):
        self.write_config(has_ui="yes")

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 2)
        self.assertIn("has no corpora/deferred-decisions.md", result.stderr)

    def test_valid_utility_candidate_passes(self):
        self.write_candidates(self.candidate())

        result = self.run_command("lint-utility-candidates")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("1 entries", result.stdout)

    def test_empty_utility_candidate_ledger_passes(self):
        self.write_candidates()

        result = self.run_command("lint-utility-candidates")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("0 entries", result.stdout)

    def test_missing_utility_candidate_ledger_fails(self):
        result = self.run_command("lint-utility-candidates")

        self.assertEqual(result.returncode, 2)
        self.assertIn("no corpora/utility-candidates.md", result.stderr)

    def test_invalid_utility_candidate_status_and_date_fail(self):
        self.write_candidates(
            self.candidate(status="maybe").replace("date: 2026-07-14", "date: today")
        )

        result = self.run_command("lint-utility-candidates")

        self.assertEqual(result.returncode, 1)
        self.assertIn("status must be", result.stdout)
        self.assertIn("date must be valid YYYY-MM-DD", result.stdout)

    def test_utility_candidate_requires_evidence(self):
        candidate = self.candidate().replace(
            '            evidence:\n              - date: 2026-07-14\n                workstream: settings-redesign\n                burden: "Repeated manual color derivation."',
            "",
        )
        self.write_candidates(candidate)

        result = self.run_command("lint-utility-candidates")

        self.assertEqual(result.returncode, 1)
        self.assertIn("requires at least one evidence record", result.stdout)

    def test_denied_utility_candidate_requires_reason(self):
        self.write_candidates(self.candidate(status="denied"))

        result = self.run_command("lint-utility-candidates")

        self.assertEqual(result.returncode, 1)
        self.assertIn("denied status requires disposition reason", result.stdout)

    def test_duplicate_utility_candidate_ids_fail(self):
        first = textwrap.dedent(self.candidate()).strip()
        second = textwrap.dedent(self.candidate()).strip().removeprefix("candidates:\n")
        self.write_candidates(first + "\n" + second)

        result = self.run_command("lint-utility-candidates")

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate id", result.stdout)

    def test_utility_candidates_lists_status_and_sightings(self):
        self.write_candidates(
            self.candidate(status="denied", reason="Wait for recurrence.", second_evidence=True)
        )

        result = self.run_command("utility-candidates")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("color-math  status=denied  sightings=2", result.stdout)
        self.assertIn("first=2026-07-14  last=2026-08-03", result.stdout)

    def test_record_utility_candidate_creates_and_resurfaces_recurrence(self):
        self.write_candidates()
        base = [
            "record-utility-candidate",
            "--id", "color-math",
            "--operation-shape", "Deterministic perceptual color transformation.",
            "--workstream", "settings-redesign",
            "--burden", "Repeated manual color derivation.",
        ]

        first = self.run_command([*base, "--date", "2026-07-14"])
        second = self.run_command([
            "record-utility-candidate",
            "--id", "color-math",
            "--operation-shape", "Deterministic perceptual color transformation.",
            "--workstream", "reporting-redesign",
            "--burden", "Manual compositing recurred.",
            "--date", "2026-08-03",
        ])
        listing = self.run_command("utility-candidates")

        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        self.assertIn("recorded sighting 1", first.stdout)
        self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
        self.assertIn("RESURFACE", second.stdout)
        self.assertIn("sightings=2", listing.stdout)
        self.assertIn("first=2026-07-14  last=2026-08-03", listing.stdout)

    def test_record_utility_candidate_deduplicates_identical_evidence(self):
        self.write_candidates()
        command = [
            "record-utility-candidate",
            "--id", "color-math",
            "--operation-shape", "Deterministic perceptual color transformation.",
            "--workstream", "settings-redesign",
            "--burden", "Repeated manual color derivation.",
            "--date", "2026-07-14",
        ]
        self.run_command(command)

        duplicate = self.run_command(command)
        listing = self.run_command("utility-candidates")

        self.assertEqual(duplicate.returncode, 0, duplicate.stderr + duplicate.stdout)
        self.assertIn("identical evidence already recorded", duplicate.stdout)
        self.assertIn("sightings=1", listing.stdout)

    def test_set_utility_status_requires_and_persists_denial_reason(self):
        self.write_candidates(self.candidate())

        missing = self.run_command([
            "set-utility-status", "--id", "color-math", "--status", "denied"
        ])
        saved = self.run_command([
            "set-utility-status", "--id", "color-math", "--status", "denied",
            "--reason", "Wait for recurrence.",
        ])
        linted = self.run_command("lint-utility-candidates")

        self.assertEqual(missing.returncode, 2)
        self.assertIn("requires --reason", missing.stderr)
        self.assertEqual(saved.returncode, 0, saved.stderr + saved.stdout)
        self.assertEqual(linted.returncode, 0, linted.stderr + linted.stdout)


class AdoptCommandTest(CorpusCommandTestCase):
    def test_adopt_finds_kernel_seed_domain(self):
        result = self.run_command(["adopt", "--domain", "coding-general"])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("domains/coding-general.md", result.stdout)
        self.assertIn("ask-before-architecture", result.stdout)
        self.assertIn("fork-status: forked", result.stdout)

    def test_adopt_finds_pack_domain_when_role_pack_declared(self):
        (self.root / "corpora" / "config.md").write_text(
            "# Config\n\nhas-ui: yes\nrole-pack: web-frontend\n"
        )

        result = self.run_command(["adopt", "--domain", "css"])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("packs/web-frontend/domains/css.md", result.stdout)

    def test_adopt_fails_without_role_pack_for_pack_only_domain(self):
        result = self.run_command(["adopt", "--domain", "css"])

        self.assertEqual(result.returncode, 2)
        self.assertIn("nothing to fork from", result.stderr)

    def test_adopt_fails_for_domain_with_no_seed_counterpart(self):
        result = self.run_command(["adopt", "--domain", "not-a-real-domain"])

        self.assertEqual(result.returncode, 2)
        self.assertIn("nothing to fork from", result.stderr)

    def test_adopt_refuses_audit_which_is_the_ledger_not_a_domain(self):
        result = self.run_command(["adopt", "--domain", "audit"])

        self.assertEqual(result.returncode, 2)
        self.assertIn("nothing to fork from", result.stderr)

    def test_adopt_refuses_to_resync_an_already_forked_domain(self):
        (self.root / "corpora" / "domains" / "coding-general.md").write_text(
            "# Domain: coding-general\n\n```yaml\n"
            "fork-status: forked\n"
            "forked-from: domains/coding-general.md\n"
            "forked-date: 2026-07-18\n\n"
            "principles:\n\nkilled:\n```\n"
        )

        result = self.run_command(["adopt", "--domain", "coding-general"])

        self.assertEqual(result.returncode, 2)
        self.assertIn("already forked", result.stderr)


if __name__ == "__main__":
    unittest.main()
