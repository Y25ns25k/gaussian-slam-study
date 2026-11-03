#!/usr/bin/env python3
"""Conceptual evidence map; annotations summarize retained diagnostic summaries."""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from plot_style import COLORS, export, heading

ROOT = Path(__file__).resolve().parents[1]


def main():
    fig, ax = plt.subplots(figsize=(13.5, 8))
    ax.set(xlim=(0, 13), ylim=(0, 8)); ax.axis('off')
    heading(fig, 'Transfer diagnostics: what is observed, and what remains open',
            'Decision rules constrain the interpretation; an unmet threshold does not establish a zero effect.',
            'Conceptual synthesis of retained transfer, tail and opacity-band summaries. '
            'Arrows show the reasoning path, not identified causal effects.')

    def box(x, y, w, h, title, body, dashed=False, fill='#F5F8FC'):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.12',
                     facecolor=fill, edgecolor=COLORS['trace'] if dashed else '#CCD5E1',
                     linewidth=1.5, linestyle='--' if dashed else '-'))
        ax.text(x+.15, y+h-.18, title, va='top', fontsize=12, weight='bold')
        ax.text(x+.15, y+h-.64, body, va='top', fontsize=11, linespacing=1.5)

    box(.2, 5.35, 5.8, 1.65, '1  Spatial / statistics-window diagnostics',
        'Isolation prediction unsupported; window rule mixed.\nRank correlation 0.92–0.94 weakens a simple window\nexplanation; it does not validate deletion quality.')
    box(.2, 3.25, 5.8, 1.65, '2  Remove the low-opacity tail first',
        'Random-relative advantage falls 36%, not the set 50%.\nOpacity-relative advantage increases. Tail removal also\nchanges the population, residuals and amount removed.')
    box(.2, 1.15, 5.8, 1.65, '3  Compare within opacity bands',
        'H mean +0.11 dB vs random: B1 mean rule met.\nL mean +0.72 dB: B2 +1.0 dB rule not met.\nSmall pooled H mean includes opposing scene effects.')
    box(7.0, 5.35, 5.7, 1.65, 'Observed composition difference',
        'Opacity ≥ 0.5: SLAM 82.2–84.9%, static 13.5–21.8%.\nAll 94 SLAM submaps; 8 static Taming models.\nAn operational split, not a material-opacity label.', fill='#EAF2FF')
    box(7.0, 2.3, 5.7, 2.1, 'Candidate explanation — not established',
        'Map composition may affect score usefulness.\nIts causal contribution is unresolved: protocols,\nspatial quotas and refinement also differ.\nB1 does not prove equivalence or no opaque-band gain.',
        dashed=True, fill='#F3F7FF')
    for start in [(6.15,6.15),(6.15,4.05),(6.15,1.95)]:
        ax.add_patch(FancyArrowPatch(start,(6.8,3.35),arrowstyle='->',
                     mutation_scale=14,color=COLORS['muted'],connectionstyle='arc3,rad=0.08'))
    ax.add_patch(FancyArrowPatch((9.85,5.15),(9.85,4.55),arrowstyle='->',
                 mutation_scale=14,color=COLORS['trace'],linestyle='--'))
    fig.subplots_adjust(left=.025,right=.99,bottom=.05,top=.88)
    export(fig, ROOT/'figures/fig14_diagnostic_flow')


if __name__ == '__main__': main()
