# Gaussian SLAM: Resource Profiling and Compression Optimization

**Resource profiling, controlled pruning experiments, and verified compression optimizations for Gaussian SLAM on a 16 GB GPU.**

This project investigates resource bottlenecks and map-compression costs in Gaussian SLAM. It profiles Gaussian
state, keyframe data and checkpoint storage separately across Flow4DGS-SLAM, SplaTAM, Gaussian-SLAM and the
LSG-SLAM front end, and compares a sensitivity score accumulated from training gradients with other pruning scores.

Controlled experiments separate score quality from allocation and replacement effects. Static 3DGS follow-ups
match actual deletion counts; offline Gaussian-SLAM comparisons use matched spatial quotas and refinement work.
Gradient and contribution controls remain visible alongside small gains and failed decision rules.

The implementation follow-up optimizes statistics accumulation and per-voxel selection. On nine saved submaps,
mean compression-stage time falls from **2.32 s to 0.99 s**, a **57.4% reduction** versus the original trace
implementation. These means average five-repeat timing medians per submap. The optimized selector passes
**264 same-input mask checks** against the original selector. Compression is also **14.5% faster** than
contribution-sum using the same selector optimization.

These compression-stage timings exclude earlier statistics collection. Including collection in short GT-pose
mapping runs and subsequent compression produces small, seed-dependent differences; a robust total-cost advantage
is not established. The results concern offline compression and short mapping prefixes, without an online
tracking or full-system throughput claim.

The repository provides reports, measured metrics, figure scripts, independent numerical helpers and CPU examples.
It supports numerical reanalysis and standalone examples; the upstream integrations, complete configurations,
datasets and models needed for full training or SLAM reruns are outside this release.

