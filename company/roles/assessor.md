# The Assessor

**Job:** celebrations and scores, worked out by a script from what actually happened, so it can't be flattered.

| Points | For |
|---:|---|
| +10 | a task ticked off (`python plan/goal.py done <id>`) |
| +50 | a whole goal achieved |
| +5 | an application sent (a dated row in `private/job_hunt/APPLICATIONS.md`) |
| +5 | a real 3-sentence answer in `LEARNING_LOG.md` |
| +2 | every active day (a tick, an application or a commit to this repo) |

**Ranks:** Trainee (0) → Apprentice Analyst (50) → Junior Analyst (150) → Analyst (300) → Bioinformatician (500)
→ Senior Bioinformatician (800) → Lead Scientist (1200). A rank-up is announced in the next Coach message.

**Streak:** active days in a row. **One missed day per week (Mon–Sun) is your rest day** and doesn't break it.
Badges at 3, 7, 14, 30, 60 and 100 days.

| | |
|---|---|
| **Inputs** | `plan/goals.json`, `private/job_hunt/APPLICATIONS.md`, `LEARNING_LOG.md`, `git log` |
| **Outputs** | numbers on screen and in every Coach message. Nothing is stored, so there's no scoreboard file in the public repo. |
| **Code** | [`company/tools/assessor.py`](../tools/assessor.py) — run `python company/tools/assessor.py` |
| **Built as** | tooling, written by Claude |

**Honesty rule:** a task must be at least ~30 minutes of real work. Adding tiny tasks to farm points only fools
yourself, and the Strategist will notice.
