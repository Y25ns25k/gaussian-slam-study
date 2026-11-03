#!/usr/bin/env python3
"""Recompute every paired difference and count invariant in the online metric extract."""
import json
import math
from pathlib import Path
from statistics import mean

ROOT=Path(__file__).resolve().parents[1]


def close(a,b):
    if not math.isclose(a,b,abs_tol=1e-10,rel_tol=1e-10):raise ValueError((a,b))


def main():
    data=json.loads((ROOT/'results/online_budget25.json').read_text())
    rows={(r['seed'],r['arm']):r for r in data['rows']}
    if len(data['rows'])!=8 or set(rows)!={(s,a) for s in [0,1] for a in ['baseline','area','trace','random']}:
        raise ValueError('Expected exactly two seeds and four unique arms')
    for seed in [0,1]:
        baseline=rows[seed,'baseline']; reference=baseline['budget_events'];same=None
        if len(reference)!=51:raise ValueError('Incomplete baseline')
        for arm in ['baseline','area','trace','random']:
            r=rows[seed,arm];events=r['budget_events']
            if len(events)!=51:raise ValueError('Incomplete arm')
            if r['gaussian_count']!=events[-1]['after']:raise ValueError('Saved count mismatch')
            for i,e in enumerate(events):
                if e['frame_index']!=i or e['before']-e['removed']!=e['after']:raise ValueError('Invalid event accounting')
                if i and e['before']!=events[i-1]['after']+e['birth_count']:raise ValueError('Hidden count change')
                if arm!='baseline' and i and e['after']!=reference[i]['after']*3//4:raise ValueError('Budget violation')
                if arm!='baseline' and i and e['eligible_count']<e['removed']:raise ValueError('Infeasible pool')
            if arm!='baseline':
                counts=[tuple(e[k] for k in ['frame_index','before','after','removed','birth_count']) for e in events]
                if same is not None and counts!=same:raise ValueError('Actual deletion or birth mismatch')
                same=counts
            for mode,metrics in r['quality'].items():
                frames=[f for f in r['per_frame'] if f['mode']==mode]
                if len(frames)!=11:raise ValueError('Missing evaluation view')
                for name,value in metrics.items():close(value,mean(f[name] for f in frames))
            print(f'Seed {seed} {arm:8}: N={r["gaussian_count"]:,}, wall={r["frontend_wall_seconds"]:.2f}s, '
                  f'selection={sum(e["selection_seconds"] for e in events):.3f}s')
    differences=data['paired_trace_differences']
    if len(differences)!=6 or len({(d['seed'],d['control']) for d in differences})!=6:raise ValueError('Missing pairs')
    for d in differences:
        a=rows[d['seed'],'trace'];b=rows[d['seed'],d['control']]
        close(d['psnr_delta'],a['quality']['estimated_camera']['psnr']-b['quality']['estimated_camera']['psnr'])
        close(d['lpips_delta'],a['quality']['estimated_camera']['lpips']-b['quality']['estimated_camera']['lpips'])
        close(d['wall_change_percent'],100*(a['frontend_wall_seconds']/b['frontend_wall_seconds']-1))
        close(d['ate_delta_cm'],a['ate_rmse_cm']-b['ate_rmse_cm'])
        print(f'Seed {d["seed"]} trace − {d["control"]}: PSNR {d["psnr_delta"]:+.4f}dB, '
              f'LPIPS {d["lpips_delta"]:+.5f}, wall {d["wall_change_percent"]:+.3f}%, ATE {d["ate_delta_cm"]:+.3f}cm')
    print('Compression loss and across-score ranges (estimated cameras):')
    for seed in [0,1]:
        def metric(arm,name):return rows[seed,arm]['quality']['estimated_camera'][name]
        for name in ['psnr','lpips']:
            values=[metric(arm,name) for arm in ['area','trace','random']]
            loss=metric('trace',name)-metric('baseline',name)
            gap=metric('trace',name)-metric('area',name)
            print(f'Seed {seed} {name}: trace-reference {loss:+.6f}, across-score range {max(values)-min(values):.6f}, '
                  f'abs(loss)/abs(trace-area) {abs(loss/gap):.3f}')
    print('Verified every-event budget, equal actual births/deletions, per-view arithmetic and all paired differences.')
    print('Selection time excludes earlier gradient collection and visibility query. Two seeds do not establish superiority/equivalence.')


if __name__=='__main__':main()
