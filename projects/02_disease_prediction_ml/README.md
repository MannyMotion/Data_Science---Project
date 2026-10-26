# Project 2 — Disease prediction with machine learning · goal G4

_Status: not started._

## Question
_Can gene expression predict ___ (e.g. cancer subtype / disease vs healthy), and which genes drive the prediction?_

## Data
_Dataset, labels, sample counts per class, link._

## Plan (BEFORE touching the data)
1. Split off a **sealed test set** first — it is used once, at the very end.
2. Baseline model (logistic regression) with cross-validation on the training set; then one stronger model.
3. Metrics: balanced accuracy / ROC-AUC, confusion matrix; compare with a "guess the majority class" baseline.
4. Feature importance → which genes, and does that make biological sense?
5. Leakage checks: scaling/feature selection fitted inside the CV folds only.

## Results · Limitations · How to run
_..._
