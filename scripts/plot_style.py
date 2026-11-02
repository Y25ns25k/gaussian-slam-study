"""Shared scientific figure style and vector/raster export."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'trace': '#2563EB', 'trace_light': '#A5C4FD', 'contrib': '#D97706',
          'contrib_light': '#FAD5A5', 'contribmax': '#A85408', 'taming': '#0F766E',
          'gradient': '#7C3AED', 'opacity': '#667085', 'random': '#ADB5C3',
          'ink': '#172B4D', 'muted': '#5B677A', 'grid': '#E5EAF0', 'growth': '#D97706'}
SCORE_COLOR = {'safe_final_voxel': COLORS['trace'], 'contrib_voxel': COLORS['contrib'],
               'contribmax_voxel': COLORS['contribmax'], 'hybrid_voxel': COLORS['taming'],
               'opacity_voxel': COLORS['opacity'], 'random_voxel': COLORS['random']}
LABELS = {'safe_final_voxel': 'Trace', 'contrib_voxel': 'Contribution sum',
          'contribmax_voxel': 'Contribution max', 'hybrid_voxel': 'Hybrid rank',
          'opacity_voxel': 'Opacity', 'random_voxel': 'Random'}
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12, 'axes.titlesize':14,
    'axes.labelsize':12, 'axes.titleweight':'bold', 'figure.facecolor':'white',
    'axes.facecolor':'white', 'savefig.facecolor':'white', 'text.color':COLORS['ink'],
    'axes.labelcolor':COLORS['ink'], 'xtick.color':COLORS['muted'], 'ytick.color':COLORS['ink'],
    'axes.edgecolor':'#C8D1DE', 'axes.spines.top':False, 'axes.spines.right':False,
    'axes.axisbelow':True, 'grid.color':COLORS['grid'], 'grid.linewidth':.8,
    'legend.frameon':False, 'legend.fontsize':11, 'svg.fonttype':'none',
    'svg.hashsalt':'gaussian-slam-study', 'lines.linewidth':2.2})


def style(ax, axis='x'):
    ax.grid(axis=axis)
    ax.tick_params(length=0, pad=7)


def heading(fig, title, subtitle, footnote=None):
    fig.suptitle(title, x=.03, y=.985, ha='left', fontsize=18, fontweight='bold')
    fig.text(.03,.935,subtitle,ha='left',va='top',fontsize=11.5,color=COLORS['muted'])
    if footnote:
        fig.text(.03,.015,footnote,ha='left',va='bottom',fontsize=10,color=COLORS['muted'])


def export(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path.with_suffix('.png'), dpi=180, bbox_inches='tight')
    fig.savefig(path.with_suffix('.svg'), bbox_inches='tight', metadata={'Date':None})
    plt.close(fig)
    print('wrote',path.with_suffix('.png').name,'and SVG')


def mean_marker(ax, x, y):
    ax.scatter(x,y,marker='D',s=58,color=COLORS['ink'],edgecolors='white',linewidth=.8,zorder=5)
