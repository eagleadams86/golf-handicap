# Golf Handicap — rules for Claude sessions

A golf handicap tracker that shows two figures side by side: a configurable rolling method —
**the league handicap** (default: the average of the last 5 rounds) — and the official World
Handicap System index. Deployed via GitHub Pages:
https://eagleadams86.github.io/golf-handicap/

Built for a friend's dad, who has always worked his handicap out from his last 5 cards in
Excel. **The rolling method is the point of the app, not a novelty** — it is what the page
leads with, and the official figure is the one shown alongside for reference. Don't reverse
that emphasis.

- **Names in Golfers & Courses are edited IN THE BOX** (2026-08-21), not through a `prompt()` behind an underlined name — Sprint Predictability's and Flow Metrics' arrangement. Three rules the handlers must keep, all of them the siblings': the record is **re-found by id on every keystroke** (a sync adoption or another tab can replace `state` while the dialog is open, and a rename onto a detached copy is lost silently); the length cap is applied **in code as well as `maxlength`**, because a paste ignores the attribute; and `save()` must **not** redraw the list being typed in — that replaces the input and throws away the caret, so `render()` covers the rest of the page and this list is left alone.
- **A course's tees are reached by the PENCIL in its row actions**, not by its name. The name had to stop being a link when it became a box, and the row actions are where every other per-row action in that window already lives. Neutral `.icon-btn`, not `.danger`: editing tees is not destructive.
- **The leaderboard row is clickable as a whole, and there is no "you" pill.** One delegated listener on the table finds `closest('[data-golfer]')`, so the row and the underlined name are the same action rather than two handlers that could drift — the name stays a real `<button>` because a `<tr>` cannot be focused or pressed from a keyboard. The tinted row keeps its own colour on hover: it is already the row you are on, and lighting it up as a destination is the one place this could mislead. The pill went because the tint already says it, and on a shared view nobody in the table is the person reading.
- **The header buttons wear a glyph in front of the word** (2026-08-21) — `☰ Golfers & Courses`, `⚙ League Rules`, `⇩ Back up`, `↗ Share`, `☁️ Sign in to sync`. Plain text characters, NOT emoji and not an icon font: one more file to fetch is the last thing a header painted this early needs, and a text glyph inherits the theme's colour for free, so it can never become the thing that carries a meaning by hue. Each is `aria-hidden` — the word beside it is already the whole label. The glyphs are Money Map's own where the same button exists there, so one action looks the same in every app; ☁️ keeps its emoji because the sync module rewrites that label as the state changes. Added to Sprint Predictability, Flow Metrics and PAPTrack in the same commit.
- **`color-scheme` is set per theme** alongside the chart colours — `dark` for midnight and dark, `light` for light AND sepia (sepia is a warm *light* theme). It overrides nothing in the pack; it is how the page tells the browser which way round it is, so browser-drawn UI follows. Without it the calendar button inside `<input type="date">` was a near-black glyph on a near-black field on the dark themes, and that glyph is not restylable from CSS. It fixes the number spinners, the checkbox and the scrollbars too. Sprint Predictability, Flow Metrics, Money Map and PAPTrack already had it; this app and the lottery pages were the last without.
- **With NO ROUNDS the page shows only the Rounds card's CONTENTS, and the Leaderboard tab waits for a SECOND golfer** (`renderEmptyState`, called from `render`). Current Handicap, At a Glance, Handicap Over Time and Course Handicap are all reports ON rounds — with none logged each was a heading over a dash, four cards of chrome between a first-time visitor and the one button they need. The Leaderboard ranks golfers against each other and with one is a table of one row. Both are pure display: nothing is deleted, nothing is stored, and the same `render()` puts it back. A shared view is skipped — `viewOnly` builds its own panel and hides the tablist itself. The empty state itself is `.empty.first-run`, which is deeper and wider than the plain `.empty` the app uses elsewhere, because it is now holding the whole page on its own rather than sitting under four occupied cards. **The Rounds card's own HEADING ROW goes with the other cards** (`#roundsHead`, 2026-08-22): "Rounds" over a card that says there are none, beside an `+ Add round` the empty state offers again — in the right order, under a sentence saying which comes first — is a title and a button competing with the one thing a first-time visitor is being asked to do. Because that hides the ONLY `+ Add round` on the page, **the empty state's primary button has to be the right NEXT step rather than always the first one**: with a course already saved it becomes `+ Add round` and opens the round dialog, and its lede drops the "add a course first" sentence the visitor has already followed. Take the heading back out of hiding and that adaptation stops being load-bearing — but don't, because they were changed together for a reason.
- **Golfers and courses live behind ONE header button, in one window (2026-08-21).** They were two buttons and two dialogs of the same shape, and adding a round often means adding one of each — which meant closing one window to open the other. `#manageDialog` is modelled on Sprint Predictability's "Teams, ARTs & PIs": a section per list, each opening with its own `<h3>` and the button that adds to it (`.sec-hd`), a sentence of context, then the table — and ONE Done for the pair. The add buttons sit in the section HEADINGS, not down beside Done, which is what makes it read as two lists rather than one long form.
  - **Adding a golfer is a `prompt()` now**, not a text field at the foot. That is the gesture RENAMING a golfer has always used here, so the two ways of typing a golfer's name are the same one, and the section is shaped like the courses one beside it.
  - **Row actions are `.icon-btn` squares**, ported from Sprint Predictability — one × per row, `--chrome-h` square, NEUTRAL at rest and red only on hover. The two colour declarations are written as `button.icon-btn.danger` to beat this app's own `button.danger`, which is red at rest: right for a full-width "Delete everything", wrong for a column of small squares.
  - **The course × is never disabled, whatever the round count.** A first attempt greyed it out while rounds pointed at the course, assuming deletion would take them with it — **it does not.** Rounds are kept and simply stop counting (`orphan` in `rowsFor`), and the course dialog's own Delete has always allowed it on those terms. Both routes now call `deleteCourse(id)` so the warning cannot say two different things.
- **The league method's name is DERIVED, never stored or typed.** `normalizeMethod` returns `autoName({window, use})`. It used to be a "What to call it" field in the League rule window, kept in step with the numbers by an `auto` flag that a hand-typed name cleared — and the comment on that flag already said what was wrong with it: "Rolling last 5" over a best-3-of-5 calculation is worse than no label. `src.name` is still read past and ignored, deliberately: older saved data and share links carry one, and there is nothing to migrate to. `DEFAULT_METHOD.name` is the one place it is written out, because `autoName` cannot be called before it exists.
- **The brand line carries a FIXED strapline** — `Golf Handicap · Charlie's Epic League Tracker` — matching Sprint Predictability's and Money Map's. It is the text that used to be typed into that "What to call it" box, which labelled the calculation rather than the app. `.brand` is **not** a flex row any more: with a strapline on the end, flex makes the name and the strapline two columns and the strapline then wraps inside its own narrow column on a phone instead of running on below. Inline flow, and the mark takes `vertical-align` rather than `align-items` — Sprint Predictability's arrangement, and its comment says why.
- **`.headbar select` wears the BUTTON palette, not the input one.** The base `select` rule gives every dropdown `--surface` on `--input-border`, which is right in a dialog where it sits beside text fields and is a thing you fill in. In the header it sits beside five buttons and is a thing you press, and the input colours made the golfer and theme pickers read as two dark holes in a row of raised controls. Same two tokens as `button`, so it is not a new colour — and the scope is what keeps dialogs right.
- **The app is INSTALLABLE on a Mac or a PC (2026-08-21), and offline is a separate, older thing.** `manifest.webmanifest` is what turns Chrome's "Install page as app…" into a real install — its own window, its own Dock/taskbar icon. Four things have to stay in step or installing silently stops being offered, with nothing but a console line to say so:
  - **`manifest-src 'self'` in the CSP.** It falls back to `default-src`, which is `'none'` here, so without the directive the manifest fetch is refused. Suspect this first.
  - **`make_favicon.py` writes the install icons too** — `icon-192.png`, `icon-512.png` (rounded, `purpose: any`, since nothing masks those) and `icon-512-maskable.png` (square, full bleed, since a launcher supplies its own outline). Nothing had to move for the maskable crop and the script records the arithmetic: the circular safe zone is a disc of radius 25.6 in the 64 viewport, the mark's furthest point (the flag tip, the stick foot, the ball) is 21.1 from centre, and its bounding box is centred on the tile. **Move the flagstick or grow the ball and re-check that number.**
  - **All four files are on `sw.js`'s SHELL allowlist, and `tests.html` pins that list by exact equality.** Adding an entry means editing the test too — that is the security review, by design. Their justification is written ABOVE the array, not between the entries: the suite pulls every quoted string out of the array straight from the source, comments and all, so a note inside it with an apostrophe in the prose hands that check a fake entry.
  - `<meta name="theme-color">` is rewritten by `applyThemeColor()` from the pack's `--bg`, so an installed window's title bar follows the theme instead of staying dark behind a light page.
  - **The manifest is deliberately NOT linked from `privacy.html`** — that is a policy page, not a surface anyone installs from, and a manifest on it would offer to install something the reader is not looking at.
  - Offline predates all of this and is unchanged: it is `sw.js`, network-first. The manifest adds the window and the icon, not the caching.
