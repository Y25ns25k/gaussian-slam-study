# Publication record — November 3, 2026

This repository update presents the static-to-SLAM transfer study and the completed exact-budget online score
comparison. It uses the reviewed public extract from the local study archival commit `f227865`, with publication
status wording updated for the repository. The public update commit is recorded in this repository's Git history.
No new release tag or external archive is created by this update.

The main finding remains the measured saved-map trade-off: 24.0–24.6% fewer Gaussians for a mean PSNR decrease
of about 0.22 dB on three Replica scenes. The separate online screen finds close image-quality metrics across
area, trace and random under an adapted exact-count policy. It does not establish equivalence or causal spatial-
budget superiority. All controls and the experimental boundaries remain in REPORT and ONLINE_COMPARISON.

This is a post-experiment archival publication, not evidence of pre-experiment registration. DRAFT_SOURCE.json
records the earlier local review snapshot; its hashes describe that source, not the edited publication files.
MANIFEST.sha256 describes this prepared publication snapshot, excluding the manifest itself.

CPU verification covers retained-metric arithmetic, selector tests and figure regeneration. It does not rerun
GPU training or restore unbundled datasets, models, upstream code or patches. The latest verification environment
and commands are in results/release_verification.json; file-boundary checks are in results/artifact_audit.json.
The earlier report remains in ARCHIVE_REPORT.md, and prior repository versions remain in Git history.

By [Y25ns25k](https://github.com/Y25ns25k). See LICENSE and THIRD_PARTY.md for attribution and redistribution scope.
