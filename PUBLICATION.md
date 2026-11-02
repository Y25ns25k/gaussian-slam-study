# Prepared public artifact

This directory is the release unit. It can be uploaded as a new GitHub repository after choosing its name.
No repository has been created and nothing has been pushed by the preparation process. The existing static
3DGS repository is a separate project.

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

The public archive contains this directory's contents with relative paths. Its checksum is supplied beside the
archive. Repository creation, description/topics and the final public URL are the remaining publication steps.

## Suggested repository metadata

Description: Gaussian SLAM resource profiling, controlled pruning ablations, and exact-mask implementation optimization.

Topics: `gaussian-splatting`, `slam`, `3d-reconstruction`, `pytorch`, `profiling`, `reproducibility`.

Choose the repository name before creating its remote; no particular name or visibility setting has been applied.