- **`--page-w` stays 1100px, and that is not drift.** Sprint Predictability, Flow Metrics, PAPTrack and the lottery pages are 1500 and Money Map is 2400; the family rule is that the CHROME is shared and the width is justified per app. This app's widest thing is an eight-column leaderboard, which goes sparse and gappy stretched to 1500 — tried and reverted. PAPTrack could take 1500 because its cards flow into columns rather than stretching; a table has no such move.
- **The rolling figure is called the LEAGUE handicap on screen**, and its settings dialog is
  reached from the header button **League rule**. It used to be "My method" everywhere; the
  rename is deliberate and total (2026-08-11) — the rule is one setting shared by every
  golfer in the app, which is exactly what makes the leaderboard a fair comparison, so
  naming it after the owner was wrong. The rule's *own* name (`method.name`, auto-generated
  as "Rolling last 5" or typed by the user) is a different string and still appears: as the
  sub-line under the figure, the leaderboard's column heading, the "used in" pills and the
  working-out heading. The front figure is titled "League"; don't put `method.name` back
  there.
- **Two tabs: My handicap and Leaderboard.** The panel on screen is driven by `data-tab` on
  `<html>`, set by the boot script in `<head>` **before first paint** — a tab restored by
  the script at the foot of the page would paint the handicap view and then jump. CSS does
  the switching; `setTab()` only keeps `aria-selected` and the roving tabindex in step. The
  tab is remembered in its own localStorage key (`gh-tab`), beside the theme and never in
  the saved data — it is where this browser is looking, not something about the golfers.
  With no script at all the attribute is never set and both panels show, which is the
  honest fallback. The tablist is Sprint Velocity's, arrow keys included.
- **On screen it is the "Leaderboard"; in the code it is `league`** (`#leaguePanel`,
  `renderLeague`, `rankLeague`). That is not drift: the view ranks the *league handicap*, so
  the code is named after the figure and the tab after what it shows.
- **`rankLeague()` is pure and pinned by tests.** Three rules that must not be "tidied": a
  golfer with no figure sorts to the FOOT with **no rank** (null sorting low would rank a
  golfer with no rounds first, the worst possible answer); ties share a rank and the next
  one skips (1, 2, 2, 4); and ties break by name so the order doesn't wander between
  renders.
- **`changeOverRounds()` is the one place the "change over 5 rounds" figure is worked out**,
  shared by the at-a-glance tile and the leaderboard's column. Two copies of that
  subtraction is how the same golfer ends up with two different trends on two screens.
