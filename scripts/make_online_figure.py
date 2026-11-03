#!/usr/bin/env python3
"""Plot every primary seed/arm from the exact-count online comparison, CPU only."""
import hashlib
import json
from pathlib import Path
from matplotlib.lines import Line2D
from plot_style import COLORS, plt, style, heading, export

ROOT=Path(__file__).resolve().parents[1]


def main():
    source=ROOT/'results/online_budget25.json'
    data=json.loads(source.read_text()); rows=data['rows']
    if not data['per_event_count_match_verified'] or len(rows)!=8:
        raise ValueError('Expected all verified primary runs, no selective plotting')
    colors={'baseline':COLORS['ink'],'area':COLORS['contrib'],
            'trace':COLORS['trace'],'random':COLORS['random']}
    labels={'baseline':'No-deletion reference','area':'Area (adapted)','trace':'Trace','random':'Random'}
    fig,axes=plt.subplots(1,3,figsize=(14.5,6.2),sharex=True)
    count_notes=[]
    for seed in [0,1]:
        subset={r['arm']:r for r in rows if r['seed']==seed}
        counts=[subset[a]['gaussian_count'] for a in ['area','trace','random']]
        if len(set(counts))!=1:raise ValueError('Count mismatch')
        count_notes.append(f'Seed {seed}: {subset["baseline"]["gaussian_count"]:,} → {counts[0]:,} Gaussians')
        for arm,r in subset.items():
            ys=[r['quality']['estimated_camera']['psnr'],r['quality']['estimated_camera']['lpips'],r['ate_rmse_cm']]
            for ax,y in zip(axes,ys):
                ax.scatter(r['frontend_wall_seconds'],y,c=colors[arm],marker='o' if seed==0 else '^',
                           s=85,edgecolors='white',linewidth=.7,zorder=3)
    for ax,title,label in zip(axes,['A  Reconstruction PSNR ↑','B  Perceptual distance ↓','C  Tracking error ↓'],
                            ['Full-image PSNR (dB)','AlexNet LPIPS','SE(3)-aligned ATE RMSE (cm)']):
        ax.set(title=title,xlabel='Frontend process wall (s)',ylabel=label)
        ax.margins(x=.15,y=.15);style(ax,'both')
    handles=[Line2D([],[],marker='o',ls='',color=colors[a],label=labels[a]) for a in colors]
    handles += [Line2D([],[],marker=m,ls='',color=COLORS['muted'],label=f'Seed {s}') for s,m in [(0,'o'),(1,'^')]]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.5,.87),ncol=6,fontsize=10)
    heading(fig,'Online score comparison at an exact 25% smaller map budget',
            'KITTI07 · 51 inputs · 2 seeds · common replayed births · area/trace/random counts matched at every event.',
            ' | '.join(count_notes)+'.\nObserved views; frontend excludes stereo preprocessing, loop closure and backend. '
            'Reference includes instrumentation. Area is a modified Pocket-inspired control, not full Pocket-SLAM.')
    fig.subplots_adjust(left=.065,right=.98,top=.73,bottom=.24,wspace=.36)
    export(fig,ROOT/'figures/fig15_online_budget25')
    numeric=dict(source='online_budget25.json',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                 plotted=[dict(arm=r['arm'],seed=r['seed'],count=r['gaussian_count'],
                               wall_seconds=r['frontend_wall_seconds'],psnr=r['quality']['estimated_camera']['psnr'],
                               lpips=r['quality']['estimated_camera']['lpips'],ate_cm=r['ate_rmse_cm']) for r in rows])
    (ROOT/'results/online_figure_data.json').write_text(json.dumps(numeric,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
