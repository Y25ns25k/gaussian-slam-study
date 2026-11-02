# Public research artifact

This directory is the release unit for the public repository
[Y25ns25k/gaussian-slam-study](https://github.com/Y25ns25k/gaussian-slam-study), on the `main` branch.
The existing static 3DGS repository is a separate project.

The landing page has five findings and two main figures. The original ten-section report remains available,
with dated follow-ups in a separate page. Negative controls, failed gates, the rejected kernel candidate and
unresolved tracking/generalization questions remain visible.

## Verification

[Release verification](results/release_verification.json) records the actual CPU commands, package versions,
outputs and exit codes from a fresh environment without Torch. [Artifact audit](results/artifact_audit.json)
checks local links, strict JSON, file boundaries, private-path/credential-like patterns and export hashes.
`MANIFEST.sha256` lists hashes of the prepared files, excluding the manifest itself. On systems with
`sha256sum`, run `sha256sum -c MANIFEST.sha256` from the release root.

These checks validate the public package and arithmetic. They do not rerun the original GPU experiments,
reconstruct deleted models/renders, establish independent prior registration or validate online SLAM throughput.

## Redistribution scope

Only independent original helpers, scripts, tests, documentation, figures and metric extracts are included.
No dataset frames, checkpoints, pretrained weights, upstream source/patches, personal IDE configuration, account
credentials or Git history are included. See [THIRD_PARTY.md](THIRD_PARTY.md) and [LICENSE](LICENSE).

The public archive contains this directory's contents with relative paths under `gaussian-slam-study/`.
The November 3 write-up archive is named `gaussian-slam-study-20261103.tar.gz`; its checksum is supplied beside it.
The current public download is
[v1.0.1](https://github.com/Y25ns25k/gaussian-slam-study/releases/tag/v1.0.1), with the archive and checksum
attached to that release. The superseded release entry and its attachments have been removed; Git commit
history and tags remain available. Experiment results and numerical helper implementations are unchanged.
The attached archive remains the unchanged v1.0.1 snapshot; publication guidance on `main` records this cleanup.

## Repository metadata

Repository name: `gaussian-slam-study`

README title: Gaussian SLAM: Resource Profiling and Compression Optimization

Description: Resource profiling, controlled pruning experiments, and verified compression optimizations for Gaussian SLAM on a 16 GB GPU.

Topics: `gaussian-splatting`, `slam`, `3d-reconstruction`, `pytorch`, `profiling`, `reproducibility`.

The local research workspace and helper namespace retain the SAGE-4D name. Experiment records remain dated
November 2; November 3 identifies this write-up update. No new GPU experiments were run for the text revision.

## Release v1.0.1

Tag: `v1.0.1`

Title: Research artifact v1.0.1 — Documentation update

Documentation update with the agreed project title and introduction, Korean/English portfolio descriptions,
and refreshed artifact checks and packaging. The reports, controlled follow-up experiments, measured
implementation improvements, curated metrics, independent numerical helpers and CPU reproduction commands
remain available. On nine saved
submaps, mean compression-stage time decreases from 2.32 s to 0.99 s (57.4%) versus original trace. Earlier
statistics collection is excluded from those stage times. A robust total-cost advantage over optimized
contribution scoring is not established. Full upstream training and SLAM reruns are outside the release scope.
