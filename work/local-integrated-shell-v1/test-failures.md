# First local integrated shell — failure ledger

## F01 — Transparent overlay drawer competes with underlying content (pending approval)

**TEST FAILURE**. Test: visually inspect the open Home and activity drawer at projector 1920x1080, desktop 1600x900, laptop 1366x768, tablet 768x1024 and mobile 390x844/320x812. Expected: clear navigation labels, protected visual materials, no competing page text. Actual: at 390x844 the activity heading/content is readable through the glass and collides with navigation; Home scenes/name lettering also compete; at 1366x768 the dropdown overlaps part of the title. Evidence: `initial-mobile-activity-navigation.png`, `initial-mobile-home-open.png`, `initial-laptop-home-open.png`; the original screenshots remain preserved.

Cause: the drawer is an overlay with intentionally transparent panes. `main.inert` blocks input but does not affect rendering. Components: `src/app.js` overlay state and `src/styles.css`. Proposed minimum correction: temporarily conceal main content only during the overlay state, preserving its layout/scroll position and keeping the global background/navigation visible. No opaque background or artwork change; the permanent desktop activity rail stays unchanged. Protected effect: the protected Home title would be temporarily concealed, so a DEPENDENCY CONFLICT was reported and explicit user approval requested before changing the display state. No correction applied yet. Regression requirements: closed-state title bounds/source, background visibility, all route transitions, close/Escape/focus restoration and top/bottom scroll reachability. Prevention: an inert transparent overlay requires separate visual overlap testing; input isolation alone is insufficient.

## F02 — Initial local asset request refused (diagnosing)

**TEST FAILURE**. Test: first projector browser load. Expected: every approved image loads without network/console errors. Actual: one Door to Darkness 38px thumbnail request was refused; initial-browser-inspection.json records its unloaded image and `net::ERR_CONNECTION_REFUSED`. Components: local preview server/request concurrency, not the protected asset. Proposed correction pending server-log diagnosis. Protected source will not be changed or replaced. Do not hide this failed initial attempt in later results.

## F03 — Browser favicon request returns 404 (diagnosing)

**TEST FAILURE**. Test: first browser load console. Expected: no missing asset requests. Actual: a 404 resource message accompanies the first projector load. Likely automatic favicon request; confirm server log before correction. Proposed correction, if confirmed: explicit empty favicon declaration in index.html, avoiding a request for nonexistent artwork. No protected asset change, no generated icon. Prevention: account for automatic browser requests as well as authored paths.

## Correction authorization and actions

F01: the user explicitly answered **Approve temporary content concealment**. Applied `.is-menu-open main { visibility: hidden; }` only for the overlay drawer state. No change to background, title geometry/source, frame materials or permanent rail. Closed state/layout stays intact. This is approved functional display behaviour, not asset modification. Retest pending.

F02: server log contains no failed thumbnail HTTP response, consistent with the browser's refused connection occurring before the handler accepted it. The default server queue of 5 is a likely cause during the first concurrent asset load; no missing source file exists. Applied a 128-connection queue to the local-only preview server. Cause is an inference until repeat clean-load tests; protected/runtime artwork untouched. Retest pending.

F03: server log confirmed `GET /favicon.ico` 404. Added `<link rel="icon" href="data:,">` to index.html so no nonexistent favicon asset is requested. No new artwork. Retest pending.

## F04 — Test runner whitespace assertion and cascading state (recorded before harness correction)

**TEST FAILURE**. Test: run-1 expected the empty activity panel to render with precisely one newline between its heading and paragraph. Actual: Chromium `innerText` includes blank-line formatting, causing the no-invented-content assertion to fail despite matching words. Later tests inherited the early-aborted route, producing misleading selected-state/open-focus/missing-card failures. Components: `test_shell.cjs`, not protected artwork or website content. The run was interrupted and its screenshots retained. Proposed correction: normalize whitespace when comparing the exact placeholder wording; give each interaction test an explicit independent starting state; persist each test result incrementally. Verify accessibility issues separately rather than accepting cascade messages as website failures. No protected design effect. Prevention: assert meaningful content, not browser formatting, and isolate test states.

