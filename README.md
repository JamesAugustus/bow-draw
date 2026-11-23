# Bow Draw

Bow Draw is a counting question about Pascal's triangle. For every row k, add the two halves ⌊k/2⌋ and ⌈k/2⌉ in a base b and count the carries. After how many rows does the total number of carries equal the number of rows? The answer is an exact point n(b), just beyond b³, given by a formula that depends only on b modulo 6. For a prime base p, the total is the exponent of p in the product of the central binomial coefficients c(1)·c(2)···c(n), so n(p) is the exact point from which p^n divides that product.

[Türkçe](README_TR.md)

> **Version 1.0 (23 November 2026).** Not yet reviewed by others. The uniqueness for even bases b ≥ 4 is measured, not proved.

## Result and example

The difference between the carries and the rows first falls, reaches its lowest point near b³, and then crosses zero at the point n(b). This point depends only on b modulo 6:

```text
b even:          n(b) = b³ + b² + b − 2
b ≡ 1 (mod 6):   n(b) = b³ + (2b² + 2b − 7) / 3
b ≡ 3 (mod 6):   n(b) = b³ + (2b² + 2b − 6) / 3
b ≡ 5 (mod 6):   n(b) = b³ + (4b² + 5b − 11) / 6
```

For base 7 the carries of rows 1 to 378 add up to exactly 378, and 378 = 7³ + 35.

```text
b      2    3     5     7     11     13     17     19
n(b)   12   33   144   378   1419   2316   5118   7110
```

In the papers I prove that n(b) is a solution for every base b ≥ 2. For every odd base and for base 2 a written proof shows that n(b) is a solution and the only one, so for prime bases no computer is needed. For the other even bases the existence proof is computer-assisted. For even bases b ≥ 4 I checked the uniqueness by counting for every b < 2000, but I have not proved it. The result is not a primality test and not a factoring method.

## FactorX, the language around it

Bow Draw grew out of FactorX. FactorX describes numbers with three states: nothing (0), existence (1) and duality (two existences side by side, `11`). I call the written world of one base a universe, and a digit may be wide, larger than the base. In this language every number n ≥ 2 is the first pair `[1][1]` of the universe with base n − 1, and it appears in τ(n) − 1 universes, where τ(n) is the number of divisors. A prime is a number that appears in exactly one universe. For example 12 appears in five universes, as `[1][1]_11`, `[2][2]_5`, `[3][3]_3`, `[4][4]_2` and `[6][6]_1`. The prime 17 appears only as `[1][1]_16`. The content of these language results is classical (FactorX, Section 3.6); the language gives them one picture.

## Reading order

1. Bow Draw, the paper for referees: [paper/BOW_DRAW_EN.pdf](paper/BOW_DRAW_EN.pdf) (Markdown: [paper/BOW_DRAW_EN.md](paper/BOW_DRAW_EN.md)). It contains the definitions, the theorems with their proofs, where the problem came from, all checks, and in Appendix A the full list of the 51 Mersenne primes checked.
2. FactorX, the full text: [full/FACTORX_EN.pdf](full/FACTORX_EN.pdf) (Markdown: [full/FACTORX_EN.md](full/FACTORX_EN.md)). Section 2 is the dictionary of the language and Section 3 gives its three theorems. Sections 4 to 7 are Bow Draw. Section 4 gives the definitions, Section 6.1 the statements and Section 7 the worked examples. Sections 8 and 9 give the checks and the limits.
3. The test record: [tests/RESULTS.md](tests/RESULTS.md), with the commands and their raw output.
4. The programs, all in [tests/](tests/): Python in `tests/`, the C scans in [tests/c/](tests/c/) and the graphics card scan in [tests/gpu/](tests/gpu/).
5. A demo for teaching: [demo/bow_draw_demo.html](demo/bow_draw_demo.html). One HTML file in English and Turkish. Download it and open it in a browser; it needs no installation and no network. Pick a base b, and the bow is drawn by the carries of that base and the arrow lands at n(b), computed with exact integers. `bow_draw_demo.html?selftest=1` prints its own check and ends with a summary line.

