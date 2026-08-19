# Golf Handicap — rules for Claude sessions

A golf handicap tracker that shows two figures side by side: a configurable rolling method —
**the league handicap** (default: the average of the last 5 rounds) — and the official World
Handicap System index. Deployed via GitHub Pages:
https://eagleadams86.github.io/golf-handicap/

Built for a friend's dad, who has always worked his handicap out from his last 5 cards in
Excel. **The rolling method is the point of the app, not a novelty** — it is what the page
leads with, and the official figure is the one shown alongside for reference. Don't reverse
that emphasis.

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
  no CDN calls beyond the Firebase
  SDK. **It was one self-contained file until 2026-08-18**, when the palette moved from an
  inline transcription to the theme pack's generated `theme.css`, linked. That was the
  user's explicit call, made against the trade-off: every web app now reads the same bytes
  and cannot drift, at the cost of `index.html` no longer standing alone — **`theme.css`
  has to travel with it**, and opening the HTML off disk without it leaves the page
  unstyled. Don't re-inline the palette to "restore" the single file; the alignment is the
  point. Everything ELSE stays inline: no second script, no second stylesheet.
  SDK that optional sync loads.
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
- **Help buttons (`.help-btn`) carry `margin-left: 7px`** and cells containing one are
  `nowrap`. An icon must never sit flush against the word it follows — a standing preference
  across every app in this family.
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
  deleted, or marked "don't count" — is named on the front page via `#handicapWarn`, and the
  *Used in* column shows which rounds each method actually leaned on. A round quietly
  missing from a handicap is worse than the bug that hiding it would avoid.
- **Example data is per-golfer and additive.** `buildDemo()` (pure, pinned by tests) builds
  rounds for the golfer **on screen**, the demo course is *added* to the list (never a
  replacement — someone may have typed real courses in), and its fixed `demo-*` ids make a
  reload replace the previous example instead of duplicating it. Other golfers' rounds are
  never touched.
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
  index.html plus the four theme blocks inlined for just the tokens it uses (inline, not a
  stylesheet link, so `file://` keeps working). If sync or what the app stores ever changes,
  update it and its effective date in the same commit.
- **`firestore.rules` is a checked-in copy of what is deployed in the console.** Nothing here
  deploys it. If the console rules change, change this file to match.
- **The CSP meta tag is the only place a policy can be declared** (GitHub Pages can't set
  headers). Any new network endpoint must be added to `connect-src` or it is silently
  blocked. `frame-src` needs only `accounts.google.com` — GIS sign-in never loads the
  Firebase `authDomain`, even if the project is repointed.
- **`example-league.json` is a checked-in fixture, not data** — a backup anyone can restore
  to see a populated leaderboard (8 golfers, 112 rounds, 6 courses). `make_example_league.py`
  writes it from a fixed seed, so re-running produces the identical file; regenerate it
  rather than hand-editing, and keep the awkward cases it deliberately holds — a
  near-scratch player with negative differentials, golfers either side of 20 rounds, one on
  4 (the reduced-scores table), one on 2 (no official index at all), one who has never
  played, and two rounds marked "don't count".
- **README.md is the index** — keep it current whenever the app meaningfully changes.
- **`tests.html` pins the pure functions — open it on a local server and check
  "All N tests pass"** whenever you touch `round1`, `scoreDifferential`, `averageLowest`,
  `whsIndex`/`whsSelection`, `rollingIndex`/`rollingSelection`, `normalizeMethod`,
  `clampInt`/`clampNum`, `applyCaps`, `courseHandicap`, `indexHistory`, `pickUsed`,
  `syncDecision`, `buildDemo`, `rankLeague`, `changeOverRounds`,
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
- **Scope: 18-hole rounds only**, deliberately. The WHS pairs 9-hole scores into 18-hole
  differentials, which interacts awkwardly with a "last N games" method. The data model
  carries what a 9-hole feature would need, so it wouldn't be a migration — but don't add it
  without deciding first what a 9-hole round means to the rolling method.
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
