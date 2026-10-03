# Presentation audit history

Recorded on 2026-10-02. This audit modifies no runtime files, protected imagery or Git state. Runtime remained frozen during the presentation runs.

## Read-only lookup mistake

- Expected: read the previous browser-testing helper.
- Actual: a guessed `test_local_shell.cjs` filename did not exist.
- Cause: a filename was assumed before checking the inventory.
- Correction: read the listed `test_normal.cjs` and `inspect_before.cjs` instead.
- Prevention: inventory actual filenames before reading historical helpers.
- Effect: no source, image or repository mutation.

## Preserved presentation-run-1: 53 PASS / 8 FAIL

The original `presentation-run-1/results.json`, incremental results and screenshots remain preserved. Its eight failures were test-harness problems, not confirmed application failures. All were reported to the parent agent before correcting the harness. No runtime correction was made in response to them.

### Zero-offset CSS serialization

- Expected: drawer body top equals `-0px` when opening at scrollY0.
- Actual: the CSSOM serializes this value as `0px`; document offset remained zero and route remained Home.
- Cause: literal string comparison rather than numeric comparison.
- Correction: compare `parseFloat(top)` with the negative original offset.
- Prevention: compare numeric CSS values numerically.

### Non-equivalent rail screenshot baseline

- Expected: the clicked Build the Haunted Banquet row would retain the same list scroll offset as the archived direct-load baseline.
- Actual: rail geometry matched exactly, but Playwright's click auto-centering had scrolled the list to180; the archived direct-load baseline used90.
- Cause: comparing different navigation histories. The test exercised link clicking before comparing against a direct-load screenshot.
- Correction: after verifying mode state on the active route, reload that exact route to reproduce the archived baseline's initial state before measuring/saving rail evidence.
- Prevention: compare screenshots/scroll positions only from equivalent starting states. Link navigation is tested separately.

### Two cascading drawer-test precondition failures

- Expected: the following independent drawer tests started on Home.
- Actual: the failed aggregate baseline test had left the laptop on an activity route with a permanent rail; a modal-only focus assertion and overlay scroll-lock assertion were therefore inapplicable.
- Cause: later tests relied on cleanup at the end of an earlier aggregate test.
- Correction: explicitly load Home before each independent drawer test.
- Prevention: give each independent test its own required starting state instead of relying on earlier success.

### Three fullscreen fixtures and aggregate console audit

- Expected: absent, denied and delayed fullscreen APIs were installed before exercising fallback behavior.
- Actual: all three fixtures attempted to define a method on `document.documentElement` before the DOM element existed. Three fixture TypeErrors occurred and native fullscreen remained available; the three fallback assertions and aggregate console audit failed.
- Cause: an early initialization fixture targeted a DOM node that was not yet present.
- Correction: override `Element.prototype.requestFullscreen`, which exists at initialization, and explicitly verify the fixture method/type before interaction.
- Prevention: validate test fixture installation before interpreting the application response.

## Coverage distinctions

## Preserved presentation-run-2 baseline setup refinement

The laptop Build rail comparison still retained180 after calling `page.goto` with its unchanged fragment URL. A separate read-only browser probe confirmed: fresh direct load90; setting180 then same-URL goto180; explicit page.reload90. The initial harness correction had not forced a new document. Correct the harness to use reload before baseline comparison and rerun the affected laptop aggregate only, because runtime is unchanged. Prevention: verify whether a navigation actually creates a new document when a screenshot comparison depends on reset state. Preserve run2 evidence; do not classify this as a runtime navigation regression.

## Browser-memory replay source-verification preflight

The first replay preflight stopped before opening a browser because the normalized `source_before` string for `src/activities.js` did not match its raw-file hash. The snapshot used Python text reading, which normalized original CRLF newlines toLF. The other three saved sources matched asLF. A read-only LF/CRLF hash probe established that restoring CRLF in the registry string exactly reproduces its recorded raw-file hash. The corrected audit verifies an exact per-file reconstruction before serving original app/styles in browser memory; it does not write or repair any runtime source. Preserve the empty `rail-rendering-replay-v1` attempt and use a new v2 output folder. Prevention: distinguish text-normalized snapshots from raw bytes during hash verification and require an exact hash match before replaying a baseline.

## Strict rail screenshot mismatch investigation: controlled replay

Root's initial `rail-pixel-comparison.json` found7 exact matches and11 mismatches. Differences were at most1 channel value at projector size and2 at laptop size, while geometry and imagery looked unchanged. This original failed comparison remains preserved.

`rail-rendering-replay-v2/browser-evidence.json` verifies four pre-change source hashes and captures the original app/styles served only in browser memory, then the current runtime, using identical browser options, reduced-motion, interaction sequence and viewport progression. No runtime sources or original images were rewritten.

Results in `rail-rendering-replay-v2/comparison-results.json`:

- All18 contemporaneous original/current rail pairs have **zero changed pixels**. Geometry, selection, list scroll, image sources, material URLs andDPR also match.
- Comparing the replayed original against the archived original gives17 exact matches and one laptop Echoes mismatch:27,779 pixels with maximum channel difference2. Rendering variation therefore occurs even when the original source is replayed.
- Zero console/runtime errors and zero failed requests occurred during the replay.

The evidence establishes no activity-rail source/design regression. Browser raster/compositor rounding related to rendering history is the supported explanation for the earlier1–2-channel variations; the precise internal GPU rounding mechanism is not independently proven. Do not claim all archived/screenshots are byte- or pixel-identical. The protected asset byte hashes are verified separately by the root audit.

- Native fullscreen is observed through actual `document.fullscreenElement === document.documentElement`, not inferred from the presentation CSS class.
- Keyboard, mouse and emulated touch are local installed-Edge browser tests. They are not physical-device or projector tests.
- All six viewports test wheel scrolling outside the open drawer, unchanged route, body lock and exact restoration of the pre-open document scroll offset.
- Inner-list final-entry reachability and focus scrolling are tested; this runner does not separately dispatch wheel inside the navigation list.
- The delayed promise fixture exercises rapid enter/exit/re-enter without an actual native fullscreen element. It establishes stale-promise state handling, not physical browser-window timing behavior.
- The preserved failed run is not used as final acceptance evidence. The separately saved corrected run is the regression evidence.