By [Y25ns25k](https://github.com/Y25ns25k). Latest experiment: November 2, 2026. Public write-up updated November 3, 2026.

**[Full report (§1–10)](REPORT.md)** · **[Follow-up results](FOLLOW_UP.md)** · **[Evidence guide](results/README.md)** · **[Runnable helpers](code/README.md)**

## Five findings

| Finding | Measured result and scope | Evidence |
|---|---|---|
| **Resource bottlenecks differ.** | In the sampled SplaTAM room1 run, final keyframe images/depth take **1.38 GiB**, versus **0.12 GiB** of Gaussian parameters and tracked state. LSG-SLAM measurements cover its front end only. | [Report §5](REPORT.md#5-slam-is-the-gaussian-count-ever-the-bottleneck) |
| **Memory engineering improves execution feasibility.** | At approximately 2× keyframe density, **3/3 Flow4DGS runs fail** during refinement and **3/3 with memory options complete**, at **9.11–9.53 GiB** profiled peak allocated memory. Quality equivalence is unconfirmed. | [Run records](results/flow4dgs/memory_options.json) |
| **Compression needs matched controls.** | On three Replica scenes, per-voxel trace pruning removes **24.0–24.6%** of Gaussians with **0.19–0.27 dB** loss against refine-only after 50 colour-frozen refinement steps. Room0 checkpoints shrink **24.0%**. Strong contribution controls are within 0.06 dB at this removal level. | [Compression records](results/gslam_submap_compression.json) · [Storage](results/gslam_storage_summary.json) |
| **The tested selection results can be computed faster.** | Compression-stage time changes by **-57.4%** versus original trace and **-14.5%** versus equally optimized contribution-sum, with **264 same-input mask checks** passing. Earlier collection is excluded from these stage times. | [Implementation results](FOLLOW_UP.md#4-optimize-the-same-computation-before-changing-the-method) |
| **The public artifact is runnable on a CPU.** | Stored-metric summaries, a selection example, independent oracle tests and seven regenerated figures are provided. The documented seven CPU commands passed without Torch. Full upstream reruns are outside the package. | [Code guide](code/README.md) · [Verification](results/release_verification.json) |

The static score study retains its negative controls: a matched-turnover trace gain of **+0.074 dB** misses the
fixed +0.10 dB gate. A separate fresh soft-trace screen gains +0.074 dB over trace but remains **0.104 dB behind
gradient** in PSNR. These experiments use different controls and are not pooled. See [the follow-up](FOLLOW_UP.md).

With mapping and collection included, mean paired cost changes against optimized contribution-sum are
**-0.37% in room0 / -0.05% in office0**
(three seeds each; positive means more cost). Trace costs less in **3/6** scene–seed pairs;
the sign varies. [All timings and quality results](FOLLOW_UP.md#4-optimize-the-same-computation-before-changing-the-method)

<p align="center">
  <img src="figures/fig1_slam_memory.png" width="95%" alt="Sampled SplaTAM memory composition and LSG-SLAM frontend memory versus Gaussian count"><br>
  <em>Choose the resource first: keyframe data can outweigh Gaussian state. These are system-specific probes,
  not comparable full-system peak measurements.</em>
</p>

<p align="center">
  <img src="figures/fig6_implementation.png" width="100%" alt="Original and optimized closing costs, fresh mapping runs and mapping-plus-compression accounting"><br>
  <em>Time collection and selection separately, and give the same selector improvement to competing scores.
  Nine fixed-source submaps; two 100-frame GT-pose prefixes × three seeds.</em>
</p>

## What you can run

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

The summaries use Python's standard library; the example/tests use NumPy; plots additionally use Matplotlib.
All commands above run on a CPU without Torch, a dataset or model weights. Optional PyTorch/CUDA helpers and
input contracts are documented in [code/README.md](code/README.md).

| Path | What it provides |
|---|---|
| [REPORT.md](REPORT.md) | Original questions, experiments, evaluation repairs and limitations (§1–10) |
| [FOLLOW_UP.md](FOLLOW_UP.md) | Matched-turnover, stronger gradient controls, collection cost and implementation results |
| [results/](results/) | Curated measured metrics, follow-up timing repetitions/per-view metrics, and explicit evidence gaps |
| [code/](code/) and [tests/](tests/) | Independent quota selection and dense accumulation helpers; a CPU oracle test |
| [scripts/](scripts/) and [figures/](figures/) | Recompute stored summaries and regenerate seven charts |
| [THIRD_PARTY.md](THIRD_PARTY.md), [LICENSE](LICENSE) | Redistribution boundary and MIT / CC BY 4.0 scope |
| [PUBLICATION.md](PUBLICATION.md) | Prepared artifact scope and local verification details |
| [PORTFOLIO.md](PORTFOLIO.md) | Concise Korean and English portfolio descriptions |

This release supports **numerical reanalysis, figure regeneration and a standalone selection example**.
It does not support a full training/SLAM rerun: upstream systems, local integration patches, complete configs,
datasets, models and renders are not bundled. Public export hashes and retained private-source hashes are
separate in [provenance](results/followups/provenance.json).

## Scope and limitations

- One RTX 5070 Ti (16 GB), WSL2. The original static study uses four scenes × two seeds; follow-up quality screens
  use two existing scenes. Cost runs add three seeds on two short GT-pose prefixes, not a broad SLAM benchmark.
- Offline compression is evaluated on **mapping views**. No online tracking, held-out-view quality, full-system
  throughput gain or new state-of-the-art pruning algorithm is established.
- Trace needs no extra scoring render when reusing training gradients, but its accumulator, updates and selection
  have costs. The same-result checks include 264 deferred original-mask comparisons; CUDA refinement and
  source-map evolution are not claimed bit-identical. Fixed-source quality guards pass 12/12 comparisons;
  guards are descriptive tolerances, not equivalence tests. See every delta in [FOLLOW_UP.md](FOLLOW_UP.md).
- Original decision rules, amendments, unsuccessful candidates and evidence gaps remain visible. Public metric
  tables and hashes alone do not independently prove protocol timing or repair deleted raw artifacts.

The related [sensitivity-guided-3dgs](https://github.com/Y25ns25k/sensitivity-guided-3dgs) project concerns static
3DGS budget control. It has different benchmarks and controls; this report's small score gains and SLAM timings
must not be presented as improvements to that repository's results.

## AI assistance and license

Claude Code (Anthropic) and Codex (OpenAI) assisted with implementation, experiment execution, design review,
result checking and drafting. Claims refer to recorded experiments within their stated scope.

Code in `scripts/`, `code/` and `tests/`: MIT. Original text, figures and result tables: CC BY 4.0.
See [LICENSE](LICENSE) and [THIRD_PARTY.md](THIRD_PARTY.md).
