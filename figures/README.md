# Figure index

Numeric plots are generated from retained JSON; Fig. 0 is a conceptual synthesis. PNGs are for reading in GitHub; SVGs preserve scalable text and geometry.
The chart values and input SHA256 hashes are in [figure_data.json](../results/figure_data.json).

| Figure | Question / aggregation | PNG | SVG | Read in context |
|---|---|---|---|---|
| Fig. 0 | Research question and decision map — Conceptual synthesis; no numeric aggregation | [PNG](fig0_research_flow.png) | [SVG](fig0_research_flow.svg) | [Report](../REPORT.md#1-research-question-and-experiment-map) |
| Fig. 1 | Resource diagnosis — SplaTAM snapshots; separate LSG front-end prefixes | [PNG](fig1_slam_memory.png) | [SVG](fig1_slam_memory.svg) | [Report](../REPORT.md#2-find-the-resource-bottleneck) |
| Fig. 2 | Temporal storage vs quality — Three repeated seed-0 runs; mean bank bytes / paired PSNR | [PNG](fig2_flow4dgs_storage.png) | [SVG](fig2_flow4dgs_storage.svg) | [Report](../REPORT.md#2-find-the-resource-bottleneck) |
| Fig. 3 | Separate growth and deletion — Four scenes × two seeds; all paired deltas and means | [PNG](fig3_taming_roles.png) | [SVG](fig3_taming_roles.svg) | [Report](../REPORT.md#3-separate-ranking-quality-from-growth-and-turnover) |
| Fig. 4 | Removal-budget comparison — Eight finished models; no fine-tuning | [PNG](fig4_posthoc_curves.png) | [SVG](fig4_posthoc_curves.svg) | [Report](../REPORT.md#4-test-the-removal-budget-on-finished-models) |
| Fig. 5 | Coverage and score comparison — Same quotas / reference / scale; missing arms explicitly unmeasured | [PNG](fig5_gslam_compression.png) | [SVG](fig5_gslam_compression.svg) | [Report](../REPORT.md#5-preserve-coverage-when-compressing-slam-submaps) |
| Fig. 6 | Complete compression-stage timing — Mean of nine five-repeat map-level medians; earlier collection excluded | [PNG](fig6_implementation.png) | [SVG](fig6_implementation.svg) | [Report](../REPORT.md#7-optimize-the-same-computation-and-validate-it) |
| Fig. 7 | Original cost boundary screen — Earlier-run reference only; resident stage vs wider accounting | [PNG](fig7_original_cost.png) | [SVG](fig7_original_cost.svg) | [Report](../REPORT.md#6-measure-the-cost-boundary-before-optimizing) |
| Fig. 8 | Matched turnover and fresh controls — Separate policies / seeds / references; do not pool | [PNG](fig8_trace_controls.png) | [SVG](fig8_trace_controls.svg) | [Report](../REPORT.md#3-separate-ranking-quality-from-growth-and-turnover) |
| Fig. 9 | Collection-inclusive comparison — All six seed pairs vs two optimized controls; means of percentages | [PNG](fig9_total_cost.png) | [SVG](fig9_total_cost.svg) | [Report](../REPORT.md#8-retest-collection-inclusive-cost-and-quality) |
| Fig. 10 | Where the implementation time changes — Separate phase medians; not a constructed closing median | [PNG](fig10_phase_breakdown.png) | [SVG](fig10_phase_breakdown.svg) | [Report](../REPORT.md#7-optimize-the-same-computation-and-validate-it) |
| Fig. 11 | Mapping cost of statistics — 18 fresh runs; all differences vs paired statistics-off source | [PNG](fig11_collection_overhead.png) | [SVG](fig11_collection_overhead.svg) | [Report](../REPORT.md#8-retest-collection-inclusive-cost-and-quality) |

Diamonds represent descriptive means, not confidence intervals. Seed dots are retained; scenes and seeds are not interchangeable independent samples.
The common method colours identify trace (blue), contribution (orange), Taming/hybrid (teal) and gradient (purple).
Plots that colour resource, score-role or implementation roles instead of scores label those roles explicitly. Every plot states units and the sign of its effect.

Regeneration commands are in [README.md](../README.md). This revision redraws existing evidence; it adds no training runs.
