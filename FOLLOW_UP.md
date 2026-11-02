# Detailed comparisons and validation

[Integrated report](REPORT.md) · [Figure index](figures/README.md) · [Data guide](results/README.md)

This supplement retains all runs and guard outcomes behind the report. Expand only the tables needed for a
particular comparison. Experiments with different seeds, growth rules, driver environments or references are not
pooled. Percentages are time changes, not FLOP reductions. The original plans/logs remain local; this snapshot
does not establish independent preregistration.

## 1. Match actual turnover before attributing a quality gain

**Question / control.** Can trace improve deletion ranking when growth and actual deletions at each event are
matched? Two scenes × two seeds × two scores; eight retained 30k conditions. A common threshold relaxation
addresses growth candidate shortages; one prior bonsai pair is reused only after proving it never needs that fallback.

**Result / decision.** Mean ΔPSNR +0.074060 dB, 4/4 positive pairs, mean ΔLPIPS
-0.000682. The fixed +0.10 dB mean gate fails; the original confound is not retroactively removed.
The other gates require ≥3/4 positive pairs, positive means in both scenes, mean LPIPS ≤+0.002 and correctness.

<details>
<summary>All four paired outcomes</summary>

| Scene | Seed | ΔPSNR | ΔLPIPS | Final count | Actual deletions |
|---|---|---|---|---|---|
| bonsai | 1 | +0.017662 | -0.001179 | 374265 | 46108 |
| bonsai | 2 | +0.011770 | -0.000067 | 374265 | 55382 |
| kitchen | 1 | +0.099193 | -0.000459 | 559773 | 12613 |
| kitchen | 2 | +0.167614 | -0.001022 | 559773 | 12523 |

</details>


Source: [matched_turnover.json](results/followups/matched_turnover.json). Figure: [Fig. 8](figures/fig8_trace_controls.png).

## 2. A small improvement still has to face the gradient control

**Question / control.** One fixed soft-trace candidate, five deletion scores on two existing scenes at fresh seed 3.
Common growth and historical Taming seed-1 actual-deletion schedule. All ten 30k conditions finish; no historical
metrics are pooled into the fresh screen. The gradient control changes deletion only.

**Result / decision.** Soft trace gains +0.074007 dB over trace, with LPIPS
+0.000440, but is -0.103738 dB behind gradient.
Advancement requires positive mean PSNR and mean LPIPS ≤+0.002 against each Taming/gradient/random control.
Neither trace candidate passes; seed 4 is not run and the offset is not retuned. One bonsai view explains much
of the gain over Taming; per-view and view-exclusion diagnostics remain in the source JSON, without replacing the primary result.

<details>
<summary>All ten fresh runs</summary>

| Scene | Score | PSNR | SSIM | LPIPS | Count |
|---|---|---|---|---|---|
| bonsai | taming | 32.049934 | 0.936011 | 0.219312 | 374265 |
| bonsai | trace | 32.215322 | 0.937951 | 0.217772 | 374265 |
| bonsai | trace_soft | 32.278292 | 0.937927 | 0.218215 | 374265 |
| bonsai | gradient | 32.376847 | 0.937832 | 0.218182 | 374265 |
| bonsai | random | 32.173672 | 0.936759 | 0.219053 | 374265 |
| kitchen | taming | 31.189571 | 0.923714 | 0.136682 | 559773 |
| kitchen | trace | 31.305134 | 0.924146 | 0.136061 | 559773 |
| kitchen | trace_soft | 31.390178 | 0.924157 | 0.136499 | 559773 |
| kitchen | gradient | 31.499099 | 0.924235 | 0.136041 | 559773 |
| kitchen | random | 31.361892 | 0.924250 | 0.136244 | 559773 |

</details>


Source: [trace_development.json](results/followups/trace_development.json). Figure: [Fig. 8](figures/fig8_trace_controls.png).

## 3. Render-free scoring does not mean zero collection cost

**Control.** Nine saved sources, five timing repeats after one warmup; 12 native on/off runs from two 100-frame
GT-pose prefixes × three seeds. Same 5 cm quotas, frozen colours, 50 optimizer steps. Contribution uses a colour-
only autograd pass; this is a local implementation, not an official full-method or specialized-kernel comparison.

**Result / decision.** Resident trace is 7.89% / 8.23% faster than contribution-sum/max. Collection-inclusive
cost versus contribution-sum is +6.593% / +0.809% in room0 / office0. The original
implementation does not establish a net advantage. Its selector consumes roughly 55% of closing time.

<details>
<summary>Earlier-run resident-compression times</summary>

| Score | Mean of map medians [s] |
|---|---|
| Trace | 2.733793 |
| Contribution sum | 2.967867 |
| Contribution max | 2.978972 |
| Opacity | 2.797455 |
| Random | 2.708970 |

</details>


Source: [slam_score_cost.json](results/followups/slam_score_cost.json). Figure: [Fig. 7](figures/fig7_original_cost.png).