## How to run

Python 3.8 or later is enough for the main checks. No third-party packages are needed. From the package root:

```sh
python3 tests/check_small.py
python3 tests/check_certificates.py
python3 tests/check_proof_steps.py
python3 tests/check_odd_existence.py
python3 tests/check_primes.py
python3 tests/check_composite.py
python3 tests/check_universe_language.py
```

Each program prints one line per case, marked PASS or FAIL, and ends with a summary: the number of failures, or PASS for the whole run. `check_small.py` counts every n up to 3b³ + 300 for every base below 41. `check_certificates.py` is the computer-assisted existence proof for every base (for odd bases and base 2 there is also a written proof). `check_proof_steps.py` checks every step of the uniqueness proof in odd bases, and `check_odd_existence.py` checks Step 6, the written existence proof for odd bases (default b ≤ 101; the full run to 401 is in tests/RESULTS.md). `check_primes.py` uses the closed form for all primes below one million and for 200 random primes with 20 to 200 digits by default; the full run recorded in tests/RESULTS.md used all primes below 10¹⁰ and 12 000 random primes. `check_universe_language.py` checks the three theorems of Section 3.

The optional checks need extra software. `tests/check_mersenne.py` needs gmpy2. By default it checks the 19 Mersenne primes with exponent up to 4423 in a few seconds. The full run over all 51, `python3 tests/check_mersenne.py 136279841 132049 2`, takes about 45 minutes (2646 s in tests/RESULTS.md). `tests/make_figures.py` needs numpy and matplotlib. The C programs need a C compiler with OpenMP:

```sh
gcc -O3 -march=native -fopenmp tests/c/bow_draw_scan.c -o bow_draw_scan
./bow_draw_scan 400
gcc -O3 -march=native -fopenmp tests/c/bow_draw_composite.c -o bow_draw_composite
./bow_draw_composite 500
```

The graphics card scan needs Vulkan 1.2 with 64-bit shader integers and `glslc`. Build it with `sh tests/gpu/build.sh` and run it with `./tests/gpu/bow_draw_gpu 1000`.

## Files and terms

- `paper/`: the Bow Draw paper for referees, in English (`BOW_DRAW_EN`) and Turkish (`BOW_DRAW_TR`), as PDF and Markdown.
- `full/`: FactorX, the full text with the language and my intuitions, in English (`FACTORX_EN`) and Turkish (`FACTORX_TR`).
- `README_TR.md`: this page in Turkish.
- `figures/`: the five figures, in English and in Turkish (suffix `_tr`).
- `demo/`: the teaching demo, one HTML file.
- `tests/`: the programs (Python, C in `tests/c/`, Vulkan in `tests/gpu/`), the test record `tests/RESULTS.md` and the Mersenne results as a table, `tests/mersenne.csv`.
- Licenses: all source code, the tests and the demo are covered by [MIT](LICENSE). The English and Turkish text, PDFs, figures, tables and citation metadata are covered by [CC BY 4.0](LICENSE-CC-BY-4.0). Copyright © 2026 James Augustus. Each license applies to its own materials. Each file falls under one of the two licenses; you do not choose between them.
- [CITATION.cff](CITATION.cff): citation information.

## How to cite

If you use this work in a course, a talk, a paper or a program, please cite it like this:

> James Augustus, "Bow Draw: where the carries of the central binomial coefficients catch up with the number of rows", version 1.0, 2026, doi:10.5281/zenodo.24451375.

> James Augustus, "FactorX: the universe language of numbers and its main example, Bow Draw", 2026, ORCID 0009-0002-7286-7730.

Repository: https://github.com/JamesAugustus/bow-draw · DOI: [10.5281/zenodo.24451375](https://doi.org/10.5281/zenodo.24451375) (archived on Zenodo). Citation metadata is in [CITATION.cff](CITATION.cff).

Corrections and missing references are welcome. I will add them in the next version and name the person who reported them.

James Augustus · ORCID [0009-0002-7286-7730](https://orcid.org/0009-0002-7286-7730) · jamesaugustus1313@gmail.com
