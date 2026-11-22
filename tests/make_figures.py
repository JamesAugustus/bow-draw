#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Figures 1 to 5 of FactorX (Section 7), computed from the definitions (requires matplotlib and numpy).

Usage: python3 tests/make_figures.py en figures
       python3 tests/make_figures.py tr figures      (Turkish files get the suffix _tr)
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from bow_draw import E, n_draw, carry_b, is_prime

LANG = sys.argv[1] if len(sys.argv) > 1 else "en"
OUT = sys.argv[2] if len(sys.argv) > 2 else "figures"
os.makedirs(OUT, exist_ok=True)
T = {
    "en": dict(n="$n$", min="minimum", arrow="arrow", sx="$(n - b^3)\\,/\\,b^2$", sy="$(E_b(n) - n)\\,/\\,b^2$",
               odd="odd b", even="even b", line="line", dashed="dashed", band="band", b="base b (logarithmic axis)",
               off="$(n(b) - b^3)\\,/\\,b^2$", cls1="b ≡ 1 (mod 6)", cls3="b ≡ 3 (mod 6)", cls5="b ≡ 5 (mod 6)", clse="b even",
               gap="prime gap $q - p$", dist="$(n(q) - n(p))\\,/\\,3p^2$", q="$q$", ratio="ratio (see the caption)",
               a="exponent $a$", lf="$\\log_q$ of the first solution", b7="base 7", pp="prime powers $q^a$"),
    "tr": dict(n="$n$", min="en dip", arrow="ok", sx="$(n - b^3)\\,/\\,b^2$", sy="$(E_b(n) - n)\\,/\\,b^2$",
               odd="tek b", even="çift b", line="çizgi", dashed="kesikli", band="bant", b="taban b (logaritmik eksen)",
               off="$(n(b) - b^3)\\,/\\,b^2$", cls1="b ≡ 1 (mod 6)", cls3="b ≡ 3 (mod 6)", cls5="b ≡ 5 (mod 6)", clse="b çift",
               gap="asal boşluğu $q - p$", dist="$(n(q) - n(p))\\,/\\,3p^2$", q="$q$", ratio="oran (alt yazıya bakın)",
               a="üs $a$", lf="ilk çözümün $\\log_q$ değeri", b7="taban 7", pp="asal kuvvetleri $q^a$"),
}[LANG]
# Text and axes stay in ink. Each series has its own hue (fixed order, checked for colour-blind separation on white)
# and a second cue (line style or marker), so the figures also read in black and white.
INK, GREY, LIGHT = "#182731", "#536675", "#b4bec5"
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"
LW = 1.8
DASH = (0, (5, 2.5))
plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 10, "axes.edgecolor": GREY, "axes.linewidth": 0.6,
                     "xtick.color": GREY, "ytick.color": GREY, "axes.labelcolor": INK, "text.color": INK,
                     "axes.spines.top": False, "axes.spines.right": False, "mathtext.fontset": "custom",
                     "mathtext.rm": "Liberation Serif", "mathtext.it": "Liberation Serif:italic", "mathtext.bf": "Liberation Serif:bold"})
from matplotlib.ticker import FuncFormatter
def save(fig, name):
    if LANG == "tr":                       # Turkish decimal comma on linear axes
        comma = FuncFormatter(lambda v, pos: ("%g" % v).replace("-", "−").replace(".", ","))
        for ax in fig.axes:
            if ax.get_xscale() == "linear": ax.xaxis.set_major_formatter(comma)
            if ax.get_yscale() == "linear": ax.yaxis.set_major_formatter(comma)
    if LANG == "tr": name = name.replace(".png", "_tr.png")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, name), dpi=200, metadata={"Software": None}); plt.close(fig)
def dot(ax, x, y, col):                    # point with a white ring, so it stands out where lines cross
    ax.plot([x], [y], "o", ms=6.5, color=col, mec="white", mew=1.2, zorder=5)

