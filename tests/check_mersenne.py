#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bow Draw on Mersenne primes p = 2^e - 1 (requires gmpy2).

Exponents up to LLMAX are confirmed prime here with the Lucas-Lehmer test; larger exponents are
taken from the list of known Mersenne primes. For each p: E(n(p)) = n(p), the neighbours n(p) - 1 and
n(p) + 1, the minimum E(p^3 - 1) - (p^3 - 1) = -(p - 1)(p + 2), K random points on each side, and the
product m = p q with the previous Mersenne prime q (exponent of m: solution n(p)).
Usage: python3 tests/check_mersenne.py [EMAX] [LLMAX] [K]     (default 4423 4423 5)
Full run reported in tests/RESULTS.md: EMAX = 136279841, LLMAX = 132049, K = 2 (about 35 minutes, 1 GB).
"""
import sys, time, random
from decimal import Decimal, getcontext
import gmpy2
from gmpy2 import mpz

EXPONENTS = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689,
             9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787,
             1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657,
             37156667, 42643801, 43112609, 57885161, 74207281, 77232917, 82589933, 136279841]

def f(m, p):
    s, q = mpz(0), p
    while q <= m: s += m // q; q *= p
    return s
def g(n, q):
    a, r = gmpy2.f_divmod(n, q); return q * a * (a - 1) // 2 + a * (r + 1)
def S(n, p):
    s, q = mpz(0), p
    while q <= n: s += g(n, q); q *= p
    return s
def E(n, p):
    n = mpz(n); m = n // 2
    T = 4 * S(m, p) - f(m, p) if m > 0 else mpz(0)
    if n % 2: T += f(m, p) + f(m + 1, p)
    return S(n, p) - T
def n_draw(p):
    e = p % 3; return p**3 + (4 * p * p + (3 + e) * p + 3 * e - 17) // 6
def digits(e):
    """Decimal digits of 2^e - 1: floor(e log10 2) + 1, since 2^e is never a power of ten."""
    getcontext().prec = 40
    return int(e * Decimal(2).log10()) + 1

def lucas_lehmer(e):
    if e == 2: return True
    M = (mpz(1) << e) - 1; s = mpz(4)
    for _ in range(e - 2):
        s = s * s - 2; s = (s & M) + (s >> e)
        if s >= M: s -= M
    return s == 0

EMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4423
LLMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 4423
K = int(sys.argv[3]) if len(sys.argv) > 3 else 5
rng = random.Random(2026)
t = time.time(); tested = [e for e in EXPONENTS if e <= LLMAX]
print(f"Lucas-Lehmer: {len(tested)} exponents e <= {LLMAX} confirmed: {all(lucas_lehmer(e) for e in tested)}  [{time.time() - t:.1f} s]")
prev, fails, count = None, 0, 0
for e in EXPONENTS:
    if e > EMAX: break
    if e < 3: continue                     # p = 3: n(3) = 33, outside the p >= 5 formula
    t = time.time(); p = (mpz(1) << e) - 1; n = n_draw(p)
    ok = E(n, p) == n and E(n - 1, p) < n - 1 and E(n + 1, p) > n + 1
    ok &= E(p**3 - 1, p) - (p**3 - 1) == -(p - 1) * (p + 2)
    for _ in range(K):
        x = mpz(rng.randrange(1, int(n) - 1)); ok &= E(x, p) < x
        x = mpz(rng.randrange(int(n) + 2, int(50 * p**3))); ok &= E(x, p) > x
    if prev is not None:
        q = prev; ok &= min(E(n, p), E(n, q)) == n and min(E(n - 1, p), E(n - 1, q)) < n - 1
    count += 1; fails += not ok
    print(f"e = {e:>9}  p has {digits(e):>9} digits  {'PASS' if ok else 'FAIL'}  [{time.time() - t:.1f} s]", flush=True)
    prev = p
print(f"{count} Mersenne primes, {fails} failures")
