# Domain: dependency-management

Judgment for tasks whose actual subject is upgrading, migrating, or auditing dependencies — not
feature work that happens to touch a dependency in passing. Composed instead of `coding-general`
for this task shape: a task's coding-general judgment applies to every coding task regardless of
shape, but upgrade/migration judgment only applies when the task is actually about that. Audit
metadata lives in `domains/audit.md`, loaded only at ratify/retrospective time.

Read `corpora/config.md` first, for registered utilities and verification commands. Run the
project's verification commands before finishing. Report a `tradeoffs` block for any migration step
where cost clearly outweighs value, rather than proceeding or skipping silently.

```yaml
last-retrospective: 2026-07-22

principles:

- id: adopt-forced-migration-early-on-disposable-branch
  rule: "When a platform or framework sets a hard cutover date for a breaking architectural change (support for the old path ends on a named future release) but the change is still optional now, adopt it early on a disposable test branch rather than deferring to the deadline. Assess feasibility by temporarily removing or swapping out dependencies suspected of incompatibility to isolate what actually breaks, instead of reading changelogs and guessing."
  condition: "A framework or platform announces a mandatory architectural migration with a stated future cutoff while the current version still allows opting out."
  reason: "The real breakage surface of a large architectural change — especially one touching low-level internals a project doesn't control — is only discoverable by actually running the project against it, not by reading migration docs. Waiting until the deadline converts a bounded, correctable investigation into a forced, time-pressured cutover. A disposable branch makes the experiment free to abandon and cheap to repeat as dependencies update. First seen concretely in Expo's New Architecture migration (support for the old architecture ends at SDK 55 while still optional at the time of writing) — real breakage there is only discoverable by running the app against it, not by reading the migration guide."
  domains: [dependency-management]
  see-also: expo-filesystem-migrate-once-feature-gaps-close

- id: audit-transitive-dependencies-after-major-upgrade
  rule: "If code imports a package never added directly to the project's own dependency manifest — it worked because a parent dependency happened to include it — declare it explicitly rather than relying on the transitive resolution, and re-audit for this specifically after any major upgrade of a dependency it comes through."
  condition: "A dependency upgrade, especially a framework's own major version bump, removes an internal dependency that other packages had been quietly relying on without declaring it."
  reason: "A framework can stop bundling a package it previously included transitively; projects that imported it directly without listing it in their own manifest get module-not-found errors with no obvious link back to the upgrade, because nothing in their own dependency list changed — the removal happened one level up, invisible to their own diff. The fix (declare it explicitly, or migrate off it) is cheap, but only if caught by intentional audit rather than by a production stack trace with no clear cause. First seen concretely when Expo SDK 56 stopped bundling @expo/vector-icons as a transitive dependency."
  domains: [dependency-management]

killed:
```
