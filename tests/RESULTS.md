# Test record

This file holds the raw output of the checks reported in Section 7 of Bow Draw (`paper/BOW_DRAW_EN.md`) and in Section 8 of FactorX (`full/FACTORX_EN.md`). Every output below was produced by the programs in this package, in the version that is in the package. All commands were run from the package root.

## Environment

| Item | Value |
|---|---|
| Processor | AMD Ryzen 7 9700X, 8 cores, 16 threads |
| Graphics card | AMD Radeon RX 9060 XT, Vulkan driver RADV |
| Operating system | Linux 7.3 |
| Python | 3.14.10, gmpy2 2.3.1, numpy 2.5.1, matplotlib 3.11.1 |
| C compiler | GCC 16.2.1, flags `-O3 -march=native -fopenmp` (GPU host program `-O2`) |
| Shader compiler | glslc (shaderc v2026.1), `--target-env=vulkan1.2` |
| Date of the runs | 22 November 2026 (Section 12: 23 November 2026) |

Times are wall-clock seconds on this machine. Some runs shared the machine with other runs, so the times are an indication, not a benchmark.

## How to read the output

Every program marks each case with PASS or FAIL and ends with a summary line. In `check_composite.py` and `bow_draw_composite`, "rule yes" or "rule no" reports an observation that is not a theorem. A "rule no" is not a failure. Where an output is long, its first lines are omitted and this is stated.

## 1. Direct count, small bases

`python3 tests/check_small.py 41`. Every n from 1 to 3b³ + 300 is counted for 2 ≤ b ≤ 40. The closed form is compared with the count for n < 3000.

```text
b =   2: solution [12]  formula        12  minimum (3, -2)  PASS
b =   3: solution [33]  formula        33  minimum (26, -10)  PASS
b =   4: solution [82]  formula        82  minimum (47, -14)  PASS
b =   5: solution [144]  formula       144  minimum (124, -28)  PASS
b =   6: solution [256]  formula       256  minimum (179, -34)  PASS
b =   7: solution [378]  formula       378  minimum (342, -54)  PASS
b =   8: solution [582]  formula       582  minimum (447, -62)  PASS
b =   9: solution [787]  formula       787  minimum (728, -88)  PASS
b =  10: solution [1108]  formula      1108  minimum (899, -98)  PASS
b =  11: solution [1419]  formula      1419  minimum (1330, -130)  PASS
b =  12: solution [1882]  formula      1882  minimum (1583, -142)  PASS
b =  13: solution [2316]  formula      2316  minimum (2196, -180)  PASS
b =  14: solution [2952]  formula      2952  minimum (2547, -194)  PASS
b =  15: solution [3533]  formula      3533  minimum (3374, -238)  PASS
b =  16: solution [4366]  formula      4366  minimum (3839, -254)  PASS
b =  17: solution [5118]  formula      5118  minimum (4912, -304)  PASS
b =  18: solution [6172]  formula      6172  minimum (5507, -322)  PASS
b =  19: solution [7110]  formula      7110  minimum (6858, -378)  PASS
b =  20: solution [8418]  formula      8418  minimum (7599, -398)  PASS
b =  21: solution [9567]  formula      9567  minimum (9260, -460)  PASS
b =  22: solution [11152]  formula     11152  minimum (10163, -482)  PASS
b =  23: solution [12537]  formula     12537  minimum (12166, -550)  PASS
b =  24: solution [14422]  formula     14422  minimum (13247, -574)  PASS
b =  25: solution [16056]  formula     16056  minimum (15624, -648)  PASS
b =  26: solution [18276]  formula     18276  minimum (16899, -674)  PASS
b =  27: solution [20185]  formula     20185  minimum (19682, -754)  PASS
b =  28: solution [22762]  formula     22762  minimum (21167, -782)  PASS
b =  29: solution [24972]  formula     24972  minimum (24388, -868)  PASS
b =  30: solution [27928]  formula     27928  minimum (26099, -898)  PASS
b =  31: solution [30450]  formula     30450  minimum (29790, -990)  PASS
b =  32: solution [33822]  formula     33822  minimum (31743, -1022)  PASS
b =  33: solution [36683]  formula     36683  minimum (35936, -1120)  PASS
b =  34: solution [40492]  formula     40492  minimum (38147, -1154)  PASS
b =  35: solution [43719]  formula     43719  minimum (42874, -1258)  PASS
b =  36: solution [47986]  formula     47986  minimum (45359, -1294)  PASS
b =  37: solution [51588]  formula     51588  minimum (50652, -1404)  PASS
b =  38: solution [56352]  formula     56352  minimum (53427, -1442)  PASS
b =  39: solution [60357]  formula     60357  minimum (59318, -1558)  PASS
b =  40: solution [65638]  formula     65638  minimum (62399, -1598)  PASS
39 bases, 0 failures
[2.23 s]
```

