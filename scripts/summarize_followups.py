#!/usr/bin/env python3
"""Recompute dated follow-up comparisons from public numeric records (CPU)."""
import hashlib
import json
import math
from pathlib import Path
from statistics import mean,median

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'results/followups'
METRICS=('PSNR','SSIM','LPIPS','depth_l1_mm')


def reject(x):raise ValueError('Nonstandard JSON: '+x)
def load(name):return json.loads((DATA/name).read_text(),parse_constant=reject)
def indexed(rows,keys):
    result={}
    for r in rows:
        k=tuple(r[x] for x in keys)
        if k in result:raise ValueError('Duplicate row: '+str(k))
        result[k]=r
    return result


def validate_timings(data,repetitions):
    phases=('score_seconds','selection_seconds','restore_prune_seconds','refine_seconds','closing_seconds')
    for c in data['components']:
        for arm,record in c['arms'].items():
            rows=[r for r in c['timing_records'] if r['arm']==arm]
            assert sorted(r['trial'] for r in rows)==list(range(repetitions))
            for k in phases:
                assert math.isclose(median(r[k] for r in rows),record['median'][k],abs_tol=1e-10)
            for r in rows:
                assert math.isclose(sum(r[k] for k in phases[:-1]),r['closing_seconds'],abs_tol=1e-8)
                assert r['count_after']==r['count_before']-r['pruned']
            views=next(r['views'] for r in rows if r['trial']==0)
            assert [v['frame_id'] for v in views]==c['keyframe_ids']
            for k in METRICS:assert math.isclose(mean(v[k] for v in views),record['quality'][k],abs_tol=1e-10)
    for p in data['prefix']:
        maps=data['prefix_details'][p['job']]
        assert math.isclose(sum(m['arms'][p['arm']]['median']['closing_seconds'] for m in maps),p['closing_seconds'],abs_tol=1e-10)
        assert math.isclose(sum(m['common_load_seconds'] for m in maps),p['load_prepare_seconds'],abs_tol=1e-10)
        assert math.isclose(p['mapping_seconds']+p['load_prepare_seconds']+p['closing_seconds'],p['accounted_seconds'],abs_tol=1e-10)
    print('Retained timing repetitions, phase sums, quality means and prefix accounting: consistent.')


def main():
    provenance=load('provenance.json')
    for record in provenance['records']+provenance['code']:
        path=ROOT/record['public_file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['public_sha256'],path
    print('Bundled numeric exports and independent helpers: SHA256 matches.')
    d=load('matched_turnover.json');rows=indexed(d['runs'],('scene','seed','arm'))
    assert len(rows)==8 and d['correctness']['all_exact_control_sequences_match']
    delta=[]
    for scene in ('bonsai','kitchen'):
        for seed in (1,2):
            a,b=rows[scene,seed,'trace'],rows[scene,seed,'taming']
            assert a['count']==b['count'] and a['pruned_total']==b['pruned_total']
            delta.append(a['PSNR']-b['PSNR'])
    print(f'Matched turnover: trace - Taming {mean(delta):+.6f} dB, {sum(x>0 for x in delta)}/4 positive pairs; gate {d["gate_passes"]}')
    d=load('trace_development.json');rows=indexed(d['runs'],('scene','seed','arm'))
    assert len(rows)==10 and not d['historical_metrics_pooled']
    for a,b in [('trace_soft','trace'),('trace_soft','gradient'),('trace','gradient'),('trace_soft','random')]:
        delta=[rows[s,3,a]['PSNR']-rows[s,3,b]['PSNR'] for s in ('bonsai','kitchen')]
        print(f'Fresh seed 3, {a} - {b}: {mean(delta):+.6f} dB')
    for candidate in ('trace','trace_soft'):
        gate=all(mean(rows[s,3,candidate]['PSNR']-rows[s,3,ref]['PSNR'] for s in ('bonsai','kitchen'))>0
                 and mean(rows[s,3,candidate]['LPIPS']-rows[s,3,ref]['LPIPS'] for s in ('bonsai','kitchen'))<=.002
                 for ref in ('taming','gradient','random'))
        assert gate==d['stage1_decision']['candidate_passes'][candidate]
    assert d['stage1_decision']['run_seed4']==any(d['stage1_decision']['candidate_passes'].values())
    print('Fixed candidate decision:',d['final_decision']['verdict'])
    d=load('slam_score_cost.json');validate_timings(d,5)
    def totals(components,arm):return sum(r['arms'][arm]['median']['closing_seconds'] for r in components)
    assert len(d['components'])==9 and len(d['native'])==12
    for a in ('contrib_voxel','contribmax_voxel'):
        print(f'Original resident closing trace vs {a}: {100*(totals(d["components"],"safe_final_voxel")/totals(d["components"],a)-1):+.3f}%')
    for scene in ('room0','office0'):
        x=[r['percent_change'] for r in d['prefix_comparisons'] if r['scene']==scene and r['reference']=='contrib_voxel']
        assert len(x)==3
        print(f'Original mapping + compression vs contrib sum, {scene}: {mean(x):+.3f}%')
    path=DATA/'slam_implementation.json'
    if not path.exists():raise RuntimeError('Implementation export missing: release is incomplete')
    d=load(path.name);validate_timings(d,5)
    assert len(d['components'])==9 and len(d['native'])==18 and len(d['prefix'])==48
    for c in d['components']:
        assert c['parity']['passed']
        for a in c['arms'].values():assert a['count_after']==c['count_before']-c['pruned']
    fast=totals(d['components'],'safe_final_fast_voxel')
    print(f'Optimized resident trace closing: sum of 9 map medians = {fast:.6f} s')
    for a in ('safe_final_voxel','contrib_voxel','contrib_fast_voxel','contribmax_fast_voxel'):
        print(f'  vs {a}: {100*(fast/totals(d["components"],a)-1):+.3f}%')
    for scene in ('room0','office0'):
        for seed in (0,1,2):
            rows=[r for r in d['native'] if r['scene']==scene and r['seed']==seed]
            assert len(rows)==3 and all(r['gt_pose_check'] and r['runtime']['frame_count']==100 for r in rows)
            assert len({tuple((x['iterations_argument'],x['forward_backward_steps'],tuple(x['keyframe_ids'])) for x in r['optimization_calls']) for r in rows})==1
        for reference in ('safe_final_voxel','contrib_fast_voxel','contribmax_fast_voxel'):
            x=[r['percent_change'] for r in d['prefix_comparisons'] if r['scene']==scene and r['reference']==reference]
            assert len(x)==3
            print(f'Optimized mapping + compression, {scene}, vs {reference}: {mean(x):+.3f}% (3 paired seeds)')
    print('Same-input original-mask checks:',d['same_input_mask_checks'])
    assert not d['sampling_frequency_changed'] and not d['online_tracking_fps_claim']
    print('Quality guards (not equivalence tests):')
    for r in d['quality_comparisons']:print(' ',r['scene'],r['reference'],r['delta'],r['passed'])
    print('These are recorded phase/compute sums, not a full SLAM FPS or FLOP comparison.')


if __name__=='__main__':main()
