#!/bin/sh
# corpora SessionStart hook — runs in a project's working directory at every
# session start. Two jobs, both deterministic:
#   1. Announce that this is a corpora-managed project (so role work loads
#      lens + domains via the skill even when the operator forgets to invoke it).
#   2. Reconcile the counters ledger against the working files, surfacing any
#      gate that ran off the books at the moment of peak attention.
# Always exits 0 — this hook informs; it never blocks a session.
#
# Register in the project's .claude/settings.json:
#   { "hooks": { "SessionStart": [ { "hooks": [ { "type": "command",
#     "command": "~/.claude/skills/corpora/scripts/session-start.sh" } ] } ] } }

[ -f corpora/config.md ] || exit 0

ROLE_PACK=$(sed -n 's/^role-pack:[[:space:]]*//p' corpora/config.md | head -1)
echo "This is a corpora-managed project (role-pack: ${ROLE_PACK:-none})."
echo "Role work (coding, design, planning, review) goes through the corpora skill:"
echo "load the role's lens + declared domains before starting — see ~/.claude/skills/corpora/SKILL.md."

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$SCRIPT_DIR/corpus.py" --root . verify 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . lint-deferred 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . deferred 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . lint-utility-candidates 2>&1
python3 "$SCRIPT_DIR/corpus.py" --root . utility-candidates 2>&1

exit 0
