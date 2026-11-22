#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Full scan for small bases: every n from 1 to 3b^3 + 300 is counted one by one.

Checks, for each base 2 <= b < B:
  1. the closed form E(n, b) equals the carry count (n < 3000),
  2. E_b(n) = n has exactly one solution and it equals n_draw(b),
  3. E_b(n) - n is negative before the solution and positive after it,
  4. the minimum of E_b(n) - n: odd b at n = b^3 - 1 with value -(b - 1)(b + 2);
     even b at n = b^3 - b^2 - 1 with value -(b^2 - 2).
Usage: python3 tests/check_small.py [B]        (default 41)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bow_draw import carry_b, E, n_draw

B = int(sys.argv[1]) if len(sys.argv) > 1 else 41
fails = 0
for b in range(2, B):
    t = 0
    closed = True
    for n in range(1, 3000):
        t += carry_b(n, b)
        closed &= E(n, b) == t
    N, e, sol, low = 3 * b**3 + 300, 0, [], (0, 0)
    pattern = True
    for n in range(1, N + 1):
        e += carry_b(n, b)
        d = e - n
        if d == 0:
            sol.append(n)
        if d < low[1]:
            low = (n, d)
        if (not sol and d > 0) or (sol and n > sol[0] and d <= 0):
            pattern = False
    want_low = (b**3 - 1, -(b - 1) * (b + 2)) if b % 2 else (b**3 - b * b - 1, -(b * b - 2))
    ok = closed and sol == [n_draw(b)] and pattern and (b == 2 or low == want_low)
    fails += not ok
    print(f"b = {b:>3}: solution {sol}  formula {n_draw(b):>9}  minimum {low}  {'PASS' if ok else 'FAIL'}")
print(f"{B - 2} bases, {fails} failures")
