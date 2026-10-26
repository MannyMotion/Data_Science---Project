# How my learning company works

One goal: **a bioinformatics / data science job by April 2027.** Eight roles keep me moving. Two are free scripts
on my PC; the rest are Claude in this repo, each with a clear job. I do the learning; they plan, teach, check,
remind and celebrate.

## Who does what
| Role | Does | Ask it |
|---|---|---|
| 🧭 [Mentor](roles/mentor.md) (CEO) | Sets the weekly plan, holds me to the order of work | "Mentor: plan my week" |
| 📚 [Tutor](roles/tutor.md) | Teaches, sets exercises, reviews my code (I write it) | "Tutor: next video session" |
| 📱 [Coach](roles/coach.md) | Telegram: today's 3 at 07:00, check-in at 21:45, review Sunday 18:00 | *(automatic, free)* |
| 🔭 [Strategist](roles/strategist.md) | Monthly: what's working, what's not, what to change | "Strategist: monthly review" |
| 📖 [Librarian](roles/librarian.md) | Papers and datasets for each project; teaches me to search | "Librarian: check my dataset pick" |
| 💼 [Careers Officer](roles/careers_officer.md) | CV, LinkedIn, tailoring, interview prep, applications tracker | "Careers: tailor my CV for <link>" |
| ⚖️ [Council](roles/council.md) | Scores big decisions 0–100 and logs them | "Council: should I …?" |
| 🏆 [Assessor](roles/assessor.md) | Points, streaks, ranks, celebrations | `python company/tools/assessor.py` *(free)* |

## My rhythm
- **Every day:** see the [routine card](ROUTINE_CARD.md). The Coach's 07:00 message gives today's 3 tasks;
  the 21:45 check-in asks what got done.
- **When I finish a task:** `python plan/goal.py done <id>` → celebration, points, the board updates.
- **When I learn something:** 3 sentences in `LEARNING_LOG.md`. That's my interview answer.
- **Sunday 18:00:** the Coach makes `private/reviews/<date>.md` with the week's facts filled in. I fill in
  the rest, then tell Claude "weekly review", and the Mentor sets next week's `this_week` list.
- **Last Sunday of the month:** "Strategist: monthly review".
- **Big decision:** "Council: should I …?" before spending money or changing course.

## How to ask for help
Open this folder in VS Code and talk to Claude. Start with the role's name, e.g. "Tutor: I don't get loops", or
just say what's going on. Stuck for more than 20 minutes? Ask; that's what the Tutor is for.

## The Coach on Telegram
- **First-time setup:** put the bot token in `.env` (repo folder, git-ignored), message the bot once, then run
  `python company/tools/coach.py setup`. It finds the chat id and sends a test message.
- **See a message without sending it:** `python company/tools/coach.py morning --dry-run` (or `evening` / `sunday`).
- **Did it run?** Look in `company/tools/coach_log.txt`.

### Switching the Coach off
Run these in PowerShell from the repo folder:
- **Pause** (keep the tasks, stop the messages):
  `Get-ScheduledTask -TaskPath "\LearningCompany\" | Disable-ScheduledTask`
  Resume: `Get-ScheduledTask -TaskPath "\LearningCompany\" | Enable-ScheduledTask`
- **Off completely:** `.\company\tools\remove_tasks.ps1` · **back on:** `.\company\tools\install_tasks.ps1`
- **Change the times:** edit the `-At "07:00"` style times in `company/tools/install_tasks.ps1`, then run it again.

## Where things live
```
company/   roles/ (one page per role) · tools/ (coach.py, assessor.py, tests, scheduler scripts) · library/
plan/      goals.json (the source of truth; this_week = the Mentor's plan) · goal.py · board.html
private/   job_hunt/ (applications, contacts, advert skills) · reviews/ (weekly + monthly). Never pushed.
.env       the Telegram token. Never pushed, never pasted into chat.
```
