# Discovery agent

Finds high-quality sources worth reading for new principles and adds them to the queue.
Runs Fridays at 8 AM PST. Self-contained — no prior session context needed.

---

## Setup

1. Add and clone the corpora repo: `johnnyboyy/corpora`
2. Read `reading/config.md` for feeds and author list
3. Read all domain working files: `domains/*.md` and `packs/web-frontend/domains/*.md`

## Gap identification

From the domain files, identify:
- **Thin areas** — domains with few principles, or principles whose conditions leave obvious
  ground uncovered
- **Contested kills** — entries in any `killed:` log where `reason_killed` suggests the
  question is unresolved rather than definitively closed

Derive 3–5 search queries from these gaps. Queries must be specific:
"React hook encapsulation patterns" not "React best practices".

## Author and feed check

For each author in `config.md`:
- Search for recent writing (last 6 months) on topics matching the current domains
- WebFetch known URLs if listed

For each feed in `config.md`:
- WebFetch to retrieve current content
- Scan titles/summaries for topic match against identified gaps

Also follow one citation hop from listed authors: if a source by a listed author cites
someone, add that cited source to the candidate pool for argument-density check.

## Quality filter

Both conditions must pass before an entry is queued:

1. **Topic match** — addresses a gap you identified. (Listed authors bypass this — go
   straight to argument-density.)
2. **Argument density** — makes a specific, reasoned claim with a because. A single tweet
   that argues a position qualifies. A listicle does not. Ask: could this claim become a
   principle with `rule`, `condition`, and `reason` fields?

## Write to queue

For each source that clears the filter, append to `reading/queue.md` inside the `queue:` block:

```yaml
- id: [kebab-case-slug]
  url: [full URL]
  domains: [domain names this addresses, e.g. coding-general, coding-js-react]
  gap: "[one sentence: the gap this addresses]"
  status: unread
  added: [YYYY-MM-DD]
  source: discovery
```

Do not add sources already present in `queue.md` (check by URL).

## Commit and push

```bash
git add reading/queue.md
git commit -m "discovery: queue [N] new sources ([date])"
git push
```

If nothing cleared the filter this run, still commit a brief dated note in `queue.md`
as a comment so there is a record of the run.
