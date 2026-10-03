# The Haunted Realm

The official project-facing name is **The Haunted Realm**. Do not change it without the user's explicit request.

## User approval workflow

Work on one meaningful step at a time. Information and design approval do not automatically authorize implementation. Explain proposed changes, their method, scope, effects, and relevant choices; wait for explicit approval. Implement only the approved step, verify it, report actual results, and stop for the user's inspection. Only the user's explicit final approval protects a completed component. Do not start the next component independently. Report failures and proposed corrections rather than silently retrying. Preserve supplied content and previously approved work. No emojis; use realistic, atmospheric, spooky visuals.

## Permanent development and regression procedure

Follow the complete user-authored procedure in `docs/the-haunted-realm-development-workflow.md`, recorded on 2026-10-02. Read it before proposing or performing future implementation, testing, GitHub or deployment work. Work through its stages separately; do not skip stages, combine them for convenience or work ahead. Information, silence and design approval do not authorize implementation.

Keep these states distinct: DESIGNED; APPROVED DESIGN; IMPLEMENTED; TESTED; PUSHED; LIVE; USER VERIFIED; APPROVED / PROTECTED. Report only states supported by actual work or the user's explicit approval. Previously approved/protected background, title and navigation assets retain their protection; their future implemented website behaviour requires separate live inspection and acceptance.

Before implementation, identify created/modified files, dependencies, effects on protected work and the testing plan, then obtain explicit implementation authorization if not already given. Implement only that approved change. Execute relevant local and regression checks, report actual results and limitations, and stop on failure to explain the cause and propose the correction rather than silently retrying.

For future authorized implementations that pass the required checks, commit/push the exact tested state to the existing repository and branch workflow; verify the remote commit, website files and protected assets, and report the commit identifier. Verify Pages deployed that intended commit, then test the actual live website including relevant paths, images, JavaScript, controls and viewport behaviour. Stop with the live URL and specific inspection instructions for the user. Only the user's explicit acceptance of the actual live component protects that implementation and permits moving to the next component. Corrections require understanding/proposal/approval and the necessary repeated testing, GitHub, deployment and live-inspection cycle.

Permanent regression requirements include dependency checks when removing features; relevant 1920 x 1080 classroom/projector, desktop/laptop, tablet and mobile checks; actual mouse, touch and keyboard interaction; and complete game flows rather than rendered interfaces alone. Future participation uses host-created sessions and join codes without participant accounts; do not recreate separate Teacher/Student Mode architecture. Multiplayer tests must cover session creation, joining, host visibility, answers/buzzes, scoring, progression, applicable leaderboards and completion. These are future requirements, not authorization to build them now.

Use `NSAdyad/the-haunted-realm`; do not create replacement repositories, reset history, force-push without explicit approval, delete content to solve deployment problems or repeatedly change Pages settings to solve code problems. Diagnose the actual repository/deployment/path/code/asset/layout/logic cause. If a genuine technical dependency requires a protected design or Pages configuration change, stop, explain it and obtain approval before changing it.

## Protected global background

The user explicitly said **BACKGROUND APPROVED** on 2026-10-01. The exact protected background is:

- File: `outputs/the-haunted-realm-background-corrected-review-v3.png`
- Dimensions: 1536 x 1024 pixels; 3:2; PNG.
- SHA-256: `1561627199D2DA3412C5D5E49143A6B699201659AD1CEE56A38CEB8E96F28C06`
- Approval record: `outputs/the-haunted-realm-background-approval.md`

This exact file is the global visual source of truth. Do not regenerate, redesign, replace, recolour, crop destructively, or modify the scene, witch, window presence, lighting, perspective, image edges, or any other image content without the user's explicit request. Responsive display cropping may be proposed separately; it must not alter the protected source file.

Preserve the original backup `outputs/the-haunted-realm-background-review-v1.png` with SHA-256 `63392BF751F4C5518A26E9D82188C3C29CDCEB61B9A50C6E8F2F32BB34BC668F`. The enhanced v2 image is rejected and must never become the global background.

Before any authorized image operation, verify the protected file and backup against their recorded hashes. Do not silently repair or replace a mismatch; report it and stop image work.