## 2. Existence proof: polynomial certificates

`python3 tests/check_certificates.py`.

```text
b = 12t + 0   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >= 12  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 1   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >= 13  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 2   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >= 14  smaller bases [2] checked directly: True  300 values: True  PASS
b = 12t + 3   n odd   certificates  7  E_b(n) - n = 0 as a polynomial: True  valid for b >=  3  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 4   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >=  4  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 5   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >= 17  smaller bases [5] checked directly: True  300 values: True  PASS
b = 12t + 6   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >=  6  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 7   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >= 19  smaller bases [7] checked directly: True  300 values: True  PASS
b = 12t + 8   n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >=  8  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 9   n odd   certificates  7  E_b(n) - n = 0 as a polynomial: True  valid for b >=  9  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 10  n even  certificates  9  E_b(n) - n = 0 as a polynomial: True  valid for b >= 10  smaller bases [] checked directly: True  300 values: True  PASS
b = 12t + 11  n odd   certificates  7  E_b(n) - n = 0 as a polynomial: True  valid for b >= 11  smaller bases [] checked directly: True  300 values: True  PASS
all twelve classes: PASS
[0.18 s]
```

## 3. Steps of the uniqueness proof

`python3 tests/check_proof_steps.py 151`. Odd bases 3 ≤ b ≤ 149, prime and composite. The first 72 lines (b = 3 to 145) are omitted. Each of them reads `all steps PASS`.

```text
b = 147 (composite): all steps PASS
b = 149 (prime): all steps PASS
74 odd bases, 0 failures
```

## 4. Direct count in C

`gcc -O3 -march=native -fopenmp tests/c/bow_draw_scan.c -o bow_draw_scan`, then `./bow_draw_scan 600 all` and `./bow_draw_scan 1000 primes`. For every base the program checks one solution equal to n(b), the sign pattern, and the minimum. For odd b the minimum must lie at n = b³ − 1 with value −(b − 1)(b + 2). For even b ≥ 4 it must lie at n = b³ − b² − 1 with value −(b² − 2). "steps" is the number of rows counted.

```text
== ./bow_draw_scan 600 all
all bases 2 <= b < 600: 598 bases, 96876449397 steps (every n counted), 598 PASS, 0 FAIL  [126.7 s]
== ./bow_draw_scan 1000 primes
primes 2 <= b < 1000: 168 bases, 109503445911 steps (every n counted), 168 PASS, 0 FAIL  [144.1 s]
```

## 5. Direct count on the graphics card

`sh tests/gpu/build.sh`, then `./tests/gpu/bow_draw_gpu 2000`. For every base the program checks one solution equal to n(b), the sign pattern, and for odd b the minimum. The minimum of even bases is checked by the C program in Section 4. The first two lines come from the driver and from the Vulkan helper. The driver warns that RADV is not a conformant implementation. This run was recorded when the program still printed its messages in Turkish: `kart` means card. The program now prints `card:`. The last line is the time and peak memory measured with `/usr/bin/time`.

```text
WARNING: radv is not a conformant Vulkan implementation, testing use only.
kart: AMD Radeon RX 9060 XT (RADV GFX1200) ; shaderInt64=1
GPU full scan, all bases (64-bit, division-free): 1998 bases (2 <= b < 2000), 11988003599397 steps; one solution = n_draw, sign pattern and minimum: 1998/1998 PASS
card time 746.8 s, total 1602.9 s; blocks recounted on the CPU: 1998
[1602.98 s, peak 58632 KB]
```

