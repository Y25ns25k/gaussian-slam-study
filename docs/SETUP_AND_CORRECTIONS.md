# Setup and evaluation corrections

## Environment and starting points

One RTX 5070 Ti (16 GB, sm_120), Windows/WSL2, CUDA 12.8 and PyTorch 2.11 were used for the GPU experiments.
Static experiments use Mip-NeRF 360 kitchen/room/bonsai and Tanks & Temples train. SLAM experiments use TUM
fr3/walking_xyz, Bonn balloon, Replica room0/room1/office0 and KITTI07. CPU regeneration has separate versions
recorded in [release_verification.json](../results/release_verification.json).

Upstream commits identify starting points, not complete rerunnable experiment versions. Local configurations,
integration patches, weights, input data and large model artifacts are not bundled.

| system | upstream | local changes |
|---|---|---|
| Flow4DGS-SLAM (wangys16/Flow4DGS-SLAM) | `ecb4e94` | sm_120 / WSL port; opt-in profiling, memory options, tracking log |
| Taming 3DGS (humansensinglab/taming-3dgs) | `fd0f7d9` | one-line `<cfloat>` build fix; opt-in score modes; pruning-weight alignment after split |
| PUP 3D-GS (j-alex-hanson/gaussian-splatting-pup) | `e971ea4` | CUDA 12.8 build fixes |
| SplaTAM (spla-tam/SplaTAM) | `da6bbcd` | read-only per-frame memory/time profile |
| Gaussian-SLAM (VladimirYugay/Gaussian-SLAM) | `eaec10d` | passive trace statistics in checkpoints; offline voxel-stratified pruning tool |
| LSG-SLAM (lsg-slam/LSG-SLAM) | `2b8cfdb` | KITTI 07 config; parser paths |

The newer online and local-system comparisons identify their exact released branches and scopes in
[ONLINE_COMPARISON.md](ONLINE_COMPARISON.md), [LOCAL_SYSTEM_COMPARISONS.md](LOCAL_SYSTEM_COMPARISONS.md) and
[THIRD_PARTY.md](../THIRD_PARTY.md). They are distinct from the original saved-map experiments.

## Evaluation corrections

Each of these was found by a check or review. Corrected comparisons are used in the current report; historical confounded rows
remain in the JSON and are explicitly excluded from the main analyses.

- **Release baseline arithmetic.** The seed-1 table gives 29.570231 − 28.764565 ≈ 0.806 dB for Taming versus the hard-cap
  policy. The earlier 0.76 dB wording did not match this table; the comparison now reports 0.81 dB.
- **Release memory units.** The original draft reported 9.3–9.8 GiB for the optimized 2× runs. Direct extraction
  from the retained profiler byte records gives 9.11–9.53 GiB, now used here. This is profiler allocated memory,
  not total device memory. The release also renames historical Flow4DGS `ate_cm` to `ate_mean_cm` and represents
  unavailable/OOM metrics as JSON `null`; those old ATE values are not RMSE.

- **Flow4DGS's `ATE_0.json`.** It stores a mean error, not an RMSE. Corrected RMSE and retained historical
  `ate_mean_cm` fields are explicitly distinguished; mean errors in the public historical tables were not converted.
- **LSG-SLAM's printed "ATE RMSE".** It is a mean, computed on world-to-camera translations instead of camera
  centres. We recomputed it, and withdrew an earlier claim that long single maps "collapse".
- **Gaussian-SLAM pruning tool.** Re-creating the parameters re-enabled colour learning in pruned arms only. After the
  fix:
  - the 25 % loss went from −0.095 to −0.216 dB;
  - checkpoint savings went from 12 % to 24 % (optimizer state for colours is no longer saved).
- **Post-hoc Taming score.** It was first computed on 10 sampled views, so Gaussians unseen in those views scored zero.
  It was recomputed on all training views; this amendment is documented.
- **Early 3DGS summary.** A count of 7/34 gate failures was wrong; the correct count is 36/114.
- **Two arithmetic and wording errors** in intermediate notes:
  - "+0.72 dB" should have been +1.20 dB;
  - a depth advantage held in 2 of 3 scenes, not 3 of 3.

## Evidence boundaries

Historical confounded rows remain in the metric JSON and are excluded by the documented filters. Some original
checkpoints and renders were deleted; tables cannot restore pixel-level parity checks or unbundled diagnostics.
The public package supports CPU arithmetic, selection tests and figure regeneration, not full GPU experiment reruns.

This is a post-experiment record. The timing of locally specified rules is author-reported; the publication commit
does not establish pre-experiment registration. See [the data guide](../results/README.md) for retained fields and gaps.
The earlier full narrative remains available in [Git history](https://github.com/Y25ns25k/gaussian-slam-study/blob/bdf2c2eef05ee146279a52b5a0ae3bed467f2844/ARCHIVE_REPORT.md).
