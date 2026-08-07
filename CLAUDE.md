# Golf Handicap — rules for Claude sessions

A golf handicap tracker that shows two figures side by side: a configurable rolling method
(default: the average of the last 5 rounds) and the official World Handicap System index.
Deployed via GitHub Pages: https://eagleadams86.github.io/golf-handicap/

Built for a friend's dad, who has always worked his handicap out from his last 5 cards in
Excel. **The rolling method is the point of the app, not a novelty** — it is what the page
leads with, and the official figure is the one shown alongside for reference. Don't reverse
that emphasis.

- The whole app is **one file — `index.html`** — everything inline, no build step, no server,
  works via `file://`. Keep it that way: no npm, no bundler, no CDN calls beyond the Firebase
  SDK that optional sync loads.
- No account is ever required. The only exception is an **optional** Google sign-in for
  cross-device sync, backed by the `golfhandicap-14246` Firebase project (auth + one
  Firestore doc per user, free tier). `FIREBASE_CONFIG` in the bottom `<script type="module">`
  block controls it; set it to `null` to force fully-local mode. The config is a public
  client config, not a secret — access is enforced by the Firestore rules.
- Firebase authorized domain is `eagleadams86.github.io`, so sync works at this
  `/golf-handicap/` path unchanged. The project's `authDomain`
  (`golfhandicap-14246.firebaseapp.com`) is also in the CSP's `frame-src` — the sign-in popup
  is an iframe from that host and is blocked without it. **Both have to move together if the
  project ever changes.**
- **`computeAll()` is the only place either handicap is calculated.** Every figure, tile,
  table, chart and the working-out panel reads from it. A new number takes its value from
  there or the screen starts disagreeing with itself.
- **The official calculation must never be affected by the rolling-method settings.** That
  independence is the app's whole claim; it is stated in the UI and in the README, and a
  test pins it indirectly (`whsIndex` takes only differentials).
- The palette is **transcribed inline** from `~/claude-theme-pack` (private repo
  eagleadams86/claude-theme-pack), the source of truth for all apps — inlined rather than
  linked so `file://` works. Four themes (Midnight default, Dark, Light, Sepia), listed
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
  *not* bolded. Two sizes only — `--chrome-h: 30px` for the header row, `--control-h` for
  everything in the page body — and the pickers sitting beside a button are pinned to the
  same height, because a native `<select>` ignores line-height and would otherwise sit
  shorter. Buttons deliberately run a size above the 13px body text. `.link` and `.rowbtn`
  take the body size back: they sit inside sentences and tables, not on their own.
  **A change to this block belongs in Sprint Velocity too, or the two drift.**
- **Help buttons (`.help-btn`) carry `margin-left: 7px`** and cells containing one are
  `nowrap`. An icon must never sit flush against the word it follows — a standing preference
  across every app in this family.
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
- **Everything in the header row is written into the markup at its final size.** The header
  paints long before the script at the foot of the page runs, so a control filled in by JS
  grows on screen and shoves the page down. The sync button is therefore **visible by default
  and hidden on failure**, not the other way round. If you add header chrome, give it its
  final width in the HTML.
- **Live regions stay in the tree.** `#handicapWarn` and the dialog warnings are
  `role="status"` and are emptied rather than `hidden` — an element toggled out of the tree
  announces nothing on the way back — with `.warn:empty` collapsing them visually.
- **A clickable row needs a real control in it.** Every table's first cell is a
  `<th scope="row">` holding a `.rowbtn`: a `<tr>` can't take focus, and giving it a button
  role would break the grid semantics that make the numeric columns readable. `tbody th`
  re-styles the row-header cells back to body text.
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
  tab might not survive.
- **Same-browser tabs share one copy.** A `storage` listener adopts another tab's write
  (localStorage is shared, so the tabs would otherwise last-write-wins each other). Adopt
  and render only — never `save()` from that listener: the writing tab already pushed to
  the cloud, and the event only fires in *other* tabs, so it cannot loop.
- **`privacy.html` is the privacy policy** (static, midnight only, linked from the footer via
  `.privacy-links` — deliberately a separate element from `#privacyNote`, whose textContent
  the sync code rewrites). If sync or what the app stores ever changes, update it and its
  effective date in the same commit.
- **`firestore.rules` is a checked-in copy of what is deployed in the console.** Nothing here
  deploys it. If the console rules change, change this file to match.
- **The CSP meta tag is the only place a policy can be declared** (GitHub Pages can't set
  headers). Any new network endpoint must be added to `connect-src`, and the Firebase
  `authDomain` to `frame-src`, or it is silently blocked.
- **README.md is the index** — keep it current whenever the app meaningfully changes.
- **`tests.html` pins the pure functions — open it on a local server and check
  "All N tests pass"** whenever you touch `round1`, `scoreDifferential`, `averageLowest`,
  `whsIndex`/`whsSelection`, `rollingIndex`/`rollingSelection`, `normalizeMethod`,
  `clampInt`/`clampNum`, `applyCaps`, `courseHandicap`, `indexHistory`, `pickUsed`,
  `syncDecision`, `buildDemo`, `sanitizeIds` or `normalizeState`. It loads
  the real `index.html` in a hidden iframe and calls the functions directly — no copies, no
  build step — so it needs `http://localhost` (`file://` iframes are blocked in some
  browsers). `window.__ghTestHooks` exists solely to hand it the `const` values, which aren't
  on `window`; function declarations it reaches directly. **When a rule in this file changes,
  change the matching test in the same commit.**
- After changes: **browser-test locally first** (`python3 -m http.server 8014`), then commit,
  push, verify the Pages deploy, and spot-check live. Any local server + browser works —
  don't hunt for a specific tool.
- **Scope: 18-hole rounds only**, deliberately. The WHS pairs 9-hole scores into 18-hole
  differentials, which interacts awkwardly with a "last N games" method. The data model
  carries what a 9-hole feature would need, so it wouldn't be a migration — but don't add it
  without deciding first what a 9-hole round means to the rolling method.
- Write commit subject lines in plain English a non-developer can read. **They are
  user-facing**: the "Recent changes" box at the foot of the page fetches the last 10 commits
  touching `index.html` from the GitHub API and lists the subject lines verbatim. Write them
  for a reader, not for a diff.
