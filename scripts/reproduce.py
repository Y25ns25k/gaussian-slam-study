#!/usr/bin/env python3
"""Recompute retained metrics, run the CPU selector tests and regenerate all current figures.

Requires NumPy and Matplotlib. No Torch, GPU, models or dataset frames are required.
This does not rerun the original GPU experiments or refresh the publication manifest.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ['scripts/summarize_results.py'],
    ['scripts/summarize_followups.py'],
    ['scripts/summarize_online.py'],
    ['scripts/demo_selection.py'],
    ['-m', 'unittest', 'discover', '-s', 'tests'],
    ['scripts/make_figures.py'],
    ['scripts/make_implementation_figure.py', '--input', 'results/followups/slam_implementation.json',
     '--output', 'figures/fig6_implementation.png'],
    ['scripts/make_transfer_figures.py'],
    ['scripts/make_diagnostic_flow.py'],
    ['scripts/make_online_figure.py'],
]


def main():
    for command in COMMANDS:
        print('python ' + ' '.join(command), flush=True)
        subprocess.run([sys.executable, *command], cwd=ROOT, check=True)
    print('CPU recomputation, selector tests and current figure regeneration completed.')
    print('MANIFEST.sha256 identifies the published snapshot; rendering versions can affect regenerated figure bytes.')


if __name__ == '__main__':
    main()
