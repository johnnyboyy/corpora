import datetime
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

    def write_manifest(self, entries="screens: []"):
        manifest_dir = self.root / "corpora" / "screenshots"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        (manifest_dir / "manifest.md").write_text(
            "# Screenshot manifest\n\n```yaml\n"
            + textwrap.dedent(entries).strip()
            + "\n```\n"
        )

    def write_image(self, relative_path):
        image_path = self.root / "corpora" / "screenshots" / relative_path
        image_path.parent.mkdir(parents=True, exist_ok=True)
        image_path.write_bytes(b"fake-png")

    def write_handoff(self, ui_drift="ui-drift:\n  screens: []\n  components: []", status="complete"):
        path = self.root / "handoff.md"
        path.write_text(f"""---
stance: convergent
composition: coder
status: {status}
domains-loaded: [coding-general]
proposals: []
utility-candidates: []
violations-noted: []
{ui_drift}
token-usage: "n/a"
delegated-workers: []
---

## Artifact

Nothing.

## Surfaced

""")
        return path

    def run_command(self, command):
        command = [command] if isinstance(command, str) else command
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *command],
            text=True,
            capture_output=True,
            check=False,
        )

    @staticmethod
    def entry(identifier="empty-state", stance="convergent", status="queued", blocking="no"):
        return f"""
        decisions:
          - id: {identifier}
            stance: {stance}
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
        self.assertIn("missing stance", result.stdout)
        self.assertIn("missing provisional-treatment", result.stdout)

    def test_invalid_stance_status_and_date_fail(self):
        self.write_config()
        entry = self.entry(stance="sideways", status="waiting").replace(
            "created: 2026-07-14", "created: today"
        )
        self.write_queue(entry)

        result = self.run_command("lint-deferred")

        self.assertEqual(result.returncode, 1)
        self.assertIn("stance must be", result.stdout)
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

    def test_deferred_groups_active_items_by_stance(self):
        self.write_config()
        ux = textwrap.dedent(self.entry(identifier="ux-choice")).strip()
        ui_item = textwrap.dedent(
            self.entry(identifier="ui-choice", stance="divergent")
        ).strip().removeprefix("decisions:\n")
        self.write_queue(ux + "\n" + ui_item)

        result = self.run_command("deferred")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("divergent (1)", result.stdout)
        self.assertIn("convergent (1)", result.stdout)
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


class LintHandoffUiDriftTest(CorpusCommandTestCase):
    def test_valid_nested_ui_drift_passes(self):
        path = self.write_handoff()

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS", result.stdout)

    def test_populated_nested_ui_drift_passes(self):
        path = self.write_handoff(
            ui_drift="ui-drift:\n  screens: [now-playing]\n  components: [like-button]"
        )

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_missing_ui_drift_fails(self):
        path = self.write_handoff(ui_drift="")

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 1)
        self.assertIn("ui-drift.screens missing or not a list", result.stdout)
        self.assertIn("ui-drift.components missing or not a list", result.stdout)

    def test_old_boolean_shape_fails(self):
        path = self.write_handoff(ui_drift="ui-drift: no")

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 1)
        self.assertIn("ui-drift.screens missing or not a list", result.stdout)
        self.assertIn("ui-drift.components missing or not a list", result.stdout)

    def test_missing_components_field_fails(self):
        path = self.write_handoff(ui_drift="ui-drift:\n  screens: []")

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 1)
        self.assertIn("ui-drift.components missing or not a list", result.stdout)
        self.assertNotIn("ui-drift.screens missing", result.stdout)

    def test_missing_stance_fails(self):
        path = self.write_handoff()
        path.write_text(path.read_text().replace("stance: convergent\n", ""))

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 1)
        self.assertIn("stance", result.stdout)

    def test_invalid_stance_fails(self):
        path = self.write_handoff()
        path.write_text(path.read_text().replace("stance: convergent", "stance: neutral"))

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 1)
        self.assertIn("stance 'neutral' not in", result.stdout)

    def test_empty_composition_fails(self):
        path = self.write_handoff()
        path.write_text(path.read_text().replace("composition: coder", "composition:"))

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 1)
        self.assertIn("composition present but empty", result.stdout)

    def test_old_role_field_no_longer_required(self):
        path = self.write_handoff()
        path.write_text(path.read_text().replace("composition: coder\n", ""))

        result = self.run_command(["lint-handoff", str(path)])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


class ScreenshotCommandsTest(CorpusCommandTestCase):
    @staticmethod
    def screen(identifier="now-playing", components="transport-cluster, like-button",
               status="current", last_touched="2026-07-21", variant_label="default",
               variant_path=None, captured="2026-07-21"):
        variant_path = variant_path or f"{identifier}/{variant_label}.png"
        return f"""
        screens:
          - id: {identifier}
            components: [{components}]
            status: {status}
            last-touched: {last_touched}
            variants:
              - label: {variant_label}
                path: {variant_path}
                captured: {captured}
        """

    def test_lint_missing_manifest_fails(self):
        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 2)
        self.assertIn("no corpora/screenshots/manifest.md", result.stderr)

    def test_lint_valid_manifest_passes(self):
        self.write_manifest(self.screen())
        self.write_image("now-playing/default.png")

        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("1 screens", result.stdout)

    def test_lint_empty_manifest_passes(self):
        self.write_manifest()

        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("0 screens", result.stdout)

    def test_lint_catches_missing_path_on_disk(self):
        self.write_manifest(self.screen())
        # deliberately do not write the image file

        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 1)
        self.assertIn("does not exist on disk", result.stdout)

    def test_lint_catches_missing_captured_date(self):
        self.write_manifest(self.screen(captured=""))
        self.write_image("now-playing/default.png")

        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing captured date", result.stdout)

    def test_lint_catches_orphaned_image(self):
        self.write_manifest()
        self.write_image("stray/orphan.png")

        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 1)
        self.assertIn("orphaned image not in manifest: stray/orphan.png", result.stdout)

    def test_lint_catches_duplicate_ids(self):
        first = textwrap.dedent(self.screen()).strip()
        second = textwrap.dedent(self.screen()).strip().removeprefix("screens:\n")
        self.write_manifest(first + "\n" + second)
        self.write_image("now-playing/default.png")

        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate id", result.stdout)

    def test_lint_catches_invalid_status(self):
        self.write_manifest(self.screen(status="fresh"))
        self.write_image("now-playing/default.png")

        result = self.run_command("lint-screenshots")

        self.assertEqual(result.returncode, 1)
        self.assertIn("status must be one of", result.stdout)

    def test_screenshot_record_creates_new_screen(self):
        self.write_manifest()

        result = self.run_command([
            "screenshot-record", "--screen", "now-playing", "--variant", "default",
            "--path", "now-playing/default.png",
            "--components", "transport-cluster, like-button",
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        manifest_text = (self.root / "corpora" / "screenshots" / "manifest.md").read_text()
        self.assertIn("id: now-playing", manifest_text)
        self.assertIn("status: current", manifest_text)
        self.assertIn("components: [transport-cluster, like-button]", manifest_text)
        self.assertIn("path: now-playing/default.png", manifest_text)

    def test_screenshot_record_updates_existing_variant(self):
        self.write_manifest()
        self.run_command([
            "screenshot-record", "--screen", "now-playing", "--variant", "default",
            "--path", "now-playing/default.png", "--components", "transport-cluster",
        ])

        result = self.run_command([
            "screenshot-record", "--screen", "now-playing", "--variant", "default",
            "--path", "now-playing/default.png", "--components", "transport-cluster, queue-sheet",
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        manifest_text = (self.root / "corpora" / "screenshots" / "manifest.md").read_text()
        self.assertIn("components: [transport-cluster, queue-sheet]", manifest_text)
        # only one variant entry for the same label, not a duplicate
        self.assertEqual(manifest_text.count("label: default"), 1)

    def test_screenshot_record_adds_second_variant(self):
        self.write_manifest()
        self.run_command([
            "screenshot-record", "--screen", "now-playing", "--variant", "default",
            "--path", "now-playing/default.png", "--components", "transport-cluster",
        ])

        result = self.run_command([
            "screenshot-record", "--screen", "now-playing", "--variant", "dark",
            "--path", "now-playing/dark.png", "--components", "transport-cluster",
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        manifest_text = (self.root / "corpora" / "screenshots" / "manifest.md").read_text()
        self.assertIn("label: default", manifest_text)
        self.assertIn("label: dark", manifest_text)

    def test_screenshot_mark_stale_direct_screen(self):
        self.write_manifest(self.screen())
        self.write_image("now-playing/default.png")

        result = self.run_command([
            "screenshot-mark-stale", "--screens", "now-playing", "--components", "",
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("marked stale: now-playing", result.stdout)
        manifest_text = (self.root / "corpora" / "screenshots" / "manifest.md").read_text()
        self.assertIn("status: stale", manifest_text)

    def test_screenshot_mark_stale_ripples_via_shared_component(self):
        entries = (
            textwrap.dedent(self.screen(identifier="now-playing", components="queue-sheet")).strip()
            + "\n"
            + textwrap.dedent(
                self.screen(identifier="discover", components="queue-sheet",
                            variant_path="discover/default.png")
            ).strip().removeprefix("screens:\n")
        )
        self.write_manifest(entries)
        self.write_image("now-playing/default.png")
        self.write_image("discover/default.png")

        result = self.run_command([
            "screenshot-mark-stale", "--screens", "", "--components", "queue-sheet",
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("now-playing", result.stdout)
        self.assertIn("discover", result.stdout)
        manifest_text = (self.root / "corpora" / "screenshots" / "manifest.md").read_text()
        self.assertEqual(manifest_text.count("status: stale"), 2)

    def test_screenshot_mark_stale_unknown_screen_is_noop(self):
        self.write_manifest(self.screen())
        self.write_image("now-playing/default.png")

        result = self.run_command([
            "screenshot-mark-stale", "--screens", "nonexistent-screen", "--components", "",
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("marked stale: none", result.stdout)

    def test_screenshot_status_lists_current_and_stale(self):
        entries = (
            textwrap.dedent(self.screen(identifier="now-playing")).strip()
            + "\n"
            + textwrap.dedent(
                self.screen(identifier="discover", status="stale", variant_path="discover/default.png")
            ).strip().removeprefix("screens:\n")
        )
        self.write_manifest(entries)
        self.write_image("now-playing/default.png")
        self.write_image("discover/default.png")

        result = self.run_command("screenshot-status")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("1 current, 1 stale", result.stdout)
        self.assertIn("now-playing", result.stdout)
        self.assertIn("discover", result.stdout)

    def test_screenshot_status_absent_manifest(self):
        result = self.run_command("screenshot-status")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("absent", result.stdout)

    def test_screenshot_lookup_finds_matching_screens(self):
        entries = (
            textwrap.dedent(self.screen(identifier="now-playing", components="queue-sheet")).strip()
            + "\n"
            + textwrap.dedent(
                self.screen(identifier="discover", components="hero-card",
                            variant_path="discover/default.png")
            ).strip().removeprefix("screens:\n")
        )
        self.write_manifest(entries)
        self.write_image("now-playing/default.png")
        self.write_image("discover/default.png")

        result = self.run_command(["screenshot-lookup", "--component", "queue-sheet"])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("now-playing", result.stdout)
        self.assertIn("now-playing/default.png", result.stdout)
        self.assertNotIn("discover", result.stdout)

    def test_screenshot_lookup_no_matches(self):
        self.write_manifest(self.screen())
        self.write_image("now-playing/default.png")

        result = self.run_command(["screenshot-lookup", "--component", "nonexistent-component"])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("no screens tagged", result.stdout)


class RecordGateCoOccurrenceAndOriginTest(CorpusCommandTestCase):
    def write_domain(self, name):
        (self.root / "corpora" / "domains" / f"{name}.md").write_text(
            f'# Domain: {name}\n\n```yaml\nprinciples:\n\n- id: p1\n  rule: "R"\n  condition: "C"\n  reason: "Why."\n```\n'
        )

    def record_gate(self, extra=()):
        return self.run_command([
            "record-gate", "--domain", "color", "--ratified", "0", "--killed", "0",
            "--violations", "0", *extra,
        ])

    def test_record_gate_tallies_domain_co_occurrence(self):
        self.write_domain("color")
        self.write_domain("motion")

        result = self.record_gate(["--co-occurs-with", "motion"])

        self.assertEqual(result.returncode, 0, result.stderr)
        audit_text = (self.root / "corpora" / "domains" / "audit.md").read_text()
        self.assertIn("domains: [color, motion]", audit_text)
        self.assertIn("count: 1", audit_text)

    def test_record_gate_co_occurrence_accumulates_across_gates(self):
        self.write_domain("color")
        self.write_domain("motion")

        for _ in range(2):
            result = self.record_gate(["--co-occurs-with", "motion"])
            self.assertEqual(result.returncode, 0, result.stderr)

        audit_text = (self.root / "corpora" / "domains" / "audit.md").read_text()
        self.assertIn("count: 2", audit_text)

    def test_record_gate_defaults_origin_to_project(self):
        self.write_domain("color")

        result = self.record_gate()

        self.assertEqual(result.returncode, 0, result.stderr)
        audit_text = (self.root / "corpora" / "domains" / "audit.md").read_text()
        self.assertIn("origin: project", audit_text)

    def test_record_gate_stamps_explicit_origin(self):
        self.write_domain("color")

        result = self.record_gate(["--origin", "seed"])

        self.assertEqual(result.returncode, 0, result.stderr)
        audit_text = (self.root / "corpora" / "domains" / "audit.md").read_text()
        self.assertIn("origin: seed", audit_text)


class ArbitraryLayerOverrideTest(unittest.TestCase):
    """measure/verify/record-gate must work on any domains-dir + audit.md pair — e.g. the
    kernel-seed layer, not only a project's own corpora/domains — the same treatment
    kill-report/graduate-kill already have."""

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.domains_dir = self.root / "seed-domains"
        self.domains_dir.mkdir()
        self.audit_path = self.domains_dir / "audit.md"
        (self.domains_dir / "widgets.md").write_text(
            '# Domain: widgets\n\n```yaml\nprinciples:\n\n- id: p1\n  rule: "R"\n  condition: "C"\n  reason: "Why."\n```\n'
        )
        self.audit_path.write_text("# Audit\n\n```yaml\nprovenance:\n```\n")

    def tearDown(self):
        self.tempdir.cleanup()

    def run_command(self, command):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *command],
            text=True, capture_output=True, check=False,
        )

    def layer_args(self):
        return ["--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path)]

    def test_measure_registers_a_non_project_layer(self):
        result = self.run_command(["measure", *self.layer_args()])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("widgets:", result.stdout)
        self.assertIn("counters:", self.audit_path.read_text())

    def test_verify_reconciles_a_non_project_layer(self):
        self.run_command(["measure", *self.layer_args()])

        result = self.run_command(["verify", *self.layer_args()])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("ledger reconciled", result.stdout)

    def test_record_gate_writes_to_the_given_audit_file(self):
        self.run_command(["measure", *self.layer_args()])

        result = self.run_command([
            "record-gate", *self.layer_args(), "--domain", "widgets", "--ratified", "1",
        ])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ratified: 1", self.audit_path.read_text())

    def test_measure_without_domains_dir_falls_back_to_root_corpora_domains(self):
        (self.root / "corpora" / "domains").mkdir(parents=True)
        (self.root / "corpora" / "domains" / "color.md").write_text(
            "# Domain: color\n\n```yaml\nprinciples:\n```\n"
        )

        result = self.run_command(["--root", str(self.root), "measure"])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("color:", result.stdout)


class ComposeSpawnPromptTest(CorpusCommandTestCase):
    def write_task(self, content="Implement the thing."):
        path = self.root / "task.md"
        path.write_text(content)
        return path

    def test_rejects_invalid_stance(self):
        task = self.write_task()

        result = self.run_command([
            "compose-spawn-prompt", "--stance", "neutral", "--domains", "coding-general",
            "--task-file", str(task),
        ])

        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice: 'neutral'", result.stderr)

    def test_assembles_seed_domain_stance_frame_and_handoff_schema(self):
        task = self.write_task("Fix the flaky test.")
        out = self.root / "out.md"

        result = self.run_command([
            "compose-spawn-prompt", "--stance", "convergent", "--domains", "coding-general",
            "--task-file", str(task), "--output", str(out),
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        text = out.read_text()
        self.assertIn("### Generative stance", text)
        self.assertIn("### Domain: coding-general", text)
        self.assertIn("## The handoff artifact", text)
        self.assertIn("Fix the flaky test.", text)
        # byte-for-byte, not summarized: a real principle id from the seed file must survive whole
        seed_text = (Path(__file__).parents[1] / "domains" / "coding-general.md").read_text()
        first_id_line = next(line for line in seed_text.splitlines() if line.strip().startswith("- id:"))
        self.assertIn(first_id_line.strip(), text)

    def test_project_domain_always_merges_with_seed(self):
        # No fork mechanism — a project's own domain file merges with the seed by concatenation,
        # always, regardless of what the project file's content looks like.
        task = self.write_task()
        out = self.root / "out.md"
        (self.root / "corpora" / "domains" / "coding-general.md").write_text(
            "# Domain: coding-general (project)\n\n```yaml\n"
            "principles:\n\n- id: project-only-rule\n  rule: \"R\"\n  condition: \"C\"\n  reason: \"Why.\"\n\nkilled:\n```\n"
        )

        result = self.run_command([
            "compose-spawn-prompt", "--stance", "convergent", "--domains", "coding-general",
            "--task-file", str(task), "--output", str(out),
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        text = out.read_text()
        self.assertIn("<!-- seed:", text)
        self.assertIn("<!-- project:", text)
        self.assertIn("project-only-rule", text)
        self.assertIn("ask-before-architecture", text)

    def test_project_only_domain_with_no_seed_counterpart(self):
        task = self.write_task()
        out = self.root / "out.md"
        (self.root / "corpora" / "domains" / "spatial-metaphor.md").write_text(
            "# Domain: spatial-metaphor\n\n```yaml\nprinciples:\n\nkilled:\n```\n"
        )

        result = self.run_command([
            "compose-spawn-prompt", "--stance", "convergent", "--domains", "spatial-metaphor",
            "--task-file", str(task), "--output", str(out),
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("### Domain: spatial-metaphor", out.read_text())

    def test_unknown_domain_fails(self):
        task = self.write_task()

        result = self.run_command([
            "compose-spawn-prompt", "--stance", "convergent", "--domains", "not-a-real-domain",
            "--task-file", str(task),
        ])

        self.assertEqual(result.returncode, 2)
        self.assertIn("nothing to compose", result.stderr)

    def test_defaults_output_path_under_session_prompts(self):
        task = self.write_task()

        result = self.run_command([
            "compose-spawn-prompt", "--stance", "convergent", "--domains", "coding-general",
            "--task-file", str(task), "--composition", "coder",
        ])

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        expected_dir = self.root / "corpora" / "session-prompts"
        self.assertTrue(expected_dir.is_dir())
        written = list(expected_dir.glob("*-coder.md"))
        self.assertEqual(len(written), 1)


class KillGraduationTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.domains_dir = self.root / "domains"
        self.domains_dir.mkdir()
        self.audit_path = self.root / "audit.md"
        today = datetime.date.today()
        self.old_date = (today - datetime.timedelta(days=200)).isoformat()
        self.recent_date = (today - datetime.timedelta(days=5)).isoformat()

    def tearDown(self):
        self.tempdir.cleanup()

    def write_domain(self, killed_ids):
        killed_block = "\n\n".join(
            f'- id: {kid}\n  rule: "Some rejected rule."\n  kill_type: quality\n  reason_killed: "Reason."'
            for kid in killed_ids
        )
        (self.domains_dir / "test-domain.md").write_text(
            "# Domain: test-domain\n\n```yaml\nprinciples:\n\n"
            '- id: active-one\n  rule: "R"\n  condition: "C"\n  reason: "Why."\n\n'
            f"killed:\n\n{killed_block}\n```\n"
        )

    def write_audit(self, entries):
        # No `promoted:` section — retired per v3-redesign-proposal.md. provenance: runs to EOF.
        lines = ["# Audit", "", "```yaml", "provenance:", ""]
        for kid, fields in entries.items():
            lines.append(f"- id: {kid}")
            lines.append("  domain: test-domain")
            lines.append('  provenance: "Some provenance."')
            for key, value in fields.items():
                lines.append(f"  {key}: {value}")
            lines.append("")
        lines += ["```", ""]
        self.audit_path.write_text("\n".join(lines))

    def run_command(self, command):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *command],
            text=True, capture_output=True, check=False,
        )

    def test_reports_missing_killed_date(self):
        self.write_domain(["undated-kill"])
        self.write_audit({"undated-kill": {}})

        result = self.run_command([
            "kill-report", "--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path),
        ])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("missing killed-date for: undated-kill", result.stdout)

    def test_reports_graduation_candidate_past_threshold(self):
        self.write_domain(["old-kill"])
        self.write_audit({"old-kill": {"killed": self.old_date}})

        result = self.run_command([
            "kill-report", "--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path),
            "--min-age-days", "90",
        ])

        self.assertIn("'old-kill' killed", result.stdout)
        self.assertIn("graduation candidate", result.stdout)

    def test_does_not_report_recent_kill_or_already_graduated(self):
        self.write_domain(["recent-kill", "graduated-kill"])
        self.write_audit({
            "recent-kill": {"killed": self.recent_date},
            "graduated-kill": {"killed": self.old_date, "graduated": self.old_date},
        })

        result = self.run_command([
            "kill-report", "--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path),
            "--min-age-days", "90",
        ])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("recent-kill", result.stdout)
        self.assertNotIn("graduated-kill", result.stdout)
        self.assertIn("no kills missing a date", result.stdout)

    def test_graduate_kill_removes_from_working_file_and_annotates_audit(self):
        self.write_domain(["old-kill", "other-kill"])
        self.write_audit({
            "old-kill": {"killed": self.old_date},
            "other-kill": {"killed": self.old_date},
        })

        result = self.run_command([
            "graduate-kill", "--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path),
            "--domain", "test-domain", "--id", "old-kill",
        ])

        self.assertEqual(result.returncode, 0, result.stderr)
        domain_text = (self.domains_dir / "test-domain.md").read_text()
        self.assertNotIn("old-kill", domain_text)
        self.assertIn("other-kill", domain_text)
        audit_text = self.audit_path.read_text()
        self.assertIn("graduated:", audit_text)

    def test_graduate_kill_refuses_without_recorded_date(self):
        self.write_domain(["undated-kill"])
        self.write_audit({"undated-kill": {}})

        result = self.run_command([
            "graduate-kill", "--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path),
            "--domain", "test-domain", "--id", "undated-kill",
        ])

        self.assertEqual(result.returncode, 2)
        self.assertIn("no recorded killed-date", result.stderr)

    def test_graduate_kill_refuses_when_already_graduated(self):
        self.write_domain(["old-kill"])
        self.write_audit({"old-kill": {"killed": self.old_date, "graduated": self.old_date}})

        result = self.run_command([
            "graduate-kill", "--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path),
            "--domain", "test-domain", "--id", "old-kill",
        ])

        self.assertEqual(result.returncode, 2)
        self.assertIn("already graduated", result.stderr)

    def test_parses_last_entry_with_no_promoted_marker(self):
        # promoted: retired as a section boundary; provenance: now runs to EOF. An entry that
        # would previously have sat right where a `promoted:` marker used to go must still parse.
        self.write_domain(["first-kill", "last-kill"])
        self.write_audit({
            "first-kill": {"killed": self.old_date},
            "last-kill": {"killed": self.old_date},
        })

        result = self.run_command([
            "kill-report", "--domains-dir", str(self.domains_dir), "--audit", str(self.audit_path),
            "--min-age-days", "90",
        ])

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("'first-kill' killed", result.stdout)
        self.assertIn("'last-kill' killed", result.stdout)


if __name__ == "__main__":
    unittest.main()
