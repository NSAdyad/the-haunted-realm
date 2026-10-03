from pathlib import Path
import json
import hashlib
import re

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
def read(name):return json.loads((WORK/name).read_text(encoding='utf-8'))
normal=read('normal-run-2/results.json')
presentation=read('presentation-final-results.json')
support=read('support-run-1/results.json')
inputs=read('drawer-input-run-2/results.json')
verification=read('protected-and-source-verification.json')
rail=read('rail-final-comparison.json')
assert all(t['status']=='PASS' for data in [normal,presentation,support,inputs,rail] for t in data['tests'])
assert all(not data.get(key) for data in [normal,presentation,support,inputs,rail] for key in ['errors','badRequests'])
assert verification['all_protected_unchanged'] and not verification['existing_image_changes']
for name,expected in presentation['runtimeHashes'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest().upper()==expected
browser_count=sum(len(data['tests']) for data in [normal,presentation,support,inputs])
protected=verification['protected_count']
hash_rows='\n'.join(f'| `{name}` | `{value}` |' for name,value in verification['protected_hashes_after'].items())
viewport_rows=[]
for label,width,height in [('projector',1920,1080),('desktop',1600,900),('laptop',1366,768),('tablet',768,1024),('mobile',390,844),('mobile-narrow',320,812)]:
    entry=next(t for t in presentation['tests'] if t['viewport']==label and t['test']=='Normal Home bounds, exact names and protected title')
    measured=entry['evidence']['documentHeight']
    viewport_rows.append(f'| {width}×{height} | PASS | PASS; native fullscreen observed | {measured}px |')
scripts='\n'.join(f'- `{p.relative_to(ROOT).as_posix()}`' for p in sorted(WORK.iterdir()) if p.suffix in ['.py','.cjs'])
report=f'''# The Haunted Realm — Home and Presentation correction report

2026-10-02. **READY FOR CONTROLLED GITHUB DEPLOYMENT — AWAITING USER APPROVAL.**

The same integrated shell is corrected and locally tested. No staging, commit, push, deployment, Pages-setting change or repository change was performed. The latest corrections remain awaiting personal inspection; this report does not grant final visual approval. Activity educational content remains intentionally empty.

## USER INSPECTION FINDINGS

Your inspection found that the website looked great, the atmosphere worked and the activity shells looked good. You specifically found the activity-page left navigation fantastic. That behavior is recorded as **USER INSPECTION — WORKING WELL / REGRESSION-PROTECTED BEHAVIOUR**.

You also found unwanted Home document scrolling, an Activities action that felt like movement towards the activity section, and a need for a shared classroom Presentation Mode. Empty activity content was expected. Your inspection supersedes the earlier weaker automated reachability assertion.

## ROOT CAUSE

At1920×1080 the previous Home document was1190px high:110px more than the viewport. The earlier test checked whether scrolling could reach the last card, rather than checking that the entire primary selection fitted. Title215px, scene spaces178px and lettering80px (104px for the two-line Banquet name) combined with top/row/bottom spacing created the excess.

Activities already opened the destination drawer: opening it did not change the route or scroll the document in the baseline probe. It was not coded as a section anchor. However, the open overlay did not lock the document: wheeling outside it moved Home from scrollY0 to110, and closing retained110. That provides a concrete source of apparent page movement; it does not prove exactly which gesture you used. No shared Presentation Mode existed.

## IMPLEMENTED CORRECTIONS

- At wide viewports at least1200px wide and1000px high, Home uses12px top grid spacing instead of28px and10px row gaps instead of26px. Each lettering layer overlaps only its existing transparent top/bottom gutters by12px. Title, scene and lettering assets/sizes are retained. No artwork was cropped, resized or rewritten.
- An overlay drawer now fixes the body at its saved scroll offset, locks background scrolling, and restores the exact offset on close. It preserves the approved temporary concealment/inert content behavior and completed-click outside closing.
- Added one reusable Presentation controller outside route rendering. It requests fullscreen directly from button activation and preserves responsive layout/route/navigation when fullscreen is absent or rejected.
- The new utility sits at upper centre on Home/tablet, upper right beside a permanent activity rail, or lower right on narrow screens with reserved bottom space. While a narrow drawer is open, it moves into the existing header as Present/Exit mode and remains in the focus trap. Its full accessible name remains Presentation mode/Exit presentation.
- Corrected the new tablet utility placement after its first test exposed overlap with Activities. No existing rail geometry rule was changed.
- Recorded inspection, failure, cumulative testing, protected-work and explicit deployment-gate requirements in project documentation.

## PRESERVED SUCCESSFUL WORK

The existing left rail retains430px width on laptop and460px on projector, its position, row materials, chains, typography, exact destination order, approved thumbnails and amber selected state. All nine destination transitions and Home returns pass in both normal and Presentation states. Source assets are byte-for-byte unchanged.

The additional rendered comparison is recorded separately in `work/home-presentation-correction-v1/rail-final-comparison.json`:18/18 contemporaneous verified-original/current rail pairs have zero changed pixels and matching geometry/state/sources/materials. A repeated original versus archived original shows small browser-rendering variation in one pair; no blanket claim of identical screenshots across browser histories is made. Background, title, all existing review images, nine protected navigation masters and all prior rendering scripts remain unchanged. Existing mobile title display scaling and approved temporary overlay concealment remain in place.

## FILES CHANGED

Existing runtime/source changed in this step:

- `src/app.js`: shared mode initialization/placement and drawer background-scroll lock/restoration.
- `src/styles.css`: projector Home spacing, new utility placement and overlay body lock.
- `AGENTS.md`: documentation of your controlling inspection/workflow requirements; this is not a runtime file.

`index.html`, `src/activities.js`, previous runtime material PNGs, all previously existing images/reviews/tests and all existing protected approval records are unchanged relative to this task's baseline. They may still be new/uncommitted from the previous integration step; the deployment inventory distinguishes Git state from this task's changes.

## FILES CREATED

Runtime: `src/presentation.js` only. No new artwork, lesson, game, multiplayer, activity-page content or registry entry was created.

Documentation: `docs/the-haunted-realm-user-inspection-and-presentation-workflow.md` (full instruction), this report, and `outputs/the-haunted-realm-home-presentation-validation-candidate.md`.

New test/audit source files in this task:

{scripts}

Audit artifacts include the immutable before snapshot, original browser measurements/rail captures, preserved failed runs, normal/presentation/support/drawer results, runtime hashes, pixel comparisons, protected/source verification, failure ledger, presentation audit notes and read-only GitHub evidence. Exact included/excluded paths are enumerated in the deployment scope, rather than treating all of `work/` or `outputs/` as disposable. Screenshot archives and excluded material remain safely local.

## PRESENTATION MODE

The control works on Home and every activity route. Mouse click or keyboard activation enters the same site's Presentation state and calls the browser fullscreen API before any awaited work. Native fullscreen was observed in installed Edge at all six viewport sizes. Exit presentation and Escape leave mode; the first Escape in an open drawer closes that drawer according to its established behavior. Native fullscreen departure is synchronized with mode state.

If fullscreen is absent or rejected, the Presentation state stays usable with an explicit exit and accessible status feedback. The same responsive projector fit applies without relying on successful fullscreen. The layout does not hide oversized Home content with overflow clipping. Mode changes do not rebuild navigation, reset the route, duplicate controls, alter artwork or replace the background. Delayed-request tests cover stale-promise state after rapid entry/exit/re-entry; they do not claim real hardware/browser-window race validation.

Fullscreen activation/rejection/event handling follows the [Element.requestFullscreen documentation](https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullscreen) and [fullscreenchange documentation](https://developer.mozilla.org/en-US/docs/Web/API/Document/fullscreenchange_event).

## HOME FIT RESULTS

At1920×1080 in normal and Presentation states:

- Document dimensions:1920×1080; scrollY0. The previous height was1190px.
- Title:650×215 at(635,65), centred and uppermost as approved.
- Nine activity hit regions, scenes and full names fit without ordinary document scrolling or horizontal overflow.
- Scene layout spaces stay178px high; name layers stay440px wide. The lowest full name box ends at1050px, leaving30px before the viewport bottom.
- Home, Activities and mode/exit controls are visible, separate and usable. Wheel scrolling is not needed to reveal a missing primary choice.

Smaller targets retain readable scrolling layouts; fitting all nine full scenes onto a phone was not substituted for readability. The one-screen requirement is met at the specified1920×1080 projector viewport.

## HOME NAVIGATION RESULTS

Activities opens the existing nine-destination navigation drawer with approved realistic identifiers and exact names. It is not a scroll-to-section action. Choosing a destination opens its real integrated shell and sets its current navigation state. Home returns to Home. The opened overlay locks document scrolling while its own list remains independently scrollable when its content exceeds available height. Close, Escape and outside completed-click restore the original position without click-through. The registry remains extensible: a browser-only15-entry fixture passes without changing production files or generating future artwork.

## RESPONSIVE TEST RESULTS

Installed Microsoft Edge/Chromium headless, mouse/keyboard plus emulated touch; these are local browser tests, not physical devices.

| Viewport | Normal regression | Presentation regression | Measured Home document height |
|---|---|---|---:|
{chr(10).join(viewport_rows)}

Final browser acceptance evidence:{browser_count} passing checks, zero unresolved failures:normal70, Presentation64 (a provenance rollup of valid run2 checks and the corrected laptop aggregate), support4, drawer input6. Full original result paths and exact tested source hashes are retained. All six outside-wheel/background-lock tests pass; actual inner-list wheel is tested where overflow exists, and emulated mobile touch swipes scroll that list. Menus that already fit all rows correctly remain unscrolled.

## ACTIVITY-PAGE REGRESSION

All nine shells passed in normal and Presentation states:Echoes of the Past; The Cursed Quest; The Book of Shadows; Fastest Finger First; Words of the Feast; The Phantom Order; Door to Darkness; Build the Haunted Banquet; Hotel Transylvania.

Each opens the exact route/name, keeps the correct amber/current destination and approved navigation image, returns Home, transitions through other destinations, retains the same global background, and reports no routing/runtime error. Content remains the existing empty shell. Presentation mode persists across routes and preserves navigation rather than creating separate websites.

## PREVIOUS-FAILURE REGRESSION

| Prior failure/requirement | Current result |
|---|---|
| F01 transparent drawer/content collision | PASS:approved content concealment only while overlay is open; background/nav visible; title restores |
| F02 refused thumbnail/local queue | PASS:no failed requests; original files unchanged; enlarged local preview queue retained; original queue cause remains an inference |
| F03 favicon404 | PASS:existing empty data favicon retained; no missing favicon request |
| F04 whitespace/cascading fixture state | PASS:meaningful exact placeholder words; independent route starts |
| F05 Home heading focus | PASS:Home and destination headings receive route focus |
| F06 skip link routing | PASS:Home/activity skip targets main without changing route |
| F07 malformed encoded route | PASS:safe unknown shell; no URIError |
| F08 query-sensitive URL matcher | PASS:direct/prefix/query/hash route checks |
| F09 outside-tap click-through | PASS:completed-click closure; exact original scroll/route retained for Close/Escape/outside touch |
| F10 expanded registry/current-row visibility | PASS:15-entry browser fixture, list-only selected alignment, last entry reachable |
| Mobile clipping/last Hotel row | PASS:top/bottom bounds, focus/list scrolling and header mode-control access |
| Protected background/black replacements | PASS:same shared image, no competing full-screen background |
| Inaccessible/overlapping controls | PASS:keyboard trap, focus restoration, mouse/touch and all-six control bounds/hit tests |
| Home projector fit | PASS:all nine primary destinations visible at1920×1080, document1080px |

## PROTECTED-ASSET VERIFICATION

Authoritative merged current manifests/baseline give **{protected}/{protected} matching hashes before and after**, including final Hotel Transylvania navigation approval. No assumption of an outdated count was used. All561 pre-existing files remain present; zero pre-existing image changes. Only app/styles/AGENTS changed among those files.

| Protected file | Verified SHA-256 |
|---|---|
{hash_rows}

Full preservation evidence: `work/home-presentation-correction-v1/protected-and-source-verification.json`.

## CONSOLE / NETWORK / ROUTING

Final accepted local runs report zero console/runtime errors and zero failed/missing requests. All nine direct/reloaded routes, Home, history/back-forward, safe unknown/malformed paths and the `/the-haunted-realm/` Pages-prefix simulation pass. Case-sensitive path/runtime dependency closure is checked again by the deployment preparation gate. These results concern the local candidate; they are not a live Pages deployment claim.

## FAILURES DURING THIS TASK

- User-discovered fit acceptance gap:the previous reachability test passed despite1190px Home. Corrected spacing and added measured one-screen acceptance. Prevention:reachability and fit are separate gates. Final1920 normal/Presentation fit passes.
- User-reported Activities difference:baseline exposed actual background scrolling under an open destination drawer. Corrected only overlay lock/restoration. Prevention:measure route and scroll both during and after overlay interaction. Final six-size lock/restoration passes.
- F11 actual runtime tablet overlap:new mode control intercepted Activities. Corrected only its601–900px position to centre. Prevention:test shared utilities in both Home and activity responsive states. Full normal70 and mode/control regression passes.
- Presentation harness run1:53 pass/8 fail from zero CSS serialization, non-equivalent rail scroll history, two cascading Home preconditions, three uninstalled early fullscreen fixtures and their aggregate console failure. Numeric assertions, isolated Home setup and verified Element.prototype fixtures correct these without runtime changes. Run2:63 pass/1 remaining baseline setup mismatch. A read-only probe proved same-fragment goto retains scroll180 while actual reload restores archived90. The affected all-nine laptop aggregate was rerun after reload; final64-test provenance rollup is all PASS. Prevention:prove fixture installation/new-document state and compare equivalent histories.
- F12 extra drawer-input harness:3 pass/3 fail from strict negative-zero equality and expecting scrollbars when all rows fitted. Corrected numeric equality/content-capacity expectations; preserved run1. Final input6 passes. Prevention:apply earlier numeric lessons to new audits and measure overflow before requiring scroll.
- F13 rendered rail comparison:initial exact comparison yielded7 exact/11 differences across18 screenshots. Every channel difference was at most2/255; no shifted geometry was observed. Controlled verified-original/current replay then produced18/18 pixel-exact pairs. Repeating the original alone also produced one at-most2-level difference versus its archived original. This demonstrates rendering variation independent of runtime changes; the precise compositor mechanism is an inference. No image or rail redesign was applied; strict original/current acceptance was retained.
- Read-only helper/file-directory lookups guessed nonexistent names; inventory corrected the lookups. Replay source-hash preflight exposed Python newline normalization of the unchanged registry; exact CRLF reconstruction in memory reproduced its raw hash, with no disk/source rewrite. The failed empty replay folder is preserved. Web adapter GitHub lookups were unsupported; a read-only GitHub connector provided actual repository/branch/account evidence. No project/Git content changed from these issues. Prevention:inventory tools/files, preserve byte/text distinctions and distinguish access limitations from Git connection failures.

Complete expected/actual/cause/method/prevention records and failed-run evidence remain in `failure-ledger.md`, `presentation-audit-notes.md` and the original run folders. No corrected failure was discarded.

## STILL REQUIRES LIVE VALIDATION

After your later explicit push approval:verify remote commit/files, protected hashes and Pages build, then live URL/routes/assets and smoke tests. You must personally inspect the actual site on laptop/phone/tablet where available and classroom projector, including actual browser fullscreen, screen/chrome/orientation differences, touch, legibility/contrast and navigation geometry. Installed-Edge emulation is useful evidence but cannot establish physical-device or user approval. Other browser/device fullscreen behavior remains pending.

## UNRESOLVED ITEMS

- Final supernatural Landing activity-name lettering.
- Door to Darkness larger-scene bill/departure cue.
- Hotel Transylvania larger Landing scene wolf-headed guest/interior observations.
- Final navigation geometry pending genuine live/device validation.

These were not redesigned or marked resolved. They remain separate non-blocking design/live-validation observations. No critical local functional failure remains.

## GITHUB STATUS

Existing project:`C:\\Users\\DELL\\Documents\\Codex\\2026-09-30\\ar`. Existing repository:[NSAdyad/the-haunted-realm](https://github.com/NSAdyad/the-haunted-realm), public; local main tracks origin/main at `https://github.com/NSAdyad/the-haunted-realm.git`.

Read-only connector inspection confirmed authenticated NSAdyad and remote main commit125798046dfc25e5b97e331ffc86112468c0f20d matching local HEAD. No new candidate commit exists. Pages remains main/(root) per your current explicit configuration; this connector did not expose a fresh Pages-settings GET, so that setting is not misrepresented as independently queried. No configuration change occurred. Planned live validation URL:[The Haunted Realm](https://nsadyad.github.io/the-haunted-realm/).

The candidate uses root index.html and relative static CSS/ES-module/asset paths with hash routing. It fits the existing main/root publishing method without a separate build/site or Pages configuration change. The previous intentionally absent remote entry point remains unchanged until an approved push.

Proposed commit message:**Integrate Haunted Realm shell and classroom presentation mode**.

Exact file inclusion/exclusion paths, sizes and SHA-256 values are prepared in `work/home-presentation-correction-v1/exact-deployment-scope.md` and `deployment-candidate-files.json`. The allowlist includes this same tested integrated runtime, required approved navigation assets/provenance and workflow/test/approval records. Existing tracked history is retained. Excluded review/support/screenshots remain local; no files are deleted/untracked and no blanket exclusion removes runtime paths under work/outputs.

**STOP:await your explicit later approval before any staging, commit or push. No deployment and no Echoes content work has begun.**
'''
report=re.sub(r'\b(At|at|was|Title|spaces|lettering|scrollY|to|retained|least|and|uses|of|by|retains|normal|Presentation|support|input|all|All|final|run|before|after|give|source|checks|pass|fail)(?=\d)',r'\1 ',report)
report=re.sub(r':(?=\d)',': ',report)
(ROOT/'docs/the-haunted-realm-home-presentation-correction-report-v1.md').write_text(report,encoding='utf-8')
status=f'''# The Haunted Realm — controlled live-validation candidate

Status: **READY FOR CONTROLLED GITHUB DEPLOYMENT — AWAITING USER APPROVAL**.

This is the same local integrated shell. Latest corrections are not yet personally verified/finally protected. The user-inspected successful activity rail remains regression-protected.

Home fits1920×1080 without document scrolling in normal/Presentation states. Shared direct-action native fullscreen and graceful fallback/exit pass. Final browser checks:{browser_count} PASS/0 FAIL. Protected hashes:{protected}/{protected}. All9 shells remain educational-content-free. All561 pre-existing files and images/reviews are preserved.

Rendered rail comparisons distinguish browser rounding from unchanged source/assets; see final rail audit and report. Exact runtime SHA-256 values are in presentation-final-results.json and deployment candidate manifest.

Report:docs/the-haunted-realm-home-presentation-correction-report-v1.md.
Exact scope:work/home-presentation-correction-v1/exact-deployment-scope.md.

Existing NSAdyad/the-haunted-realm, main tracking origin/main; Pages main/(root) per user configuration. No staging/commit/push/deployment or Pages change. Physical/laptop/phone/tablet/projector/live validation pending explicit push approval. Existing lettering/Door/Hotel/geometry observations remain unresolved.

Do not start Echoes or any other component. Stop for the user's instruction.
'''
status=re.sub(r'\b(fits|all|All)(?=\d)',r'\1 ',status)
status=re.sub(r':(?=\d)',': ',status)
(ROOT/'outputs/the-haunted-realm-home-presentation-validation-candidate.md').write_text(status,encoding='utf-8')
print(json.dumps({'browser_checks':browser_count,'protected':protected,'reports_written':2}))
