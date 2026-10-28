# How I learn: the loop, the 7 steps, the code layout

Everything I do is one numbered step on my [goal board](../GOAL_BOARD.md). Each step runs the same loop, so there's
never a "what now?".

## 1. Every question: I do → we do → you do
| | What happens | Who |
|---|---|---|
| 🔁 **Recap** | Start by explaining the last question **from memory**, then open its PLAN.md and code to check | me |
| 🎯 **Context** | Why this question, and where the skill gets used: in PM2.5 v2 or in a job | Claude |
| ✍️ **My attempt** | I copy [PLAN_TEMPLATE.md](rosalind/PLAN_TEMPLATE.md) and fill in the 7 steps myself. Wrong is fine | me |
| 🧑‍🏫 **Review + worked plan** | Each step is marked right / half / missed, then shown the way a bioinformatician would plan it, saved under my attempt | Claude |
| 🛠 **Build together** | In VS Code, one function at a time: the idea + a tiny example → I **predict** → I type it → run it | me, guided |
| ✅ **Check** | Run it on the tiny example I worked out by hand, then on the real dataset | me |
| 📦 **Box it** | 3-sentence recap in the PLAN.md and [LEARNING_LOG.md](../LEARNING_LOG.md) · `python plan/goal.py done <id>` · commit + push | me |

**Fading:** the help shrinks on purpose. Week 1: full worked examples. Then hints only. Then I plan and code alone,
and Claude only reviews. Recognising a worked answer isn't the same as producing one, so the training wheels come off.

**Saturday, the week review:**
1. Recap every question from the week.
2. Annotate every line of the week's code in my own words.
3. Do one **big question** that uses everything from the week.
4. Push, so the week is boxed before the new one starts.

The same loop applies to video sessions (predict → type → change something) and to every PM2.5 v2 step.

**How I want to be taught** (my answers, 28 Oct):
- **Something new:** a short explanation → a picture → an analogy → straight into an easy example.
- **When I'm wrong:**
  1. Tell me what's wrong straight away.
  2. Give up to 3 hints.
  3. If I still haven't got it, explain the process and give the answer. That item goes on the **Rebrush list** in
     [TOOLBOX.md](TOOLBOX.md).
- **Messages:** short and straight to the point, broken into steps. Scientific terms are welcome, with their meaning
  the first time. Then keep using them.
- **After every question:** [TOOLBOX.md](TOOLBOX.md) gets the new options for each step (when and why), new words,
  and the rebrush items.
- **Where the work goes:** one folder per question, holding:
  - `PLAN.md`
  - a Jupyter notebook (`.ipynb`) with text, code and outputs together, wrong attempts kept and labelled
  - the small example file

  Files are named by what they do, never `test1` or `Untitled`.

## 2. The lanes (see the [routine card](../company/ROUTINE_CARD.md))
| Lane | When | What, in order |
|---|---|---|
| 📚 Learning | every evening, 1 hour | video sessions S1–S16 (G2) → Kaggle, Git (G4) → SQL + R in January (G4) |
| 🧪 Project | Mon · Wed · Fri + Saturday 2 hours | **PM2.5 v2** Part A (G5) → Part B genetics (G6) → disease ML (G7) → RNA-seq (G8) → Snakemake (G9) |
| 🧩 Rosalind | Tue · Thu 1 hour + Saturday week review | one problem each weekday; Saturday = recap, annotate, big question (G3) |
| 💼 Career | every evening, 30 minutes | applications, CV, LinkedIn, contacts (G1, G12, G13) |

## 3. The 7 steps: any question → an answer
For every Rosalind problem and every project, these are written as a `PLAN.md` **before any code**.

| Step | Ask yourself |
|---|---|
| 1. **Question** | What is it really asking, in my own words? What will the answer look like (a number, a list, a plot)? What would prove me wrong? |
| 2. **Data** | What data answers it? Which format (FASTA, CSV/TSV, VCF…)? Where from (GEO, Ensembl, ONS, Fingertips, Kaggle)? |
| 3. **Look** | Open it before analysing. What does one record look like? How many? Anything odd? |
| 4. **Clean** | Missing values, duplicates, wrong types, IDs that don't match, records split over several lines |
| 5. **Compute** | The real work: count, filter, group, merge, test, model |
| 6. **Check** | Run it on a tiny example I can do by hand. Does the answer make biological sense? |
| 7. **Report** | The answer + one limitation, in 3 sentences |

## 4. The code layout (the same every time)
Each step becomes a function. **Write the reader first, and print what it returns before going further.**
```
read_file(path)   -> the data in a structure I can use
clean(data)       -> the same data, fixed
compute(data)     -> the answer
report(answer)    -> printed / saved exactly as asked
```
A project uses the same idea, with one numbered script per step:
```
data/raw/        downloaded files, never edited by hand
data/clean/      what the cleaning scripts write
scripts/         01_download.py → 02_clean.py → 03_merge.py → 04_model.py → 05_report.py
results/         figures + tables
README.md        question, data, method, results, limitations, how to run
requirements.txt
```
Relative paths only (`data/raw/...`, never `C:/Users/...`), so it runs on anyone's computer. Later, Snakemake runs
the numbered scripts for me.
