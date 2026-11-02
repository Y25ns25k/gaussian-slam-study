#!/usr/bin/env python3
"""Regenerate every figure in figures/ from the JSON tables in results/ (CPU only; numpy + matplotlib).

    python scripts/make_figures.py
"""
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES, FIG = ROOT / "results", ROOT / "figures"
FIG.mkdir(exist_ok=True)

# Palette: validated categorical order (blue, orange, aqua, yellow, magenta); text tokens; recessive grid.
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
GRAY = "#8a8984"
SURFACE, TEXT, TEXT2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e0"
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": TEXT2, "xtick.color": TEXT2, "ytick.color": TEXT2,
    "text.color": TEXT, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "font.size": 10, "axes.titlesize": 11,
    "axes.titleweight": "bold", "legend.frameon": False, "lines.linewidth": 2, "lines.solid_capstyle": "round",
})


def load(name):
    return json.loads((RES / name).read_text())


def mean(x):
    return sum(x) / len(x)


def dot(ax, x, y, color, **kw):
    ax.plot(x, y, "o", color=color, markersize=8, markeredgecolor=SURFACE, markeredgewidth=2, **kw)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=160)
    plt.close(fig)
    print("wrote", name)


# 1. SLAM memory: SplaTAM composition over a sequence, LSG-SLAM front-end peak against map size
mp = load("splatam_memprof_room1.json")["rows"]
lsg = load("lsg_kitti07_frontend.json")["rows"]
fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.8))
f = [r["frame"] for r in mp]
kf = [r["keyframe_bytes"] / 2**30 for r in mp]
gs = [(r["param_bytes"] + r["variable_bytes"]) / 2**30 for r in mp]
alloc = [r["alloc"] / 2**30 for r in mp]
for y, c, lab in ((alloc, GRAY, "all allocated"), (kf, C[0], "keyframe images + depth"), (gs, C[1], "Gaussian params + tracked state")):
    a.plot(f, y, color=c, label=lab)
    a.annotate(f"{y[-1]:.2f} GiB", (f[-1], y[-1]), xytext=(4, 0), textcoords="offset points", va="center", color=TEXT2, fontsize=9)
a.set_title("SplaTAM, Replica room1: what fills GPU memory")
a.set_xlabel("frame")
a.set_ylabel("GiB (end of frame)")
a.set_xlim(0, 2250)
a.legend(loc="upper left")
g = [r["gaussians"] / 1e6 for r in lsg]
p = [r["peak_alloc_gib"] for r in lsg]
b.plot(g, p, color=C[0])
for i, (r, x, y) in enumerate(zip(lsg, g, p)):
    dot(b, x, y, C[0])
    b.annotate(f"{r['frames']} frames", (x, y), xytext=(-8, 10) if i % 2 else (6, -14), textcoords="offset points",
               ha="right" if i % 2 else "left", color=TEXT2, fontsize=9)
b.set_ylim(0, 8)
b.set_title("LSG-SLAM front end, KITTI 07: peak vs map size")
b.set_xlabel("Gaussians in one map (millions)")
b.set_ylabel("peak allocated (GiB)")
save(fig, "fig1_slam_memory.png")

# 2. Flow4DGS temporal storage: lossless and epsilon-merge baselines (three repeated seed-0 TUM runs)
names = [("dense", "dense"), ("fb1", "drop pre-birth"), ("fb2", "merge copies"), ("fb1_fb2", "both (lossless)"),
         ("fb3_eps5mm", "ε = 5 mm"), ("fb3_eps10mm", "ε = 10 mm"), ("fb3_eps20mm", "ε = 20 mm")]