The interrupted run reached projector, desktop, laptop, tablet and part of mobile. At each viewport the whitespace assertion aborted both destination loops and history tests; subsequent Hotel-selected/open-focus/missing-card assertions were invalidated by the starting state. No pass claim is made for these interrupted chains. Raw browser wording was independently confirmed in `accessibility-probe.json`: `Activity content area\n\nContent and interactions will be developed after separate approval.`

## F05 — Home route heading focus

**TEST FAILURE**. Test: separate `probe_accessibility.cjs`, activity -> Home using the real Home link. Expected: router focuses Home h1 for keyboard/screen-reader orientation. Actual: document body became active; the heading was not programmatically focusable. Evidence: `accessibility-probe.json`. Cause: Home h1 lacked the `tabindex="-1"` already present on activity headings. File: `src/app.js`. Proposed correction: add that attribute only, preserving title source, scale, placement and artwork. No protected visual effect. Prevention: verify focus on every route class, not just activity headings. Retest Home focus and all keyboard flows.

## F06 — Skip link mistakenly routed as a destination

**TEST FAILURE**. Test: focus Skip to content, press Enter on Home. Expected: main content focused, Home route unchanged. Actual: hash became `#main-content`, router rendered Destination not found. Evidence: `accessibility-probe.json`. Cause: browser anchor fragment and SPA route shared the hash without a skip-click handler. Files: `index.html` skip anchor and `src/app.js` routing/input integration. Proposed correction: prevent default only for the skip link; close any overlay and focus the existing main element without changing the route. No protected artwork/design change. Prevention: test utility anchors alongside destination links; keyboard access is behaviour, not a screenshot claim. Retest skip on Home and a destination.

## F07 — Malformed encoded destination crashes route rendering

**TEST FAILURE**. Test: direct `#/activities/%zz` in `probe_invalid_route.cjs`. Expected: safe unknown-destination shell. Actual: `URIError: URI malformed`, no heading rendered. Evidence: `invalid-route-probe.json`. Cause: unguarded `decodeURIComponent` in route lookup. File: `src/app.js`. Proposed correction: catch only invalid decoding and use the existing unknown-destination state. No protected artwork/design or educational content change. Prevention: validate external URL fragments before lookup; regression includes unknown/malformed routes and valid direct/reloaded routes.

## F08 — Test URL matcher ignored diagnostic query strings

**TEST FAILURE**. Test: run-2 isolated keyboard/Home-focus tests. Expected: recognize `#/activities/...` after activation. Actual: Playwright's `**/#/activities/...` glob timed out on a URL containing `?test=keyboard` or `?test=focus` before its fragment. The isolated tests had introduced those queries to force a fresh document. Other destination tests without queries passed. Components: test runner route wait, not website router; run-2 partial results/screenshots are preserved. Proposed correction: compare `URL.hash` directly, including Home waits, so route assertions are independent of query/prefix. No protected design/runtime change. Prevention: tests for a hash router must compare the fragment rather than assuming the entire URL shape. The interrupted run cannot be called a completed pass.

## F09 — Mobile overlay focus changes underlying page scroll (diagnosing)

**TEST FAILURE**. Test: Home scrolled to Words of the Feast at 390x844, open Activities with emulated touch, tap outside to close. Expected: the underlying Home scroll position is retained. Actual: scrollY differs after close (`supplemental/results.json` first attempt preserved). Likely cause: default focus scrolling on the fixed drawer's Close/toggle controls; `visibility:hidden` itself retains layout. File: `src/app.js` overlay focus handling. Proposed minimum correction after tracing: use preventScroll for opening/restoration focus, preserving list scrolling separately. No protected artwork/geometry effect, consistent with the explicitly approved temporary concealment/restoration. Prevention: test overlays opened from a scrolled page, not only from its top. Probe and regression must cover Close/outside/Escape.

