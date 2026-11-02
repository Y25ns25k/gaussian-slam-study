"""Adapt independent quota selection to the retained local experiment API.

Copyright (c) 2026 Y25ns25k. MIT License.
"""
import torch
from .selection import voxel_mask_numpy,voxel_mask_cuda


def select(params,selection,prune_ratio,max_prune_abs=0,min_samples=1,opacity_gate=0,backend='numpy'):
    if selection not in ('safe_final_voxel','contrib_voxel','contribmax_voxel','opacity_voxel','random_voxel','none'):
        raise ValueError('Only equal per-voxel quota modes are supported')
    n=len(params['xyz'])
    if selection=='none' or prune_ratio<=0 or n==0:
        mask=torch.zeros(n,dtype=torch.bool)
    else:
        if selection=='safe_final_voxel':
            samples=params['sensitivity_count'].float().reshape(-1)
            importance=torch.log(params['sensitivity_accum'].float().reshape(-1)/samples.clamp(min=1)+1e-12)
            importance=torch.where((samples>=min_samples)&importance.isfinite(),importance,float('inf'))
        elif selection.startswith('contrib'):
            importance=params['contrib_max' if selection=='contribmax_voxel' else 'contrib_sum'].float()
        elif selection=='random_voxel':
            importance=torch.rand(n,generator=torch.Generator().manual_seed(20261021+n))
        else:
            importance=params['opacity'].float().reshape(-1).sigmoid()
            importance=torch.where(importance.isfinite(),importance,float('inf'))
        voxels=torch.floor(params['xyz'].float()/.05).long().numpy()
        fn=voxel_mask_cuda if backend=='cuda' else voxel_mask_numpy
        mask=torch.from_numpy(fn(voxels,importance.numpy(),prune_ratio))
    return mask,{'current_count':n,'valid_count':n,'candidate_count':n if selection!='none' else 0,
                 'pruned_count':int(mask.sum()),'mean_score':'','min_score':'','max_score':''}
