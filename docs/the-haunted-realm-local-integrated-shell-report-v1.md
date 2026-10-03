# The Haunted Realm — first local integrated shell report

**Status: IMPLEMENTED / LOCALLY TESTED / AWAITING USER INSPECTION. Not LIVE, not USER VERIFIED and not a protected implementation.**

[Open the local preview](http://127.0.0.1:4173/). The loopback server runs on this computer only; it has not published the website. The preview can also be served with the read-only `work/local-integrated-shell-v1/serve_local.py` helper.

## IMPLEMENTED

Hotel Transylvania is formally APPROVED / PROTECTED — NAVIGATION IMAGE. All nine navigation images are now fully recorded in the shared manifest. Historical failed/artwork-only/corrected reviews remain preserved.

One integrated static website: Home with the existing mist-scene material and title; Home + expandable Activities controls; shared iron/glass navigation; desktop/laptop/projector left rail; mobile/tablet drawer; nine empty destination shells. A single activity registry supplies exact names, routes, order and existing image paths. Hash routing supports direct links/reloads under the existing future Pages subdirectory without server rewrites. No build framework is needed.

All shells contain only their exact heading, Page shell status and the explicitly temporary Activity content area. No lesson, history, quiz, game, restaurant workflow, role-play, login or multiplayer function has been implemented. The main content space is a temporary layout reservation, not an approved final activity design.

The shared background is the exact approved file, displayed as one fixed CSS layer with proportional cover display. Viewport edges can crop the display on differing aspect ratios; the source is unchanged. No competing full-screen black/background layer exists. The title stays upper-centred at y=65 and 650x215 for widths at least 650px. The separately approved proportional display exception is used below 650px, with 16px side margins and no source edit.

The separately approved drawer-open treatment temporarily conceals main content, preserving its layout and scroll position while leaving the village/navigation visible. Closing restores it. Permanent desktop rails leave content visible. Current destination is amber and kept in view by list-only scrolling. Mobile names can wrap in the existing 70px rows, including selected Hotel Transylvania in bold; names are never shortened.

Home uses current v3 name-rest/name-focus PNGs as a temporary existing treatment. Hover/keyboard focus reuses the existing focus lighting; no new artwork or animation of the protected title was introduced. Final lettering is still unresolved.

## FILES CHANGED

**Existing runtime/source files changed: none.** The project had no runtime website before this authorized step.

Four existing documentation files changed:

- [AGENTS.md](C:/Users/DELL/Documents/Codex/2026-09-30/ar/AGENTS.md)
- [docs/the-haunted-realm-development-workflow.md](C:/Users/DELL/Documents/Codex/2026-09-30/ar/docs/the-haunted-realm-development-workflow.md)
- [outputs/the-haunted-realm-navigation-current-design-status.md](C:/Users/DELL/Documents/Codex/2026-09-30/ar/outputs/the-haunted-realm-navigation-current-design-status.md)
- [outputs/the-haunted-realm-navigation-images-approved.json](C:/Users/DELL/Documents/Codex/2026-09-30/ar/outputs/the-haunted-realm-navigation-images-approved.json)

They record current phase/Hotel approval, preserve earlier history and distinguish the newer local-only workflow from older authorization notes.

## FILES CREATED

New website source:

- [index.html](C:/Users/DELL/Documents/Codex/2026-09-30/ar/index.html)
- [src/activities.js](C:/Users/DELL/Documents/Codex/2026-09-30/ar/src/activities.js)
- [src/app.js](C:/Users/DELL/Documents/Codex/2026-09-30/ar/src/app.js)
- [src/styles.css](C:/Users/DELL/Documents/Codex/2026-09-30/ar/src/styles.css)

Nineteen canonical runtime material PNGs under `assets/navigation/` derive from the already-existing protected frame/chain layers and established authoring functions. The source layers and all approved imagery remain untouched. They contain material/state treatment, not new activity imagery. Their precise filenames and source lineage, plus every new approval/audit/test artifact, are separated in [work/local-integrated-shell-v1/file-inventory.md](C:/Users/DELL/Documents/Codex/2026-09-30/ar/work/local-integrated-shell-v1/file-inventory.md). The asset-lineage JSON is provenance documentation, not a browser dependency.

Existing scene, name and 34/38px navigation thumbnail PNGs are referenced directly. Full-page comparison boards, rendering scripts and diagnostic screenshots are not used as the website UI.

## PROTECTED-ASSET VERIFICATION

**20/20 protected hashes pass before and after implementation:** background and original backup; title PNG/reference/original artwork; six navigation references/material layers; all nine 1254x1254 navigation masters. The protected title remains a 650x215 RGBA source.

Of 395 pre-existing files, 391 are byte-for-byte unchanged; only the four intended documentation records changed. No file is missing. Every pre-existing image, review and rendering script is unchanged, including failed Hotel material and the pending Door/Hotel Landing scenes. All 70 exact-case runtime file/asset paths and the 18 approved 34/38px thumbnails pass. Evidence: [work/local-integrated-shell-v1/final-source-audit.json](C:/Users/DELL/Documents/Codex/2026-09-30/ar/work/local-integrated-shell-v1/final-source-audit.json).

## LOCAL TESTS

Actual browser: installed Microsoft Edge (Chromium), headless via bundled Playwright. Mouse clicks/wheel, keyboard Tab/Shift-Tab/Enter/Escape and emulated touchscreen taps/CDP swipes were exercised. Emulated touch does not claim a physical phone/tablet test. Screenshots were inspected for Home, open drawer, last entry and shell boundaries.

| Context | Viewport | Layout/input | Final result |
|---|---|---|---|
| Projector | 1920x1080 | 460px left rail; mouse/wheel and keyboard | 11/11 PASS |
| Desktop | 1600x900 | 430px left rail; mouse/wheel and keyboard | 11/11 PASS |
| Laptop | 1366x768 | 430px left rail; mouse/wheel and keyboard | 11/11 PASS |
| Tablet portrait | 768x1024 | 288px drawer; emulated taps/swipes and keyboard | 11/11 PASS |
| Mobile portrait | 390x844 | 288px drawer; emulated taps/swipes and keyboard | 11/11 PASS |
| Narrow mobile portrait | 320x812 | 288px drawer; emulated taps/swipes and keyboard | 11/11 PASS |

All six contexts checked Home/nine exact names/images/no emoji; title bounds; Home bottom scrolling; open/close visibility/title restoration; all nine Home scene destinations and returns; shared navigation transitions through all nine; selected state/background/content-area bounds/horizontal overflow; last Hotel row/image/name reachability; direct URL/reload/history; keyboard open/trap/last-entry activation; Home heading focus; skip-link behaviour; no console/runtime/network errors.

Four additional routing/responsive cases verified every direct route and reload under `/the-haunted-realm/`; the 649/650px title exception boundary plus laptop/mobile/projector resize transitions; unknown route handling; malformed encoded route handling.

Four supplemental cases verified outside-touch/Close/Escape retain Home and scrollY=918 without click-through; activity skip link; existing focus lettering/reduced motion; registry capacity with 15 entries and selected-row visibility. The six extra entries were browser-only intercepted test fixtures using existing artwork, never saved to production or approved as names/content.

The Home scene grid has three columns on large screens, two on tablet/smaller screens and one on mobile. Its full nine-scene composition needs vertical scrolling, including at 1920x1080; the last scene and complete name were actually reached. This is normal page scrolling, not proof of a separate presentation-mode feature. The mobile drawer and shorter laptop rails scroll independently; no final destination is permanently clipped.

### Every final test case

| Context | Test actually performed | Result |
|---|---|---|
| projector | Home, exact nine names, approved images and no emojis | PASS |
| projector | Home bottom card and document scrolling are reachable | PASS |
| projector | Home drawer only conceals content temporarily; close restores exact title | PASS |
| projector | Every Home scene opens its exact shell and returns Home | PASS |
| projector | Home menu reaches every activity; activity navigation transitions through all nine | PASS |
| projector | Last Hotel entry: actual navigation scroll, complete label and 34/38px image | PASS |
| projector | Direct destination URL, reload, back/forward preserve exact route/current state | PASS |
| projector | Keyboard opens menu, traps focus, reaches final entry and activates it | PASS |
| projector | Home route restores a programmatically focusable heading | PASS |
| projector | Skip link focuses content without changing the Home route | PASS |
| projector | No local console/runtime/network errors | PASS |
| desktop | Home, exact nine names, approved images and no emojis | PASS |
| desktop | Home bottom card and document scrolling are reachable | PASS |
| desktop | Home drawer only conceals content temporarily; close restores exact title | PASS |
| desktop | Every Home scene opens its exact shell and returns Home | PASS |
| desktop | Home menu reaches every activity; activity navigation transitions through all nine | PASS |
| desktop | Last Hotel entry: actual navigation scroll, complete label and 34/38px image | PASS |
| desktop | Direct destination URL, reload, back/forward preserve exact route/current state | PASS |
| desktop | Keyboard opens menu, traps focus, reaches final entry and activates it | PASS |
| desktop | Home route restores a programmatically focusable heading | PASS |
| desktop | Skip link focuses content without changing the Home route | PASS |
| desktop | No local console/runtime/network errors | PASS |
| laptop | Home, exact nine names, approved images and no emojis | PASS |
| laptop | Home bottom card and document scrolling are reachable | PASS |
| laptop | Home drawer only conceals content temporarily; close restores exact title | PASS |
| laptop | Every Home scene opens its exact shell and returns Home | PASS |
| laptop | Home menu reaches every activity; activity navigation transitions through all nine | PASS |
| laptop | Last Hotel entry: actual navigation scroll, complete label and 34/38px image | PASS |
| laptop | Direct destination URL, reload, back/forward preserve exact route/current state | PASS |
| laptop | Keyboard opens menu, traps focus, reaches final entry and activates it | PASS |
| laptop | Home route restores a programmatically focusable heading | PASS |
| laptop | Skip link focuses content without changing the Home route | PASS |
| laptop | No local console/runtime/network errors | PASS |
| tablet | Home, exact nine names, approved images and no emojis | PASS |
| tablet | Home bottom card and document scrolling are reachable | PASS |
| tablet | Home drawer only conceals content temporarily; close restores exact title | PASS |
| tablet | Every Home scene opens its exact shell and returns Home | PASS |
| tablet | Home menu reaches every activity; activity navigation transitions through all nine | PASS |
| tablet | Last Hotel entry: actual navigation scroll, complete label and 34/38px image | PASS |
| tablet | Direct destination URL, reload, back/forward preserve exact route/current state | PASS |
| tablet | Keyboard opens menu, traps focus, reaches final entry and activates it | PASS |
| tablet | Home route restores a programmatically focusable heading | PASS |
| tablet | Skip link focuses content without changing the Home route | PASS |
| tablet | No local console/runtime/network errors | PASS |
| mobile | Home, exact nine names, approved images and no emojis | PASS |
| mobile | Home bottom card and document scrolling are reachable | PASS |
| mobile | Home drawer only conceals content temporarily; close restores exact title | PASS |
| mobile | Every Home scene opens its exact shell and returns Home | PASS |
| mobile | Home menu reaches every activity; activity navigation transitions through all nine | PASS |
| mobile | Last Hotel entry: actual navigation scroll, complete label and 34/38px image | PASS |
| mobile | Direct destination URL, reload, back/forward preserve exact route/current state | PASS |
| mobile | Keyboard opens menu, traps focus, reaches final entry and activates it | PASS |
| mobile | Home route restores a programmatically focusable heading | PASS |
| mobile | Skip link focuses content without changing the Home route | PASS |
| mobile | No local console/runtime/network errors | PASS |
| mobile-narrow | Home, exact nine names, approved images and no emojis | PASS |
| mobile-narrow | Home bottom card and document scrolling are reachable | PASS |
| mobile-narrow | Home drawer only conceals content temporarily; close restores exact title | PASS |
| mobile-narrow | Every Home scene opens its exact shell and returns Home | PASS |
| mobile-narrow | Home menu reaches every activity; activity navigation transitions through all nine | PASS |
| mobile-narrow | Last Hotel entry: actual navigation scroll, complete label and 34/38px image | PASS |
| mobile-narrow | Direct destination URL, reload, back/forward preserve exact route/current state | PASS |
| mobile-narrow | Keyboard opens menu, traps focus, reaches final entry and activates it | PASS |
| mobile-narrow | Home route restores a programmatically focusable heading | PASS |
| mobile-narrow | Skip link focuses content without changing the Home route | PASS |
| mobile-narrow | No local console/runtime/network errors | PASS |
| additional-routing | Pages project-prefix entry/assets and every direct route reload | PASS |
| additional-routing | Title exception boundary at 649 and 650px; resize preserves routing | PASS |
| additional-routing | Unknown route handled without incorrect activity | PASS |
| additional-routing | Malformed encoded route handled without runtime exception | PASS |
| Supplemental | Mobile overlay touch close/outside close, page scroll state restored | PASS |
| Supplemental | Activity skip link retains exact route and focuses main | PASS |
| Supplemental | Hover/focus reuses existing focus lettering, reduced-motion preference honored | PASS |
| Supplemental | Registry expands to 15 entries/routes without changing production files | PASS |

Raw final evidence: [work/local-integrated-shell-v1/run-4/results.json](C:/Users/DELL/Documents/Codex/2026-09-30/ar/work/local-integrated-shell-v1/run-4/results.json) and [work/local-integrated-shell-v1/supplemental-2/results.json](C:/Users/DELL/Documents/Codex/2026-09-30/ar/work/local-integrated-shell-v1/supplemental-2/results.json). Viewport top/bottom/open-drawer/current-shell screenshots are preserved beside the results.

## PASSED

**74 final cases PASS; 0 final FAIL.** The matrix includes repeated nine-destination subcases. Final matrix console errors: 0; runtime errors: 0; failed/404 requests: 0. Protected-source/hash/case audits also pass. These are shell tests, not a claim that activities/games work.

## FAILED

Failures were recorded before correction, with expected/actual/cause/files/proposal/protection effect and prevention. The complete ledger is [work/local-integrated-shell-v1/test-failures.md](C:/Users/DELL/Documents/Codex/2026-09-30/ar/work/local-integrated-shell-v1/test-failures.md). Initial screenshots/probes, interrupted/partial test runs and the failed supplemental result remain preserved.

| ID | Initial failure and cause | Correction/final disposition |
|---|---|---|
| F01 | Transparent drawer showed page text/title behind labels. | Explicit user-approved temporary main-content concealment; all six closed-title restoration/visual checks pass. |
| F02 | First projector load refused one thumbnail request. | Local server queue increased from default 5 to 128; final requests clean. Queue saturation is a likely diagnosis, not independently proven. Asset never missing/modified. |
| F03 | Automatic favicon.ico request returned 404. | Confirmed by server log; explicit empty favicon declaration prevents the request. No artwork created. |
| F04 | Test compared literal newline formatting; later tests inherited an aborted route. | Normalize exact words, isolate start states and persist partial results. Harness issue, no invented content. |
| F05 | Returning Home did not focus its heading. | Add tabindex=-1 to Home h1; route-focus checks pass with title unchanged. |
| F06 | Skip anchor fragment was mistaken for a destination route. | Prevent default only on skip; focus main without changing hash. Home/activity checks pass. |
| F07 | Invalid percent-encoded hash threw URIError. | Safe decoding falls back to the existing unknown-destination shell; valid and malformed routes pass. |
| F08 | Test URL glob omitted diagnostic query strings. | Compare URL.hash instead; isolated keyboard/history checks pass. Harness issue. |
| F09 | Outside touch closed on pointerdown, allowing click-through to a scene and resetting scroll. | Close on completed click; outside/Close/Escape retain Home and scroll. Earlier focus-scrolling hypothesis was disproved, not silently applied. |
| F10 | 15-entry selected row moved below the visible rail after route geometry changed. | List-only alignment of selected row; 15-entry fixture and nine-entry regression pass. No geometry/artwork change. |

## REGRESSION RESULTS

All local Home, navigation and nine-shell tests were rerun cumulatively after the final runtime changes. Previously corrected mobile last-entry visibility, exact Hotel name/thumbnail sizes, all canonical names, UTF-8 manifest reads, route focus/skip/unknown handling, background continuity, title exceptions, page/drawer scrolling and the outside-tap bug were checked. The latest static reviews and all rejected/failed history remain unchanged.

No teacher/student session architecture, educational content, multiplayer, emoji, new artwork, black replacement background or separate disconnected activity site was introduced. The capacity fixture was removed automatically with its browser context; runtime remains the shared nine-item registry.

## STILL REQUIRES LIVE VALIDATION

Explicit push/deployment approval; remote commit/file verification; actual Pages build/publish/MIME/path/cache checks; live URL routing and responsive regression; personal live inspection. Physical classroom projector legibility, real phone/tablet touch/scroll/browser chrome/orientation and Safari/iOS/Firefox remain untested. This task tested Edge with concrete emulated viewports, not those devices/engines. Later activities and presentation behaviour require their own implementation/tests and cumulative regressions.

## UNRESOLVED ITEMS

Final Landing name lettering (cursed stone/spectral/antique metal) is unresolved; current v3 PNGs are temporary/current material. Door to Darkness large-scene departure/bill cue remains small. Hotel Transylvania large-scene wolf-headed guest and architecture/furniture/lighting observations remain pending. No scene correction or false resolution was made.

Rail/drawer geometry remains provisional until live validation and personal approval; local passes do not protect it automatically. Mobile transparent-drawer text collision was addressed locally only through the separately approved display treatment; live visual inspection still matters. Final complete Landing design/implementation approval, future content, games/session model and later activities are outside this step.

## GITHUB STATUS

No commit, push, fetch, pull, branch switch, remote change, Pages configuration change, visibility change or deployment occurred. Read-only local checks show branch main, origin `https://github.com/NSAdyad/the-haunted-realm.git`, HEAD `125798046dfc25e5b97e331ffc86112468c0f20d` unchanged. Remote/Pages were not re-inspected or modified during this local task; no new claim is made about their current external state. Local source/assets/documentation remain uncommitted.

## CURRENT PROJECT STATE

**Hotel navigation image set: APPROVED / PROTECTED (nine).**

**Integrated website shell: IMPLEMENTED + LOCALLY TESTED; awaiting personal inspection and explicit next instruction.**

**Live deployment: NOT PERFORMED. User verification/final implementation protection: NOT GRANTED.**

Work stops here. Echoes of the Past content and all other activity/game work have not started.
