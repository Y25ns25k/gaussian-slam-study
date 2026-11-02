#!/usr/bin/env python3
"""Plot recorded compute costs without running any GPU experiment."""
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
    fig,axes=plt.subplots(1,3,figsize=(15,4.8),constrained_layout=True)
    arms=['safe_final_voxel','contrib_voxel','contribmax_voxel','opacity_voxel','random_voxel']
    labels=['trace','contrib sum','contrib max','opacity','random']
    bottom=np.zeros(len(arms))
    for key,label,color in [('score_seconds','extra score pass','#d95f02'),('selection_seconds','CPU voxel selection','#7570b3'),
                             ('restore_prune_seconds','restore + prune','#66a61e'),('refine_seconds','refinement','#1b9e77')]:
        values=np.array([mean(c['arms'][arm]['median'][key] for c in d['components']) for arm in arms])
        axes[0].bar(range(len(arms)),values,bottom=bottom,label=label,color=color);bottom+=values
    axes[0].set(xticks=range(len(arms)),xticklabels=labels,ylabel='Mean of phase medians [s]',
                title='A: resident closing components\nTrace collection is excluded here')
    axes[0].tick_params(axis='x',rotation=25);axes[0].legend(fontsize=8)
    rows=d['native_on_off']
    for i,scene in enumerate(('room0','office0')):
        values=[r for r in rows if r['scene']==scene]
        if not values:continue
        for r in values:
            axes[1].plot([i-.15,i+.15],[r['off_seconds'],r['on_seconds']],color='0.75',lw=.8)
        axes[1].scatter([i-.15]*len(values),[r['off_seconds'] for r in values],color='#377eb8',label='stats off' if i==0 else None)
        axes[1].scatter([i+.15]*len(values),[r['on_seconds'] for r in values],color='#e41a1c',label='stats on' if i==0 else None)
    axes[1].set(xticks=[0,1],xticklabels=['room0','office0'],ylabel='Mapping run wall time [s]',
                title='B: actual 100-frame GT-pose mapping\nThree paired seeds per scene')
    axes[1].set_ylim(bottom=0)
    if rows:axes[1].legend(fontsize=8)
    refs=['contrib_voxel','contribmax_voxel','opacity_voxel'];pairs=d['prefix_comparisons']
    for scene,shift,color in [('room0',-.18,'#377eb8'),('office0',.18,'#e67e22')]:
        values=[mean(r['percent_change'] for r in pairs if r['scene']==scene and r['reference']==ref)
                if any(r['scene']==scene and r['reference']==ref for r in pairs) else float('nan') for ref in refs]
        axes[2].bar(np.arange(len(refs))+shift,values,width=.32,color=color,label=scene)
        for i,ref in enumerate(refs):
            seeds=[r['percent_change'] for r in pairs if r['scene']==scene and r['reference']==ref]
            axes[2].scatter(i+shift+np.linspace(-.07,.07,len(seeds)),seeds,s=15,color='black',alpha=.65,zorder=3)
    axes[2].axhline(0,color='black',lw=.8)
    axes[2].set(xticks=range(len(refs)),xticklabels=['vs contrib sum','vs contrib max','vs opacity'],
                ylabel='Trace compute sum change [%]',
                title='C: mapping + offline compression accounting\nPositive means trace costs more')
    axes[2].tick_params(axis='x',rotation=20)
    if pairs:axes[2].legend(fontsize=8)
    fig.suptitle('Gaussian-SLAM cost screen: local score implementations, nominal 25% removal\n'
                 'Mapping views and short GT-pose prefixes; no online SLAM FPS claim',fontsize=11)
    args.output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(args.output,dpi=150)
    plt.close(fig);print(args.output)


if __name__=='__main__':main()
