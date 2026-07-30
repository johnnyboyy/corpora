---
subject: coding
posture: guardrail
applies-when:
  - framework: [expo, react-native]
units-of-work: [migrate-dependencies]
universal: false
---

# Domain: dependency-management-expo

Expo/React Native-specific dependency, upgrade, and migration judgment — loaded by any convergent
coding spawn when the project's stack is Expo (`corpora/config.md` framework is Expo or React
Native via Expo), alongside the stack-agnostic `dependency-management` domain. Split out
2026-07-23 rather than folded into either `dependency-management` or `coding-expo`: none of its
seed principles were general enough to state as stack-agnostic guidance, but they are specifically
about upgrade/dependency judgment rather than coding-expo's broader implementation judgment — see
`LINEAGE.md`. Two of the five (`codemod-deprecation-check-after-rewrite`,
`escalate-unmapped-symbols-dont-diy-workaround`) are themselves codemod-migration judgment rather
than Expo-specific judgment; left here rather than force-generalized, since a real cross-stack
`codemod-migration` domain only earns its own fork once a comparable codemod scenario shows up
outside Expo (e.g. a Next.js codemod) to test whether the generalization actually holds. Audit
metadata lives in `domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: none

principles:

- id: pin-multi-package-versions-for-native-graphics-stack
  rule: "When integrating a from-scratch native GPU/graphics stack built from several young, tightly-coupled libraries (e.g. react-native-wgpu + three.js + @react-three/fiber + wgpu-matrix), pin exact tested-compatible versions across all of them rather than letting each package's own semver range resolve independently, and re-verify the whole set together before bumping any single package."
  condition: "Adding or upgrading WebGPU/Three.js/react-three-fiber (or a comparable emerging, multi-package native-bridge integration) in an Expo project."
  reason: "The real compatibility contract between these packages isn't expressed in any one package's own semver range — a version bump in one can silently break the FFI/type contract with the others even though npm install succeeds and each package's own constraints are individually satisfied. The failure surfaces as type errors or runtime crashes discovered only by running the app, not by dependency resolution."
  domains: [dependency-management-expo]

- id: recheck-workaround-artifacts-every-sdk-upgrade
  rule: "At every Expo SDK upgrade, review expo.install.exclude entries in package.json and any patches in patches/ — both are workarounds for a specific past incompatibility. Remove any whose blocking reason the new SDK version has closed; don't leave them in by default just because they still 'work'."
  condition: "Any Expo SDK upgrade where the project has one or more expo.install.exclude entries or dependency patches accumulated from earlier versions."
  reason: "Both artifacts route around a problem that held at some past SDK version, carry no expiration, and nothing prompts a recheck. An unreviewed exclude or patch silently keeps a project on stale dependency resolution or a stale source patch past the point the underlying fix shipped — the same failure shape as an unreviewed ceiling comment."
  domains: [dependency-management-expo]
  see-also: [ceiling-comment-for-deliberate-shortcuts, expo-filesystem-migrate-once-feature-gaps-close]

- id: codemod-deprecation-check-after-rewrite
  rule: "After a codemod or scripted import rewrite completes cleanly, check each rewritten symbol for a @deprecated tag or runtime deprecation warning before treating the migration as finished."
  condition: "Any automated or semi-automated import-rewrite migration that resolves imports to a compatibility/interop module — e.g. the Expo SDK 56 @react-navigation/* → expo-router import rewrite."
  reason: "A codemod's success criterion is 'does this compile and resolve,' not 'is this the currently recommended API' — an import can resolve cleanly to a deprecated shim kept only for backward compatibility, which passes typecheck and build but silently leaves the project one step behind, discovered again at the next upgrade cycle when the shim may be removed outright."
  domains: [dependency-management-expo]

- id: escalate-unmapped-symbols-dont-diy-workaround
  rule: "If a @react-navigation/* symbol has no expo-router replacement during this migration, don't invent a local workaround (a shim, a re-export, a copied implementation) to keep the old symbol alive. Ask the user to file an issue upstream describing what's needed, and treat the symbol as blocked until a real replacement exists."
  condition: "Performing the SDK 56 react-navigation-to-expo-router import migration and encountering a symbol not covered by the manual mapping table or the codemod."
  reason: "A hand-rolled workaround creates project-specific technical debt that has to be undone later when the framework adds real support, and risks diverging from the eventual official API. Filing upstream keeps the project on the framework's supported surface and turns an invisible local patch into a visible, trackable blocker."
  domains: [dependency-management-expo]

- id: reanimated-worklets-new-required-peer-post-newarch
  rule: "After a major framework or architecture upgrade, explicitly check whether libraries already in the project gained new required peer dependencies — don't rely on a dependency audit that only checks direct imports against package.json."
  condition: "Any Expo SDK upgrade crossing SDK 54 in a project using react-native-reanimated, where react-native-worklets became a required (no longer bundled) peer dependency under the New Architecture — and more generally, any major framework upgrade where a previously-bundled capability of an existing dependency splits out into its own required peer package."
  reason: "A project that upgrades cleanly can still have a dependency silently fail at first use: a missing new peer dependency shows up as a native-module resolution failure, not a JS-level one caught by typecheck. This is the forward-migration mirror of auditing transitive dependencies after a major upgrade."
  domains: [dependency-management-expo]
  see-also: [audit-transitive-dependencies-after-major-upgrade]

- id: root-stack-vs-js-stack-codemod-collision
  rule: "When migrating @react-navigation/* imports to expo-router on SDK 56+, never rewrite `import { Stack } from 'expo-router'` to `expo-router/js-stack`."
  condition: "Running or reviewing the SDK 56 @react-navigation/* → expo-router import migration, whether via the automated codemod or a manual pass, specifically for files importing the root layout Stack component."
  reason: "The root Stack from expo-router is the file-based layout component used in route files — a different thing from expo-router/js-stack's JS stack navigator (the replacement for @react-navigation/stack). The two Stack exports are unrelated APIs sharing an identifier, so a naive global replace (or codemod bug) treating every Stack import identically would silently point layout-file Stack usage at the wrong module — an error a diff review focused on 'did the import path change' would not catch without knowing this distinction exists."
  domains: [dependency-management-expo]
  see-also: [expo-router-no-direct-react-navigation-imports]

- id: expo-av-video-android-parity-gap-fails-silently
  rule: "When migrating from expo-av to expo-video, explicitly test the Android build, not just iOS — known migration issues (both packages installed simultaneously causing a black VideoView; the same player mounted in multiple VideoViews at once; setting player.currentTime inside the useVideoPlayer setup callback) are Android-specific, work fine on iOS, and fail as a blank video view with no thrown error."
  condition: "Migrating video playback from expo-av to expo-video, at the point of verifying the migration on both platforms."
  reason: "Every named failure mode is a silent visual regression (black screen) rather than an exception, and every one is Android-only — a migration verified only on iOS will pass cleanly and still ship a broken video screen on Android."
  domains: [dependency-management-expo]

killed:
```
