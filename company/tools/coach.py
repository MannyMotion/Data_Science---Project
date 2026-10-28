"""coach.py - The Coach: your daily Telegram reminders, read straight from plan/goals.json.

Commands (run from the repo folder):
    python company/tools/coach.py setup       first time only: finds your chat id, saves it to .env, sends a test
    python company/tools/coach.py morning     today's plan (learning, project or Rosalind, career) + overdue nudges
    python company/tools/coach.py evening     "what did you finish?" + does today count for your streak
    python company/tools/coach.py sunday      weekly review prompt + applications count; starts this week's review file
Add --dry-run to print a message instead of sending it, --force to send again on the same day.

Windows Task Scheduler runs morning / evening / sunday for you (company/tools/install_tasks.ps1).
The token lives only in .env at the repo root, which git ignores. No token = the message is printed and logged,
never a crash. The only network call is to Telegram's free Bot API. Zero tokens, standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

import assessor as A

TOOLS = A.TOOLS
ROOT = A.ROOT
ENV_FILE = ROOT / ".env"
STATE_FILE = TOOLS / "coach_state.json"                 # git-ignored: what was sent when
LOG_FILE = TOOLS / "coach_log.txt"                      # git-ignored: every run, so you can check it worked
REVIEWS = ROOT / "private" / "reviews"
REVIEW_TEMPLATE = ROOT / "plan" / "WEEKLY_REVIEW_TEMPLATE.md"
APPS_TARGET = 5

# which slot of the daily routine each goal category belongs to (see company/ROUTINE_CARD.md)
SLOT_OF = {"Skills": "learning", "Credentials": "learning",
           "Portfolio": "project", "Research": "project", "Practice": "practice",
           "Visibility": "career", "Career": "career", "Network": "career", "Life": "career"}
SLOTS = [("learning", "📚 Learning (1h)"), ("project", "🧪 Project (1h)"), ("practice", "🧩 Rosalind (1h)"),
         ("career", "💼 Career (30m)")]
DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]       # how goals.json names a goal's "days"


# ── small helpers ───────────────────────────────────────────────────────────
def log(text: str) -> None:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {text}\n")


def read_env(path: Path | None = None) -> dict:
    path = path or ENV_FILE                             # looked up at call time, so tests can point it elsewhere
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def write_env_value(key: str, value: str, path: Path | None = None) -> None:
    path = path or ENV_FILE
    lines =path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    for i, line in enumerate(lines):
        if line.split("=", 1)[0].strip() == key:
            lines[i] = f"{key}={value}"
            break
    else:
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def when(due: str, today: date) -> str:
    left = (date.fromisoformat(due) - today).days
    return f"OVERDUE {-left}d" if left < 0 else ("due today" if left == 0 else f"due in {left}d")


# ── Telegram ────────────────────────────────────────────────────────────────
def telegram_call(token: str, method: str, params: dict | None = None) -> dict:
    url = f"https://api.telegram.org/bot{token}/{method}"
    body = urllib.parse.urlencode(params).encode() if params else None
    with urllib.request.urlopen(urllib.request.Request(url, data=body), timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send(text: str, env: dict | None = None) -> bool:
    """Send a message. Never raises - a reminder must never crash a scheduled task."""
    env = env if env is not None else read_env()
    token, chat = env.get("TELEGRAM_BOT_TOKEN"), env.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        log("NOT SENT (no token / chat id in .env yet): " + text.splitlines()[0])
        print(text)
        print("\n  (Not sent: .env has no Telegram token / chat id yet - see company/HOW_IT_WORKS.md)")
        return False
    try:
        ok = telegram_call(token, "sendMessage", {"chat_id": chat, "text": text}).get("ok", False)
    except Exception as e:                                  # the error text never includes the token
        log(f"SEND FAILED ({type(e).__name__}): " + text.splitlines()[0])
        print(f"  Telegram send failed: {type(e).__name__}")
        return False
    log(("SENT: " if ok else "TELEGRAM SAID NO: ") + text.splitlines()[0])
    return ok


# ── choosing today's tasks ──────────────────────────────────────────────────
def open_tasks(data: dict) -> list[tuple[dict, dict]]:
    return [(g, t) for g in data["goals"] for t in g["tasks"] if not t["done"]]


def runs_today(goal: dict, today: date) -> bool:
    """A goal can name the days it runs on (e.g. Rosalind: Tue, Thu, Sat). No "days" = every day."""
    days = goal.get("days")
    return not days or DAY_NAMES[today.weekday()] in days


def pick_today(data: dict, today: date | None = None) -> list[tuple[str, dict]]:
    """One task per routine slot: the Mentor's this_week list first (in its order), then soonest due date.
    Only goals that run today are considered."""
    today = today or date.today()
    focus = [i.lower() for i in data.get("this_week", [])]
    rank = lambda gt: (focus.index(gt[1]["id"].lower()) if gt[1]["id"].lower() in focus else len(focus), gt[1]["due"])
    picks = []
    for slot, label in SLOTS:
        options = sorted((gt for gt in open_tasks(data)
                          if SLOT_OF.get(gt[0]["category"]) == slot and runs_today(gt[0], today)), key=rank)
        if options:
            picks.append((label, options[0][1]))
    return picks


def overdue(data: dict, today: date, skip: set[str]) -> list[dict]:
    late = [t for _, t in open_tasks(data) if t["due"] < today.isoformat() and t["id"] not in skip]
    return sorted(late, key=lambda t: t["due"])


def done_today(data: dict, today: date) -> list[dict]:
    return [t for g in data["goals"] for t in g["tasks"] if t["done"] and t["done_on"] == today.isoformat()]


# ── the messages ────────────────────────────────────────────────────────────
def rank_news(r: dict, state: dict) -> str:
    """A line to celebrate a new rank - only once, the first message after it happens."""
    before = state.get("last_rank")
    state["last_rank"] = r["rank"]
    return f"\n🎖🎖 RANK UP: you're now {r['rank']}! 🎖🎖" if before and before != r["rank"] else ""


def morning_message(data: dict, r: dict, now: datetime) -> str:
    today = now.date()
    picks = pick_today(data, today)
    lines = [f"☀️ Morning Manny - {today:%a %d %b}"]
    if now.hour >= 12:
        lines.append("(sent late - your PC was off at 07:00)")
    lines.append("\nToday's plan, after work:")
    lines += [f"{label}: {t['id']} {t['title']} - {when(t['due'], today)}" for label, t in picks]
    late = overdue(data, today, {t["id"] for _, t in picks})
    if late:
        lines.append("\n⚠️ Overdue - do it, move it, or drop it:")
        lines += [f"  {t['id']} {t['title']} ({when(t['due'], today)})" for t in late[:3]]
        if len(late) > 3:
            lines.append(f"  ...and {len(late) - 3} more (python plan/goal.py)")
    lines.append(f"\n{A.one_line(r)}")
    lines.append(f"📨 Applications this week: {r['apps_this_week']}/{APPS_TARGET}")
    lines.append("\nTick off: python plan/goal.py done <id>")
    return "\n".join(lines)


def evening_message(data: dict, r: dict, now: datetime) -> str:
    today = now.date()
    finished = done_today(data, today)
    lines = ["🌙 Evening check-in - what did you finish today?"]
    if finished:
        lines.append("\n✅ Already ticked today:")
        lines += [f"  {t['id']} {t['title']}" for t in finished]
    lines.append("\nStill open from today's plan:")
    lines += [f"  {label}: {t['id']} {t['title']}" for label, t in pick_today(data, today)]
    lines.append("\nFinished one? python plan/goal.py done <id>")
    lines.append("Learned something? 3 sentences in LEARNING_LOG.md - that's your interview answer.")
    if r["active_today"]:
        lines.append(f"\n✅ Today counts. {A.one_line(r)}")
    else:
        lines.append(f"\n⏳ Today doesn't count yet - one commit, tick or application keeps your "
                     f"{r['streak']}-day streak alive. (Taking today off? That's your one rest day this week.)")
    return "\n".join(lines)


def start_review_file(data: dict, r: dict, today: date) -> Path:
    """Copy the template into private/reviews/ with this week's facts filled in at the top. Never overwrites."""
    monday = today - timedelta(days=today.weekday())
    path = REVIEWS / f"{today.isoformat()}.md"
    if path.exists():
        return path
    REVIEWS.mkdir(parents=True, exist_ok=True)
    won = [t for g in data["goals"] for t in g["tasks"]
           if t["done"] and t["done_on"] and monday.isoformat() <= t["done_on"] <= today.isoformat()]
    facts = [f"> **Filled in by the Coach:** {r['tasks_this_week']} tasks done · "
             f"{r['apps_this_week']}/{APPS_TARGET} applications · {A.one_line(r)}"]
    facts += [f"> - ✅ {t['id']} {t['title']} ({t['done_on']})" for t in won] or ["> - no tasks ticked this week"]
    template = REVIEW_TEMPLATE.read_text(encoding="utf-8").replace("YYYY-MM-DD", monday.isoformat(), 1)
    head, _, rest = template.partition("\n")
    path.write_text(head + "\n\n" + "\n".join(facts) + "\n" + rest, encoding="utf-8")
    return path


