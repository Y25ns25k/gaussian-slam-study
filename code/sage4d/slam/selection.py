"""Stable per-voxel quotas with CPU key packing and optional GPU sorting.

Copyright (c) 2026 Y25ns25k. MIT License.
Inputs are integer voxel coordinates: floating-point voxel assignment is kept
outside this helper so callers can preserve their exact existing convention.
"""
import numpy as np


def _inputs(voxels, importance, fraction):
    voxels = np.asarray(voxels)
    importance = np.asarray(importance)
    if voxels.ndim != 2 or voxels.shape[1] != 3 or voxels.dtype != np.int64:
        raise ValueError('voxels must be an N x 3 int64 array')
    if importance.shape != (len(voxels),) or not np.issubdtype(importance.dtype, np.floating):
        raise ValueError('importance must be an aligned floating vector')
    if np.isnan(importance).any() or not np.isfinite(fraction) or not 0 <= fraction <= 1:
        raise ValueError('NaN scores or invalid fraction')
    return voxels, importance


def packed_voxel_keys(voxels):
    """Return collision-free int64 keys, or None when the bounding box overflows."""
    if not len(voxels):
        return np.empty(0, dtype=np.int64)
    low, high = voxels.min(axis=0), voxels.max(axis=0)
    spans = [int(b)-int(a)+1 for a,b in zip(low,high)]
    if spans[0]*spans[1]*spans[2] > np.iinfo(np.int64).max:
        return None
    offset = voxels-low
    return (offset[:,0]*spans[1]+offset[:,1])*spans[2]+offset[:,2]


def voxel_mask_numpy(voxels, importance, fraction=.25):
    voxels, importance = _inputs(voxels, importance, fraction)
    n = len(voxels)
    mask = np.zeros(n, dtype=bool)
    if not n or fraction == 0:
        return mask
    keys = packed_voxel_keys(voxels)
    ids = np.arange(n, dtype=np.int64)
    if keys is None:
        order = np.lexsort((ids, importance, voxels[:,2], voxels[:,1], voxels[:,0]))
        different = np.any(voxels[order][1:] != voxels[order][:-1], axis=1)
    else:
        order = np.lexsort((ids, importance, keys))
        different = keys[order][1:] != keys[order][:-1]
    starts = np.r_[0, np.flatnonzero(different)+1]
    counts = np.diff(np.r_[starts,n])
    quota = np.floor(counts.astype(np.float32)*np.float32(fraction)).astype(np.int64)
    rank = ids-np.repeat(starts,counts)
    mask[order] = rank < np.repeat(quota,counts)
    return mask


def voxel_mask_cuda(voxels, importance, fraction=.25):
    """Use stable CUDA sorts; preserve CPU score and voxel arithmetic exactly."""
    import torch
    voxels, importance = _inputs(voxels, importance, fraction)
    n = len(voxels)
    if not n or fraction == 0:
        return np.zeros(n,dtype=bool)
    keys = packed_voxel_keys(voxels)
    if keys is None:
        return voxel_mask_numpy(voxels,importance,fraction)
    key = torch.from_numpy(np.ascontiguousarray(keys)).cuda()
    score = torch.from_numpy(np.ascontiguousarray(importance)).cuda()
    order = torch.argsort(score, stable=True)
    order = order[torch.argsort(key[order], stable=True)]
    sorted_key = key[order]
    index = torch.arange(n, device='cuda')
    begin = torch.ones(n, dtype=torch.bool, device='cuda')
    begin[1:] = sorted_key[1:] != sorted_key[:-1]
    start = torch.cummax(torch.where(begin,index,0),dim=0).values
    end = torch.full((n,), n, device='cuda',dtype=torch.int64)
    end[:-1] = torch.where(begin[1:],index[:-1]+1,n)
    end = torch.cummin(end.flip(0),dim=0).values.flip(0)
    quota = torch.floor((end-start).float()*fraction).long()
    mask = torch.empty(n,device='cuda',dtype=torch.bool)
    mask[order] = index-start < quota
    return mask.cpu().numpy()
