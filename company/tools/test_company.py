"""Tests for the Coach and the Assessor - run: python company/tools/test_company.py
They use made-up data and a temp folder: your real goals, reviews and .env are never touched, nothing is sent.
"""
import shutil
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

import assessor as A
import coach as C

fails = []


def check(name, cond):
    print(f"  [{'OK' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


def task(tid, due, done_on=None):
    return {"id": tid, "title": f"Task {tid}", "due": due, "done": done_on is not None, "done_on": done_on}


TODAY = date(2026, 10, 28)                                      # a Wednesday
data = {
    "this_week": ["G2.2"],
    "goals": [
        {"id": "G1", "category": "Career", "tasks": [task("G1.1", "2026-10-20"), task("G1.2", "2026-11-01")]},
        {"id": "G2", "category": "Skills", "tasks": [task("G2.1", "2026-11-01"), task("G2.2", "2026-11-30")]},
        {"id": "G3", "category": "Portfolio", "tasks": [task("G3.1", "2026-10-27", "2026-10-27")]},
        {"id": "G9", "category": "Life", "tasks": [task("G9.1", "2026-10-01", "2026-10-26")]},
    ],
}

# ── the Assessor ─────────────────────────────────────────────────────────────
d = lambda s: date.fromisoformat(s)
check("streak counts days in a row", A.current_streak({d("2026-10-26"), d("2026-10-27"), d("2026-10-28")}, TODAY) == 3)
check("today not done yet doesn't break it", A.current_streak({d("2026-10-26"), d("2026-10-27")}, TODAY) == 2)
check("one rest day a week is allowed", A.current_streak({d("2026-10-26"), d("2026-10-28")}, TODAY) == 2)
check("two missed days in a week end it", A.current_streak({d("2026-10-26")}, TODAY + timedelta(days=1)) == 0)
check("best streak remembers the past", A.best_streak({d("2026-09-01"), d("2026-09-02"), d("2026-09-03")}, TODAY) == 3)
check("ranks climb with points", A.rank_for(0)[0] == "Trainee" and A.rank_for(160)[:2] == ("Junior Analyst", "Analyst"))
check("top rank has no next", A.rank_for(5000)[1] is None)

tmp = Path(tempfile.mkdtemp())
apps_md = tmp / "APPLICATIONS.md"
apps_md.write_text("| Scheme | Opens |\n|---|---|\n| NHS STP | Jan |\n\n| Date sent | Company |\n|---|---|\n"
                   "| 2026-10-27 | Acme Bio |\n| 2026-10-10 | Old Co |\n| | |\n", encoding="utf-8")
check("applications: only dated rows count", A.application_dates(apps_md) == [d("2026-10-27"), d("2026-10-10")])
log_md = tmp / "LEARNING_LOG.md"
log_md.write_text("| Date | Topic | Where | Answer |\n|---|---|---|---|\n| 2026-03 | x | y | _write it_ |\n"
                  "| 2026-10-27 | lists | video | A list holds items in order. |\n", encoding="utf-8")
check("learning log: placeholders don't count", A.learning_answers(log_md) == 1)

r = A.report(today=TODAY, data=data, apps=[d("2026-10-27")], answers=1, commits=[d("2026-10-28")])
check("points add up", r["points"] == 2 * 10 + 2 * 50 + 1 * 5 + 1 * 5 + 3 * 2)    # G3 + G9 complete = 2 goals
check("streak from ticks + apps + commits", r["streak"] == 3 and r["active_today"])
check("applications this week", r["apps_this_week"] == 1)

# ── the Coach ───────────────────────────────────────────────────────────────
picks = C.pick_today(data)
ids = [t["id"] for _, t in picks]
check("one task per slot", len(picks) == 2 and picks[0][0].startswith("📚") and picks[1][0].startswith("💼"))
check("the Mentor's this_week list wins over due date", ids[0] == "G2.2")
check("otherwise soonest due first", ids[1] == "G1.1")
week = {"this_week": [], "goals": [
    {"id": "G3", "category": "Practice", "days": ["Tue", "Thu", "Sat"], "tasks": [task("G3.1", "2026-11-01")]},
    {"id": "G5", "category": "Portfolio", "days": ["Mon", "Wed", "Fri", "Sat"], "tasks": [task("G5.1", "2026-11-01")]},
]}
slots_on = lambda day: [label[0] for label, _ in C.pick_today(week, day)]
check("Rosalind only on its days", "🧩" in slots_on(date(2026, 10, 29)) and "🧩" not in slots_on(TODAY))
check("project only on its days", "🧪" in slots_on(TODAY) and "🧪" not in slots_on(date(2026, 10, 29)))
check("Saturday gets both", slots_on(date(2026, 10, 31)) == ["🧪", "🧩"])
morning = C.morning_message(data, r, datetime(2026, 10, 28, 7, 0))
check("morning nudges overdue tasks", "OVERDUE" in morning and "G1.1" in morning)
check("morning isn't marked late at 07:00", "sent late" not in morning)
check("morning after noon says it's late", "sent late" in C.morning_message(data, r, datetime(2026, 10, 28, 19, 0)))
evening = C.evening_message(data, r, datetime(2026, 10, 28, 21, 45))
check("evening asks what got finished", "finish" in evening)

real_env = C.ENV_FILE.read_text(encoding="utf-8") if C.ENV_FILE.exists() else None
real_env_path = C.ENV_FILE
C.ENV_FILE, C.STATE_FILE, C.LOG_FILE = tmp / ".env", tmp / "state.json", tmp / "log.txt"
C.ENV_FILE.write_text("# comment\nTELEGRAM_BOT_TOKEN=abc:123\nTELEGRAM_CHAT_ID=\n", encoding="utf-8")
C.write_env_value("TELEGRAM_CHAT_ID", "42")
env = C.read_env()
check(".env read + chat id saved", env == {"TELEGRAM_BOT_TOKEN": "abc:123", "TELEGRAM_CHAT_ID": "42"})
check("no token = no crash, just not sent", C.send("hello", {}) is False and "NOT SENT" in C.LOG_FILE.read_text("utf-8"))
check("your real .env was not touched",
      (real_env_path.read_text(encoding="utf-8") if real_env_path.exists() else None) == real_env)

C.REVIEWS = tmp / "reviews"
review = C.start_review_file(data, r, TODAY)
text = review.read_text(encoding="utf-8")
check("review file starts with this week's facts", "week of 2026-10-26" in text and "Filled in by the Coach" in text)
review.write_text("my own notes", encoding="utf-8")
C.start_review_file(data, r, TODAY)
check("review file is never overwritten", review.read_text(encoding="utf-8") == "my own notes")

state = {"last_rank": "Trainee"}
check("rank up is announced once", "RANK UP" in C.rank_news(r, state) and C.rank_news(r, state) == "")

shutil.rmtree(tmp)
print("\nALL PASS" if not fails else f"\nFAILED: {fails}")
raise SystemExit(1 if fails else 0)
