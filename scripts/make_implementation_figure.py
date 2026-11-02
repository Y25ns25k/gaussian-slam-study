#!/usr/bin/env python3
"""Regenerate four separate implementation/cost figures; CPU, PNG and SVG."""
import argparse
from pathlib import Path
from statistics import mean
import numpy as np
from figure_data import build
from plot_style import COLORS as C, plt, style, heading, export, mean_marker


def closing(d,output):
    rows=d['closing'];fig,ax=plt.subplots(figsize=(10,6.3))
    labels=['Trace · original','Trace · optimized','Contribution sum · original',
            'Contribution sum · optimized','Contribution max · optimized','Opacity · optimized']
    cols=[C['trace_light'],C['trace'],C['contrib_light'],C['contrib'],C['contribmax'],C['opacity']]
    for i,(row,col) in enumerate(zip(rows,cols)):
        value=row['mean_seconds'];ax.barh(i,value,height=.6,color=col)
        ax.text(value+.055,i,f'{value:.3f} s',va='center',fontweight='bold',fontsize=12)
    ax.set(yticks=np.arange(len(rows)),yticklabels=labels,xlabel='Compression-stage time [seconds per submap]',xlim=(0,max(r['mean_seconds'] for r in rows)*1.24),ylim=(len(rows)-.5,-.6));style(ax)
    by={r['arm']:r['mean_seconds'] for r in rows}
    saving=100*(1-by['safe_final_fast_voxel']/by['safe_final_voxel'])
    heading(fig,f'Same tested masks, {saving:.1f}% shorter compression stage',
        'Fresh reference and optimized runs · nine fixed submaps · mean of map-level timing medians.',
        'Five measured repetitions per map after one warmup. Includes scoring, selection, restore/prune and 50 refinement steps.\nEarlier statistics collection, load, evaluation and output serialization are excluded. Opacity has different quality (Fig. 5).')
    fig.subplots_adjust(left=.32,right=.97,top=.81,bottom=.20)
    export(fig,output)


def total_cost(d,output):
    refs=[('contrib_fast_voxel','A  vs optimized contribution sum'),
          ('contribmax_fast_voxel','B  vs optimized contribution max')]
    fig,axes=plt.subplots(1,2,figsize=(10.6,7.2),sharex=True,sharey=True)
    labels=[]
    for scene in ('room0','office0'):
        labels += [f'{scene} · seed {s}' for s in (0,1,2)]+[f'{scene} · mean']
    all_values=[r['percent_change'] for r in d['prefix'] if r['reference'] in {x[0] for x in refs}]
    limit=max(2.,max(abs(x) for x in all_values)*1.35)
    for ax,(ref,title) in zip(axes,refs):
        ax.axhspan(-.5,3.5,color='#F3F6FB',zorder=0)
        for block,scene in enumerate(('room0','office0')):
            rows=sorted([r for r in d['prefix'] if r['scene']==scene and r['reference']==ref],key=lambda x:x['seed'])
            assert len(rows)==3
            for j,r in enumerate(rows):
                y=block*4+j;x=r['percent_change'];q=r['direct_quality_delta']
                failed=not(q['PSNR']>=-.1 and q['LPIPS']<=.002 and q['depth_l1_mm']<=.1)
                ax.scatter(x,y,s=58,color=C['trace'],edgecolors=C['contrib'] if failed else 'white',linewidth=2 if failed else .7,zorder=4)
                ax.annotate(f'{x:+.2f}%'+(' †' if failed else ''),(x,y),xytext=(9,0) if x>=0 else (-9,0),textcoords='offset points',ha='left' if x>=0 else 'right',va='center',fontsize=10)
            avg=mean(r['percent_change'] for r in rows);y=block*4+3
            mean_marker(ax,avg,y);ax.annotate(f'{avg:+.2f}%',(avg,y),xytext=(9,0) if avg>=0 else(-9,0),textcoords='offset points',ha='left' if avg>=0 else 'right',va='center',fontsize=10,fontweight='bold')
        ax.axvline(0,color=C['muted'],lw=1.1);ax.set(title=title,xlim=(-limit,limit),xlabel='Optimized trace cost change [%]');style(ax)
    axes[0].set(yticks=np.arange(8),yticklabels=labels,ylim=(7.6,-.7))
    heading(fig,'Including mapping: small means, changing seed-level signs',
        'Negative: trace costs less. Positive: trace costs more. Black diamonds: mean paired percentage change.',
        'Two 100-frame GT-pose prefixes × three seeds; sources can differ numerically even at the same seed.\nAccounting = native mapping wall + common load + compression. Native checkpoint I/O included; not online FPS.\n† office0 seed 1 vs contribution-max: direct ΔPSNR = −0.101133 dB, below the −0.10 dB quality guard.')
    fig.subplots_adjust(left=.21,right=.98,top=.80,bottom=.24,wspace=.18)
    export(fig,output)


