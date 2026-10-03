# The Haunted Realm — integrated shell and cumulative workflow

Recorded from the user on 2026-10-02. This update supersedes conflicting earlier workflow/current-authorization notes. This task authorizes local shell implementation/testing ONLY; an explicit later approval is required before committing, pushing or deploying. The complete user instruction follows unchanged.

# MESSAGE

I have personally inspected the corrected **Hotel Transylvania mobile bottom-scrolled navigation review**.

**I love it and approve it.**

The corrected mobile entry now properly shows:

- the exact name **Hotel Transylvania**
- the already-approved **34×34px artwork**
- the existing navigation treatment
- unchanged drawer width
- unchanged lettering
- unchanged frame
- unchanged row dimensions
- unchanged spacing

I accept the correction method: only the static review scroll position changed.

The previous failed mobile attempt must remain preserved as part of the project history.

The UTF-8 audit-reader issue was correctly identified and resolved without changing or repairing visual assets.

We have now reached an important transition point in the project.

The design/review stage has produced enough approved material to begin building and testing the actual website shell.

This prompt establishes the permanent development, integration, regression-testing and deployment workflow from this point forward.

---

# ASK

Perform TWO controlled tasks only:

## TASK A
Finalize the Hotel Transylvania navigation approval and establish the complete current navigation-image set as protected.

## TASK B
Prepare and implement the **first local integrated website shell** using the already-approved project material.

This means:

**Home/Landing Page + global navigation + nine destination page shells**

working together as ONE website.

Do NOT build the actual educational/activity content inside Echoes of the Past or Activities 2–9 yet.

Do NOT push anything to GitHub yet.

Do NOT deploy anything yet.

First build and test locally, then report back and STOP.

---

# PART 1 — HOTEL TRANSYLVANIA FINAL NAVIGATION APPROVAL

Mark:

**Hotel Transylvania — APPROVED / PROTECTED — NAVIGATION IMAGE**

The artwork was already approved.

The corrected complete mobile entry has now also been personally inspected and approved.

The current nine navigation images are therefore:

1. **Echoes of the Past**
2. **The Cursed Quest**
3. **The Book of Shadows**
4. **Fastest Finger First**
5. **Words of the Feast**
6. **The Phantom Order**
7. **Door to Darkness**
8. **Build the Haunted Banquet**
9. **Hotel Transylvania**

Verify all nine approved navigation images and all other protected assets against their recorded hashes before implementation begins.

Do NOT regenerate, redesign or replace them.

---

# PART 2 — IMPORTANT: NINE IS NOT A PERMANENT LIMIT

The site currently contains nine activities.

That is the CURRENT structure, not a permanent architectural maximum.

The architecture must support future additions such as:

Activity 10,
Activity 11,
Activity 12,
Activity 15,
etc.

Do not hard-code the website in a way that requires rebuilding the navigation or architecture when another activity is introduced.

Use a maintainable shared structure/data source where appropriate.

---

# PART 3 — WE ARE NOW CHANGING DEVELOPMENT PHASE

Until now the project has primarily been:

**DESIGN / REVIEW / NOT IMPLEMENTED**

We are now beginning:

**CONTROLLED IMPLEMENTATION + TESTING**

Do not confuse this with authorization to build the entire project.

We are implementing only the first shared website shell.

---

# PART 4 — FIRST IMPLEMENTATION SCOPE

Build locally:

## A. HOME / LANDING PAGE

Use the existing approved/current Haunted Realm design material.

The Home page must provide access to all nine current activities.

Use the established Landing Page design direction and existing assets.

Do NOT invent a completely new Home page.

Do NOT regenerate approved images.

Do NOT replace the approved global background.

Do NOT replace the approved title.

---

## B. HOME NAVIGATION

Implement the established Home navigation direction:

**Home + Activities**

The Activities control provides access to all nine exact activity names.

Do NOT attempt to force nine full activity names permanently across one narrow horizontal row.

Use the established approved/current iron/glass Haunted Realm navigation visual language.

---

## C. ACTIVITY PAGE NAVIGATION

Each destination page must use the established activity-page navigation direction:

