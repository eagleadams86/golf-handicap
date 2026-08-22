# Golf Handicap

A handicap tracker for golfers who keep their own number.

**Live: https://eagleadams86.github.io/golf-handicap/**

Most handicap apps will only ever show you the official figure. Plenty of golfers don't
work it out that way — they take their last few cards and average them, usually in a
spreadsheet. This app does both, from exactly the same rounds, and shows them side by side:

- **Install it like an app** — on a Mac or a PC, open the site in Chrome or Edge and choose "Install Golf Handicap". It gets its own window with no browser chrome, its own icon in the Dock or on the taskbar, and it opens straight from there. On an iPhone or iPad, Safari's Share ▸ "Add to Home Screen" does the same. Working offline was already here and is unchanged — the app has kept a copy of itself since August; what is new is that the manifest and its icons are kept too, because an installed app is the copy most likely to be opened with no connection at all
- **The league handicap** — by default the average of your **last 5 rounds**, and
  configurable from there (see [The League Handicap](#the-league-handicap)). This is the
  figure the app leads with, and the one the leaderboard is ranked on.
- **The official World Handicap System index** — best 8 of the last 20, with the
  reduced-scores table and the soft/hard caps. Always calculated, never affected by
  anything you change about the league rule.

Add everyone you play with and the **Leaderboard** tab ranks the lot of you on the same
rule, from the same rounds. **Share** turns any of it into a read-only link you can send —
the data rides inside the link, so nothing is uploaded anywhere.

Everything works offline and without an account. Google sign-in is optional and only exists
to put the same rounds on your phone and your laptop.

---

## Contents

- [Using It](#using-it)
- [The Leaderboard](#the-leaderboard)
- [The League Handicap](#the-league-handicap)
- [How the Official Index Is Worked Out](#how-the-official-index-is-worked-out)
- [Course Handicap](#course-handicap)
- [Sharing a Read-Only Link](#sharing-a-read-only-link)
- [Backups](#backups)
- [Working Offline](#working-offline)
- [Sync Setup](#sync-setup)
- [What's in This Repo](#whats-in-this-repo)
- [Development](#development)
- [Scope and Known Limits](#scope-and-known-limits)

---

## Using It

1. **Add a course.** *Courses → Add course* in the header. A course needs, for each set of tees,
   a **course rating**, a **slope rating** and a **par** — all three are printed on the
   scorecard. The rating is what a scratch golfer is expected to shoot (e.g. 69.4); the
   slope is how much harder it plays for everyone else (55–155, average 113). Add as many
   sets of tees as you play from.
2. **Log a round.** *+ Add round.* Date, score, course, tees. The next round pre-fills with
   whatever the last one used, so a regular fourball at the same club is four taps.
3. **Read the two numbers.** Both figures update as you type, and *How these are worked out*
   shows the actual arithmetic — which rounds were used, what they averaged to, and every
   step in between.

The app has two tabs. **My handicap** is one golfer's page — the two figures, the trend
chart, the course handicap and the full list of rounds. **Leaderboard** is everybody at
once (see [The leaderboard](#the-leaderboard)).

Multiple golfers are supported: use **Golfers & Courses** in the header, which is also where
courses and their tees are added and edited. Each golfer keeps their own rounds and their own
handicap. Courses and the league rule are shared between everyone, which is what makes the
leaderboard a fair comparison.

Under **Rounds**, the *Used in* column shows which rounds each figure actually leaned on, so
it is always visible why a number moved. A round can be marked *don't count* when you edit
it — useful for a practice round or a scramble — and the app says so on the front page
rather than quietly leaving it out.

### Trying It Out — The Example League

The empty state offers **load the example league**: eight golfers, six courses and a season
of rounds ending today, in one tap. It's the app's demo, and the rule is that **every
feature has to be reachable from it** — so the cast is chosen to cover every case the
figures have to handle, not just to fill the table.

| Golfer | Rounds | What they're there to show |
|---|---|---|
| **Alex Nash** | 26 | Near scratch — the score differentials go **negative**, which is the case a spreadsheet usually gets wrong. |
| **Priya Raman** | 24 | A solid single figure, with one round marked *don't count*. |
| **Dad** | 22 | The mid handicapper the app was built for, and the golfer it lands on. Past 20 rounds, so the official index is a true best-8-of-20. |
| **Marcus Bell** | 20 | Exactly **on** the 20-round WHS window, and also carries a *don't count* round. |
| **Joan Whitlock** | 14 | Improving, and under 20 rounds, so the window is short. |
| **Sam Okafor** | 4 | Four rounds: an index from the **reduced-scores table**. |
| **Ruth Carey** | 2 | Two rounds: under the minimum, so **no official index is issued**. |
| **New Member** | 0 | Has never played, so neither figure exists. |

The six courses are picked the same way. **Old Mill** is a par 69 whose rating sits *below*
par — the one place a course handicap comes out lower than the index. **Kilbryde Dunes**'s
Championship tee is slope 142, near the 155 ceiling, where the 113/slope factor visibly
pulls a differential down. **Brookvale Municipal** has a single set of tees, so the tee
picker has its no-choice case. There's a round with a conditions adjustment too, so PCC
isn't a setting nobody has seen take effect.

**It adds, and destroys nothing.** Your own golfer, courses and rounds are left exactly
where they were — your golfer simply joins the leaderboard. The `demo-` ids are stable, so
loading it twice refreshes the example league rather than stacking a second copy. *Clear
everything*, in the Back up dialog, is the way back out.

**The dates are counted from the day you load it**, so the league is never stale, and the
scores come from a seeded generator — the same league on every device and in every run, so
it can be pinned by a test and talked through twice.

Beside it, **load a single golfer's season** is the older, narrower example: one golfer, one
course, added to whatever you already have. That one's for someone who already has a real
league and just wants to see what a populated page of their own looks like.

[`example-league.json`](example-league.json) is a separate thing and stays: a checked-in
**backup file**, for exercising *Back up → Restore from backup*. It holds a league of the
same shape, frozen at a fixed date rather than counted from today. The button is the demo;
the file is a restore fixture.

### The Score to Enter

Enter the **adjusted gross score**: your gross score with each hole capped at *net double
bogey* (double bogey plus any handicap strokes you get on that hole). That is what you would
return to the club, and it is what the official calculation expects. The app takes one
number per round rather than a full card, so this cap is yours to apply.

### Conditions Adjustment (PCC)

The Playing Conditions Calculation is a daily −1 to +3 adjustment that a golf association
publishes when a course played harder or easier than normal. Almost always 0, which is the
default; set it only if your club has published one for that day.

---

## The Leaderboard

The **Leaderboard** tab puts every golfer in one table, lowest handicap first:

| Column | What it is |
|---|---|
| **#** | Position. Ties share a place and the next one skips, the way a leaderboard reads. |
| **Golfer** | Select a name to open that golfer's own page. |
| *The league rule's name* | Their league handicap — the figure the app leads with. |
| **Official** | Their World Handicap System index. |
| **Rounds** | How many of their rounds count towards the figures. |
| **Best diff** | Their lowest score differential ever logged. |
| **Change over 5** | How far their handicap has moved over their last 5 counting rounds. ▼ is improving. |
| **Last round** | When they last played. |

**Rank by** chooses which of the two figures decides the order — the same setting as *Show
as primary* on the handicap tab, so one figure leads wherever you are looking. Both are
always in the table.

Every row goes through exactly the same calculation as that golfer's own page, so the two
can never disagree. A golfer with no figure yet — fewer than 3 counting rounds gets no
official index, and someone who has never played gets neither — sits at the foot with no
position, rather than being ranked first for having no number. Rounds left out of the
figures are counted up underneath the table, as they are on the front page.

---

## The League Handicap

*League Rules*, in the header. Everything about the rolling calculation is a setting, so most
club and society formulas can be reproduced exactly:

| Setting | What it does |
|---|---|
| **Look at the last N rounds** | The window. Default 5. |
| **Use the best N of them** | Keep only the lowest differentials in that window. Set it equal to the window (the default) to average all of them. |
| **Work from** | *Score differentials* uses the course rating and slope, so rounds on different courses are comparable. *Shots over par* ignores both and just averages how far over par you went — closer to a plain spreadsheet column, and fine if you always play the same course. |
| **Multiply by** | For formulas that scale the average — the old CONGU 0.96, for instance. |
| **Add / subtract** | A flat offset. |

The name follows the settings (`Rolling last 5`, `Best 3 of last 5`) until you type your own,
after which yours sticks.

Two examples:

- *Average of my last 5 cards*: window 5, use 5, differentials, ×1, +0. **This is the
  default.**
- *Best 3 of the last 5, off par*: window 5, use 3, shots over par, ×1, +0.

It is **one rule for everybody in the app**, not a per-golfer setting — that is what lets
the leaderboard compare like with like. Whatever you set here, **the official figure is
untouched.** They are two readings of the same rounds.

### Why the Two Numbers Differ

The official index keeps only your **best 8 of 20** — it describes what you are capable of
on a good day, so it is usually the *lower* of the two and moves slowly. A rolling average
of your last 5 includes the bad ones, so it sits higher and reacts fast. Neither is wrong;
they answer different questions.

---

## How the Official Index Is Worked Out

**Score differential** for each round:

```
(113 ÷ slope rating) × (adjusted gross score − course rating − PCC)
```

rounded to one decimal. The `113 ÷ slope` factor is what makes a round at one course
comparable with a round at another.

**Handicap index** = the average of the lowest 8 differentials from the most recent 20
rounds. With fewer than 20 rounds, the official reduced-scores table applies:

| Rounds | Differentials used | Adjustment |
|---:|---:|---:|
| 3 | lowest 1 | −2.0 |
| 4 | lowest 1 | −1.0 |
| 5 | lowest 1 | — |
| 6 | lowest 2 | −1.0 |
| 7–8 | lowest 2 | — |
| 9–11 | lowest 3 | — |
| 12–14 | lowest 4 | — |
| 15–16 | lowest 5 | — |
| 17–18 | lowest 6 | — |
| 19 | lowest 7 | — |
| 20 | lowest 8 | — |

Below **3 rounds the app shows no official index at all**, because the system does not issue
one — inventing a number there would be worse than saying so. The result is capped at 54.0.

**Soft cap and hard cap.** Once 20 rounds exist, a rise is measured against the lowest index
held in the previous 365 days: anything more than **3.0** above it counts half, and it can
never sit more than **5.0** above it. These can be switched off under *League Rules* to see the
uncapped figure, but that is not what a club would issue. Two caveats, both deliberate and
both pinned by tests:

- The 365-day lookback covers the whole year, including the stretch before the 20th round —
  so an early index carrying the table's −2.0 counts, and can end up being the low index.
  That follows the letter of the rule.
- A real Low Handicap Index is maintained by your golf association from the day your index
  was first issued. The app can only work from the history you have typed in.

---

## Course Handicap

Your index is portable; the **course handicap** is what it becomes on one course off one set
of tees — the shots you actually take off on the day:

```
index × (slope ÷ 113) + (course rating − par)
```

rounded to a whole number. It follows whichever figure you have set as primary, so switching
between the league handicap and the official one changes it.

---

## Sharing a Read-Only Link

**Share** in the header builds a link that shows someone the handicaps you pick, with no
sign-in and no way for them to change anything. Tick the golfers to include — **Select all**
takes the lot, and the count above the list says where you are — and pick more than one and
the link opens on the leaderboard.

**How many rounds** decides how much history rides along: every round, each golfer's last 20
or 10, the last 12 or 6 months, or everything from a date you choose. "Last N" counts *per
golfer*, so a link for four people carries four comparable records rather than twenty rounds
belonging to whoever plays most. Nothing is deleted — this only trims the link. **A trimmed
link shows trimmed figures:** both handicaps are worked out from the rounds inside it, so
they can differ from the ones on your screen, and whoever opens it is told which window they
are looking at.

The data rides **inside the link**, in the part after the `#` — which a browser never sends
to any server. Nothing is uploaded, this app's Firebase project never sees it, and opening
someone else's link cannot touch whatever they have saved in their own browser. A link
carries the chosen golfers, their rounds, only the courses those rounds were played on, and
the league rule the figures were worked out with. Nothing identifying travels: no email
address, no account, not even a theme.

A season of rounds for five golfers packs down to a link of about 2,300 characters. The
dialog shows the length as you tick, and warns past 8,000 — some mail apps break links that
long across two lines. Trimming the history is the quickest fix; sharing fewer golfers also
helps.

Two things worth knowing before you send one:

- It is a **snapshot**, frozen as it looked when you built it. Later rounds don't appear;
  send a fresh link when the numbers have moved.
- It **can't be withdrawn**. Anyone who has the link can open it, so treat it like emailing
  a spreadsheet.

Whoever opens it gets a standing *Read-only view* bar naming the golfers and the date it was
shared, with a link back to their own data.

---

## Backups

**Back up** in the header holds the three things you can do to the data as a whole.
**Download backup (JSON)** writes everything — golfers, courses, rounds,
settings — to a file. **Restore from backup** reads one back, replacing what is in the
browser after a confirmation that names the counts.

This matters more than it does in most apps: with no account, clearing your browser data is
the one thing that will lose your history. Take a backup now and then, or turn sync on.

**Clear everything** wipes the rounds, courses and golfers after a confirmation naming the
counts, with a *Download backup first* button in the same dialog. The league rule and your
theme survive it — clearing is for starting fresh with real rounds, not for undoing the
settings you tuned. If you are signed in it says so, because it also clears the copy in your
Google account and your other devices will then ask whether to follow suit. This is the way
back out after trying the example data.

Restored files go through the same validation as everything else — a field that is missing
or the wrong shape is replaced with a sane default rather than throwing, and any id that
isn't a plain `[A-Za-z0-9_-]` string is regenerated with every reference rewritten to match.

---

## Working Offline

The app keeps a copy of itself on your device, so it opens with no network at all — handy
at a course with no signal. Your rounds were always local, so once the page loads everything
works: logging a round, the leaderboard, the charts, backups. Sync is the one thing that
can't — it needs the network by definition, and picks up again on its own when you're back.

What's kept is only the app's own public files — the page, the stylesheet and the icon, the
same files anyone can read on GitHub. **Nothing of yours is ever put there**, which matters
more than it sounds: every one of these apps shares a single browser origin, so that cache
is not private to this app.

The network is always tried **first**, and the stored copy is used only when it genuinely
doesn't answer (or takes more than five seconds). So you can't be left running an old
version while you're online — and if a device does end up behind, the version check below
stops it misreading anything.

**If one device is behind** — every saved copy carries the data format the app that wrote it
understood. A copy written by a *newer* version than the one you're running won't be opened:
you get a card saying so, nothing is changed or deleted, and reloading picks up the current
version. A backup file from a newer version is refused the same way — without stopping the
app you're using — and a share link from one tells the reader the link is fine and their
copy is behind.

`sw-kill.js` sits in the repo unused, as an escape hatch: copying it over `sw.js` and
pushing makes every installed copy uninstall itself and go back to being an ordinary
online-only page.

## Sync Setup

Sync runs on the **`golfhandicap-14246`** Firebase project, on the free tier. The client
config is already in `index.html`. Three things live in the Firebase console rather than in
this repo, and all three have to be right or sync fails:

1. **Google sign-in enabled** — *Authentication → Sign-in method → Google → Enable*.
2. **`eagleadams86.github.io` in the authorised domains** — *Authentication → Settings →
   Authorized domains*. (`localhost` is authorised by default, so local testing works
   without this, which is exactly how you ship a build that only fails in production.)
3. **The rules from [`firestore.rules`](firestore.rules) published** — *Firestore Database →
   Rules*. **Do this before the first sign-in.** Firestore's defaults either deny everything
   (sync silently fails) or, in test mode, let any signed-in Google account read every other
   user's rounds — and from the outside those two look identical to a rule of
   `request.auth != null`.

`firestore.rules` in this repo is a **checked-in copy** of what should be deployed. Nothing
here deploys it; if the console rules change, change the file to match.

### Checking the Console Side From a Terminal

Both products answer unauthenticated probes, so you can tell whether they are set up without
opening the console. Nothing here is a secret and nothing is written.

```bash
curl -s "https://identitytoolkit.googleapis.com/v1/projects?key=AIzaSyBgBhAMUmXvq1vXb4KdSDALC2kNqsFZmxU"
```

Healthy: a JSON body listing `authorizedDomains`, which must include `eagleadams86.github.io`.
`CONFIGURATION_NOT_FOUND` means Authentication has never been enabled on the project.

```bash
curl -s "https://firestore.googleapis.com/v1/projects/golfhandicap-14246/databases/(default)/documents/golfhandicap/probe?key=AIzaSyBgBhAMUmXvq1vXb4KdSDALC2kNqsFZmxU"
```

Healthy: `PERMISSION_DENIED — Missing or insufficient permissions`. That is the **success**
case: the database exists and the rules are correctly refusing an anonymous read. A message
saying the *API has not been used in this project* means the database has not been created
yet.

The Firebase config in `index.html` is a **public client config, not a secret** — it ships
in the page of every Firebase web app. Access is enforced by the security rules, not by
hiding the key.

### Pointing It at a Different Project

Replace `FIREBASE_CONFIG` in the `<script type="module">` block at the foot of `index.html`.
No CSP change is needed: sign-in goes through Google Identity Services, so `frame-src` stays
`accounts.google.com` only — nothing ever loads the project's `authDomain` (see
[Why Sign-In Doesn't Use Firebase's Popup](#why-sign-in-doesnt-use-firebases-popup)). Only a
genuinely new *network* endpoint would need adding to `connect-src`. Setting
`FIREBASE_CONFIG` to `null` returns the app to fully-local: the button hides and nothing is
ever sent anywhere.

### Why Sign-In Doesn't Use Firebase's Popup

Sign-in goes through **Google Identity Services**: a popup straight to `accounts.google.com`
returns an OAuth access token, and Firebase exchanges it for a session via
`signInWithCredential`. `GOOGLE_CLIENT_ID` sits just above `FIREBASE_CONFIG` and is what makes
that possible.

Firebase's own `signInWithPopup` is deliberately not used. It **starts** at
`<project>.firebaseapp.com/__/auth/handler` and only redirects on to Google from there, so a
proxy that blocks that first hop kills sign-in outright — nothing in the app ever runs.
Corporate filters do exactly that, and per **hostname**, not per domain. On one network on a
single day, two sibling apps' hostnames were refused while a third's went through untouched,
with identical code. Which way a filter lands on a hostname is outside our control and can
change, so a sibling app working today would be no guarantee for this one.

Same Google account, same Firestore document, same rules — only the doorway changed. All four
apps in this family now do this, and all four were confirmed working on the network that
needed it on 7 August 2026.

Two consequences worth knowing:

- **The CSP carries `accounts.google.com` and not `firebaseapp.com`.** `authDomain` remains in
  `FIREBASE_CONFIG` because the SDK requires the field, but nothing loads it, so it no longer
  needs a matching `frame-src` entry. `apis.google.com` is gone too — it served the old popup.
- **Auth is built with `initializeAuth`, not `getAuth`,** so the SDK never asks for
  `apis.google.com` in the first place. `getAuth()` always wires in
  `browserPopupRedirectResolver`, and the SDK initialises that resolver during startup — which
  loads `apis.google.com/js/api.js` to build the gapi iframe that carries `signInWithPopup` and
  `signInWithRedirect` results back to the page. This app calls neither, so nothing consumed it;
  the visible symptom was a CSP error in the console and nothing else. Token refresh, sign-out
  and the cross-tab session all run elsewhere in the SDK and never touch the resolver. The three
  persistences passed in are the ones `getAuth` would have set, in its order, so existing
  sessions and cross-tab behaviour are unchanged. Dropping the resolver costs
  `signInWithPopup`/`signInWithRedirect`/phone sign-in, which now raise `auth/argument-error`;
  if one is ever wanted, pass `browserPopupRedirectResolver` to that call rather than reverting
  to `getAuth()`.
- **`GOOGLE_CLIENT_ID` is not part of `firebaseConfig`** and can't be derived from it. Cloud
  Console → APIs & Services → Credentials → the OAuth 2.0 Client ID named *Web client (auto
  created by Google Service)*. That same screen's **Authorized JavaScript origins** must list
  the app's origin — exact match including port, so `http://localhost` and
  `http://localhost:8014` are different origins — or Google refuses with `origin_mismatch`.

### How Syncing Behaves

One Firestore document per user at `golfhandicap/{uid}`, holding `{ state, updatedAt }`.
localStorage stays the source of truth; the cloud copy is a mirror, and the app works
offline either way.

- The **first time a Google account syncs in a browser**, if both sides already hold rounds
  you are asked which copy to keep. It does not guess by timestamp.
- Underneath that, **an empty copy never beats a copy with data in it**, whatever the
  timestamps say. Without this rule, signing in on a fresh browser pushes an empty state
  stamped *now*, and the device that actually had the rounds — carrying an older timestamp —
  takes the empty copy as "newer" and empties itself. This is not hypothetical; it cost real
  data in a sibling app, which is where the rule comes from.
- A device clearing everything **asks** the others rather than silently wiping them.
- Two tabs of the **same browser** share one copy: an edit saved in one appears in the
  other immediately, signed in or not.
- **Sync failures are shown, not logged.** The button reads "⚠️ Not syncing" with the cause
  in plain English. There is deliberately no retry button: transient failures are retried by
  the SDK, permanent ones are not fixed by pressing anything, and the next save recovers the
  state on its own.

To go back to fully-local, set `FIREBASE_CONFIG` to `null` again.

---

## What's in This Repo

| File | What it is |
|---|---|
| `index.html` | The app — markup, styles, logic, sync. No build step, no dependencies, no CDN calls except the Firebase SDK when sync is enabled. |
| `theme.css` | The shared palette, copied from the private theme pack. Linked by `index.html` and `privacy.html`; it has to sit beside them. |
| `sw.js` | Service worker: keeps the app's own public files on your device so it opens offline. |
| `sw-kill.js` | The escape hatch — copy it over `sw.js` and push to uninstall every installed worker. |
| `tests.html` | Pins the pure handicap maths, the leaderboard's order, the share codec, the restore/repair rules, the offline shell and the sync decisions. Loads the real `index.html` in a hidden iframe and calls its functions directly. The suite prints its own count; this line deliberately doesn't, having said 147 while the suite ran 156. |
| `privacy.html` | Privacy policy. Exists because other people may sign in with their own Google accounts. Linked from the app's footer, beside a **How it works** link back to this README on GitHub. |
| `firestore.rules` | A checked-in copy of the security rules to deploy in the Firebase console. |
| `favicon.ico` | The app's icon — the fallback a browser fetches from the site root on its own. |
| `make_favicon.py` | Draws `favicon.ico` to match the inline SVG icon in `index.html`. |
| `example-league.json` | A checked-in **backup file**, for exercising Restore: a league of 8 golfers, 112 rounds, 6 courses, frozen at a fixed date. The in-app **example league** button is the demo — see [Trying It Out](#trying-it-out--the-example-league). |
| `make_example_league.py` | Writes `example-league.json` from a fixed seed, so re-running it produces the identical file. |
| `LICENSE` | MIT. |

The icon is a flagstick on the green with a ball beside it, on the tile the whole app family
wears; the header shows the same mark, where a ⛳ used to sit. `make_favicon.py` (Pillow)
keeps `favicon.ico` and the page's inline SVG the same picture, rather than leaving a binary
nobody can review in a diff. Re-run it with `python3 make_favicon.py`, then bump the `?v=` on
every `favicon.ico` reference — browsers hold on to an icon for a long time.

The palette comes from [`claude-theme-pack`](https://github.com/eagleadams86/claude-theme-pack)
(private), the source of truth for every app in this family, and is **linked** as
`theme.css` rather than inlined, so a pack change reaches the app by replacing one file. Four themes — Midnight
(default), Dark, Light, Sepia — listed alphabetically in the picker. Never retune a colour
here: change the pack's `tokens.json`, run its contrast gate, rebuild, re-transcribe.

---

## Development

No build step. Serve the folder and open it:

```bash
python3 -m http.server 8014
```

Then <http://localhost:8014/index.html>, and <http://localhost:8014/tests.html> for the
tests — they need `http://localhost` because `file://` iframes are blocked in some browsers.

**Run `tests.html` and check it says "All N tests pass"** whenever you touch `round1`,
`scoreDifferential`, `averageLowest`, `whsIndex`/`whsSelection`,
`rollingIndex`/`rollingSelection`, `normalizeMethod`, `clampInt`/`clampNum`, `applyCaps`,
`courseHandicap`, `indexHistory`, `pickUsed`, `rankLeague`, `changeOverRounds`,
`syncDecision`, `buildDemo`, `buildDemoLeague`, `encodeShare`/`decodeShare`, `buildSharePayload`,
`windowRounds`, `sanitizeIds` or `normalizeState`.

**It only runs on localhost, and enforces that itself.** The test code writes nothing, but
the iframe boots the real app — and GitHub Pages publishes `tests.html` next to it, at
`/golf-handicap/tests.html`, where that iframe would be your signed-in copy: sync would start
inside an invisible frame, and the which-copy dialog could fire where nobody can answer it.
Two guards. The iframe carries `data-gh-tests`, which the sync module checks so it never
initialises in the harness; and a gate at the foot of `tests.html` checks `location.hostname`
and, anywhere but `localhost` / `127.0.0.1` / `[::1]`, never creates the iframe at all — it
explains why and says how to run the suite properly. CI reaches the page on `localhost:8014`,
so it is unaffected.

![tests](https://github.com/eagleadams86/golf-handicap/actions/workflows/tests.yml/badge.svg)

The suite also runs on every push: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
serves the folder, opens `tests.html` in headless Chromium and fails the build if the
summary goes red or the page throws — same workflow as the rest of the app family.

`computeAll()` is the only place either handicap is worked out. Every figure, table, chart
and explanation reads from it, so no two parts of the screen can disagree about the maths.
If you add a new figure, take it from there.

Commit subject lines are written in plain English for a reader, not for a diff. (The
"Recent changes" section that listed them in the app was removed in August 2026.)

---

## Scope and Known Limits

- **18-hole rounds only.** The World Handicap System combines 9-hole scores in pairs into
  18-hole differentials, which interacts awkwardly with a "last N *games*" method — is half a
  round a game? Rather than guess, the app takes 18-hole rounds and says so. The data model
  carries what a later 9-hole feature would need, so adding it would not be a migration.
- **One score per round, not a hole-by-hole card.** That means the net-double-bogey cap is
  applied by you, not by the app.
- **The caps are as good as your history.** See the caveats under
  [the official index](#how-the-official-index-is-worked-out).
- Not affiliated with, endorsed by, or a substitute for your club or golf association. The
  official figure here is a faithful implementation of the published method, but the
  handicap that counts is the one your association issues.
