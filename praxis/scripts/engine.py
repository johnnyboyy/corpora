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

import json
import subprocess
import sys
from pathlib import Path

# In-repo binding: praxis lives at <corpora-root>/praxis/, so corpora's CLI is two levels up.
# Identical anchor to frame.py::DEFAULT_CORPUS_PY — the two merge into one registry entry on lift.
DEFAULT_CORPUS_PY = Path(__file__).resolve().parents[2] / "scripts" / "corpus.py"

# The engine's declared capability surface, as data. Praxis core never hardcodes a corpora verb; it
# resolves a capability NAME through this manifest, exactly as the handoff engine composes its schema
# from plugin manifests. A second engine drops its own manifest here and everything else is unchanged.
DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "engine" / "plugins" / "corpora.json"


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


class CapabilityError(KeyError):
    """A capability was not declared by the manifest, or a required param was not supplied.

    Raised before the engine is ever touched — an unresolvable capability is praxis's own bug (a
    script asking for something the manifest does not declare), not an engine failure to degrade past.
    """


def load_manifest(manifest_path: Path = DEFAULT_MANIFEST) -> dict:
    """Load the engine capabilities manifest and index it by capability name.

    Returns {"plugin": str, "capabilities": {name: entry}}. Praxis learns the verb/arg-shape of every
    engine capability from here — never from a hardcoded string in a script.
    """
    data = json.loads(Path(manifest_path).read_text())
    caps = {c["capability"]: c for c in data.get("capabilities", [])}
    return {"plugin": data.get("plugin", "?"), "capabilities": caps}


def build_argv(manifest: dict, capability: str, params: dict) -> list[str]:
    """Compose the corpora argv for a capability from declared params. Pure data → argv; no I/O.

    Global args (corpora's `--root`) precede the verb; positionals emit their value alone; booleans
    emit just the flag when truthy; everything else is a `--flag value` pair. Order within the verb's
    args follows the manifest's declared order. A missing required param raises CapabilityError.
    """
    cap = manifest["capabilities"].get(capability)
    if cap is None:
        raise CapabilityError(
            f"capability '{capability}' not declared by engine plugin '{manifest.get('plugin','?')}'")
    globals_: list[str] = []
    rest: list[str] = []
    for a in cap.get("args", []):
        name = a["param"]
        present = name in params and params[name] not in (None, "", False)
        if a.get("required") and not present:
            raise CapabilityError(f"capability '{capability}' requires param '{name}'")
        if not present:
            continue
        val = params[name]
        if a.get("boolean"):
            piece = [a["flag"]]
        elif a.get("positional"):
            piece = [str(val)]
        else:
            piece = [a["flag"], str(val)]
        (globals_ if a.get("global") else rest).extend(piece)
    return globals_ + [cap["verb"]] + rest


def resolve(corpus_py: Path, capability: str, params: dict, *, manifest: dict | None = None,
            timeout: int = 60) -> EngineResult:
    """Resolve a capability NAME to its argv via the manifest, then run it through `invoke`.

    This is how every sequence script calls the engine: by capability, never by verb string. The
    manifest (data) is the only place a corpora verb name lives; on lift it and `frame.engine_compose`
    collapse into the one engine registry. Param errors raise (praxis's own bug); engine
    unavailability/failure still degrades through `invoke`'s EngineResult, unchanged.
    """
    caps = manifest if manifest is not None else load_manifest()
    argv = build_argv(caps, capability, params)
    return invoke(corpus_py, argv, timeout=timeout)


def echo(result: EngineResult, label: str) -> None:
    """Relay an engine step's output to the caller, verbatim, tagged with which step it was."""
    tag = "ok" if result.ok else ("skipped (engine unavailable)" if not result.ran else "FAILED")
    sys.stdout.write(f"[{label}] {tag}\n")
    if result.stdout.strip():
        sys.stdout.write(result.stdout if result.stdout.endswith("\n") else result.stdout + "\n")
    if not result.ok and result.stderr.strip():
        sys.stdout.write(result.stderr.rstrip() + "\n")