# Figure 1: the bow for b = 7, every n counted
b, run, xs, ys = 7, 0, [], []
for n in range(1, 721):
    run += carry_b(n, b); xs.append(n); ys.append(run - n)
fig, ax = plt.subplots(figsize=(6.4, 2.4))
ax.axhline(0, color=LIGHT, lw=0.8)
ax.plot(xs, ys, color=BLUE, lw=LW)
dot(ax, 342, -54, INK); ax.annotate(f"{T['min']}: n = 342 = 7³ − 1, −54", (342, -54), (380, -48), fontsize=9)
dot(ax, 378, 0, INK); ax.annotate(f"{T['arrow']}: n(7) = 378", (378, 0), (150, 60), fontsize=9, arrowprops=dict(arrowstyle="-", color=GREY, lw=0.7))
ax.set_xlabel(T["n"]); ax.set_ylabel("$E_7(n) - n$"); ax.set_title(T["b7"], fontsize=10, loc="left")
save(fig, "fig1_bow_base7.png")

# Figure 2: scaled curves near the cube, odd and even bases. The larger base is a wide pale band,
# the smaller base a line on top of it: where the two coincide, the line runs inside the band.
fig, ax = plt.subplots(figsize=(6.4, 2.8))
ax.axhline(0, color=LIGHT, lw=0.8)
for b, st, col in ((301, "-", BLUE), (300, "-", ORANGE), (101, "-", BLUE), (100, DASH, ORANGE)):
    x = np.arange(b**3 - 2 * b * b, b**3 + 2 * b * b + 1, max(1, b // 8))
    y = [(E(int(v), b) - int(v)) / b**2 for v in x]
    if b > 200: ax.plot((x - b**3) / b**2, y, "-", color=col, lw=6, alpha=0.28, solid_capstyle="round")
    else:       ax.plot((x - b**3) / b**2, y, linestyle=st, color=col, lw=LW)
ax.plot([-1.95, -1.65], [1.32, 1.32], "-", color=BLUE, lw=LW)
ax.text(-1.58, 1.28, f"{T['odd']}: 101 ({T['line']}), 301 ({T['band']})", fontsize=9)
ax.plot([-1.95, -1.65], [1.06, 1.06], linestyle=DASH, color=ORANGE, lw=LW)
ax.text(-1.58, 1.02, f"{T['even']}: 100 ({T['dashed']}), 300 ({T['band']})", fontsize=9)
dot(ax, 2/3, 0, INK); ax.annotate("2/3", (2/3, 0), (0.45, 0.2), fontsize=9)
dot(ax, 1, 0, INK); ax.annotate("1", (1, 0), (1.05, -0.25), fontsize=9)
ax.set_xlabel(T["sx"]); ax.set_ylabel(T["sy"])
save(fig, "fig2_scaled_shape.png")

# Figure 3: offset of the arrow beyond the cube, per class (a logarithmic b axis spreads the small bases)
fig, ax = plt.subplots(figsize=(6.4, 2.6))
B = range(5, 401)
for test, lab, mk, col, ls in ((lambda b: b % 6 == 1, T["cls1"], "o", BLUE, "-"), (lambda b: b % 6 == 3, T["cls3"], "^", AQUA, (0, (4, 2))),
                               (lambda b: b % 6 == 5, T["cls5"], "D", YELLOW, "-"), (lambda b: b % 2 == 0, T["clse"], "s", ORANGE, "-")):
    bs = [b for b in B if test(b)]; vs = [(n_draw(b) - b**3) / b**2 for b in bs]
    ax.plot(bs, vs, linestyle=ls, color=col, lw=1.5, label=lab, marker=mk, ms=4, mec=col, mfc="white", mew=1.0,
            markevery=[i for i, b in enumerate(bs) if b < 60])
ax.axhline(2/3, color=GREY, lw=0.7, ls=":"); ax.axhline(1, color=GREY, lw=0.7, ls=":")
ax.set_xscale("log"); ax.set_xticks([5, 10, 20, 50, 100, 200, 400]); ax.set_xticklabels(["5", "10", "20", "50", "100", "200", "400"])
ax.minorticks_off()
ax.set_ylim(0.6, 1.2); ax.set_xlabel(T["b"]); ax.set_ylabel(T["off"]); ax.legend(fontsize=9, ncol=2, frameon=False, loc="upper right")
if LANG == "tr": ax.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: ("%g" % v).replace(".", ",")))
save(fig, "fig3_offset_by_class.png")

