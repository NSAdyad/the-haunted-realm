# MESSAGE

I have now personally inspected the first local integrated shell.

This is my actual user inspection, and it takes priority over assumptions based only on automated tests.

Overall:

# THE WEBSITE LOOKS GREAT.

I am very happy with the overall visual appearance.

The Haunted Realm atmosphere works.

The activity pages look good as shells.

Most importantly:

# THE LEFT-SIDE NAVIGATION ON THE ACTIVITY PAGES WORKS FANTASTICALLY.

Do NOT redesign or unnecessarily change that successful system.

However, I found several important issues/differences between the implementation and the intended classroom experience.

We need to correct/understand these before treating the shell as approved.

---

# ASK

Work on the existing integrated shell.

Do NOT rebuild it.

Do NOT create another project.

Do NOT create another repository.

Do NOT start Echoes of the Past content yet.

First address the user-inspection findings below.

Then perform the complete regression testing.

If all required local checks pass, prepare this SAME integrated shell for the existing GitHub repository and live GitHub Pages validation.

Because real phone/projector testing requires an actual accessible site, the goal of this stage is to reach a controlled live-validation candidate.

However, follow the Git/GitHub safety gate defined later in this prompt.

---

# 1. CURRENT USER-VERIFIED SUCCESS — PRESERVE IT

My personal inspection confirms:

## Activity-page left navigation

When I enter the individual activity pages, the left-side navigation works extremely well.

I can navigate through the activity destinations and the overall presentation looks fantastic.

Treat this as:

**USER INSPECTION — WORKING WELL / REGRESSION-PROTECTED BEHAVIOUR**

Do NOT redesign it while fixing unrelated Home issues.

Any changes required elsewhere must be regression-tested against this navigation.

---

# 2. EMPTY ACTIVITY PAGES ARE EXPECTED

The individual activity pages currently have no educational content.

That is expected.

Do NOT fill them now.

The first activity we will develop later is:

# Echoes of the Past

Its:

- content
- historical material
- images
- structure
- interactions
- presentation behaviour
- internal navigation
- responsive behaviour

will be provided and developed separately.

Do NOT begin that work now.

---

# 3. USER-FOUND ISSUE — HOME DOES NOT FIT WITHIN ONE SCREEN

The Home/Landing Page currently requires me to scroll vertically.

I have to scroll up/down to see the complete Home experience.

For the classroom/presentation experience, this is not the intended result.

The previous automated report stated that Home scrolling worked and that the final activity remained reachable.

That proves reachability.

It does NOT prove the intended presentation layout.

These are different requirements.

---

# 4. REQUIRED HOME / PRESENTATION BEHAVIOUR

For the intended classroom/projector presentation view, the primary Home/Landing interface should fit inside the available presentation viewport.

At:

# 1920 × 1080

I should NOT need ordinary document scrolling simply to access the complete primary Home interface/activity selection.

The important Home elements should remain usable within the presentation viewport.

Do NOT solve this by blindly shrinking everything.

First determine exactly what creates the vertical overflow.

Preserve:

- readability
- Haunted Realm atmosphere
- approved imagery
- title prominence
- activity-scene quality
- usable controls
- sensible proportions

Use responsive layout intelligently.

---

# 5. HOME NAVIGATION DOES NOT MATCH MY EXPECTATION

On Home I currently see an:

# Activities

control.

When I activate it, the behaviour feels like it takes/scrolls me down toward the activity section.

That is not the navigation experience I expected from the design work.

We previously established the Home navigation direction as:

# Home + Activities

with **Activities acting as access to the activity destinations/navigation**, rather than merely behaving like a scroll-to-section control.

Please inspect the current implementation and explain exactly what it currently does.

Then correct it so the Home navigation behaves as the intended navigation system.

---

# 6. HOME ACTIVITIES CONTROL — REQUIRED PURPOSE

The Home Activities control should provide navigation access to the current activity destinations.

Current exact names:

1. Echoes of the Past
2. The Cursed Quest
3. The Book of Shadows
4. Fastest Finger First
5. Words of the Feast
6. The Phantom Order
7. Door to Darkness
8. Build the Haunted Banquet
9. Hotel Transylvania

The architecture must remain expandable beyond nine.

Do NOT create a fixed architecture where nine is the permanent maximum.

---

# 7. DO NOT DAMAGE THE SUCCESSFUL ACTIVITY-PAGE NAVIGATION

