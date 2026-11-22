// bow_draw_gpu.c -- Bow Draw full scan on a GPU (Vulkan compute), every base 2 <= b < B, every n.
// SPDX-License-Identifier: MIT
//
// The card handles blocks of 256 consecutive n: it keeps floor(n/2) and n - floor(n/2) as digit arrays in
// base b and increments one digit per step (no division), and returns for each block the sum of (carries - 1)
// and the smallest and largest prefix sum. The CPU adds the blocks in order, recounts exactly every block
// where a zero could occur and the block of the minimum. Identifiers inside are in Turkish (see vk_common.h).
// Build: sh tests/gpu/build.sh  Usage: ./tests/gpu/bow_draw_gpu [B]      (default 1000; the .spv file must sit next to the program)
#include "vk_common.h"
typedef long long ll;
static int elde(ll k, ll p) { ll a = k / 2, b = k - k / 2; int c = 0, s = 0; while (a || b || c) { ll t = a % p + b % p + c; c = t >= p; s += c; a /= p; b /= p; } return s; }
static ll draw(ll b) { if (b % 2 == 0) return b*b*b + b*b + b - 2; if (b % 6 == 1) return b*b*b + (2*b*b + 2*b - 7)/3; if (b % 6 == 3) return b*b*b + (2*b*b + 2*b - 6)/3; return b*b*b + (4*b*b + 5*b - 11)/6; }
int main(int argc, char **argv) {
    int PA = argc > 1 ? atoi(argv[1]) : 1000; if (PA < 3) PA = 3;
    const uint32_t B = 256, CH = 1u << 16;                 // block length, blocks per submission
    vk_baslat();
    Tampon O = vk_tampon((VkDeviceSize)CH * 16, 1); Tampon *bag[1] = { &O };
    Boru K = vk_boru("bow_draw_block64.spv", 1, bag, 32);
    int32_t *al = malloc((size_t)CH * 16);
    double t0 = simdi(), kart = 0; ll adim = 0, yeniden = 0; int np = 0, iyi = 0;
    for (ll p = 2; p < PA; p++) {
        np++;
        ll N = 3 * p * p * p + 300, T = (N + B - 1) / B;
        ll V = 0;                                          // E(n) - n at the start of the block (at the previous n)
        int say = 0, gecti = 0, ihlal = 0; ll cozum = -1, dipv = 1, dipb = -1, dipV = 0;
        for (ll b0 = 0; b0 < T; b0 += CH) {
            uint32_t nb = (uint32_t)((T - b0) < CH ? (T - b0) : CH);
            ll n0 = b0 * B; int L = 1; { ll x = N; while (x) { L++; x /= p; } } uint32_t pc[8] = { (uint32_t)p, (uint32_t)(n0 & 0xffffffff), (uint32_t)(n0 >> 32), B, nb, (uint32_t)(N & 0xffffffff), (uint32_t)(N >> 32), (uint32_t)L };
            VkCommandBuffer cb = vk_kb_ac(); vk_damga_sifirla(cb); vk_damga(cb, 0); vk_boru_bagla(cb, &K); vk_itme(cb, &K, pc);
            vk_dagit(cb, (nb + 63) / 64); vk_damga(cb, 1); vk_kb_bitir(cb); vk_kb_gonder(cb); kart += vk_damga_sure(); vk_kb_birak(cb);
            vk_indir(al, &O, (VkDeviceSize)nb * 16);
            for (uint32_t i = 0; i < nb; i++) {
                ll s = al[4 * i], lo = V + al[4 * i + 1], hi = V + al[4 * i + 2];
                ll bas = (b0 + i) * B + 1;
                if (lo < dipv) { dipv = lo; dipb = b0 + i; dipV = V; }
                if (lo <= 0 && hi >= 0) {                  // a zero may occur here: count one by one
                    ll v = V; yeniden++;
                    for (ll n = bas; n < bas + B && n <= N; n++) {
                        v += elde(n, p) - 1;
                        if (v == 0) { say++; cozum = n; gecti = 1; }
                        else if (!gecti && v > 0) ihlal = 1;
                        else if (gecti && v < 0) ihlal = 1;
                    }
                } else if (!gecti && lo > 0) ihlal = 1;    // became positive without touching zero
                else if (gecti && hi < 0) ihlal = 1;       // negative after the solution
                V += s;
            }
        }
        // the minimum: count the block one by one, place of the first smallest value
        ll v = dipV, dipn = -1, dmin = 1; ll bas = dipb * B + 1;
        for (ll n = bas; n < bas + B && n <= N; n++) { v += elde(n, p) - 1; if (v < dmin) { dmin = v; dipn = n; } }
        adim += N;
        int ok_draw = cozum == draw(p);
        int ok_dip = (p % 2 == 0) ? 1 : (dipn == p * p * p - 1 && dmin == -(p - 1) * (p + 2));
        if (say == 1 && ok_draw && !ihlal && ok_dip) iyi++;
        else printf("FAIL b=%lld solutions=%d solution=%lld violation=%d minimum=(%lld,%lld)\n", p, say, cozum, ihlal, dipn, dmin);
    }
    printf("GPU full scan, all bases (64-bit, division-free): %d bases (2 <= b < %d), %lld steps; one solution = n_draw, sign pattern and minimum: %d/%d PASS\n", np, PA, adim, iyi, np);
    printf("card time %.1f s, total %.1f s; blocks recounted on the CPU: %lld\n", kart, simdi() - t0, yeniden);
    return 0;
}
