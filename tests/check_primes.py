#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""All primes 5 <= p < L and R random large primes, with the closed form of E_p(n).

For every prime: E(n(p)) = n(p), E(n(p) - 1) < n(p) - 1 and E(n(p) + 1) > n(p) + 1.
For random primes of 20 to 200 digits, also 200 random n in [p^3 - 1, 3p^3]: E(n) - n < 0 before n(p), > 0 after.
Usage: python3 tests/check_primes.py [L] [R]      (default 1000000 200; uses all CPU cores)
"""
import os, sys, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool
from bow_draw import E, n_draw, is_prime

def segment(ab):
    a, b = ab
    root = int(b ** 0.5) + 1
    small = bytearray([1]) * (root + 1); small[0:2] = b"\0\0"
    for i in range(2, int(root ** 0.5) + 1):
        if small[i]: small[i * i::i] = bytearray(len(small[i * i::i]))
    sieve = bytearray([1]) * (b - a)
    for q in range(2, root + 1):
        if small[q]:
            start = max(q * q, (a + q - 1) // q * q)
            sieve[start - a::q] = bytearray(len(sieve[start - a::q]))
    count = bad = 0
    for i in range(b - a):
        p = a + i
        if p < 5 or not sieve[i]: continue
        n = n_draw(p); count += 1
        if not (E(n, p) == n and E(n - 1, p) < n - 1 and E(n + 1, p) > n + 1): bad += 1
    return count, bad

def big(seed):
    rng = random.Random(seed)
    digits = rng.randint(20, 200)
    p = rng.randrange(10 ** (digits - 1), 10 ** digits) | 1
    while not is_prime(p, rng=rng): p += 2
    n = n_draw(p)
    ok = E(n, p) == n and E(n - 1, p) < n - 1 and E(n + 1, p) > n + 1
    for _ in range(200):
        x = rng.randrange(p**3 - 1, 3 * p**3); d = E(x, p) - x
        ok &= (d < 0) if x < n else (d > 0) if x > n else d == 0
    return digits, ok

if __name__ == "__main__":
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    R = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    t = time.time(); step = 1_000_000
    with Pool() as pool:
        res = pool.map(segment, [(a, min(a + step, L)) for a in range(0, L, step)])
    c = sum(x for x, _ in res); bad = sum(y for _, y in res)
    print(f"all primes 5 <= p < {L}: {c} primes, {bad} failures  {'PASS' if not bad else 'FAIL'}  [{time.time() - t:.1f} s]")
    t = time.time()
    with Pool() as pool:
        res = pool.map(big, range(R))
    ok = sum(o for _, o in res)
    print(f"{R} random primes ({min(d for d, _ in res)} to {max(d for d, _ in res)} digits): {ok}/{R}  {'PASS' if ok == R else 'FAIL'}  [{time.time() - t:.1f} s]")