Future pages and activities must inherit this background through one shared global background system. Do not introduce competing full-screen background images, full-screen black replacements, or unnecessary opaque layers covering it. Local readable content panels are permitted when approved.

## Protected Landing Page title

The user explicitly said **TITLE APPROVED** after visually inspecting the centred Ancient Village Sign on 2026-10-01. The title is now **APPROVED / PROTECTED**.

- Exact wording: **THE HAUNTED REALM**.
- Exact rendered title: `outputs/the-haunted-realm-title-approved.png`, a 650 x 215 RGBA PNG.
- Rendered asset SHA-256: `5F3DB4E9112D076A73E22587FCAEE26022B2188993A1DB6ABBB7A912ABF68A4A`.
- Approved visual/position reference: `outputs/the-haunted-realm-title-option-1-centred-review-v2.png`.
- Reference SHA-256: `1A4B8C14C4229B0C2E68DB47086B0A741C667930B16E531DCB2455905A0C7942`.
- Original artwork backup: `outputs/the-haunted-realm-title-original-artwork-backup.png`.
- Artwork backup SHA-256: `D40B8107D55723CD6976C880905564458DCA17082D55AAAF7F561D6DC6D3F7C1`.
- Approval record: `outputs/the-haunted-realm-title-approval.md`.

The rendered asset exactly reproduces the approved mock-up when placed at x=443, y=65 on the protected 1536 x 1024 background. The complete sign is 650 x 215, with bounds (443,65)-(1093,280), horizontal centre x=768, and equal 443-pixel horizontal margins. Preserve this upper-centre placement and scale.

Protect the Ancient Village Sign design, broad gold/amber Gothic lettering, aged dark-oak plaque, tarnished bronze edging, skull, carved/thorn ornament, fine cobwebs, all existing details, and realistic atmospheric appearance. Do not redesign, regenerate, replace, resize, reposition, recolour, trim, animate, or otherwise modify the approved title without the user's explicit request. Do not automatically resize or reposition it for responsive layouts; any adaptation needs separate user approval. Preserve the rendered asset, original artwork backup, and approved reference unchanged. Verify their hashes before authorized image operations, and report any mismatch rather than silently repairing or replacing it.

The title remains a separate transparent asset. Do not bake it into or alter the protected global background.

## Protected navigation design

The user explicitly stated **NAVIGATION DESIGN = APPROVED / PROTECTED** on 2026-10-01 after inspecting the latest Option B iron/glass redesign. Both horizontal Home and vertical left-side activity presentations are protected.

- Approval record: `outputs/the-haunted-realm-navigation-approval.md`.
- Exact protected references and material-layer hashes: `outputs/the-haunted-realm-navigation-approved-assets.json`.
- Home reference: `outputs/the-haunted-realm-navigation-b-home-redesign-review-v3-final.png`; SHA-256 `3F9F352DEEBADD00B3B590F71E7E3370E882064C42B6FE7D953F2D13181E5DE3`.
- Activity reference: `outputs/the-haunted-realm-navigation-b-activity-redesign-review-v3-final.png`; SHA-256 `A2554321B13D1DFC384AA6C38C400A404C1A8B2328A80B600A0770AD00C119E1`.
- Both references are 1536 x 1024. Exact navigation-only RGBA overlays, iron/glass frame and slender chain artwork are preserved separately in `outputs/` under `the-haunted-realm-navigation-approved-*` filenames. Preserve original working artwork/backups as well.

Protect corroded iron framing, aged transparent glass, slender chains, fractured/weathered details, fine cobwebs, open construction with scenery visible through and between elements, clear readable lettering, current-destination amber/gold illumination, distinct identity from the Ancient Village Sign, and realistic cinematic haunted appearance. Do not restore opaque oak title-like plaques or a large solid navigation backing panel.

Do not redesign navigation without an explicit user request. If a genuine technical dependency requires a design change, explain it and obtain approval before changing anything; do not infer authorization from the dependency. Verify the navigation manifest and existing background/title hashes before authorized asset operations. Report mismatches and stop instead of silently replacing assets. Do not rerun review rendering scripts to overwrite protected files.