The activity-page left navigation is currently one of the strongest parts of the implementation.

While correcting Home:

do NOT unnecessarily change:

- its physical design
- destination ordering
- selected/current state
- navigation-image usage
- background relationship
- general behaviour

If shared code must change, regression-test every activity destination afterwards.

---

# 8. PRESENTATION / PROJECTOR MODE

I also need an actual:

# Presentation Mode / Projector Mode

for classroom use.

If the current implementation does not contain a clear Presentation Mode control/capability, implement a shared site-level Presentation Mode.

This must NOT be a completely separate website.

It must be a state of the same integrated Haunted Realm site.

---

# 9. PRESENTATION MODE PURPOSE

Presentation Mode should optimize the site for classroom projection.

It should:

- maximize usable screen area
- support the one-screen Home presentation requirement
- preserve navigation access
- avoid top/bottom clipping
- avoid hidden controls
- avoid unnecessary document scrolling for the primary Home presentation interface
- preserve the Haunted Realm background
- preserve approved imagery
- preserve readable text
- provide a clear way to exit
- work correctly at 1920×1080

Use browser fullscreen appropriately if supported.

Do not depend exclusively on fullscreen succeeding.

If browser security requires fullscreen to be initiated by a direct user action, implement that correctly.

If fullscreen is unavailable/rejected, the presentation layout must fail gracefully rather than breaking the site.

---

# 10. PRESENTATION MODE MUST BE SHARED

Do NOT make Presentation Mode a temporary Home-only hack.

Later we will use the same infrastructure with:

- Echoes of the Past
- The Cursed Quest
- The Book of Shadows
- Fastest Finger First
- restaurant activities
- future activities

Do NOT implement their content now.

Just ensure Presentation Mode is a reusable site-level capability.

---

# 11. PRESENTATION MODE MUST NOT BREAK STATE

Entering/exiting Presentation Mode must not:

- unexpectedly return Home
- lose the current activity
- break navigation
- duplicate navigation
- alter activity names
- alter protected artwork
- create a competing black background
- reset the destination unnecessarily

---

# 12. REAL LIVE TESTING IS NOW IMPORTANT

The previous local testing used simulated/emulated viewport sizes.

That is useful, but it is NOT enough for final classroom validation.

I need to be able to open the actual site on:

- my laptop
- my phone
- tablet where available
- classroom/projector environment

This requires an accessible deployed site.

The existing GitHub repository / Pages site is therefore part of the validation workflow.

---

# 13. WHY GITHUB CURRENTLY SHOWS NO UPDATE

The previous report correctly stated:

**No commit, push, Pages change or deployment occurred.**

Therefore the absence of the new shell on GitHub is expected.

Do NOT treat that as a GitHub connection failure unless actual Git operations demonstrate a failure.

We intentionally stopped before deployment.

---

# 14. EXISTING PROJECT ONLY

Continue using the existing repository:

# the-haunted-realm

Continue using the existing GitHub Pages configuration:

# main / root

Do NOT:

- create another repository
- create another Pages site
- reset Git history
- force-push
- replace the project
- delete repository history

There must remain:

**ONE evolving repository**
**ONE evolving website**
**ONE eventual live Pages site**

---

# 15. IMPORTANT GITHUB SAFETY GATE

Do NOT immediately push the current version simply because I want live testing.

First:

1. correct the Home one-screen/presentation behaviour;
2. correct Home navigation behaviour;
3. implement/verify Presentation Mode;
4. run the complete local regression suite;
5. verify protected assets;
6. verify no critical local test is failing.

If a critical test still fails:

# DO NOT PUSH.

Report the failure under the permanent failure rule.

If all required local checks pass, then prepare the exact tested candidate for GitHub.

Before performing the actual commit/push, report:

**READY FOR CONTROLLED GITHUB DEPLOYMENT**

and provide:

- exact files to be committed;
- exact files intentionally excluded;
- test summary;
- protected-asset verification;
- known unresolved non-blocking items;
- proposed commit message;
- confirmation that this is the existing repository/main branch/Pages root.

Then:

# STOP AND WAIT FOR MY EXPLICIT APPROVAL TO PUSH.

Do not commit/push merely because the candidate is ready.

---

# 16. AFTER I APPROVE THE PUSH

Only after my explicit approval in a later instruction:

