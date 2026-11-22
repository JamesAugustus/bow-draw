# SPDX-License-Identifier: MIT
"""Bow Draw: shared definitions (no external libraries).

c(k)     = C(k, floor(k/2)), the central binomial coefficient.
carry_b(k) = number of carries when floor(k/2) and ceil(k/2) are added in base b.
E_b(n)   = carry_b(1) + ... + carry_b(n).
For a prime p, E_p(n) is the exponent of p in c(1) c(2) ... c(n) (Kummer).
"""

def carries(x, y, b):
    """Number of carries when x and y are added in base b."""
    c = s = 0
    while x or y or c:
        t = x % b + y % b + c
        c = 1 if t >= b else 0
        s += c
        x //= b
        y //= b
    return s

def carry_b(k, b):
    return carries(k // 2, k - k // 2, b)

def f(m, b):
    """sum_{i>=1} floor(m / b^i)."""
    s, q = 0, b
    while q <= m:
        s += m // q
        q *= b
    return s

def g(n, q):
    """sum_{k=1..n} floor(k / q)."""
    a, r = divmod(n, q)
    return q * a * (a - 1) // 2 + a * (r + 1)

def S(n, b):
    """sum_{k=1..n} f(k)."""
    s, q = 0, b
    while q <= n:
        s += g(n, q)
        q *= b
    return s

def E(n, b):
    """E_b(n) in closed form; each value costs O(log n) big-integer operations."""
    m = n // 2
    T = 4 * S(m, b) - f(m, b) if m > 0 else 0
    if n % 2:
        T += f(m, b) + f(m + 1, b)
    return S(n, b) - T

def n_draw(b):
    """The unique n with E_b(n) = n, b >= 2."""
    if b % 2 == 0:
        return b**3 + b * b + b - 2
    if b % 6 == 1:
        return b**3 + (2 * b * b + 2 * b - 7) // 3
    if b % 6 == 3:
        return b**3 + (2 * b * b + 2 * b - 6) // 3
    return b**3 + (4 * b * b + 5 * b - 11) // 6

def is_prime(n, rounds=16, rng=None):
    """Miller-Rabin; deterministic below 3.3e24, probable prime above."""
    import random
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    for q in small:
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    rng = rng or random
    bases = small + (tuple(rng.randrange(2, n - 1) for _ in range(rounds)) if n >= 3317044064679887385961981 else ())
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True