## 4. Optimize the same computation before changing the method

**Control.** Every-step collection, original score formula, CPU float32 voxel assignment, per-voxel quotas,
index tie breaking, colour freeze and refinement work stay fixed. The selector optimization is also applied to
contribution and opacity. Fresh original implementations are rerun; earlier absolute timings are not reused.

**Validation.** Dense buffers are bitwise equal on 63 real gradient packets and 96 edge cases. Both selector
backends match 45 real masks; a further 26 GPU edge cases pass. Deferred CPU oracles verify 264 masks in frozen
runs outside the timers. Equal masks do not guarantee bitwise CUDA refinement or independently evolved maps.
The Triton candidate fails exactness and is rejected. The first profiler attempt is excluded after correcting
its shape proxy allocation; only corrected v2 timing selects one global backend.

**Result / decision.** Resident trace is 57.44% faster than fresh original trace and 14.49% / 14.17%
faster than equally optimized contribution-sum/max. Collection-inclusive cost against contribution-sum is
-0.374% / -0.046%, with only 3/6 pairs lower.
All 12 fixed-source guards pass. One of 24 direct prefix comparisons fails PSNR: office0 seed 1 vs contribution-max,
−0.101133 dB against a −0.10 dB guard. The failure is retained. Guards are descriptive tolerances, not equivalence tests.

<details>
<summary>Six implementations: complete-stage timing totals</summary>

| Implementation | Sum of 9 map medians [s] | Mean per map [s] | Optimized trace change |
|---|---|---|---|
| Trace / original | 20.850468 | 2.316719 | -57.44% |
| Trace / optimized | 8.874015 | 0.986002 | +0.00% |
| Contribution sum / original | 22.268848 | 2.474316 | -60.15% |
| Contribution sum / optimized | 10.377644 | 1.153072 | -14.49% |
| Contribution max / optimized | 10.338910 | 1.148768 | -14.17% |
| Opacity / optimized | 8.772671 | 0.974741 | +1.16% |

</details>


<details>
<summary>All 18 fresh native mapping runs</summary>

| Scene | Seed | Statistics | Native wall [s] | Gaussians | Optimizer steps |
|---|---|---|---|---|---|
| room0 | 0 | Dense | 118.5327 | 2423066 | 4900 |
| room0 | 0 | Original | 122.4650 | 2422963 | 4900 |
| room0 | 0 | Off | 117.7135 | 2423396 | 4900 |
| room0 | 1 | Original | 121.8361 | 2423274 | 4900 |
| room0 | 1 | Off | 117.9359 | 2422874 | 4900 |
| room0 | 1 | Dense | 118.3731 | 2423052 | 4900 |
| room0 | 2 | Off | 120.2828 | 2424158 | 4900 |
| room0 | 2 | Dense | 118.4384 | 2423925 | 4900 |
| room0 | 2 | Original | 120.1100 | 2423638 | 4900 |
| office0 | 0 | Off | 85.4484 | 1577367 | 3000 |
| office0 | 0 | Original | 85.7819 | 1577486 | 3000 |
| office0 | 0 | Dense | 84.1449 | 1577432 | 3000 |
| office0 | 1 | Original | 86.0596 | 1576864 | 3000 |
| office0 | 1 | Dense | 85.5930 | 1577347 | 3000 |
| office0 | 1 | Off | 83.0302 | 1577054 | 3000 |
| office0 | 2 | Dense | 84.6834 | 1577951 | 3000 |
| office0 | 2 | Off | 85.0758 | 1578128 | 3000 |
| office0 | 2 | Original | 85.2365 | 1578279 | 3000 |

</details>


<details>
<summary>All six seed-level totals against optimized contribution-sum</summary>

| Scene | Seed | Optimized trace [s] | Optimized contribution sum [s] | Trace change |
|---|---|---|---|---|
| room0 | 0 | 122.5591 | 122.0055 | +0.454% |
| room0 | 1 | 122.4033 | 122.2915 | +0.091% |
| room0 | 2 | 122.5383 | 124.6144 | -1.666% |
| office0 | 0 | 86.3608 | 88.0636 | -1.934% |
| office0 | 1 | 87.8029 | 85.4804 | +2.717% |
| office0 | 2 | 86.8040 | 87.6116 | -0.922% |

</details>


<details>
<summary>Scene-mean total-cost changes against every reference</summary>

| Scene | Reference | Mean paired change |
|---|---|---|
| room0 | Trace / original | -4.6736% |
| room0 | Contribution sum / optimized | -0.3736% |
| room0 | Contribution max / optimized | -0.3260% |
| room0 | Opacity / optimized | -0.0574% |
| office0 | Trace / original | -3.5652% |
| office0 | Contribution sum / optimized | -0.0461% |
| office0 | Contribution max / optimized | +0.0497% |
| office0 | Opacity / optimized | +0.3582% |

</details>


