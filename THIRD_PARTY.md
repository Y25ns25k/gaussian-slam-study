# Third-party systems and datasets

This repository contains our own text, figures, scripts, independent numerical helpers, tests and metric tables.
It contains no vendored third-party source or patches, model weights, dataset images or rendered images.
`code/sage4d/slam/` implements numerical selection and statistics accumulation independently; it does not include
Gaussian-SLAM's renderer, mapping system, offline pruning harness or integration patches. NumPy and Matplotlib
are runtime dependencies for CPU examples/figures, and PyTorch is optional for GPU use; their distributions and
licenses are supplied separately by their respective projects.

## Systems used in the experiments

This inventory describes the experiment versions identified in the
[original setup record](ARCHIVE_REPORT.md#8-reproducibility). Current reproducibility boundaries are in
[REPORT.md §9](REPORT.md#9-reproducibility-and-evidence-boundaries).
Top-level licenses do not replace notices in individual files, submodules, or dependencies. Official sources are
linked so readers can check the applicable version and terms.

| System | Source | License inventory for the versions used | Redistributed here |
|---|---|---|---|
| Flow4DGS-SLAM | [wangys16/Flow4DGS-SLAM](https://github.com/wangys16/Flow4DGS-SLAM) | No top-level license file. Its `gaussian_splatting/` folder carries the Inria Gaussian-Splatting license (non-commercial) | No: neither code nor patches |
| Taming 3DGS | [humansensinglab/taming-3dgs](https://github.com/humansensinglab/taming-3dgs) | [MIT for the authors' modifications only](https://github.com/humansensinglab/taming-3dgs/blob/main/LICENSE.md); original 3DGS code retains its own license | No |
| PUP 3D-GS | [j-alex-hanson/gaussian-splatting-pup](https://github.com/j-alex-hanson/gaussian-splatting-pup) | Inria Gaussian-Splatting license (non-commercial) | No |
| 3D Gaussian Splatting | [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) | Inria Gaussian-Splatting license (non-commercial) | No |
| SplaTAM | [spla-tam/SplaTAM](https://github.com/spla-tam/SplaTAM) | BSD 3-Clause | No |
| Gaussian-SLAM | [VladimirYugay/Gaussian-SLAM](https://github.com/VladimirYugay/Gaussian-SLAM) | MIT. Some files carry an Inria notice | No |
| LSG-SLAM | [lsg-slam/LSG-SLAM](https://github.com/lsg-slam/LSG-SLAM) | BSD 3-Clause | No |

**Why the patches are not included in this release.** Local changes cover ports, profiling, memory handling,
score modes, and an offline pruning tool. Several touch files with non-commercial or unclear terms. This release
therefore provides metrics and a description of the changes while leaving code redistribution for a file-level
review. Non-commercial terms do not by themselves imply that all patches are unpublishable. No general
redistribution permission or blanket prohibition is asserted here, and the upstream commit list is not enough
to reproduce the modified experiments.

**Pretrained weights.** These systems load pretrained networks, for example optical flow (RAFT/GMA) in Flow4DGS-SLAM
and stereo depth (IGEV) in the LSG-SLAM KITTI pipeline. The weights are not included and keep their own licenses.

## Datasets

Only metrics computed on these datasets appear here. To rerun anything, obtain each dataset from its source and
follow its terms.

| Dataset | Used for | Terms |
|---|---|---|
| Mip-NeRF 360 (kitchen, room, bonsai) | static 3DGS | [Official dataset page](https://jonbarron.info/mipnerf360/); no dataset redistribution license identified on that page |
| Tanks and Temples (train) | static 3DGS | [Official dataset page](https://www.tanksandtemples.org/); obtain data under its download terms |
| TUM RGB-D (fr3/walking_xyz) | Flow4DGS-SLAM | [CC BY 4.0 for data, unless otherwise stated](https://cvg.cit.tum.de/data/datasets/rgbd-dataset#license) |
| Bonn RGB-D Dynamic (balloon) | Flow4DGS-SLAM reproduction | [Official dataset page](https://www.ipb.uni-bonn.de/data/rgbd-dynamic-dataset/); check dataset terms separately from code |
| Replica (room0, room1, office0) | SplaTAM, Gaussian-SLAM | [Replica Dataset Research Terms](https://github.com/facebookresearch/Replica-Dataset/blob/main/LICENSE), research/education subject to its non-commercial or not-for-profit conditions |
| KITTI odometry (sequence 07) | LSG-SLAM | [CC BY-NC-SA 3.0](https://www.cvlibs.net/datasets/kitti/) |

## Related work referenced in the report

- [Pocket-SLAM: Rendering-Area-Aware Pruning for Memory-Efficient 3DGS-SLAM](https://arxiv.org/abs/2606.24796):
  online pruning with image-tile budgets and a source for the LSG-SLAM KITTI memory discussion. Our offline
  ΣTα/3D-voxel control does not reproduce its full method.
- Taming 3DGS, PUP 3D-GS: the budgeted training and post-hoc pruning baselines above.