## 6. Closed form, all primes and random large primes

`python3 tests/check_primes.py` (default: primes below 10⁶ and 200 random primes):

```text
all primes 5 <= p < 1000000: 78496 primes, 0 failures  PASS  [0.9 s]
200 random primes (20 to 200 digits): 200/200  PASS  [1.1 s]
[1.98 s]
```

`python3 tests/check_primes.py 1000000000 12000`:

```text
all primes 5 <= p < 1000000000: 50847532 primes, 0 failures  PASS  [38.3 s]
12000 random primes (20 to 200 digits): 12000/12000  PASS  [20.7 s]
[59.04 s, peak 22496 KB]
```

`python3 tests/check_primes.py 10000000000 12000`:

```text
all primes 5 <= p < 10000000000: 455052509 primes, 0 failures  PASS  [426.8 s]
12000 random primes (20 to 200 digits): 12000/12000  PASS  [22.4 s]
[449.17 s, peak 24380 KB]
```

## 7. Mersenne primes

`python3 tests/check_mersenne.py 136279841 132049 2`. Exponents up to 132 049 are confirmed prime by the Lucas-Lehmer test inside the program. Larger exponents are taken from the list of known Mersenne primes. Two random points on each side of n(p) are checked for every p.

```text
Lucas-Lehmer: 30 exponents e <= 132049 confirmed: True  [41.1 s]
e =         3  p has         1 digits  PASS  [0.0 s]
e =         5  p has         2 digits  PASS  [0.0 s]
e =         7  p has         3 digits  PASS  [0.0 s]
e =        13  p has         4 digits  PASS  [0.0 s]
e =        17  p has         6 digits  PASS  [0.0 s]
e =        19  p has         6 digits  PASS  [0.0 s]
e =        31  p has        10 digits  PASS  [0.0 s]
e =        61  p has        19 digits  PASS  [0.0 s]
e =        89  p has        27 digits  PASS  [0.0 s]
e =       107  p has        33 digits  PASS  [0.0 s]
e =       127  p has        39 digits  PASS  [0.0 s]
e =       521  p has       157 digits  PASS  [0.0 s]
e =       607  p has       183 digits  PASS  [0.0 s]
e =      1279  p has       386 digits  PASS  [0.0 s]
e =      2203  p has       664 digits  PASS  [0.0 s]
e =      2281  p has       687 digits  PASS  [0.0 s]
e =      3217  p has       969 digits  PASS  [0.0 s]
e =      4253  p has      1281 digits  PASS  [0.0 s]
e =      4423  p has      1332 digits  PASS  [0.0 s]
e =      9689  p has      2917 digits  PASS  [0.0 s]
e =      9941  p has      2993 digits  PASS  [0.0 s]
e =     11213  p has      3376 digits  PASS  [0.0 s]
e =     19937  p has      6002 digits  PASS  [0.0 s]
e =     21701  p has      6533 digits  PASS  [0.0 s]
e =     23209  p has      6987 digits  PASS  [0.0 s]
e =     44497  p has     13395 digits  PASS  [0.0 s]
e =     86243  p has     25962 digits  PASS  [0.1 s]
e =    110503  p has     33265 digits  PASS  [0.1 s]
e =    132049  p has     39751 digits  PASS  [0.2 s]
e =    216091  p has     65050 digits  PASS  [0.3 s]
e =    756839  p has    227832 digits  PASS  [1.6 s]
e =    859433  p has    258716 digits  PASS  [1.3 s]
e =   1257787  p has    378632 digits  PASS  [2.1 s]
e =   1398269  p has    420921 digits  PASS  [2.3 s]
e =   2976221  p has    895932 digits  PASS  [5.9 s]
e =   3021377  p has    909526 digits  PASS  [4.7 s]
e =   6972593  p has   2098960 digits  PASS  [17.0 s]
e =  13466917  p has   4053946 digits  PASS  [36.5 s]
e =  20996011  p has   6320430 digits  PASS  [53.9 s]
e =  24036583  p has   7235733 digits  PASS  [78.1 s]
e =  25964951  p has   7816230 digits  PASS  [111.5 s]
e =  30402457  p has   9152052 digits  PASS  [133.1 s]
e =  32582657  p has   9808358 digits  PASS  [154.4 s]
e =  37156667  p has  11185272 digits  PASS  [132.9 s]
e =  42643801  p has  12837064 digits  PASS  [172.6 s]
e =  43112609  p has  12978189 digits  PASS  [207.7 s]
e =  57885161  p has  17425170 digits  PASS  [364.2 s]
e =  74207281  p has  22338618 digits  PASS  [226.9 s]
e =  77232917  p has  23249425 digits  PASS  [214.3 s]
e =  82589933  p has  24862048 digits  PASS  [237.6 s]
e = 136279841  p has  41024320 digits  PASS  [445.6 s]
51 Mersenne primes, 0 failures
[2645.98 s, peak 1038564 KB]
```

