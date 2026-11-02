"""Same-score trace accumulation without dynamic-length Boolean gathers.

Copyright (c) 2026 Y25ns25k. MIT License.
"""
import torch


@torch.no_grad()
def update_dense(accum, count, xyz_gradient, scale_gradient, visible=None):
    n = len(accum)
    if not n:
        return
    score = torch.zeros_like(accum)
    if xyz_gradient is not None:
        score = score+xyz_gradient.detach().square().sum(dim=1,keepdim=True)
    if scale_gradient is not None:
        score = score+scale_gradient.detach().square().sum(dim=1,keepdim=True)
    if visible is None or visible.numel() != n:
        visible = torch.ones(n,device=accum.device,dtype=torch.bool)
    visible = visible.to(device=accum.device,dtype=torch.bool).reshape(n,1)
    accum.copy_(torch.where(visible,accum+score,accum))
    count.copy_(torch.where(visible,count+1,count))


def install_collector(gaussian_class):
    """Install the accepted dense update on the local statistics interface."""
    def collect(self, xyz_grad=None, scaling_grad=None, visible_mask=None):
        if not self.sensitivity_enabled:
            return
        self.ensure_sensitivity_stats()
        update_dense(self.sensitivity_accum,self.sensitivity_count,xyz_grad,scaling_grad,visible_mask)
    gaussian_class.update_sensitivity_stats = collect