The IMAGE spaces, numbered labels, displayed example count and Activity 3 selected-state example remain temporary. They do not approve final activity content, names/order, icons or a permanently selected destination. Approval protects the shared appearance, not those example values.

## Future activity navigation visuals and expansion

Every future activity must receive its own unique realistic thematic visual identifier based on that activity's approved content, theme, supplied information and references. It must be realistic, cinematic, atmospheric, physically believable, professionally integrated into The Haunted Realm, and haunted/spooky where appropriate. An activity-related object, scene, symbol, environment or character/detail may be used when supported by its actual approved information.

No emojis, emoji-style graphics, cartoons, clip-art, flat vector icons, generic app icons or random unrelated symbols. Do not invent final activity images in advance or reuse generic symbols as substitutes.

Create activity visuals one activity at a time after its information is supplied: review approved information; propose the visual concept; show the proposed/generated visual; stop for inspection; only after the user's explicit approval may it permanently replace that activity's temporary IMAGE space. A new review copy may show the proposed candidate in its reserved space for inspection without changing an archived study or implementing navigation. Do not create other activity visuals ahead of the user's authorized single step.

Navigation must support additional activities without an eight-activity limit. Activities 9, 10, 15 and later additions use the same system and receive their own individually approved realistic visual identifiers. Do not hard-code capacity based on mock-up examples.

## Protected Echoes of the Past navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **Echoes of the Past — APPROVED / PROTECTED — NAVIGATION IMAGE**.

- Asset: `outputs/the-haunted-realm-echoes-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `635C75D8C030905D103547E41690216A7431B8003C41D672CD49F4492D670E05`.
- Approval record: `outputs/the-haunted-realm-echoes-navigation-image-approval.md`.
- Approved navigation-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-echoes-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails as well.

Protect the approved artwork and appearance: ancient roundhouse, weathered stone, cold mist, ember-lit doorway and realistic historical atmosphere. Do not regenerate, redesign or replace it without the user's explicit request. If later live implementation reveals a genuine technical problem requiring adaptation, explain it first and obtain approval before changing it. Verify its recorded hash before and after authorized image operations.

Record the mobile text showing through transparent glass separately as **NAVIGATION / MOBILE READABILITY — LIVE VALIDATION REQUIREMENT**. Test underlying actual page content during eventual navigation implementation. Any correction proposal concerns navigation/background treatment rather than unnecessarily changing approved Echoes artwork. Do not solve this issue now. This image approval does not protect final geometry or implemented navigation behaviour.

## Protected The Cursed Quest navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **The Cursed Quest — APPROVED / PROTECTED — NAVIGATION IMAGE**.

- Asset: `outputs/the-haunted-realm-cursed-quest-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `769DCC3822B08FAD9FF14DCD38E1D519CE06E35A5D244AC5F3E804EC5FBEF3AE`.
- Approval record: `outputs/the-haunted-realm-cursed-quest-navigation-image-approval.md`.
- Shared approved-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-cursed-quest-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails.

Protect the realistic iron-bound chest, old lock, parchment, supernatural illuminated seam, cold chamber atmosphere and approved image appearance. Do not regenerate, redesign or replace it without an explicit user request. Explain any adaptation required by a genuine later live implementation problem and obtain approval before changing protected work. Verify this asset and Echoes against their recorded hashes before and after image operations. The Cursed Quest remains a factual quiz/challenge based on Echoes; supernatural presentation must not distort or fictionalize quiz facts.

## Protected The Book of Shadows navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **The Book of Shadows — APPROVED / PROTECTED — NAVIGATION IMAGE**.