The same 51 results as a table: `tests/mersenne.csv` (exponent, digits, result, seconds).

## 8. Composite m

`python3 tests/check_composite.py` (2 ≤ m ≤ 40, n range chosen automatically):

```text
2 <= m <= 40, every n from 1 to 152959 counted
m =   2  prime                        solutions   1  first     12  PASS
m =   3  prime                        solutions   1  first     33  PASS
m =   4  prime power                  solutions  12  first     60
m =   5  prime                        solutions   1  first    144  PASS
m =   6  square-free                  solutions   1  first     33  PASS
m =   7  prime                        solutions   1  first    378  PASS
m =   8  prime power                  solutions  11  first    252
m =   9  prime power                  solutions   7  first    321
m =  10  square-free                  solutions   1  first    144  PASS
m =  11  prime                        solutions   1  first   1419  PASS
m =  12  other (farthest factor 4)    solutions  12  first     60  rule yes
m =  13  prime                        solutions   1  first   2316  PASS
m =  14  square-free                  solutions   1  first    378  PASS
m =  15  square-free                  solutions   1  first    144  PASS
m =  16  prime power                  solutions   7  first   1020
m =  17  prime                        solutions   1  first   5118  PASS
m =  18  other (farthest factor 9)    solutions   7  first    321  rule yes
m =  19  prime                        solutions   1  first   7110  PASS
m =  20  other (farthest factor 5)    solutions   1  first    144  rule yes
m =  21  square-free                  solutions   1  first    378  PASS
m =  22  square-free                  solutions   1  first   1419  PASS
m =  23  prime                        solutions   1  first  12537  PASS
m =  24  other (farthest factor 8)    solutions  11  first    252  rule yes
m =  25  prime power                  solutions   2  first   3668
m =  26  square-free                  solutions   1  first   2316  PASS
m =  27  prime power                  solutions  21  first   2913
m =  28  other (farthest factor 7)    solutions   1  first    378  rule yes
m =  29  prime                        solutions   1  first  24972  PASS
m =  30  square-free                  solutions   1  first    144  PASS
m =  31  prime                        solutions   1  first  30450  PASS
m =  32  prime power                  solutions  15  first   4092
m =  33  square-free                  solutions   1  first   1419  PASS
m =  34  square-free                  solutions   1  first   5118  PASS
m =  35  square-free                  solutions   1  first    378  PASS
m =  36  other (farthest factor 9)    solutions   7  first    321  rule yes
m =  37  prime                        solutions   1  first  51588  PASS
m =  38  square-free                  solutions   1  first   7110  PASS
m =  39  square-free                  solutions   1  first   2316  PASS
m =  40  other (farthest factor 8)    solutions  11  first    252  rule yes
39 values of m, 0 skipped: 0 failures among primes and square-free m  PASS; farthest-factor rule 7 yes, 0 no
[4.53 s]
```

`gcc -O3 -march=native -fopenmp tests/c/bow_draw_composite.c -o bow_draw_composite`, then `./bow_draw_composite 1000`:

