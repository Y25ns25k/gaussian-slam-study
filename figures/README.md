# Figure index

Numeric plots are generated from retained JSON; Figs. 0 and 14 are conceptual syntheses. PNGs are for reading in GitHub; SVGs preserve scalable text and geometry.
The chart values and input SHA256 hashes of Fig. 1–11 are in [figure_data.json](../results/figure_data.json); Fig. 12–13 are drawn by `scripts/make_transfer_figures.py` from `results/posthoc_prune_rules.json`, `results/gslam_submap_compression.json` and `results/transfer/`.

| Figure | Question / aggregation | PNG | SVG | Read in context |
|---|---|---|---|---|
| Fig. 0 | Research question and decision map of the earlier (v1.1.0) narrative — Conceptual synthesis; no numeric aggregation; not used in the current report | [PNG](fig0_research_flow.png) | [SVG](fig0_research_flow.svg) | [Report](../REPORT.md#1-question-and-the-score) |
| Fig. 1 | Resource diagnosis — SplaTAM snapshots; separate LSG front-end prefixes | [PNG](fig1_slam_memory.png) | [SVG](fig1_slam_memory.svg) | [Report](../REPORT.md#3-moving-trace-to-gaussian-slam) |
| Fig. 2 | Temporal storage vs quality — Three repeated seed-0 runs; mean bank bytes / paired PSNR | [PNG](fig2_flow4dgs_storage.png) | [SVG](fig2_flow4dgs_storage.svg) | [Report](../REPORT.md#7-engineering-results-outside-the-score-question) |
| Fig. 3 | Separate growth and deletion — Four scenes × two seeds; all paired deltas and means | [PNG](fig3_taming_roles.png) | [SVG](fig3_taming_roles.svg) | [Report](../REPORT.md#2-static-3dgs-what-trace-does) |
| Fig. 4 | Removal-budget comparison — Eight finished models; no fine-tuning | [PNG](fig4_posthoc_curves.png) | [SVG](fig4_posthoc_curves.svg) | [Report](../REPORT.md#2-static-3dgs-what-trace-does) |
| Fig. 5 | Coverage and score comparison — Same quotas / reference / scale; missing arms explicitly unmeasured | [PNG](fig5_gslam_compression.png) | [SVG](fig5_gslam_compression.svg) | [Report](../REPORT.md#3-moving-trace-to-gaussian-slam) |
| Fig. 6 | Complete compression-stage timing — Mean of nine five-repeat map-level medians; earlier collection excluded | [PNG](fig6_implementation.png) | [SVG](fig6_implementation.svg) | [Report](../REPORT.md#6-cost-and-implementation) |
| Fig. 7 | Original cost boundary screen — Earlier-run reference only; resident stage vs wider accounting | [PNG](fig7_original_cost.png) | [SVG](fig7_original_cost.svg) | [Report](../REPORT.md#6-cost-and-implementation) |
| Fig. 8 | Matched turnover and fresh controls — Separate policies / seeds / references; do not pool | [PNG](fig8_trace_controls.png) | [SVG](fig8_trace_controls.svg) | [Report](../REPORT.md#2-static-3dgs-what-trace-does) |
| Fig. 9 | Collection-inclusive comparison — All six seed pairs vs two optimized controls; means of percentages | [PNG](fig9_total_cost.png) | [SVG](fig9_total_cost.svg) | [Report](../REPORT.md#6-cost-and-implementation) |
| Fig. 10 | Where the implementation time changes — Separate phase medians; not a constructed closing median | [PNG](fig10_phase_breakdown.png) | [SVG](fig10_phase_breakdown.svg) | [Report](../REPORT.md#6-cost-and-implementation) |
| Fig. 11 | Mapping cost of statistics — 18 fresh runs; all differences vs paired statistics-off source | [PNG](fig11_collection_overhead.png) | [SVG](fig11_collection_overhead.svg) | [Report](../REPORT.md#6-cost-and-implementation) |
| Fig. 12 | Static 3DGS vs Gaussian-SLAM removal–quality — A: 8 finished models, global removal, test views; B: 3 scenes, per-voxel quotas, refine-only reference, mapping cameras | [PNG](fig12_static_vs_slam.png) | [SVG](fig12_static_vs_slam.svg) | [Report](../REPORT.md#3-moving-trace-to-gaussian-slam) |
| Fig. 13 | Opacity composition and band test — A: all maps; B: 8 grad-arm models, per-model gains and pre-set thresholds; causal link is a hypothesis | [PNG](fig13_opacity_hypothesis.png) | [SVG](fig13_opacity_hypothesis.svg) | [Report](../REPORT.md#5-spatial-constraints-and-unresolved-transfer-diagnostics) |

| Fig. 14 | Diagnostic outcomes and unresolved causal explanation — Conceptual evidence map; dashed box is a hypothesis | [PNG](fig14_diagnostic_flow.png) | [SVG](fig14_diagnostic_flow.svg) | [Report](../REPORT.md#5-spatial-constraints-and-unresolved-transfer-diagnostics) |

| Fig. 15 | Exact-budget online comparison — Every primary seed/arm; full-image quality and aligned ATE vs frontend process wall | [PNG](fig15_online_budget25.png) | [SVG](fig15_online_budget25.svg) | [Online comparison](../ONLINE_COMPARISON.md) |

Diamonds represent descriptive means, not confidence intervals. Seed dots are retained; scenes and seeds are not interchangeable independent samples.
The common method colours identify trace (blue), contribution (orange), Taming/hybrid (teal) and gradient (purple).
Plots that colour resource, score-role or implementation roles instead of scores label those roles explicitly. Every plot states units and the sign of its effect.

Regeneration commands are in [README.md](../README.md). The transfer revision adds Figs. 12–14. The separate online appendix documents newly executed GPU runs; those runs are not pooled into the historical figures.
