# Local system comparisons: exploratory context

These are already-completed runs, separate from the new exact-budget online score experiment. Code was available and executed for both VCGS and MemGS. VCGS denotes its released SplaTAM mask/RVQ version, not a full-paper reproduction.

Replica room0 first 500 frames, RTX 5070 Ti, one run per condition, 48 observed evaluation views. No held-out evaluation. Every matched-count adaptation is shown, including the weak ten-submap conditions.

| Configuration | Gaussians | Wall(s) | Estimated-camera PSNR↑ | LPIPS↓ | Aligned-GT-camera PSNR↑ | ATE(cm)↓ |
|---|---:|---:|---:|---:|---:|---:|
| Gaussian-SLAM + trace, default | 6,233,433 | 1101.84 | 31.254 | 0.07241 | 28.614 | 0.1448 |
| VCGS released SplaTAM branch | 1,658,168 | 3284.22 | 37.261 | 0.04854 | 24.598 | 0.2438 |
| MemGS | 26,751 | 19.65 | 30.511 | 0.20527 | 29.482 | 0.3540 |
| Gaussian-SLAM, default | 8,206,864 | 1091.50 | 30.952 | 0.07134 | 27.725 | 0.2684 |
| Trace · 10 submaps · MemGS budget | 26,751 | 819.82 | 16.827 | 0.51254 | 16.598 | 1.8192 |
| Trace · 10 submaps · VCGS budget | 1,658,168 | 868.47 | 28.122 | 0.13406 | 26.504 | 0.1602 |
| Trace · one map · MemGS budget | 26,751 | 700.01 | 32.597 | 0.20234 | 27.388 | 0.2880 |
| Trace · one map · VCGS budget (α=0.6) | 1,658,168 | 1249.71 | 39.495 | 0.03085 | 29.240 | 0.1989 |

## What the comparisons can establish

- `total_wall_seconds` is GNU process wall through fresh tracking/mapping, trace collection, final compression/refinement/export. Installation/build and shared evaluation are excluded. Parent-polled process time is retained under a different field and can differ; do not mix the two time bases.
- Final-count matching is exact in the four adapted trace runs. It does not match active map size, insertion policy, optimizer iterations, tracking algorithm or representation capacity. MemGS uses higher-order spherical harmonics; trace uses SH0.
- The ten-submap adaptations use a lifetime insertion budget 1.6× target, split 70% initially/30% later, and proportional quotas without a per-voxel minimum. The later one-map adaptations preserve one survivor per occupied voxel when feasible; the VCGS-sized condition uses insertion alpha 0.6. These exploratory changes followed earlier results.
- One-map results improve strongly over the ten-submap configurations, but no otherwise identical trace-off control was run. Attribute neither gain nor loss to trace alone.
- MemGS is much faster here. Its mapper performed 1,381 iterations; the trace one-map conditions used 11,000 plus iterative rendering-based camera optimization. The logged MemGS merge removed only 35 points (35,764→35,729) once; it does not explain the whole system speed gap.
- Estimated-camera PSNR can reflect adaptation to a system’s own trajectory. At the MemGS point budget, trace scores 32.597 versus 30.511 dB there, but 27.388 versus 29.482 dB with aligned GT cameras: the ordering reverses. Neither metric alone establishes geometry or generalization.
- Float payloads, optimizer checkpoints and native compressed bitstreams are different quantities. The retained numeric export labels their scopes; decoded float NPZ size is not a VCGS index-coded bitstream.
- These are local systems/settings, not paper-level rankings. They do not prove zero-cost compression or real-time trace SLAM. The new [exact-budget online comparison](ONLINE_COMPARISON.md) asks a narrower score question.

[Numeric extract](../results/local_system_comparisons.json) · [Main report](../REPORT.md)