- **Read-only share links are Team Dashboard's feature, ported.** `#share=<marker>.<b64url>`,
  marker 1 = deflate-raw and 0 = plain JSON. The payload is a *trimmed copy* built by the
  pure `buildSharePayload(state, ids)` — it takes the state as an ARGUMENT so tests can pin
  exactly what a link carries and what it must not: the chosen golfers, their rounds, only
  the courses those rounds used, and the settings (the figures are meaningless read under
  someone else's league rule). Nothing identifying, ever — no email, no uid, no theme; a
  test pins the exact key list. **How much history rides along is `windowRounds()`**, pure
  and pinned: `{ lastN }` counts PER GOLFER (a link for four people should carry four
  comparable records, not one golfer's twenty), `{ from }` is an inclusive date cutoff, and
  a window that leaves nothing leaves nothing rather than falling back to everything. A
  trimmed payload carries `from`/`lastN` so the recipient's banner can say so — **both
  handicaps are recalculated from what is in the link**, so a trimmed copy legitimately
  disagrees with the sender's screen, and that has to stay visible. `viewOnly` is decided
  before anything renders, `save()`
  returns early in it (a visitor very likely has their own rounds in that browser), the
  storage listener is muted, the rounds table's dates become text rather than editors, and
  the sync module is gated on `window.ghViewOnly` — signing in inside someone else's
  snapshot would push their rounds into the visitor's own document.
- **Headings are Title Case**, here and in every app in this family (`Current Handicap`,
  `Back Up & Restore`, `How These Are Worked Out`). Body copy, buttons, table column headers
  and field labels are unaffected.

- The app is **`index.html` plus `theme.css`** — no build step, no server, no npm, no bundler,
  no CDN calls beyond the Firebase SDK that optional sync loads. **It was one self-contained
  file until 2026-08-18**, when the palette moved from an
  inline transcription to the theme pack's generated `theme.css`, linked. That was the
  user's explicit call, made against the trade-off: every web app now reads the same bytes
  and cannot drift, at the cost of `index.html` no longer standing alone — **`theme.css`
  has to travel with it**, and opening the HTML off disk without it leaves the page
  unstyled. Don't re-inline the palette to "restore" the single file; the alignment is the
  point. Everything ELSE stays inline: no second script, no second stylesheet.
- No account is ever required. The only exception is an **optional** Google sign-in for
  cross-device sync, backed by the `golfhandicap-14246` Firebase project (auth + one
  Firestore doc per user, free tier). `FIREBASE_CONFIG` in the bottom `<script type="module">`
  block controls it; set it to `null` to force fully-local mode. The config is a public
  client config, not a secret — access is enforced by the Firestore rules.
- Firebase authorized domain is `eagleadams86.github.io`, so sync works at this
  `/golf-handicap/` path unchanged. The project's `authDomain`
  (`golfhandicap-14246.firebaseapp.com`) is **no longer** in the CSP's `frame-src` — it used
  to have to be, because the sign-in popup was an iframe from that host, but sign-in no longer
  goes anywhere near it (see the next rule). It stays in `FIREBASE_CONFIG` only because the
  SDK requires the field.
- **Sign-in uses Google Identity Services, not Firebase's popup.** `GOOGLE_CLIENT_ID` +
  `initTokenClient()` opens a popup straight to `accounts.google.com`, and the OAuth access
  token it returns is exchanged for the same Firebase session via `signInWithCredential`.
  Firebase's `signInWithPopup` is **gone on purpose**: it opens at
  `<project>.firebaseapp.com/__/auth/handler` first, and corporate filters block **individual**
  `firebaseapp.com` hostnames — per hostname, not per domain; two sibling apps were refused on
  a network where a third went through, with identical code. `firebaseapp.com` and
  `apis.google.com` are therefore **not** in the CSP; only `accounts.google.com` is, in
  `script-src`, `connect-src` and `frame-src`. `authDomain` stays in `FIREBASE_CONFIG` because
  the SDK requires it, but nothing loads it, so it no longer needs a matching `frame-src`.
  The client ID is **not** in `firebaseConfig` — Cloud Console → Credentials → *Web client
  (auto created by Google Service)*, whose **Authorized JavaScript origins** must list this
  app's origin (exact, port included) or Google returns `origin_mismatch`. All four web apps
  in the family do this, all confirmed working on the network that needed it, 2026-08-07.
  Auth is built with `initializeAuth`, **not `getAuth`** — `getAuth()` always wires in
  `browserPopupRedirectResolver`, which the SDK initialises at startup, pulling in
  `apis.google.com/js/api.js` for the popup-redirect gapi iframe nothing here reads (it showed
  up only as a CSP console error). The persistences passed in are `getAuth`'s own, in its
  order. Don't go back to `getAuth()` to "fix" a popup/redirect call — pass the resolver to
  that call instead. Same change in Team Dashboard, Sprint Velocity and PAPTrack.
- **`computeAll()` is the only place either handicap is calculated.** Every figure, tile,
  table, chart and the working-out panel reads from it. A new number takes its value from
  there or the screen starts disagreeing with itself.
- **`computeAll()` works in GAMES, not rounds, and the distinction is load-bearing**
  (2026-08-22). `c.counted` is the ROUNDS that count; `c.games` is what the maths runs on,
  after `pairNines()` has folded each pair of nines into one 18-hole record. Anything about
  the OFFICIAL WINDOW — "3 counting rounds", "best 8 of 20", the best differential, the
  per-course table — reads `c.games`; anything about what the golfer has LOGGED reads
  `c.counted` or `c.all`. Reading the wrong one is not a crash, it is a figure that is
  quietly out by one whenever a nine is in play. `c.pendingNine` is the odd nine still
  waiting, and it is named on screen rather than dropped.
- **A nine is scored against the NINE-hole rating, slope and par, or it is not scored at
  all.** `tee.rating9`/`slope9`/`par9` are optional and all-or-nothing (the course dialog
  refuses two of three). Never fall back to half the 18-hole figures: nine holes are not half
  as hard, and a fallback would look like an answer. A nine on tees without them gets `no9`,
  is excluded from `counted`, and says so in the rounds table and on the front page.
  **The PCC is HALVED for a nine**, and that one is the app's own reading rather than a
  quoted rule — PCC is published in strokes over a full round, so charging a nine the whole
  of it would double-count the moment the pair is added. It is written that way round in the
  README too; don't quietly promote it to a rule or quietly drop it.
- **`pairNines()` is pure and pinned.** Chronological, oldest-first, the two differentials
  ADDED, and the game dated to the SECOND nine — the games list has to come out in date
  order, because `indexHistory` walks it forward and measures the low index's 365 days from
  each entry's own date. A game carries `parts`, which is why `pickUsed()` credits both of a
  pair's rounds; `parts || [item]` keeps it working for the plain entries the tests pass.
- **The exceptional score reduction is the fourth part of the official calculation**, beside
  the best-8-of-20 window, the reduced-scores table and the caps — it was missing until
  2026-08-22, which made the README's "a faithful implementation of the published method"
  not quite true. Three things about it that a tidy-up would break, all pinned:
  - It is measured against the index the golfer **held before** the round (`out[i-1].whs`),
    never the one the round produces.
  - It does not stop with that round. `indexHistory` keeps a per-game `esrs` array and sums
    the **last 20** of them, so a reduction stays in force for 19 more scores, falls away as
    that round leaves the window, and two inside one window stack. One number adjusted and
    forgotten would be a different rule.
  - **Reduction first, cap second.** That is the published order, and it has a consequence
    that reads like a bug: under a HARD cap the figure is pinned either way, so the
    reduction can be swallowed. A test asserts the order explicitly and says so.
  It has its own setting (`applyEsr`, default on) beside `applyCaps`, for the same reason
  that one exists — to see the plain averaging underneath. Neither touches the league figure.
- **The playing handicap is the course handicap times an allowance, and the ALLOWANCE IS A
  DEVICE PREFERENCE.** `gh-allowance`, its own localStorage key beside the theme and the tab
  — it is what you are playing today, not a fact about the golfers, so it never enters the
  saved data, never travels in a share link, and needed no SCHEMA bump. Both places it
  appears (the Course Handicap card and Strokes on the Day) read the one variable through
  `setAllowance()`, so they cannot disagree. `playingHandicap()` rounds half AWAY from zero
  for the same reason `round1` does: a plus handicap is negative, and `Math.round(-2.5)` is
  `-2`, which would hand the better player a shot.
- **The rounds filter never reaches the maths, and its markup is written once.** It filters
  what is SHOWN and the line beside it says so out loud. The controls live in the HTML rather
  than being redrawn by `render()` — a render that replaced them would replace the box being
  typed in and throw away the caret, the same rule the name boxes follow. It appears only
  past `FILTER_FROM` rounds.
- **Adding a round offers every golfer, and nobody is ticked but the one on screen.** A
  checkbox that starts ticked is a round logged for someone who did not play, and an
  unnoticed extra round is far worse than an extra tap. A row's score box is disabled until
  its row is ticked, and the validation NAMES the golfer whose score is missing — "enter a
  score between 30 and 200" over four rows sends someone hunting. Editing an existing round
  is always the single box it has always been. The active golfer's box keeps `id="f_score"`
  whatever the shape, so the live differential hint has one field to read.
- **`csvRounds()` is pure, and its quoting is the part that is ever actually wrong.** RFC
  4180 quoting, CRLF line ends, a UTF-8 BOM at the download so Excel doesn't guess a code
  page — and a leading `'` on anything starting `=`, `+`, `-` or `@`, which a spreadsheet
  would otherwise run as a FORMULA. Nothing in the app can hold one today; a CSV is a file
  that leaves the app, and a hand-edited backup is one restore away. Each line carries the
  SINGLE round's differential, not a paired game's — that is the figure that reconciles with
  the score beside it. Restore reads the JSON and never this.
- **The official calculation must never be affected by the rolling-method settings.** That
  independence is the app's whole claim; it is stated in the UI and in the README, and a
  test pins it indirectly (`whsIndex` takes only differentials).
- The palette is **`theme.css`, linked** — copied byte-for-byte from `~/claude-theme-pack`
  (private repo eagleadams86/claude-theme-pack), the source of truth for all apps. It was
  transcribed inline until 2026-08-18 so `file://` would work; linking replaced that so the
  file cannot drift from the pack or from the other apps. `privacy.html` links the same
  file — **its CSP needed `style-src 'self'` added**, which it did not have, and a linked
  stylesheet is silently blocked without it. `tests.html` uses no tokens and links nothing.
  The app's own additions (`--c-roll`/`--c-whs` chart colours, `--chrome-h`, `--control-h`,
  `--page-w`) stay in the inline `<style>` AFTER the link, which is what lets them win.
  Four themes (Midnight default, Dark, Light, Sepia), listed
  **alphabetically** in the picker, unknown/missing saved values falling back to midnight
  (`slate` → `dark`). Never retune a colour here: change the pack's `tokens.json`, run its
  `check_contrast.py` gate, rebuild, re-transcribe, and keep the other apps in step (drift
  policy in the pack's CLAUDE.md).
- **The two chart series sit on the blue↔amber axis** — the one that survives red-green
  colour deficiency — and colour is not the only cue: the rolling line is solid with round
  points, the official line is dashed with square points, and both are named in the legend.
  Don't re-hue them, and don't drop the dash/shape distinction for a tidier look.
  `--c-roll`/`--c-whs` are app-specific *additions*, not overrides of pack tokens, which is
  why their midnight values live in `:root` (as the pack's own do). Any app-local *override*
  of a pack token would have to target `[data-theme="…"]`, never `:root`.
  **They sit OUTSIDE the pack's `check_contrast.py` gate, and that is the trade this
  arrangement makes** (recorded 2026-08-20, after an audit asked why 8 colour values across
  four themes were being defined outside the source of truth). Chart series aren't pack
  tokens — the pack has no concept of "this app's two lines" — so gating them would mean
  teaching it a per-app section, which is a bigger change than the risk warrants for two
  colours. What that costs: nobody re-checks them automatically when the palette moves.
  Both pairs were verified by hand at that audit and pass AA against `--bg`, `--surface`
  and `--surface-alt` in all four themes. **Re-check them by hand whenever the pack's
  surface tokens change**, and keep the dash/shape distinction, which is what makes the
  chart readable regardless. Sprint Velocity carries the same note for its six series.
- **A status surface is a tint fill plus a full-strength edge.** The `-bg` tints are nearly
  identical to each other once red-green deficiency flattens them, so `.pill` carries a
  1.5px border in the status colour and that is what tells the states apart. Never a fill
  alone. Chart *lines* are exempt — a 2px line is not a large flat area, so it keeps the
  colour at full strength.
- **Buttons are Sprint Velocity's `.btn`, transcribed.** SV is the design lead for shared
  chrome across this family, so the metrics here are its verbatim: 15px text, `7px 12px`
  padding, `--control-h: 38.5px`, hover to `--text-muted`, and a primary that is filled but
  *not* bolded. Two sizes only: `--chrome-h: 30px` for the **header row**, whose
  controls are utilities rather than the action the page is asking for (the same size SV
  gives the very same three: back up, share, sign in), and `--control-h` for everything in
  the page body and the dialogs. Backup/restore/clear used to be a footer row at chrome
  size, for the same "beside small print" reason; they are a header button and a dialog
  now, and inside a dialog they are full-size because there they ARE the action being asked
  for. The pickers sitting beside a header button are pinned to the same height, because a
  native `<select>` ignores line-height and would otherwise sit shorter. Full-size buttons
  deliberately run a size above the 13px body text. `.link` and `.rowbtn`
  take the body size back: they sit inside sentences and tables, not on their own.
  **A change to this block belongs in Sprint Velocity too, or the two drift.**
- **The base field rule's TYPE LIST is the theme pack's own, and it has to be** (2026-08-22).
  `select, textarea, input[type=text|number|date|month|search|tel|url|email|password]` — the
  same list the pack's coarse-pointer rule enumerates. It is a whitelist because it must be
  (a checkbox handed a surface, a border and a 32px box stops being a checkbox), and a
  whitelist grown by hand is a field that arrives silently unstyled: the rounds filter's
  `type=search` shipped wearing the browser's own grey rounded box beside three fields
  wearing the theme's, and nothing failed — it just looked wrong. Borrowing the pack's list
  is what stops that being a fresh discovery each time, since it is the same question
  ("is this a thing you type into?") already answered there. **Adding a type to one means
  adding it to the other.** `input[type=search]` also takes `appearance: none`, like the
  pack's date fields, because the native inset shape ignores the border and radius; that
  removes Chromium's native × as well, which is a fair trade only because the Clear control
  beside it does strictly more.
  **The siblings carry the same gap**: Flow Metrics and Money Map have their own hand-grown
  lists with no `search` in them, and PAPTrack, which does have a search box, styles it
  through a bespoke `.search` class rather than the rule. Nothing is broken in any of them
  today — the next search field is what would break.
- **Help buttons (`.help-btn`) carry `margin-left: 7px`** and cells containing one are
  `nowrap`. An icon must never sit flush against the word it follows — a standing preference
  across every app in this family.
- **The leaderboard's Trend cell is a sparkline PLUS the figure, and the figure is what
  counts.** Flow Metrics' column, ported: the shape answers "which way is this going", the
  number answers "by how much", and the number is what a screen reader reads and what a CSV
  could carry — so the SVG is `aria-hidden` and never the only thing saying anything. It is
  drawn with LOW at the top, because a lower handicap is better and an improving run has to
  rise. It shares the existing "Change over 5" cell rather than adding a ninth column, which
  an eight-column table at `--page-w: 1100` has no room for. `td.trend` is deliberately NOT
  `display: flex` — that takes the cell out of the table's own layout and the column stops
  lining up.
- **The At-a-glance tiles are Sprint Velocity's tile, and their columns are counted by
  hand.** `.stat` shares `.stats`'s rows through `grid-template-rows: subgrid`, which is what
  keeps the label and the number lined up across a row when one label wraps and its
  neighbours' don't — the same reason SV and Team Dashboard do it. The column counts are
  spelled out rather than left to `auto-fit`, which stranded the fifth tile alone on a row
  with three empty slots beside it: six tracks with each tile spanning two puts three across,
  and tiles 4 and 5 span three apiece to finish the second row. **There are exactly five
  tiles, and those spans assume it** — add or remove one in `renderStats` and the spans (and
  the two-across phone rule under 620px) have to be redone in the same commit. **The order of
  the `tiles` array is layout, not editorial**: under 620px the fifth tile is the one that
  takes the full width, so the last-round *date* sits there — it is the only value that isn't
  a short number. Reordering the array moves that wide box to something that doesn't need it.
- **Exclusions are never silent.** Every round that sits outside the numbers — course
  deleted, marked "don't count", a nine with no 9-hole rating, or a nine still waiting for a
  partner — is named on the front page via `#handicapWarn`, and the *Used in* column shows
  which rounds each method actually leaned on. A round quietly missing from a handicap is
  worse than the bug that hiding it would avoid. The waiting nine gets `.pill.pending`, an
  accent edge and neither status colour: it is not counting and it is not excluded, and
  borrowing either colour would claim an outcome it hasn't got.
- **Example data is per-golfer and additive.** `buildDemo()` (pure, pinned by tests) builds
  rounds for the golfer **on screen**, and the demo course is *added* to the list (never a
  replacement — someone may have typed real courses in). Its fixed `demo-course` id is what
  lets a reload replace the course instead of duplicating it; the ROUNDS are replaced by
  dropping that golfer's rounds wholesale, behind a confirm, since real rounds would go
  with them. Other golfers' rounds are never touched.
- **THE SAMPLE DATA IS THE DEMO, and a feature isn't finished until it reaches it.**
  `buildDemoLeague()` / `loadDemoLeague()` — eight golfers, six courses, a season of rounds
  ending today — is what someone sent a share link explores and what the app gets shown
  with, so every feature must be visible from it. Adding one means adding the golfer,
  course or round that demonstrates it, a line in the roster comment above
  `buildDemoLeague()`, a row in the README's demo table, and an assertion in tests.html.
  The same rule runs in Sprint Velocity and Flow Metrics; all three got it on 2026-08-19.
  - **Every figure in the cast is load-bearing**: 26/24/22/20/14/4/2/0 EIGHTEEN-HOLE rounds
    walks every rung of the official calculation (past 20, exactly 20, under 20, the
    reduced-scores table at 4, under the minimum at 2, never played at 0); Alex Nash's
    differentials go NEGATIVE; Old Mill rates below par (the only place a course handicap
    comes out under the index); Kilbryde is slope 142; Brookvale has one set of tees. Two
    "don't count" rounds and one PCC give the exclusion line and the pills something to name.
  - **The nine-hole and exceptional-score cases are in it too** (2026-08-22), and both are
    easy to lose by accident. `DEMO_NINES` gives Joan a PAIR and Alex a single one left
    WAITING — Alex holds the waiting one because his job is negative differentials rather
    than a round count, and on Marcus, who is there to sit exactly on 20, an extra round
    counting towards nothing would muddy the case he exists for. Only Ashfield's yellows and
    Brookvale's tee carry 9-hole figures, so the "no 9-hole rating" state is reachable as
    well. Joan's `esrAt` round is **15 shots** better than she usually plays, not a rounder
    number: the threshold is measured against the INDEX, which is already a best-of average
    several shots below her typical round, and 12 was tried and produced a very good day
    rather than an exceptional score. A test asserts the reduction actually lands AND is
    still in force today — the half of that rule a single good round can't show.
  - **It is ADDITIVE and destroys nothing**, the same promise `buildDemo()` makes. Stable
    `demo-` ids are what make that work: golfers and courses are upserted by id, the old
    example rounds are dropped by their `demo-r-` prefix, and the user's own golfer simply
    joins the leaderboard. It only moves off the golfer on screen if that golfer has no
    rounds. Don't make it replace state — "Clear everything" is the way back out, and a
    `confirm()` can't hold the backup button that makes a destructive action safe.
  - Dates count back from today, so the league is never stale. The generator is **seeded**
    (`demoRandom`, mulberry32 + Box-Muller) — never swap it for `Math.random()`, or the
    league reshuffles per device and no test can pin it.
- **`example-league.json` and the example-league BUTTON are two different things, on
  purpose.** The button is the demo: generated, dated from today, additive. The JSON is a
  checked-in backup file whose job is exercising *Restore*, frozen at a fixed date. Neither
  claims to be the other, which is why they can't drift — don't "unify" them.
- **The example-data button and "Clear everything" are a pair.** Offering one-tap sample
  data without a one-tap way back out is how someone ends up hand-deleting two dozen rounds;
  if either is ever removed, reconsider the other. Clearing uses a dialog rather than nested
  `confirm()` boxes because the thing that makes it safe — taking a backup — has to be a
  button you can press at the moment of hesitation, and a `confirm()` can't hold a control.
  **Settings deliberately survive a clear** (`state.settings` is carried across
  `blankState()`): someone clearing the demo data is starting fresh with real rounds, not
  asking to lose the method they just configured. It goes through `save()` like everything
  else, so it reaches the cloud copy, and `window.ghSignedIn()` is what lets the dialog say
  so — the classic script can't see the module-scoped `user`.
- **The toast is a POPOVER (`popover="manual"`), and that is the only way it can be seen
  while a dialog is open.** A modal `<dialog>` sits in the browser's TOP LAYER, which paints
  above every z-index in the ordinary document, so a toast fired from an open dialog was
  drawn under it and under its backdrop — invisible, indistinguishable from a button that
  does nothing. The share dialog's "Copy link" is the case that has to work: copying leaves
  the dialog open, so the toast is the only thing that says it happened. **Anything else
  that has to appear over a dialog needs the same treatment** — a bigger z-index cannot
  reach the top layer. Sprint Velocity's CLAUDE.md carries the fuller note (it is the design
  lead for this chrome, and the fix is mirrored in all four web apps); the short version is
  that `toast()` raises the popover before writing the text, forces a reflow so the fade
  still runs, and drops out of the top layer once it has faded.
- **Every dialog closes on a click outside it, except one.** `closeOnBackdropClick()` is
  Sprint Velocity's and Team Dashboard's helper, ported: it hit-tests against the dialog's
  *box* rather than `e.target === dialog` (a click on the dialog's own padding is still
  inside the window), and it requires the press to have **started** outside as well, so
  selecting text in a field and releasing past the edge doesn't discard what you typed.
  `syncChoiceDialog` is deliberately left out and blocks Escape too — which copy of your
  rounds survives has to be a choice, not something clicked past. This app adds an optional
  `onClose` argument the siblings don't have, because `courseEditDialog` opens on top of
  `courseDialog` and backing out has to put the courses list back: it dismisses by clicking
  its own Cancel button, and its `cancel` event is intercepted so **Escape, Cancel and a
  click outside all take the same route**. A new dialog goes in the registration list at the
  foot of the classic script, and a nested one needs the `onClose` treatment. **A dialog
  whose `const` is declared further down registers beside its own wiring instead** — the
  share dialog shipped un-dismissable for exactly that reason: adding it to the list would
  have read it inside its temporal dead zone, so it was left out and then forgotten. Sprint
  Velocity and Team Dashboard register theirs the same way, next to their share buttons.
- **Deleting a course or a set of tees keeps the rounds that used it**, flagged as orphaned
  rather than deleted, after a confirmation that names the count. Losing history to a typo in
  the courses screen is the worse failure.
- **Below 3 counting rounds there is no official index**, and the app says so rather than
  showing a number. The WHS does not issue one; inventing it would be worse than the gap.
- **The low-index lookback deliberately includes the pre-20-round stretch**, so an early
  index carrying the reduced-scores table's −2.0 can become the low index the caps are
  measured against. That follows the letter of the rule and is pinned by a test — don't
  "fix" it.
- **Dates are calendar days with no time on them.** `isoOf()`/`daysBefore()` build strings
  from LOCAL date parts and anchor at noon. Never reach for `toISOString()` here: it converts
  to UTC and silently shifts every date back a day for anyone east of Greenwich.
- **Ids from outside are not trusted.** `sanitizeIds()` runs on everything entering through
  `normalizeState()` — the JSON restore, the cloud document, localStorage — replacing any id
  that isn't `[A-Za-z0-9_-]{1,64}` with a fresh one and rewriting every reference through the
  same map. Ids go into `data-id` and `<option value>` in a dozen places. Don't add a render
  site that interpolates an id raw, and don't drop the boundary check.
- **The header and the page width are Team Dashboard's and Sprint Velocity's.** A sticky bar
  (`<header>` outside `.wrap`, `--surface` on `--bg`, 1px bottom border, `10px 0`, 20px
  below) with a `.headbar` inside it held to the same `--page-w` as `.wrap`, and a `.brand`
  `<h1>` at 17px/700 whose `margin: 0 auto 0 0` is what pushes the controls right. The
  horizontal 16px gutter lives on `.wrap`/`.headbar`, **not on `<body>`** — the bar runs
  edge to edge behind it. The control labels are `.sr-only` with a `title` on each control,
  as in both siblings; don't put visible captions back. The strapline is **gone** (2026-08-11): with the courses and league-rule
  buttons moved up here the row had no room for it, and the media query that used to drop it
  on a narrow screen went with it. Below 560px the bar is deliberately **not sticky** — seven
  controls wrap to four lines on a phone, and a sticky bar that deep eats half the screen on
  the one view you scroll most.
- **The mark is the app's own icon, drawn, not an emoji.** A flagstick on the green with a
  ball beside it, on the family tile Money Map, PAPTrack, Sprint Predictability and Flow
  Metrics all wear: midnight page, soft disc in the corner, one accent gradient. It replaced
  the ⛳ this line used to open with. It exists twice — `make_favicon.py` (Pillow →
  `favicon.ico`) and the inline SVG data URI in `<head>` — and the two must stay the same
  picture: the SVG is what a browser shows in the tab (and it needs no sibling file, so it
  survives `file://`), the `.ico` is the fallback a browser fetches from the site root on its
  own and what the header `<img>` wears. Re-running the script means bumping `?v=` on **every**
  `favicon.ico` reference, `privacy.html` included, or the old icon stays cached for months.
  `favicon.ico` used to be one file shared byte-for-byte with claude-lottery / prototypes /
  sprint-velocity; each app has its own mark now, so there is nothing left to keep in step.
  The two extra tints (`#a5b4fc`, `#141c33`) are artwork, not palette — copied byte-for-byte
  from Money Map's icon rather than re-picked, so nothing new enters the theme pack.
- **`--page-w` is 1100px, and both `.wrap` and `.headbar` read it.** They must stay the same
  number or the brand stops lining up with the left edge of the first card — that is the
  whole reason it is a token. This is the **one** deliberate divergence from the siblings'
  1500px: they earn that width with dense many-column tables, and the rounds table here is
  seven columns that went sparse and gappy stretched to it. The full-bleed sticky bar, the
  16px gutter and everything else about the header are still theirs.
- **Everything in the header row is written into the markup at its final size.** The header
  paints long before the script at the foot of the page runs, so a control filled in by JS
  grows on screen and shoves the page down. The sync button is therefore **visible by default
  and hidden on failure**, not the other way round, and midnight carries `selected` in the
  theme picker so it never reads a different theme from the one already painted. If you add
  header chrome, give it its final width in the HTML.
- **`[hidden] { display: none !important; }` sits at the top of the stylesheet, and it is
  not belt-and-braces** (2026-08-22). The browser's own `[hidden]` rule lives in the
  USER-AGENT stylesheet, and any author rule beats a UA rule whatever the specificity — so a
  class that sets `display` cancels it and the element stays on screen with `hidden` set.
  Nothing throws and nothing logs; the thing is simply there. It has cost this app twice:
  `.tabs` was patched with its own `.tabs[hidden]` rule when the Leaderboard tab would not
  hide, and the rounds filter shipped with the same fault — an empty course picker and a
  Clear link above an app with no rounds in it. The per-element patch is gone in favour of
  the global one, and `!important` is what makes it independent of source order (a
  `.thing[hidden]` rule and `.thing` have identical specificity, so otherwise the fix would
  depend on which was written further down). **A new class that sets `display` needs no
  special case now — leave it that way rather than reintroducing per-element rules.**
  Pinned by tests that read COMPUTED STYLE in the app frame, not the rule text.
- **Live regions stay in the tree.** `#handicapWarn` and the dialog warnings are
  `role="status"` and are emptied rather than `hidden` — an element toggled out of the tree
  announces nothing on the way back — with `.warn:empty` collapsing them visually.
- **A clickable row needs a real control in it.** Every table's first cell is a
  `<th scope="row">` holding a `.rowbtn`: a `<tr>` can't take focus, and giving it a button
  role would break the grid semantics that make the numeric columns readable. `tbody th`
  re-styles the row-header cells back to body text.
- **`pushNow()` sends the state through JSON (`forCloud()`), exactly as `save()` writes the
  local copy** — so the two are the same bytes by construction rather than nearly so. Don't
  "simplify" it back to handing `state` straight to `setDoc()`: Firestore walks the live
  object and rejects the **whole document** over a single `undefined` anywhere in it, where
  localStorage silently drops that key and carries on. That asymmetry cost Sprint Velocity
  its sync on 2026-08-12 (a new optional setting, absent from every copy saved before it
  existed, written back as undefined by its sanitiser) with the local copy looking perfect
  throughout. `sanitizeIds()` here can't produce one today — `fix()` always returns a string
  — so the guard is against the next optional field. Pinned in tests.html by **key**, not by
  value: `x === undefined` passes whether the key exists or not.
- **`invalid-argument` does not mean "too big".** Firestore uses that one code for both an
  oversized document and a value it can't store, so the "too large" wording waits until
  Firestore's own message mentions size; otherwise it says the fault is in the app. A remedy
  that has the user deleting rounds must never be the guess.
- Sync is ported from PAPTrack/Sprint Velocity, including the two rules learned the hard way
  there. Both are load-bearing: the first-sign-in "which copy?" dialog, and — underneath it —
  **an empty copy never beats a copy with data in it**, whatever the timestamps say. Keep
  both halves. The `onSnapshot` **error callback** is not optional either: a listener that
  errors is dropped by Firestore and never fires again, so without it another device's
  updates just stop arriving silently. Sync failures are surfaced on the button, never only
  logged, and only a successful push clears the state — there is deliberately no retry button.
  The which-copy-wins rules live in the pure `syncDecision()` in the classic script so
  tests.html can pin them; the module only acts on the verdict. "Clear everything" calls
  `window.cloudFlush()` to skip the push debounce — a clear must not sit in a window the
  tab might not survive. Ordinary edits get the same protection from `flushPending()`, which
  sends a *pending* debounced push on visibilitychange-hidden/pagehide (pending-only, so
  app-switching doesn't fire pointless pushes) — without it, "edit then close the tab" left
  the cloud stale until the next edit on that device.
- **Same-browser tabs share one copy.** A `storage` listener adopts another tab's write
  (localStorage is shared, so the tabs would otherwise last-write-wins each other). Adopt
  and render only — never `save()` from that listener: the writing tab already pushed to
  the cloud, and the event only fires in *other* tabs, so it cannot loop.
- **`privacy.html` is the privacy policy** (static, linked from the footer via
  `.privacy-links` — deliberately a separate element from `#privacyNote`, whose textContent
  the sync code rewrites). It follows the saved theme: the same pre-paint boot script as
  index.html, and the same linked `theme.css` (since 2026-08-18, when the inlined theme
  blocks went with the app's — its CSP carries `style-src 'self'` for exactly that link).
  If sync or what the app stores ever changes, update it and its effective date in the
  same commit.
- **`firestore.rules` is a checked-in copy of what is deployed in the console.** Nothing here
  deploys it. If the console rules change, change this file to match.
- **The CSP meta tag is the only place a policy can be declared** (GitHub Pages can't set
  headers). Any new network endpoint must be added to `connect-src` or it is silently
  blocked. `frame-src` needs only `accounts.google.com` — GIS sign-in never loads the
  Firebase `authDomain`, even if the project is repointed.
- **`example-league.json` is a checked-in fixture, not data** — a backup anyone can restore,
  and the way *Restore from backup* gets exercised with something real (8 golfers, 115
  rounds, 6 courses). `make_example_league.py` writes it from a fixed seed, so re-running
  produces the identical file; regenerate it rather than hand-editing, and keep the awkward
  cases it deliberately holds — a near-scratch player with negative differentials, golfers
  either side of 20 rounds, one on 4 (the reduced-scores table), one on 2 (no official index
  at all), one who has never played, two rounds marked "don't count", a pair of nines, a
  single nine left waiting, and one exceptional round still holding a reduction. **Its
  `version` tracks SCHEMA** — it went to 2 with `holes`, or an older build would restore it
  and score a nine as a full round. Those are the same
  cases `buildDemoLeague()` covers, and deliberately so: the two are kept in step by holding
  the same LIST OF CASES, not the same numbers. **The demo is the button, not this file** —
  see the demo rule above.
- **README.md is the index** — keep it current whenever the app meaningfully changes.
- **`tests.html` busts its own cache, on the frame AND on the source fetches
  (2026-08-22), and that is not tidiness.** `const BUST = '?t=' + Date.now()` goes on
  the hidden `iframe.src` and through `bustFetch()` on every read of a file this repo
  ships. The frame cache and the HTTP cache are different caches and they can disagree:
  in the lottery repo the same harness reported **all-green against a page three
  features out of date**, because the source-level tests were reading the file off the
  server while the frame ran a copy the browser had cached. Nothing errored; the new
  code was simply never run. A suite that can pass against a build which exists nowhere
  is worse than no suite — it turns "untested" into "verified". **If a test passes when
  you expected it to fail, check the frame's `contentWindow` has the function you just
  wrote before believing anything.** `api.github.com` is deliberately left un-busted:
  somebody else's endpoint, not a file we ship.
- **`tests.html` pins the pure functions — open it on a local server and check
  "All N tests pass"** whenever you touch `round1`, `scoreDifferential`, `averageLowest`,
  `whsIndex`/`whsSelection`, `rollingIndex`/`rollingSelection`, `normalizeMethod`,
  `clampInt`/`clampNum`, `applyCaps`, `courseHandicap`, `playingHandicap`/`allowanceById`,
  `esrFor`, `pairNines`, `courseStats`, `csvRounds`/`csvCell`, `indexHistory`, `pickUsed`,
  `syncDecision`, `buildDemo`, `buildDemoLeague`, `rankLeague`, `changeOverRounds`,
  `encodeShare`/`decodeShare`/`buildSharePayload`, `windowRounds`, `sanitizeIds` or
  `normalizeState`. It loads
  the real `index.html` in a hidden iframe and calls the functions directly — no copies, no
  build step — so it needs `http://localhost` (`file://` iframes are blocked in some
  browsers). **It also refuses to run anywhere else, and that is load-bearing:** Pages
  publishes `tests.html` beside the app, where the iframe would be the signed-in copy and
  `onAuthStateChanged` would start a real sync — or raise the which-copy dialog — inside an
  invisible frame. Two guards, both needed: the iframe carries `data-gh-tests`, which the
  sync module checks before `init()`, and the gate at the foot of `tests.html` never creates
  the iframe at all off localhost (booting the app IS the side effect, so the check can't
  live in the load handler). **`file://` is deliberately NOT in `LOCAL_HOSTS`**: it has no
  hostname, and `''` used to sit in that list on the reasoning that the suite couldn't run
  there anyway — but that sent it down the iframe branch, where the frame silently fails to
  load and the suite blamed the app ("did not expose `__ghTestHooks`"). Opening the file off
  disk now gets the advice that fixes it. For the same reason the missing-hooks message
  distinguishes **a frame that never loaded the app** (no server running) from **an app that
  loaded and threw**: one is a setup problem, the other is a bug, and a single message for
  both sent a reader hunting through `index.html` for neither.
  Don't put the iframe back in the markup. **Refusing to run is not the same as saying
  nothing**: off localhost the page asks the GitHub API for the last `tests.yml` run on
  `main` and shows whether it was green, when, and which commit, with a link to the run —
  the question someone opens that page to ask is "is it passing?". The workflow writes the
  full per-group scorecard to `$GITHUB_STEP_SUMMARY`, so that link lands on a scorecard
  rather than a log. If the results markup in `tests.html` changes shape (`<h2>` + `<ol><li>`,
  `li.ok` for a pass), the scrape in the workflow has to change with it. CI runs the same page
  headless on every push (`.github/workflows/tests.yml`) on `localhost:8014`, so the gate
  lets it through, and fails the build if the summary goes red. `window.__ghTestHooks` exists solely to hand it the `const` values, which aren't
  on `window`; function declarations it reaches directly. **When a rule in this file changes,
  change the matching test in the same commit.**
- After changes: **browser-test locally first** (`python3 -m http.server 8014`), then commit,
  push, verify the Pages deploy, and spot-check live. Any local server + browser works —
  don't hunt for a specific tool.
- **Scope: 9 or 18 holes, and nothing else.** Nine-hole rounds landed 2026-08-22, on the
  answer this rule used to say had to be decided first: **a nine is not a game.** Two nines
  are PAIRED into one 18-hole record — the official system's rule, applied to the league
  handicap as well, because "the last 5 rounds" must not mean something different depending
  on how many nines are in it. A twelve-hole round has nothing to pair with and is out.
  See the nine-hole rule below.
- Write commit subject lines in plain English a non-developer can read. The "Recent
  changes" box that made them user-facing was removed 2026-08-18, across the whole app
  family, and the GitHub API went out of the CSP with it — the habit stands anyway.
- **There IS a service worker, and it was refused for a long time.** The three
  objections were right to be made; two turned out to be answerable by design
  rather than by abstention, and the third is what the whole thing is built
  around. Recorded because the next person to touch this needs the reasoning:
  - *"A resident process on the shared origin."* Bounded. A worker's scope
    cannot exceed its own directory without the `Service-Worker-Allowed` header,
    and GitHub Pages cannot send headers — so this one structurally cannot see
    any sibling app. Locally, where the app is served from the
    root, it does control `tests.html`; the allowlist is what makes that
    harmless, not the scope.
  - *"Caches are ORIGIN-wide, not per app."* True, and it does not go away — any
    page on the origin can read this cache, and the sibling workers share the
    store. The answer is the rule in `sw.js`: **only files already public in
    this repo are ever cached** (`./`, `theme.css`, `privacy.html`,
    `favicon.ico` — this app vendors no chart library). Nothing in there is anything an attacker
    could not read straight off GitHub, and the data stays in localStorage,
    which every page on the origin could already reach. It cuts the other way
    too — `activate` must only ever delete caches with this app's `gh-shell-`
    prefix, or it wipes a sibling's.
  - *"A caching bug serves stale code to an app whose data shape moves."* Still
    the real risk. **The worker is network-first for everything**: you can only
    be served cached code on a visit where the network did not answer. The
    braces to that belt is `SCHEMA` / `haltForNewerData()` above — a saved copy
    from a newer build is refused rather than run through normalizeState(),
    which rebuilds it without the fields that build added.
- **The page's CSP does not apply to the worker.** It takes its policy from its
  own script's HTTP response headers, and Pages cannot set headers, so `sw.js`
  runs with **no CSP at all**, permanently installed. Hence: tiny, no `eval`, no
  `importScripts`, no dynamic import, no cross-origin URL anywhere in it — and
  hence `worker-src 'self'` spelled out in the page CSP rather than left to the
  `worker-src → child-src → script-src` fallback chain, which would inherit
  script-src's gstatic and accounts.google.com hosts.
- **`sw-kill.js` is the escape hatch, and it exists BEFORE it is needed.** A bad
  page is fixed by pushing a new one; a bad worker is resident and can keep
  serving itself. `cp sw-kill.js sw.js`, commit, push — every installed copy
  then clears this app's caches, unregisters itself and reloads its windows.
- **Two traps, both of which fail silently:** `cache.addAll` is all-or-nothing
  (one 404 rejects the whole precache, install fails, and there is no offline at
  all while the app looks perfectly healthy online); and **`install` fires once
  per script version**, so if the cache is later evicted nothing rebuilds it and
  offline decays to "whatever the last online visit happened to request". Hence
  `topUp()`, fetching entries one by one, pinged by the page on every load via a
  `shell-check` message — the repair must be able to run without a new worker
  version to hang it on.
- **`shellKey()` matches on the PATH, not the URL**, because the markup asks for
  `favicon.ico?v=1`: keyed on the full URL, the precached favicon would never be
  the entry that answers. `index.html` folds onto `./` for the same reason.
- Registration is guarded three ways, all load-bearing: **not in a frame** (or a
  `tests.html` run would install a worker and then test whatever it had cached),
  **not under `window.ghViewOnly`** — which covers both a shared view and a page
  stopped by `haltForNewerData()`, since the halt's `throw` cannot reach a
  separate script block — and **on `load`**.
- **Testing it locally will mislead you.** The browser holds its own copy of
  `sw.js`, and a byte-identical script fires no `install`, so edits appear to do
  nothing and an emptied cache appears not to refill. `await reg.update()`
  before judging any of it. Related: a suite run against a registered dev worker
  is testing the cache, not the disk — unregister it on localhost before
  trusting a green run.
- The scope is `./`, never absolute: on the local server the app is at the root,
  not under `/golf-handicap/`, and an absolute scope is simply invalid there.

## Fields, Dialogs and Scroll Boxes (2026-08-20)

- **Every modal opens through `openModal(dlg)`, never `showModal()` directly.**
  `showModal()` runs the spec's dialog focusing steps — the `autofocus` element, or failing
  that the FIRST FOCUSABLE one — and there is no `autofocus` anywhere in the file, so which
  dialogs raised a phone's keyboard was decided entirely by which happened to open with a
  text box — four did, since a round opens on its date and the
  course, method and golfer editors each open on a name box; the courses list, Share, Back
  up and Help did not. The keyboard then covers half the dialog before it has been read. On a
  COARSE pointer `openModal` moves focus off the field and onto the dialog itself.
  - **Focus still goes INTO the dialog** — that part is not optional, or a keyboard or
    screen-reader user is stranded outside a thing covering the page. The CONTAINER is what
    the ARIA practices offer for this case: every dialog here carries `aria-labelledby`, so
    it announces itself, and Tab reaches the first field. `tabIndex` is set at open rather
    than in the markup — a dialog is a focus target only for that moment.
  - **`(pointer: coarse)`, NOT a width breakpoint.** The keyboard is a fact about touch, not
    width: a desktop window dragged narrow keeps its click-and-type, a wide tablet is spared.
  - **`raisesKeyboard(el)` is pure and pinned** over `{tagName, type}`, so the type list is a
    test rather than a rediscovery. It is a no-op when the browser landed on a button, a
    picker or a disclosure, which is what leaves those dialogs exactly as they were.
  - A dialog that genuinely wants the keyboard needs no special case: call `openModal` and
    then focus the field yourself afterwards, which simply wins.
  Ported from Money Map, and mirrored across the app family the same afternoon.
- **A box you land on has its contents SELECTED**, so typing replaces the value
  rather than running on to the end of it — one delegated `focusin` listener
  (`SELECT_ON_FOCUS`), which bubbles where `focus` does not, so it covers every
  field including the ones built a moment before a dialog is shown, with nothing
  to remember when adding one. Ported from Money Map 2026-08-20 and now in every
  app in the family. Four things it must keep doing:
  - **The type list is a WHITELIST.** A date, a checkbox, a range and a file
    picker have no text for `select()` to take, and a type nobody has thought
    about is left alone rather than silently swept in.
  - **A TEXTAREA is never touched** — the `INPUT` check does it. A box you write
    several lines into should not be one keystroke from gone, and unlike a
    mistyped figure there is nothing on screen to retype it from.
  - **`data-keep-caret` is the by-hand opt-out for a single-line PROSE field**,
    which the TEXTAREA rule cannot catch. **The round's Note (`#f_note`) carries it**: a
    120-char `input[type=text]` that gets added to later, so the type check would
    otherwise sweep it in.
  - **The one-shot `mouseup` guard is load-bearing, and only for a POINTER-driven
    focus.** A click focuses on mousedown and then places the caret on mouseup,
    which collapses the selection made a moment earlier: without it the feature
    works from the keyboard and looks broken with a mouse, which is how everybody
    would meet it. A `{once:true}` listener left hanging after a Tab would sit
    there and eat the caret placement of a later, deliberate click — hence
    `focusFromPointer`, set on a capturing `pointerdown`. Clicking a second time
    places the caret normally (the field is focused by then, so no focusin
    fires), and that is the way back in for editing rather than replacing.
  It does not fight `openModal`: on a touch screen focus goes to the dialog, so
  nothing is selected until you tap a field.
- **A horizontal scroll box must carry `position: relative`.** `overflow-x: auto` is the
  whole design for `.table-scroll` and `.chart-wrap` — content too wide for a phone scrolls inside its card and the
  page stays the width of the screen. On iOS that only half worked: WebKit clipped it on
  screen but still counted its full width in the DOCUMENT's scrollable area, so the page
  itself became horizontally scrollable into a band of nothing. Measured on iOS 27 at a
  402px viewport: `documentElement.scrollWidth` 906 against a 402px body. `position:
  relative` is what fixes it and nothing weaker does — a stacking context alone
  (`isolation: isolate`) leaves it at 906, and so does spelling out `overflow-y`;
  `contain: paint` works but takes the containing block for fixed descendants with it.
  Chrome and Firefox were always right here, so it is only ever visible on a phone.
- **Date fields are `appearance: none`, and that lives in `theme.css`, not here.** WebKit
  ignores an author `box-sizing` on a natively drawn control, so `width: 100%` on a date
  input meant the column PLUS its padding and border and the box hung over its neighbour.
  See rule 11 in the theme pack's CLAUDE.md; don't re-fix it locally.

## The Privacy Page Carries the Family Footer (2026-08-21)

Every public page in this account carries the same three things at the foot: the privacy
policy, the repo under the label **How it works**, and the authorship line. The APP's footer
has had all three for a while. `privacy.html` had **none** of them until now — and it is a
public page reached by a link in that very footer, so anybody who followed it landed on a
document with no way back to the thing it documents and no statement of who wrote it. The
lottery site's privacy page had grown the footer first and was the only one; the other four
were brought into line together rather than one at a time, because a convention held by one
page out of five is not a convention.

- **No privacy link in it**, unlike the app's own footer — you are standing on that page. That
  absence is asserted, not just omitted: the test checks there is no `href="privacy.html"`.
- **The authorship line is the app's own, verbatim**, which means the two-link form is not
  used here — this repo has no NOTICE, so *independent personal project* is plain text and
  only *MIT licensed* is a link, exactly as the app's own footer has it.
- `.foot` and `.foot a` are copied from the lottery page's stylesheet unchanged, so all five
  read identically. Muted, inheriting the link colour — provenance at the foot of a document
  rather than something to click on the way in.
- **Pinned in `tests.html`**, so the next page added to this repo cannot quietly ship without
  it.
- **It is a real `<footer>`, and the policy is in a real `<main>`** (2026-08-21, a day after
  the footer itself). A styled `<p>` is not a landmark, and a page whose only landmark is
  contentinfo is worse than one with none — the actual policy would sit in no landmark at all.
  So both went in together.
  - **`</main>` closes BEFORE the `<footer>`, and that ordering is the whole thing.** A
    `<footer>` nested inside `main`, `article` or `section` is **not** contentinfo — it is a
    plain footer for that section. So `.wrap` stays an ordinary `<div>` rather than becoming
    the `<main>`, which would have swallowed the footer and left the page with no contentinfo
    at all while looking correct in the source. A test asserts the ORDER, not just the tags.
  - The back link stays outside `<main>` — it is navigation, not the document.
  - **The tests strip HTML comments and match the footer by its class**, because the notes
    beside both elements name them in prose and one of those notes lives in the `<style>`
    block, which an HTML-comment strip does not reach. Without both, a page that had lost the
    element and kept the comment explaining it would still pass. That is not hypothetical —
    it is how the first version of this test failed.
  - **The strip is a LOOP, not a single `.replace()`** (2026-08-21, `stripHtmlComments`).
    One pass over a multi-character delimiter can leave a NEW opener behind that the pass has
    already gone past, so a single pass is only as good as the input is well-formed — CodeQL's
    `js/incomplete-multi-character-sanitization` flagged exactly this line, and it was open on
    five of the nine public repos at once. Nothing here renders what it strips, so there was
    no vulnerability; the reason to fix it is that a helper that can be fooled about what is
    commented out is one that can miss a live off-origin script, which is what these suites
    exist to catch. Same helper, same wording, in every sibling repo's suite.
  - `.foot` sets `margin`, not `margin-top`, so the rule no longer depends on which element
    carries it: a `<p>` brought a UA bottom margin with it and a `<footer>` does not.

- **The privacy page's back link lives in a `<nav>` (2026-08-21).** It stays OUTSIDE `<main>`
  — it is navigation, not the document — but "outside main" is not the same as "outside every
  landmark", which is where it sat: axe-core's `region` rule found it on all six privacy pages
  at once. The `<nav>` carries an `aria-label` naming where it goes back to.
- **Decorative glyphs on buttons are `aria-hidden` everywhere, not just in the header.** The
  header row got the treatment on 2026-08-21 and the rest of the app did not, so a screen
  reader still read "downwards black arrow, Export JSON" in every dialog. Around 50 buttons
  across the family were wrapped in the same pass. The sync button is the exception that
  proves it: its label is rewritten with `textContent` as the state changes, so a span there
  would be blown away — it carries an `aria-label`, re-stated in every branch of `updateUI()`
  so it can never be left describing the previous state.

- **Google's code is fetched when it is asked for, not on every visit (2026-08-22).** `init()`
  used to run unconditionally, so Firebase and the sign-in client were downloaded before
  anyone had touched anything — which is what made the privacy page's wording false. The boot
  branch now asks `shouldBootSync()`, which reads `gh-sync-live`: `'1'` load now, `'0'`
  load nothing, absent → fall back to the legacy `gh-sync-uid` marker (the migration, worth
  at most ONE eager load per browser). `onAuthStateChanged` writes the flag on EVERY report,
  including the null one after signing out — that is what makes signing out stop the requests
  rather than just the syncing.
  - **The warming is load-bearing.** `requestAccessToken()` must be called inside the click
    handler or the popup is blocked, and awaiting a cold import would spend the gesture — so
    the load starts on `pointerenter` / `pointerdown` / `focus`, which all fire before click.
    `onClick` still awaits `ensureInit()` for a keyboard user who never hovers.
  - **The click listener is wired at the boot branch, not at the end of `init()`** — `init()`
    may not have run, and the button has to be pressable in order to be what runs it.
  - `ensureInit()` is idempotent, or a hover and a click start two Firebase apps.
- **Firebase is pinned in `package.json` AND in the `firebasejs/…` URL, and a test holds them
  equal.** Dependabot cannot rewrite a URL, so a manifest-only bump has to fail. All three sync
  apps move to the same version together, like the vendored Chart.js.
