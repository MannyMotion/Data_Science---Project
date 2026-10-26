"""assessor.py - The Assessor: points, streaks and ranks, worked out from what you actually did.

Nothing is typed in by hand and nothing is stored - every number is recomputed each run from:
    plan/goals.json                     tasks ticked off (their done_on dates)
    private/job_hunt/APPLICATIONS.md    applications sent (table rows that start with a YYYY-MM-DD date)
    LEARNING_LOG.md                     entries with a real 3-sentence explanation (not the _write it_ placeholder)
    git log                             days you committed work to this repo

Points:  task done +10 · goal achieved +50 · application sent +5 · learning-log answer +5 · active day +2
Active day = a day with at least one task ticked, application sent or commit pushed to this repo.
Streak = active days in a row. One missed day per week (Mon-Sun) counts as your rest day and doesn't break it.

Usage (from the repo folder):
    python company/tools/assessor.py        your points, rank and streak

Zero tokens, standard library only - so the scoring can't be talked into anything.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

TOOLS = Path(__file__).resolve().parent         # .../company/tools
ROOT = TOOLS.parents[1]                         # the repo folder
GOALS_FILE = ROOT / "plan" / "goals.json"
APPLICATIONS = ROOT / "private" / "job_hunt" / "APPLICATIONS.md"
LEARNING_LOG = ROOT / "LEARNING_LOG.md"

try:                                            # emoji must not crash the Windows console
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

POINTS = {"task": 10, "goal": 50, "application": 5, "answer": 5, "active_day": 2}

# (points needed, rank) - a career ladder, lowest first
RANKS = [
    (0, "Trainee"),
    (50, "Apprentice Analyst"),
    (150, "Junior Analyst"),
    (300, "Analyst"),
    (500, "Bioinformatician"),
    (800, "Senior Bioinformatician"),
    (1200, "Lead Scientist"),
]

# (streak days, badge)
STREAK_BADGES = [
    (3, "Warming up"),
    (7, "One week strong"),
    (14, "Two-week habit"),
    (30, "Habit locked in"),
    (60, "Unstoppable"),
    (100, "Hundred-day club"),
]

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ── reading the evidence ────────────────────────────────────────────────────
def load_goals(path: Path = GOALS_FILE) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def task_done_dates(data: dict) -> list[date]:
    return [date.fromisoformat(t["done_on"]) for g in data["goals"] for t in g["tasks"] if t["done"] and t["done_on"]]


def goals_achieved(data: dict) -> int:
    return sum(1 for g in data["goals"] if g["tasks"] and all(t["done"] for t in g["tasks"]))


def table_rows(path: Path) -> list[list[str]]:
    """Every row of every markdown table in a file, as a list of cell strings."""
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


def application_dates(path: Path = APPLICATIONS) -> list[date]:
    """Only rows whose first cell is a real date count - so headers and the deadlines table are skipped."""
    out = []
    for cells in table_rows(path):
        if cells and ISO_DATE.match(cells[0]):
            try:
                out.append(date.fromisoformat(cells[0]))
            except ValueError:
                pass
    return out


def learning_answers(path: Path = LEARNING_LOG) -> int:
    """Rows in the log whose last cell holds a real explanation (not empty, not an _italic placeholder_)."""
    count = 0
    for cells in table_rows(path)[1:]:                  # [0] is the header row
        last = cells[-1] if cells else ""
        if set(last) <= set("-: "):                     # the |---|---| separator row
            continue
        if last and not (last.startswith("_") and last.endswith("_")):
            count += 1
    return count


def commit_dates(repo: Path = ROOT) -> list[date]:
    no_window = getattr(subprocess, "CREATE_NO_WINDOW", 0)   # no console flash when run by Task Scheduler
    try:
        out = subprocess.run(["git", "-C", str(repo), "log", "--format=%ad", "--date=short"],
                             capture_output=True, text=True, timeout=20, creationflags=no_window).stdout
    except Exception:
        return []
    return [date.fromisoformat(l) for l in out.split() if ISO_DATE.match(l)]


# ── streaks ─────────────────────────────────────────────────────────────────
def week_of(d: date) -> tuple[int, int]:
    iso = d.isocalendar()
    return iso[0], iso[1]


def current_streak(active: set[date], today: date) -> int:
    """Walk back from today. Today only counts if it's already active (the day isn't over yet)."""
    day = today if today in active else today - timedelta(days=1)
    count, rest_weeks = 0, set()
    for _ in range(1000):
        if day in active:
            count += 1
        elif week_of(day) in rest_weeks:                # second missed day in the same week -> streak over
            break
        else:
            rest_weeks.add(week_of(day))                # first missed day this week = rest day
        day -= timedelta(days=1)
    return count


def best_streak(active: set[date], today: date) -> int:
    if not active:
        return 0
    best = run = 0
    rest_weeks: set = set()
    day = min(active)
    while day <= today:
        if day in active:
            run += 1
            best = max(best, run)
        elif week_of(day) in rest_weeks:
            run, rest_weeks = 0, set()
        else:
            rest_weeks.add(week_of(day))
        day += timedelta(days=1)
    return max(best, current_streak(active, today))


# ── ranks ───────────────────────────────────────────────────────────────────
def rank_for(points: int) -> tuple[str, str | None, int]:
    """(rank now, next rank or None, points still needed for it)"""
    now = [name for need, name in RANKS if points >= need][-1]
    nxt = [(need, name) for need, name in RANKS if points < need]
    return (now, nxt[0][1], nxt[0][0] - points) if nxt else (now, None, 0)


def badge_for(streak: int) -> str | None:
    got = [name for need, name in STREAK_BADGES if streak >= need]
    return got[-1] if got else None


# ── the report ──────────────────────────────────────────────────────────────
def report(today: date | None = None, data: dict | None = None, apps: list[date] | None = None,
           answers: int | None = None, commits: list[date] | None = None) -> dict:
    """Everything the Coach and goal.py show. Each input can be passed in (that's how the tests work)."""
    today = today or date.today()
    data = data if data is not None else load_goals()
    apps = apps if apps is not None else application_dates()
    answers = answers if answers is not None else learning_answers()
    commits = commits if commits is not None else commit_dates()

    done = task_done_dates(data)
    active = set(done) | set(apps) | set(commits)
    active = {d for d in active if d <= today}
    breakdown = {
        "tasks": len(done) * POINTS["task"],
        "goals": goals_achieved(data) * POINTS["goal"],
        "applications": len(apps) * POINTS["application"],
        "learning answers": answers * POINTS["answer"],
        "active days": len(active) * POINTS["active_day"],
    }
    total = sum(breakdown.values())
    rank, next_rank, to_next = rank_for(total)
    streak = current_streak(active, today)
    monday = today - timedelta(days=today.weekday())
    return {
        "today": today,
        "points": total,
        "breakdown": breakdown,
        "rank": rank,
        "next_rank": next_rank,
        "to_next": to_next,
        "streak": streak,
        "best_streak": best_streak(active, today),
        "badge": badge_for(streak),
        "active_today": today in active,
        "apps_this_week": sum(1 for d in apps if monday <= d <= today),
        "tasks_this_week": sum(1 for d in done if monday <= d <= today),
    }


def one_line(r: dict) -> str:
    nxt = f" ({r['to_next']} to {r['next_rank']})" if r["next_rank"] else ""
    badge = f" · {r['badge']}" if r["badge"] else ""
    return f"🔥 Streak {r['streak']} day{'s' * (r['streak'] != 1)}{badge} · 🎖 {r['rank']} · {r['points']} pts{nxt}"


def main() -> None:
    r = report()
    print(f"\n  {one_line(r)}")
    print(f"  Best streak: {r['best_streak']} day{'s' * (r['best_streak'] != 1)} · today counts: {'yes' if r['active_today'] else 'not yet'}")
    print(f"  This week: {r['tasks_this_week']} tasks · {r['apps_this_week']}/5 applications\n")
    for name, pts in r["breakdown"].items():
        print(f"    {name:<17} {pts:>5}")
    print(f"    {'total':<17} {r['points']:>5}\n")


if __name__ == "__main__":
    main()
