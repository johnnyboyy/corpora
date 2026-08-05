#!/usr/bin/env python3
"""engine — the single overridable corpora binding shared by praxis's sequence scripts.

Part of praxis. The framing script isolated its one coupling to `frame.py::engine_compose` (the
*compose* capability). The migrated write-back / lifecycle processes (chunk close, ratify, kill
graduation, domain import, domain migration) need to invoke the engine's *write verbs* too — and
every one of those must go through ONE place, for the same reason `engine_compose` is one place:
praxis never imports corpora, never learns its schema, and the whole coupling surface is a single
function so that on lift it becomes an engine registry and nothing else changes.

`invoke()` is that function. A sequence script decides the ORDER, PRECONDITIONS, and GUARDS
(the deterministic orchestration praxis owns and tests); `invoke()` is the only thing that knows
*where corpora is* and *how to call it*. Tests drive every sequence script against a stub engine
via `--corpus-py`, so the orchestration is verified without corpora present.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# In-repo binding: praxis lives at <corpora-root>/praxis/, so corpora's CLI is two levels up.
# Identical anchor to frame.py::DEFAULT_CORPUS_PY — the two merge into one registry entry on lift.
DEFAULT_CORPUS_PY = Path(__file__).resolve().parents[2] / "scripts" / "corpus.py"


class EngineResult:
    """The outcome of one engine call. `ok` is the guard a sequence script branches on."""

    def __init__(self, returncode: int, stdout: str, stderr: str, ran: bool):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.ran = ran  # False when the engine binary was absent (praxis degrades, does not crash)

    @property
    def ok(self) -> bool:
        return self.ran and self.returncode == 0

    def note(self) -> str:
        if not self.ran:
            return "engine unavailable"
        if self.returncode == 0:
            return "ok"
        return f"engine returned {self.returncode}: {self.stderr.strip()[:200]}"


def invoke(corpus_py: Path, args: list[str], timeout: int = 60) -> EngineResult:
    """Run one corpora engine command. The sole coupling surface for engine write verbs.

    Never raises for an absent or failing engine — returns a result the caller guards on, so praxis
    reports facts (which step failed, in what order) instead of crashing on the engine.
    """
    corpus_py = Path(corpus_py)
    if not corpus_py.is_file():
        return EngineResult(127, "", f"engine not found at {corpus_py}", ran=False)
    try:
        p = subprocess.run(["python3", str(corpus_py), *args],
                           capture_output=True, text=True, timeout=timeout)
    except (subprocess.SubprocessError, OSError) as e:
        return EngineResult(1, "", f"engine invocation failed: {e}", ran=True)
    return EngineResult(p.returncode, p.stdout, p.stderr, ran=True)


def echo(result: EngineResult, label: str) -> None:
    """Relay an engine step's output to the caller, verbatim, tagged with which step it was."""
    tag = "ok" if result.ok else ("skipped (engine unavailable)" if not result.ran else "FAILED")
    sys.stdout.write(f"[{label}] {tag}\n")
    if result.stdout.strip():
        sys.stdout.write(result.stdout if result.stdout.endswith("\n") else result.stdout + "\n")
    if not result.ok and result.stderr.strip():
        sys.stdout.write(result.stderr.rstrip() + "\n")
