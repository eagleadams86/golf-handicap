# Golf Handicap

A handicap tracker for golfers who keep their own number.

**Live: https://eagleadams86.github.io/golf-handicap/**

Most handicap apps will only ever show you the official figure. Plenty of golfers don't
work it out that way — they take their last few cards and average them, usually in a
spreadsheet. This app does both, from exactly the same rounds, and shows them side by side:

- **Your own method** — by default the average of your **last 5 rounds**, and configurable
  from there (see [Your own method](#your-own-method)). This is the figure the app leads
  with.
- **The official World Handicap System index** — best 8 of the last 20, with the
  reduced-scores table and the soft/hard caps. Always calculated, never affected by
  anything you change about your own method.

Everything works offline and without an account. Google sign-in is optional and only exists
to put the same rounds on your phone and your laptop.

---

## Contents

- [Using it](#using-it)
- [Your own method](#your-own-method)
- [How the official index is worked out](#how-the-official-index-is-worked-out)
- [Course handicap](#course-handicap)
- [Backups](#backups)
- [Turning sync on](#turning-sync-on)
- [What's in this repo](#whats-in-this-repo)
- [Development](#development)
- [Scope and known limits](#scope-and-known-limits)

---

## Using it

1. **Add a course.** *Rounds → Courses → Add course.* A course needs, for each set of tees,
   a **course rating**, a **slope rating** and a **par** — all three are printed on the
   scorecard. The rating is what a scratch golfer is expected to shoot (e.g. 69.4); the
   slope is how much harder it plays for everyone else (55–155, average 113). Add as many
   sets of tees as you play from.
2. **Log a round.** *+ Add round.* Date, score, course, tees. The next round pre-fills with
   whatever the last one used, so a regular fourball at the same club is four taps.
3. **Read the two numbers.** Both figures update as you type, and *How these are worked out*
   shows the actual arithmetic — which rounds were used, what they averaged to, and every
   step in between.

Multiple golfers are supported: use **Manage** in the header. Each golfer keeps their own
rounds and their own handicap; courses are shared between everyone.

Under **Rounds**, the *Used in* column shows which rounds each method actually leaned on, so
it is always visible why a number moved. A round can be marked *don't count* when you edit
it — useful for a practice round or a scramble — and the app says so on the front page
rather than quietly leaving it out.

### The score to enter

Enter the **adjusted gross score**: your gross score with each hole capped at *net double
bogey* (double bogey plus any handicap strokes you get on that hole). That is what you would
return to the club, and it is what the official calculation expects. The app takes one
number per round rather than a full card, so this cap is yours to apply.

### Conditions adjustment (PCC)

The Playing Conditions Calculation is a daily −1 to +3 adjustment that a golf association
publishes when a course played harder or easier than normal. Almost always 0, which is the
default; set it only if your club has published one for that day.

---

## Your own method

*Rounds → My method.* Everything about the rolling calculation is a setting, so most club
and society formulas can be reproduced exactly:

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

Whatever you set here, **the official figure is untouched.** They are two readings of the
same rounds.

### Why the two numbers differ

The official index keeps only your **best 8 of 20** — it describes what you are capable of
on a good day, so it is usually the *lower* of the two and moves slowly. A rolling average
of your last 5 includes the bad ones, so it sits higher and reacts fast. Neither is wrong;
they answer different questions.

---

## How the official index is worked out

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
never sit more than **5.0** above it. These can be switched off in *My method* to see the
uncapped figure, but that is not what a club would issue. Two caveats, both deliberate and
both pinned by tests:

- The 365-day lookback covers the whole year, including the stretch before the 20th round —
  so an early index carrying the table's −2.0 counts, and can end up being the low index.
  That follows the letter of the rule.
- A real Low Handicap Index is maintained by your golf association from the day your index
  was first issued. The app can only work from the history you have typed in.

---

## Course handicap

Your index is portable; the **course handicap** is what it becomes on one course off one set
of tees — the shots you actually take off on the day:

```
index × (slope ÷ 113) + (course rating − par)
```

rounded to a whole number. It follows whichever figure you have set as primary, so switching
between your method and the official one changes it.

---

## Backups

**Download backup (JSON)** in the footer writes everything — golfers, courses, rounds,
settings — to a file. **Restore from backup** reads one back, replacing what is in the
browser after a confirmation that names the counts.

This matters more than it does in most apps: with no account, clearing your browser data is
the one thing that will lose your history. Take a backup now and then, or turn sync on.

Restored files go through the same validation as everything else — a field that is missing
or the wrong shape is replaced with a sane default rather than throwing, and any id that
isn't a plain `[A-Za-z0-9_-]` string is regenerated with every reference rewritten to match.

---

## Sync setup

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

### Checking the console side from a terminal

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

### Pointing it at a different project

Replace `FIREBASE_CONFIG` in the `<script type="module">` block at the foot of `index.html`,
**and** change the `authDomain` in the CSP's `frame-src` at the top of the same file — the
sign-in popup is an iframe from that host, so it is blocked without it. Any other new
network endpoint needs adding to `connect-src` for the same reason. Setting
`FIREBASE_CONFIG` to `null` returns the app to fully-local: the button hides and nothing is
ever sent anywhere.

### How syncing behaves

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
- **Sync failures are shown, not logged.** The button reads "⚠️ Not syncing" with the cause
  in plain English. There is deliberately no retry button: transient failures are retried by
  the SDK, permanent ones are not fixed by pressing anything, and the next save recovers the
  state on its own.

To go back to fully-local, set `FIREBASE_CONFIG` to `null` again.

---

## What's in this repo

| File | What it is |
|---|---|
| `index.html` | The entire app — markup, styles, logic, sync. No build step, no dependencies, no CDN calls except the Firebase SDK when sync is enabled. |
| `tests.html` | 58 tests pinning the pure handicap maths. Loads the real `index.html` in a hidden iframe and calls its functions directly. |
| `privacy.html` | Privacy policy. Exists because other people may sign in with their own Google accounts. |
| `firestore.rules` | A checked-in copy of the security rules to deploy in the Firebase console. |
| `LICENSE` | MIT. |

The palette is **transcribed inline** from [`claude-theme-pack`](https://github.com/eagleadams86/claude-theme-pack)
(private), the source of truth for every app in this family. It is inlined rather than
linked so the app still works opened straight off disk via `file://`. Four themes — Midnight
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
`rollingIndex`/`rollingSelection`, `normalizeMethod`, `applyCaps`, `courseHandicap`,
`indexHistory`, `sanitizeIds` or `normalizeState`.

`computeAll()` is the only place either handicap is worked out. Every figure, table, chart
and explanation reads from it, so no two parts of the screen can disagree about the maths.
If you add a new figure, take it from there.

Commit subject lines are **user-facing** — the page lists its last 10 commits in the
"Recent changes" section at the foot. Write them in plain English for a reader, not for a
diff.

---

## Scope and known limits

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
