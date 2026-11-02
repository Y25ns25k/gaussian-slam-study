# Public research artifact

Repository: [Y25ns25k/gaussian-slam-study](https://github.com/Y25ns25k/gaussian-slam-study), branch `main`.

Current presentation release: [v1.1.0](https://github.com/Y25ns25k/gaussian-slam-study/releases/tag/v1.1.0).
The public Releases page provides the current artifact; Git commit and tag history are retained.

## What changed in this presentation

The main report now follows resource diagnosis → score controls → spatial compression → cost measurement →
implementation optimization → final assessment. Each chapter states the question, control, observation and
resulting decision. Full tables are in expandable sections of [FOLLOW_UP.md](FOLLOW_UP.md), and the corrected
original report is preserved in [ARCHIVE_REPORT.md](ARCHIVE_REPORT.md).

Twelve figures replace crowded mixed-scope comparisons with readable plots, consistent score colours, explicit
references/units and seed-level outcomes. Each is supplied as PNG and scalable SVG. The plotted values and input
hashes are recorded in [figure_data.json](results/figure_data.json); the original measured JSON is unchanged.
[SUMMARY_KO.md](SUMMARY_KO.md) gives a Korean research overview. No new GPU training or score search was run.

## Verification and redistribution

[CPU verification](results/release_verification.json) records command outputs and versions from an environment
without Torch. [Artifact audit](results/artifact_audit.json) checks local links, strict JSON, numeric export
provenance, file boundaries and private-path/credential-like patterns. `MANIFEST.sha256` covers the prepared files,
excluding itself; run `sha256sum -c MANIFEST.sha256` from the release root to check the snapshot.

These checks validate the public package and arithmetic. They do not rerun upstream GPU systems, restore deleted
models/renders, establish independent preregistration, or validate online SLAM throughput.

Only original numerical helpers, scripts, tests, documents, figures and metric extracts are included. Dataset
frames, weights, checkpoints, upstream source/patches, personal IDE configuration and credentials are excluded.
See [THIRD_PARTY.md](THIRD_PARTY.md) and [LICENSE](LICENSE).

## Download and metadata

Archive: `gaussian-slam-study-20261103-v1.1.0.tar.gz`, with a SHA256 checksum beside it. Files use relative paths
under `gaussian-slam-study/`. The release tag identifies the corresponding source snapshot.

Repository title: Gaussian SLAM: Resource Profiling and Compression Optimization

Description: Resource profiling, controlled pruning experiments, and verified compression optimizations for Gaussian SLAM on a 16 GB GPU.

Topics: `gaussian-splatting`, `slam`, `3d-reconstruction`, `pytorch`, `profiling`, `reproducibility`.

The local research workspace and helper namespace retain the SAGE-4D name. Experiment dates remain unchanged;
November 3, 2026 identifies the presentation revision.
