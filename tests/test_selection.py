import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"code"))
import unittest
from collections import defaultdict
import numpy as np
from sage4d.slam.selection import voxel_mask_numpy,packed_voxel_keys


class QuotaSelection(unittest.TestCase):
    def oracle(self,v,s,f):
        groups=defaultdict(list)
        for i,row in enumerate(v):groups[tuple(row)].append(i)
        mask=np.zeros(len(v),dtype=bool)
        for ids in groups.values():
            q=int(np.floor(np.float32(len(ids))*np.float32(f)))
            mask[sorted(ids,key=lambda i:(s[i],i))[:q]]=True
        return mask

    def test_ties_infinities_negative_voxels_and_fractions(self):
        rng=np.random.default_rng(42)
        for n in (0,1,3,40,511):
            v=rng.integers(-2,3,size=(n,3),dtype=np.int64)
            s=rng.choice(np.array([-np.inf,-0.,0.,1.,np.inf],dtype=np.float32),size=n)
            for f in (0.,.25,.35,.5,1.):
                self.assertTrue(np.array_equal(voxel_mask_numpy(v,s,f),self.oracle(v,s,f)))

    def test_overflow_falls_back_without_key_collisions(self):
        v=np.array([[-2**62,0,0],[-2**62,0,0],[2**62,3,0],[2**62,3,0]],dtype=np.int64)
        s=np.array([1,0,1,0],dtype=np.float32)
        self.assertIsNone(packed_voxel_keys(v))
        self.assertTrue(np.array_equal(voxel_mask_numpy(v,s,.5),self.oracle(v,s,.5)))

    def test_rejects_nan_and_misalignment(self):
        with self.assertRaises(ValueError):voxel_mask_numpy(np.zeros((2,3),dtype=np.int64),np.array([0.,np.nan]))
        with self.assertRaises(ValueError):voxel_mask_numpy(np.zeros((2,3),dtype=np.int64),np.array([0.]))


if __name__=='__main__':unittest.main()
