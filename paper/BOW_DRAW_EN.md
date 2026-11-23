# Bow Draw

James Augustus · ORCID [0009-0002-7286-7730](https://orcid.org/0009-0002-7286-7730)

Where the carries of the central binomial coefficients catch up with the number of rows

Version 1.0, 23 November 2026 · DOI [10.5281/zenodo.24451375](https://doi.org/10.5281/zenodo.24451375)

## Abstract

Fix a base b ≥ 2. For every row k ≥ 1 of Pascal's triangle, add the two halves ⌊k/2⌋ and ⌈k/2⌉ in base b and count the carries. Let E_b(n) be the total number of carries over the rows 1 to n. When b is a prime p, Kummer's theorem says that E_p(n) is the exponent of p in the product c(1)·c(2)···c(n) of the central binomial coefficients c(k) = C(k, ⌊k/2⌋). The difference E_b(n) − n first falls, reaches a minimum near b³, then rises and crosses zero (for even b ≥ 4 this shape is measured, not proved). I call the crossing point the Bow Draw point n(b). It is given exactly by a formula that depends only on b modulo 6. For example n(b) = b³ + b² + b − 2 for every even b, and n(7) = 378.

I prove that E_b(n(b)) = n(b) for every base b ≥ 2 by a computer-assisted proof with polynomial certificates. For every odd base and for b = 2 I also prove by hand that n(b) is a solution, that it is the only one, and that E_b(n) − n changes sign only there. So for every prime base the result needs no computer. For even bases b ≥ 4 the uniqueness is measured, not proved: for every base b < 2000 I counted every n up to 3b³ + 300.

As a test of the programs, the location formula was also checked with exact integer arithmetic for all primes 5 ≤ p < 10¹⁰ (the bases 2 and 3 are counted directly), for 12 000 random primes with 20 to 200 digits, and for the known Mersenne primes 2^e − 1 with 3 ≤ e ≤ 136 279 841. These are 51 of the 52 Mersenne primes known on 22 November 2026 (list of GIMPS [7]): all except the smallest one, 2² − 1 = 3, whose base 3 is counted directly. All 51 are listed in Appendix A. For a composite m, the exponent of m in c(1)···c(n) is a different quantity. For square-free m the equation K_m(n) = n (Section 5.7) has exactly one solution, at the point of the largest prime factor: every prime has its own point, and a square-free composite takes the point of a prime.

Section 2 tells where the problem came from. All programs are part of the package, with their raw output.

## 1. Purpose and scope

The question is simple to state. Count the carries row by row. After how many rows does the total number of carries equal the number of rows? I answer it for every base b ≥ 2, with a proof of uniqueness for odd b and b = 2. I give the definitions, the location formula, the proofs, small and large worked examples and the programs that reproduce every number. I also describe where the crossing points of different bases lie relative to each other.

I do not describe a primality test, a factoring method or a hardware design. Where a statement rests only on counting over a finite range, I say so and give the range.

## 2. Where the problem came from

The question came from counting. In my earlier work I read rows of Pascal's triangle without carries in Mersenne bases (the N(p) threshold formula [8]). From there I moved to the product of the central binomial coefficients and to the exponent of every prime in it. A program that follows these exponents row by row (Factorx) showed that, for every prime, the exponent catches up with the number of rows exactly once: at 12 for 2, at 33 for 3, at 144 for 5 and at 378 for 7. I derived the location formula backwards from these numbers and then proved it (13 November 2026). On 22 November 2026 I extended the result to every base, and on 23 November 2026 I proved the existence and the location for odd bases by hand.

The starting point, in my own words (translated from Turkish):

> "A number is always as strong as its last state. … 6+6 = 7, because without the work of the earlier 6 there is no 7. … He did not solve it in 5 minutes. He solved it in 30 years + 5 minutes. … After 6 comes 7, but not as 1 after 6: 7 comes because 6 receives an existence of its own."

Here "+" is not ordinary addition. It means that a full counter overflows and passes a single unit on: in base 6, 7 is written 11. A number is an accumulation, and the carries that I count are exactly these overflows.

The name comes from the way I describe a shot:

> "Like the motion of a shot, it goes as far as I aim. I mean, the more I draw the arrow, the farther it goes. My limit is the arrow."

The difference E_b(n) − n first goes down, like a bow being drawn, and then crosses zero, where the arrow lands. The bigger the base, the farther the arrow lands, a little beyond b³. My other intuitions are explained in the appendix of the companion document FactorX [9].

## 3. Definitions and notation


### 3.1 Base, digits and carries

A base is an integer b ≥ 2. Every integer x ≥ 0 has digits 0 to b − 1 in base b. When x and y are added digit by digit, a carry occurs at a position when the digit sum there, together with the incoming carry, is at least b. The number of carries is written carries_b(x, y).

The carry into position i equals ⌊(x + y)/b^i⌋ − ⌊x/b^i⌋ − ⌊y/b^i⌋. This gives the identity

```text
carries_b(x, y) = Σ_{i ≥ 1} ( ⌊(x + y)/b^i⌋ − ⌊x/b^i⌋ − ⌊y/b^i⌋ )    (3.1)
                = ( s_b(x) + s_b(y) − s_b(x + y) ) / (b − 1)    (3.2)
```

where s_b(x) is the sum of the digits of x in base b. Both forms hold for every base, prime or composite.

### 3.2 Rows, central coefficients and the carry sum

Pascal rows are numbered from k = 0. Row k has k + 1 entries. The central coefficient of row k is its largest entry (OEIS A001405 [3]):

```text
c(k) = C(k, ⌊k/2⌋)

k      1   2   3   4    5    6    7    8     9    10
c(k)   1   2   3   6   10   20   35   70   126   252
```

For k ≥ 1 the carry count of row k in base b is

```text
κ_b(k) = carries_b(⌊k/2⌋, ⌈k/2⌉)
```

and the carry sum up to row n is

```text
E_b(n) = κ_b(1) + κ_b(2) + ... + κ_b(n)
E_b(0) = 0
D_b(n) = E_b(n) − n
```

D_b(n) is the difference between the accumulated carries and the number of rows.

### 3.3 Kummer's theorem

For a prime p and an integer N ≥ 1, v_p(N) denotes the exponent of p in N, that is the largest e with p^e dividing N. The exponent v_p(C(x + y, x)) equals carries_p(x, y) [1] (see also the survey of Granville [10]). Therefore κ_p(k) is the exponent of p in c(k), and E_p(n) is the exponent of p in the product c(1)·c(2)···c(n).

Example with p = 3 and k = 10. The two halves are 5 and 5, and 5 = 12 in base 3.

```text
      1 2
    + 1 2
    -----
    2 + 2 = 4 ≥ 3            carry 1
    1 + 1 + 1 = 3 ≥ 3        carry 2
```

There are two carries. Indeed c(10) = 252 = 4 · 9 · 7, and the exponent of 3 is 2.

For a composite base b, E_b(n) is still a well-defined carry count, but it is not the exponent of b in the product. The exponent of a composite m is a different function, called K_m(n) in Section 5.7.

### 3.4 Bow Draw point

I call the number n(b) given by formula (5.1) the Bow Draw point of b. Theorem 1 shows that E_b(n(b)) = n(b) for every b ≥ 2. For odd b and for b = 2 it is the only solution (Theorem 2). For even b ≥ 4 no other solution was found in the counted range (Section 5.1). The name describes the shape of D_b. The difference first goes down, like a bow being drawn. It reaches its lowest point near b³. Then it rises and crosses zero at n(b), which is where the arrow lands.

### 3.5 Status of statements

| Label | Meaning |
|---|---|
| HOLDS (proof) | Proved in this paper by a written argument |
| HOLDS (computer-assisted proof) | Proved in this paper. One step is a finite set of polynomial inequalities checked by a program in exact arithmetic |
| MEASURED | Counted by a program over the stated range only. No proof |
| UNTESTED | Neither proved nor counted |

Program runs report PASS or FAIL.

## 4. Method

### 4.1 Direct counting

The first method follows the definition. For each n from 1 to a bound N, the program adds the two halves of n in base b digit by digit and adds the carries to a running total. It records every zero of D_b(n), the sign of D_b(n) before and after the first zero, and the position and value of the minimum. The bound used throughout is N = 3b³ + 300, about three times the expected crossing point. This method does not use any formula. It is implemented in `tests/check_small.py` and `tests/c/bow_draw_scan.c`.

### 4.2 Closed form

The second method computes E_b(n) for one n without visiting the rows before it. Define, for the base b,

```text
f(m)     = Σ_{i ≥ 1} ⌊m / b^i⌋
g(n, q)  = Σ_{k=1..n} ⌊k / q⌋ = q · a(a − 1)/2 + a(r + 1)
           where n = a·q + r, 0 ≤ r < q
S(n)     = f(1) + f(2) + ... + f(n) = Σ_{i ≥ 1} g(n, b^i)
```

By (3.1), κ_b(k) = f(k) − f(⌊k/2⌋) − f(⌈k/2⌉). Summing over k gives

```text
E_b(n)  = S(n) − T(n)
T(2m)   = 4·S(m) − f(m)
T(2m+1) = T(2m) + f(m) + f(m + 1)    (4.1)
```

T(n) is the sum of f(⌊k/2⌋) + f(⌈k/2⌉) over k = 1 to n. For n = 2m, the even rows k = 2j contribute 2f(j) for j = 1 to m. The odd rows k = 2j + 1 contribute f(j) + f(j + 1) for j = 0 to m − 1. Together this is 2S(m) + (S(m) − f(m)) + S(m) = 4S(m) − f(m). The odd case adds row 2m + 1.

The formula for g counts the k with ⌊k/q⌋ = j. For 1 ≤ j < a there are q of them, and for j = a there are r + 1. Each value of E_b(n) costs O(log_b n) operations on integers of the size of n. For a prime p, f(m) is the exponent of p in m! (Legendre's formula [2]).

Example with b = 7 and n = 378, so m = 189: S(378) = 11 388, S(189) = 2760, f(189) = 30, T(378) = 4 · 2760 − 30 = 11 010, and E_7(378) = 11 388 − 11 010 = 378.

### 4.3 Block scan on a graphics card

The third method repeats the direct count on a graphics card with Vulkan compute shaders, as an independent implementation. The card keeps ⌊n/2⌋ and ⌈n/2⌉ as arrays of base-b digits. From n to n + 1 exactly one of the two halves increases by one, so no division is needed. The card splits the range into blocks of 256 consecutive n. For each block it returns the sum of κ_b(n) − 1 and the smallest and largest partial sum inside the block. The processor adds the blocks in order, so it knows D_b at every block boundary. It then recounts on the processor every block in which a zero is possible, and the block that contains the minimum. The program is `tests/gpu/bow_draw_gpu.c` with the shader `tests/gpu/bow_draw_block64.comp`. It uses 64-bit integers.

### 4.4 Polynomial certificates

The fourth method proves existence. Write b = 12t + r with r one of 0 to 11. In each of the twelve classes, n(b) from (5.1) is a polynomial in t with rational coefficients. Every floor ⌊x(t)/q(t)⌋ in the closed form (4.1) has a polynomial numerator x(t) and a denominator q(t) that is b, b² or b³. For each floor the program finds a candidate polynomial F(t) by interpolation. It then shows that 0 ≤ x(t) − q(t)F(t) ≤ q(t) − 1 for all t ≥ t₀. This is done by shifting t to t + t₀ and checking that every coefficient of both polynomials is non-negative. Once every floor is replaced by its certified polynomial, E_b(n(b)) − n(b) becomes a polynomial in t, and the program checks that it is the zero polynomial. Bases below t₀ are checked directly. All arithmetic is exact. Three facts make the certificate a proof. First, F(t) interpolates integer values at six consecutive integers and has degree at most 5, so all its forward differences are integers and F(t) is an integer for every integer t. Second, x(t) is an integer for every b of the class: n(b) is an integer-valued cubic in t, and its parity is constant in the class (the parity of an integer-valued cubic is periodic with a period dividing 4, and the program checks 60 consecutive values). With F and x integer valued, 0 ≤ x − qF ≤ q − 1 means exactly F = ⌊x/q⌋. Third, the program certifies b³ ≤ n(b) < b⁴ and m + 1 < b³, so the closed form has a fixed number of terms in the whole class (Section 5.3). The program is `tests/check_certificates.py`.

## 5. Mathematical relation

### 5.1 Main results

**Theorem 1 (existence).** For every integer b ≥ 2, E_b(n(b)) = n(b), where

```text
b even:              n(b) = b³ + b² + b − 2
b ≡ 1 (mod 6):       n(b) = b³ + (2b² + 2b − 7) / 3
b ≡ 3 (mod 6):       n(b) = b³ + (2b² + 2b − 6) / 3
b ≡ 5 (mod 6):       n(b) = b³ + (4b² + 5b − 11) / 6    (5.1)
```

**Theorem 2 (uniqueness and sign).** Let b be odd, or b = 2. Then n(b) is the only n ≥ 1 with E_b(n) = n. Moreover D_b(n) < 0 for 1 ≤ n < n(b) and D_b(n) > 0 for n > n(b).

**Theorem 3 (depth).** For odd b, the minimum of D_b(n) over all n ≥ 1 is −(b − 1)(b + 2). It is attained at n = b³ − 1.

| Statement | Status |
|---|---|
| Theorem 1, every b ≥ 2 | HOLDS (computer-assisted proof), Section 5.3 |
| Theorem 1, odd b and b = 2 | HOLDS (proof), Sections 5.4 and 5.5 |
| Theorem 2, odd b and b = 2 | HOLDS (proof), Sections 5.4 and 5.5 |
| Theorem 3, odd b | HOLDS (proof), Section 5.4 |
| Theorem 4, square-free m | HOLDS (proof), Section 5.7 |
| Rule of the farthest prime-power factor, composite m | MEASURED: 2 ≤ m ≤ 1000, three exceptions (72, 360, 544) |
| Uniqueness and sign pattern for even b ≥ 4 | MEASURED: every n ≤ 3b³ + 300 for every even b with 4 ≤ b < 2000 |
| Minimum for even b ≥ 4, value −(b² − 2), first reached at n = b³ − b² − 1 and kept up to n = b³ − b² + b − 1 | MEASURED: every even b with 4 ≤ b < 600 |
| Uniqueness for even b ≥ 4 beyond the counted range | UNTESTED |

For primes p ≥ 5 the formula (5.1) has a one-line form. With ε = p mod 3 (1 or 2),

```text
n(p) = p³ + (4p² + (3 + ε)·p + 3ε − 17) / 6    (5.2)
```

The two smallest primes are covered by (5.1): n(2) = 12 and n(3) = 33.

```text
b      2    3    4     5     6     7     8     9
n(b)   12   33   82   144   256   378   582   787

b      10     11     12     13     14     15     16
n(b)   1108   1419   1882   2316   2952   3533   4366
```

The parity of n(b) depends on b modulo 12. n(b) is odd exactly when b ≡ 3, 9 or 11 (mod 12), and even otherwise. The value depends on b modulo 6. No single polynomial covers all odd bases, because the linear terms of the classes differ.

In its own base b, n(b) and m = ⌊n(b)/2⌋ have fixed digits, most significant first (HOLDS, proof):

| Class | n(b) in base b | m = ⌊n(b)/2⌋ in base b |
|---|---|---|
| b even | (1, 1, 0, b−2) | (b/2, b/2, b/2−1) |
| b ≡ 1 (mod 6) | (1, 0, (2b+1)/3, (b−7)/3) | ((b−1)/2, (5b+1)/6, (b−7)/6) |
| b ≡ 3 (mod 6) | (1, 0, 2b/3, (2b−6)/3) | ((b−1)/2, (5b−3)/6, (5b−9)/6) |
| b ≡ 5 (mod 12) | (1, 0, (2b+2)/3, (b−11)/6) | ((b−1)/2, (5b−1)/6, (7b−11)/12) |
| b ≡ 11 (mod 12) | (1, 0, (2b+2)/3, (b−11)/6) | ((b−1)/2, (5b−1)/6, (7b−17)/12) |

Each row of n(b) follows from (5.1) by writing n(b) − b³ = c·b + d with 0 ≤ c, d < b, and each row of m by halving. The row b ≡ 5 (mod 12) needs b ≥ 17 for n(b); for b = 5, n(5) = 144 is (1, 0, 3, 4) in base 5. For example n(10) = 1108 is (1, 1, 0, 8) in base 10, and n(7) = 378 is (1, 0, 5, 0) in base 7, with m = 189 = (3, 6, 0). For odd b the digits of m are those of Step 6 in Section 5.4, m = (r, r + 1 + k, y). n(b) is odd exactly in the rows b ≡ 3 (mod 6) and b ≡ 11 (mod 12). These are exactly the rows where G steps over zero in that step, and this explains the parity rule above.

### 5.2 Size

From (5.1),

```text
b odd:    n(b) = b³ + (2/3)·b² + O(b)
b even:   n(b) = b³ + b² + O(b)
```

The arrow lands just beyond the cube of the base. The distance beyond the cube, measured in units of b², tends to 2/3 for odd bases and to 1 for even bases.

### 5.3 Proof of Theorem 1

The method is the one described in Section 4.4. In every class the number of terms in the closed form is fixed: the program certifies b³ ≤ n(b) < b⁴ and ⌊n(b)/2⌋ + 1 < b³ as polynomial inequalities. So S(n) has three terms and S(m), f(m) have two.

| Class | n(b) | Certificates | Valid for | Checked directly |
|---|---|---|---|---|
| b = 12t | even | 9 | b ≥ 12 | none |
| b = 12t + 1 | even | 9 | b ≥ 13 | none |
| b = 12t + 2 | even | 9 | b ≥ 14 | b = 2 |
| b = 12t + 3 | odd | 7 | b ≥ 3 | none |
| b = 12t + 4 | even | 9 | b ≥ 4 | none |
| b = 12t + 5 | even | 9 | b ≥ 17 | b = 5 |
| b = 12t + 6 | even | 9 | b ≥ 6 | none |
| b = 12t + 7 | even | 9 | b ≥ 19 | b = 7 |
| b = 12t + 8 | even | 9 | b ≥ 8 | none |
| b = 12t + 9 | odd | 7 | b ≥ 9 | none |
| b = 12t + 10 | even | 9 | b ≥ 10 | none |
| b = 12t + 11 | odd | 7 | b ≥ 11 | none |

The column Certificates counts the floors ⌊x/q⌋ that the program replaces by certified polynomials. For even n the program writes T = 2S(m − 1) + f(m) + 2S(m), with 3 + 2 + 2 + 2 = 9 floors (S(n) needs three, the other terms two each). For odd n it writes T = 4S(m) + f(m + 1), with 3 + 2 + 2 = 7 floors. Both forms equal (4.1), because S(m) − S(m − 1) = f(m).

In all twelve classes E_b(n(b)) − n(b) is the zero polynomial. The bases 2, 5 and 7, which lie below the certified range of their class, satisfy E_b(n(b)) = n(b) by direct evaluation. The twelve classes cover every b ≥ 2. ∎

The certificate uses only floors and powers of b. It does not use primality, so Theorem 1 holds for composite bases too.

### 5.4 Proof of Theorems 1 to 3 for odd b

Let b ≥ 3 be odd and r = (b − 1)/2. Write κ(h) = carries_b(h, h) for the carries of h + h. A digit d of h, with incoming carry c ∈ {0, 1}, produces a carry exactly when 2d + c ≥ b. This holds when d > r, never when d < r, and when d = r only if c = 1.

**Lemma 1 (odd rows).** For odd b and h ≥ 0, carries_b(h, h + 1) = κ(h + 1).

*Proof.* Let t(x) be the number of trailing digits of x equal to b − 1. Adding one to x turns these digits into 0 and raises the next digit by one, so s_b(x + 1) = s_b(x) + 1 − (b − 1)·t(x). By (3.2),

```text
carries_b(h, h + 1) − carries_b(h + 1, h + 1)
    = ( s_b(h) − s_b(h + 1) − s_b(2h + 1) + s_b(2h + 2) ) / (b − 1)
    = t(h) − t(2h + 1).
```

It remains to show t(2h + 1) = t(h). Compute 2h + 1 digit by digit, with the added 1 as the carry into position 0. Each of the t(h) lowest digits of h is b − 1 and receives a carry of 1. It gives 2(b − 1) + 1 = 2b − 1, so the output digit is b − 1 and a carry of 1 goes on. The next digit d of h is not b − 1, and it also receives a carry of 1. Its output digit is 2d + 1 or 2d + 1 − b. The first is odd and b − 1 is even, so it is not b − 1. The second equals b − 1 only if d = b − 1, which is excluded. Hence t(2h + 1) = t(h). ∎

So κ_b(2h) = κ(h) and κ_b(2h + 1) = κ(h + 1). The lemma fails in even bases (Section 6.3).

**Lemma 2.** Let G(m) = Σ_{h=1..m} (κ(h) − 1), with G(0) = 0. Then

```text
E_b(2m) − 2m              = 2·G(m)
E_b(2m + 1) − (2m + 1)    = G(m) + G(m + 1)
```

*Proof.* By Lemma 1 the even rows 2h and the odd rows 2h − 1 each contribute κ(h) for h = 1 to m, so E_b(2m) = 2(κ(1) + ... + κ(m)). Row 2m + 1 adds κ(m + 1). ∎

So the sign of D_b follows from the sign of G.

**Lemma 3 (block rule).** Let h = d·b^J + x with 0 ≤ x < b^J and 1 ≤ d ≤ b − 1. Then

```text
d < r :   κ(h) = κ(x)
d = r :   κ(h) = κ(x) + 1  if x > (b^J − 1)/2,   κ(h) = κ(x)  otherwise
d > r :   κ(h) = κ(x) + 1
```

*Proof.* The lower J digits produce the same carries in h + h and in x + x. A carry leaves them exactly when 2x ≥ b^J. The top digit d then carries according to the digit rule above. All digits above d are 0, so a carry out of d produces no further carry. ∎

The proof follows G over the first b³ values of m and then beyond.

**Step 0. For 1 ≤ m ≤ b² − 1, G(m) < 0, with G((b² − 1)/2) = −r² − 2r and G(b² − 1) = −r.** For one-digit h, κ(h) = 1 if h > r and 0 otherwise. So G falls by one for h = 1 to r and stays flat up to b − 1, and G(b − 1) = −r. Including x = 0, the sum of κ(x) − 1 over a full block of b values is −(r + 1). For two-digit h = d·b + x, Lemma 3 with J = 1 gives three cases. Blocks with d < r repeat this pattern, and each lowers G by r + 1. In the block d = r, κ(h) − 1 is −1 for x ≤ r and +1 for x > r. Blocks with d > r have κ(h) − 1 = κ(x) ≥ 0, and each raises G by r. Before the middle of the block d = r, G never rises. The middle is h = r·b + r = (b² − 1)/2, where

```text
G((b² − 1)/2) = −r − (r − 1)(r + 1) − (r + 1) = −r² − 2r.
```

After it, G never falls and ends at G(b² − 1) = −r² − r + r·r = −r < 0. So G is negative on the whole range. The sum of κ(x) − 1 over all x from 0 to b² − 1 is G(b² − 1) − 1 = −(r + 1).

**Step 1. For 1 ≤ m ≤ (b³ − 1)/2, G(m) < 0, and the smallest value of G on 1 ≤ m ≤ b³ − 1 is μ = G((b³ − 1)/2) = −2r² − 3r.** Take three-digit h = d·b² + x. Let B_d = G(d·b² − 1) be the value before block d. Then B_1 = −r, and each block with d < r lowers G by r + 1, so B_d = −r − (d − 1)(r + 1). Inside such a block G(d·b² + x) = B_d − 1 + G(x). By Step 0 this is negative and at least B_{r−1} − 1 − r² − 2r = −2r² − 2r + 1 > μ. In the lower half of the block d = r (x ≤ (b² − 1)/2), Lemma 3 again gives κ(h) = κ(x). So G = B_r − 1 + G(x) = −r² − r + G(x), which is smallest at x = (b² − 1)/2. Since r·b² + (b² − 1)/2 = (b³ − 1)/2,

```text
μ = G((b³ − 1)/2) = −r² − r − r² − 2r = −2r² − 3r.
```

Steps 2 to 4 show that G stays above μ for the remaining m up to b³ − 1.

**Step 2. On (b³ − 1)/2 ≤ m < (r + 1)·b² − 1, G rises by at least 1 at each step.** In the upper half of the block d = r, x > (b² − 1)/2. So x + x carries out of its top digit, κ(x) ≥ 1, and Lemma 3 gives κ(h) = κ(x) + 1 ≥ 2.

**Step 3. G((r + 1)·b² − 1) = r² > 0.** The block d = r adds −(r + 1) + (b² − 1)/2 to B_r = −r² − r + 1. With (b² − 1)/2 = 2r² + 2r the total is r².

**Step 4. On (r + 1)·b² − 1 ≤ m ≤ b³ − 1, G never falls, and G(b³ − 1) = r·(b² − 1).** For d > r, κ(h) − 1 = κ(x) ≥ 0. Each of the r blocks adds b² − (r + 1), and r² + r(b² − r − 1) = r(b² − 1).

**Step 5. For m ≥ b³, G(m) ≥ 4r³ + 2r² − 3r − 1 ≥ 2.** Let J ≥ 3 with b^J ≤ m < b^(J+1), and write m = d·b^J + y with y < b^J. By Lemma 3, κ(d'·b^J + x) ≥ κ(x) for every top digit d'. So every complete block of length b^J adds at least G(b^J − 1) − 1, and the last, partial block adds at least G(y) − 1. Hence

```text
G(m) ≥ G(b^J − 1) + (d − 1)·(G(b^J − 1) − 1) + G(y) − 1.
```

Use induction on J with the hypothesis G(b^J − 1) ≥ r(b² − 1) and G(y) ≥ μ for 1 ≤ y < b^J. For J = 3 this is Steps 1 to 4. The inequality then gives G(m) ≥ r(b² − 1) + μ − 1 = 4r³ + 2r² − 3r − 1 > μ, which is 2 for r = 1 and grows with r. It also gives G(b^(J+1) − 1) ≥ b·G(b^J − 1) − (b − 1) ≥ r(b² − 1). So the hypothesis holds for J + 1. ∎

**Step 6 (existence and location). D_b has a zero, and it is n(b) from (5.1).** In the upper half of the block d = r, write the two-digit part as x = (r + 1 + k)·b + y with 0 ≤ k ≤ r − 1 and 0 ≤ y ≤ 2r. By Lemma 3 with J = 2, G(r·b² + x) = B_r − 1 + G(x) + (x − (b² − 1)/2). By Step 0, G((r + 1)·b − 1) = −r² − r and each two-digit block with d > r adds r, so G(x) = −r² − r + k·r + max(0, y − r). Hence

```text
G(r·b² + x) = −2r² − r + 1 + k·(3r + 1) + φ(y),    φ(y) = y + max(0, y − r).
```

For x = r·b + y with y > r the same computation gives G ≤ −2r² − r < 0. So G changes sign at the k and y with k·(3r + 1) + φ(y) = 2r² + r − 1. Inside a block φ rises by 1 for y ≤ r and by 2 for y > r, and from one block to the next G rises by 1. With r = 3s + t and t ∈ {0, 1, 2}:

| r | k | y | zero of D_b |
|---|---|---|---|
| 3s (b ≡ 1 mod 6) | 2s | s − 1 | G(m₀) = 0, n = 2m₀ |
| 3s + 1 (b ≡ 3 mod 6) | 2s | 5s + 1 | G(m₁) = −1, G(m₁ + 1) = 1, n = 2m₁ + 1 |
| 3s + 2, s even (b ≡ 5 mod 12) | 2s + 1 | (7s + 4)/2 | G(m₀) = 0, n = 2m₀ |
| 3s + 2, s odd (b ≡ 11 mod 12) | 2s + 1 | (7s + 3)/2 | G(m₁) = −1, G(m₁ + 1) = 1, n = 2m₁ + 1 |

Here m = r·b² + (r + 1 + k)·b + y. In every row n equals (5.1). For example, for b = 6s + 1, 2m₀ = 6s·b² + (10s + 2)·b + 2s − 2 = b³ + (2b² + 2b − 7)/3. In the second and fourth rows φ passes the needed value with a step of 2, so G goes from −1 to 1, and D_b(2m₁ + 1) = G(m₁) + G(m₁ + 1) = 0 by Lemma 2. So for odd b the zero exists and lies at n(b), without the computer step. I also checked every value of this step numerically for each odd b from 3 to 401 (`tests/check_odd_existence.py`).

**Example.** Three bases show both kinds of zero.

| b | r, s, t | k, y | m | G near m (counted) | zero of D_b |
|---|---|---|---|---|---|
| 7 | 3, 1, 0 | 2, 0 | m₀ = 3·49 + 6·7 + 0 = 189 | G(188) = −1, G(189) = 0, G(190) = 1 | n = 2·189 = 378 = n(7) |
| 3 | 1, 0, 1 | 0, 1 | m₁ = 1·9 + 2·3 + 1 = 16 | G(16) = −1, G(17) = 1 | n = 2·16 + 1 = 33 = n(3) |
| 11 | 5, 1, 2 | 3, 5 | m₁ = 5·121 + 9·11 + 5 = 709 | G(709) = −1, G(710) = 1 | n = 2·709 + 1 = 1419 = n(11) |

For b = 7 the formula gives G(189) = −2·9 − 3 + 1 + 2·10 + φ(0) = 0. G reaches zero exactly, and the arrow lands on an even row. For b = 3 and b = 11, G steps over zero from −1 to 1, and the arrow lands on the odd row between the two values, where D_b = G(m₁) + G(m₁ + 1) = 0.

**Conclusion.** G is negative for 1 ≤ m ≤ (b³ − 1)/2. It rises strictly from there to the positive value r² at (r + 1)·b² − 1, and it is positive from then on. A strictly rising sequence takes the value zero at most once, and it changes sign only once. If G(m₀) = 0, then n = 2m₀ is a zero of D_b, while D_b(2m₀ − 1) = G(m₀ − 1) < 0 and D_b(2m₀ + 1) = G(m₀ + 1) > 0. If G changes sign without vanishing, G(m₁) < 0 < G(m₁ + 1), then only n = 2m₁ + 1 can be a zero. At every other n both terms in Lemma 2 have the same sign. So D_b has at most one zero, it is negative before it and positive after it, and by Step 6 the zero exists and is n(b). This proves Theorems 1 and 2 for odd b without the computer step.

For Theorem 3, D_b(2m) = 2G(m) and D_b(2m + 1) = G(m) + G(m + 1) are both at least 2μ. Equality holds at 2m = b³ − 1, which is even for odd b. So the minimum of D_b is 2μ = −(4r² + 6r) = −(b − 1)(b + 2). ∎

### 5.5 Proof of Theorem 2 for b = 2

Let s(j) be the number of ones in the binary form of j. Then carries_2(j, j) = s(j) and carries_2(y, y + 1) = s(y + 1) − 1, by (3.2). Let H(m) = Σ_{j=1..m} (2s(j) − 3). Then

```text
E_2(2m) − 2m              = H(m)
E_2(2m + 1) − (2m + 1)    = H(m) + s(m + 1) − 2
```

The first values are H(1), ..., H(7) = −1, −2, −1, −2, −1, 0, 3. So n = 12 is a zero, and the odd values D_2(1), D_2(3), ..., D_2(11) are −1, −2, −2, −2, −2, −1. For J ≥ 3 and j = 2^J + x with 0 ≤ x < 2^J, 2s(j) − 3 = 2s(x) − 1. This is −1 for x = 0 and at least 1 for x ≥ 1. Over a full block H rises by 2^J(J − 1). So H(2^J − 1) ≥ H(7) = 3, and inside the block H stays at least H(2^J − 1) − 1 ≥ 2. Hence H(m) ≥ 2 for m ≥ 7, and D_2(2m + 1) ≥ 1 for m ≥ 6. The only zero is n = 12. ∎

### 5.6 Related work

The following are known and are used here. The exponent of a prime in a binomial coefficient equals a carry count (Kummer, 1852 [1]). The exponent of a prime in m! is f(m) (Legendre [2]). The identities (3.1) and (3.2) are standard.

In standard notation, c(2h − 1) = C(2h, h)/2, so c(1)···c(2m) = A(m)²/2^m with A(m) = C(2,1)·C(4,2)···C(2m,m) (OEIS A007685 [3]). For an odd prime p this gives E_p(2m) = 2·v_p(A(m)), and an even solution n = 2m means v_p(A(m)) = m. Examples are p = 5 with m = 72, p = 7 with m = 189 and p = 13 with m = 1158.

For p = 2, (3.2) together with s_2(2j) = s_2(j) and s_2(2j + 1) = s_2(j) + 1 gives κ_2(k) = s_2(k + 1) − 1, the exponent of 2 in C(k, ⌊k/2⌋) (OEIS A048881 [3]). Summing over k = 1, …, n and using s_2(1) = 1 gives E_2(n) = A000788(n + 1) − (n + 1) = A078903(n + 1) for every n ≥ 1, where A000788(N) = s_2(0) + … + s_2(N) [3]. The same entries give a close relative of the base-2 case. The formula A000788(4^k − 2) = k(4^k − 2) gives E_2(n) = m(n + 1) at n = 4^(m+1) − 3, and A078904 gives the largest difference before that point. For m = 1 this is E_2(13) = 14, one row after n(2) = 12.

Since E_b(n) is a combination of cumulative digit sums by (3.2), Delange's formula [11] (for b = 2 already Trollope [12]) gives E_b(n) = (n/2)·log_b n + O(n) for fixed b. Near n = b³ the O(n) term oscillates and is of the same size as the main term, so this estimate does not locate the crossing. The formula (5.1) does.

On 22 November 2026 I searched the OEIS (by terms and by words), arXiv (titles and abstracts), zbMATH Open, Crossref and a general web search engine, and I consulted the works cited here. I did not find the equation E_b(n) = n, the formula (5.1), Theorems 1 to 4, the rule of the farthest prime-power factor in Section 5.7, the depth −(b − 1)(b + 2) or the sequences 12, 33, 82, 144, 256, … and 12, 33, 144, 378, 1419, … in these sources. They may well appear in work I have not seen. If such work is pointed out to me, I will add it in the next version.

The nearest work I found treats the product of all binomial coefficients in one row (OEIS A001142 [3]). Lagarias and Mehta [4] write the prime exponents of that product with cumulative digit sums and define the same digit-sum expression for every base b ≥ 2; they also note that for a composite b this expression is not always the exponent of b. Du and Lagarias [13] study the partial factorizations of the same product. Straub, Moll and Amdeberhan [5] treat single central and k-central binomial coefficients. Hirschhorn [14] and Kellner [15] study the size of such products, not their prime exponents. Work on carries as a random process (Holte [16]; Diaconis and Fulman [17]) asks a different question.

### 5.7 Composite m

For a composite m the natural question uses the exponent of m, not a carry count. Write m = q₁^a₁ ··· q_k^a_k with primes q₁ < ... < q_k. The exponent of m in c(1)···c(n), that is the largest e with m^e dividing the product, is

```text
K_m(n) = min_i ⌊ E_{q_i}(n) / a_i ⌋.
```

For a prime m, K_m = E_m. For a composite m, K_m and E_m are different functions (Section 6.3).

**Theorem 4 (square-free m)** (HOLDS, proof). Let m be square-free with largest prime factor q_k. Then K_m(n) = n has exactly one solution, n = n(q_k).

*Proof.* By Theorem 2, for every prime q, E_q(n) − n is negative before n(q) and positive after it. The points n(q) increase with q, because b³ < n(b) < (b + 1)³ for every b ≥ 2 by (5.1). If n < n(q_k), then E_{q_k}(n) < n, so K_m(n) < n. If n > n(q_k), then n > n(q_i) for every i and every E_{q_i}(n) > n, so K_m(n) > n. At n = n(q_k), E_{q_k}(n) = n and the other terms exceed n. ∎

For general m only measurements are available. Each prime-power factor q^a has its own solution set. Its first solution lies near q^(2a+1), or near 2^(2a+2) when q = 2 (Figure 5). In the measured range 2 ≤ m ≤ 1000 there are 806 numbers with two or more distinct prime factors. For 803 of them the solution set of m equals the solution set of the prime-power factor whose first solution lies farthest out. The exceptions are 72 = 2³·3², 360 = 2³·3²·5 and 544 = 2⁵·17. In all three, the solution set of m is the set of the farthest factor plus some later solutions of another factor. No solution of the farthest factor is missing. For 72 and 360 the farthest factor is 9, with first solution 321, and the factor 8 adds 323 and 324. For 544 the farthest factor 17 has the single solution 5118 = n(17), and the factor 32 adds 5120, 5121 and further solutions, 13 in total (Section 7).

Among the 25 prime powers q^a ≤ 1000 with a ≥ 2, exactly eight have a single solution. They are the prime squares q² with 7 ≤ q ≤ 31, from 49 (solution 18 710) to 961 (solution 29 266 018). The square 25 = 5² has two solutions, 3668 and 3669. For each m every n up to 3q^(2a+1) + 1000 was counted, where q^a is the prime-power factor with the farthest first solution (3·2^(2a+2) + 1000 when q = 2). For a prime square q² the bound is 3q⁵ + 1000. A single solution means a single solution in this range.

## 6. Numerical examples

### 6.1 Small example: base 7

Figure 1 shows D_7(n) for every n from 1 to 720. The difference falls slowly with small oscillations, reaches −54 at n = 342 = 7³ − 1, and then rises steeply. From n = 343 on, rows with three carries and rows with two carries come in alternating blocks: 343 to 348 three, 349 to 356 two, 357 to 362 three, 363 to 370 two, 371 to 376 three, 377 to 384 two. A row with three carries raises D_7 by two, a row with two carries by one. Around the crossing:

```text
n        372   373   374   375   376   377   378   379   380   381
D_7(n)   −10    −8    −6    −4    −2    −1     0     1     2     3
```

The crossing is n(7) = 7³ + (2·49 + 14 − 7)/3 = 343 + 35 = 378, as given by (5.1). The depth is −(7 − 1)(7 + 2) = −54, as given by Theorem 3.

![Figure 1. D_7(n) = E_7(n) − n for every n from 1 to 720. The minimum is at n = 342 = 7³ − 1 with value −54. The single zero is at n(7) = 378.](../figures/fig1_bow_base7.png)

### 6.2 Boundary cases

The values just before and after the crossing are ±1 or ±2. Counted for 2 ≤ b ≤ 16:

```text
b               2    3    4    5    6    7    8    9
D_b(n(b) − 1)  −1   −2   −1   −1   −1   −1   −1   −2
D_b(n(b) + 1)   1    2    1    2    1    1    1    2

b              10   11   12   13   14   15   16
D_b(n(b) − 1)  −1   −2   −1   −1   −1   −2   −1
D_b(n(b) + 1)   1    2    1    1    1    2    1
```

Since D_b(n) − D_b(n − 1) = κ_b(n) − 1, a step of 2 next to n(b) means a row with three carries there. This happens for odd and for even n(b), for example b = 5 with n(5) = 144.

The smallest bases are boundary cases of the formulas. The class formula (5.1) covers b = 2 and b = 3: 8 + 4 + 2 − 2 = 12 and 27 + (18 + 6 − 6)/3 = 33. The prime form (5.2) needs p ≥ 5 (Section 6.3).

### 6.3 Invalid and failing cases

1. **The prime form at p = 3.** With ε = 0, (5.2) gives 27 + 28/6, which is not an integer. The form (5.2) is valid only for p ≥ 5. The class formula gives n(3) = 33.
2. **Lemma 1 in an even base.** In base 4 with h = 1, carries_4(1, 2) = 0 but carries_4(2, 2) = 1. For h < 4000 the equality fails 1334 times in base 4, 801 times in base 6 and 444 times in base 10. This is why the proof of Section 5.4 does not apply to even bases ≥ 4.
3. **The exponent of a composite is not unique.** For m = 4, K_4(n) = n has 12 solutions, starting with 60, 65, 66, 67 and 68. Uniqueness does not carry over from primes to prime powers.
4. **Carry count and exponent differ for a composite base.** For b = 6, E_6(256) = 256, so n(6) = 256 as (5.1) says. But the exponent of 6 in c(1)···c(256) is K_6(256) = min(770, 424) = 424. The only solution of K_6(n) = n is n = 33 = n(3), as Theorem 4 says.

### 6.4 Large examples

**A 39-digit prime.** Take p = 2¹²⁷ − 1. Then p ≡ 1 (mod 3), and n(p) has 115 decimal digits. It begins with 49252507745493099015 and ends with 71468138216236078418. The dots below stand for the 75 digits that are not shown.

```text
n(p) = 49252507745493099015 ... 71468138216236078418          (115 digits)
```

The closed form gives E_p(n(p)) = n(p), D_p(n(p) − 1) = −1, D_p(n(p) + 1) = 1 and D_p(p³ − 1) = −(p − 1)(p + 2), all in exact integer arithmetic.

**The largest known Mersenne prime.** Take p = 2^136279841 − 1, which has 41 024 320 digits. The digit count is ⌊136279841·log₁₀2⌋ + 1, because a power of two is never a power of ten. Then n(p) has 123 072 960 digits. This follows from 3·136279841·log₁₀2 = 123 072 959.836 and from n(p) = 2^(3e)·(1 + O(2^(−e))). The relative correction is far too small to change the digit count. The leading digits 685415845289511071 come from the same logarithm with 60-digit precision. They are not read from a stored value. n(p) itself was never printed. It was computed as an exact GMP integer, and E_p was evaluated at n(p), at n(p) ± 1, at p³ − 1 and at four random points with the closed form. All checks passed in 445.6 s (Section 7).

### 6.5 Where the arrows land

The formula (5.1) fixes the landing point of every base. The status of each item is given in its heading.

1. **Beyond the cube (HOLDS, proof).** (n(b) − b³)/b² tends to 2/3 for odd b and to 1 for even b (Figure 3). For b = 10 001 the value is 0.66675, and for b = 10 002 it is 1.00010.
2. **Distance between the arrows of consecutive primes (HOLDS, proof; the ratio range is MEASURED).** For primes 5 ≤ p < q, write (5.2) as n(p) = p³ + (2/3)p² + α_p·p + β_p with α_p = (3 + ε)/6 and β_p = (3ε − 17)/6. Then

   ```text
   n(q) − n(p) = (q³ − p³) + (2/3)(q² − p²) + (α_q·q − α_p·p) + (β_q − β_p).
   ```

   So the distance is close to 3p²·(q − p). Figure 4 shows that (n(q) − n(p))/3p² follows the prime gap q − p. This is a consequence of n(p) ≈ p³ and carries no information beyond the gap itself. For the 2259 pairs of consecutive primes below 20 000, the ratio of n(q) − n(p) to q³ − p³ + (2/3)(q² − p²) lies between 0.99889 and 1.00483.
3. **Parity (HOLDS, proof).** n(b) is odd exactly for b ≡ 3, 9, 11 (mod 12). Among primes p ≥ 5 these are the primes p ≡ 11 (mod 12).
4. **Distance from the minimum to the arrow (HOLDS, proof for odd b; MEASURED for even b).** For odd b it is n(b) − (b³ − 1) = (2/3)b² + O(b). For example it is 36 for b = 7, 660 for b = 31 and 6884 for b = 101. For even b, if the minimum is first reached at b³ − b² − 1 as measured, the distance is exactly 2b² + b − 1.
5. **One shape for each parity (MEASURED).** Scale D_b by b² and shift n by b³ in units of b². Then the curves of large odd bases come close to one broken line and those of large even bases to another (Figure 2). For finite b the curves are close to them but not equal: the actual zeros are at x = 0.6747 for b = 101, 0.6689 for b = 301, 1.0098 for b = 100 and 1.0033 for b = 300. Odd bases have the minimum −1 at x = (n − b³)/b² = 0, rise with slope 3/2 and reach 1/2 at x = 1, cross zero at x = 2/3 and then rise with slope 1/2. Even bases have the minimum −1 at x = −1, rise with slope 1/2 to cross zero at x = 1 and then rise with slope 3/2. For b = 1001 the scaled values at x = 0, 2/3, 1 and 2 are −1.001, −0.001, 0.499 and 0.998. For b = 1000 the values at x = −1, 1 and 2 are −1.000, −0.001 and 1.4985.
6. **Third differences across bases (MEASURED).** The sequence n(b) over consecutive b is not a single polynomial. Its third differences n(b + 3) − 3n(b + 2) + 3n(b + 1) − n(b) alternate in sign and grow (−15, 37, −40, 72, ... for b = 2, 3, 4, 5, ...). The regularity is inside each class, where n(b) is a polynomial.

![Figure 2. Scaled difference (E_b(n) − n)/b² against (n − b³)/b² for odd b = 101 (blue line) and 301 (blue band) and even b = 100 (orange dashed) and 300 (orange band). The curves of each parity nearly coincide. Their zeros approach 2/3 for odd bases and 1 for even bases as b grows.](../figures/fig2_scaled_shape.png)

![Figure 3. Distance of the arrow beyond the cube, (n(b) − b³)/b², for 5 ≤ b ≤ 400, by class, on a logarithmic b axis. Dotted lines at 2/3 and 1.](../figures/fig3_offset_by_class.png)

![Figure 4. Left: the prime gap q − p against (n(q) − n(p))/3p² for the first 400 pairs of consecutive primes from 5. Right: ratio of n(q) − n(p) to q³ − p³ + (2/3)(q² − p²) for all consecutive primes below 20 000.](../figures/fig4_prime_arrows.png)

![Figure 5. First solution of K_{q^a}(n) = n for prime powers, as log_q. The lines are 2a + 1 and 2a + 2. Every n was counted up to the first solution. Points of q ≥ 3 are shifted slightly sideways so that they do not overlap.](../figures/fig5_prime_powers.png)

## 7. Implementation and verification

All programs are in this package. Python programs need Python 3.8 or later and no third-party packages, except `tests/check_mersenne.py` (gmpy2) and `tests/make_figures.py` (numpy and matplotlib). The C programs need a C compiler with OpenMP. The graphics card program needs Vulkan 1.2 with 64-bit shader integers and the `glslc` compiler. All commands run from the package root. The raw outputs are in `tests/RESULTS.md`.

| Program and command | Method | Scope | Result |
|---|---|---|---|
| `python3 tests/check_small.py 41` | direct count, closed form compared | 2 ≤ b ≤ 40, every n ≤ 3b³ + 300 | 39 bases, 0 failures, PASS |
| `python3 tests/check_certificates.py` | polynomial certificates | 12 classes of b mod 12 | 12 of 12 classes PASS |
| `python3 tests/check_proof_steps.py 151` | every lemma and step of Section 5.4 | odd 3 ≤ b ≤ 149, prime and composite | 74 odd bases, 0 failures, PASS |
| `python3 tests/check_odd_existence.py 401` | Step 6 of Section 5.4: existence and location | odd 3 ≤ b ≤ 401 | 200 odd bases, 0 failures, PASS |
| `./bow_draw_scan 600` (from `tests/c/bow_draw_scan.c`) | direct count, all bases | 2 ≤ b < 600, every n ≤ 3b³ + 300 | 598 of 598 PASS, 9.69 × 10¹⁰ rows, 127 s |
| `./bow_draw_scan 1000 primes` | direct count, primes | p < 1000 | 168 of 168 PASS, 1.10 × 10¹¹ rows, 144 s |
| `./tests/gpu/bow_draw_gpu 2000` | block scan on a graphics card | 2 ≤ b < 2000, every n ≤ 3b³ + 300 | 1998 of 1998 PASS, 1.20 × 10¹³ rows, 1603 s (747 s on the card) |
| `python3 tests/check_primes.py 10000000000 12000` | closed form | all primes 5 ≤ p < 10¹⁰, and 12 000 random primes with 20 to 200 digits | 455 052 509 primes and 12 000 random primes, 0 failures, PASS, 449 s |
| `python3 tests/check_mersenne.py 136279841 132049 2` | closed form with GMP | 51 Mersenne primes 2^e − 1, 3 ≤ e ≤ 136 279 841 | 51 of 51 PASS, the 29 exponents 3 ≤ e ≤ 132 049 confirmed by Lucas-Lehmer (the program's count of 30 includes e = 2), 2646 s, 1.04 GB |
| `python3 tests/check_composite.py` | direct count of K_m | 2 ≤ m ≤ 40 | primes and square-free m PASS, farthest-factor rule 7 of 7 |
| `./bow_draw_composite 1000` (from `tests/c/bow_draw_composite.c`) | direct count of K_m | 2 ≤ m ≤ 1000 | primes 168 of 168 and square-free 439 of 439 PASS, farthest-factor rule 803 of 806, 262 s |

Each check compares two independent computations wherever possible. The direct count is compared with the closed form. The processor count is compared with the graphics card count. The certificate polynomials are compared with 300 numerical values per class. In the Mersenne check, the exponents e ≤ 132 049 are confirmed prime with the Lucas-Lehmer test [6] inside the program. The larger exponents are taken from the list of known Mersenne primes [7].

The direct counts do not depend on any formula. The closed-form checks evaluate E_p only at the points n(p) and n(p) ± 1, at p³ − 1 and at random points. For large primes, the guarantee that there is no other zero comes from Theorem 2, not from the counts.

## 8. Limits and open questions

1. **Even bases.** For even b ≥ 4 the uniqueness of the solution and the position of the minimum are measured, not proved. Lemma 1 fails in even bases, so the odd-base proof does not transfer. A proof for even bases is open.
2. **Computer-assisted step.** For even b ≥ 4, Theorem 1 rests on polynomial certificates checked by `tests/check_certificates.py` in exact rational arithmetic. The program is short and runs in under a second, but a reader must trust or re-implement it. For odd b and b = 2 the written proofs in Sections 5.4 and 5.5 do not need it.
3. **Independent reading.** The written proofs in Sections 5.4 and 5.5 have not yet been checked by an independent reader. Every landmark value and monotonicity claim in them was checked numerically for the odd bases listed in Section 7.
4. **Not a primality test.** Theorem 1 holds for every base, so E_b(n(b)) = n(b) cannot separate primes from composites. Kummer's interpretation as an exponent holds only for prime bases.
5. **Not a factoring method.** Theorem 4 and the measurements for composite m use the factorization of m. No speed claim is made.
6. **Composite m.** The rule of the farthest prime-power factor is an observation with three exceptions in the measured range, 72, 360 and 544. A statement that covers the exceptions, and the constant in the landing point of prime powers near q^(2a+1), are open.
7. **Program limits.** The C and graphics card programs use 64-bit integers, so they require n < 2⁶³ and E_b(n) < 2⁶³. The first condition alone is not enough: for b = 1 400 000 the end of the scan, 3b³ + 300, is below 2⁶³ but E_b there is not. For b < 2000 both stay below 4·10¹⁰. The direct count costs about 3b³ log_b(3b³) digit operations per base. The closed form has no fixed limit, but its cost grows with the size of p³.
8. **Literature.** Section 5.6 lists the databases searched, the date of the search and what was found. A result missing from those sources may still be known.
9. **Programs.** The programs and their raw output (tests/RESULTS.md) are in the package that accompanies this paper. The run times and the graphics card results are recorded there.

## 9. Conclusion

For every base b ≥ 2, the carries of the central binomial coefficients, summed over rows 1 to n, catch up with the number of rows at the point n(b) given by (5.1), just beyond b³. For odd bases and for base 2 this is the only point where they are equal, the difference changes sign only there, and all of this is proved by hand. For even bases b ≥ 4 uniqueness is measured, not proved. For a prime p, E_p(n) is the exponent of p in the product of the central binomial coefficients. For a square-free m, Theorem 4 places the only solution of K_m(n) = n at the point of the largest prime factor. The landing points follow simple rules. They depend on b modulo 6 and lie about (2/3)b² or b² beyond the cube. The arrows of consecutive primes p < q are about 3p²(q − p) apart.

## Appendix A. All Mersenne primes checked

The table lists every Mersenne prime p = 2^e − 1 checked by `python3 tests/check_mersenne.py 136279841 132049 2` (Section 7). These are the 51 known Mersenne primes with 3 ≤ e ≤ 136 279 841. The smallest of the 52 known Mersenne primes, 3 = 2² − 1, lies outside the prime form (5.2), which needs p ≥ 5. Its point n(3) = 33 is confirmed by the direct count (Section 7).

For every p the program checks, in exact integer arithmetic with GMP: E_p(n(p)) = n(p), the signs at n(p) − 1 and n(p) + 1, the minimum E_p(p³ − 1) − (p³ − 1) = −(p − 1)(p + 2), two random points on each side of n(p), and the product of p with the previous Mersenne prime (Theorem 4). The program itself confirms with the Lucas-Lehmer test that 2^e − 1 is prime for the 30 exponents e ≤ 132 049 (this count includes e = 2). The larger exponents are taken from the list of known Mersenne primes [7]. The whole run took 2646 s with a peak memory of 1.04 GB. The raw output is in Section 7 of `tests/RESULTS.md`, and the same table in machine-readable form is `tests/mersenne.csv`.

| exponent e | digits of 2^e − 1 | result | time (s) |
|---|---|---|---|
| 3 | 1 | PASS | 0.0 |
| 5 | 2 | PASS | 0.0 |
| 7 | 3 | PASS | 0.0 |
| 13 | 4 | PASS | 0.0 |
| 17 | 6 | PASS | 0.0 |
| 19 | 6 | PASS | 0.0 |
| 31 | 10 | PASS | 0.0 |
| 61 | 19 | PASS | 0.0 |
| 89 | 27 | PASS | 0.0 |
| 107 | 33 | PASS | 0.0 |
| 127 | 39 | PASS | 0.0 |
| 521 | 157 | PASS | 0.0 |
| 607 | 183 | PASS | 0.0 |
| 1 279 | 386 | PASS | 0.0 |
| 2 203 | 664 | PASS | 0.0 |
| 2 281 | 687 | PASS | 0.0 |
| 3 217 | 969 | PASS | 0.0 |
| 4 253 | 1 281 | PASS | 0.0 |
| 4 423 | 1 332 | PASS | 0.0 |
| 9 689 | 2 917 | PASS | 0.0 |
| 9 941 | 2 993 | PASS | 0.0 |
| 11 213 | 3 376 | PASS | 0.0 |
| 19 937 | 6 002 | PASS | 0.0 |
| 21 701 | 6 533 | PASS | 0.0 |
| 23 209 | 6 987 | PASS | 0.0 |
| 44 497 | 13 395 | PASS | 0.0 |
| 86 243 | 25 962 | PASS | 0.1 |
| 110 503 | 33 265 | PASS | 0.1 |
| 132 049 | 39 751 | PASS | 0.2 |
| 216 091 | 65 050 | PASS | 0.3 |
| 756 839 | 227 832 | PASS | 1.6 |
| 859 433 | 258 716 | PASS | 1.3 |
| 1 257 787 | 378 632 | PASS | 2.1 |
| 1 398 269 | 420 921 | PASS | 2.3 |
| 2 976 221 | 895 932 | PASS | 5.9 |
| 3 021 377 | 909 526 | PASS | 4.7 |
| 6 972 593 | 2 098 960 | PASS | 17.0 |
| 13 466 917 | 4 053 946 | PASS | 36.5 |
| 20 996 011 | 6 320 430 | PASS | 53.9 |
| 24 036 583 | 7 235 733 | PASS | 78.1 |
| 25 964 951 | 7 816 230 | PASS | 111.5 |
| 30 402 457 | 9 152 052 | PASS | 133.1 |
| 32 582 657 | 9 808 358 | PASS | 154.4 |
| 37 156 667 | 11 185 272 | PASS | 132.9 |
| 42 643 801 | 12 837 064 | PASS | 172.6 |
| 43 112 609 | 12 978 189 | PASS | 207.7 |
| 57 885 161 | 17 425 170 | PASS | 364.2 |
| 74 207 281 | 22 338 618 | PASS | 226.9 |
| 77 232 917 | 23 249 425 | PASS | 214.3 |
| 82 589 933 | 24 862 048 | PASS | 237.6 |
| 136 279 841 | 41 024 320 | PASS | 445.6 |

## References

1. E. E. Kummer, "Über die Ergänzungssätze zu den allgemeinen Reciprocitätsgesetzen", Journal für die reine und angewandte Mathematik 44 (1852), 93–146, doi:10.1515/crll.1852.44.93.
2. A.-M. Legendre, Essai sur la théorie des nombres, second edition, Courcier, Paris, 1808.
3. OEIS Foundation, The On-Line Encyclopedia of Integer Sequences, sequences A000788, A001142, A001405, A007685, A048881, A078903 and A078904, https://oeis.org, accessed 22 November 2026.
4. J. C. Lagarias and H. Mehta, "Products of binomial coefficients and unreduced Farey fractions", International Journal of Number Theory 12 (2016), no. 1, 57–91, doi:10.1142/S1793042116500044, arXiv:1409.4145.
5. A. Straub, V. H. Moll and T. Amdeberhan, "The p-adic valuation of k-central binomial coefficients", Acta Arithmetica 140 (2009), no. 1, 31–42, doi:10.4064/aa140-1-2, arXiv:0811.2028.
6. D. H. Lehmer, "An extended theory of Lucas' functions", Annals of Mathematics (2) 31 (1930), no. 3, 419–448, doi:10.2307/1968235.
7. Great Internet Mersenne Prime Search, List of known Mersenne prime numbers, https://www.mersenne.org/primes/, accessed 22 November 2026.
8. J. Augustus, "Pascal Mersenne Rows: powers of two as carry-free Pascal rows in Mersenne bases", 2026, https://github.com/JamesAugustus/pascal-mersenne-rows.
9. J. Augustus, "FactorX: the universe language of numbers and its main example, Bow Draw", version 1.0, 2026, companion document in the same archive, doi:10.5281/zenodo.24451375.
10. A. Granville, "Arithmetic properties of binomial coefficients I: Binomial coefficients modulo prime powers", in: J. Borwein et al. (eds.), Organic Mathematics (Burnaby, BC, 1995), CMS Conference Proceedings 20, American Mathematical Society, Providence, RI, 1997, 253–276, https://dms.umontreal.ca/~andrew/Binomial/.
11. H. Delange, "Sur la fonction sommatoire de la fonction « somme des chiffres »", L'Enseignement Mathématique (2) 21 (1975), 31–47, doi:10.5169/seals-47328.
12. J. R. Trollope, "An explicit expression for binary digital sums", Mathematics Magazine 41 (1968), no. 1, 21–25, doi:10.1080/0025570X.1968.11975826.
13. L. Du and J. C. Lagarias, "Partial factorizations of products of binomial coefficients", International Journal of Number Theory 18 (2022), no. 3, 691–728, doi:10.1142/S1793042122500373, arXiv:2006.15439.
14. M. D. Hirschhorn, "The asymptotic behavior of ∏_{k=0}^{n} C(n, k)", The Fibonacci Quarterly 51 (2013), no. 2, 163–173, doi:10.1080/00150517.2013.12427960.
15. B. C. Kellner, "Asymptotic products of binomial and multinomial coefficients revisited", Integers 24 (2024), Paper A59, doi:10.5281/zenodo.12167556, arXiv:2312.11369.
16. J. M. Holte, "Carries, combinatorics, and an amazing matrix", The American Mathematical Monthly 104 (1997), no. 2, 138–149, doi:10.1080/00029890.1997.11990612.
17. P. Diaconis and J. Fulman, "Carries, shuffling, and an amazing matrix", The American Mathematical Monthly 116 (2009), no. 9, 788–803, doi:10.4169/000298909X474864, arXiv:0806.3583.

The source code in this package is licensed under MIT. The text, figures and tables are licensed under CC BY 4.0. Copyright © 2026 James Augustus.
