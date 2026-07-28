#!/bin/sh
# corpora SessionStart hook — runs in a project's working directory at every
# session start. Two jobs, both deterministic:
#   1. Announce that corpora is available here as a queryable domain/judgment
#      service and ratify-gate procedure — not an active orchestrator that
#      claims ownership of the session, just a service on request.
#   2. Reconcile the counters ledger against the working files, surfacing any
#      gate that ran off the books at the moment of peak attention.
# Always exits 0 — this hook informs; it never blocks a session.
#
# Register in the project's .claude/settings.json:
#   { "hooks": { "SessionStart": [ { "hooks": [ { "type": "command",
#     "command": "~/.claude/skills/corpora/scripts/session-start.sh" } ] } ] } }

[ -f corpora/config.md ] || exit 0

echo "corpora is available in this project: a domain/judgment service and ratify-gate procedure,"
echo "queryable on request — see ~/.claude/skills/corpora/SKILL.md for how to compose a stance +"
echo "domain subset, or invoke the ratify-gate procedure."

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$SCRIPT_DIR/corpus.py" --root . verify 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . lint-deferred 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . deferred 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . lint-deterministic-shortcut-candidates 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . deterministic-shortcut-candidates 2>&1

exit 0