```text
rule does not hold: m = 72, farthest factor 9 (7 solutions: 321 325 326 327 ...), m has 9 solutions: 321 323 324 325 326 327 ...
   rule does not hold: m = 360, farthest factor 9 (7 solutions: 321 325 326 327 ...), m has 9 solutions: 321 323 324 325 326 327 ...
   rule does not hold: m = 544, farthest factor 17 (1 solutions: 5118), m has 13 solutions: 5118 5120 5121 5371 5372 5377 ...
2 <= m <= 1000 (every n counted):
   primes: 168, exactly one solution: 168  PASS
   square-free composites: 439, one solution equal to that of the largest prime factor: 439  PASS
   prime powers q^a (a >= 2): 25, of which with exactly one solution: 8
   composites with two or more prime factors: 806, same set as the farthest prime-power factor: 803, different: 3  (observation)
   prime powers with exactly one solution: 49 (18710) 121 (172015) 169 (392041) 289 (1479875) 361 (2568060) 529 (6633447) 841 (21003686) 961 (29266018)
   [261.6 s]
```

## 9. Figures

`python3 tests/make_figures.py en figures` and `python3 tests/make_figures.py tr figures` produce the five figures of FactorX (the Turkish ones with the suffix `_tr`) from the definitions. The program prints the first solutions of the prime powers used in Figure 5.

## 10. The universe language

`python3 tests/check_universe_language.py 200000 6000`. The program checks Theorems 1 to 3 of FactorX (Section 3), the count with ordinary digits, the large examples and Bow Draw in three universes. The number of universes is computed from the divisors and τ(n) from the prime factorisation, separately.

```text
1. every n, 2 <= n <= 200000: universes = tau(n) - 1, one universe <=> prime: 0 failures  PASS
    7 1 [1][1]_6
    9 2 [1][1]_8  [3][3]_2
    12 5 [1][1]_11  [2][2]_5  [3][3]_3  [4][4]_2  [6][6]_1
    17 1 [1][1]_16
2. composites 4 <= n <= 200000 with no copy in ordinary digits = 6 and the prime squares: 87 numbers: [4, 6, 9, 25, 49, 121] ...  PASS
3. 200000 random additions, bases 2 to 999, numbers below 10^30: largest carry: 1  PASS
4. rows d - 1 for 2 <= d <= 6000: break column = smallest prime factor, none for primes: 0 failures  PASS
   d = 3587 = 17 * 211: breaks at column 17  PASS
   d = 1022117 = 1009 * 1013: breaks at column 1009  PASS
5. 2^61 - 1 = 2305843009213693951 is prime, so it appears in 1 universe: [1][1]_2305843009213693950  PASS
   2^67 - 1 = 147573952589676412927 = 193707721 * 761838257287, both factors prime, so tau = 4 and 3 universes: [1][1]_147573952589676412926  [193707721][193707721]_761838257286  [761838257287][761838257287]_193707720  PASS
6. universe 7: E_b(n) = n: solutions [378], formula 378  PASS
6. universe 9: E_b(n) = n: solutions [787], formula 787  PASS
6. universe 10: E_b(n) = n: solutions [1108], formula 1108  PASS
0 failures
[5.42 s, peak 11232 KB]
```

## 11. Not run in this record

The following were not run for this record. The certificate check, the proof-step check and the direct counts do not depend on them.

1. No check was run on another machine or operating system.
2. The C programs were not compiled with other compilers.
3. For even bases b ≥ 2000, nothing was counted.

## 12. Existence and location for odd bases (Step 6)

`python3 tests/check_odd_existence.py 401`, added on 23 November 2026 with Step 6 of the odd-base proof (FactorX Section 6.4, Bow Draw paper Section 5.4). For every odd b from 3 to 401 the program counts G directly and checks the closed expression for G in the upper half of the block d = r, that the steps of G there are 1 or 2, and that the zero given by the table of Step 6 is n(b). It prints the first bases and every failure. Same machine as above.

```text
b =    3  zero of D_b from Step 6 at n = 33  PASS
b =    5  zero of D_b from Step 6 at n = 144  PASS
b =    7  zero of D_b from Step 6 at n = 378  PASS
b =    9  zero of D_b from Step 6 at n = 787  PASS
b =   11  zero of D_b from Step 6 at n = 1419  PASS
b =   13  zero of D_b from Step 6 at n = 2316  PASS
b =   15  zero of D_b from Step 6 at n = 3533  PASS
odd bases 3 <= b <= 401: 200 bases, 0 failures
[303.09 s, peak 30572 KB]
```
