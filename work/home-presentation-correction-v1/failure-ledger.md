# Home/presentation correction — user findings and failure ledger

## User inspection takes priority

The user personally inspected the shell: overall appearance and activity shells look great; the activity-page left navigation works fantastically and is now USER INSPECTION — WORKING WELL / REGRESSION-PROTECTED BEHAVIOUR. Empty educational content is expected. Preserve this successful rail, exact names/order/materials/images/selected state and background relationship.

## UF01 — Home presentation fit failed the user's intended requirement

**TEST FAILURE — USER DISCOVERED.** Expected: complete primary Home selection at 1920x1080 without ordinary document scrolling. Actual: prior document was 1190px high, requiring110px scrolling. Cause: fixed scene/name slots and generous transparent lettering gutters plus row/top/bottom gaps. The earlier automated test asserted reachability through scrolling, not viewport fit; its PASS did not establish presentation acceptance. Components: Home-only CSS and the previous acceptance test. Proposed correction: preserve title650x215 at y65, original scene178px and440px lettering display; overlap only existing transparent name gutters by12px at top/bottom, reduce Home row gaps26->10 and top grid margin28->12 at suitable wide/high viewports. Estimated height1070px. No artwork/source/title/nav change. Actual content bounds, focus outlines and every Home choice must be tested inside the viewport. Prevention: use document-height and all-content-bound checks, not a reachability substitute.

## UF02 — Home Activities perceived as scrolling toward content

User finding: activating Activities feels like moving/scrolling toward the activity section, contrary to intended destination navigation. Code inspection: it is already a button toggling a fixed destination drawer, with no section anchor/scroll-to-section handler. The hidden/inert main still retains its tall page layout and background document scrolling is not suspended; ordinary focus is also unguarded. Browser measurements are required before attributing the actual movement. Proposed correction: preserve the existing destination drawer and exact registry, use preventScroll for open/restoration focus and suspend background page scrolling only while its overlay is open, restore its saved scroll on close; list scrolling must remain usable. No activity permanent-rail geometry/material change. Prevention: test menu activation and wheel/touch background isolation from both top and a scrolled Home position.

## New authorized capability — Presentation Mode

Previous scope had no shared Presentation control/state/fullscreen API. This is a new explicit user requirement. Implement a controller once outside route rendering, retain route/current activity/nav DOM, enter fullscreen only from direct control activation, preserve presentation layout if rejected/unavailable, and provide explicit exit/native-Escape handling. No other content or project. Test real native fullscreen separately from simulated fallback. Title/background/nav imagery remain unchanged. Any protected dependency must be reported before changing it.

## GitHub gate

Only prepare an exact tested candidate/allowlist/exclusion list/commit message after all required local gates pass. No Git mutation, commit/push, remote/Pages change or deployment is authorized before the user's later explicit approval. Existing repository/main/root only. Preserve all local excluded artifacts/history.

## F11 — New Presentation utility overlaps tablet Activities

**TEST FAILURE.** Test: normal-run-1 tablet768x1024 activity navigation/open-last/history checks. Expected: Activities remains clickable beside the new mode control. Actual: Playwright reports presentation-toggle intercepting its pointer events; the tablet tests time out. Root cause: `.activity-view .presentation-controls` inherited desktop right16 placement even though tablet top navigation becomes visible. File: `src/styles.css` new utility selector. Proposed minimum correction recorded before application: centre ONLY the new utility control at601-900px widths, between existing Home and Activities; retain narrow<=600 footer/header placement. No protected source/material/left-rail geometry changes. Regression: full six-viewport normal/presentation tests, tablet hit-testing, allnine routes/selected states/controls and baseline rail comparison. Prevention: new site-level utilities must be hit-tested in both Home and activity responsive states, not just Home.

## Read-only external lookup limitation

The web adapter could not access GitHub repository/Pages API URLs or fetch the public repository page. This is a tool-access limitation, not evidence of a Git connection failure. No Git mutation/network configuration change occurred. Use a read-only GitHub connector if available; do not invent authentication/Pages configuration claims.

## F12 — Additional drawer-input test assumptions

**TEST FAILURE.** `drawer-input-run-1` produced3 PASS/3 FAIL, no browser or request errors. The projector assertion used Node strict equality, which distinguishes JavaScript positive and negative zero even after numeric parsing. Desktop and tablet assertions required an inner scrollbar even though all nine rows already fit their list. Laptop real-wheel scrolling and both mobile wheel/emulated-swipe checks passed. Files: this task's `test_drawer_input.cjs` only. Proposed correction recorded before editing: compare offsets using numeric `===`, which treats both zero signs equally; if list content exceeds its viewport require wheel movement, otherwise require zero inner scroll and all rows to fit. Preserve the failed JSON. No runtime, artwork or geometry correction is justified. Prevention: apply the already identified zero-value lesson to every new audit and derive scrolling expectations from measured content capacity. Rerun only this6-case input supplement after correcting its assertions.

## F13 — Activity-rail screenshot pixel comparison (investigating)

**TEST FAILURE.** `rail-pixel-comparison.json` records7 exact matches and11 differences across18 same-size rail screenshots,172028 changed pixels in total. Expected: equivalent direct-load rail screenshots remain identical. Geometry, name/order/image-source/state tests pass, but these pixel differences must be explained before a readiness claim. Files: baseline `before-rail-*` versus `presentation-run-2/after-rail-1920-*` and `presentation-run-3-laptop-baseline/after-rail-1366-*`. No runtime correction, asset edit or replacement is justified yet. Proposed next step: inspect difference locations and compare screenshot loading/focus/context conditions; distinguish a real rail regression from non-equivalent audit state. Preserve both originals and comparison. Protected effects: none; no authorized design change. Prevention: separate geometry, source-byte and rendered-pixel claims and prove each on equivalent loaded states.

### F13 disposition — controlled original-source replay

Verified original app/styles source hashes, intercepted them in browser memory only, and captured original/current under the same Edge/context/reduced-motion/interaction/viewport sequence into a new folder.18/18 contemporaneous original/current rail pairs have ZERO changed pixels; geometry, selection, list position, sources/materials/DPR match. Repeated original versus archived original is17/18 exact, with the remaining original-vs-original difference at most2/255 channel levels, demonstrating rendering variation without runtime changes. The precise internal compositor mechanism remains an inference. Final strict18-pair evidence is `rail-final-comparison.json`; no tolerance was substituted for the original/current pixel check. All failed original screenshots/results remain preserved. No source/artwork/rail correction was applied.

### Additional audit-only lookup/preflight lessons

The root guessed `rail-replay-v2` before listing the actual directory, producing a read-only missing-directory lookup. Inventory then identified `rail-rendering-replay-v2`. This repeats the earlier inventory lesson and is recorded instead of hidden; no file changed. Do not guess audit filenames/directory names.

Replay preflight initially compared normalized snapshot strings with raw-byte hashes. Python read_text had converted only the unchanged registry's CRLF to LF; source app/styles were already byte-exact. Exact CRLF reconstruction in verification memory reproduced the registry's original SHA256; nothing on disk was rewritten. The empty first replay folder is preserved. Prevention: raw-byte hashing and text newline normalization are different operations; prove exact reconstruction before replaying archived source.

### Final disposition

Actual runtimeF11: corrected utility tablet placement, full normal70 and Presentation64 pass. HarnessF12: scoped input rerun6PASS,0errors/requests. All earlier corrected tests and their original failures remain recorded. Protected/source verification20/20,561pre-existing files retained,zero existing image changes. No staging/commit/push/deployment is authorized or performed.