# Figure 4: distance between the arrows of consecutive primes
P = [p for p in range(5, 20000) if is_prime(p)]
fig, ax = plt.subplots(1, 2, figsize=(6.6, 2.8))
d = [((n_draw(q) - n_draw(p)) / (3 * p * p), q - p) for p, q in zip(P[:400], P[1:401])]
ax[0].plot([0, 36], [0, 36], color=GREY, lw=0.8, ls=":")
ax[0].plot([x for x, _ in d], [y for _, y in d], "o", ms=3.4, color=BLUE, mec="white", mew=0.4)
ax[0].set_xlabel(T["dist"]); ax[0].set_ylabel(T["gap"])
r = [(n_draw(q) - n_draw(p)) / ((q**3 - p**3) + (2 / 3) * (q * q - p * p)) for p, q in zip(P, P[1:])]
ax[1].axhline(1, color=GREY, lw=0.7, ls=":")
ax[1].plot(P[1:], r, ".", ms=1.8, color=BLUE); ax[1].set_xscale("log"); ax[1].set_xlabel(T["q"]); ax[1].set_ylabel(T["ratio"])
save(fig, "fig4_prime_arrows.png")

# Figure 5: first solution for prime powers q^a, every n counted. Points of q ≥ 3 at the same a
# are shifted slightly sideways so that they do not hide each other.
def first_solution(q, a, N):
    s = 0
    for n in range(1, N + 1):
        s += carry_b(n, q)
        if s // a == n: return n
pts = []
for q, amax in ((2, 6), (3, 4), (5, 3), (7, 2), (11, 2), (13, 2)):
    for a in range(1, amax + 1):
        N = 3 * q ** (2 * a + 2 if q == 2 else 2 * a + 1) + 1000
        if N > 1_300_000: continue
        f = first_solution(q, a, N)
        pts.append((q, a, math.log(f, q)))
fig, ax = plt.subplots(figsize=(6.4, 2.9))
aa = np.array([0.8, 6.2]); ax.plot(aa, 2 * aa + 1, color=GREY, lw=0.9); ax.plot(aa, 2 * aa + 2, color=GREY, lw=0.9, ls="--")
ax.text(4.35, 7.9, "2a + 1", color=GREY, fontsize=9); ax.text(2.35, 8.5, "2a + 2  (q = 2)", color=GREY, fontsize=9)
QS = ((2, "s", BLUE), (3, "^", ORANGE), (5, "o", AQUA), (7, "D", YELLOW), (11, "v", MAGENTA), (13, "P", GREEN))
for i, (q, mk, col) in enumerate(QS):
    sel = [(a, v) for qq, a, v in pts if qq == q]; dx = 0 if q == 2 else (i - 3) * 0.07   # q = 2 lies apart, the others cluster
    ax.plot([a + dx for a, _ in sel], [v for _, v in sel], mk, ms=5.5, color=col, mec=INK, mew=0.5, label=f"q = {q}", zorder=4)
ax.set_xticks(range(1, 7)); ax.set_xlabel(T["a"]); ax.set_ylabel(T["lf"])
ax.legend(fontsize=9, ncol=6, frameon=False, loc="upper left", handletextpad=0.2, columnspacing=0.9); ax.set_title(T["pp"], fontsize=10, loc="left")
save(fig, "fig5_prime_powers.png")
print("figures written to", OUT, ":", sorted(os.listdir(OUT)))
for q, a, v in pts: print(f"   q = {q:>2}, a = {a}: log_q(first solution) = {v:.3f}")
