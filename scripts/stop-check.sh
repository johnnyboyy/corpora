#!/bin/sh
# corpora Stop hook — best-effort reconciliation check, not a transcript-level guarantee.
#
# kernel.md's "Before writing it, re-read the output against the composed domains" is an
# instruction to the spawn, and an instruction is a thing that sometimes doesn't happen (kernel.md,
# "The handoff artifact"). This hook cannot see whether that re-read happened — Stop-hook input
# does not carry the originating spawn prompt, and it remains unverified whether SubagentStart's
# does either (open question, see kernel.md's "Chunk chaining" cross-reference and LINEAGE.md). So
# it checks the one thing it CAN verify mechanically instead: every chunk recorded in
# corpora/chunks/*.md still matches what `corpus.py select` would compose today. A mismatch means
# either the project's config.md or a domain's frontmatter changed since the chunk closed
# (composition drift), or a chunk record was hand-edited — both worth surfacing before the session
# ends silently, per `verify-chunks`'s own docstring in corpus.py.
#
# Blocking at Stop continues the conversation rather than erroring, so the spawn can fix the drift
# before terminating. A project with no corpora/chunks/ directory (no chunked work this session) is
# always allowed through — this hook has nothing to reconcile in that case, not a violation.
#
# Register in the project's .claude/settings.json:
#   { "hooks": { "Stop": [ { "hooks": [ { "type": "command",
#     "command": "~/.claude/skills/corpora/scripts/stop-check.sh" } ] } ] } }

[ -f corpora/config.md ] || exit 0

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUTPUT=$(python3 "$SCRIPT_DIR/corpus.py" --root . verify-chunks 2>&1)
STATUS=$?

if [ "$STATUS" -ne 0 ]; then
  REASON=$(printf '%s' "$OUTPUT" | python3 -c 'import json, sys; print(json.dumps(sys.stdin.read()))')
  printf '{"decision": "block", "reason": %s}\n' "$REASON"
fi

exit 0
