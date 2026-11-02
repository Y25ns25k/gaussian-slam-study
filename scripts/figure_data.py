"""Derive chart values from retained measurements, without running experiments."""
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'


def load(name):
    return json.loads((RESULTS / name).read_text())


def build():
    data = {'schema_version': 1, 'scope': 'Derived chart values; original experiment JSON is unchanged.', 'sources': {}}
    names = ['splatam_memprof_room1.json', 'lsg_kitti07_frontend.json',
             'flow4dgs/memory_options.json', 'taming_score_arms.json', 'posthoc_prune_rules.json',
             'gslam_submap_compression.json', 'followups/matched_turnover.json',
             'followups/trace_development.json', 'followups/slam_score_cost.json',
             'followups/slam_implementation.json']
    names += [f'flow4dgs/b1_posthoc_storage_r{i}.json' for i in (1, 2, 3)]
    for name in names:
        data['sources'][name] = hashlib.sha256((RESULTS / name).read_bytes()).hexdigest()
    data['memory'] = {'splatam': load(names[0])['rows'], 'lsg': load(names[1])['rows'],
                      'flow_options': load('flow4dgs/memory_options.json')['rows']}
    runs = [load(f'flow4dgs/b1_posthoc_storage_r{i}.json')['results'] for i in (1, 2, 3)]
    storage = []
    for key, label, exact in [('dense', 'Dense bank', True), ('fb1', 'Drop pre-birth slots', True),
         ('fb2', 'Merge unchanged copies', True), ('fb1_fb2', 'Combine both', True),
         ('fb3_eps5mm', 'Merge within 5 mm', False), ('fb3_eps10mm', 'Merge within 10 mm', False),
         ('fb3_eps20mm', 'Merge within 20 mm', False)]:
        storage.append({'key': key, 'label': label, 'exact_scheme': exact,
            'mib': [r[key]['center_bytes']/2**20 for r in runs],
            'dpsnr': [r[key]['psnr']-r['dense']['psnr'] for r in runs]})
    data['storage'] = storage
    arms = defaultdict(dict)
    for r in load('taming_score_arms.json')['cells']:
        arms[r['arm']][(r['scene'], r['seed'])] = r['psnr']
    contrasts = [('Change deletion\nTaming growth', 'taming_grow_trace_prune', 'taming', 'pruning'),
        ('Change deletion\nTrace growth', 'trace', 'trace_grow_taming_prune', 'pruning'),
        ('Change growth\nTaming deletion', 'trace_grow_taming_prune', 'taming', 'growth'),
        ('Change growth\nTrace deletion', 'trace', 'taming_grow_trace_prune', 'growth'),
        ('Trace in both roles\nvs Taming in both', 'trace', 'taming', 'control'),
        ('Gradient in both roles\nvs Taming in both', 'grad', 'taming', 'control'),
        ('Uniform in both roles\nvs Taming in both', 'uniform', 'taming', 'control')]
    roles = []
    for label, a, b, role in contrasts:
        assert set(arms[a]) == set(arms[b]) and len(arms[a]) == 8
        roles.append({'label': label, 'candidate': a, 'reference': b, 'role': role,
            'pairs': [{'scene': s, 'seed': seed, 'delta': arms[a][s, seed]-arms[b][s, seed]}
                      for s, seed in sorted(arms[a])]})
    data['roles'] = roles
    post = load('posthoc_prune_rules.json')['rows']
    data['posthoc'] = []
    for score in ('trace', 'taming', 'opacity', 'random'):
        for share in (10, 20, 30):
            rows = sorted([r for r in post if r['rule'] == f'{score}_low{share}%'], key=lambda r:(r['scene'], r['seed']))
            assert len(rows) == 8
            data['posthoc'].append({'score': score, 'share': share,
                'pairs': [{'scene': r['scene'], 'seed': r['seed'], 'delta': r['dpsnr']} for r in rows]})
    rows = [r for r in load('gslam_submap_compression.json')['rows'] if r['colour_fix'] and r['refine_iters'] == 50]
    refs = {r['scene']: r for r in rows if r['selection'] == 'none'}
    scores = ('safe_final_voxel', 'contrib_voxel', 'contribmax_voxel', 'hybrid_voxel', 'opacity_voxel', 'random_voxel')
    data['compression'] = [{'scene': r['scene'], 'score': r['selection'], 'nominal_removed': r['nominal_share'],
        'removed': r['removed'], 'dpsnr': r['psnr']-refs[r['scene']]['psnr']}
        for r in rows if r['selection'] in scores and r['nominal_share'] in (.25, .5)]
    data['matched'] = load('followups/matched_turnover.json')['cells']
    data['trace_screen'] = load('followups/trace_development.json')['runs']
    for file, label, arms_wanted, trace in [
        ('followups/slam_score_cost.json', 'original',
         ['safe_final_voxel', 'contrib_voxel', 'contribmax_voxel', 'opacity_voxel', 'random_voxel'], 'safe_final_voxel'),
        ('followups/slam_implementation.json', 'optimized',
         ['safe_final_voxel', 'safe_final_fast_voxel', 'contrib_voxel', 'contrib_fast_voxel', 'contribmax_fast_voxel', 'opacity_fast_voxel'], 'safe_final_fast_voxel')]:
        raw = load(file)
        components = []
        for arm in arms_wanted:
            maps = [{'job': c['job'], 'scene': c['scene'], 'seconds': c['arms'][arm]['median']['closing_seconds']}
                    for c in raw['components']]
            components.append({'arm': arm, 'maps': maps, 'mean_seconds': mean(m['seconds'] for m in maps),
                'phase_means': {k: mean(c['arms'][arm]['median'][k] for c in raw['components']) for k in
                    ('score_seconds', 'selection_seconds', 'restore_prune_seconds', 'refine_seconds')}})
        data[label] = {'closing': components, 'prefix': raw['prefix_comparisons'],
                       'native': raw['native'], 'trace_arm': trace}
        if label == 'optimized':
            data[label]['native_comparisons'] = raw['native_comparisons']
            data[label]['quality'] = raw['quality_comparisons']
            data[label]['mask_checks'] = raw['same_input_mask_checks']
    return data


def write_data():
    data = build()
    (RESULTS / 'figure_data.json').write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')
    return data


if __name__ == '__main__':
    write_data()
    print('Derived figure data rebuilt from original metrics.')
