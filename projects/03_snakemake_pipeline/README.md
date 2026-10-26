# Project 3 — A reproducible RNA-seq pipeline (Snakemake) · goal G5

_Status: not started._

## What it does
Raw reads (FASTQ) → quality check → alignment / quantification → gene count table, with **one command**.

## Plan
1. Small public dataset (a few samples, subsampled) so it runs on a laptop.
2. Rules: QC (FastQC) → trimming (optional) → quantification (e.g. Salmon) → merge counts → summary report (MultiQC).
3. A conda `environment.yml`, a `config.yaml` for samples, and a DAG figure of the workflow.

## How to run
_`snakemake --cores 4 --use-conda`_ (fill in once it works)