runs = [load(f"flow4dgs/b1_posthoc_storage_r{i}.json")["results"] for i in (1, 2, 3)]
fig, ax = plt.subplots(figsize=(8, 4.2))
for i, (k, lab) in enumerate(names):
    mb = mean([r[k]["center_bytes"] / 2**20 for r in runs])
    dp = mean([r[k]["psnr"] - r["dense"]["psnr"] for r in runs])
    dot(ax, mb, dp, C[0] if i < 4 else C[1])
    positions = {"dense": (mb - 5, -0.045), "fb1": (mb, -0.065), "fb2": (285, 0.045),
                 "fb1_fb2": (215, 0.045), "fb3_eps5mm": (208, -0.080),
                 "fb3_eps10mm": (260, -0.145), "fb3_eps20mm": (260, -0.285)}
    ax.annotate(lab, (mb, dp), xytext=positions[k], color=TEXT2, fontsize=9,
                ha="center", arrowprops={"arrowstyle": "-", "color": GRID})
ax.plot([], [], "o", color=C[0], label="lossless (bit-identical renders)")
ax.plot([], [], "o", color=C[1], label="lossy ε-merge")
ax.legend(loc="lower right", fontsize=9)
ax.set_ylim(-0.36, 0.08)
ax.set_title("Flow4DGS-SLAM per-keyframe centre bank: storage vs quality")
ax.set_xlabel("modeled centre bank incl. Adam + indices (MiB, 3 seed-0 repeats)")
ax.set_ylabel("ΔPSNR vs dense (dB)")
save(fig, "fig2_flow4dgs_storage.png")

# 3. Taming 3DGS at 35 %: which part of the score matters (paired per cell, 4 scenes x 2 seeds)
arms = defaultdict(dict)
for c in load("taming_score_arms.json")["cells"]:
    arms[c["arm"]][(c["scene"], c["seed"])] = c["psnr"]
contrasts = [("Taming growth + trace pruning", "taming_grow_trace_prune", "taming", C[0]),
             ("trace pruning, with trace growth", "trace", "trace_grow_taming_prune", C[0]),
             ("trace growth, with Taming pruning", "trace_grow_taming_prune", "taming", C[1]),
             ("trace growth, with trace pruning", "trace", "taming_grow_trace_prune", C[1]),
             ("trace score alone vs Taming score", "trace", "taming", GRAY),
             ("vanilla gradient vs Taming score", "grad", "taming", GRAY),
             ("uniform (no score) vs Taming score", "uniform", "taming", GRAY)]
fig, ax = plt.subplots(figsize=(10.4, 5.5))
for i, (lab, a_, b_, col) in enumerate(contrasts):
    if set(arms[a_]) != set(arms[b_]) or len(arms[a_]) != 8:
        raise ValueError(f"Incomplete paired comparison: {a_}, {b_}")
    d = [arms[a_][k] - arms[b_][k] for k in sorted(arms[a_])]
    y = len(contrasts) - 1 - i
    ax.plot(d, [y] * len(d), "o", color=col, alpha=0.35, markersize=5, markeredgewidth=0)
    dot(ax, mean(d), y, col)
    ax.annotate(f"{mean(d):+.3f}", (mean(d), y), xytext=(0, 9), textcoords="offset points", ha="center", color=TEXT2, fontsize=9)
ax.axvline(0, color=GRAY, linewidth=1)
ax.set_yticks(range(len(contrasts)))
ax.set_yticklabels([c[0] for c in contrasts][::-1])
ax.set_xlabel("paired ΔPSNR, test views (dB); large dot = mean, small dots = 4 scenes × 2 seeds")
ax.set_title("Taming 3DGS at 35% retained budget: the score’s role matters", pad=28)
ax.set_ylim(-0.35, 6.65)
ax.axvline(0.10, color=GRAY, linewidth=1, linestyle="--")
ax.text(0.10, 1.01, "+0.10 dB adoption threshold", transform=ax.get_xaxis_transform(),
        ha="center", fontsize=8, color=TEXT2)
ax.plot([], [], "o", color=C[0], label="trace used for pruning")
ax.plot([], [], "o", color=C[1], label="trace used for growth")
ax.plot([], [], "o", color=GRAY, label="score controls")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.19), fontsize=8, ncol=3)
save(fig, "fig3_taming_roles.png")

