// bow_draw_composite.c -- exponent of a composite m in c(1) c(2) ... c(n), every n counted one by one.
// SPDX-License-Identifier: MIT
//
// m = q_1^a_1 ... q_k^a_k.  K_m(n) = min_i floor(E_{q_i}(n) / a_i), with E_q the carry sum (Kummer).
// For every 2 <= m <= M the solutions of K_m(n) = n are counted for n up to 3 q^(2a+1) + 1000
// (largest factor; q = 2: 3 * 2^(2a+2) + 1000). Reported:
//   primes:        exactly one solution (proved),
//   square-free:   exactly one solution, equal to that of the largest prime factor (proved),
//   prime powers:  number of solutions and the first one,
//   other m:       does the solution set equal that of the prime-power factor whose first solution
//                  lies farthest out? (an observation, counted, not a theorem). Only stored solutions are printed.
// Build: gcc -O3 -march=native -fopenmp tests/c/bow_draw_composite.c -o bow_draw_composite
// Usage: ./bow_draw_composite [M]      (default 300; M <= 4095)
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
#define KEEP 64
typedef struct { int count; ll first[KEEP]; } Set;      // solution set: first KEEP solutions and total count
static Set scan(int nf, const ll *q, const int *a, ll N) {
    Set S; S.count = 0; ll E[8] = {0};
    for (ll n = 1; n <= N; n++) {
        ll mn = -1;
        for (int i = 0; i < nf; i++) { E[i] += carry_b(n, q[i]); ll v = E[i] / a[i]; if (mn < 0 || v < mn) mn = v; }
        if (mn == n) { if (S.count < KEEP) S.first[S.count] = n; S.count++; }
    }
    return S;
}
static int same(const Set *x, const Set *y) {
    if (x->count != y->count) return 0;
    int k = x->count < KEEP ? x->count : KEEP;
    for (int i = 0; i < k; i++) if (x->first[i] != y->first[i]) return 0;
    return 1;
}
static ll bound(ll q, int a) { ll v = 1; int e = (q == 2) ? 2 * a + 2 : 2 * a + 1; for (int i = 0; i < e; i++) v *= q; return 3 * v + 1000; }
static int factor(ll m, ll *q, int *a) {
    int nf = 0;
    for (ll d = 2; d * d <= m; d++) if (m % d == 0) { q[nf] = d; a[nf] = 0; while (m % d == 0) { m /= d; a[nf]++; } nf++; }
    if (m > 1) { q[nf] = m; a[nf] = 1; nf++; }
    return nf;
}
int main(int argc, char **argv) {
    int M = argc > 1 ? atoi(argv[1]) : 300; if (M > 4095) M = 4095;
    double t0 = omp_get_wtime();
    static Set sol[4096]; static int is_pp[4096];
    #pragma omp parallel for schedule(dynamic, 1)
    for (int j = 0; j < M - 1; j++) {
        ll m = M - j, q[8]; int a[8], nf = factor(m, q, a); ll N = 0;
        for (int i = 0; i < nf; i++) { ll u = bound(q[i], a[i]); if (u > N) N = u; }
        sol[m] = scan(nf, q, a, N); is_pp[m] = nf == 1;
    }
    int n_prime = 0, ok_prime = 0, n_sf = 0, ok_sf = 0, n_pp = 0, one_pp = 0, n_other = 0, rule = 0;
    for (ll m = 2; m <= M; m++) {
        ll q[8]; int a[8], nf = factor(m, q, a), sf = 1;
        for (int i = 0; i < nf; i++) if (a[i] > 1) sf = 0;
        if (nf == 1 && a[0] == 1) { n_prime++; ok_prime += sol[m].count == 1; continue; }
        if (nf == 1) { n_pp++; one_pp += sol[m].count == 1; continue; }
        if (sf) { n_sf++; ll Q = q[nf - 1]; if (sol[m].count == 1 && sol[Q].count == 1 && sol[m].first[0] == sol[Q].first[0]) ok_sf++; }
        n_other++;
        ll lead = -1;
        for (int i = 0; i < nf; i++) { ll v = 1; for (int t = 0; t < a[i]; t++) v *= q[i]; if (lead < 0 || sol[v].first[0] > sol[lead].first[0]) lead = v; }
        if (same(&sol[m], &sol[lead])) rule++;
        else {
            printf("   rule does not hold: m = %lld, farthest factor %lld (%d solutions:", m, lead, sol[lead].count);
            for (int i = 0; i < sol[lead].count && i < 4; i++) printf(" %lld", sol[lead].first[i]);
            printf("%s), m has %d solutions:", sol[lead].count > 4 ? " ..." : "", sol[m].count);
            for (int i = 0; i < sol[m].count && i < 6; i++) printf(" %lld", sol[m].first[i]);
            printf("%s\n", sol[m].count > 6 ? " ..." : "");
        }
    }
    printf("2 <= m <= %d (every n counted):\n", M);
    printf("   primes: %d, exactly one solution: %d  %s\n", n_prime, ok_prime, ok_prime == n_prime ? "PASS" : "FAIL");
    printf("   square-free composites: %d, one solution equal to that of the largest prime factor: %d  %s\n", n_sf, ok_sf, ok_sf == n_sf ? "PASS" : "FAIL");
    printf("   prime powers q^a (a >= 2): %d, of which with exactly one solution: %d\n", n_pp, one_pp);
    printf("   composites with two or more prime factors: %d, same set as the farthest prime-power factor: %d, different: %d  (observation)\n", n_other, rule, n_other - rule);
    printf("   prime powers with exactly one solution:");
    for (ll m = 4; m <= M; m++) if (is_pp[m] && sol[m].count == 1) { ll q[8]; int a[8]; factor(m, q, a); if (a[0] >= 2) printf(" %lld (%lld)", m, sol[m].first[0]); }
    printf("\n   [%.1f s]\n", omp_get_wtime() - t0);
    return 0;
}
