#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exponent of a composite m in c(1) ... c(n): K_m(n) = min_i floor(E(n, q_i) / a_i), m = prod q_i^a_i.

Counts the solutions of K_m(n) = n for 2 <= m <= M (n <= N, every n one by one) and checks:
  primes: one solution n(p); square-free m: one solution n(q_max) (proved);
  other m: is the solution set equal to that of the prime-power factor whose first solution lies
  farthest out? This is an observation, reported as "rule yes/no", not counted as a failure.
n runs up to 3 q^(2a+1) + 1000 for the largest factor (q = 2: 3 * 2^(2a+2) + 1000), as in tests/c/bow_draw_composite.c.
A smaller N can be given; then m whose range is not covered are reported as SKIP.
Usage: python3 tests/check_composite.py [M] [N]     (default M = 40, N automatic)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bow_draw import carry_b, n_draw

M = int(sys.argv[1]) if len(sys.argv) > 1 else 40
def factor(m):
    out, d = {}, 2
    while d * d <= m:
        while m % d == 0: out[d] = out.get(d, 0) + 1; m //= d
        d += 1
    if m > 1: out[m] = out.get(m, 0) + 1
    return out
def bound(q, a):
    return 3 * q ** (2 * a + 2 if q == 2 else 2 * a + 1) + 1000
def needed(m):
    return max(bound(q, a) for q, a in factor(m).items())
N = int(sys.argv[2]) if len(sys.argv) > 2 else max(needed(m) for m in range(2, M + 1))
primes = sorted({q for m in range(2, M + 1) for q in factor(m)})
Eq = {}
for q in primes:
    run, s = [0] * (N + 1), 0
    for n in range(1, N + 1): s += carry_b(n, q); run[n] = s
    Eq[q] = run
def solutions(fac):
    return [n for n in range(1, N + 1) if min(Eq[q][n] // a for q, a in fac.items()) == n]
fails = rule_yes = rule_no = skipped = 0
print(f"2 <= m <= {M}, every n from 1 to {N} counted")
for m in range(2, M + 1):
    if needed(m) > N:
        skipped += 1
        print(f"m = {m:>3}  SKIP (needs n up to {needed(m)})")
        continue
    fac = factor(m); sol = solutions(fac)
    if len(fac) == 1 and list(fac.values()) == [1]:
        kind, ok = "prime", sol == [n_draw(m)] if m >= 5 else len(sol) == 1
    elif max(fac.values()) == 1:
        kind, ok = "square-free", sol == [n_draw(max(fac))] if max(fac) >= 5 else sol == solutions({max(fac): 1})
    elif len(fac) == 1:
        print(f"m = {m:>3}  {'prime power':<28} solutions {len(sol):>3}  first {sol[0] if sol else '-':>6}")
        continue
    else:
        parts = {q**a: solutions({q: a}) for q, a in fac.items()}
        lead = max(parts, key=lambda x: parts[x][0])
        same = sol == parts[lead]
        rule_yes += same; rule_no += not same
        print(f"m = {m:>3}  {'other (farthest factor ' + str(lead) + ')':<28} solutions {len(sol):>3}  first {sol[0] if sol else '-':>6}  rule {'yes' if same else 'no'}")
        continue
    fails += not ok
    print(f"m = {m:>3}  {kind:<28} solutions {len(sol):>3}  first {sol[0] if sol else '-':>6}  {'PASS' if ok else 'FAIL'}")
print(f"{M - 1} values of m, {skipped} skipped: {fails} failures among primes and square-free m  {'PASS' if not fails else 'FAIL'}; farthest-factor rule {rule_yes} yes, {rule_no} no")