- navigation on the LEFT for desktop/laptop/projector
- Home accessible
- all current activities accessible
- current destination visibly identified
- same underlying navigation system/data where appropriate
- mobile behaviour based on the existing drawer direction

Do NOT create separate unrelated navigation systems for every page.

---

# PART 5 — CREATE THE NINE DESTINATION PAGE SHELLS

Create functional destination/page shells for:

1. Echoes of the Past
2. The Cursed Quest
3. The Book of Shadows
4. Fastest Finger First
5. Words of the Feast
6. The Phantom Order
7. Door to Darkness
8. Build the Haunted Banquet
9. Hotel Transylvania

At this stage these are **page shells only**.

They exist so we can verify:

- routing/navigation
- shared background
- page structure
- responsive layout
- available content space
- scrolling
- navigation positioning
- transitions between major sections
- future activity integration

Do NOT invent educational content for them.

Do NOT build their games.

Do NOT create fake finished activities.

Do NOT fill them with content simply to make them look complete.

A clearly identified temporary content area is sufficient where needed for layout testing.

---

# PART 6 — ECHOES OF THE PAST COMES NEXT, BUT NOT NOW

After this shell has been tested, eventually deployed and personally approved, our next major development task will be:

# Echoes of the Past

We will then separately develop:

- exact content
- structure
- historical material
- images
- interactions
- presentation behaviour
- navigation within the activity
- responsive behaviour
- any other approved functionality

Do NOT begin that work during this task.

Receiving this information is NOT permission to work ahead.

---

# PART 7 — PERMANENT CUMULATIVE DEVELOPMENT MODEL

From this point forward, development must be cumulative.

We are NOT going to create disconnected versions of the website.

There must be:

**ONE evolving project**
**ONE evolving repository**
**ONE integrated website**
**ONE live GitHub Pages site once deployment is authorized**

The development sequence will conceptually become:

**Shell**

then:

**Shell + Activity 1**

then:

**Shell + Activities 1–2**

then:

**Shell + Activities 1–3**

then:

**Shell + Activities 1–4**

and so on.

Eventually:

**Shell + Activities 1–9**

Future activities must extend this same architecture rather than creating another disconnected site.

---

# PART 8 — PERMANENT CUMULATIVE REGRESSION RULE

When a new activity is added, testing MUST NOT cover only the newest activity.

Example:

After Echoes of the Past is implemented:

test:

**Home + navigation + Echoes**

After The Cursed Quest is implemented:

test:

**Home + navigation + Echoes + The Cursed Quest**

After The Book of Shadows is implemented:

test:

**Home + navigation + Activities 1–3**

Continue cumulatively.

By Activity 9, the regression scope includes:

**Home + navigation + Activities 1–9**

Previously approved functionality must not silently break because new functionality was added.

---

# PART 9 — PROTECTED WORK IS A REGRESSION CONTRACT

Once something has been personally approved/protected, treat its working behaviour and approved visual identity as a regression requirement.

Future development must not casually:

- redesign it
- replace it
- remove it
- rename it
- change its meaning
- break its navigation
- change its responsive behaviour
- alter approved artwork
- reintroduce previously corrected problems

If a genuine dependency requires modifying protected work:

**STOP.**

Explain:

1. what must change;
2. why;
3. what depends on it;
4. the smallest proposed change;
5. possible effects/regression risks.

Then wait for approval before making that protected change.

---

# PART 10 — PERMANENT MISTAKE / FAILURE RULE

This is a permanent project requirement and must be followed throughout development:

> **When you make a mistake or fail at a task, do not silently retry or repeat the same mistake. Clearly identify what went wrong, why it happened, how it was corrected, and what rule or constraint should prevent it from happening again. Apply those lessons to subsequent work in the conversation and, when appropriate, retain them as project guidance for future work. Before delivering a revision, check it against previously identified mistakes and requirements so that previously fixed problems are not reintroduced.**

Also:

> **Before making changes, check them against previous mistakes and do not reintroduce fixed problems. Before delivering a release candidate or approved stage, check the work against every applicable requirement and every previously identified problem.**

This applies to:

- coding errors
- visual regressions
- navigation errors
- responsive problems
- clipping
- scrolling
- failed tests
- broken links
- asset mistakes
- deployment failures
- encoding errors
- GitHub errors
- game/functionality errors later
- incorrect assumptions
- accidental scope expansion