- Asset: `outputs/the-haunted-realm-book-of-shadows-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `92B2113248B402BCFC3FC6CF0D7B4C74235FB50265ED7547D95168F5E1E144AF`.
- Approval record: `outputs/the-haunted-realm-book-of-shadows-navigation-image-approval.md`.
- Shared approved-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-book-of-shadows-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails.

Protect the dominant book, worn leather, broad aged pages, restrained spectral illumination, uncluttered realistic cinematic appearance and approved navigation-size identity. Do not regenerate, redesign or replace it without the user's explicit request. Explain any adaptation required by a genuine later live implementation problem and obtain approval before changing protected work. Verify this asset, Echoes and The Cursed Quest against their recorded hashes before and after image operations. This approval concerns navigation artwork only, not implemented vocabulary content or live website behaviour.

## Protected Fastest Finger First navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **Fastest Finger First — APPROVED / PROTECTED — NAVIGATION IMAGE**, including acceptance of its reported small-size limitation.

- Asset: `outputs/the-haunted-realm-fastest-finger-first-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `7F2B22364E94AE8BD820086996C70E387BC472328DA4444C4035D9ED9495A975`.
- Approval record: `outputs/the-haunted-realm-fastest-finger-first-navigation-image-approval.md`.
- Shared approved-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-fastest-finger-first-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails.

Protect the illuminated mechanical plunger, aged metal base, active amber light, restrained spectral light and competing-device atmosphere. The reduced visibility of background competitors/mist at navigation size is expressly accepted; do not independently revise it. Do not regenerate, redesign or replace the image without the user's explicit request. Explain any adaptation required by a genuine later live implementation problem and obtain approval before changing protected work. Verify all four approved navigation images before and after image operations. This approval concerns artwork, not implemented game mechanics or live website behaviour.

## Protected Words of the Feast navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **Words of the Feast — APPROVED / PROTECTED — NAVIGATION IMAGE**, including acceptance of reduced fine detail at navigation size.

- Asset: `outputs/the-haunted-realm-words-of-the-feast-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `A86B35F797A3639142B65D94AD938DF011D371D7174B8C67C93A9C413C7E98E7`.
- Approval record: `outputs/the-haunted-realm-words-of-the-feast-navigation-image-approval.md`.
- Shared approved-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-words-of-the-feast-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails.

Protect the dominant aged menu, antique cutlery, partial plate and cinematic supernatural dining atmosphere. Reduced fine menu writing, cutlery detail and vapour at navigation size are expressly accepted; do not independently revise them. All writing is visual decoration only, not approved lesson/vocabulary content. Do not regenerate, redesign or replace the image without the user's explicit request. Explain any adaptation required by a genuine later live implementation problem and obtain approval before changing protected work. Verify all five approved navigation images before and after image operations. This approval concerns artwork, not implemented lesson content or website behaviour.

## Protected The Phantom Order navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **The Phantom Order — APPROVED / PROTECTED — NAVIGATION IMAGE**, including acceptance of reduced fine detail at navigation size.

- Asset: `outputs/the-haunted-realm-phantom-order-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `5EDCC385202CBE7BC3E87D15C76EECDE4DD6D3E080BB10B8A3B40AEBE5DFA492`.
- Approval record: `outputs/the-haunted-realm-phantom-order-navigation-image-approval.md`.
- Shared approved-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-phantom-order-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails.

Protect the dominant curling ticket, antique serving tray, service hatch, cold illumination and supernatural materialization. Diminished fine writing/materialization detail at navigation size is expressly accepted; do not independently revise it. Any generated writing is decorative only, not approved vocabulary, game content, orders or clues. Do not regenerate, redesign or replace the image without the user's explicit request. Explain any adaptation required by a genuine later live implementation problem and obtain approval before changing protected work. Verify all six approved navigation images before and after image operations. This approval concerns artwork, not implemented game content or website behaviour.

## Protected Door to Darkness navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **Door to Darkness — APPROVED / PROTECTED — NAVIGATION IMAGE**, including acceptance of reduced fine restaurant details at navigation size.