- commit the tested candidate
- push to the existing repository
- verify the remote commit
- verify required files exist remotely
- verify GitHub Pages deployment
- verify the live URL responds
- run appropriate live smoke tests
- report the exact live URL/state
- STOP

Then I will personally test the actual live website on my devices.

Do not mark it USER VERIFIED until I personally inspect it.

---

# 17. PERMANENT CUMULATIVE DEVELOPMENT MODEL

After the shell is eventually live and personally approved, we will develop:

# Activity 1 — Echoes of the Past

Then we test:

**Home + navigation + Echoes**

When Activity 2 is built:

**Home + navigation + Echoes + Activity 2**

When Activity 3 is built:

**Home + navigation + Activities 1–3**

Continue cumulatively.

By Activity 9:

**Home + navigation + Activities 1–9**

Every new activity must integrate into the SAME site.

---

# 18. NO DISCONNECTED VERSIONS

Do NOT create:

- separate Echoes website
- separate Cursed Quest website
- separate copies of the entire project for each activity
- disconnected runtime versions

Use the existing integrated architecture and Git history.

---

# 19. PROTECTED WORK = REGRESSION CONTRACT

Anything approved/protected must not be casually altered while implementing later work.

This includes:

- global background
- THE HAUNTED REALM title
- navigation physical design
- nine approved navigation images
- successful activity-page navigation
- exact activity names
- existing approved responsive exceptions
- corrected behaviours

If protected work genuinely must change:

# STOP.

Report:

**DEPENDENCY CONFLICT**

Explain:

- what must change
- why
- what depends on it
- smallest possible change
- alternatives
- regression risk

Wait for approval.

---

# 20. PERMANENT MISTAKE / FAILURE RULE

This rule applies again and remains permanent:

> When you make a mistake or fail at a task, do not silently retry or repeat the same mistake. Clearly identify what went wrong, why it happened, how it was corrected, and what rule or constraint should prevent it from happening again. Apply those lessons to subsequent work and preserve meaningful failure information. Before delivering a revision, check it against previously identified mistakes and requirements so that previously fixed problems are not reintroduced.

Also:

> Before making changes, check them against previous mistakes and do not reintroduce fixed problems. Before delivering a release candidate or approved stage, check the work against every applicable requirement and every previously identified problem.

---

# 21. NEW PERMANENT REGRESSION REQUIREMENTS FROM MY INSPECTION

Record these user-discovered requirements:

## HOME PRESENTATION FIT

At the intended projector/presentation viewport, the primary Home interface must not require ordinary vertical document scrolling merely to access the complete activity selection.

## HOME NAVIGATION

The Home Activities control must behave as actual activity navigation according to the established design direction, not merely as an unexpected scroll-to-section action.

## PRESENTATION MODE

The shared site must provide a usable classroom Presentation/Projector Mode.

## REAL-DEVICE VALIDATION

Local viewport emulation does not equal physical-device validation.

Important responsive behaviour must ultimately be tested through the deployed site on real devices where available.

---

# 22. PREVIOUS FAILURES MUST NOT RETURN

While correcting the current issues, explicitly regression-test against previously corrected problems, including:

- transparent drawer/content collision
- mobile drawer clipping
- Home focus problems
- skip-link routing problems
- malformed URL handling
- outside-tap click-through
- selected-row visibility
- favicon/request problems
- asset connection/path problems
- console/runtime errors
- broken destination routes
- black/competing backgrounds
- top/bottom clipping
- inaccessible controls
- unreachable final navigation entry

Do not silently reintroduce any of them.

---

# 23. PROTECTED ASSET VERIFICATION

Before and after implementation changes, verify protected asset hashes.

The previous state reported:

**20/20 protected asset hashes matched.**

After Hotel Transylvania final navigation approval, use the authoritative current protected-asset manifest/count rather than assuming the old count if it has changed.

Report the actual result.

---

# 24. RESPONSIVE LOCAL RETEST

After the corrections, rerun the local responsive suite at minimum:

- **1920×1080** projector
- **1600×900** desktop
- **1366×768** laptop
- **768×1024** tablet portrait
- **390×844** mobile portrait
- **320×812** narrow mobile

Distinguish:

**normal mode**

from:

**Presentation Mode**

where relevant.

---

# 25. PROJECTOR ACCEPTANCE TEST

At **1920×1080 Presentation Mode**, explicitly verify:

