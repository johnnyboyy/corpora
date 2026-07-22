# Audit record — web-frontend pack layer

Provenance and per-kill audit detail for the web-frontend pack domains. Loaded only at
ratify/retrospective time — never in a spawn's working context. Keyed by principle `id`, each
noting its `domain`. See `kernel.md`, "Storage: working vs audit." (Kill logs live in the
per-domain working files.)

> **Migration note (2026-06-22).** These principles were re-homed from the old role corpora
> (`coder.md` pack overlay, `ui-designer.md`, `ux-designer.md`) into domain working files as part of
> the corpus redesign. The role→domain move is uniform and recorded here once rather than as a
> `history` stanza on every principle; only notable moves (cross-role re-homing, consolidations,
> the documentation-before-screenshots dedup) carry an explicit `history` entry below.

```yaml
provenance:

# ---- domains: coding-ts, coding-react (split from coding-js-react 2026-07-18; see LINEAGE.md,
#      "The coding-ts / coding-react split") ----
- id: undefined-check-by-source
  domain: coding-ts
  provenance: "Merged from strict-undefined-check-in-arrays + array-access-undefined-not-null, Blog project, 2026-06-01."
  history:
    - date: 2026-07-18
      type: generalized
      reason: "Placed in coding-ts (not coding-react) once its actual test — matching the equality operator to a value's source — was recognized as general TS/JS semantics despite its 'optional props' framing. Tightened for seed level: the single-letter generic T became Value (this corpus's own no-single-char-names applies to its own examples), and the reason's project-level 'common codebase convention' framing was replaced with the general undefined-vs-null distinction the rule actually rests on."

- id: null-first-ternary
  domain: coding-react
  provenance: "2026-06-18, Blog project explicit-by-default post review."

- id: css-var-over-mapped-class-for-dynamic-color
  domain: coding-react
  provenance: "2026-06-13, Blog project WireCircle refactor."

- id: font-mono-at-element-not-container
  domain: coding-ts
  provenance: "2026-06-13, Blog project FixedBottomResultsBar refactor."

- id: hook-params-named-for-hook-concern
  domain: coding-react
  provenance: "2026-06-15, Blog project useHistoryState."

- id: hook-options-object-for-named-args
  domain: coding-react
  provenance: "2026-06-15, Blog project useHistoryState."

- id: wizard-callbacks-unconditional
  domain: coding-react
  provenance: "2026-06-14, Blog project load-calculator, Issue 19. see-also wizard-output-consistent-regardless-of-path (wizards-flows) — the implementation and UX faces of one concern, now legibly linked across domains."

- id: coordinated-setters-signal-reducer
  domain: coding-react
  kind: judgment
  provenance: "2026-06-28, HiraganaQuiz refactor. useQuizQueue had 8 useState calls; submitAnswer fired 5 setters and the advance timer fired 6. These groups mapped cleanly to 'submit' and 'advance' action types. Recognizing the grouped setters as an unnamed state machine — not just a large hook — is the non-obvious judgment."
  history:
    - date: 2026-06-29
      type: moved
      reason: "Promoted from Blog project domain to web-frontend pack seed — condition makes no reference to Blog-specific structure; general React hook wisdom."

- id: same-state-same-name
  domain: coding-ts
  kind: judgment
  provenance: "2026-06-28, HiraganaQuiz refactor. TileState 'resting' vs SpellTile 'idle' — same visual concept, two names. Decision to rename before extracting rather than casting or adding a translation layer. Renaming made SpellTile['state'] a structurally valid subset of TileState, eliminating buildSpellTileClass."
  history:
    - date: 2026-06-29
      type: moved
      reason: "Promoted from Blog project domain to web-frontend pack seed — general TypeScript/React structural wisdom, no Blog-specific framing."
- id: extract-named-concern-into-custom-hook
  domain: coding-react
  provenance: "2026-07-04, reading kyleshevlin.com/use-encapsulation/. Identified gap between coordinated-setters-signal-reducer (threshold-based) and the article's broader claim: the extraction signal is a nameable concern, not a setter count. Judgment call: extraction overhead vs. readability gain."
- id: effect-only-derived-state-belongs-in-render
  domain: coding-react
  kind: judgment
  provenance: "2026-07-15, FAMOUS PlayerBarContent review (operator flagged a coder principle possibly too web-specific for an unrelated hook-encapsulation question; while fixing the hook extraction, a separate useEffect surfaced that only reset scrubberOpen on track-id change via a ref comparison — moved to render body). Operator asked whether the sibling knowledge-tier kill no-read-after-set-in-same-scope was wrongly killed given this miss; on inspection the two patterns are unrelated (that kill concerns reading state synchronously after its own setter, this concerns an effect used purely for derivable state with no external interaction) but the miss itself prompted an audit of FAMOUS and Blog for recurrence. FAMOUS had only the one instance; Blog's ResultBar.tsx useResultFlash showed the identical shape independently (throttled setFlashKey bump keyed off prop-derived label/delta, no external interaction). Two independent hits across two different project shapes (Expo/RN, Next.js) in one pass — satisfies the cross-project-shape bar for promotion straight to seed rather than starting provisional in one project's working file."

- id: hook-returns-own-handlers
  domain: coding-react
  provenance: "2026-07-04, reading kyleshevlin.com/use-encapsulation/. Bundled-handler pattern shown in useOnOff and useInput examples — no existing principle covered it. Judgment call: complete hook interface vs. consumer flexibility."
  history:
    - date: 2026-07-06
      type: merged
      reason: "Merged with extract-named-concern-into-custom-hook into custom-hook-owns-its-concern. Extraction and interface completeness are co-decisions."

- id: extract-named-concern-into-custom-hook
  domain: coding-react
  provenance: "2026-07-04, reading kyleshevlin.com/use-encapsulation/. Identified gap between coordinated-setters-signal-reducer (threshold-based) and the article's broader claim: the extraction signal is a nameable concern, not a setter count. Judgment call: extraction overhead vs. readability gain."
  history:
    - date: 2026-07-06
      type: merged
      reason: "Merged with hook-returns-own-handlers into custom-hook-owns-its-concern. See that entry."

- id: hook-callsite-legibility
  domain: coding-react
  kind: judgment
  provenance: "2026-07-06, retrospective consolidation. Merged from hook-params-named-for-hook-concern (2026-06-15, Blog useHistoryState) and hook-options-object-for-named-args (same session). Both addressed hook callsite legibility and always co-fired. Judgment: naming params for the hook's concern and wrapping ambiguous primitives in an options object are two expressions of the same rule."

- id: custom-hook-owns-its-concern
  domain: coding-react
  kind: judgment
  provenance: "2026-07-06, retrospective consolidation. Merged from extract-named-concern-into-custom-hook (2026-07-04, kyleshevlin.com) and hook-returns-own-handlers (same source). Judgment: extraction and handler-return are co-decisions — separating them invites partial application."

- id: nan-serializes-to-null-in-json
  domain: coding-ts
  kind: judgment
  provenance: "Promoted from project domains 2026-07-06. Surfaced in Blog (2026-06-20, load calculator NaN incident); ported to FAMOUS (2026-07-01, cross-project review — no FAMOUS incident yet, but condition is easy to hit unknowingly). Two-project exposure via cross-project review justifies seed promotion. Condition broadened to cover any JSON serialization boundary, not only localStorage."

- id: behavior-flags-in-refs
  domain: coding-react
  provenance: "2026-07-01, cross-project Blog→FAMOUS deep review. Surfaced from load calculator useAutosave (isMountRef, pendingRef) and hiragana useSpellQueue (errorInRoundRef). All are boolean flags that gate logic without affecting rendered output. Written to seed domain."
  history:
    - date: 2026-07-06
      type: generalized
      reason: "Retrospective: absorbed timer-handles-in-refs-not-state. Timer IDs are behavioral flags; the dep-cascade concern is now part of this principle's reason. Rule and condition extended to name timer handles explicitly."
    - date: 2026-07-18
      type: generalized
      reason: "Structural-kinship retrospective signal: absorbed stable-ref-for-document-listeners. Both were instances of the same ref-vs-state test — mirroring current state for an external listener is a specific case of 'does this value drive rendered output.' Rule and reason extended to name the document-listener case explicitly."

- id: stable-ref-for-document-listeners
  domain: coding-react
  provenance: "No provenance was ever recorded for this principle when it was originally ratified — a pre-existing gap found while executing the 2026-07-18 structural-kinship merge, backfilled here rather than left permanently orphaned. Its rule concerned mirroring current React state into a ref for document-level event handlers to avoid stale closures."
  killed: 2026-07-18
  history:
    - date: 2026-07-18
      type: merged
      reason: "Merged into behavior-flags-in-refs — see that entry's history."

- id: nested-conditional-signals-sub-component
  domain: coding-react
  kind: judgment
  provenance: "2026-07-04, FAMOUS Discover refactor — operator refactored the chained isHydrated × data.length ternary into a binary skeleton/content switch at the parent level, with DiscoveryList owning its own empty/populated states. Judgment call: whether to extend generic-defers-to-consumer or stand alone — standalone chosen because generic-defers-to-consumer requires a reusable-unit framing that wouldn't fire on specific components. Originally ratified into FAMOUS project domain 2026-07-04."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Promoted from FAMOUS project domain to web-frontend pack seed at retrospective. Condition makes no reference to FAMOUS-specific structure — universal React/JSX judgment."

- id: named-exports-over-default
  domain: coding-ts
  kind: knowledge
  provenance: "2026-07-06, FAMOUS Expo migration gate. Surfaced from reading pipeline (basarat/typescript-book). Originally ratified into FAMOUS project domain."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Promoted from FAMOUS project domain to web-frontend pack seed at retrospective. Universal JS/TS module pattern; no FAMOUS-specific condition."

- id: prefers-reduced-motion-requires-js-hook
  domain: coding-react
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (joshwcomeau.com/react/prefers-reduced-motion — source URL returned 403 at extraction time, content pulled from training-data knowledge of this well-known article). Ratified directly to seed as the implementation-mechanics half of the reduced-motion pair; see reduced-motion-instant-not-absent (motion domain) for the design-judgment half."
  see-also: reduced-motion-instant-not-absent

- id: discriminated-union-for-mutually-exclusive-props
  domain: coding-react
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (developerway.com/posts/advanced-typescript-for-react-developers-discriminated-unions — source URL returned 403, extracted from search-result summaries of this and closely related sources). Ratified directly to seed — genuine recurring TS/React prop-typing decision, applicable to any project on this pack with variant-prop components."
  see-also: unified-representation-no-type-leakage

# ---- domain: coding-nextjs (new domain, forked from coding-js-react at retrospective 2026-07-06) ----
- id: suspense-not-needed-for-sync-client-components
  domain: coding-nextjs
  kind: judgment
  provenance: "2026-07-05, FAMOUS discover misc polish session. DiscoverPage wrapped Discover in Suspense with no fallback; operator reported intermittent back-button misdirection. Removing Suspense was the fix. Judgment call: the Suspense was a no-op for loading UX but a live variable in Next.js App Router's router cache handling on back navigation. Originally ratified into FAMOUS coding-js-react project domain."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Moved from FAMOUS project coding-js-react to coding-nextjs seed domain at retrospective. Condition is Next.js App Router-specific; FAMOUS migrated to Expo Router. Principle travels with the framework, not the project."

- id: view-transition-scope-at-page-slot-not-layout
  domain: coding-nextjs
  kind: judgment
  provenance: "2026-07-05, FAMOUS view transitions technology research session. Coder evaluated CSS View Transitions API, Framer Motion AnimatePresence, React 19 experimental ViewTransition. Judgment call: the risk of misapplying route-keying at the layout level (which would unmount a persistent audio player) is non-obvious. Originally ratified into FAMOUS coding-js-react project domain."
  history:
    - date: 2026-07-06
      type: moved
      reason: "Moved from FAMOUS project coding-js-react to coding-nextjs seed domain at retrospective. Condition is Next.js App Router-specific; FAMOUS migrated to Expo Router."

# ---- domain: css ----
- id: tailwind-extract-component-before-apply
  domain: css
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (tailwindcss.com/docs/reusing-styles). Ratified directly to seed — real recurring web-frontend decision (extract component vs @apply); FAMOUS itself has zero @apply usage (NativeWind/RN is component-first by default) but Blog or other DOM-CSS projects on this pack face the tradeoff directly."

- id: tailwind-loop-duplication-is-not-a-problem
  domain: css
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (tailwindcss.com/docs/reusing-styles), companion to tailwind-extract-component-before-apply from the same source. Ratified directly to seed for the same reason."

- id: grid-for-layout-flexbox-for-flow
  domain: css
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (blog.logrocket.com/css-flexbox-vs-css-grid). Ratified directly to seed with an explicit condition carve-out for React Native (no CSS Grid support natively) — applies to any DOM-CSS project on this pack, not to FAMOUS's native surfaces."

- id: mobile-fixed-bar-bottom-gap
  domain: css
  provenance: "2026-06-03, Blog project Box Selector mobile bottom bar."

- id: imports-before-tailwind-directives
  domain: css
  provenance: "2026-06-12, Blog project globals.css restructure."

- id: tokenize-only-recurring-magic-values
  domain: css
  provenance: "2026-06-12, Blog project globals.css restructure."

- id: table-row-color-override
  domain: css
  provenance: "2026-06-15, Blog project ampacity table temperature header text color."

# ---- domain: color ----
- id: semantic-tokens-required-for-theme-switching
  domain: color
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (smashingmagazine.com/2024/05/naming-best-practices). Ratified directly to seed — FAMOUS has one fixed dark aesthetic with no theme-switching need, but the two-tier (primitive/semantic) architecture is standard practice any project on this pack would need if it ever added light/dark or brand-variant theming."
  see-also: semantic-token-names-by-role-not-value

- id: semantic-token-names-by-role-not-value
  domain: color
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (smashingmagazine.com/2024/05/naming-best-practices), companion to semantic-tokens-required-for-theme-switching from the same source. Ratified directly to seed as structural confirmation — FAMOUS's own token names (--color-bg-canvas, --color-accent-fame, --color-bg-overlay) already follow role-based naming, not value-based."
  see-also: semantic-tokens-required-for-theme-switching

- id: color-palette-inspiration
  domain: color
  provenance: "2026-06-02, operator-provided. Clarified 2026-06-13."

- id: palette-chromatic-depth
  domain: color
  provenance: "2026-06-03, taste training session."

# ---- domain: surfaces-elevation ----
- id: disclosure-panel-vs-modal
  domain: surfaces-elevation
  provenance: "2026-06-14, load calculator history panel design spec."

- id: dark-floating-surface-fill
  domain: surfaces-elevation
  provenance: "2026-06-19, nav background depth session."

- id: scroll-fade-gradient-surface-match
  domain: surfaces-elevation
  provenance: "2026-06-19, nav background depth session."

# ---- domain: visual-hierarchy ----
- id: redundant-badge-sublabel
  domain: visual-hierarchy
  provenance: "2026-06-02, Box Selector visual spec."

- id: control-grouping-encodes-unity
  domain: visual-hierarchy
  provenance: "2026-06-03, taste training session (originally as capsule-encodes-same-value)."
  history:
    - date: 2026-06-20
      type: generalized
      reason: "Original rule prescribed capsule as the specific pattern — 'join into a capsule when segments share a value.' This directed the designer to a single implementation rather than stating the underlying principle. The insight is that any form of visual grouping (capsule, joined buttons, bordered cluster) encodes semantic unity; the specific form is a design decision the rule should inform, not resolve. Rule rewritten to state the general principle with capsule as one named example. Id renamed from capsule-encodes-same-value to reflect the broader concept."

- id: hierarchy-through-scarcity
  domain: visual-hierarchy
  provenance: "2026-06-04, retrospective consolidation."
  history:
    - date: 2026-06-20
      type: absorbed-examples
      reason: "Killed one-highlight-per-result-set and accent-color-for-distinction-not-data as redundant instances of this principle. Concrete examples those principles captured: (1) apply highlight to exactly one card per results panel — when two outputs are co-primary, merge into one highlighted card with an internal divider rather than two competing highlights; (2) accent color belongs only on the distinguished row, all other data values in secondary text color. Both earned in Box Selector results panel."

- id: responsive-text-by-viewport-distance
  domain: visual-hierarchy
  provenance: "2026-06-09, Box Selector desktop text legibility audit."

# ---- domain: motion ----
- id: motion-as-accent
  domain: motion
  provenance: "2026-06-03, taste training session."

- id: scrollytelling-must-always-react
  domain: motion
  provenance: "2026-06-13, homepage journey audit."

- id: reduced-motion-instant-not-absent
  domain: motion
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (joshwcomeau.com/react/prefers-reduced-motion — source URL returned 403 at extraction time, content pulled from training-data knowledge of this well-known article). Ratified directly to seed — no reduced-motion handling exists anywhere in FAMOUS yet, but the instant-vs-absent distinction is real UX judgment applicable to any project on this pack with JS-driven animation."
  see-also: motion-as-accent, prefers-reduced-motion-requires-js-hook

# ---- domain: recoverability ----
- id: recovery-path-replaces-confirmation
  domain: recoverability
  provenance: "2026-06-14, load-calculator audit."
  history:
    - date: 2026-06-20
      type: consolidated
      reason: "Absorbed recoverable-action-surfaces-its-path (originated ui-designer seed 2026-06-14, moved to ux-designer seed 2026-06-20). Both principles shared identical conditions and formed one complete thought: skip confirmation when recovery exists, and surface that recovery path. Separated, a designer could apply one without the other and get incomplete guidance. Merged rule absorbs both: recovery path is the gate AND must be made visible. Merged reason combines both justifications."
    - date: 2026-06-22
      type: moved
      reason: "Re-homed to the recoverability domain, now declared by BOTH ui-designer and ux-designer. The redesign makes structural what the 2026-06-20 consolidation did by hand: this judgment is one concern spanning flow (UX) and visible affordance (UI), and a domain both lenses declare is its natural home."
    - date: 2026-07-18
      type: generalized
      reason: "Absorbed destructive-global-actions-require-confirmation's ~30-second severity threshold — same recovery-or-confirmation test, one just named the bar for when the gate is mandatory."

- id: destructive-global-actions-require-confirmation
  domain: recoverability
  provenance: "2026-06-14, load-calculator UX audit."
  killed: 2026-07-18

- id: destructive-inline-confirmation
  domain: recoverability
  provenance: "2026-06-02 (originated in ui-designer seed corpus)."
  history:
    - date: 2026-06-20
      type: moved
      reason: "Principle describes interaction behavior (inline row transformation, confirm/cancel affordance), not visual design. Moved from UI designer seed to UX designer seed."
    - date: 2026-06-22
      type: moved
      reason: "Re-homed to the recoverability domain (declared by both designers). The 2026-06-20 UI→UX move was the container problem in miniature — the principle kept getting reassigned because no single role owned it. The domain ends the ping-pong."

- id: optimistic-ui-for-high-confidence-mutations
  domain: recoverability
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (dev.to/a1guy — React 19 useOptimistic deep dive; source URL returned 403, extracted from training-data knowledge of the API and standard optimistic-UI patterns). Ratified directly to seed — FAMOUS has zero server mutations currently (grepped, no fetch/API calls in the codebase), but the risk-weighing judgment (safe-to-assume vs. plausible-failure) is general and applicable to any project on this pack with a backend."
  see-also: recovery-path-replaces-confirmation, optimistic-rollback-requires-explicit-error

- id: optimistic-rollback-requires-explicit-error
  domain: recoverability
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (dev.to/a1guy), companion to optimistic-ui-for-high-confidence-mutations from the same source. Ratified directly to seed for the same reason."
  see-also: recovery-path-replaces-confirmation, optimistic-ui-for-high-confidence-mutations

# ---- domain: validation-feedback ----
- id: warning-colocated-with-resolution
  domain: validation-feedback
  provenance: "2026-06-02, Box Selector visual spec."

- id: warning-banner-must-locate-its-fix
  domain: validation-feedback
  provenance: "2026-06-02, Box Selector UX review."

- id: filter-side-effects-are-surfaced
  domain: validation-feedback
  provenance: "2026-06-02, Box Selector UX review."

# ---- domain: forms-inputs ----
- id: numeric-inputs-start-empty-not-zero
  domain: forms-inputs
  provenance: "2026-06-14, load-calculator UX audit."

- id: zero-count-orphan-rows
  domain: forms-inputs
  provenance: "2026-06-02, Box Selector UX review."

- id: unified-field-over-derived-dual-fields
  domain: forms-inputs
  provenance: "2026-06-14, load-calculator appliance row overhaul."

- id: persistent-controls-not-conditional
  domain: forms-inputs
  provenance: "2026-06-14, load-calculator appliance row overhaul."

- id: forms-reveal-conditional-fields
  domain: forms-inputs
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (nngroup.com/articles/progressive-disclosure). Ratified directly to seed — no current form in FAMOUS has this shape, but the guidance is applicable to any project on this pack with conditional-field forms."
  see-also: progressive-disclosure-for-primary-advanced-split, persistent-controls-not-conditional

- id: validate-on-blur-then-on-change
  domain: forms-inputs
  kind: knowledge
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (smashingmagazine.com/2022/09/inline-validation-web-forms-ux — source URL returned 403, extracted from search-result summaries and corroborating UX research). Ratified directly to seed — no field-level validation surface exists in FAMOUS yet, but the blur-then-change sequencing is standard, non-obvious enough to be worth encoding for any project on this pack with inline form validation."
  see-also: warning-colocated-with-resolution

# ---- domain: lists-selection ----
- id: indicator-weight-matches-job
  domain: lists-selection
  provenance: "2026-06-16, load calculator history redesign."

- id: active-row-is-inert
  domain: lists-selection
  provenance: "2026-06-16, load calculator history redesign."
  history:
    - date: 2026-07-10
      type: killed
      reason: "Superseded by active-row-is-inert-exact-route-only, promoted directly from the Meridian project (operator-approved cross-project edit, not a retrospective promotion) — see that entry below for the discovered defect."

- id: active-row-is-inert-exact-route-only
  domain: lists-selection
  kind: judgment
  provenance: "Meridian project, coder, 2026-07-10, top-bar rewrite pass. A Sidebar nav item's active state (`pathname.startsWith('/clients')`) spanned both the Clients list screen and every client-detail sub-page. Applying active-row-is-inert's blanket 'no hover, no click' treatment made a real, meaningful click (returning to the list from a detail page) silently do nothing, breaking tests/replay/runCase.ts's persistent-chrome recovery path (30 tests failed, confirmed via git stash bisection against the untouched baseline). Operator reviewed the coder's fix (keep it a real Link, styled to look inert) and pushed back: the styling itself was wrong too, not just an implementation detail — a section-spanning active item should stay visually and functionally interactive, since a click there does something real. Refined and edited directly into the shared pack seed at the operator's explicit request, rather than deferred to a project-level override or a future retrospective promotion."

- id: section-level-explanation-not-row-level
  domain: lists-selection
  provenance: "2026-06-14, load-calculator appliance row overhaul."

# ---- domain: wizards-flows ----
- id: origin-step-marked-visited-on-navigation
  domain: wizards-flows
  provenance: "2026-06-14, load-calculator UX audit."

- id: wizard-output-consistent-regardless-of-path
  domain: wizards-flows
  provenance: "2026-06-14, load-calculator UX audit. see-also wizard-callbacks-unconditional (coding-react)."

- id: optional-step-must-be-labeled-optional
  domain: wizards-flows
  provenance: "2026-06-14, load-calculator UX audit."

# ---- domain: ranking-evaluation ----
- id: triage-and-ranking-are-independent-signals
  domain: ranking-evaluation
  provenance: "Merged from intake-and-ranking-are-separate-activities + elo-as-independent-ranking-signal, 2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a comparative ranking/evaluation tool (Taste Trainer). Condition is narrow — tools that mix quick triage with deliberate ranking. Plausible general principle but untested against a second project with a ranking or evaluation feature. Do not promote until confirmed in a second context."

- id: category-scope-is-visible-on-ranked-items
  domain: ranking-evaluation
  provenance: "2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a per-category ranking tool (Box Selector). Condition presupposes category-scoped rankings — a pattern that may not recur in other web-frontend projects. Do not promote until confirmed in a second context."

- id: choice-prompt-anchors-on-usefulness-not-preference
  domain: ranking-evaluation
  provenance: "2026-06-02."
  history:
    - date: 2026-06-20
      type: provisional-flag
      reason: "Earned exclusively in a reference-building tool (Taste Trainer). Condition is narrow — tools whose output is meant to inform future decisions, not record taste. Do not promote until confirmed in a second context."

- id: callout-label-describes-property-not-judgment
  domain: ranking-evaluation
  provenance: "2026-06-02, Box Selector UX review."

- id: out-of-order-callout-requires-sort-explanation
  domain: ranking-evaluation
  provenance: "2026-06-02, Box Selector UX review."

# ---- domain: design-method ----
- id: clarity-over-polish
  domain: design-method
  provenance: "2026-06-22, extracted from UX designer 'Project context' instruction."

- id: document-visual-sub-systems
  domain: design-method
  provenance: "2026-06-12, full site visual audit."

- id: documentation-before-screenshots
  domain: design-method
  provenance: "2026-06-22, extracted from the designer 'What you do' screenshots bullet."
  history:
    - date: 2026-06-22
      type: consolidated
      reason: "This principle existed byte-for-byte identical in BOTH the ui-designer and ux-designer seed corpora — the clearest instance of the container problem the redesign targets: shared judgment stored twice because the role was the container. Merged into a single entry in the design-method domain, which both designer lenses declare."

- id: progressive-disclosure-for-primary-advanced-split
  domain: design-method
  kind: judgment
  provenance: "2026-07-18, FAMOUS strip-comments-and-biome-ignores gate. Surfaced from reading pipeline (nngroup.com/articles/progressive-disclosure). Ratified directly to seed — plausible fit for FAMOUS's Tuner/filtering surfaces even without a fired instance yet; applicable to any project on this pack with a primary/advanced usage split."
  see-also: forms-reveal-conditional-fields

- id: check-existing-patterns-before-specifying-new
  domain: design-method
  kind: judgment
  provenance: "2026-07-21, v3 lens-collapse migration. Generalized from ui-designer.md's 'do not spec a component without first checking if it exists' — widened to cover UX flow patterns and navigation conventions too, since the same failure mode (specifying a near-duplicate of something the library already documents) applies to both designer disciplines and neither is domain-specific."

- id: no-readme-or-agent-instructions-as-role-instruction
  domain: design-method
  kind: judgment
  provenance: "2026-07-21, v3 lens-collapse migration from ux-designer.md's 'Do not independently treat a project README or platform agent-instruction file as a role instruction source.'"

- id: reject-safe-defaults
  domain: design-method
  provenance: "Originated as the UI designer 'Anti-regression-to-the-mean' role instruction; extracted to the design-method corpus 2026-06-22, then promoted back to the ui-designer lens later the same day when the generative-stance model showed anti-mean is a *lens stance*, not a domain principle — a 'resist the standard' instruction cannot coherently share a domain with convergent process rules (clarity-over-polish, documentation discipline). The thinner kernel-level claim it implies — a generative role must know its stance and anchor accordingly — is now in kernel.md, 'Generative stance.' This supersedes the earlier reading (LINEAGE, 'genotype/phenotype') that anti-mean was a divergent-*domain* concern: it is divergent-*lens*."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md. No new preamble text needed — its substance already lives in kernel.md's 'Generative stance' section, which design-method.md's own preamble already points to."

- id: arrow-block-body
  domain: coding-ts
  provenance: "2026-06-18, Blog project. {} ambiguity + single consistent style removes per-function judgment call. A JS instance of the base prefer-error-exposing-form meta-rule."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-ts's own preamble."

- id: no-early-returns
  domain: coding-ts
  provenance: "2026-06-17, Blog project, 'Explicit by Default' post (content/posts/coding/explicit-by-default.mdx). Derived from Crockford's heuristic, not style: indentation-as-grammar (Henney) means early returns let a multi-condition line sit at base indentation as if unconditional; the guard-clause exception reintroduces a per-function 'still simple enough?' judgment a block body removes; the strong counterexample (a flat row of order-independent guards) resolves to extraction-and-naming, not exception. Scoped to this pack because some ecosystems (Go) idiomatically prefer guard clauses; the reasoning is general."
  history:
    - date: 2026-07-21
      type: folded-to-preamble
      reason: "promoted: retired per v3-redesign-proposal.md; substance moved into coding-ts's own preamble."

- id: no-shell-for-structural-absence
  domain: coding-ts
  provenance: "2026-07-19, sibling-implementation review (slider-puzzle/four vs one, two, three). Surfaced from four/script.js's repeated empty-else-with-restating-comment pattern (getAdjacentPositions, isBoardSolved, ensureTileElements, stopTimer, setCaption, handleTileClick — six instances). Weighed against no-early-returns: that principle governs branches where both sides do real work; this one covers the narrower case of a branch with no true opposite side, which the guard-clause reasoning was never meant to force into a populated shell. Held as a see-also peer, not a caveat rewrite of the existing bullet."
```
