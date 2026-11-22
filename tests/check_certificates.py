#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Existence of the Bow Draw point in every base b >= 2: polynomial certificates.

For each class b = 12t + r (r = 0..11), n(b) is a polynomial in t. The closed form of E_b(n)
contains floors floor(x(t) / q(t)) with q = b^i. Each floor is replaced by a polynomial F(t)
(found by interpolation) and certified: 0 <= x - qF <= q - 1 for all t >= t0, shown by
non-negative coefficients after the shift t -> t + t0. Then E_b(n(b)) - n(b) is a polynomial
in t, and the script checks that it is the zero polynomial. Bases below t0 are checked directly.
Primality is not used anywhere.
Usage: python3 tests/check_certificates.py
"""
from fractions import Fraction as Fr

class Poly:
    def __init__(self, c):
        c = [Fr(x) for x in c]
        while c and c[-1] == 0:
            c.pop()
        self.c = c
    def __add__(self, o):
        o = P(o); n = max(len(self.c), len(o.c))
        return Poly([(self.c[i] if i < len(self.c) else 0) + (o.c[i] if i < len(o.c) else 0) for i in range(n)])
    __radd__ = __add__
    def __neg__(self): return Poly([-x for x in self.c])
    def __sub__(self, o): return self + (-P(o))
    def __rsub__(self, o): return P(o) - self
    def __mul__(self, o):
        o = P(o); r = [Fr(0)] * (len(self.c) + len(o.c))
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                r[i + j] += a * b
        return Poly(r)
    __rmul__ = __mul__
    def __call__(self, t):
        v = Fr(0)
        for x in reversed(self.c):
            v = v * t + x
        return v
    def shift(self, t0):
        r = Poly([0])
        for x in reversed(self.c):
            r = r * Poly([t0, 1]) + x
        return r
    def nonneg(self, t0): return all(x >= 0 for x in self.shift(t0).c)
    def is_zero(self): return not self.c

def P(x): return x if isinstance(x, Poly) else Poly([x])
T = Poly([0, 1])

class CertFail(Exception):
    """A certificate condition failed. Raised explicitly, so the checks also run under python3 -O."""

def require(cond, what):
    if not cond:
        raise CertFail(what)

def integer_valued(F, t0):
    """True if F takes integer values at every integer t: a polynomial of degree d does so exactly when its
    values at d + 1 consecutive integers are integers (all forward differences are then integers)."""
    d = max(len(F.c) - 1, 0)
    return all(F(t).denominator == 1 for t in range(t0, t0 + d + 1))

def interpolate(xs, ys):
    r = Poly([0])
    for i, xi in enumerate(xs):
        term = Poly([ys[i]])
        for j, xj in enumerate(xs):
            if i != j:
                term = term * Poly([Fr(-xj, xi - xj), Fr(1, xi - xj)])
        r = r + term
    return r

COUNT = [0]
def floor_poly(x, q, t0):
    xs = list(range(t0, t0 + 6)); ys = [int(x(t)) // int(q(t)) for t in xs]
    F = interpolate(xs, ys); R = x - q * F
    require(integer_valued(x, t0) and integer_valued(F, t0), "x and F integer valued")
    require(R.nonneg(t0) and (q - R - 1).nonneg(t0), "0 <= x - qF <= q - 1 for t >= t0")
    COUNT[0] += 1
    return F

def f_poly(m, b, t0, powers):
    s, q = Poly([0]), b
    for _ in range(powers):
        s = s + floor_poly(m, q, t0); q = q * b
    return s

def S_poly(x, b, t0, powers):
    s, q = Poly([0]), b
    for _ in range(powers):
        a = floor_poly(x, q, t0)
        s = s + q * a * (a - 1) * Fr(1, 2) + a * (x - q * a + 1); q = q * b
    return s

def E_poly(n, b, t0, even):
    # b^3 <= n < b^4 (three powers); m ~ n/2 < b^3 (two powers, certified below)
    if even:
        m = n * Fr(1, 2)
        require((b * b * b - m - 2).nonneg(t0), "m + 1 < b^3")
        return S_poly(n, b, t0, 3) - (2 * S_poly(m - 1, b, t0, 2) + f_poly(m, b, t0, 2) + 2 * S_poly(m, b, t0, 2))
    m = (n - 1) * Fr(1, 2)
    require((b * b * b - m - 2).nonneg(t0), "m + 1 < b^3")
    return S_poly(n, b, t0, 3) - (4 * S_poly(m, b, t0, 2) + f_poly(m + 1, b, t0, 2))

def n_poly(r, b):
    if r % 2 == 0: return b * b * b + b * b + b - 2
    if r % 6 == 1: return b * b * b + (2 * b * b + 2 * b - 7) * Fr(1, 3)
    if r % 6 == 3: return b * b * b + (2 * b * b + 2 * b - 6) * Fr(1, 3)
    return b * b * b + (4 * b * b + 5 * b - 11) * Fr(1, 6)

if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from bow_draw import E, n_draw
    ok_all = True
    for r in range(12):
        b = 12 * T + r; n = n_poly(r, b); t_start = 1 if r < 2 else 0
        # n(t) is integer valued (degree 3: four consecutive integer values suffice) and equals n_draw(b)
        form_ok = integer_valued(n, t_start) and all(int(n(t)) == n_draw(int(b(t))) for t in range(t_start, t_start + 8))
        # the parity of an integer-valued cubic is periodic with a period dividing 4, so 60 values decide it
        parity = {int(n(t)) % 2 for t in range(t_start, t_start + 60)}
        form_ok = form_ok and len(parity) == 1
        even = parity == {0}
        D = None
        for t0 in range(t_start, 12):
            COUNT[0] = 0
            try:
                D = E_poly(n, b, t0, even) - n
                break
            except CertFail:
                continue
        else:
            t0 = t_start                          # no certificate found: the class fails below
        range_ok = D is not None and (n - b * b * b).nonneg(t0) and (b * b * b * b - n - 1).nonneg(t0)
        small = [int(b(t)) for t in range(t_start, t0)]
        small_ok = all(E(n_draw(q), q) == n_draw(q) for q in small)
        num_ok = all(E(n_draw(int(b(t))), int(b(t))) == n_draw(int(b(t))) for t in range(t0, 300))
        ok = form_ok and range_ok and D.is_zero() and small_ok and num_ok
        ok_all &= ok
        print(f"b = 12t + {r:<2}  n {'even' if even else 'odd '}  certificates {COUNT[0]:>2}  E_b(n) - n = 0 as a polynomial: {D is not None and D.is_zero()}  "
              f"valid for b >= {int(b(t0)):>2}  smaller bases {small} checked directly: {small_ok}  300 values: {num_ok}  {'PASS' if ok else 'FAIL'}")
    print("all twelve classes:", "PASS" if ok_all else "FAIL")
