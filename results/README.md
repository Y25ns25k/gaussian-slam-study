# Evidence and data guide

These files are curated metric extracts from completed, stopped, and failed experiments. They support numerical
recomputation at the resolution stored here, not re-execution of the underlying experiments. All paths below are
relative to this directory. `python scripts/summarize_results.py` prints the headline comparisons from the
repository root. The plotting commands in [README.md](../README.md) regenerate the PNG/SVG figure pairs listed in the figure index;
[the figure index](../figures/README.md) maps each plot to its question, reference and aggregation.
Dated follow-ups and independently runnable helpers are described below.

## Claim-to-file map

| Claim or figure | File and selection | Scope |
|---|---|---|
| Flow4DGS execution improvement | `flow4dgs/memory_options.json`, `arm=options_off/on` | Three seed-0 repetitions per configuration; off-runs fail in refinement; on-runs have final metrics. Profiled peaks are allocated bytes / 2³⁰. |
| 44.8% temporal centre-bank saving; Fig. 2 | `flow4dgs/b1_posthoc_storage_r{1,2,3}.json`, `dense` vs `fb1_fb2` | `1 − mean(compressed bytes)/mean(dense bytes)`; Adam moments and index overhead included. Render equality is recorded, not rechecked from images. |
| Keyframe-density comparison | `flow4dgs/b1_kf_split.json`, `conditions.*.after.never_keyframe` | Same 223 frames that are keyframes in none of the compared runs; selection excludes keyframes, not necessarily every training use. |
| Flow4DGS density/OOM history | `flow4dgs/b1_aggregate.json` | `1.99x` is the approximately 2× condition. `ate_mean_cm` is historical mean error, not RMSE. `null` is unavailable, not zero. |
| Growth/pruning score effects; Fig. 3 | `taming_score_arms.json`, pair by `(scene, seed)` | Four scenes × seeds 1 and 2; only compare arms with the common alignment fixes. |
| Static budget table | `static_3dgs_reference.json` plus seed 1 from `taming_score_arms.json` | Four-scene means; code bases differ. PUP time excludes the source training. |
| Finished-model deletion; Fig. 4 | `posthoc_prune_rules.json`, rules `{trace,taming,opacity,random}_low{10,20,30}%` | Test-view deltas against the same unpruned model, eight pairs, no fine-tuning. |
| SplaTAM composition; Fig. 1A | `splatam_memprof_room1.json`, `rows` | Samples every 50 frames plus final frame 1999; recorded tensor bytes and allocated memory at those snapshots. Not a complete peak-memory decomposition. |
| LSG-SLAM peak vs count; Fig. 1B | `lsg_kitti07_frontend.json`, `rows` | Front end, KITTI 07 prefixes with stride 2; no loop closure/back end. ATE here is recomputed RMSE. |
| Voxel compression; Fig. 5 | `gslam_submap_compression.json`, `colour_fix=true`, `refine_iters=50` | Subtract same-scene `selection=none`. Mapping views, source trajectory fixed, one source run per scene. |
| Room0 checkpoint saving | `gslam_storage_summary.json` | Rounded retained measurements, 4.939 → 3.755 GiB, after the colour-freeze fix. Not VRAM or an exact byte audit. |

## Fields and comparison rules

- PSNR/dPSNR: dB, larger is better. SSIM: larger is better. LPIPS and depth L1: smaller is better.
  `dpsnr`, `dssim`, `dlpips` are differences from the same unpruned model in the post-hoc table.
- GiB = bytes / 2³⁰; MiB = bytes / 2²⁰. Do not combine allocated, reserved, modeled-storage, and checkpoint measures.
- Static `35%` means a retained-count budget relative to vanilla; compression `nominal_share` means removed share.
  `removed` is the realized fraction. Voxel methods round each voxel's quota down.
- Taming arms: `taming` uses Taming for both roles; `trace` uses trace for both;
  `taming_grow_trace_prune` and `trace_grow_taming_prune` swap one role; `grad` and `uniform` change both roles.
  `taming_trace` is a separate arm, not an alias for either crossed arm.
- `taming_upstream_20261018` lacks the shared fixes. Its two run labels both used actual seed 0; they must not be
  treated as two independent seeds or silently mixed into Fig. 3.