- Asset: `outputs/the-haunted-realm-door-to-darkness-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `CA6780FCFD224FCD161BC710E24C5705A007CAC85E8DC366DB717C1B2BF99389`.
- Approval record: `outputs/the-haunted-realm-door-to-darkness-navigation-image-approval.md`.
- Shared approved-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-door-to-darkness-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails.

Protect the doorway/threshold, partially open ancient door, reception near the entrance, dining depth, cold exterior/warm opening and realistic cinematic restaurant atmosphere. Diminished fine restaurant details at navigation size are expressly accepted; do not independently revise them. Do not regenerate, redesign or replace the image without the user's explicit request. Explain any adaptation required by a genuine later live validation problem and obtain approval before changing protected work. Verify all seven approved navigation images before and after image operations. This approval concerns navigation artwork, not implemented restaurant/customer-journey content or website behaviour.

The relatively small departure/bill cue in the separate larger Landing Page Door to Darkness scene remains an **UNRESOLVED SEPARATE OBSERVATION**. Preserve that scene unchanged; navigation-image approval does not resolve or approve the Landing Page observation.

## Protected Build the Haunted Banquet navigation image

On 2026-10-02 the user personally inspected review v1 and explicitly approved **Build the Haunted Banquet — APPROVED / PROTECTED — NAVIGATION IMAGE**, including acceptance of diminished arrangement/planning detail at navigation size.

- Asset: `outputs/the-haunted-realm-build-the-haunted-banquet-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `4279EB082241C1BAFC79E688D3ED5B2667F98E1C328222105C5842FB04C807D7`.
- Approval record: `outputs/the-haunted-realm-build-the-haunted-banquet-navigation-image-approval.md`.
- Shared approved-image manifest: `outputs/the-haunted-realm-navigation-images-approved.json`.
- Appearance reference: `outputs/the-haunted-realm-build-the-haunted-banquet-navigation-entry-review-v1.png`; preserve existing 38- and 34-pixel thumbnails.

Protect the spectral hand, empty plate, loose cutlery, materials, planning sheets and active unfinished preparation identity. The user accepts that the arranging gesture and planning details are clearer when enlarged; do not independently revise this limitation. Any generated planning-material writing is decorative only, not approved lesson content. Do not regenerate, redesign or replace the artwork without an explicit user request. Explain any adaptation required by a genuine later live-validation problem and obtain approval before changing protected work. Verify all eight approved images before and after image operations. This approval concerns artwork, not implemented preparation, restaurant materials, role-play requirements or website behaviour.

## Protected Hotel Transylvania navigation artwork — entry approval pending

On 2026-10-02 the user personally inspected the generated artwork and explicitly approved **Hotel Transylvania — NAVIGATION ARTWORK APPROVED**. The exact artwork is protected from regeneration/redesign/alteration. The complete navigation entry remains **NOT YET FULLY APPROVED**; do not mark it APPROVED / PROTECTED — NAVIGATION IMAGE before the user's inspection of the corrected mobile presentation.

- Artwork: `outputs/the-haunted-realm-hotel-transylvania-navigation-image-review-v1.png`, 1254 x 1254 PNG.
- SHA-256: `B52E7ACCB7CF63C9964B9D679A3D03450D0803DD4EB14C74CCEDDAF91B50DBD3`.
- Artwork-only approval record: `outputs/the-haunted-realm-hotel-transylvania-navigation-artwork-approval.md`.
- Preserve the existing 34- and 38-pixel thumbnails in `work/hotel-transylvania-navigation-image-review-v1/`.

Protect the original spectral guest/waiter interaction, inhabited gothic hotel dining room, all characters, lighting, composition and details. Diminished fine faces/gestures at thumbnail size are accepted. Do not generate a replacement or modify the artwork. Keep it original to The Haunted Realm and avoid copying film characters, artwork, logo or distinctive film designs. Preserve the failed mobile-review attempt and all its original failure records byte-for-byte.

The user explicitly approved only a separate static bottom-scrolled mobile correction, using the same 34 x 34 thumbnail, exact name, iron/glass materials, font, frame, 288-pixel drawer width, 70-pixel row and spacing. Move the list to its existing bottom-scrolled state rather than adapting geometry. This is a raster review, not actual mobile navigation implementation or live validation. Verify the artwork and the earlier eight approved images before and after composition; stop for inspection afterward.

## Current navigation direction and canonical destination names

Follow `outputs/the-haunted-realm-navigation-current-design-status.md`, recorded on 2026-10-02. Every new study and eventual implementation representing intended navigation must use **Home** and these exact activity names, without abbreviation, renaming, substitution or translation:

