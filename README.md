# Manny Ogbu — Data Science & Bioinformatics

Bioinformatics graduate building the skills and portfolio to work as a **bioinformatician / data scientist**.
This repo is my learning hub: course work, portfolio projects, and a public goal board tracking my progress —
applying machine learning and statistics to biomedical data for disease prediction and pattern discovery.

**🎯 Progress: [GOAL_BOARD.md](GOAL_BOARD.md)** · **🏆 Wins: [ACHIEVEMENTS.md](ACHIEVEMENTS.md)** · **📓 [LEARNING_LOG.md](LEARNING_LOG.md)**

## Projects
| Project | What it shows | Status |
|---|---|---|
| ⭐ [BioAgent](https://github.com/MannyMotion/Bioinformatics-Agent) | Upload a FASTA/FASTQ, RNA-seq or VCF file → automatic QC, differential expression or variant annotation, plots, and a local-LLM explanation (FastAPI, RAG with ChromaDB) | v0.5.1 |
| [PM2.5 v2: air pollution and health](projects/01_pm25_air_pollution_health/) | My MSc dissertation rebuilt properly: public pollution + NHS health data per council area, a reproducible pipeline and honest modelling | in progress |
| [PM2.5 v2 Part B: genetics](projects/02_pm25_genetics/) | Adding the genetics correctly: per-person scores, variants matched on position | planned |
| [Disease prediction with ML](projects/03_disease_prediction_ml/) | Classification on a disease dataset with honest validation | planned |
| [Gene expression analysis](projects/04_gene_expression_analysis/) | RNA-seq differential expression + pathway enrichment on real public data | planned |
| [Reproducible pipeline](projects/05_snakemake_pipeline/) | FASTQ → counts with Snakemake, one command | planned |

## Learning
Python for data science (freeCodeCamp), Kaggle Learn, Rosalind bioinformatics problems, SQL and R — see
[learning/](learning/). How I work through every step: [learning/HOW_I_LEARN.md](learning/HOW_I_LEARN.md).

## Repo layout
```
plan/        goals.json (source of truth) · goal.py (tracker) · board.html (visual board) · weekly review template
learning/    courses and practice problems
projects/    portfolio projects, one folder each
company/     how I run my learning: roles, a zero-cost Telegram coach (Python + Task Scheduler),
             points/streak tracker, and a library of papers and public datasets
```

<sub>Goal tracker: `python plan/goal.py` (status) · `python plan/goal.py done G2.1` (tick off + celebrate) · `python plan/goal.py board` (open the board)</sub>
