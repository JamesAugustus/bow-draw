// bow_draw_scan.c -- Bow Draw full scan: every n from 1 to 3b^3 + 300 is counted one by one.
// SPDX-License-Identifier: MIT
//
// E_b(n) = number of carries when floor(k/2) and ceil(k/2) are added in base b, summed over k = 1..n.
// For every base b in [2, B) (or every prime, with "primes"): exactly one solution of E_b(n) = n,
// equal to n_draw(b); E_b(n) - n negative before it and positive after it; minimum at the expected place.
// Build: gcc -O3 -march=native -fopenmp tests/c/bow_draw_scan.c -o bow_draw_scan
// Usage: ./bow_draw_scan [B] [all|primes]       (default 400 all)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
typedef long long ll;
static inline int carry_b(ll k, ll b) {
    ll x = k / 2, y = k - k / 2; int c = 0, s = 0;
    while (x || y || c) { ll t = x % b + y % b + c; c = t >= b; s += c; x /= b; y /= b; }
    return s;
}
static ll n_draw(ll b) {
    if (b % 2 == 0) return b * b * b + b * b + b - 2;
    if (b % 6 == 1) return b * b * b + (2 * b * b + 2 * b - 7) / 3;
    if (b % 6 == 3) return b * b * b + (2 * b * b + 2 * b - 6) / 3;
    return b * b * b + (4 * b * b + 5 * b - 11) / 6;
}
static int is_prime(ll n) { if (n < 2) return 0; for (ll d = 2; d * d <= n; d++) if (n % d == 0) return 0; return 1; }
int main(int argc, char **argv) {
    int B = argc > 1 ? atoi(argv[1]) : 400, only_primes = argc > 2 && !strcmp(argv[2], "primes");
    double t0 = omp_get_wtime(); int bases = 0, pass = 0; ll steps = 0;
    #pragma omp parallel for schedule(dynamic, 1) reduction(+:bases, pass, steps)
    for (int i = B - 1; i >= 2; i--) {
        ll b = i;
        if (only_primes && !is_prime(b)) continue;
        ll N = 3 * b * b * b + 300, e = 0, sol = -1, low_n = 0, low = 0; int count = 0, pattern = 1;
        for (ll n = 1; n <= N; n++) {
            e += carry_b(n, b); ll d = e - n;
            if (d == 0) { count++; sol = n; }
            if (d < low) { low = d; low_n = n; }
            if (sol < 0 && d > 0) pattern = 0;
            if (sol >= 0 && n > sol && d <= 0) pattern = 0;
        }
        int low_ok = (b == 2) ? 1 : (b % 2) ? (low_n == b * b * b - 1 && low == -(b - 1) * (b + 2))
                                            : (low_n == b * b * b - b * b - 1 && low == -(b * b - 2));
        int ok = count == 1 && sol == n_draw(b) && pattern && low_ok;
        bases++; pass += ok; steps += N;
        if (!ok) {
            #pragma omp critical
            printf("FAIL b=%lld solutions=%d solution=%lld formula=%lld pattern=%d minimum=(%lld,%lld)\n", b, count, sol, n_draw(b), pattern, low_n, low);
        }
    }
    printf("%s 2 <= b < %d: %d bases, %lld steps (every n counted), %d PASS, %d FAIL  [%.1f s]\n",
           only_primes ? "primes" : "all bases", B, bases, steps, pass, bases - pass, omp_get_wtime() - t0);
    return 0;
}