def sunday_message(data: dict, r: dict, now: datetime, review: Path) -> str:
    gap = APPS_TARGET - r["apps_this_week"]
    lines = ["📋 Weekly review time (~20 min)" + ("" if now.weekday() == 6 else " - catching up, your PC was off on Sunday")]
    lines.append(f"\nThis week: {r['tasks_this_week']} tasks done · {r['apps_this_week']}/{APPS_TARGET} applications")
    if gap > 0:
        lines.append(f"   {gap} application{'s' * (gap != 1)} short - be honest about why in the review.")
    lines.append(A.one_line(r))
    lines.append(f"\nYour review file is ready: private/reviews/{review.name}")
    lines.append("Fill it in, then tell Claude \"weekly review\" - the Mentor sets next week's plan from it.")
    lines.append("Then re-read private/VISION.md. That's why you're doing this.")
    return "\n".join(lines)


# ── commands ────────────────────────────────────────────────────────────────
def cmd_setup() -> None:
    env = read_env()
    token = env.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("  No token yet. Open .env (repo folder), paste your @BotFather token after TELEGRAM_BOT_TOKEN=, save, "
              "then run this again.")
        return
    try:
        me = telegram_call(token, "getMe")
        updates = telegram_call(token, "getUpdates")
    except Exception as e:
        print(f"  Telegram didn't accept the token ({type(e).__name__}). Check you copied the whole thing.")
        return
    chats = {u["message"]["chat"]["id"]: u["message"]["chat"].get("first_name", "")
             for u in updates.get("result", []) if "message" in u}
    if not chats:
        print(f"  Token works (bot: @{me['result']['username']}). Now open that bot in Telegram, press Start, "
              "send it 'hi', then run this again.")
        return
    chat_id = list(chats)[-1]
    write_env_value("TELEGRAM_CHAT_ID", str(chat_id))
    env["TELEGRAM_CHAT_ID"] = str(chat_id)
    ok = send("✅ The Coach is connected. Morning tasks at 07:00, evening check-in at 21:45, "
              "weekly review Sunday 18:00. Let's get you into the field. 💪", env)
    print(f"  Chat id saved to .env. Test message {'SENT - check Telegram 🎉' if ok else 'FAILED - see coach_log.txt'}")