- Gaussian-SLAM `safe_final_voxel` means trace ranking within voxels. `contrib_voxel` sums blending contributions
  over views; `contribmax_voxel` takes the per-view maximum; `hybrid_voxel` averages trace/contribution percentile
  ranks. `*_voxcap` changes the allocation policy and is not a matched-quota score comparison.
- Exclude `colour_fix=false` from compression losses against refine-only: those arms also trained colours.
  At 200/500 refinement iterations, use the control with the same iteration count. Historical `selection=none`
  may carry nominal share 0.25 even though `removed=0`; it is still the no-prune control.
- Opacity/random/max-contribution rows are not available at every removal budget. Their absence is not zero loss
  or an unreported tie. Fig. 5 displays the available corrected arms only.

## What this release cannot independently establish

The public tables do not contain the full original run logs, per-view arrays, render images, source trajectories,
protocol commit history, local implementation patches, or complete configurations. In particular, the following
report observations remain supported by the author's retained study notes rather than public raw records:

- the initial paper-reproduction table, camera-memory growth diagnosis, and porting details;
- the 36/114 vanilla gate-noise check, early within-policy random comparisons, and replacement-count/turnover logs;
- keyframe-placement and tracking-diagnostic results, including AUROC and iteration-cap analyses;
- the sampled empty-voxel diagnosis, SplaTAM timing regression, and most exact checkpoint sizes;
- the timing of pre-specified decision rules and pixel-level bit-identical rendering checks.

Later follow-up exports do include their retained per-view numeric arrays and timing repetitions; this does not
restore the missing original-study images, logs or protocol history.

The memory-options extract contains source filenames and SHA256 hashes for traceability. Those files are not
bundled, so the hashes alone are not public verification. The room0 storage summary is explicitly transcribed
from rounded notes. Some large artifacts were deleted; their absence cannot be repaired by aggregate tables.

## Release corrections

- Historical non-standard JSON `NaN` values became `null`; finite measured values were preserved.
- Historical Flow4DGS `ate_cm` keys became `ate_mean_cm`, including the corresponding aggregate keys. These old
  values were not converted to RMSE; newer `memory_options.json` uses `stats_final.json` RMSE explicitly.
- Memory-options peak bytes give 9.11–9.53 GiB. This supersedes the old draft's 9.3–9.8 GiB wording.

## Transfer diagnostics (November 3, 2026)

