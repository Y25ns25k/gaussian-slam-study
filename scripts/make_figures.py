#!/usr/bin/env python3
"""Rebuild the resource and score/quality figures from original JSON (CPU)."""
from pathlib import Path
from statistics import mean
import numpy as np
from matplotlib.lines import Line2D
from figure_data import write_data
from plot_style import COLORS as C, LABELS, SCORE_COLOR, plt, style, heading, export, mean_marker

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'figures'


def memory(d):
    fig,axes=plt.subplots(2,1,figsize=(9.5,8.4))
    a,b=axes;rows=d['memory']['splatam'];frames=[r['frame'] for r in rows]
    for key,lab,col in [('alloc','All allocated',C['opacity']),('keyframe_bytes','Keyframes: RGB + depth',C['trace']),
                         ('gaussian','Gaussian parameters + tracked state',C['contrib'])]:
        values=[(r['param_bytes']+r['variable_bytes'] if key=='gaussian' else r[key])/2**30 for r in rows]
        a.plot(frames,values,color=col,label=lab)
        a.annotate(f'{values[-1]:.2f} GiB',(frames[-1],values[-1]),xytext=(9,0),textcoords='offset points',va='center',color=col,fontweight='bold')
    a.set(title='A  SplaTAM · Replica room1',xlabel='Processed frame',ylabel='Allocated / recorded tensors [GiB]',xlim=(0,2260),ylim=(0,2.85))
    a.legend(loc='upper left',fontsize=10);style(a,'y')
    rows=d['memory']['lsg'];x=[r['gaussians']/1e6 for r in rows];y=[r['peak_alloc_gib'] for r in rows]
    b.plot(x,y,color=C['trace'],marker='o',markersize=7)
    for xx,yy,r in zip(x,y,rows):b.annotate(f"{r['frames']} frames",(xx,yy),xytext=(0,10),textcoords='offset points',ha='center',fontsize=10)
    b.set(title='B  LSG-SLAM front end · KITTI 07 prefixes',xlabel='Gaussians in one map [millions]',ylabel='Peak allocated memory [GiB]',ylim=(0,7.8),xlim=(.6,4.4))
    style(b,'y')
    heading(fig,'Choose the resource before reducing the map','Keyframe data and Gaussian state are separate targets.',
        'A: end-of-frame snapshots, not a full peak decomposition. B: front end only; no backend or loop closure.\nThese are different workloads, not a cross-system memory ranking.')
    fig.subplots_adjust(left=.13,right=.92,top=.83,bottom=.15,hspace=.58)
    export(fig,FIG/'fig1_slam_memory.png')


def storage(d):
    rows=d['storage'];fig,axes=plt.subplots(1,2,figsize=(10,6.3),sharey=True,gridspec_kw={'width_ratios':[1.1,1]})
    y=np.arange(len(rows));cols=[C['trace'] if r['exact_scheme'] else C['contrib'] for r in rows]
    for i,r in enumerate(rows):
        value=mean(r['mib']);axes[0].barh(i,value,color=cols[i],height=.58,alpha=.85)
        axes[0].text(value+5,i,f'{value:.1f}',va='center',fontsize=10)
        axes[1].scatter(r['dpsnr'],i+np.linspace(-.075,.075,3),s=23,color=cols[i],alpha=.55)
        mean_marker(axes[1],mean(r['dpsnr']),i)
        axes[1].text(1.02,i,f"{mean(r['dpsnr']):+.3f}",transform=axes[1].get_yaxis_transform(),va='center',fontsize=10)
    axes[0].set(yticks=y,yticklabels=[r['label'] for r in rows],xlabel='Modeled bank size [MiB]',title='A  Storage',xlim=(0,max(mean(r['mib']) for r in rows)*1.18))
    axes[0].invert_yaxis();axes[1].axvline(0,color=C['muted'],lw=1)
    axes[1].set(xlabel='PSNR change vs dense [dB]',title='B  Observed quality change',xlim=(-.36,.025))
    for ax in axes:style(ax)
    reduction=100*(1-mean(rows[3]['mib'])/mean(rows[0]['mib']))
    heading(fig,f'Temporal storage: combined exact scheme saves {reduction:.1f}%',
        'Three repeated seed-0 runs · blue: exact schemes · orange: approximate merges · diamonds: means.',
        'Bytes include centres, Adam moments and indices. This is a storage model, not measured VRAM saving.\nExact-scheme render parity was recorded originally; the original parity images are not bundled.')
    fig.subplots_adjust(left=.26,right=.93,top=.80,bottom=.20,wspace=.35)
    export(fig,FIG/'fig2_flow4dgs_storage.png')