Do NOT silently retry until something appears to work.

A failure must become information that prevents repetition.

---

# PART 11 — KNOWN HISTORICAL FAILURES FROM THE PREVIOUS PROJECT

The previous project repeatedly suffered from problems that MUST become regression checks.

These included:

### A. Unwanted teacher/student login architecture

Do NOT introduce a mandatory Teacher Session / Student Session login architecture.

Future live multiplayer should follow the simpler intended model:

**host starts session → code shown → participants enter code → join**

No participant account is required.

Do not build this functionality now.

---

### B. Presentation/projector clipping

Previous versions had serious problems where:

- top content disappeared
- bottom content disappeared
- controls were inaccessible
- content was clipped
- presentation mode behaved badly

The new site must be tested for these risks.

---

### C. Mobile usability

Previous mobile versions had:

- poor layouts
- inaccessible content
- clipping
- unusable navigation
- insufficient scrolling

Mobile portrait must be genuinely tested.

---

### D. Broken functionality after unrelated changes

Previously, removing/changing one system broke other functions.

This must not happen again.

Every meaningful addition requires regression testing.

---

### E. Games appeared visually but did not actually work

Later, when games are developed, rendering the interface is NOT proof of functionality.

The required distinction is:

**DESIGNED**
≠
**IMPLEMENTED**
≠
**TESTED**
≠
**VERIFIED**

For future multiplayer games, actual end-to-end testing will eventually need to verify flows such as:

host starts
→ join code
→ participant joins
→ host sees participant
→ activity starts
→ participant interaction reaches host
→ scoring/state updates
→ next round/question
→ leaderboard/state
→ completion

Do NOT build those games now.

This is recorded now so the mistake is never repeated.

---

# PART 12 — NO EMOJIS

Permanent rule:

**NO EMOJIS ANYWHERE IN THE WEBSITE.**

This includes:

- buttons
- navigation
- headings
- cards
- games
- instructions
- scoreboards
- podiums
- restaurant material
- temporary UI
- placeholder icons

Use approved realistic thematic imagery/illustrations instead.

---

# PART 13 — GLOBAL BACKGROUND

The approved/protected global Haunted Realm background must remain the global visual foundation.

Do NOT create competing full-screen black backgrounds.

Do NOT repeat the previous failure where individual pages became black or almost black because multiple background systems competed.

All activity page shells must visibly inherit/belong to the same Haunted Realm world.

Content surfaces may provide readability where necessary, but must not replace the entire global background with an unrelated opaque layer.

---

# PART 14 — PROTECTED TITLE

Preserve:

# THE HAUNTED REALM

Do not redesign, regenerate, replace, resize or reposition the protected title without explicit approval.

Use the approved Ancient Village Sign design/assets.

---

# PART 15 — EXACT ACTIVITY NAMES

Use exactly:

1. **Echoes of the Past**
2. **The Cursed Quest**
3. **The Book of Shadows**
4. **Fastest Finger First**
5. **Words of the Feast**
6. **The Phantom Order**
7. **Door to Darkness**
8. **Build the Haunted Banquet**
9. **Hotel Transylvania**

Do NOT:

- rename them
- shorten them
- translate them
- replace them with Activity 1–9 in intended UI
- call The Cursed Quest “Crusade Quest”
- change The Book of Shadows to plural

---

# PART 16 — APPROVED NAVIGATION IMAGES

Use the nine approved navigation images exactly.

Do NOT regenerate them.

Do NOT substitute emojis/icons.

Do NOT replace them with generic images.

They are now protected project assets.

---

# PART 17 — NAVIGATION PHYSICAL DESIGN

Preserve the established navigation material language:

- corroded iron
- aged glass
- slender chains
- fractured details
- restrained cobweb detail
- cold reflections
- readable lettering
- warm amber current/selected state
- village/background visible through/between elements

Do not revert to:

- wooden button grids
- generic web navigation
- colourful cards
- flat modern app navigation
- cartoon UI

---

# PART 18 — IMPORTANT: SOME GEOMETRY IS STILL PROVISIONAL

Current direction includes approximately:

