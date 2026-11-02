#!/usr/bin/env python3
"""Small CPU example: same per-voxel quota, stable index tie-breaking."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import numpy as np
from sage4d.slam.selection import voxel_mask_numpy

voxels=np.array([[0,0,0]]*4+[[1,0,0]]*3,dtype=np.int64)
scores=np.array([4,1,1,3,2,0,5],dtype=np.float32)
mask=voxel_mask_numpy(voxels,scores,fraction=.5)
# floor(4*.5)=2 and floor(3*.5)=1; index breaks the first group's tie.
assert np.array_equal(np.flatnonzero(mask),[1,2,5])
print('Removed indices:',np.flatnonzero(mask).tolist())
print('Removed:',int(mask.sum()),'of',len(mask),'(per-voxel floor quotas)')
