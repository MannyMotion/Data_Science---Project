# Decisions

Newest first. One line of *what* and one of *why*.

## 2026-10-28 — My dissertation first, one numbered track, Rosalind 3× a week
- **What:**
  - The video is slimmed to 16 sessions (G2): Regex and Project #4 skipped, the ML chapter kept. Finishes 16 Nov.
  - Rosalind runs 3× a week, Tue · Thu · Sat (G3).
  - Kaggle and Git follow the video; SQL + R come in January (G4).
  - Projects reordered:
    1. **PM2.5 v2**, my MSc dissertation rebuilt with pollution + health data (G5).
    2. Part B: genetics (G6).
    3. Disease ML (G7).
    4. RNA-seq (G8).
    5. Snakemake (G9).
  - A biology refresh lands before each project (G10).
  - Every task is one step of the loop in `learning/HOW_I_LEARN.md`: learn → do → box it → next. The Coach shows
    each goal only on its days (projects Mon · Wed · Fri · Sat, Rosalind Tue · Thu · Sat).
- **How I'm taught:** I do → we do → you do.
  1. Every question starts with my own attempt at the 7 steps.
  2. It gets reviewed and shown as a worked plan.
  3. Then it's built together, one function at a time, and recapped.
  4. The next day starts with a recap from memory.
  5. Saturday is a week review: annotate all the week's code, plus one big question.

  The help fades week by week.
- **Why:** my dissertation is my starting point and my best interview story. I want it done properly, then built on.
  Small numbered steps keep me moving and show the progress on GitHub.
- **Trade-off:** RNA-seq moves to March and Snakemake to April, which is after the job deadline. If the job-advert
  research (G1.1) shows most adverts want RNA-seq / NGS pipelines, the Strategist's end-of-November review revisits
  the order.

## 2026-10-26 — Build a "learning company" around the plan (Phase 0)
- **What:** `company/` with eight roles (Mentor, Tutor, Coach, Strategist, Librarian, Careers Officer, Council,
  Assessor). The Coach and the Assessor are free Python scripts (Telegram via Task Scheduler on this PC); the rest
  are Claude roles with one page each. Layout approved by me; tightened in review (one `tools/` folder, Council
  scale in its role file, monthly reports kept private, the Mentor's weekly plan as `this_week` in `goals.json`).
- **Why:** I need structure, reminders and visible progress to keep going for five months, at zero running cost.

## 2026-10-26 — Routine sized for a full-time job
- **What:** work days ~2.5h (1h learning · 1h project · 30m career), Saturday the full 2h · 2h · 1h, Sunday rest +
  review — ~17–18h a week (`company/ROUTINE_CARD.md`).
- **Why:** 5h every evening after an 08:00–18:00 job means midnight finishes six days a week; steady beats burnt out.

## 2026-10-26 — This repo becomes my learning + planning hub
- **What:** course work in `learning/`, portfolio projects in `projects/`, goals + tasks in `plan/` (goal board,
  achievements), personal plans in `private/` (git-ignored). Claude works here in tutor mode (see CLAUDE.md).
- **Why:** one structured place to learn, track progress toward a job by April 2027, and show the work. Each
  finished portfolio project may later get its own repo; BioAgent stays the flagship.
