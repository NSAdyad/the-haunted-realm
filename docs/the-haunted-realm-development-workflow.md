# The Haunted Realm — permanent development and regression procedure

Recorded locally on 2026-10-02 from the user's complete workflow instructions.

**Later controlling update:** follow `docs/the-haunted-realm-integrated-shell-and-cumulative-workflow.md`. The first integrated shell is authorized for local implementation/testing only. Commit/push/deployment require explicit later approval; earlier automatic-push language and recording-time current-state instructions are historical. Internal non-destructive fixes within the authorized scope may follow a recorded TEST FAILURE; protected-design/scope changes still require approval.

The procedure below governs future development. Its current-state, current-next-step and recording-request sections describe the state when it was recorded; they do not approve design revisions, implementation, a commit, a push or configuration changes in this recording step.

The previously approved/protected background, title and navigation design assets retain their existing protection. Future working website components require the explicit live-result approval described below. Any responsive adaptation of protected assets still requires separate approval.

Before we continue, I want to establish the permanent development workflow for **The Haunted Realm**.

This is extremely important because previous versions of this project repeatedly failed during GitHub, GitHub Pages, implementation and testing.

We are NOT going to repeat that process.

From this point onward, work must proceed **one small controlled step at a time**, with GitHub and the actual live website included in the approval process.

Do not skip steps.

Do not combine stages because they seem technically convenient.

Do not work ahead.

---

# CURRENT VERIFIED STATE

The current verified situation is:

- GitHub repository exists:
  **NSAdyad/the-haunted-realm**
- Repository is now **PUBLIC**.
- Local project:
  `C:\Users\DELL\Documents\Codex\2026-09-30\ar`
- Branch:
  **main**
- Local project tracks:
  **origin/main**
- GitHub Pages is enabled:
  **Deploy from a branch → main → /(root)**
- Live URL:
  `https://nsadyad.github.io/the-haunted-realm/`
- GitHub Pages deployment itself works.
- The live URL currently returns 404 because there is deliberately **no `index.html` yet**.
- There is currently no implemented website.
- The current Landing Page remains:
  **REVIEW / NOT IMPLEMENTED**
- Protected background remains unchanged.
- Protected THE HAUNTED REALM title remains unchanged.
- Protected navigation design remains unchanged.
- Current repository contains the design/review/project material already created.

The current 404 is therefore NOT a GitHub Pages configuration failure.

Do not attempt to “fix” it independently.

It will naturally disappear when an approved Landing Page is eventually implemented with the correct website entry point.

---

# PERMANENT DEVELOPMENT WORKFLOW

For EVERY major component, use the following sequence.

## STEP 1 — INFORMATION

I provide the content, requirements, references, corrections or other information for the component.

Receiving information is NOT permission to implement it.

---

## STEP 2 — UNDERSTANDING

Explain what you understood.

Identify:

- what is being created or changed
- what requirements apply
- what existing protected components could be affected
- any dependencies
- any ambiguity that genuinely needs resolving

Do not implement yet.

---

## STEP 3 — PROPOSAL

Explain exactly what you propose to do.

Explain:

- what will change
- how it will work
- what will remain untouched
- what files/components would eventually be affected
- any meaningful design/technical choices

If meaningful alternatives exist, show them before implementation.

---

## STEP 4 — APPROVAL TO DESIGN/REVISE

Wait for my explicit approval.

Silence is NOT approval.

Additional information is NOT approval.

Do not work ahead.

---

## STEP 5 — VISUAL / CONCEPT REVIEW WHERE APPLICABLE

For visual components, create the required review/mock-up first.

Do NOT automatically implement the mock-up.

I personally inspect it.

If I request corrections:

**discuss → correct → show again → inspect again**

Repeat until I explicitly approve the design.

---

# VERY IMPORTANT DISTINCTION

Always distinguish:

**DESIGNED**  
A concept/mock-up exists.

**APPROVED DESIGN**  
I personally accepted that design.

**IMPLEMENTED**  
The approved design has been converted into working website code.

**TESTED**  
Specific tests were actually executed.

**PUSHED**  
The tested implementation was committed/pushed to GitHub.

**LIVE**  
GitHub Pages deployed the pushed version.

**USER VERIFIED**  
I personally opened and inspected the actual live website.