# 4. Post-hoc pruning of finished Taming models: damage vs removed share, no fine-tuning
rows = load("posthoc_prune_rules.json")["rows"]
fig, ax = plt.subplots(figsize=(6.4, 3.9))
series = [("trace", "trace", C[0]), ("taming", "Taming score (all views)", C[1]), ("opacity", "opacity", C[2]), ("random", "random", C[3])]
for key, lab, col in series:
    xs, ys = [], []
    for share in (10, 20, 30):
        v = [r["dpsnr"] for r in rows if r["rule"] == f"{key}_low{share}%"]
        xs.append(share)
        ys.append(mean(v))
    ax.plot(xs, ys, color=col, label=lab)
    for x, y in zip(xs, ys):
        dot(ax, x, y, col)
    ax.annotate(lab, (xs[-1], ys[-1]), xytext=(8, 0), textcoords="offset points", va="center", color=TEXT2, fontsize=9)
ax.axhline(0, color=GRAY, linewidth=1)
ax.set_xticks([10, 20, 30])
ax.set_xticklabels(["10 %", "20 %", "30 %"])
ax.set_xlim(8, 38)
ax.set_xlabel("share of Gaussians removed")
ax.set_ylabel("mean ΔPSNR, test views (dB), 8 cells")
ax.set_title("Removing Gaussians from finished Taming models")
ax.legend(loc="lower left", fontsize=8)
save(fig, "fig4_posthoc_curves.png")

# 5. Gaussian-SLAM submap compression: same per-voxel quotas, colours frozen, 50 refinement iterations
gsr = [r for r in load("gslam_submap_compression.json")["rows"] if r["colour_fix"] and r["refine_iters"] == 50]
ref = {r["scene"]: r["psnr"] for r in gsr if r["selection"] == "none"}
arm_list = [("safe_final_voxel", "trace", C[0]), ("contrib_voxel", "contribution sum", C[1]),
            ("contribmax_voxel", "contribution max", "#7458a6"), ("hybrid_voxel", "hybrid rank", C[2]),
            ("opacity_voxel", "opacity", C[3]), ("random_voxel", "random", C[4])]
scenes = ["room0", "office0", "room1"]
fig, axes = plt.subplots(1, 2, figsize=(11.2, 5.1), sharey=False)
for ax, share in zip(axes, (0.25, 0.5)):
    present = [a for a in arm_list if any(r["selection"] == a[0] and r["nominal_share"] == share for r in gsr)]
    width = 0.78 / len(present)
    for j, (sel, lab, col) in enumerate(present):
        vals = []
        for scene in scenes:
            v = [r["psnr"] - ref[scene] for r in gsr
                 if r["scene"] == scene and r["selection"] == sel and r["nominal_share"] == share]
            if len(v) != 1:
                raise ValueError(f"Expected one corrected result: {scene}, {sel}, {share}")
            vals.append(v[0])
        x = np.arange(len(scenes)) + (j - (len(present) - 1) / 2) * width
        ax.bar(x, vals, width * 0.88, color=col, label=lab, linewidth=0)
    ax.axhline(0, color=GRAY, linewidth=1)
    ax.set_xticks(range(len(scenes)))
    ax.set_xticklabels(scenes)
    actual = "24.0–24.6%" if share == 0.25 else "49.3–49.7%"
    ax.set_title(f"{actual} removed (nominal {int(share * 100)}%)")
    ax.set_ylabel("ΔPSNR vs refine-only (dB)")
    ax.set_ylim(-1.7 if share == 0.25 else -2.8, 0.05)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), fontsize=8, ncol=2 if share == 0.25 else 1)
fig.suptitle("Gaussian-SLAM: score comparisons within equal 5 cm voxel quotas", fontweight="bold", fontsize=11)
fig.text(0.5, 0.025, "Offline · mapping views · 50 refinement iterations · colours frozen · different vertical scales", 
         ha="center", color=TEXT2, fontsize=9)
fig.tight_layout(rect=(0, 0.06, 1, 0.96))
fig.savefig(FIG / "fig5_gslam_compression.png", dpi=160)
plt.close(fig)
print("wrote", "fig5_gslam_compression.png")