def roles(d):
    rows=d['roles'];fig,ax=plt.subplots(figsize=(10,6.8))
    for i,r in enumerate(rows):
        values=[p['delta'] for p in r['pairs']];col={'pruning':C['trace'],'growth':C['growth'],'control':C['opacity']}[r['role']]
        ax.scatter(values,i+np.linspace(-.11,.11,len(values)),s=29,color=col,alpha=.55,zorder=3)
        mean_marker(ax,mean(values),i)
        ax.text(1.02,i,f'{mean(values):+.3f}',transform=ax.get_yaxis_transform(),va='center',fontweight='bold',fontsize=11)
    ax.set(yticks=np.arange(len(rows)),yticklabels=[r['label'] for r in rows],xlabel='Paired test-view PSNR change [dB]')
    ax.set_ylim(len(rows)-.5,-.5);ax.axvline(0,color=C['muted'],lw=1);style(ax)
    ax.legend(handles=[Line2D([0],[0],marker='o',color='none',markerfacecolor=c,label=l) for c,l in
        [(C['trace'],'Deletion change'),(C['growth'],'Growth change'),(C['opacity'],'Both-role controls')]],
        loc='upper left',bbox_to_anchor=(0,-.14),ncol=2,fontsize=10)
    heading(fig,'Separate the score’s growth and deletion roles',
        '35% retained-count budget · four scenes × two seeds · each row names its reference.',
        'Small dots: paired scene–seed differences. Black diamonds / right labels: means.\nHistorical gradient control changes both roles; the later gradient screen changes deletion only.')
    fig.subplots_adjust(left=.35,right=.89,top=.82,bottom=.25)
    export(fig,FIG/'fig3_taming_roles.png')


def posthoc(d):
    fig,axes=plt.subplots(2,1,figsize=(9.5,8.3));a,b=axes
    for score,label in [('trace','Trace'),('taming','Taming · all scoring views'),('opacity','Opacity'),('random','Random')]:
        rows=[r for r in d['posthoc'] if r['score']==score];x=[r['share'] for r in rows];y=[mean(p['delta'] for p in r['pairs']) for r in rows]
        a.plot(x,y,color=C[score],marker='o',label=label)
    a.axhline(0,color=C['muted'],lw=1);a.set(title='A  Mean loss against each unpruned source',ylabel='PSNR change [dB]',xticks=[10,20,30],xlim=(8,32))
    a.legend(loc='lower left',fontsize=10);style(a,'y')
    for share in (10,20,30):
        trace=next(r for r in d['posthoc'] if r['score']=='trace' and r['share']==share)
        taming=next(r for r in d['posthoc'] if r['score']=='taming' and r['share']==share)
        assert [(r['scene'],r['seed']) for r in trace['pairs']]==[(r['scene'],r['seed']) for r in taming['pairs']]
        values=[x['delta']-y['delta'] for x,y in zip(trace['pairs'],taming['pairs'])]
        b.scatter(share+np.linspace(-.6,.6,len(values)),values,s=31,color=C['trace'],alpha=.5)
        mean_marker(b,share,mean(values));b.annotate(f'{mean(values):+.3f}',(share,mean(values)),xytext=(12,7),textcoords='offset points',fontsize=10)
    b.axhline(0,color=C['muted'],lw=1);b.set(title='B  Paired difference against the stronger Taming control',xlabel='Gaussians removed [%]',ylabel='Trace − Taming PSNR [dB]',xticks=[10,20,30],xlim=(8,32))
    style(b,'y')
    heading(fig,'The deletion budget changes the comparison','Finished Taming models · eight scene–seed cells · no fine-tuning.',
        'A: means over four scenes × two seeds. B: all eight paired differences; black diamonds are means.\nPositive values in B favour trace. Similar observed means do not prove equivalence.')
    fig.subplots_adjust(left=.14,right=.95,top=.83,bottom=.15,hspace=.48)
    export(fig,FIG/'fig4_posthoc_curves.png')