- Home primary interface fits the intended viewport
- no required Home activity access depends on vertical document scrolling
- title remains visible
- navigation remains usable
- all activity destinations remain accessible
- controls remain visible
- no top clipping
- no bottom clipping
- no unintended horizontal scrolling
- Presentation Mode can be exited

Do not replace this with the weaker assertion:

“the final activity can be reached by scrolling.”

---

# 26. ACTIVITY-PAGE REGRESSION

Test all nine activity shells again.

For each one verify:

- destination opens
- correct exact name
- correct selected navigation state
- Home works
- navigation to other activities works
- background continuity remains
- no unexpected black page
- no route failure
- no console/runtime failure

The activity content remains empty intentionally.

---

# 27. INPUT TESTING

For functionality that exists at this stage, test what is actually supported:

- mouse
- keyboard/focus
- emulated touch locally

For Presentation Mode specifically verify keyboard/mouse entry and exit behaviour where applicable.

Do NOT claim physical touch/device testing until the deployed version is actually tested on a physical device.

---

# 28. NO EMOJIS

Permanent:

# NO EMOJIS IN THE WEBSITE.

Do not introduce them while adding Presentation Mode or correcting navigation.

---

# 29. CURRENT UNRESOLVED DESIGN ITEMS REMAIN SEPARATE

Keep unresolved unless explicitly addressed later:

- final Landing Page supernatural activity-name lettering
- Door to Darkness Landing Page bill/departure cue
- Hotel Transylvania larger Landing Page guest/interior observations
- final navigation geometry pending genuine live validation

Do not silently mark these resolved.

Do not use this task as permission to redesign those scenes.

---

# 30. SCOPE — DO NOT WORK AHEAD

For this task you may work only on:

- Home one-screen/projector fit
- correct Home navigation behaviour
- shared Presentation Mode
- directly necessary responsive/supporting code
- regression testing
- documentation/failure records
- preparation of the tested candidate for later GitHub deployment approval

Do NOT:

- develop Echoes content
- develop Activity 2–9 content
- build games
- build multiplayer
- generate new artwork
- redesign protected imagery
- resolve unrelated Landing scene issues
- commit/push without the later explicit approval gate
- change Pages configuration

---

# 31. REQUIRED REPORT

When finished, report:

## USER INSPECTION FINDINGS
Record exactly what I found.

## ROOT CAUSE
Explain why the Home scrolling/navigation/presentation differences existed despite the previous automated test pass.

## IMPLEMENTED CORRECTIONS
Exactly what changed.

## PRESERVED SUCCESSFUL WORK
Especially confirm the activity-page left navigation remains intact.

## FILES CHANGED
Exact runtime/source files.

## FILES CREATED
Separate runtime files from test/audit artifacts.

## PRESENTATION MODE
Explain exactly how it works.

## HOME FIT RESULTS
Include 1920×1080 results and document/viewport measurements where useful.

## HOME NAVIGATION RESULTS
Explain exactly what Activities now does.

## RESPONSIVE TEST RESULTS
All six viewport targets.

## ACTIVITY-PAGE REGRESSION
All nine shells.

## PREVIOUS-FAILURE REGRESSION
Report each relevant regression result.

## PROTECTED-ASSET VERIFICATION
Actual current manifest/hash result.

## CONSOLE / NETWORK / ROUTING
Report actual failures/errors.

## FAILURES DURING THIS TASK
Do not omit corrected failures.

For each:
- what failed
- why
- correction
- prevention rule
- regression rerun result

## STILL REQUIRES LIVE VALIDATION
Clearly identify physical-device/projector/browser items.

## UNRESOLVED ITEMS
Preserve existing unresolved design items.

## GITHUB STATUS
Confirm whether the candidate remains local.

If all gates pass, state:

# READY FOR CONTROLLED GITHUB DEPLOYMENT — AWAITING USER APPROVAL

and provide the exact proposed commit scope/message.

Do NOT push yet.

---

# GOAL

The goal is to preserve what already looks and works extremely well while correcting the user-discovered Home/presentation issues and preparing ONE tested candidate for real live validation.

The next stage should eventually allow me to inspect the SAME website through GitHub Pages on real devices.

But GitHub deployment happens only after this correction/testing report and my explicit approval.

When finished:

# STOP.

Do not push.

Do not deploy.

Do not start Echoes of the Past.

Wait for my next instruction.