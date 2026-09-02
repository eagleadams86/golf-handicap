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
rule, from the same rounds — and **Strokes on the Day** turns those handicaps into the shots
each of you gets at one course, in one format, which is the sheet a league actually wants
before it tees off. One round of golf is logged once: tick everyone who played and give them
their scores, and the date, course and tees are typed a single time.

**Share** turns any of it into a read-only link you can send — the data rides inside the
link, so nothing is uploaded anywhere.

Everything works offline and without an account. Google sign-in is optional and only exists
to put the same rounds on your phone and your laptop.

---

## Contents

- [Using It](#using-it)
- [The Leaderboard](#the-leaderboard)
- [The League Handicap](#the-league-handicap)
- [How the Official Index Is Worked Out](#how-the-official-index-is-worked-out)
- [Nine-Hole Rounds](#nine-hole-rounds)
- [Course Handicap and Playing Handicap](#course-handicap-and-playing-handicap)
- [By Course](#by-course)
- [Find (⌘K)](#find-k)
- [Sharing a Read-Only Link](#sharing-a-read-only-link)
- [Backups](#backups)
- [Working Offline](#working-offline)
- [Sync Setup](#sync-setup)
- [What's in This Repo](#whats-in-this-repo)
- [Development](#development)
- [Scope and Known Limits](#scope-and-known-limits)

---

## Using It

A browser with nothing in it opens on one card — no tabs, no panels:

> **Welcome to Golf Handicap**
>
> A handicap tracker for golfers who keep their own number. Log a round and it works out both
> figures from the same cards — the league handicap, an average of your last few rounds, and
> the official World Handicap System index beside it…
>
> **Start Fresh** · **Load Sample Data** · **Restore a Backup**

**Start Fresh** opens the course editor, because a score means nothing until the app knows the
rating and slope it was shot against. **Load Sample Data** loads
[the example league](#trying-it-out--the-example-league). **Restore a Backup** opens the same
[*Back Up & Restore*](#backups) window the ⇩ button does.

The card is up only while the app is completely bare. Save a course and it steps aside for the
Rounds card's own first-run state, which knows you have somewhere to play and offers the round
rather than the course again. Every app in the family opens on this same card, in the same
words and the same order.

1. **Add a course.** *Golfers & Courses → + Add Course* in the header. A course needs, for each set of tees,
   a **course rating**, a **slope rating** and a **par** — all three are printed on the
   scorecard. The rating is what a scratch golfer is expected to shoot (e.g. 69.4); the
   slope is how much harder it plays for everyone else (55–155, average 113). Add as many
   sets of tees as you play from.
2. **Log a round.** *+ Add round.* Date, holes, course, tees, then a score for everyone who
   played — the whole fourball goes in through one window, with nobody ticked but you until
   you say otherwise. The next round pre-fills with whatever the last one used, so a regular
   game at the same club is a few taps.
3. **Read the two numbers.** Both figures update as you type, and *How these are worked out*
   shows the actual arithmetic — which rounds were used, what they averaged to, and every
   step in between.

The app has two tabs. **My handicap** is one golfer's page — the two figures, the trend
chart, the course handicap and the full list of rounds. **Leaderboard** is everybody at
once (see [The leaderboard](#the-leaderboard)).

**Hover the chart and it names the round.** Anywhere in a round's column — not
just on the 3px mark — brings up a panel with the date and both figures, and rings
the two marks it is describing. On a phone a tap does the same and the next tap
takes it away. (It used to be an SVG `title`, which is the browser's own tooltip:
about a second late, in the system's colours rather than the theme's, and never
shown on a touch screen at all.)

**The trend chart fills the window.** *Handicap Over Time* carries a ⤢ button in its
top-right corner; press it and the chart alone fills the screen under the header. **The
header stays where it is and stays usable** — change golfer, or the theme, and the line
redraws in front of you, still full screen. Escape, the same button (now an arrows-in icon),
or a click on the margin round the card brings it back down, and the page is where you left
it. The chart is *redrawn* at the window's size rather than blown up: on the page it is a
fixed 900×280 drawing scaled to the card's width, and stretching that into a full window
would leave it in a band with half the screen empty. It is the same feature as in Flow
Metrics, Sprint Predictability, Money Map and the Lottery Portfolio.

Multiple golfers are supported: use **Golfers & Courses** in the header, which is also where
courses and their tees are added and edited. Each golfer keeps their own rounds and their own
handicap. Courses and the league rule are shared between everyone, which is what makes the
leaderboard a fair comparison.

Under **Rounds**, the *Used in* column shows which rounds each figure actually leaned on, so
it is always visible why a number moved. Past eight rounds a filter appears above the table —
by course, or by anything the row shows — and it changes only what is on screen, which the
line beside it says out loud: both handicaps always use every round. A round can be marked *don't count* when you edit
it — useful for a practice round or a scramble — and the app says so on the front page
rather than quietly leaving it out.

### Trying It Out — The Example League

**Load Sample Data** on the welcome card loads the example league: eight golfers, six courses
and a season of rounds ending today, in one tap. (A single golfer's season is a link inside the
same sentence, for anyone who only wants to see one populated page.) It's the app's demo, and the rule is that **every
feature has to be reachable from it** — so the cast is chosen to cover every case the
figures have to handle, not just to fill the table.

| Golfer | Rounds | What they're there to show |
|---|---|---|
| **Alex Nash** | 26 + a nine | Near scratch — the score differentials go **negative**, which is the case a spreadsheet usually gets wrong. His nine-hole round is the one left **waiting for a partner**. |
| **Priya Raman** | 24 | A solid single figure, with one round marked *don't count*. |
| **Dad** | 22 | The mid handicapper the app was built for, and the golfer it lands on. Past 20 rounds, so the official index is a true best-8-of-20. |
| **Marcus Bell** | 20 | Exactly **on** the 20-round WHS window, and also carries a *don't count* round. |
| **Joan Whitlock** | 14 + two nines | Improving, and under 20 rounds, so the window is short. Her two nines **pair** into one 18-hole record, and one round of hers is exceptional enough to earn a **reduction that is still in force**. |
| **Sam Okafor** | 4 | Four rounds: an index from the **reduced-scores table**. |
| **Ruth Carey** | 2 | Two rounds: under the minimum, so **no official index is issued**. |
| **New Member** | 0 | Has never played, so neither figure exists. |

The six courses are picked the same way. **Old Mill** is a par 69 whose rating sits *below*
par — the one place a course handicap comes out lower than the index. **Kilbryde Dunes**'s
Championship tee is slope 142, near the 155 ceiling, where the 113/slope factor visibly
pulls a differential down. **Brookvale Municipal** has a single set of tees, so the tee
picker has its no-choice case. There's a round with a conditions adjustment too, so PCC
isn't a setting nobody has seen take effect. **Ashfield Park's yellows and Brookvale's only
tee carry nine-hole ratings** and the other four deliberately do not — so both nine-hole
answers are reachable: a nine that scores, and a nine the app says it cannot score yet.

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
| **Change over 5** | A sparkline of their last few games, and how far their handicap has moved over their last 5 counting rounds. ▼ is improving — and the figure, not the line, is what a screen reader reads and what the CSV carries. |
| **Last round** | When they last played. |

**Rank by** chooses which of the two figures decides the order — the same setting as *Show
as primary* on the handicap tab, so one figure leads wherever you are looking. Both are
always in the table.

Every row goes through exactly the same calculation as that golfer's own page, so the two
can never disagree. A golfer with no figure yet — fewer than 3 counting rounds gets no
official index, and someone who has never played gets neither — sits at the foot with no
position, rather than being ranked first for having no number. Rounds left out of the
figures are counted up underneath the table, as they are on the front page.

Underneath it, **Strokes on the Day** turns those handicaps into shots at one course, off one
set of tees, in one format: each golfer's course handicap, what they play off after the
format's allowance, and how many shots they receive from the lowest player in the field, who
plays off scratch. It reads the same rows the table above it does, so an index can never
disagree between the two. See [Course Handicap and Playing
Handicap](#course-handicap-and-playing-handicap).

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

The name follows the settings (`Rolling last 5`, `Best 3 of last 5`) and is worked out from
them — it can't be typed over, so it always says what the numbers actually do.

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

**Exceptional score reduction.** Play far better than your index says you can and the index
comes down by more than the averaging alone would bring it. A differential **7.0 to 9.9**
below your index takes an extra **1.0** off; **10.0 or more** below takes **2.0**. Two things
about it are easy to get wrong, and both are pinned by tests:

- it is measured against the index you **held when you played**, not the one the round
  produces — measuring against the new index would compare the score with a number it has
  already pulled down, and nothing would ever look exceptional;
- it does **not stop with that round**. It stays in force for the next 19 scores and falls
  away as that round drops out of the last 20, so two exceptional rounds close together
  stack. The app names the date of each one in *How these are worked out*, and says on the
  front page how much is currently being taken off.

It can be switched off under *League Rules*, beside the caps, and it never touches the league
handicap.

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

**The reduction is applied before the caps**, which is the order the published method uses:
the cap procedure runs on the index the reduction produced. That has a consequence worth
stating, because it reads like a bug and is not — under a *hard* cap the figure is pinned to
5.0 above the low index either way, so the reduction can be swallowed by it.

---

## Nine-Hole Rounds

Both handicaps count *games*, and a game is 18 holes — so a nine is not a round on its own.
The official system adds two nine-hole score differentials together to make one 18-hole
differential, and this app does the same, **for the league handicap as well**. That is what
stops "the last 5 rounds" quietly meaning something different depending on how many nines
are in it.

- Nines are paired **in the order you played them**, oldest first. One left over waits for
  the next nine you log, and the app says so — on the front page, in the rounds table and in
  the working-out — rather than quietly ignoring it.
- A nine is scored against the **9-hole rating, slope and par** for those tees, which are
  printed on the scorecard and are typed in under *Golfers & Courses* (they are optional, and
  all three or none). Without them the round is kept but not scored: half the 18-hole figures
  would be a guess, not an answer, and this app does not put a guess into a differential.
- The conditions adjustment is **halved** for a nine. This one is the app's own reading rather
  than a quoted rule: PCC is published in strokes over a full round, so charging a nine the
  whole of it would double-count the moment the pair is added up. Two nines on +1 days combine
  to exactly the +1 an 18 would get.
- A paired game takes the **later** of the two dates — it was not a game until the second nine
  was played — and both of its rounds are marked as counting, since they earned that
  differential together.

---

## Course Handicap and Playing Handicap

Your index is portable; the **course handicap** is what it becomes on one course off one set
of tees — the shots those tees give you:

```
index × (slope ÷ 113) + (course rating − par)
```

rounded to a whole number. It follows whichever figure you have set as primary, so switching
between the league handicap and the official one changes it.

What a competition actually gives you is a **percentage of that**, and the percentage depends
on the format — the more balls a side plays, the more the best of them flatters a high
handicap. Pick the format and the card shows what you play off, with the full course handicap
still written out underneath:

| Format | Allowance |
|---|---:|
| Full course handicap | 100% |
| Individual stroke play | 95% |
| Individual Stableford | 95% |
| Singles match play | 100% |
| Four-ball | 90% |
| Foursomes (each partner, added) | 50% |

These are the recommended allowances; a club can and does set its own. The chosen format is
remembered in this browser and shared by both places it appears — the Course Handicap card
and **Strokes on the Day** on the Leaderboard tab, which does the same arithmetic for
everybody at once and shows how many shots each golfer receives from the lowest player in the
field.

---

## By Course

Where you actually play well, which neither handicap will tell you: both are built to be
comparable *across* courses on purpose, so a course that happens to suit you disappears into
them by design. One row per course played, best average differential first, with the raw best
and average scores beside it — the differential columns are the fair comparison, the score
columns are the numbers you remember. It appears once you have played more than one course.

---

## Find (⌘K)

**⌕ Find** in the header — or **⌘K** / **Ctrl-K** from anywhere — opens a search box over
every golfer, every course and every round. Type two characters, and clicking a result takes
you to it; a round opens straight into its card.

It's the same window, in the same place, with the same shortcut as
[Money Map's](https://github.com/eagleadams86/financial-plan),
[Sprint Predictability's](https://github.com/eagleadams86/sprint-velocity) and
[Flow Metrics'](https://github.com/eagleadams86/team-dashboard).

The golfer picker and the [rounds filter](#by-course) already narrow things down. What Find
adds is what they can't reach:

- **The note on a round.** It's the only prose in the app, and nothing else searches it —
  so *windy*, *society day* or *first round off the new tees* is the way back to that round.
- **A course, whatever the filter is set to** — every round at Kilbryde Dunes, newest first,
  across every golfer.
- **A date.** `2026-08` is August; `2026` is the season; `2026-07-04` is that day.
- **A set of tees**, by name — both the course that has them and the rounds played off them.
- **A golfer**, with how many rounds they have.

Results are capped at 80, and the list says how many more matched so the cap is never
silent. A shared read-only link searches golfers and rounds but not courses, because the
Golfers & Courses window isn't there — and a round opens read-only rather than into an
editor that would refuse to save.

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

**Download rounds (CSV)** is the other direction out: every round of every golfer as a
spreadsheet, with the differential the app worked out beside each score, for anyone who keeps
their handicap in one. It is a one-way door — *Restore* reads the JSON, never the CSV — and a
nine-hole round carries its own nine-hole differential rather than the combined figure, so
each line reconciles with the score beside it.

**The negative figures come out as numbers.** Two of the columns go below zero — a score
differential does for anyone playing under their handicap, and *vs par* does for every round
under par — and until 2026-08-27 the guard that stops a cell being read as a spreadsheet
formula was quoting them as text, in exactly the two columns somebody exports this file in
order to average. A cell that is a whole number now goes out as one; a cell that merely
*starts* like a number (`-1+1`) is still defused.

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
  state on its own. A dropped listener is re-opened by that save, and by a once-a-minute retry
  while it is down (since 2026-09-01 — before that it stayed dead until the next sign-in, so a
  device that only reads was cut off from the others' updates).

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
| `example-league.json` | A checked-in **backup file**, for exercising Restore: a league of 8 golfers, 115 rounds, 6 courses, frozen at a fixed date. The in-app **example league** button is the demo — see [Trying It Out](#trying-it-out--the-example-league). |
| `make_example_league.py` | Writes `example-league.json` from a fixed seed, so re-running it produces the identical file. |
| `LICENSE` | MIT. |

The icon is a flagstick on the green with a ball beside it, on the tile the whole app family
wears; the header shows the same mark, where a ⛳ used to sit. `make_favicon.py` (Pillow)
keeps `favicon.ico` and the page's inline SVG the same picture, rather than leaving a binary
nobody can review in a diff. Re-run it with `python3 make_favicon.py`, then bump the `?v=` on
every `favicon.ico` reference — browsers hold on to an icon for a long time.

The palette comes from [`claude-theme-pack`](https://github.com/eagleadams86/claude-theme-pack)
(private), the source of truth for every app in this family, and is **linked** as
`theme.css` rather than inlined, so a pack change reaches the app by replacing one file. Four themes — Midnight,
Dark, Light, Sepia — plus **Auto, which is the default**: with nothing saved the app follows
your own system, Light or Midnight, and changes with it while the page is open. Midnight is the
base palette, and what Auto means by "dark". All five are listed alphabetically in the picker. Never retune a colour
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
`courseHandicap`, `playingHandicap`/`allowanceById`, `esrFor`, `pairNines`, `courseStats`,
`csvRounds`/`csvCell`, `indexHistory`, `pickUsed`, `rankLeague`, `changeOverRounds`,
`syncDecision`, `buildDemo`, `buildDemoLeague`, `encodeShare`/`decodeShare`, `buildSharePayload`,
`windowRounds`, `sanitizeIds` or `normalizeState`.

**And a smoke walk, because everything above is a pure function.** Pinning the maths leaves
the largest part of the file — the render layer — never executed at all, so a throw inside a
tab panel or a dialog would ship green. A coverage run on 2026-08-27 measured exactly that:
`updateUI`, `renderScoreRows`, `openRound` and 63 others sat at zero. The walk plants the
example league in a second, full-size frame, visits both tabs, opens and closes every window,
and fails if the frame throws or if a panel comes back empty. It was verified by breaking
`renderLeague` on purpose and watching the suite go red where nothing else noticed. It writes
nothing: the plant hook replaces the state in memory rather than saving, and the one key it
does touch — the remembered tab — is put back and then read again to prove it.

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

- **One score per round, not a hole-by-hole card.** That means the net-double-bogey cap is
  applied by you, not by the app — and there is no Stableford or net scoring, which would
  need the card and a stroke index per hole.
- **Nine-hole rounds are paired, never half-counted** (see [Nine-Hole
  Rounds](#nine-hole-rounds)). A nine on tees with no 9-hole rating is kept but not scored,
  and one nine on its own counts towards nothing until you play another. Anything other than
  9 or 18 holes is out of scope: there is nothing sensible to pair a twelve with.
- **Playing-handicap allowances are the recommended ones**, not your club's. If your club
  sets its own, the course handicap on the card is the number to apply it to yourself.
- **The caps are as good as your history.** See the caveats under
  [the official index](#how-the-official-index-is-worked-out).
- Not affiliated with, endorsed by, or a substitute for your club or golf association. The
  official figure here is a faithful implementation of the published method, but the
  handicap that counts is the one your association issues.

## When Google's Code Loads (2026-08-22)

**Not on an ordinary visit any more.** `init()` used to run unconditionally at the foot of the
sync module, so `firebase-app`, `firebase-auth`, `firebase-firestore` and the Google sign-in
client were fetched from `www.gstatic.com` and `accounts.google.com` before anyone had touched
anything — four requests to Google carrying the visitor's IP and user-agent, on a page that
might never sync. That is what made the old privacy wording false; this is the change that
lets the strong sentence be true.

It cannot be made *fully* lazy, and that is the whole difficulty: a returning signed-in reader
has to be recognised **without clicking anything**, and the only thing that knows whether this
browser holds a live Firebase session is Firebase. So the app records the answer itself:

| `gh-sync-live` | meaning | on load |
|---|---|---|
| `'1'` | a session was live at last report | load Firebase now |
| `'0'` | there was none, or they signed out | load nothing |
| absent | never asked, or a browser from before this change | fall back to the legacy `gh-sync-uid` marker |

`onAuthStateChanged` writes `'1'` or `'0'` on **every** auth report, including the null one
that follows signing out — so signing out stops the requests, not just the syncing. The
`absent` case is the migration and costs at most **one** eager load per browser:
`gh-sync-uid` has been written on the first successful sync for an account since long
before this, and is never removed, so its presence means "this browser has signed in at some
point". A browser that has never signed in has neither key and never takes that path.

**The warming is load-bearing, not an optimisation.** `requestAccessToken()` has to be called
from inside the click handler or the browser judges the popup unsolicited and blocks it, and
awaiting a cold SDK import first would spend the gesture. So the load starts on
`pointerenter`, `pointerdown` and `focus` — all of which fire *before* click. `onClick` still
awaits `ensureInit()` as a fallback, for somebody who tabs straight to the button and presses
Enter; if the popup is refused there, the existing `popup_failed_to_open` message says what to
do and the second press always works. `ensureInit()` is idempotent, or a hover and a click
would start two Firebase apps.

The click listener is wired at the **boot branch**, not at the end of `init()` — `init()` may
not have run yet, and the button has to be pressable in order to be what causes it to run.

`tests.html` pins the shape of all of this, and the privacy page's wording with it.

## Firebase Version

All three sync apps are on the **same** Firebase version, moved together, exactly like the
vendored Chart.js: `package.json` pins it for Dependabot and `tests.html` pins the manifest to
the `firebasejs/…` URL in `index.html`, so a manifest-only bump fails. Bumping means changing
the URL and the pin in the same commit, in all three repos, and then proving a real Google
sign-in still works on the live origin.

## What Watches the Firebase SDK (2026-08-21)

The one genuinely third-party thing this app runs is Google's Firebase SDK, and it is loaded
by **URL** from `www.gstatic.com` — so nothing was watching it. Dependabot reads manifests, and
no manifest named it; the clean bill of health it reported covered nothing at all. (There are
no known advisories against the pinned version — the problem was that nobody would have been
told if there were.)

`package.json` is that manifest. It installs nothing — it is `private`, has no `scripts`, and
CI passes `--omit=dev` — and the bytes that run still come from Google's CDN at page load.
That creates the same way of ending up lying that a vendored library has: **Dependabot cannot
rewrite a URL**, so a version-bump PR would raise the manifest while the page went on fetching
the old one. `tests.html` pins the manifest's version to the `firebasejs/…` URL in
`index.html`, which makes a manifest-only bump fail and turns the PR into the right
instruction: *a newer SDK exists, now change the URL too.*

Never let that pin become a `^` or `~` range — a range cannot be checked against a URL.