1. Echoes of the Past
2. The Cursed Quest
3. The Book of Shadows
4. Fastest Finger First
5. Words of the Feast
6. The Phantom Order
7. Door to Darkness
8. Build the Haunted Banquet
9. Hotel Transylvania

Preserve historical review images containing numbered Activity labels unchanged; they are archived examples, not current destination names. Nine is the current list, not a capacity limit.

The 430-pixel laptop rail, 460-pixel projector rail and mobile drawer are **CURRENT DESIGN DIRECTION / SUBJECT TO LIVE VALIDATION**, not **APPROVED / PROTECTED FINAL GEOMETRY**. The general direction is acceptable for exploration only. Protected navigation material artwork and historical references remain protected; static studies do not establish approval of eventual activity-page behaviour, content space, scrolling, projector or mobile usability.

The separate activity-name lettering choice remains unresolved: Cursed stone inscriptions; Spectral apparitions; Possessed antique metal. Do not select or apply one without approval.

## Current authorization boundary

The background, title and navigation visual design remain approved/protected. The general Landing Page structure is approved in principle. The latest Landing Page visual review remains **REVIEW / NOT IMPLEMENTED** and has not received final visual approval. No Landing Page or navigation functionality, activities, games or live website entry point has been implemented. Do not create `index.html` or a placeholder, implement the Landing Page, revise artwork or start another component until the corresponding explicit approvals are given.

Preserve the exact latest review, including the revised Echoes of the Past, The Book of Shadows, Door to Darkness and Hotel Transylvania scenes, supernatural activity-name typography, controlled focus study and small-screen lettering study. Preserve its existing notes about the fully wolf-headed hotel guest, shifts in unapproved hotel interior details and the relatively small departure/bill cue in Door to Darkness. Do not replace or overwrite this review or the six navigation/lettering decision studies.

Verified infrastructure as of 2026-10-02: public repository `NSAdyad/the-haunted-realm`, local project `C:\Users\DELL\Documents\Codex\2026-09-30\ar`, branch `main` tracking `origin/main`, Pages **Deploy from a branch -> main -> /(root)**, URL `https://nsadyad.github.io/the-haunted-realm/`. The initial snapshot commit is `125798046dfc25e5b97e331ffc86112468c0f20d`; the successful deployment contains design/review material and no `index.html`, `index.md` or `README.md` entry point. The current root 404 is expected because there is no implemented website; do not independently fix it or change Pages configuration. Recheck actual infrastructure when future work requires it rather than assuming this dated snapshot remains current.

The user's latest single-step authorization is to record Hotel Transylvania as **NAVIGATION ARTWORK APPROVED**, protect its exact artwork, preserve the failed mobile attempt/history, and create ONLY a separate **static bottom-scrolled mobile entry review correction**. The complete entry remains **NOT YET FULLY APPROVED** pending personal inspection. Reuse the existing 34 x 34 thumbnail and exact Hotel Transylvania name, iron/glass treatment, lettering, frame, width, row dimensions and spacing. Verify the zero-offset reconstruction against the archived mobile study before presenting the same drawer at its bottom-scrolled state; do not change geometry to fit. Preserve all eight earlier approved images and the Hotel artwork byte-for-byte, all protected background/title/navigation materials, all old reviews and all unresolved Landing observations. Mobile transparency/readability and geometry still require live validation; Landing lettering, Door departure/bill cue and Hotel Landing guest/interior observations remain unresolved separately. Do not generate images, create another activity, implement navigation or the website, create index.html, commit, push or change GitHub/Pages/live. Save the correction separately and stop for the user's personal inspection.

## Hotel navigation-review mobile presentation failure

The new Hotel Transylvania artwork and desktop samples were created, but static visual inspection found the copied mobile sample incomplete: the archived drawer clips the final entry and its name is absent. Preserve the candidate and failed review attempt. See `work/hotel-transylvania-navigation-image-review-v1/review-notes.md` and `verification.json`. Do not treat the original board footer as a successful mobile visibility check. Image work stopped; no retry or protected-asset change occurred. The proposed separate static bottom-scrolled mobile review requires explicit user correction approval before rendering. The existing original Hotel Landing Page guest/interior observations remain separate and pending.