**APPROVED / PROTECTED**  
I explicitly accepted the live result.

Never treat these states as interchangeable.

A mock-up is not an implementation.

Implementation is not proof that something works.

A successful GitHub push is not proof that the website works.

A successful GitHub Pages deployment is not proof that the website works.

Automated testing is not a substitute for my final live inspection.

---

# STEP 6 — IMPLEMENTATION APPROVAL

Only after I approve the design/concept may you propose implementation.

Before implementation, explain:

- what files will be created
- what files will be modified
- what existing approved functionality could be affected
- how protected work will remain protected
- how the change will be tested

Then wait for explicit implementation approval if that has not already been given.

---

# STEP 7 — IMPLEMENT LOCALLY

Implement ONLY the approved component/change.

Do not simultaneously begin another component.

Do not redesign protected components.

Do not introduce unrelated features.

Do not silently restructure the entire project.

Do not delete working functionality merely because another architecture seems cleaner.

---

# STEP 8 — LOCAL TESTING

Before pushing the implementation to GitHub, test it.

Testing must correspond to what was actually changed.

For visual/layout work, test relevant viewport sizes.

For interactive work, test the actual interaction.

For games, test the actual game flow.

Do not report “working” merely because there are no syntax errors.

---

# STEP 9 — REGRESSION TESTING

Check that the new work has NOT broken previously approved/protected work.

This becomes increasingly important as the site grows.

Previously fixed problems become regression requirements.

Do not reintroduce them.

---

# STEP 10 — REPORT BEFORE/AROUND PUSH

Clearly report:

- what was implemented
- files created
- files modified
- tests actually run
- what passed
- what failed
- anything still requiring manual inspection

Never hide failures.

If something fails:

STOP.

Explain:

- what failed
- why
- what you believe caused it
- what correction you propose

Do not repeatedly retry the same failed approach silently.

---

# STEP 11 — GITHUB

After the approved implementation has passed the required local checks, commit/push the exact tested state to:

**NSAdyad/the-haunted-realm**

using the existing repository/branch workflow.

Do not create additional repositories unless I explicitly request one.

Do not reset repository history.

Do not force-push unless I explicitly approve and there is a genuine reason.

Do not delete repository content merely to solve a deployment problem.

---

# STEP 12 — VERIFY GITHUB

After pushing, verify:

- push succeeded
- expected commit exists remotely
- local and remote state correspond
- expected website files are present
- protected assets were not unexpectedly modified

Report the commit identifier.

---

# STEP 13 — GITHUB PAGES

Allow the existing GitHub Pages deployment to publish the new commit.

Do NOT repeatedly change Pages settings.

Current approved Pages configuration is:

**main → /(root)**

Do not change that configuration unless a genuine technical requirement arises.

If you believe it needs changing:

STOP and explain why before changing it.

---

# STEP 14 — VERIFY DEPLOYMENT

Verify that GitHub Pages actually deployed the intended commit.

A green deployment alone does NOT mean the website itself is correct.

---

# STEP 15 — LIVE-SITE CHECK

Check the actual live URL:

`https://nsadyad.github.io/the-haunted-realm/`

Test the relevant component on the deployed website.

Check for:

- missing files
- broken paths
- broken images
- JavaScript errors
- navigation failures
- layout problems
- incorrect asset paths
- GitHub Pages subdirectory/path issues
- interaction failures
- viewport problems relevant to the component

---

# STEP 16 — STOP FOR MY PERSONAL INSPECTION

This is mandatory.

After deployment/testing, STOP.

Give me the live URL and tell me exactly what I should inspect.

I will personally open the actual website.

I may test it on:

- laptop
- desktop
- projector
- tablet
- mobile

depending on the component.

Do NOT begin the next component while I am inspecting the current one.

---

# STEP 17 — CORRECTIONS

If I find a problem:

Do not immediately start randomly changing things.

First understand the problem.

Explain:

- what went wrong
- likely cause
- proposed correction
- what the correction could affect

Then make only the approved correction.

After correction repeat the necessary cycle:

**implement → test → regression test → push → verify GitHub → deploy → verify live site → I inspect again**

Continue until the live result is correct.

---

# STEP 18 — APPROVED / PROTECTED

Only when I explicitly approve the actual live component may it be marked:

**APPROVED / PROTECTED**

Once protected, future development must preserve it unless:

