# Manny Ogbu — Data Science & Bioinformatics

Bioinformatics graduate building the skills and portfolio to work as a **bioinformatician / data scientist**.
This repo is my learning hub: course work, portfolio projects, and a public goal board tracking my progress —
applying machine learning and statistics to biomedical data for disease prediction and pattern discovery.

**🎯 Progress: [GOAL_BOARD.md](GOAL_BOARD.md)** · **🏆 Wins: [ACHIEVEMENTS.md](ACHIEVEMENTS.md)** · **📓 [LEARNING_LOG.md](LEARNING_LOG.md)**

## Projects
| Project | What it shows | Status |
|---|---|---|
| ⭐ [BioAgent](https://github.com/MannyMotion/Bioinformatics-Agent) | Upload a FASTA/FASTQ, RNA-seq or VCF file → automatic QC, differential expression or variant annotation, plots, and a local-LLM explanation (FastAPI, RAG with ChromaDB) | v0.5.1 |
| [Gene expression analysis](projects/01_gene_expression_analysis/) | RNA-seq differential expression + pathway enrichment on real public data | planned |
| [Disease prediction with ML](projects/02_disease_prediction_ml/) | Classification from gene expression with honest validation | planned |
| [Reproducible pipeline](projects/03_snakemake_pipeline/) | FASTQ → counts with Snakemake, one command | planned |

## Learning
Python for data science (freeCodeCamp), Kaggle Learn, Rosalind bioinformatics problems — see [learning/](learning/).

## Repo layout
```
plan/        goals.json (source of truth) · goal.py (tracker) · board.html (visual board) · weekly review template
learning/    courses and practice problems
projects/    portfolio projects, one folder each
```

<sub>Goal tracker: `python plan/goal.py` (status) · `python plan/goal.py done G2.1` (tick off + celebrate) · `python plan/goal.py board` (open the board)</sub>