def phases(d,output):
    rows={r['arm']:r for r in d['closing']};fig,ax=plt.subplots(figsize=(10,5.8))
    keys=['selection_seconds','refine_seconds','restore_prune_seconds','score_seconds']
    labels=['Voxel selection','Refinement','Restore + prune','Trace score access']
    for i,key in enumerate(keys):
        a=rows['safe_final_voxel']['phase_means'][key]*1000
        b=rows['safe_final_fast_voxel']['phase_means'][key]*1000
        ax.plot([a,b],[i,i],color='#B5C0CE',lw=2,zorder=2)
        ax.scatter(a,i,color=C['opacity'],s=48,label='Original trace' if i==0 else None,zorder=3)
        ax.scatter(b,i,color=C['trace'],s=48,label='Optimized trace' if i==0 else None,zorder=3)
        fmt=lambda x:f'{x:.3f}' if x<1 else f'{x:.1f}'
        ax.text(1.03,i,f'{fmt(a)} → {fmt(b)}',transform=ax.get_yaxis_transform(),va='center',fontsize=11)
    ax.set(yticks=np.arange(4),yticklabels=labels,xlabel='Mean of map-level phase medians [milliseconds]',ylim=(3.6,-.6),xlim=(-25,1550))
    ax.legend(loc='lower right',fontsize=11);style(ax)
    heading(fig,'Voxel selection accounts for most of the measured reduction',
        'Identical historical sources · original vs optimized trace · collection frequency and score unchanged.',
        'These are separate phase medians averaged over nine maps. Their sum need not equal the median of total closing time.\nTiny differences in other phases include normal timing/refinement variability; this is not a FLOP count.')
    fig.subplots_adjust(left=.24,right=.78,top=.80,bottom=.22)
    export(fig,output)


def collection(d,output):
    fig,ax=plt.subplots(figsize=(10,6.8));labels=[]
    for block,scene in enumerate(('room0','office0')):
        vals={'reference':[],'fast':[]}
        for seed in (0,1,2):
            rows={r['variant']:r for r in d['native'] if r['scene']==scene and r['seed']==seed}
            y=block*4+seed;labels.append(f'{scene} · seed {seed}')
            for variant,offset,col,marker in [('reference',-.08,C['opacity'],'o'),('fast',.08,C['trace'],'s')]:
                delta=100*(rows[variant]['wall_seconds']/rows['off']['wall_seconds']-1);vals[variant].append(delta)
                ax.scatter(delta,y+offset,s=45,color=col,marker=marker,label={'reference':'Original collector','fast':'Dense collector'}[variant] if block==0 and seed==0 else None)
        labels.append(f'{scene} · mean')
        for variant,offset,col,marker in [('reference',-.08,C['opacity'],'o'),('fast',.08,C['trace'],'s')]:
            value=mean(vals[variant]);y=block*4+3
            ax.scatter(value,y+offset,color=col,marker=marker,s=72)
            ax.annotate(f'{value:+.2f}%',(value,y+offset),xytext=(9,8 if variant=='reference' else -8),textcoords='offset points',va='center',fontsize=10,color=col)
    ax.axvline(0,color=C['muted'],lw=1.2);ax.set(yticks=np.arange(8),yticklabels=labels,ylim=(7.6,-.6),xlabel='Mapping wall-time change vs statistics off [%]')
    ax.legend(loc='lower right');style(ax)
    heading(fig,'Collector cost must be measured during mapping',
        'Fresh off / original / dense runs · 100 GT-pose frames · three seeds per scene · balanced arm order.',
        'Native wall includes source checkpoint writes, data loading and logging. All paired optimizer-call layouts match.\nSource geometry and timing still vary: a negative observed difference does not make collection free.')
    fig.subplots_adjust(left=.23,right=.96,top=.81,bottom=.20)
    export(fig,output)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    # The CLI input remains explicit; the derived dataset binds all sources with SHA256.
    expected=Path(__file__).resolve().parents[1]/'results/followups/slam_implementation.json'
    if args.input.resolve()!=expected.resolve():
        raise ValueError('Use the bundled implementation record; derived figure data records its provenance.')
    d=build()['optimized'];closing(d,args.output)
    total_cost(d,args.output.parent/'fig9_total_cost.png')
    phases(d,args.output.parent/'fig10_phase_breakdown.png')
    collection(d,args.output.parent/'fig11_collection_overhead.png')


if __name__=='__main__':main()