<details>
<summary>All 12 fixed-source quality comparisons</summary>

| Scene | Reference | ΔPSNR [dB] | ΔLPIPS | Δdepth [mm] | All guards |
|---|---|---|---|---|---|
| room0 | Trace / original | -0.000188 | +0.000000 | +0.000025 | True |
| room0 | Contribution sum / optimized | +0.038643 | -0.001383 | +0.069389 | True |
| room0 | Contribution max / optimized | +0.029880 | -0.001429 | +0.079738 | True |
| room0 | Opacity / optimized | +0.524743 | -0.001268 | -0.142058 | True |
| office0 | Trace / original | -0.000114 | +0.000002 | +0.000049 | True |
| office0 | Contribution sum / optimized | +0.014078 | -0.000673 | -0.032069 | True |
| office0 | Contribution max / optimized | +0.003998 | -0.000689 | -0.020254 | True |
| office0 | Opacity / optimized | +0.995319 | -0.003601 | -0.295791 | True |
| room1 | Trace / original | -0.000143 | +0.000007 | -0.000028 | True |
| room1 | Contribution sum / optimized | +0.046209 | -0.000878 | +0.030928 | True |
| room1 | Contribution max / optimized | +0.029063 | -0.000851 | +0.038177 | True |
| room1 | Opacity / optimized | +0.405874 | -0.001928 | -0.098562 | True |

</details>


<details>
<summary>All 24 direct prefix quality comparisons</summary>

| Scene | Seed | Reference | ΔPSNR | ΔLPIPS | Δdepth mm | Pass |
|---|---|---|---|---|---|---|
| room0 | 0 | Trace / original | +0.014331 | -0.000128 | -0.000305 | True |
| room0 | 0 | Contribution sum / optimized | +0.044049 | -0.001547 | +0.029522 | True |
| room0 | 0 | Contribution max / optimized | +0.024450 | -0.001457 | +0.035597 | True |
| room0 | 0 | Opacity / optimized | +0.431007 | -0.000537 | -0.099248 | True |
| room0 | 1 | Trace / original | -0.004938 | +0.000191 | +0.003317 | True |
| room0 | 1 | Contribution sum / optimized | +0.071316 | -0.001680 | +0.020724 | True |
| room0 | 1 | Contribution max / optimized | +0.054360 | -0.001693 | +0.027414 | True |
| room0 | 1 | Opacity / optimized | +0.436182 | -0.000727 | -0.099604 | True |
| room0 | 2 | Trace / original | +0.004533 | +0.000061 | -0.004226 | True |
| room0 | 2 | Contribution sum / optimized | +0.050302 | -0.001589 | +0.019075 | True |
| room0 | 2 | Contribution max / optimized | +0.040351 | -0.001539 | +0.024733 | True |
| room0 | 2 | Opacity / optimized | +0.449845 | -0.000616 | -0.103580 | True |
| office0 | 0 | Trace / original | +0.004999 | -0.000073 | -0.175120 | True |
| office0 | 0 | Contribution sum / optimized | -0.058389 | -0.000904 | -0.294722 | True |
| office0 | 0 | Contribution max / optimized | -0.073337 | -0.000924 | -0.262696 | True |
| office0 | 0 | Opacity / optimized | +0.706169 | -0.004334 | -0.488300 | True |
| office0 | 1 | Trace / original | +0.011021 | -0.000073 | -0.442037 | True |
| office0 | 1 | Contribution sum / optimized | -0.084609 | -0.000493 | -0.195233 | True |
| office0 | 1 | Contribution max / optimized | -0.101133 | -0.000539 | -0.168619 | False |
| office0 | 1 | Opacity / optimized | +0.714943 | -0.003542 | -0.429485 | True |
| office0 | 2 | Trace / original | +0.008643 | +0.000049 | -0.183229 | True |
| office0 | 2 | Contribution sum / optimized | +0.006064 | -0.001030 | -0.034831 | True |
| office0 | 2 | Contribution max / optimized | -0.009731 | -0.001050 | -0.012408 | True |
| office0 | 2 | Opacity / optimized | +0.795170 | -0.003783 | -0.186973 | True |

</details>


The cost sum is native mapping wall + common load/prepare + score/select/restore/prune/refine. It includes native
checkpoint I/O and excludes deferred validation, compression evaluation, compressed-output serialization and
process import. This is not pure GPU compute, complete CLI wall time or online SLAM FPS.

Per-case timing repeats, allocator peaks, accumulator bytes, per-view metrics and refine-only-relative prefix
quality differences remain in [slam_implementation.json](results/followups/slam_implementation.json). Compression
peak allocated memory across the nine cases is 1126.50 → 1127.64 MiB; no VRAM saving is claimed.

Figures: [stage times](figures/fig6_implementation.png), [phase breakdown](figures/fig10_phase_breakdown.png),
[collection](figures/fig11_collection_overhead.png), [total-cost comparison](figures/fig9_total_cost.png).
