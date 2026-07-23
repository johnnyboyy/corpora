# Domain: coding-expo

Expo/React Native judgment — loaded by any convergent coding spawn when the project's stack is
Expo (`corpora/config.md` framework is Expo or React Native via Expo). Audit metadata lives in
`domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: 2026-07-22

principles:

- id: expo-router-typed-routes-for-link-safety
  rule: "Enable Expo Router's Typed Routes (the `experiments.typedRoutes` config) so that a broken navigation link — a route that was renamed, moved, or never existed, or a path whose params don't match — is a TypeScript compile error rather than a silent runtime failure."
  condition: "Any Expo/React Native project using Expo Router's file-based routing, especially once route files get refactored, renamed, or moved after initial creation."
  reason: "File-based routing decouples a route's identity from any import statement — routes are referenced elsewhere only as string paths (`Link href`, `router.push`), which normal TypeScript checking does not validate. Moving or renaming a route file leaves those string references stale with no compiler signal; the break only surfaces when a user actually navigates that path. Typed Routes closes exactly this gap by checking route strings against the actual file tree at compile time — the error-exposing-form choice (coding-general's preamble meta-convention) applied specifically to route paths, since the convenience of plain strings and the safety of type-checked ones produce the same successful build until the untyped path is actually hit."
  domains: [coding-expo]

- id: expo-router-default-react-navigation-for-low-level-native-control
  rule: "Default to Expo Router for a new Expo/React Native project's navigation. Reach for bare React Navigation instead only when the project needs something Expo Router's conventions don't expose — heavily customized transitions/gestures, integrating navigation into an existing (brownfield) native app, or deliberately avoiding the Expo SDK ecosystem."
  condition: "Choosing or migrating a navigation library for an Expo/React Native project."
  reason: "Expo Router is built on top of React Navigation, not a replacement for it — it adds file-based routing conventions (folder structure doubles as the route table), automatic deep-linking, and web-route parity for every screen without extra configuration. Bare React Navigation requires imperative navigator setup and manual deep-linking wiring, but keeps direct, low-level control over navigator behavior. The conventions that make Expo Router faster for the common case are the same conventions that get in the way of the uncommon case (custom transitions/gestures, non-Expo native integration) — so the choice tracks how much of that low-level control the project actually needs, not a blanket 'newer is better' preference."
  domains: [coding-expo]

- id: interop-layer-does-not-cover-native-code-dependencies
  rule: "When a framework provides a backward-compatibility interop layer for a breaking architectural change, do not assume it covers every third-party dependency uniformly. Verify dependencies that ship native code individually — the interop layer's guarantee is explicitly weaker for those than for pure-JS libraries."
  condition: "Evaluating third-party library compatibility during a framework-level architecture migration that ships an interop/compat shim (e.g. React Native's New Architecture interop layer for old-architecture libraries)."
  reason: "Expo's own documentation states the interop layer 'is not perfect and some libraries will need to be updated' — the failure cases named are specifically libraries shipping native code, not JS-only ones. Treating the interop layer as a blanket guarantee papers over exactly the class of dependency most likely to fail, deferring discovery from migration time to a runtime crash."
  domains: [coding-expo]

- id: expo-router-no-direct-react-navigation-imports
  rule: "In an Expo Router project on SDK 56 or later, do not import navigation primitives directly from `@react-navigation/*`. Use Expo Router's own exports even for code that previously worked by importing straight from React Navigation."
  condition: "Expo SDK 56+ project using Expo Router, especially code or copied examples predating SDK 56 that imported navigation primitives directly from `@react-navigation/*` because Expo Router used to re-export/borrow them from that library."
  reason: "As of SDK 56, Expo Router forked the navigation primitives it previously borrowed from React Navigation, specifically to avoid two divergent navigation libraries coexisting inside the same app. A direct `@react-navigation/*` import that worked before SDK 56 now resolves to a library whose primitives are no longer the ones Expo Router's own navigator instantiates — the failure is a silent behavioral mismatch (state desync, missing navigation context) rather than an explicit deprecation error, so it surfaces at runtime, not at the import site."
  domains: [coding-expo]
  see-also: expo-router-default-react-navigation-for-low-level-native-control

- id: expo-filesystem-migrate-once-feature-gaps-close
  rule: "Re-evaluate a deferred migration off Expo's legacy FileSystem API once a release closes the specific feature gaps that justified staying on it (e.g. download progress reporting, cancellation via AbortSignal, an explicit overwrite flag on copy/move) — don't let the migration stay deferred by default once the blocking reason is gone."
  condition: "A project still on Expo's legacy FileSystem API specifically because the new API previously lacked a feature the project needs (progress reporting, cancellation, overwrite control), evaluated at each Expo SDK upgrade."
  reason: "A deferred migration is only correctly deferred while its blocking reason holds. SDK 56 closes the FileSystem API's most commonly cited feature gaps — treating the original 'the new API can't do X yet' justification as still valid without rechecking it is the same silent-drift failure as an unreviewed ceiling comment: the condition that justified the exception can become false with nobody rechecking it."
  domains: [coding-expo]
  see-also: ceiling-comment-for-deliberate-shortcuts, adopt-forced-migration-early-on-disposable-branch

- id: ota-update-scope-excludes-native-changes
  rule: "When planning a release via EAS Update (or any Expo OTA update mechanism), treat OTA as scoped strictly to JavaScript and asset changes. Any change touching native modules — new permissions, new native libraries, native config — requires a full app-store build/review cycle; do not schedule it as an OTA release."
  condition: "Planning what a given change can ship through versus requiring a store submission, in an Expo project using EAS Update or a comparable OTA mechanism."
  reason: "OTA update mechanisms operate below the native binary boundary — they can replace the JS bundle and assets an already-installed binary loads, but cannot alter the binary itself. Assuming OTA can patch anything is a natural mistake once a team has shipped a few JS-only OTA fixes; the failure mode is discovering mid-release that a change requiring new native permissions or libraries can't ship the fast way, forcing an unplanned store-review cycle under release pressure instead of one accounted for at planning time."
  domains: [coding-expo]

- id: expo-native-dirs-generated-not-hand-edited
  rule: "In an Expo project using Continuous Native Generation (CNG — the `npx expo prebuild` workflow), treat `ios/` and `android/` as generated build output, never as source to hand-edit. Make native-level customizations through config plugins that act on `app.json`/`app.config.js` (modifying `Info.plist`, `AndroidManifest.xml`, Gradle config, etc. at generation time), not by editing the generated native files directly."
  condition: "Any Expo project running the CNG/prebuild workflow that needs a native-level customization — permission entries, native SDK config, build-time native code hooks — whether building locally (`npx expo run:[ios|android]`) or via EAS Build's cloud VMs."
  reason: "`npx expo prebuild` regenerates `ios/` and `android/` from `app.json`/`app.config.js` plus installed config plugins (`@expo/prebuild-config`, `@expo/config-plugins`) every time it runs — including on every EAS Build invocation, which always prebuilds from a clean checkout. A hand-edit made directly to the generated directories is silently discarded on the next regeneration, with no error at edit time or build time to signal the loss — the customization simply isn't there anymore. This is the same failure shape coding-general's scripts-over-hand-editing-structured-data names for any generated artifact edited at its output instead of its source: the generator is the durable location for the change, and a config plugin is that location for native customizations in a CNG Expo project specifically. Committing generated ios/android directories to version control compounds the risk by making the stale hand-edit look authoritative to anyone reading the repo."
  domains: [coding-expo]
  see-also: scripts-over-hand-editing-structured-data

- id: expo-inline-native-modules-before-ejecting
  rule: "In an Expo SDK 56+ project needing native functionality with no existing Expo/community module for it, write the native code as an inline Swift/Kotlin file under a `watchedDirectories` folder and run `npx expo prebuild`, rather than ejecting the app or scaffolding a standalone native module package."
  condition: "A small-to-medium native capability (custom haptics, biometric auth, on-device ML, Bluetooth/NFC access, etc.) is needed in an Expo project targeting SDK 56 or later, and no existing library covers it."
  reason: "Before SDK 56, adding native code meant either fully ejecting (losing the managed workflow) or building a separate native module package with its own Podfile/Gradle scaffolding — both expensive enough relative to staying JS-only that teams often reached for JS workarounds even when native code was the better fit. Inline native modules remove that setup cost: the file lives next to the TypeScript it serves, autolinking and TypeScript type generation (`expo-type-information`) happen automatically on prebuild, and `requireNativeModule` is the only manual wiring left. Collapsing the cost from 'days of setup' to 'one file and a prebuild' changes the actual build-vs-workaround decision for capabilities that weren't previously worth the ceremony."
  domains: [coding-expo]

- id: expo-sequential-sdk-upgrade-across-router-fork
  rule: "When upgrading an Expo project from SDK 54 or earlier to SDK 56, upgrade one major SDK version at a time (54→55→56) rather than jumping directly, even though the standard upgrade command will attempt the direct jump."
  condition: "Expo project upgrade spanning SDK 56's Expo Router fork — i.e., starting from SDK 54 or earlier."
  reason: "SDK 56 forked Expo Router's navigation internals out of `@react-navigation/*`, changing the navigation dependency tree in a way direct 54-to-56 upgrades don't handle correctly; the intermediate SDK 55 step is what lets dependency resolution and codemods catch up incrementally. Skipping it converts a known, documented upgrade path into an unverified one — the failure surfaces mid-upgrade instead of being avoided by following the supported path. This is a distinct risk from the import-rewrite mechanics of the fork itself (already captured in expo-router-no-direct-react-navigation-imports)."
  domains: [coding-expo]
  see-also: expo-router-no-direct-react-navigation-imports

- id: expo-sdk56-fetch-default-swap-breaks-oauth
  rule: "Before or while upgrading to Expo SDK 56, explicitly test any code path that depends on precise `fetch` behavior — especially OAuth token exchange or third-party SDKs with their own fetch expectations (crash reporting, auth libraries) — because SDK 56 replaces the global `fetch` with `expo/fetch`, a differently-behaved implementation. Use the `EXPO_PUBLIC_USE_RN_FETCH=1` fallback as a temporary stopgap only, not a permanent fix, while dependencies catch up."
  condition: "Expo project upgrading to SDK 56 whose code or dependencies perform OAuth flows, use libraries with documented fetch-behavior assumptions, or otherwise rely on the platform's global fetch implementation matching prior behavior."
  reason: "A global-fetch swap is invisible in application-code diffs — nothing a developer wrote changed — but it alters runtime behavior everywhere fetch is used, so the risk stays silent until the specific flow depending on old behavior is actually exercised. Real breakages from exactly this change (an AT Protocol OAuth client, a crash-reporting SDK's compatibility issue) show the failure mode is concrete, not hypothetical. Treating a global runtime substitution shipped as a default upgrade the same as an opt-in feature is the mistake; it needs the same behavioral verification a manual dependency swap would get."
  domains: [coding-expo]

killed:
```