## F10 — Expanded registry selected row lies below the visible rail (diagnosing)

**TEST FAILURE**. Test: intercept only the browser's registry response with six clearly test-only entries (15 total), select entry 15 from Home menu, then inspect the activity rail. Expected: the selected entry is brought into view. Actual: selection is correct but its row is below the visible rail after geometry switches from Home dropdown to activity rail. Existing production registry/files remain nine and unchanged. Evidence: `supplemental/results.json`. Cause: list height/row sizes change on route transition without aligning the selected row. File: `src/app.js` updateNavigation. Proposed minimum correction: scroll only the navigation list enough to show its selected row when the rail/drawer is displayed. Do not change rows, images, typography or page content. No protected asset/design change. Prevention: capacity testing must include geometry transitions and selected-item visibility, not merely counting generated links. Retest all nine and the isolated 15-entry fixture.

F09 diagnosis corrected: `scroll-probe-v2.json` shows scrollY 918 before/open, then 0 and `#/activities/words-of-the-feast` after the outside tap. The cause is click-through, not focus scrolling. The document pointerdown handler removed inert/visibility before the subsequent click, which activated a newly exposed scene. The first probe consequently timed out trying to find a Home card after the unexpected route; its script is preserved as `probe_scroll_v1.cjs`. Proposed correction revised before application: close on the completed document click, while its event target is still the inert-page/body target; no premature pointerdown reactivation. Retest outside touch, Close, Escape, route and scroll preservation, and cumulative navigation. This evidence supersedes the earlier likely-focus hypothesis; do not apply an unrelated speculative focus correction.

F10 correction: align the selected row by changing only destination-list.scrollTop after its visible layout is established. This must never scroll the document or alter rail/drawer geometry.

## Final regression disposition

Final cumulative evidence: `run-4/results.json` — 70 PASS, 0 FAIL, no console/runtime/network errors. Supplemental evidence: `supplemental-2/results.json` — 4 PASS, 0 FAIL, no page errors. Earlier failure evidence/partial runs remain preserved.

- F01: locally corrected with explicit user-approved overlay concealment. All six viewport open/close screenshots and exact closed-state title restoration pass. Live/physical-device visual approval remains separate.
- F02: no refused assets in final runs. Enlarged local preview queue retained. The queue diagnosis remains a likely cause, not independently proven; the source file was never missing or modified.
- F03: explicit empty favicon prevents the automatic missing-resource request; final console/network checks pass.
- F04: normalized exact placeholder words and isolated test states pass all 54 Home-scene destination/return subcases and all nine-name navigation loops at six viewports. It was a harness error, not invented lesson content.
- F05: Home/each destination route heading receives focus; all six viewport keyboard checks pass.
- F06: Home and activity skip links focus main and retain the route; no unintended unknown-destination transition.
- F07: malformed fragment produces the existing safe unknown-destination shell without URIError; all valid prefix/direct/reload/history routes pass.
- F08: query-independent hash matching passes keyboard and Home-focus checks; it was a test matcher error.
- F09: completed-click outside closing prevents click-through. At 390x844, Close/outside/Escape retain scrollY 918 and Home, with focus restoration. The final six-viewport navigation regression also passes. No speculative focus-scrolling redesign was applied.
- F10: selected row is shown by list-only scrolling. The browser-intercepted 15-entry fixture and final nine-entry route/scroll regressions pass; production registry remains nine. No new activity artwork or actual future destination was created.

All 20 protected asset hashes still match. Every pre-existing image/review/rendering script remains byte-for-byte unchanged. Tests concern the locally implemented shell only; they do not establish activity/game functionality, deployment success, physical touch-device behaviour or user approval.