def run_reminder(kind: str, dry_run: bool, force: bool, now: datetime | None = None) -> None:
    now = now or datetime.now()
    state = load_state()
    sent = state.setdefault("sent", {})
    if kind == "evening" and now.hour < 12 and not force:
        log("evening skipped: it's morning - last night's check-in was missed (PC off)")
        return
    if sent.get(kind) == now.date().isoformat() and not (dry_run or force):
        log(f"{kind} skipped: already sent today")
        return
    data = A.load_goals()
    r = A.report(today=now.date(), data=data)
    if kind == "morning":
        text = morning_message(data, r, now)
    elif kind == "evening":
        text = evening_message(data, r, now)
    else:
        review = start_review_file(data, r, now.date()) if not dry_run else REVIEWS / f"{now.date().isoformat()}.md"
        text = sunday_message(data, r, now, review)
    text += rank_news(r, state) if not dry_run else ""
    if dry_run:
        print(text)
        return
    if send(text):
        sent[kind] = now.date().isoformat()
    save_state(state)


def main(argv: list[str] | None = None) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="The Coach - daily Telegram reminders")
    ap.add_argument("cmd", choices=["setup", "morning", "evening", "sunday"])
    ap.add_argument("--dry-run", action="store_true", help="print the message, don't send it")
    ap.add_argument("--force", action="store_true", help="send even if already sent today")
    a = ap.parse_args(argv)
    if a.cmd == "setup":
        cmd_setup()
    else:
        run_reminder(a.cmd, a.dry_run, a.force)


if __name__ == "__main__":
    main()