- **430px laptop rail**
- **460px projector rail**
- **mobile drawer**

These are NOT permanently protected final geometry.

They require LIVE VALIDATION.

The implementation should respect the current design direction, but actual browser testing must determine whether:

- activity content has enough space
- names remain readable
- scrolling works
- controls remain accessible
- laptop layout works
- projector layout works
- mobile layout works

Do NOT declare this geometry permanently approved merely because it exists in a static study.

---

# PART 19 — MOBILE READABILITY IS STILL A LIVE VALIDATION REQUIREMENT

A known concern exists:

transparent/aged-glass navigation can allow underlying page text to visually compete with navigation labels on mobile.

Do NOT silently redesign the approved navigation artwork to solve this.

During implementation/testing, determine whether the problem actually occurs.

If it occurs, report:

- where
- under what viewport
- why
- proposed minimal treatment

before making a meaningful design change.

---

# PART 20 — LANDING PAGE LETTERING REMAINS UNRESOLVED

The Landing Page activity-name supernatural lettering treatment remains:

**UNRESOLVED**

Previously explored directions include:

- cursed stone inscriptions
- spectral apparitions
- possessed antique metal

Do NOT silently select one merely because implementation has begun.

If the current landing material requires a temporary/current treatment to render the page, preserve the existing review state and clearly report what was used.

Do not falsely mark the lettering as approved.

---

# PART 21 — EXISTING LANDING-PAGE OBSERVATIONS REMAIN SEPARATE

Keep pending:

### Door to Darkness
The larger Landing Page scene's departure/bill cue remains relatively small.

### Hotel Transylvania
The larger Landing Page scene has recorded guest/interior observations, including the fully wolf-headed guest and shifts in architecture/furniture/lighting.

Do NOT silently modify these scenes during shell implementation.

Do NOT mark these observations resolved.

---

# PART 22 — IMPLEMENTATION MUST REUSE, NOT REINVENT

Before coding, inspect the actual existing project structure and approved assets.

Determine:

- what approved files already exist
- what assets should be reused
- what shared navigation data already exists
- what review artifacts are NOT runtime assets
- what implementation files are genuinely required

Do not blindly convert every review file into production code.

Do not duplicate approved assets unnecessarily.

Do not create multiple competing versions of the same runtime asset.

---

# PART 23 — MAINTAINABLE SHARED ARCHITECTURE

Where appropriate, centralize shared information such as:

- activity names
- navigation order
- destination paths
- approved navigation-image paths
- current activity state

The goal is to avoid nine manually duplicated navigation systems that later drift apart.

Adding a future activity should require a controlled addition rather than rewriting every page.

Do not overengineer.

Keep the architecture understandable and maintainable.

---

# PART 24 — FIRST LOCAL TESTING GATE

Before reporting this shell ready, test locally.

At minimum verify:

### HOME

- Home loads.
- Protected background appears correctly.
- Protected title appears correctly.
- Landing activity access is present.
- All nine activity destinations are represented.
- No accidental emojis.
- No missing/broken approved images.

### NAVIGATION

- Home is accessible.
- Activities access works.
- All nine exact activity names are present.
- Every activity destination can be opened.
- Activity-page navigation can return Home.
- Activity-page navigation can move between destinations.
- Current destination state is correct.
- No destination points to the wrong activity.

### PAGE SHELLS

All nine destination page shells load.

No 404 between internal destinations.

No page accidentally inherits an unrelated black/full-screen competing background.

No page shell contains invented educational content.

### SCROLLING

Verify relevant containers actually scroll.

No navigation item becomes permanently inaccessible.

No bottom content is trapped behind overlays.

### RESPONSIVE

Test at least:

- desktop
- laptop
- **1920×1080 projector**
- tablet
- mobile portrait

Use concrete viewport sizes and report them.

### INPUT

Where applicable to the shell/navigation, verify:

- mouse
- touch/mobile interaction
- keyboard/focus accessibility where relevant

Do not claim an interaction method was tested if it was not.

---

# PART 25 — PROTECT AGAINST CLIPPING

Specifically inspect:

- top of page
- bottom of page
- title
- navigation
- last activity
- content-area boundaries
- scrollable regions
- mobile drawer
- projector viewport

Look for:

