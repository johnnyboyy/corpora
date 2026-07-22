# Principle candidates

Extracted by the reading agent from queued sources. Surfaced at the ratify gate
for domains matching the current project's composed domains. Candidates are removed
once ratified or killed.

```yaml
candidates:

- id: immutable-by-default
  rule: "Declare variables, parameters, and data structures in their immutable form by default. Reach for const, readonly, and frozen or value types before their mutable counterparts; only use a mutable form when the variable or structure genuinely needs to change."
  condition: "When declaring any variable, parameter, property, or data structure in any language where immutable alternatives exist — including const for local variables, readonly for properties and parameters, and frozen or record types for structured data."
  reason: "Most defects from incorrect state modification occur on values that were never intended to change. A mutable declaration invites reassignment at every subsequent point of use and converts unintended mutation into a silent logic error. An immutable declaration converts the same mistake into a compile-time or runtime error. The discipline extends the prefer-error-exposing-form meta-convention from syntax choices (strict equality, block arrow bodies) into data declarations."
  domains: [coding-general]
  provenance:
    source: https://kevlinhenney.medium.com/restrict-mutability-of-state-1ac69d1ec5fe
    gap: "coding-general has no principle about preferring immutable/const declarations when state does not need to change — the mutability-as-correctness-discipline angle of prefer-error-exposing-form"
    extracted: 2026-07-20
  see-also: []

- id: use-transition-vs-deferred-value
  rule: "Use useTransition when you control the state setter that triggers the expensive render — wrap the setter call inside startTransition. Use useDeferredValue when the value arrives from props or a source whose setter you don't control. Apply either only after confirming that the UI exhibits visible lag that React.memo or useMemo cannot fix."
  condition: "When de-prioritizing an expensive re-render in React to keep the UI responsive during user input. The access-level test applies first: do you own the setter, or only the value?"
  reason: "Both hooks de-prioritize a render pass, but they attach at different points in the data flow. useTransition wraps the setter call and requires setter access; useDeferredValue wraps the value at the consumer and requires only that the value is available. The decision signal is access level, not state vs. props semantics. Applying either hook before confirming visible lag adds complexity with no UX benefit — the optimization targets a rendering symptom that may not exist, and simpler memoization should be tried first."
  domains: [coding-react]
  provenance:
    source: https://www.developerway.com/posts/use-transition
    gap: "coding-react has no principle about React concurrent mode hooks — when to use useTransition vs useDeferredValue for de-prioritizing renders"
    extracted: 2026-07-20
  see-also: []

- id: container-queries-for-component-scope
  rule: "Use container queries when a component's layout should adapt to its own available width, regardless of viewport size. Use media queries for page-level layout breakpoints and browser feature detection. The two coexist: media queries set top-level column structure; container queries govern how individual components render within those columns."
  condition: "When adding responsive behavior to a CSS component that may be placed in varying container widths across different page contexts — sidebars, dialogs, full-width slots — or when the component needs to change layout independently of the viewport size."
  reason: "A media-queried component responds to viewport width, which does not change when the component moves from a wide content area to a narrow sidebar. A container query responds to the component's own allocated width, making it context-portable. Relying on media queries for component-level layout adaptations creates a hidden coupling between the component's style and its position in the page — moving it to a different context breaks its layout. Container queries remove that coupling."
  domains: [css]
  provenance:
    source: https://blog.logrocket.com/choose-between-media-container-queries/
    gap: "css domain has no principle about when to use container queries vs media queries — a recurrent decision for component-level vs. viewport-level responsive behavior"
    extracted: 2026-07-20
  see-also: []

- id: server-components-for-initial-data
  rule: "Fetch data in Server Components and pass it as props to Client Components. Only move data fetching into a Client Component when the fetch depends on client-side state — user interaction, browser APIs, or post-mount events — that is unavailable at the server render boundary."
  condition: "When a Client Component needs data from an API or database on initial render, and the fetch has no dependency on browser-only state that would prevent fetching the same data on the server."
  reason: "A Client Component that fetches data via useEffect or a client-side library sends the request from the browser after mount — adding a full network round-trip after initial HTML loads. A Server Component fetches during the server render, where the data source is co-located, before any HTML reaches the browser. The round-trip is only justified when the fetch requires client state that does not exist at server render time."
  domains: [coding-nextjs]
  provenance:
    source: https://vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them
    gap: "coding-nextjs has only 2 principles and no retrospective — the domain is thin; this Vercel post covers multiple judgment-level App Router pitfalls not yet in the corpus"
    extracted: 2026-07-20
  see-also: []

- id: revalidate-tag-over-path
  rule: "Tag cached fetches with descriptive keys using the next: { tags: [...] } option and invalidate with revalidateTag. Use revalidatePath only when the entire page cache must be cleared regardless of which data it contains."
  condition: "When deciding how to invalidate Next.js cache in a Server Action or Route Handler after a mutation."
  reason: "revalidatePath clears all cached data for a given URL path — if the page fetches N queries, all N are invalidated even if only one changed. revalidateTag targets only data carrying a specific tag, leaving unrelated cached data intact. Coarse invalidation with revalidatePath degrades performance as page data complexity grows; tag-based invalidation is surgical and scales to the mutation's actual scope."
  domains: [coding-nextjs]
  provenance:
    source: https://vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them
    gap: "coding-nextjs has only 2 principles and no retrospective — the domain is thin; this Vercel post covers multiple judgment-level App Router pitfalls not yet in the corpus"
    extracted: 2026-07-20
  see-also: []

- id: server-actions-for-mutations-not-queries
  rule: "Use Server Actions exclusively for mutation operations (create, update, delete) invoked from user interactions. Use Route Handlers for operations that return arbitrary payloads, require HTTP method control, response headers, or streaming."
  condition: "When deciding whether to implement a server-side operation as a Server Action or a Route Handler in a Next.js App Router project."
  reason: "Server Actions are optimized for the mutation → revalidate cycle: they run in response to form actions or client event handlers, mutate data, and optionally call revalidateTag or revalidatePath. They have no mechanism for HTTP method control, response headers, or streaming — capabilities Route Handlers provide. Using a Server Action as a data-fetching endpoint conflates mutation and query responsibilities and bypasses the HTTP semantics and response contract that Route Handlers are designed to enforce."
  domains: [coding-nextjs]
  provenance:
    source: https://vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them
    gap: "coding-nextjs has only 2 principles and no retrospective — the domain is thin; this Vercel post covers multiple judgment-level App Router pitfalls not yet in the corpus"
    extracted: 2026-07-20
  see-also: []
```
