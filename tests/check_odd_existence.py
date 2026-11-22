#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Step 6 of the odd-base proof (FactorX Section 6.4, Bow Draw paper Section 5.4): existence and location by hand.

For odd b with r = (b - 1)/2, G(m) = sum_{h=1..m} (kappa(h) - 1), kappa(h) = carries of h + h in base b.
The program counts G directly and checks, for every odd b in the range:
  1. G(r*b^2 + x) = -2r^2 - r + 1 + k(3r + 1) + phi(y) for x = (r + 1 + k)*b + y, phi(y) = y + max(0, y - r),
     and G <= -2r^2 - r for x = r*b + y with y > r;
  2. the steps of G between (b^3 - 1)/2 and (r + 1)*b^2 - 1 are 1 or 2;
  3. the zero given by the table of Step 6 (by r mod 3) is n(b) from (6.1): G(m0) = 0 with n = 2*m0,
     or G(m1) = -1, G(m1 + 1) = 1 with n = 2*m1 + 1.
Usage: python3 tests/check_odd_existence.py [B]      (default 101: every odd b with 3 <= b <= B)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bow_draw import n_draw

def kappa(h, b):
    c = cnt = 0
    while h or c:
        s = 2 * (h % b) + c; c = 1 if s >= b else 0; cnt += c; h //= b
    return cnt

def check(b):
    r = (b - 1) // 2
    G, vals = 0, {}
    for h in range(1, (r + 1) * b * b):
        G += kappa(h, b) - 1
        if h >= r * b * b - 1: vals[h] = G
    ok = True
    for k in range(r):
        for y in range(2 * r + 1):
            m = r * b * b + (r + 1 + k) * b + y
            ok &= vals[m] == -2 * r * r - r + 1 + k * (3 * r + 1) + y + max(0, y - r)
    for y in range(r + 1, 2 * r + 1):
        ok &= vals[r * b * b + r * b + y] <= -2 * r * r - r
    lo, hi = (b ** 3 - 1) // 2, (r + 1) * b * b - 1
    G_lo = vals.get(lo)
    if G_lo is None:                               # lo lies before r*b^2 - 1 only for tiny b; recount
        G_lo = sum(kappa(h, b) - 1 for h in range(1, lo + 1))
    prev = G_lo
    for h in range(lo + 1, hi + 1):
        g = vals[h] if h in vals else None
        if g is None: continue
        ok &= 1 <= g - prev <= 2; prev = g
    s, t = divmod(r, 3)
    if t == 0:   k, y, odd = 2 * s, s - 1, False
    elif t == 1: k, y, odd = 2 * s, 5 * s + 1, True
    elif s % 2 == 0: k, y, odd = 2 * s + 1, (7 * s + 4) // 2, False
    else:            k, y, odd = 2 * s + 1, (7 * s + 3) // 2, True
    m = r * b * b + (r + 1 + k) * b + y
    n = 2 * m + (1 if odd else 0)
    ok &= n == n_draw(b)
    ok &= (vals[m] == -1 and vals[m + 1] == 1) if odd else vals[m] == 0
    return ok, n

if __name__ == "__main__":
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 101
    fails = 0
    for b in range(3, B + 1, 2):
        ok, n = check(b)
        fails += not ok
        if b <= 15 or not ok:
            print(f"b = {b:>4}  zero of D_b from Step 6 at n = {n}  {'PASS' if ok else 'FAIL'}")
    print(f"odd bases 3 <= b <= {B}: {(B - 1) // 2} bases, {fails} failures")
