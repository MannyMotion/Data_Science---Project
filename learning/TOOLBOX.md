# My toolbox: the 7 steps

Every option I've met for each step: **what it is, when to use it, why.** Updated after every question.
✓ = I've used it (and where). The full method: [HOW_I_LEARN.md](HOW_I_LEARN.md).

## How I answer (short format)
```
1 Question   Find ___ → output ___
2 Data       Input: ___ (format) → store as ___ because ___
3 Look       Check: ___
4 Clean      Fix: ___
5 Compute    Method: ___ because ___
6 Check      Tiny example by hand → expect ___
7 Report     Print: ___ (exact format)
Layout       function(input) → output · handbook page
```

## Step 2 · Data: file formats
| Format | Looks like | Holds | Seen in |
|---|---|---|---|
| **FASTA** | a `>ID` line, then sequence line(s) | DNA / RNA / protein sequences | ✓ R1 |
| **FASTQ** | 4 lines per read: `@ID`, sequence, `+`, quality scores | raw sequencing reads | later |
| **CSV / TSV** | rows × columns, split by commas / tabs | tables: counts, clinical data | PM2.5 v2 |
| **VCF** | one row per variant: CHROM, POS, ID, REF, ALT… | genetic variants | Part B |

## Step 2 · Data: structures (where the data lives in Python)
| Structure | Picture | Use it when | Example |
|---|---|---|---|
| **list** `[ ]` | a numbered row of boxes | order matters, items have no names | `["A", "T", "G"]` |
| **dictionary** `{key: value}` | labelled drawers | every item has a name / ID | `{"Rosalind_0001": "ATGCGCGGAT"}` ✓ R1 |
| **set** `{ }` | a bag with no duplicates | unique items, fast "is it in here?" | unique gene names |
| **tuple** `( )` | a sealed pair | values that belong together and don't change | `("Rosalind_0001", 60.0)` |
| **DataFrame** | a spreadsheet | tables with named columns | PM2.5 v2 |

## Step 3 · Look
| Tool | Shows you | Use it when |
|---|---|---|
| print the first few lines | what one record looks like | always first ✓ R1 |
| count the records (`>` lines, `len()`, `df.shape`) | how many there are | always |
| spot multi-line records | whether one record spans several lines | text formats like FASTA ✓ R1 |
| `df.head()` · `df.info()` · `df.isna().sum()` | columns, data types, missing values | tables |

## Step 4 · Clean
| Fix | Code idea | Use it when |
|---|---|---|
| strip invisible characters | `line.strip()` removes the `\n` and spaces | every text file ✓ R1 |
| join a record split over lines | add each line onto the current string | FASTA ✓ R1 |
| make the case consistent | `seq.upper()` | upper- and lower-case letters mixed |
| drop or fill missing values | `dropna()` · `fillna()` | tables |
| remove duplicates | `drop_duplicates()` | tables |
| fix data types | `astype()` · `pd.to_numeric()` | numbers stored as text |

## Step 5 · Compute
| Method | What it does | Use it when | Example |
|---|---|---|---|
| **counting** | how many of something | "what fraction / how many" questions | GC % = (G + C) ÷ length × 100 ✓ R1 |
| **max / min / sort** | finds the top or bottom | "highest", "lowest", "top 10" | highest GC ✓ R1 |
| **string methods** | replace, reverse, find | transcription, reverse complement, motifs | R2–R7 |
| **group + summarise** | an average (or sum) per group | per council area, per condition | PM2.5 v2 |
| **merge** | joins tables on a shared ID | combining datasets | PM2.5 v2 |
| **pairwise alignment** | lines up **two** sequences and scores the matches. Needleman–Wunsch = the whole length (global); Smith–Waterman = the best-matching region (local) | comparing two sequences | not for R1 |
| **database search (BLAST)** | finds similar sequences in a huge database | "what is this sequence?" | later |
| **statistical test** | is a difference real, or chance? | comparing groups | t-test |
| **model** | learns a pattern to predict new cases | prediction | regression, random forest |

## Step 6 · Check
| Check | How | Use it when |
|---|---|---|
| tiny example by hand | work it out on paper, compare with the code | always ✓ R1 |
| the sample answer | Rosalind gives a sample input + its correct output | every Rosalind problem |
| print the in-between results | print what each function returns | while building ✓ R1 |
| count before / after | rows in vs rows out | cleaning, merging |
| `assert` | a line that stops the code if a result is wrong: `assert gc_content("GGCC") == 100` | small functions |
| baseline | compare a model with "always predict the average" | machine learning |

## Step 7 · Report
| Output | Use it when |
|---|---|
| exactly the format asked for | Rosalind: an extra line counts as wrong ✓ R1 |
| a table / CSV | many results |
| a plot | patterns and comparisons |
| 3 sentences + one limitation | projects, interviews |

## Words I've learned
| Word | Meaning | First seen |
|---|---|---|
| **FASTA** | a text format for sequences: a `>ID` line, then the sequence | R1 |
| **parse / parser** | to read a file and turn it into a structure the code can use; the parser is the function that does it | R1 |
| **GC content** | the % of a DNA sequence that is G or C. G–C pairs have 3 hydrogen bonds (A–T has 2), so GC-rich DNA is more stable | R1 |
| **string** | text in Python, e.g. `"ATGC"` | R1 |
| **dictionary · key · value** | Python's labelled drawers: you look a **value** up by its **key** | R1 |
| **newline `\n`** | the invisible character at the end of every line in a file | R1 |
| **Smith–Waterman** | an algorithm that finds the best-matching region between two sequences (local alignment) | R1 |
| **function** | a named, reusable block of code: input → output | R1 |
| **Jupyter notebook / kernel** | a document of text cells + code cells with each output underneath; the kernel is the Python engine that runs the cells | R1 |

## Rebrush list (things I needed the answer for: revisit every Saturday)
| Date | What | Where |
|---|---|---|
| 28 Oct | Look + clean a FASTA file: sequences can span lines, strip the `\n`, drop the `>` | R1 steps 3–4 |
| 28 Oct | GC % = (G + C) ÷ length × 100: counting, not alignment | R1 step 5 |
| 28 Oct | Check with a tiny example worked out by hand **before** running | R1 step 6 |
