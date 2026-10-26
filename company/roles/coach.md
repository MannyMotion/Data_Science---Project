# The Coach

**Job:** accountability, for free. A Python script plus Windows Task Scheduler sends Telegram reminders. It uses no
AI and no tokens.

| When | Message |
|---|---|
| Every day 07:00 | **Today's 3:** one 📚 learning, one 🧪 project, one 💼 career task (from the Mentor's `this_week` list, then soonest due) · overdue nudges · streak, rank, applications this week |
| Every day 21:45 | **Evening check-in:** what got ticked today, what's still open, does today count for the streak |
| Sunday 18:00 | **Weekly review:** tasks done, applications vs the target of 5, and a ready-made review file in `private/reviews/` with the week's facts filled in |

If the PC is off or asleep at that time, the message is sent as soon as it's back on (marked "late"). A missed
evening check-in is skipped the next morning rather than sent stale.

| | |
|---|---|
| **Inputs** | `plan/goals.json`, `private/job_hunt/APPLICATIONS.md`, the Assessor's numbers |
| **Outputs** | Telegram messages · `private/reviews/<date>.md` (Sundays) · `company/tools/coach_log.txt` (every run, git-ignored) |
| **Code** | [`company/tools/coach.py`](../tools/coach.py) — tests: `python company/tools/test_company.py` |
| **Secrets** | the bot token lives only in `.env` (repo folder, git-ignored). Never paste it into chat or a commit. |
| **Built as** | tooling, written by Claude (not a learning target) |

**Try it without sending:** `python company/tools/coach.py morning --dry-run`
**Switch it off:** see [HOW_IT_WORKS.md](../HOW_IT_WORKS.md#switching-the-coach-off).

**Possible later upgrade (still free):** run the same script on GitHub Actions so reminders arrive even when the
PC is off. Only worth it if the late messages become a problem.
