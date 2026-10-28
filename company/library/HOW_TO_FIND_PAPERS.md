# How to find papers and public datasets (and reproduce one figure)

The loop every bioinformatics project starts with:
**question → paper → the paper's data accession → download → read the methods → reproduce one figure → go further.**
Job adverts call this "working with public omics data". Here's how to do each step yourself.

## 1. Find papers
**Europe PMC** (<https://europepmc.org>): free full text for a lot of papers, and the search covers the full text.
- `psoriasis AND "RNA-seq" AND OPEN_ACCESS:y`: open-access papers you can read in full.
- Add `GSE` to the search to find papers that state a GEO accession in the text.

**PubMed** (<https://pubmed.ncbi.nlm.nih.gov>): the standard index.
- `psoriasis[mh] AND rna-seq[tiab]`: `[mh]` = the official MeSH subject heading, `[tiab]` = title or abstract.
- Filters on the left: **Free full text**, **Review** (read a recent review first to refresh the biology), years.

**Reading order for a paper:** abstract → figures and their legends → methods → results → introduction (for the biology).

## 2. Find the data
| Database | What's there | Accessions look like |
|---|---|---|
| **GEO** <https://www.ncbi.nlm.nih.gov/geo> | expression data (RNA-seq, microarrays) + sample metadata | `GSE…` study · `GSM…` sample · `GPL…` platform |
| **SRA / ENA** <https://www.ebi.ac.uk/ena> | raw sequencing reads (FASTQ), for the Snakemake project | `PRJNA…`/`PRJEB…` project · `SRR…`/`ERR…` run |
| **ArrayExpress** (now in BioStudies) <https://www.ebi.ac.uk/biostudies/arrayexpress> | the European equivalent of GEO | `E-MTAB-…` |
| **TCGA via GDC** <https://portal.gdc.cancer.gov> | cancer: expression counts + clinical data (open access); raw reads need approval | case / file IDs |
| **UniProt** <https://www.uniprot.org> | what a protein does, where, domains | `P04637` (human p53) |
| **Ensembl** <https://www.ensembl.org> | genes, transcripts, ID conversion (BioMart) | `ENSG00000141510` (human TP53) |

**GEO search tip:** in GEO DataSets, search
`psoriasis AND "expression profiling by high throughput sequencing"[DataSet Type] AND "homo sapiens"[Organism]`.

**On a GEO study (GSE) page:** read the summary and the overall design, check the sample list (how many per group?),
then scroll down. Many human and mouse RNA-seq studies have a **Download RNA-seq counts** button (counts that NCBI
re-processed the same way for every study, which makes a clean starting point). Otherwise the authors' own files
are under *Supplementary file*.

**Raw reads (later, for the pipeline):** on ENA, search the `PRJNA…`/`SRR…` accession. The *Read Files* table
gives direct FASTQ download links, which is simpler than the SRA toolkit.

## 3. Is it a good dataset for Project 1?
- [ ] Human, bulk RNA-seq, two clear groups (e.g. disease vs healthy)
- [ ] At least 3 samples per group; 6+ is better (fewer than that and the statistics won't hold up)
- [ ] Counts are downloadable (the counts button or a supplementary counts table)
- [ ] The paper is open access, and it has a figure you could reproduce (a volcano plot, number of DE genes)
- [ ] A disease you can explain in an interview, ideally linked to your biomedical science background

## 4. Read the methods section with this checklist
Organism and tissue · number of samples per group · sequencing (single/paired-end, read length) · aligner /
quantifier and versions · how counts were normalised · differential-expression tool and its thresholds (e.g.
adjusted p < 0.05, |log2 fold change| > 1) · any samples excluded, and why.
Write the answers into `DATASETS.md`. Anything you can't find is a limitation to mention in your README.

## 5. Reproduce one figure
Pick one figure, e.g. the number of significant genes or a volcano plot. Use the paper's own thresholds. Your
numbers **won't match exactly** (different tool versions, filtering). Write down what differs and why you think it
does. That paragraph shows reviewers and interviewers that you understand the analysis.

## Exercises (the Librarian checks them)
1. Pick a disease you care about. Find **3 open-access RNA-seq papers** on it that name a GEO accession → add them to `READING_LIST.md`.
2. For the best 2, open the GSE pages and fill in a row each in `DATASETS.md` (samples per group, counts available?, download steps).
3. Run checklist 3 on both, pick one, and say why in 3 sentences. That's task G8.1.
