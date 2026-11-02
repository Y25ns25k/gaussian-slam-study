# Independent numerical helpers

The helpers here were written for this study. Upstream Gaussian-SLAM source and the complete integration
harness are not bundled. They provide a small runnable part of the artifact, not a replacement SLAM system.

- `sage4d/slam/selection.py`: NumPy or optional stable CUDA sorting for a per-voxel removal mask.
- `sage4d/slam/collector.py`: the accepted dense PyTorch statistics update; no changed sampling frequency.
- `sage4d/slam/adapter.py`: the local CPU parameter-dictionary interface to score computation and selection.

`selection.py` takes **already assigned** `int64` voxel coordinates and a floating importance vector. It removes
`floor(float32(count) * float32(fraction))` points per voxel, lowest importance first, with original index as the
tie breaker. It accepts ±infinity and rejects NaN. Packed keys are collision-free; a bounding-box overflow uses
an uncompressed coordinate sort. Keeping voxel assignment outside the helper preserves the caller's original
floating-point convention. CUDA sorting still receives CPU-computed keys and scores; it is not a GPU-only path.

`update_dense(accum, count, xyz_gradient, scale_gradient, visible)` expects aligned floating `(N,1)` accumulator
and count buffers, `(N,3)` gradients or `None`, and a Boolean visibility mask. It adds the existing squared-gradient
reduction and one count only for visible entries. The installer expects the local class's `sensitivity_enabled`,
`ensure_sensitivity_stats`, `sensitivity_accum`, and `sensitivity_count` interface. It does not implement submap
creation, buffer resizing, reset policy, optimizer state updates or pruning integration.

The adapter expects CPU Torch tensors (`xyz`, `opacity` logits and either statistics or contribution scores).
Its voxel size is 0.05 m. Only equal-voxel-quota modes are supported; `max_prune_abs` and `opacity_gate` are legacy
interface arguments unused by those modes. It does not render contribution scores; the caller supplies them.

Run from the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/demo_selection.py
python -m unittest discover -s tests
```

These commands need only NumPy. PyTorch is optional for the collector/adapter; CUDA selection additionally needs
a compatible CUDA-enabled PyTorch and GPU. GPU validation used PyTorch 2.11.0+cu128, CUDA 12.8, NumPy 1.26.4
on one RTX 5070 Ti. No cross-version bitwise guarantee is made. The CPU unit tests check selection against an
independent per-voxel oracle. Real-gradient GPU parity is a retained experiment result; it cannot be rerun from
this release without the original integration and inputs.

A one-kernel Triton collector candidate failed exactness and is excluded. The published collector's
`update_dense` function is unchanged from the tested frozen function; its installer exposes only that accepted
variant. See [export provenance](../results/followups/provenance.json) for source and public-file hashes.
