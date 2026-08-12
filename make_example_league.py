#!/usr/bin/env python3
"""Write example-league.json — a backup file holding a whole league, for trying the app out.

Restore it in the app (Back up -> Restore from backup) to get a populated league
table without typing in a season of cards. It is a fixture, not real data.

Every awkward case the league table has to handle is deliberately in here: a
near-scratch player whose differentials go negative, golfers either side of the
20-round mark, one on 4 rounds (the reduced-scores table), one on 2 (no official
index is issued at all), one who has never played, and two rounds marked "don't
count" so the exclusion line has something to say.

Scores come from a per-golfer target and a fixed seed, so re-running this writes
the identical file — a fixture that changes under you is no use. Run it with
`python3 make_example_league.py` from the repo root.
"""
import json, random
from datetime import date, timedelta

random.seed(20260811)

COURSES = [
    {
        "id": "c-parkland", "name": "Ashfield Park",
        "tees": [
            {"id": "t-ash-yellow", "name": "Yellow", "rating": 69.4, "slope": 122, "par": 71},
            {"id": "t-ash-white", "name": "White", "rating": 71.2, "slope": 129, "par": 71},
            {"id": "t-ash-red", "name": "Red", "rating": 67.8, "slope": 118, "par": 71},
        ],
    },
    {
        "id": "c-links", "name": "Carrick Links",
        "tees": [
            {"id": "t-car-white", "name": "White", "rating": 72.6, "slope": 134, "par": 72},
            {"id": "t-car-yellow", "name": "Yellow", "rating": 70.9, "slope": 127, "par": 72},
        ],
    },
    {
        "id": "c-heath", "name": "Highmoor Heath",
        "tees": [
            {"id": "t-high-blue", "name": "Blue", "rating": 73.1, "slope": 138, "par": 72},
            {"id": "t-high-white", "name": "White", "rating": 70.5, "slope": 125, "par": 72},
        ],
    },
    # A short par-69 track: the one where the course rating sits below par, so a
    # course handicap comes out lower than the index rather than higher.
    {
        "id": "c-mill", "name": "Old Mill (short course)",
        "tees": [
            {"id": "t-mill-white", "name": "White", "rating": 66.2, "slope": 109, "par": 69},
            {"id": "t-mill-yellow", "name": "Yellow", "rating": 64.8, "slope": 104, "par": 69},
        ],
    },
    # The hardest in the list — slope 142 is near the 155 ceiling, so the 113/slope
    # factor visibly pulls a differential down.
    {
        "id": "c-dunes", "name": "Kilbryde Dunes",
        "tees": [
            {"id": "t-dunes-championship", "name": "Championship", "rating": 74.8, "slope": 142, "par": 72},
            {"id": "t-dunes-medal", "name": "Medal", "rating": 72.0, "slope": 131, "par": 72},
            {"id": "t-dunes-forward", "name": "Forward", "rating": 68.9, "slope": 119, "par": 72},
        ],
    },
    {
        "id": "c-brookvale", "name": "Brookvale Municipal",
        "tees": [
            {"id": "t-brook-main", "name": "Main", "rating": 70.1, "slope": 115, "par": 70},
        ],
    },
]

TEES = [(c["id"], t["id"], t["par"]) for c in COURSES for t in c["tees"]]

# name, rounds to log, average shots over the course rating, how streaky they are
GOLFERS = [
    ("Alex Nash",      26, 2.5,  2.0),   # near scratch — a low single figure
    ("Priya Raman",    24, 8.0,  2.6),   # solid single figure
    ("Dad",            22, 13.0, 3.0),   # the mid handicapper the app was built for
    ("Marcus Bell",    20, 18.5, 3.4),   # mid-to-high, right on the 20-round mark
    ("Joan Whitlock",  14, 24.0, 4.0),   # improving, fewer than 20 rounds
    ("Sam Okafor",      4, 30.0, 5.0),   # four rounds: an index from the reduced table
    ("Ruth Carey",      2, 32.0, 5.0),   # two rounds: no official index at all
    ("New Member",      0, 0.0,  0.0),   # signed up, hasn't played yet
]

NOTES = ["", "", "", "windy", "society day", "medal", "", "back nine fell apart", "best of the year"]

rounds = []
golfers = []
today = date(2026, 8, 11)
rid = 0

for gi, (name, count, over, spread) in enumerate(GOLFERS):
    gid = "g-%d" % (gi + 1)
    golfers.append({"id": gid, "name": name})
    for i in range(count):
        course_id, tee_id, par = TEES[(gi + i * 3) % len(TEES)]
        rating = next(t["rating"] for c in COURSES if c["id"] == course_id
                      for t in c["tees"] if t["id"] == tee_id)
        # A gentle improvement over the season, plus round-to-round noise.
        drift = (count - i) / max(count, 1) * 2.0
        score = round(rating + over + drift + random.gauss(0, spread))
        played = today - timedelta(days=(count - i) * 8 + (gi % 3))
        rid += 1
        rounds.append({
            "id": "r-%03d" % rid,
            "golferId": gid,
            "date": played.isoformat(),
            "courseId": course_id,
            "teeId": tee_id,
            "score": int(score),
            "pcc": 1 if i == 5 else 0,
            "note": NOTES[(gi + i) % len(NOTES)],
            # A couple of scrambles and a practice round, so the "left out" line
            # and the pills in the rounds table have something to show.
            "counts": not (i == 2 and gi in (1, 3)),
        })

state = {
    "version": 1,
    "golfers": golfers,
    "activeGolfer": golfers[2]["id"],
    "courses": COURSES,
    "rounds": rounds,
    "settings": {
        "method": {"name": "Rolling last 5", "window": 5, "use": 5,
                   "basis": "differential", "multiplier": 1, "adjustment": 0},
        "applyCaps": True,
        "primary": "rolling",
    },
    "exportedAt": "2026-08-11T09:00:00.000Z",
}

out = "example-league.json"
with open(out, "w") as f:
    json.dump(state, f, indent=2)
print(f"{out}: {len(golfers)} golfers, {len(rounds)} rounds, {len(COURSES)} courses")
