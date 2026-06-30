# Reading agent

Reads queued sources through the appropriate domain lens and extracts principle candidates.
Runs weeknights at 2 AM PST. Self-contained — no prior session context needed.

---

## Setup

1. Add and clone the corpora repo: `johnnyboyy/corpora`
2. Read `reading/queue.md`. If no entries have `status: unread`, exit — nothing to do.

## For each unread entry (one at a time, fresh context per entry)

### 1. Load the lens

From the entry's `domains` field, select the lens:
- `coding-general` → load `coder.md` + `domains/coding-general.md`
- `coding-js-react` → load `coder.md` + `packs/web-frontend/coder.md` +
  `domains/coding-general.md` + `packs/web-frontend/domains/coding-js-react.md`
- `ux-design`, `interaction`, or similar → load `packs/web-frontend/ux-designer.md`
  plus its declared domains
- `ui-design` or similar → load `packs/web-frontend/ui-designer.md` plus its declared domains

You are now reasoning through that lens for this entry.

### 2. Fetch and read

WebFetch the URL. If the URL is unknown (flagged in the entry), search for it first.

Read through the loaded lens. For each claim:
- Does it confirm, extend, or contradict an existing principle? (Note the principle id.)
- Does it address a gap the lens's domains don't cover?
- Is it specific enough to encode as `rule` + `condition` + `reason`?

### 3. Extract candidates

For each principled claim worth encoding, append to `reading/candidates.md`
inside the `candidates:` block:

```yaml
- id: [kebab-case-slug]
  rule: [the judgment, stated as guidance]
  condition: [when it applies — be specific]
  reason: [why — the justification that generalizes]
  domains: [domain names this belongs to]
  provenance:
    source: [URL]
    gap: [the gap this addressed]
    extracted: [YYYY-MM-DD]
  see-also: [ids of existing principles this relates to, if any]
```

If the source yields nothing principled, write nothing. Do not force candidates from
weak material.

### 4. Mark entry as read

Update the entry in `reading/queue.md`:

```yaml
  status: read
  read: [YYYY-MM-DD]
  candidates: [N]
```

## Commit and push

```bash
git add reading/queue.md reading/candidates.md
git commit -m "reading: [source-id] → [N] candidate(s)"
git push
```