1. I explicitly request a change, or
2. a genuine technical dependency requires a change.

If #2 occurs, explain the dependency and obtain approval before making the substantial change.

---

# STEP 19 — ONLY THEN MOVE FORWARD

Only after the current component is APPROVED / PROTECTED do we begin the next component.

For example:

**Landing Page**
→ live test
→ corrections
→ approval/protection

THEN

**Navigation**
→ live test
→ corrections
→ approval/protection

THEN

next activity/component

and so forth.

Never develop several future components merely because you already know they will eventually be required.

---

# PERMANENT REGRESSION REQUIREMENTS FROM PREVIOUS FAILED BUILDS

The following failures occurred repeatedly in previous versions.

They must be treated as permanent warnings/regression requirements.

## A. TEACHER/STUDENT LOGIN

Do NOT recreate the old separate Teacher Mode / Student Mode architecture automatically.

The intended future live-participation model is simpler:

**host starts session → join code appears → participants enter code → participants join**

No participant account should be required.

Do not build this system yet.

This is a future requirement.

---

## B. REMOVING ONE FEATURE MUST NOT BREAK EVERYTHING ELSE

Previous attempts removed unwanted teacher/student systems and other functionality subsequently stopped working.

Therefore dependencies must be understood and regression-tested.

---

## C. PROJECTOR / PRESENTATION FAILURES

Previous versions repeatedly had:

- top content cut off
- bottom content cut off
- inaccessible controls
- overlays covering content
- oversized images
- bad scrolling
- layouts failing on classroom projectors

For relevant components, future testing must include realistic presentation conditions.

At minimum where applicable:

**1920 × 1080 projector/classroom**

alongside normal desktop/laptop testing.

Tablet/mobile testing must also be performed where applicable.

---

## D. CLICK / TOUCH / KEYBOARD FAILURES

Previous versions contained controls that appeared visually but did not work reliably.

Where relevant, verify actual:

- mouse interaction
- touch interaction
- keyboard interaction
- buttons
- navigation
- reveal controls
- next/previous controls
- host controls

A visible control is NOT automatically a working control.

---

## E. GAMES DID NOT ACTUALLY WORK

This is one of the most important previous failures.

Previous games looked like games but did not work end-to-end.

For every future game:

A rendered interface does NOT count as a working game.

Actual workflows must eventually be tested.

For multiplayer activities, this may include:

**host creates session  
→ code appears  
→ participant joins  
→ host sees participant  
→ activity begins  
→ participant answers/buzzes  
→ host receives state  
→ scoring works  
→ progression works  
→ leaderboard works where applicable  
→ activity completes**

Do not build this now.

Record it as a permanent future testing requirement.

---

## F. GITHUB / GITHUB PAGES

Do not create repeated replacement repositories.

We now have the repository:

**NSAdyad/the-haunted-realm**

Use it.

Do not repeatedly alter GitHub Pages configuration to solve website-code problems.

Diagnose whether the problem is:

- repository
- deployment
- paths
- website code
- assets
- JavaScript
- responsive layout
- application logic

before changing infrastructure.

---

# CURRENT NEXT STEP

After recording this workflow, DO NOT implement anything.

We return to the current:

**Landing Page visual review — REVIEW / NOT IMPLEMENTED**

That review includes the most recent revisions to:

- Echoes of the Past
- The Book of Shadows
- Door to Darkness
- Hotel Transylvania
- supernatural activity-name typography
- controlled focus study
- small-screen lettering study

I still need to personally inspect and approve/correct that review.

---

# ASK

For this message only:

1. Confirm that you understand this complete workflow.
2. Record these requirements as the project's permanent development/regression procedure.
3. Confirm the current GitHub/GitHub Pages state.
4. Confirm that the Landing Page remains REVIEW / NOT IMPLEMENTED.
5. Confirm that you will NOT create `index.html` or implement the Landing Page until I explicitly approve the visual design and authorize implementation.
6. Confirm that after future implementation we will test locally, push to GitHub, verify deployment, inspect the actual live site, correct problems if necessary, and only then protect the component.
7. Identify any conflict you see in these instructions now rather than silently interpreting around it.

Then:

**STOP.**

Do not implement anything.

Do not push anything.

Do not change GitHub.

Do not change GitHub Pages.

Wait for my next instruction.