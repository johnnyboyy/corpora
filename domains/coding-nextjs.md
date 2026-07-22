# Domain: coding-nextjs

Next.js-specific code patterns — App Router behavior, server/client component boundaries,
routing conventions. Declared by the coder lens when `framework: nextjs`. Projects on other
frameworks (Expo Router, Vite, etc.) do not load this domain. Audit metadata lives in
`domains/audit.md`, loaded only at ratify/retrospective time.

```yaml
last-retrospective: none

principles:

- id: suspense-not-needed-for-sync-client-components
  rule: "Do not wrap a client component in Suspense on the server side when its data is synchronously available and the component manages its own loading state internally."
  condition: "When a Next.js server component passes synchronously-fetched data to a client component that already handles skeleton/loading state (e.g., via a useHydration pattern)."
  reason: "Suspense around a non-suspending client component is a no-op for loading UX, but in Next.js App Router it affects how the page is cached and restored during back navigation — producing intermittent routing anomalies where back sends the user to an unexpected page."

- id: view-transition-scope-at-page-slot-not-layout
  rule: "Apply view transition wrappers and route-keying to the page content slot ({children}) inside the layout, never to the layout element itself or any ancestor of persistent components."
  condition: "When adding route-change animations to a Next.js App Router project that has or will have persistent state (audio player, media session) mounted in a layout."
  reason: "A key prop or transition wrapper on the layout element causes React to treat it as a new instance on every navigation, unmounting and remounting any persistent components and destroying their state."

killed:
```