## Authorized mobile-review correction after preserved failure

On 2026-10-02 the user approved the proposed separate static bottom-scrolled review correction. The failure section above is preserved as history; it does not authorize overwriting the failed attempt or solving actual mobile readability/geometry. See the separate artwork approval record and `work/hotel-transylvania-mobile-bottom-scrolled-review-v1/` for this correction. Full navigation-entry approval remains pending.

## Current phase — local integrated shell authorization (2026-10-02)

The user personally approved Hotel Transylvania's corrected mobile entry. It is now **APPROVED / PROTECTED — NAVIGATION IMAGE**; earlier artwork-only/entry-pending statements describe the historical stages. All nine current navigation images are fully approved and protected; see `outputs/the-haunted-realm-navigation-images-complete-set-approval.md` and the shared manifest. Nine is not a permanent architecture maximum. Preserve all original failed/corrected mobile review material and records unchanged.

Follow the latest complete instruction at `docs/the-haunted-realm-integrated-shell-and-cumulative-workflow.md`, which supersedes earlier current-authorization notes. The only authorized implementation is one local integrated Home/Landing shell, shared navigation and nine content-free destination shells, using existing assets. No educational content, games, multiplayer, role-play content, other design task, commit, push, Pages change or deployment. Use one maintainable shared activity registry, validate actual local interactions and layouts, report precise results/files/states and stop for inspection.

The user separately approved proportional **display-only title scaling below a 650-pixel viewport width**. Preserve the exact title PNG, upper-centred placement and 650 x 215 display at wider viewports. This exception supersedes the earlier prohibition on automatic narrow-screen scaling; it authorizes no other title change.

Record TEST FAILURE details before any correction. Internal non-destructive fixes within this implementation scope may proceed after recording; protected design/scope changes require a DEPENDENCY CONFLICT report and explicit approval. Test cumulatively across Home, shared navigation and all implemented activities, including known clipping, mobile scrolling, projector and routing risks. Always read/write manifest records explicitly as UTF-8. Mobile transparency/readability, provisional geometry, unresolved Landing lettering and Door/Hotel Landing observations remain pending until the relevant required validation/approval; do not silently redesign to address them.

The user separately approved temporarily concealing main Home/activity content only while the overlay Activities drawer is open after local testing showed visual collisions through glass. Keep the global background/navigation visible, restore title/content unchanged when closed and leave the permanent desktop rail unaffected. This display exception authorizes no artwork or geometry change.

## User-inspected shell correction and deployment preparation (2026-10-02)

The latest controlling instruction is `docs/the-haunted-realm-user-inspection-and-presentation-workflow.md`. The user personally likes the appearance and confirms activity-page left navigation works fantastically: **USER INSPECTION — WORKING WELL / REGRESSION-PROTECTED BEHAVIOUR**. Preserve its successful design/order/current state/images/background relationship and regression-test every activity when shared code changes. The complete shell is not yet approved.

Authorized scope: correct Home one-screen presentation fit and destination-navigation behaviour, implement one shared site-level Presentation Mode with graceful fullscreen fallback, necessary supporting responsiveness, cumulative local tests and exact preparation for the existing GitHub repository/main/root. At1920x1080 Presentation Mode, all primary Home activity selection must be usable without ordinary document scrolling; mere bottom reachability is insufficient. Preserve the exact title/approved exceptions/artwork and successful activity rail. No activity content, games, multiplayer, new artwork, unrelated scene corrections or other project.

Only after local gates pass report **READY FOR CONTROLLED GITHUB DEPLOYMENT — AWAITING USER APPROVAL**, exact include/exclude paths, tests/protected verification/non-blocking unresolved items and proposed commit message. **STOP before any commit/push**; later explicit approval is required. No Pages configuration change. Record failures before scoped corrections and retain history. Local emulation is not physical-device validation. Final Landing lettering and Door/Hotel scene observations remain unresolved.
