#!/usr/bin/env python3
"""Draw implementation costs from retained metrics; no GPU required."""
import argparse
import json
from pathlib import Path
from statistics import mean
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();d=json.loads(args.input.read_text())
    fig,axes=plt.subplots(1,3,figsize=(15,4.7),constrained_layout=True)
    arms=['safe_final_voxel','safe_final_fast_voxel','contrib_voxel','contrib_fast_voxel','contribmax_fast_voxel']
    labels=['trace\nreference','trace\noptimized','contrib sum\nreference','contrib sum\noptimized','contrib max\noptimized']
    bottom=np.zeros(len(arms))
    for key,label,color in [('score_seconds','extra scoring','#d95f02'),('selection_seconds','voxel selection','#7570b3'),
                            ('restore_prune_seconds','restore + prune','#66a61e'),('refine_seconds','refinement','#1b9e77')]:
        values=np.array([mean(c['arms'][a]['median'][key] for c in d['components']) for a in arms])
        axes[0].bar(range(len(arms)),values,bottom=bottom,label=label,color=color);bottom+=values
    axes[0].set(xticks=range(len(arms)),xticklabels=labels,ylabel='Mean of phase medians [s]',
                title='A: compression on identical checkpoints\nAccumulation cost is excluded here')
    axes[0].tick_params(axis='x',labelsize=8);axes[0].set_ylim(bottom=0);axes[0].legend(fontsize=8)
    for i,scene in enumerate(('room0','office0')):
        for seed in (0,1,2):
            rows={r['variant']:r for r in d['native'] if r['scene']==scene and r['seed']==seed}
            x=np.array([i-.23,i,i+.23]);y=[rows[a]['wall_seconds'] for a in ('off','reference','fast')]
            axes[1].plot(x,y,color='0.8',lw=.8)
            for xx,yy,color,label in zip(x,y,['#377eb8','#e41a1c','#4daf4a'],['stats off','original stats','dense stats']):
                axes[1].scatter(xx,yy,s=20,color=color,label=label if i==0 and seed==0 else None,zorder=3)
    axes[1].set(xticks=[0,1],xticklabels=['room0','office0'],ylim=(0,None),ylabel='Mapping wall time [s]',
                title='B: fresh 100-frame GT-pose mapping\nThree seeds; balanced arm order')
    axes[1].legend(fontsize=8)
    refs=['safe_final_voxel','contrib_fast_voxel','contribmax_fast_voxel']
    for scene,shift,color in [('room0',-.18,'#377eb8'),('office0',.18,'#e67e22')]:
        values=[mean(r['percent_change'] for r in d['prefix_comparisons'] if r['scene']==scene and r['reference']==a) for a in refs]
        axes[2].bar(np.arange(3)+shift,values,width=.32,color=color,label=scene)
        for i,a in enumerate(refs):
            seeds=[r['percent_change'] for r in d['prefix_comparisons'] if r['scene']==scene and r['reference']==a]
            axes[2].scatter(i+shift+np.linspace(-.06,.06,len(seeds)),seeds,s=14,color='black',zorder=3)
    axes[2].axhline(0,color='black',lw=.8)
    axes[2].set(xticks=range(3),xticklabels=['vs original\ntrace','vs optimized\ncontrib sum','vs optimized\ncontrib max'],
                ylabel='Optimized trace compute sum change [%]',
                title='C: mapping + offline compression\nPositive means optimized trace costs more')
    axes[2].tick_params(axis='x',labelsize=8);axes[2].legend(fontsize=8)
    fig.suptitle('Same-score implementation optimization: nominal 25% per-voxel removal\nMapping-view evaluation; not an online SLAM FPS benchmark',fontsize=11)
    args.output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(args.output,dpi=150);plt.close(fig)
    print(args.output)


if __name__=='__main__':main()