Summaries of the three tests in [REPORT.md §5](../REPORT.md#5-spatial-constraints-and-unresolved-transfer-diagnostics). Plans and decision scripts
were committed in the study repository before the full runs; the first two plans followed earlier smoke runs.
Per-model raw outputs are not bundled. This is not a claim that every rule predated any execution.

| File | Scope |
|---|---|
| `transfer/transfer_diagnostic.json` | 8 static Taming models (post-hoc trace) and 94 Gaussian-SLAM submaps (room0 40, office0 28, room1 26; stored and post-hoc trace). Per static model and per-scene medians over submaps: low-quarter opacity, isolation (no other centre within 3 × max scale among 16 neighbours, 50,000 sampled Gaussians), emptied-cell ratios E25/E50, Spearman correlations; `verdict` R1–R4. |
| `transfer/tail_removal_test.json` | 8 static models: full map vs opacity < 0.1 deleted first; 10 / 20 % removal by trace, opacity, random without fine-tuning; test views; `verdict` C1–C3 and the descriptive opacity ≥ 0.5 candidate test. |
| `transfer/opacity_band_test.json` | 8 grad-arm models (rules) and 8 Taming models (reference): 20 % of band L (0.1–0.5) or band H (≥ 0.5) removed by each score; `verdict` B1–B2. B1 is a threshold on the mean, not an equivalence test. |
| `transfer/opacity_composition.json` | Opacity shares (< 0.1, 0.1–0.5, ≥ 0.5) and 20-bin histograms for the 8 static Taming models and all Gaussian-SLAM submaps. |

The tail export's historical `verdict.reading="rejected"` and the band export's
`verdict.reading="opaque part only"` are superseded interpretations, retained for source fidelity.
Use the numerical outcomes and REPORT §5: the tail has a partial effect and band H does not establish equivalence.
The diagnostic rank helper did not average tied ranks, so its reported correlations are rank diagnostics rather
than an exact tie-corrected Spearman calculation. Earlier spot checks found small differences; this release does
not recompute them without the unbundled per-point inputs.

## Dated follow-up records (October 28–November 2, 2026)

See [FOLLOW_UP.md](../FOLLOW_UP.md) for the sequence and differing controls.

| File | Scope |
|---|---|
| `followups/matched_turnover.json` | Eight retained 30k conditions, two scenes × two seeds, same actual deletion schedule; common growth fallback amendment. |
| `followups/trace_development.json` | Ten fresh seed-3 conditions, trace/soft-trace/Taming/gradient/random; per-view metrics and stopped extension decision. |
| `followups/slam_score_cost.json` | Nine saved maps × five timing repeats and twelve actual GT-pose mapping runs; original implementation. |
| `followups/slam_implementation.json` | Nine saved maps × five repeats; eighteen fresh off/original/dense mapping runs and their closing records; same-input selector checks. |
| `followups/provenance.json` | SHA256 of each bundled export and helper; separate hashes identify retained local source records, which are not bundled. |

The cost/implementation exports retain timing repetitions, per-phase summaries, counts, mapping-view metrics,
native optimizer-call records and seed-level compute sums. Source checkpoint hashes identify retained inputs;
they do not allow re-rendering without those files. `timing_records` contains the measured repetitions;
`median`/`minimum`/`maximum` summarize each phase independently, so summing phase medians need not equal the
median of complete closing time. Headline closing comparisons use the latter. Scene quality means weight views
equally across that scene's three selected submaps. Timing totals sum map-level medians; prefix headline changes
average the three seed-level percentage changes within each scene.

Follow-up exports omit machine paths, upstream code, model/data payloads and unselected metadata. Exported
numeric fields are unchanged. `scripts/summarize_followups.py` checks bundled hashes, recomputes the timing
medians, quality means and accounting sums, and prints the comparisons. The public-file hash checks the actual
bundled bytes; a retained-private-source hash refers to different, unbundled bytes. Neither proves that a plan
predated an experiment. GPU parity remains a recorded local result, whereas the included CPU selection tests
are independently runnable from this artifact.

## Derived presentation data

`figure_data.json` is a new derived export, not a new experiment. `scripts/figure_data.py` rebuilds it from the
original JSON and records each source SHA256. It retains the plotted paired points, complete-stage medians,
phase means, scene/seed references and missing-budget controls. No original measured JSON is edited to redraw
the figures. Timing differences are ratios within each experiment; earlier absolute timings are not reused as
the optimized run's references. Full paired points are shown where retained; no plotted uncertainty interval
is presented as a new-scene or statistical-equivalence result.

## Exact online 25% budget comparison

`online_budget25.json` contains the new two-seed, 51-frame KITTI07 score ablation.
It retains per-view RGB/depth metrics under estimated and aligned-GT cameras, event-level births/deletions/counts,
frontend process wall times and allocated/reserved peaks. [ONLINE_COMPARISON.md](../ONLINE_COMPARISON.md) defines
the common count reference, replayed births, adapted quota policy and timing boundary. Source-model hashes identify
retained private models, which are not bundled. Depth is IGEV pseudo-depth; views are observed, not held out.
These numbers are separate from the saved-map Replica comparisons and older unequal-count Pocket runs.

## Local external-system comparisons

`local_system_comparisons.json` retains all eight already-completed Replica room0 500-frame configurations,
including both weaker ten-submap matched-count trials and the later one-map adaptations. It includes both
estimated-camera and aligned-GT-camera quality, GNU total wall and separately named parent-polled time,
map counts, payload sizes and adaptation descriptions. Its source-summary hash identifies an unbundled private
record. The export omits machine paths and full per-view arrays; it is an aggregate numeric extract.
See [LOCAL_SYSTEM_COMPARISONS.md](../LOCAL_SYSTEM_COMPARISONS.md) for the scope and camera-dependent ordering.

`online_renderer_validation.json` preserves the three-view native/common renderer agreement check on area seed 0,
with the original mean-error threshold and both mean/max errors. It does not establish bitwise parity or all-model
agreement. `online_figure_data.json` binds Fig. 15 to its input hash. The online arithmetic helper verifies the
event counts, quality means and paired differences without re-rendering models.
