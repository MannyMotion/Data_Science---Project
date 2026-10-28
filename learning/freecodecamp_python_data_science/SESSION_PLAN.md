# freeCodeCamp — Learn Python for Data Science (session plan)

Video: <https://www.youtube.com/watch?v=CMEWVn1uZpQ> · by The PyCoach · **17h 03m** in total ·
course code and data: <https://github.com/thepycoach/python-for-data-science>

**Slimmed (28 Oct 2026):** the Machine Learning chapter is **kept**. Two chapters are skipped:
- Regular Expressions: learned through Rosalind motif problems instead, plus page 7 of my pandas cheat sheet.
- Project #4, text classification: Kaggle Intro to ML and the PM2.5 v2 model step teach the same ML on my own kind of data.

That leaves **~10 hours**: 16 sessions of ~40 minutes, one every evening (Sunday off). It finishes **Mon 16 Nov**.
Each session is a task on the goal board (G2.1–G2.16). Tick it with `python plan/goal.py done G2.x`.

My PC runs **pandas 3**, and the video was recorded on older pandas. If a line crashes, it may be the version,
not me. Check the errata in my local cheat-sheet notes, or paste the error to Claude.

| Session | Date | Video | Why it matters for PM2.5 v2 | Cheat sheet |
|---|---|---|---|---|
| S1 · G2.1 | Thu 29 Oct | Recap my notebook (20 min) + finish Project #1 → 4:05:36 | some health data only comes as web tables | pandas p1 |
| S2 · G2.2 | Fri 30 Oct | Filtering data 4:05:36 → 4:45 | keep only English council areas and the years you need | pandas p2 |
| S3 · G2.3 | Sat 31 Oct | Filtering data 4:45 → 5:34:46 | pick one disease indicator out of hundreds | pandas p2 |
| S4 · G2.4 | Mon 2 Nov | Data extraction 5:34:46 → 6:15 | pull out exactly the columns and rows you need | pandas p2, p8 |
| S5 · G2.5 | Tue 3 Nov | Data extraction 6:15 → 6:55 | | pandas p2, p8 |
| S6 · G2.6 | Wed 4 Nov | Data extraction 6:55 → 7:31:57 | | pandas p2, p8 |
| S7 · G2.7 | Thu 5 Nov | Reshaping + pivoting → 7:50:59, Project #2 → 8:10 | the PM2.5 file has one column per year → reshape to (area, year, value) | pandas p4 |
| S8 · G2.8 | Fri 6 Nov | Project #2 visualisations 8:10 → 8:56:39 | the PM2.5-vs-disease scatter plot in step 5 | |
| S9 · G2.9 | Sat 7 Nov | GroupBy 8:56:39 → 9:35 | averages per council area or per year | pandas p5 |
| S10 · G2.10 | Mon 9 Nov | GroupBy 9:35 → 10:07:41 | | pandas p5 |
| S11 · G2.11 | Tue 10 Nov | Merging 10:07:41 → 10:45 | **the heart of the project:** join PM2.5 + disease + deprivation on area code + year | pandas p6 |
| S12 · G2.12 | Wed 11 Nov | Merging 10:45 → 11:20 | inner vs left join = which council areas silently disappear | pandas p6 |
| S13 · G2.13 | Thu 12 Nov | Merging → 11:49:12, skip Regex, Project #3 cleaning 12:45:45 → 12:58 | | pandas p6, p3 |
| S14 · G2.14 | Fri 13 Nov | Project #3 data cleaning 12:58 → 13:38 | step 4 of PM2.5 v2: missing values, wrong types, duplicates | pandas p3, p9 |
| S15 · G2.15 | Sat 14 Nov | Project #3 data cleaning 13:38 → 14:17:45 | | pandas p3, p9 |
| S16 · G2.16 | Mon 16 Nov | Machine learning with Python 14:17:45 → 14:43:45 🎉 | the first look at the model in step 5 | ML sheets 02, 04, 05 |

## Every session (the loop in [HOW_I_LEARN.md](../HOW_I_LEARN.md))
1. Open a notebook named after the chapter (e.g. `P2_Filtering_Data.ipynb`). Use relative paths (`Datasets/...`).
2. Before each new cell runs, **predict** what it prints.
3. Change one thing in each example and see what breaks.
4. **Box it:** `python plan/goal.py done G2.x` → 3 sentences in `LEARNING_LOG.md` → commit + push.

Behind? Use an early-finish day for a bonus session. Don't catch up by watching without typing; that part doesn't stick.