def compression(d):
    scores=['safe_final_voxel','contrib_voxel','contribmax_voxel','hybrid_voxel','opacity_voxel','random_voxel']
    scenes=['room0','office0','room1'];markers=['o','s','D'];fig,axes=plt.subplots(1,2,figsize=(10.5,6.7),sharex=True,sharey=True)
    for ax,share,title in zip(axes,(.25,.5),('A  24.0–24.6% removed','B  49.3–49.7% removed')):
        for i,score in enumerate(scores):
            rows=[r for r in d['compression'] if r['score']==score and r['nominal_removed']==share]
            if not rows:ax.text(-1.25,i,'not evaluated',ha='center',va='center',color=C['random'],fontsize=10)
            for scene,offset,marker in zip(scenes,(-.11,0,.11),markers):
                rs=[r for r in rows if r['scene']==scene]
                assert len(rs)<=1
                if rs:ax.scatter(rs[0]['dpsnr'],i+offset,marker=marker,s=58,color=SCORE_COLOR[score],edgecolors='white',linewidth=.6,zorder=3)
        ax.axvline(0,color=C['muted'],lw=1);ax.set(title=title,xlabel='PSNR change vs refine-only [dB]',xlim=(-2.75,.09),xticks=[-2.5,-2,-1.5,-1,-.5,0]);style(ax)
    axes[0].set(yticks=np.arange(len(scores)),yticklabels=[LABELS[s] for s in scores],ylim=(len(scores)-.5,-.5))
    fig.legend(handles=[Line2D([0],[0],marker=m,color='none',markerfacecolor=C['muted'],markersize=7,label=s) for s,m in zip(scenes,markers)],
               loc='lower center',bbox_to_anchor=(.58,.10),ncol=3)
    heading(fig,'Spatial quotas: the removal budget matters',
        'Gaussian-SLAM · identical 5 cm voxel quotas · both panels use the same horizontal scale.',
        'One source run per scene. Offline, mapping views, 50 refinement steps, colours frozen.\nMissing controls at 50% are not zero loss. Less-negative PSNR change is better.')
    fig.subplots_adjust(left=.23,right=.98,top=.81,bottom=.24,wspace=.12)
    export(fig,FIG/'fig5_gslam_compression.png')


def trace_controls(d):
    fig,axes=plt.subplots(1,2,figsize=(11.5,6.7));a,b=axes
    rows=[('Original screen\n4 scenes × 2 seeds',[r['delta'] for r in d['roles'][0]['pairs']]),
          ('Matched turnover\n2 scenes × 2 seeds',[r['dpsnr'] for r in d['matched']])]
    for i,(label,values) in enumerate(rows):
        a.scatter(values,i+np.linspace(-.08,.08,len(values)),s=33,color=C['trace'],alpha=.55)
        mean_marker(a,mean(values),i);a.annotate(f'{mean(values):+.3f}',(mean(values),i),xytext=(0,-21),textcoords='offset points',ha='center',fontweight='bold',fontsize=11)
    a.axvline(0,color=C['muted'],lw=1);a.axvline(.1,color=C['contrib'],ls='--',lw=1.5,label='+0.10 dB gate')
    a.set(yticks=[0,1],yticklabels=[r[0] for r in rows],ylim=(1.5,-.5),title='A  Trace deletion − Taming deletion',xlabel='Paired PSNR change [dB]')
    a.legend(loc='lower right',fontsize=10);style(a)
    runs={(r['scene'],r['arm']):r for r in d['trace_screen']}
    for i,(score,label,col) in enumerate([('taming','Taming',C['taming']),('trace','Trace',C['trace']),
          ('trace_soft','Soft trace',C['trace_light']),('random','Random',C['random']),('gradient','Gradient',C['gradient'])]):
        values=[]
        for scene,off,marker in [('bonsai',-.08,'o'),('kitchen',.08,'s')]:
            value=runs[scene,score]['PSNR']-runs[scene,'gradient']['PSNR'];values.append(value)
            b.scatter(value,i+off,s=48,color=col,marker=marker,edgecolors=C['muted'] if score=='trace_soft' else 'white',linewidth=.5)
        mean_marker(b,mean(values),i);b.text(1.02,i,f'{mean(values):+.3f}',transform=b.get_yaxis_transform(),va='center',fontsize=11)
    b.axvline(0,color=C['gradient'],lw=1.2);b.set(yticks=np.arange(5),yticklabels=['Taming','Trace','Soft trace','Random','Gradient'],ylim=(4.5,-.5),title='B  Fresh seed 3 · deletion-only control',xlabel='PSNR change vs gradient [dB]');style(b)
    b.legend(handles=[Line2D([0],[0],marker=m,color='none',markerfacecolor=C['muted'],label=s) for s,m in [('bonsai','o'),('kitchen','s')]],loc='lower left',fontsize=10)
    heading(fig,'Stronger controls bound the trace-quality claim','Separate experiments: the panels use different seeds, policies and references.',
        'A: turnover differs in the original screen; matched turnover uses amended common growth. Do not pool them.\nB: all five arms use common growth and a fixed deletion schedule. Both trace candidates fail the expansion rule.')
    fig.subplots_adjust(left=.17,right=.93,top=.80,bottom=.21,wspace=.62)
    export(fig,FIG/'fig8_trace_controls.png')


def main():
    d=write_data()
    memory(d);storage(d);roles(d);posthoc(d);compression(d);trace_controls(d)


if __name__=='__main__':main()