- clipped content
- hidden controls
- overlays covering content
- unreachable navigation
- horizontal overflow
- accidental viewport cropping

Report actual results.

---

# PART 26 — ASSET / CONSOLE / ROUTING CHECK

Before declaring the local shell ready, check for:

- missing assets
- broken asset paths
- broken internal links
- console errors
- obvious runtime errors
- incorrect case-sensitive paths
- incorrect destination names/routes

If any check fails, follow the permanent failure rule.

Do not hide it.

---

# PART 27 — DO NOT EQUATE RENDERING WITH VERIFICATION

A screenshot is evidence of appearance.

It is NOT proof that navigation works.

A successful build is NOT proof that routing works.

A page opening once is NOT proof that responsive layouts work.

For every claim, distinguish:

**implemented**
**tested**
**passed**
**still requires live validation**

---

# PART 28 — GITHUB IS NOT AUTHORIZED YET

The existing repository is:

**the-haunted-realm**

The existing GitHub Pages configuration uses:

**main / root**

Do NOT:

- create another repository
- replace the repository
- reset repository history
- force push
- commit this implementation
- push this implementation
- alter Pages configuration
- deploy to the live URL

during this task.

We first need the local implementation/testing report.

---

# PART 29 — FUTURE GITHUB WORKFLOW

Once I explicitly approve a tested local implementation for deployment, the later workflow will be:

local implementation
→ local tests
→ cumulative regression tests
→ report
→ explicit approval to push
→ commit
→ push to existing repository
→ verify remote commit/files
→ wait for/verify GitHub Pages deployment
→ test actual live URL
→ report live results
→ STOP
→ my personal live inspection
→ corrections if required
→ retest
→ redeploy only with appropriate authorization
→ personal approval
→ mark live stage APPROVED / PROTECTED

Do not skip these states.

---

# PART 30 — ONE EVOLVING LIVE SITE

Once deployment begins, use the existing site/repository as the continuing project.

Do NOT produce disconnected website versions every time we add an activity.

Do NOT create Activity 1 as a separate independent website.

Do NOT create Activity 2 as another separate independent website.

Integrate each approved component into the existing project.

Git history provides version history.

Protected requirements provide regression boundaries.

---

# PART 31 — FUTURE ACTIVITY DEVELOPMENT RULE

When we begin Echoes of the Past, I will provide the content and requirements.

The permanent workflow for each major activity will be:

information
→ Codex explains understanding
→ Codex explains proposal
→ Codex explains how
→ included vs untouched
→ options where meaningful
→ STOP
→ my approval
→ implementation
→ local activity tests
→ cumulative regression tests
→ report
→ deployment approval
→ GitHub update
→ Pages deployment
→ live verification
→ STOP
→ my personal inspection
→ correction cycle if necessary
→ explicit approval/protection
→ only then next activity

Do not work ahead.

---

# PART 32 — INFORMATION IS NOT PERMISSION

This is permanent.

If I explain a future feature, activity, game, image, idea or correction:

**receiving that information is NOT permission to implement it.**

Do not infer authorization from:

- additional information
- silence
- discussion
- examples
- future plans

Only explicit approval authorizes the next meaningful implementation step.

---

# PART 33 — SCOPE CONTROL FOR THIS TASK

For this task, you are authorized to:

1. finalize Hotel Transylvania navigation-image approval;
2. inspect the existing project;
3. implement the local Home/Landing Page shell;
4. implement the shared navigation shell;
5. implement nine activity destination/page shells;
6. integrate already-approved assets;
7. test the local shell;
8. perform regression/verification checks;
9. create/update necessary project documentation and implementation files;
10. report the exact results.

You are NOT authorized to:

- build Echoes of the Past content
- build activity educational content
- build quizzes
- build Fastest Finger First
- build multiplayer infrastructure
- build restaurant games
- build role-play functionality
- generate new artwork
- resolve unrelated Landing Page design observations
- redesign protected components
- push to GitHub
- modify GitHub Pages
- deploy the site

---

# PART 34 — IF IMPLEMENTATION REQUIRES CHANGING PROTECTED DESIGN

STOP before making the change.

Do not decide that coding convenience is a reason to alter approved design.

Report:

