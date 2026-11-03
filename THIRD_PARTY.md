# Third-party systems and datasets

This repository contains our own text, figures, scripts, independent numerical helpers, tests and metric tables.
It contains no vendored third-party source or patches, model weights, dataset images or rendered images.
`code/sage4d/slam/` implements numerical selection and statistics accumulation independently; it does not include
Gaussian-SLAM's renderer, mapping system, offline pruning harness or integration patches. NumPy and Matplotlib
are runtime dependencies for CPU examples/figures, and PyTorch is optional for GPU use; their distributions and
licenses are supplied separately by their respective projects.

## Systems used in the experiments

This inventory describes the experiment versions identified in the
[setup record](docs/SETUP_AND_CORRECTIONS.md#environment-and-starting-points). Current reproducibility boundaries are in
[REPORT.md §8](REPORT.md#8-reproducibility-and-evidence-boundaries).
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
- [VCGS-SLAM (arXiv 2403.11247)](https://arxiv.org/abs/2403.11247): online masking and quantization applied to
  SplaTAM, MonoGS and Gaussian-SLAM. REPORT §4 compares it only through each method's change against its own baseline.
- [MemGS (arXiv 2509.13536)](https://arxiv.org/abs/2509.13536): voxel-space merging of similar Gaussians on an
  ORB-SLAM3-based system; compared in REPORT §4 only against its own Photo-SLAM baseline.
- Taming 3DGS, PUP 3D-GS: the budgeted training and post-hoc pruning baselines above.

## Additional local online score experiment

The online appendix uses the locally checked-out [Pocket-SLAM implementation](https://github.com/UMN-ZhaoLab/Pocket-SLAM) at commit
`e3b5ca4e124f74f289402aff134038ada4285542`. Its top-level license is BSD 3-Clause; the embedded
Gaussian rasterizer retains its own research-use license. No upstream source, integration patches, weights,
input images or trained model payloads are redistributed in this draft. KITTI07 and cached IGEV stereo depth
are used; the depth is not a ground-truth annotation. SuperPoint/LightGlue and stereo-network weights remain
external. The experiment changes growth replay and tile quota allocation, so the area arm is an adapted control,
not an unchanged Pocket-SLAM reproduction. See ONLINE_COMPARISON.md for its evaluation boundary.

The separate local-system appendix uses [MemGS_SLAM](https://github.com/NAIL-HNU/MemGS_SLAM) at
`65c406183810ae25349f7a98b6b462cd2be1c6c8` (top-level GPLv3) and the
[VCGS-SLAM SplaTAM branch](https://github.com/dtc111111/VCGS-SLAM/tree/splatam-version) at
`f4d86952538d014718b8f12003a54ed951408d84` (top-level BSD 3-Clause; dependencies have separate terms).
This inventory records the local versions; it is not a blanket license for their dependencies. Neither implementation
is bundled. VCGS is the released masking/RVQ branch, not all paper components. Both use Replica inputs under the
dataset terms listed above.
