#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Numerical check of every step of the uniqueness proof (odd bases, prime or composite).

kappa(h) = carries of h + h in base b, r = (b - 1)/2, G(m) = sum_{h=1..m} (kappa(h) - 1).
Checked for every odd b in [3, B):
  Lemma 1      carries(h, h + 1) = kappa(h + 1)                       for h < b^3
  Lemma 2      E_b(2m) - 2m = 2 G(m),  E_b(2m + 1) - (2m + 1) = G(m) + G(m + 1)
  Step 0       G < 0 on [1, b^2 - 1],  G((b^2 - 1)/2) = -r^2 - 2r,  G(b^2 - 1) = -r
  Step 1       G < 0 on [1, (b^3 - 1)/2] and min G on [1, b^3 - 1] = G((b^3 - 1)/2) = -2r^2 - 3r
  Step 2       G rises by at least 1 per step on [(b^3 - 1)/2, (r + 1) b^2 - 1]
  Step 3       G((r + 1) b^2 - 1) = r^2
  Step 4       G never falls on [(r + 1) b^2 - 1, b^3 - 1] and G(b^3 - 1) = r (b^2 - 1)
  Step 5       G(m) >= r (b^2 - 1) - 2r^2 - 3r - 1 on [b^3, 3 b^3]
Usage: python3 tests/check_proof_steps.py [B]      (default 101)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bow_draw import carries, E

B = int(sys.argv[1]) if len(sys.argv) > 1 else 101
fails = 0
for b in range(3, B, 2):
    r = (b - 1) // 2; top = 3 * b**3
    kap = [carries(h, h, b) for h in range(top + 2)]
    G = [0] * (top + 2)
    for h in range(1, top + 2): G[h] = G[h - 1] + kap[h] - 1
    c = {}
    c["lemma1"] = all(carries(h, h + 1, b) == kap[h + 1] for h in range(b**3))
    c["lemma2"] = all(E(2 * m, b) - 2 * m == 2 * G[m] and E(2 * m + 1, b) - (2 * m + 1) == G[m] + G[m + 1] for m in range(0, top, max(1, top // 2000)))
    q2, h3, top_r = (b * b - 1) // 2, (b**3 - 1) // 2, (r + 1) * b * b - 1
    c["step0"] = max(G[1:b * b]) < 0 and G[q2] == -r * r - 2 * r and G[b * b - 1] == -r
    c["step1"] = max(G[1:h3 + 1]) < 0 and min(G[1:b**3]) == G[h3] == -2 * r * r - 3 * r
    c["step2"] = all(G[m + 1] - G[m] >= 1 for m in range(h3, top_r))
    c["step3"] = G[top_r] == r * r
    c["step4"] = all(G[m + 1] >= G[m] for m in range(top_r, b**3 - 1)) and G[b**3 - 1] == r * (b * b - 1)
    c["step5"] = min(G[b**3:top + 1]) >= r * (b * b - 1) - 2 * r * r - 3 * r - 1
    ok = all(c.values()); fails += not ok
    print(f"b = {b:>3} ({'prime' if all(b % d for d in range(2, int(b**.5) + 1)) else 'composite'}): "
          + " ".join(k for k, v in c.items() if not v) + ("all steps PASS" if ok else " FAIL"))
print(f"{len(range(3, B, 2))} odd bases, {fails} failures")
