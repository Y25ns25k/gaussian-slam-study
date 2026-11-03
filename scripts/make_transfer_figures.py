#!/usr/bin/env python3
"""Figures 12-13: moving the trace score from static 3DGS to Gaussian-SLAM, and the opacity-composition diagnostics.

Reads results/posthoc_prune_rules.json, results/gslam_submap_compression.json and results/transfer/*.json.
CPU only (NumPy + Matplotlib).

    python scripts/make_transfer_figures.py
"""
import json
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt

from plot_style import COLORS, export, heading, mean_marker, style

ROOT = Path(__file__).resolve().parents[1]
RES, FIG = ROOT / 'results', ROOT / 'figures'
SCENES_STATIC = ('bonsai', 'kitchen', 'room', 'train')
SCENES_SLAM = ('room0', 'office0', 'room1')


def load(name):
    return json.loads((RES / name).read_text())


def transfer_curves():
    post = load('posthoc_prune_rules.json')['rows']
    rows = [r for r in load('gslam_submap_compression.json')['rows'] if r['colour_fix'] and r['refine_iters'] == 50]
    ref = {r['scene']: r['psnr'] for r in rows if r['selection'] == 'none'}
    fig, (a, b) = plt.subplots(1, 2, figsize=(13.5, 5.6))
    heading(fig, 'Moving trace from static 3DGS to Gaussian-SLAM',
            'Same score family, different maps and protocols: read each panel against its own reference.',
            'A: 8 finished Taming models (4 scenes × 2 seeds), global lowest-score removal, no fine-tuning, test views. '
            'B: 3 Replica scenes, one source run each, equal quota per 5 cm voxel,\n50 refinement steps with colours frozen, '
            'mapping cameras; nominal 25 % / 50 % = actual 24.0–24.6 % / 49.3–49.7 %. Opacity, random and contribution-max '
            'were not run at 50 %.')
    for key, label, color in (('trace', 'Trace', COLORS['trace']), ('taming', 'Taming score (all views)', COLORS['taming']),
                              ('opacity', 'Opacity', COLORS['opacity']), ('random', 'Random', COLORS['random'])):
        xs, ys = (10, 20, 30), [mean(r['dpsnr'] for r in post if r['rule'] == f'{key}_low{s}%') for s in (10, 20, 30)]
        a.plot(xs, ys, color=color, marker='o', label=label)
        a.annotate(f'{ys[-1]:+.2f}', (30, ys[-1]), xytext=(8, 0), textcoords='offset points', va='center',
                   color=COLORS['muted'], fontsize=10)
    a.set(title='A  Static 3DGS: removal from finished models', xlabel='Gaussians removed (%)',
          ylabel='Mean ΔPSNR vs unpruned model (dB)', xticks=(10, 20, 30), xlim=(7, 35))
    a.axhline(0, color=COLORS['muted'], lw=1)
    a.legend(loc='lower left')
    style(a, 'y')
    arms = (('safe_final_voxel', 'Trace', COLORS['trace']), ('contrib_voxel', 'Contribution sum', COLORS['contrib']),
            ('contribmax_voxel', 'Contribution max', COLORS['contribmax']), ('opacity_voxel', 'Opacity', COLORS['opacity']),
            ('random_voxel', 'Random', COLORS['random']))
    for i, (sel, label, color) in enumerate(arms):
        pts = {}
        for share in (0.25, 0.5):
            v = [r['psnr'] - ref[r['scene']] for r in rows if r['selection'] == sel and r['nominal_share'] == share]
            if len(v) == 3:
                pts[share] = v
        xs = [25 * (1 + (s == 0.5)) + (i - 2) * 0.5 for s in pts]
        b.plot(xs, [mean(v) for v in pts.values()], color=color, marker='o', label=label)
        for x, v in zip(xs, pts.values()):
            b.scatter([x] * 3, v, color=color, s=14, alpha=.45, zorder=3)
    b.set(title='B  Gaussian-SLAM: per-voxel quotas on saved submaps', xlabel='Nominal Gaussians removed (%)',
          ylabel='ΔPSNR vs refine-only (dB); line = mean of 3 scenes', xticks=(25, 50), xlim=(18, 57))
    b.axhline(0, color=COLORS['muted'], lw=1)
    b.legend(loc='lower left')
    style(b, 'y')
    fig.tight_layout(rect=(0, .08, 1, .9))
    export(fig, FIG / 'fig12_static_vs_slam')


