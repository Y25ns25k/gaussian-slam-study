# Gaussian SLAM: Resource Profiling and Compression Optimization

**A study of where Gaussian reduction helps, which controls change the conclusion, and what implementation work improves.**

[Read the report](REPORT.md) · [한국어 요약](SUMMARY_KO.md) · [All figures / SVG](figures/README.md) · [Detailed comparisons](FOLLOW_UP.md) · [Run the CPU example](code/README.md)

The starting idea was to reuse training gradients for a cheap sensitivity score. Resource profiling and stronger
controls narrowed that hypothesis. The clearest implementation result is **57.4% shorter compression-stage
time** on nine saved submaps, from **2.32 s to 0.99 s**, with tested same-input removal masks preserved.

Earlier statistics collection is excluded from that stage time. With mapping and collection included, differences
against optimized contribution scoring are small and change sign across seeds. The report follows both results
through the same research flow, with fixed references, sample counts and measurement boundaries beside each figure.

## Research flow and decisions

| Question | Observation | Decision |
|---|---|---|
| Resource target | Keyframes can dominate Gaussian state. | Profile runtime memory and saved-map storage separately. |
| Score quality | Matched turnover: +0.074 dB; soft trace vs gradient: -0.104 dB. | No general trace-ranking advantage established. |
| Offline compression | 24.0–24.6% fewer Gaussians; 0.19–0.27 dB PSNR loss. | Useful modest-removal trade-off on mapping views. |
| Implementation | 2.32 → 0.99 s per submap; 57.4% shorter. | Same-score optimization passes 264 same-input mask checks. |
| Collection-inclusive cost | room0 -0.37%; office0 -0.05%. | Seed signs vary; no robust total-cost advantage established. |

## Result 1: the compression implementation improves

![Nine fixed submaps · mean of five-repeat map-level timing medians · one warmup excluded. Includes scoring, selection, restore/prune and 50 refinement steps; excludes earlier collection, loading, evaluation and output serialization. Both score families receive the same selector optimization.](figures/fig6_implementation.png)

*Nine fixed submaps · mean of five-repeat map-level timing medians · one warmup excluded. Includes scoring, selection, restore/prune and 50 refinement steps; excludes earlier collection, loading, evaluation and output serialization. Both score families receive the same selector optimization.*


## Result 2: the whole-workload advantage is unconfirmed

![Each circle is one scene–seed pair; black diamonds are scene means. Negative values favour trace. The selected cost sum includes GT-pose mapping, collection, native checkpoint I/O, common loading and offline compression. It is not online SLAM FPS. The marked contribution-max comparison misses the PSNR guard.](figures/fig9_total_cost.png)

*Each circle is one scene–seed pair; black diamonds are scene means. Negative values favour trace. The selected cost sum includes GT-pose mapping, collection, native checkpoint I/O, common loading and offline compression. It is not online SLAM FPS. The marked contribution-max comparison misses the PSNR guard.*


## Read or reproduce

| Path | Purpose |
|---|---|
| [REPORT.md](REPORT.md) | Integrated question → control → observation → decision narrative, §1–10 |
| [SUMMARY_KO.md](SUMMARY_KO.md) | Korean overview of the research flow and measured claims |
| [FOLLOW_UP.md](FOLLOW_UP.md) | Full seed tables, quality guards and implementation checks in expandable sections |
| [figures/README.md](figures/README.md) | Twelve figures, each with PNG, scalable SVG, reference and source data |
| [results/README.md](results/README.md) | Numeric evidence, exclusions and preservation gaps |
| [ARCHIVE_REPORT.md](ARCHIVE_REPORT.md) | Corrected earlier report, retained for the original diagnostics and setup history |
| [PORTFOLIO.md](PORTFOLIO.md) | Concise Korean and English portfolio descriptions |

```bash
python scripts/summarize_results.py
python scripts/summarize_followups.py
python -m pip install -r requirements.txt
python scripts/demo_selection.py
python -m unittest discover -s tests
python scripts/make_figures.py
python scripts/make_cost_figure.py --input results/followups/slam_score_cost.json --output figures/fig7_original_cost.png
python scripts/make_implementation_figure.py --input results/followups/slam_implementation.json --output figures/fig6_implementation.png
```

After dependency installation, the seven verification commands run on a CPU without Torch, dataset frames or model weights. The plotting
commands regenerate twelve PNG/SVG pairs; [figure_data.json](results/figure_data.json) records the values and input
hashes used. [Verification](results/release_verification.json) checks the public commands, not a new GPU rerun.

## Scope and limitations

- One RTX 5070 Ti (16 GB), WSL2. Original static controls use four scenes × two seeds; matched-turnover/fresh-score
  follow-ups reuse two scenes. Final cost tests use two 100-frame GT-pose prefixes × three seeds.
- Gaussian-SLAM pruning is **offline** and evaluated on **mapping views**. Copied poses do not validate tracking.
  Held-out quality, online compression latency, full-system throughput and new-scene generalization remain untested.
- Flow4DGS memory options improve completion at the tested density; quality equivalence is unconfirmed.
- Same-input buffer/mask checks do not imply bit-identical CUDA refinement or independent mapping trajectories.
  All 12 fixed-source quality comparisons pass their guards; 1/24 direct prefix comparisons fails a PSNR guard.
- This release supports numeric reanalysis, figure regeneration and standalone numerical examples. Full upstream
  integrations, complete configs, datasets and models are not bundled. [Evidence gaps](results/README.md) remain explicit.

The separate [sensitivity-guided-3dgs](https://github.com/Y25ns25k/sensitivity-guided-3dgs) repository studies static
Gaussian budget control under different benchmarks; these results must not be pooled with its results.

## AI assistance and license

Claude Code (Anthropic) and Codex (OpenAI) assisted with implementation, execution, review and drafting. The report
and figures identify the measured evidence and its scope. This presentation revision adds no GPU experiments.

By [Y25ns25k](https://github.com/Y25ns25k). Experiments through November 2, 2026; presentation revised November 3, 2026.
Code: MIT. Original documentation, figures and metric tables: CC BY 4.0. See [LICENSE](LICENSE) and [THIRD_PARTY.md](THIRD_PARTY.md).
