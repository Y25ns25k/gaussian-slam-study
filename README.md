# SAGE-4D: When does removing Gaussians help Gaussian SLAM?

**Resource profiling, controlled pruning experiments, and same-result implementation optimization on a 16 GB GPU.**

This undergraduate research and engineering portfolio follows one question: does a cheaper Gaussian map improve
what actually limits a SLAM system? It covers four SLAM implementations, a static-3DGS score study, memory fixes,
and comparisons against stronger pruning controls. Its strongest results are measured engineering changes and
experiments that narrow the original hypothesis.

By [Y25ns25k](https://github.com/Y25ns25k). Latest follow-up: November 2, 2026.

**[Full report (§1–10)](REPORT.md)** · **[Follow-up results](FOLLOW_UP.md)** · **[Evidence guide](results/README.md)** · **[Runnable helpers](code/README.md)**

## Five findings

1. **Profiling improved execution feasibility.** In Flow4DGS-SLAM on TUM walking_xyz at approximately 2× keyframe
   density, three runs failed during refinement; three runs with memory options completed at **9.11–9.53 GiB**
   profiled peak allocated memory. The changes remove unread buffers, unnecessary optimizer copies and a frontend
   leak. Quality equivalence at this density is unconfirmed, with a pre-refinement degradation signal.
   [Run records](results/flow4dgs/memory_options.json) · [Report §3](REPORT.md#3-flow4dgs-slam-where-the-memory-goes-and-what-can-be-cut-exactly)

2. **Exact redundancy is a useful storage baseline.** Removing invisible slots and merging unchanged temporal
   centres reduces **modeled centre-bank storage by 44.8%**, including Adam moments and indexing overhead.
   Three seed-0 repeats recorded matching renders. This is a storage model, not measured runtime VRAM reduction;
   the original parity images are unavailable, and online use needs flow-loss slots and copy-on-write handling.
   [Records](results/flow4dgs/b1_posthoc_storage_r1.json) · [Report §3](REPORT.md#3-flow4dgs-slam-where-the-memory-goes-and-what-can-be-cut-exactly)

3. **A small score gain needs stronger controls.** Taming-growth/trace-pruning originally gained **+0.056 dB**
   against Taming, with greater actual turnover. After matching deletion counts, a smaller two-scene/two-seed
   comparison retained **+0.074 dB**, below the fixed +0.10 dB gate. A fresh soft-trace candidate gained another
   +0.074 dB over trace but remained **0.104 dB behind gradient** in the two-scene seed-3 screen. The extension
   stopped. These are separate experiments with different growth/control conditions.
   [Matched turnover](results/followups/matched_turnover.json) · [Fresh controls](results/followups/trace_development.json)

4. **Spatial quotas make saved-map compression viable at modest removal.** On three Replica scenes, offline
   trace pruning within 5 cm voxels removes **24.0–24.6%** of Gaussians, with **0.19–0.27 dB** loss against
   refine-only after 50 colour-frozen refinement steps. Room0 checkpoints shrink **24.0%**, including optimizer
   state. Contribution scores are within 0.06 dB at this removal level and are better at approximately 50% removal.
   Mapping views and copied source poses do not establish held-out quality or tracking preservation.
   [Compression records](results/gslam_submap_compression.json) · [Storage measurement](results/gslam_storage_summary.json)

5. **The same computation can be implemented more efficiently.** Dense gradient accumulation and stable packed-key
   voxel sorting preserve the tested statistics and same-input removal masks. On nine saved submaps, optimized
   trace closing changes by **-57.4% versus original trace** and **-14.5% versus equally optimized
   contribution-sum**. These closing times exclude earlier collection. Including short mapping prefixes and
   compression, mean paired trace cost changes versus optimized contribution-sum are **-0.37%
   in room0 / -0.05% in office0** (three seeds each; positive means more cost).
   Trace costs less in 3/6 scene–seed pairs; these small means do not establish a robust total-cost advantage.
   This is selected cost accounting, not online SLAM FPS. [All timings, quality and controls](FOLLOW_UP.md#4-optimize-the-same-computation-before-changing-the-method)

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
