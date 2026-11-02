#!/usr/bin/env python3
"""Original cost screen: separate resident compression from collection-inclusive cost."""
import argparse
from pathlib import Path
from statistics import mean
import numpy as np
from figure_data import build
from plot_style import COLORS as C, LABELS, SCORE_COLOR, plt, style, heading, export, mean_marker


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    expected=Path(__file__).resolve().parents[1]/'results/followups/slam_score_cost.json'
    if args.input.resolve()!=expected.resolve():raise ValueError('Use the bundled original cost record.')
    d=build()['original'];fig,axes=plt.subplots(2,1,figsize=(10,8.7));a,b=axes
    for i,row in enumerate(d['closing']):
        value=row['mean_seconds'];a.barh(i,value,height=.58,color=SCORE_COLOR[row['arm']])
        a.text(value+.045,i,f'{value:.3f} s',va='center',fontsize=11)
    a.set(yticks=np.arange(len(d['closing'])),yticklabels=[LABELS[r['arm']] for r in d['closing']],
        xlabel='Mean compression-stage time [seconds per submap]',title='A  Statistics already present',ylim=(4.6,-.6),xlim=(0,3.5));style(a)
    for i,scene in enumerate(('room0','office0')):
        values=[r['percent_change'] for r in d['prefix'] if r['scene']==scene and r['reference']=='contrib_voxel']
        b.scatter(values,i+np.linspace(-.08,.08,len(values)),s=46,color=C['trace'],alpha=.65)
        mean_marker(b,mean(values),i)
        b.annotate(f'{mean(values):+.2f}%',(mean(values),i),xytext=(9,12),textcoords='offset points',fontsize=11,fontweight='bold')
    b.axvline(0,color=C['muted'],lw=1.1);b.set(yticks=[0,1],yticklabels=['room0','office0'],ylim=(1.6,-.6),
        title='B  Mapping + compression vs contribution sum',xlabel='Trace cost change [%] · positive means more cost');style(b)
    heading(fig,'The original cost screen motivates implementation work',
        'A and B answer different cost questions. These are earlier-run timings, not the optimized run’s reference.',
        'A: nine saved submaps; mean of five-repeat map medians, one warmup excluded. Earlier collection is excluded.\nB: three paired seeds per scene; statistics collection and native mapping I/O are included. Not online SLAM FPS.')
    fig.subplots_adjust(left=.25,right=.95,top=.83,bottom=.16,hspace=.66)
    export(fig,args.output)


if __name__=='__main__':main()