**DEPENDENCY CONFLICT**

Then explain:

- what implementation requires
- which protected item would be affected
- why
- smallest possible correction
- alternatives
- regression risk

Wait for approval.

---

# PART 35 — IF A TEST FAILS

Do NOT silently retry.

Report:

**TEST FAILURE**

Then record:

1. test performed;
2. expected result;
3. actual result;
4. likely/root cause when known;
5. files/components involved;
6. proposed correction;
7. whether protected work would be affected.

If correction is internal, non-destructive and within already-approved implementation scope, apply the smallest correction only after recording the failure, then rerun the failed test and relevant regressions.

If correction changes protected design/scope, STOP for approval.

Preserve meaningful failure records.

---

# PART 36 — PRE-DELIVERY SELF-AUDIT

Before reporting back, check the work against:

- this entire prompt
- AGENTS.md
- existing protected-asset records
- navigation approval records
- existing project workflow documentation
- previously recorded failures
- unresolved observations
- scope restrictions
- exact activity names
- no-emoji rule
- global-background rule
- navigation rules
- responsive requirements
- cumulative regression rule

Do not report success until this audit is complete.

---

# GOALS

The goal of this task is NOT to finish The Haunted Realm.

The goal is to establish a **stable, maintainable, locally tested foundation** upon which we can safely build the activities one at a time.

Success means:

### 1.
All nine navigation images are formally approved/protected.

### 2.
The protected Home/Landing design is integrated into the first local website shell without unauthorized redesign.

### 3.
Home and navigation work as one system.

### 4.
All nine activity destinations exist and are reachable.

### 5.
Activity pages use the shared navigation direction.

### 6.
The architecture can grow beyond nine activities.

### 7.
Desktop/laptop/projector/tablet/mobile behaviour is actually tested locally.

### 8.
Known clipping/navigation/background failures are specifically regression-tested.

### 9.
No activity content is prematurely invented or implemented.

### 10.
No GitHub push/deployment occurs yet.

### 11.
Every failure is reported and learned from rather than silently retried.

### 12.
Previously approved/protected work remains intact.

---

# REQUIRED REPORT BACK

When the local implementation/testing is complete, report clearly:

### IMPLEMENTED
Exactly what was created or integrated.

### FILES CHANGED
Every existing runtime/source file changed.

### FILES CREATED
Every new runtime/source file created.

Separate production/runtime files from audit/review/test artifacts.

### PROTECTED-ASSET VERIFICATION
Hash/check results.

### LOCAL TESTS
Every test actually performed.

Include viewport sizes.

### PASSED
What genuinely passed.

### FAILED
Anything that failed, including failures corrected during the process.

For every failure, include the permanent failure-rule information.

### REGRESSION RESULTS
What previously approved behaviour/assets were checked.

### STILL REQUIRES LIVE VALIDATION
Anything that cannot honestly be established from local testing.

### UNRESOLVED ITEMS
Confirm all previously unresolved items that remain unresolved.

### GITHUB STATUS
Confirm that no commit/push/Pages modification/deployment occurred.

### CURRENT PROJECT STATE
Use precise status terminology.

Do NOT call the site LIVE or USER VERIFIED.

---

# FINAL INSTRUCTION

After completing the authorized local implementation and tests:

# STOP.

Do not commit.

Do not push.

Do not deploy.

Do not begin Echoes of the Past.

Do not perform another design task.

Wait for my inspection of your implementation/testing report and my explicit instruction for the next step.

## Separately approved narrow-screen title display exception

The user explicitly answered **Approve narrow-screen title display scaling** to the question about viewports narrower than 650 pixels. Only proportional display scaling is permitted there; preserve the exact title PNG, centred upper placement and 650 x 215 display at wider desktop viewports. Do not redesign, regenerate or modify the source asset.

## Separately approved overlay-content visibility treatment

After actual local screenshots showed page text/title competing through transparent navigation panes, the user explicitly answered **Approve temporary content concealment**. Conceal Home/activity main content only while the overlay Activities drawer is open, retaining layout/scroll position. Keep the approved village background and navigation visible. Closing the drawer restores content/title at the same scale and position. The permanent desktop activity rail is unaffected; no protected source artwork may be changed.
