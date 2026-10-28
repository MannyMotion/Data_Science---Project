# R1 · GC — Computing GC content

Problem: https://rosalind.info/problems/gc/ · task G3.1 · 28 Oct 2026 · my first worked example

## The question
A FASTA file holds up to 10 DNA sequences, each with an ID like `>Rosalind_6404`. Find the sequence with the
**highest GC content** (the % of its letters that are G or C). Print its ID, then its GC % on the next line.

Tiny example (made up, small enough to check by hand):
```
>Rosalind_0001
ATGCGC
GGAT
>Rosalind_0002
ATATAT
```
Expected output:
```
Rosalind_0001
60.000000
```

## 1. My attempt (before any help)
1. **Question:** go into the file, parse it, and pull out the DNA with the most GC. Put the 10 sequences in a list,
   highest GC at the top and lowest at the bottom, then print the ID of the highest and its GC %.
2. **Data:** a file with up to 10 DNA sequences → a list.
3. **Look:** I didn't know.
4. **Clean:** I didn't know.
5. **Compute:** parse the file, clean it, run an algorithm (maybe Smith–Waterman), show the output.
6. **Check:** I didn't know.
7. **Report:** the list of sequences with their GC content, the highest one first.

## 2. Review (what was right, what I missed)
| Step | | Why |
|---|---|---|
| 1. Question | ½ | Right goal. But only the **top one** is asked for, so there's no need to sort or print all 10. |
| 2. Data | ½ | "Parse the file" is exactly right. But a plain list loses which ID belongs to which sequence → a **dictionary** `{ID: sequence}` (Python handbook p9). |
| 3. Look | ✗ | Open the file and look. Lines starting with `>` are IDs, and the lines under them are the sequence. **One sequence can run over several lines** (Rosalind_0001 does). |
| 4. Clean | ✗ | Join the pieces of each sequence into one string. Strip the invisible newline `\n` at the end of every line. Remove the `>` from the ID. |
| 5. Compute | ✗ | Smith–Waterman lines up **two** sequences against each other, so it's the wrong tool here. GC content is just counting: (number of G + number of C) ÷ length × 100. Use the simplest method that answers the question. |
| 6. Check | ✗ | Work the tiny example by hand: Rosalind_0001 = `ATGCGCGGAT` → 6 of 10 letters are G or C → **60 %**. If the lines weren't joined, the code would count only `ATGCGC` → 4 of 6 → **66.7 %**: a wrong answer with no error message. This check is what catches that. |
| 7. Report | ½ | Exactly **two lines**: the ID (without `>`) and the number. Not a list. Rosalind marks extra lines as wrong. |

**The lesson:** the hard part was steps 3, 4 and 6: looking at the data, cleaning it, and knowing what the answer
must be before running anything. That's the part of the job that can't be looked up.

## 3. Worked plan
1. **Question:** which sequence has the highest GC %? Output: its ID, then its GC % (a number like `60.000000`).
2. **Data:** a FASTA text file: a `>ID` line, then one or more sequence lines. Held in a dictionary `{ID: full sequence}`.
3. **Look:** print the file's lines. How many `>` lines are there? Does any sequence span more than one line?
4. **Clean:** go line by line. Strip each line. A `>` line starts a new entry (ID without the `>`). Any other line
   gets **added on** to the current entry's sequence.
5. **Compute:** for each ID, GC % = (count of G + count of C) ÷ length × 100. Keep the ID with the biggest value.
6. **Check:** the tiny example must give `Rosalind_0001` and `60.0`. Then download the real dataset and submit.
7. **Report:** print the ID, then the GC %.

**Code layout**
```
read_fasta(path)   -> {id: sequence}       handbook p10 (files), p7 (strip, startswith), p9 (dict)
gc_content(seq)    -> GC % as a number     handbook p6 (functions), p7 (count)
highest_gc(seqs)   -> (id, GC %)           handbook p5 (loops)
main               -> read → compute → print the two lines
```

## 4. Recap (after the code works, my own words, 3 sentences)
_..._
