#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Checks for Section 3 of FactorX, the universe language (no external libraries).

Notation: a digit may be wide, so [x][y]_b means the value x*b + y for any x, y >= 0.
The first pair of the universe b is [1][1]_b = b + 1. A copy is [a][a]_b = a*(b + 1), a >= 2.

  1. Theorem 1: every n >= 2 is [a][a]_b in exactly tau(n) - 1 universes b >= 1,
     and n appears in exactly one universe if and only if n is prime.
  2. With ordinary digits (a < b) the composites that are no copy are exactly 6 and the prime squares.
  3. Theorem 2: when two numbers are added in a base b >= 2, every carry is 0 or 1.
  4. Theorem 3: row d - 1 of Pascal's triangle follows 1, -1, 1, ... modulo d up to column r - 1
     and breaks exactly at column r, the smallest prime factor of a composite d. For a prime d it never breaks.
  5. Large examples: 2^61 - 1, 2^67 - 1 = 193707721 * 761838257287, d = 1009 * 1013.
  6. Bow Draw in three universes: E_b(n) = n at n_draw(b) for b = 7, 9, 10.
Usage: python3 tests/check_universe_language.py [N] [D]      (defaults 20000, 2000)
"""
import os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bow_draw import carry_b, n_draw, is_prime

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
D = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
fails = 0

def report(name, ok, detail=""):
    global fails
    fails += 0 if ok else 1
    print(f"{name}: {detail}  {'PASS' if ok else 'FAIL'}")

def universes(n):
    """All (a, b) with [a][a]_b = n and b >= 1, that is b + 1 a divisor of n with b + 1 >= 2."""
    ds = {n}
    for d in range(2, int(n ** 0.5) + 1):
        if n % d == 0:
            ds |= {d, n // d}
    return [(n // d, d - 1) for d in sorted(ds)]

def tau(n):
    """Number of divisors from the prime factorisation."""
    t, p = 1, 2
    while p * p <= n:
        e = 0
        while n % p == 0:
            n //= p; e += 1
        t *= e + 1; p += 1
    return t * (2 if n > 1 else 1)

def trial_prime(n):
    return n >= 2 and all(n % k for k in range(2, int(n ** 0.5) + 1))

# 1. Theorem 1
bad = 0
for n in range(2, N + 1):
    u = universes(n)
    bad += any(a * b + a != n for a, b in u)
    bad += len(u) != tau(n) - 1
    bad += (len(u) == 1) != trial_prime(n)
    bad += (1, n - 1) not in u
report(f"1. every n, 2 <= n <= {N}: universes = tau(n) - 1, one universe <=> prime", bad == 0, f"{bad} failures")
for n in (7, 9, 12, 17):
    print("   ", n, len(universes(n)), "  ".join(f"[{a}][{a}]_{b}" for a, b in sorted(universes(n), key=lambda t: -t[1])))

# 2. ordinary digits
no_copy = [n for n in range(4, N + 1) if not trial_prime(n)
           and not any(2 <= a < b for a, b in universes(n))]
expected = sorted([6] + [p * p for p in range(2, int(N ** 0.5) + 1) if trial_prime(p)])
report(f"2. composites 4 <= n <= {N} with no copy in ordinary digits = 6 and the prime squares",
       no_copy == expected, f"{len(no_copy)} numbers: {no_copy[:6]} ...")

# 3. Theorem 2
rng = random.Random(2026)
worst = 0
for _ in range(200000):
    b = rng.randrange(2, 1000)
    x, y, c = rng.randrange(10 ** 30), rng.randrange(10 ** 30), 0
    while x or y or c:
        c = (x % b + y % b + c) // b
        worst = max(worst, c)
        x //= b; y //= b
report("3. 200000 random additions, bases 2 to 999, numbers below 10^30: largest carry", worst == 1, f"{worst}")

# 4. Theorem 3
def break_column(d):
    """First column j of row d - 1 with C(d-1, j) not congruent to (-1)^j modulo d, or None."""
    c = 1
    for j in range(1, d):
        c = c * (d - j) // j
        if (c - (-1) ** j) % d:
            return j
    return None

def smallest_prime_factor(d):
    return next(p for p in range(2, d + 1) if d % p == 0)

bad = 0
for d in range(2, D + 1):
    j = break_column(d)
    bad += (j is not None) if trial_prime(d) else (j != smallest_prime_factor(d))
report(f"4. rows d - 1 for 2 <= d <= {D}: break column = smallest prime factor, none for primes", bad == 0, f"{bad} failures")
for d in (3587, 1009 * 1013):
    j = break_column(d)
    report(f"   d = {d} = {smallest_prime_factor(d)} * {d // smallest_prime_factor(d)}", j == smallest_prime_factor(d), f"breaks at column {j}")

# 5. large examples
m61 = 2 ** 61 - 1
report("5. 2^61 - 1 = 2305843009213693951 is prime, so it appears in 1 universe", is_prime(m61), "[1][1]_2305843009213693950")
m67, p, q = 2 ** 67 - 1, 193707721, 761838257287
ok = p * q == m67 and is_prime(p) and is_prime(q)
report(f"   2^67 - 1 = {m67} = {p} * {q}, both factors prime, so tau = 4 and 3 universes", ok,
       f"[1][1]_{m67 - 1}  [{p}][{p}]_{q - 1}  [{q}][{q}]_{p - 1}")

# 6. Bow Draw
for b in (7, 9, 10):
    n, t, sol = n_draw(b), 0, []
    for k in range(1, 3 * b ** 3 + 300):
        t += carry_b(k, b)
        if t == k:
            sol.append(k)
    report(f"6. universe {b}: E_b(n) = n", sol == [n], f"solutions {sol}, formula {n}")

print(f"{fails} failures")