def opacity_diagnostics():
    comp = load('transfer/opacity_composition.json')
    band = load('transfer/opacity_band_test.json')['grad']
    fig, (a, b) = plt.subplots(1, 2, figsize=(14.5, 5.4), gridspec_kw=dict(width_ratios=(1, 1.15)))
    heading(fig, 'Opacity composition and band-specific trace effects',
            'Composition differs; band-H effects vary across scenes. A small pooled mean does not establish equivalence.',
            'A: static = 2 seeds per scene averaged (Taming arm); SLAM = all submaps of one source run per scene '
            '(40 / 28 / 26). Gaussian-SLAM deletes opacity < 0.1 while mapping.\nB: 8 grad-arm models, 20 % of each band '
            'removed without fine-tuning, test views; positive favours trace. Band H removes 2.7–4.3 % of a map, band L '
            '10.3–12.6 %. Lines: pre-set thresholds B1 (≤ 0.25) and B2 (≥ 1.0).')
    labels, parts = [], []
    for s in SCENES_STATIC:
        m = [v for k, v in comp['static'].items() if k.startswith(s + '_')]
        labels.append(f'{s} · static')
        parts.append([mean(x[k] for x in m) for k in ('below_0_1', 'band_0_1_0_5', 'at_or_above_0_5')])
    for s in SCENES_SLAM:
        v = comp['slam'][s]
        labels.append(f'{s} · SLAM')
        parts.append([v['below_0_1'], v['band_0_1_0_5'], v['at_or_above_0_5']])
    left = [0.0] * len(parts)
    for j, (name, color) in enumerate((('opacity < 0.1', '#D6DCE5'), ('0.1–0.5 (band L)', COLORS['trace_light']),
                                       ('≥ 0.5 (band H)', COLORS['trace']))):
        vals = [100 * p[j] for p in parts]
        a.barh(range(len(parts)), vals, left=left, color=color, label=name, height=.62, edgecolor='white', linewidth=1.2)
        for i, (x0, w) in enumerate(zip(left, vals)):
            if w >= 7:
                a.text(x0 + w / 2, i, f'{w:.0f}', ha='center', va='center', fontsize=10,
                       color='white' if j == 2 else COLORS['ink'])
        left = [x + w for x, w in zip(left, vals)]
    a.set_yticks(range(len(parts)), labels)
    a.invert_yaxis()
    a.set(title='A  Opacity composition of the maps', xlabel='Share of Gaussians (%)', xlim=(0, 100))
    a.legend(loc='upper center', bbox_to_anchor=(.5, -.2), ncol=3, fontsize=10)
    style(a, 'x')
    for row, (bk, name) in enumerate((('L', 'Band L: 0.1–0.5'), ('H', 'Band H: ≥ 0.5'))):
        for col, (x, label, color) in enumerate((('random', 'vs random', COLORS['random']),
                                                 ('opacity', 'vs opacity', COLORS['opacity']))):
            y = row * 2.4 + col
            vals = [r[f'{bk}_{x}'] for r in band.values()]
            for scene, marker in zip(SCENES_STATIC, ('o', 's', '^', 'v')):
                scene_vals = [r[f'{bk}_{x}'] for k, r in band.items() if k.startswith('grad_' + scene + '_')]
                b.scatter(scene_vals, [y] * len(scene_vals), color=color, marker=marker, s=40, alpha=.8, zorder=3, edgecolors='white', linewidth=.5)
            mean_marker(b, mean(vals), y)
            b.annotate(f'{mean(vals):+.2f}', (mean(vals), y), xytext=(0, 9), textcoords='offset points', ha='center',
                       fontsize=10, color=COLORS['ink'])
    b.set_yticks([0, 1, 2.4, 3.4], ['Band L · vs random', 'Band L · vs opacity', 'Band H · vs random', 'Band H · vs opacity'])
    b.axvline(0, color=COLORS['muted'], lw=1)
    b.axvline(1.0, color=COLORS['trace'], lw=1, ls='--')
    b.axvline(0.25, color=COLORS['muted'], lw=1, ls=':')
    b.set_ylim(3.9, -1.0)
    b.text(1.02, -.7, 'B2 ≥ 1.0', color=COLORS['trace'], fontsize=10, ha='left')
    b.text(0.27, 1.8, 'B1 ≤ 0.25 (band H)', color=COLORS['muted'], fontsize=10, ha='left')
    b.set(title='B  Trace gain within each opacity band', xlabel='Trace − control PSNR (dB); point = model')
    from matplotlib.lines import Line2D
    b.legend(handles=[Line2D([], [], color=COLORS['opacity'], marker=m, ls='', label=s)
                      for s, m in zip(SCENES_STATIC, ('o', 's', '^', 'v'))],
             loc='upper center', bbox_to_anchor=(.5, -.2), ncol=4, fontsize=9)
    style(b, 'x')
    fig.tight_layout(rect=(0, .08, 1, .9))
    export(fig, FIG / 'fig13_opacity_hypothesis')


if __name__ == '__main__':
    transfer_curves()
    opacity_diagnostics()
