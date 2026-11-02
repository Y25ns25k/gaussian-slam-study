#!/usr/bin/env python3
"""Recompute selected public comparisons. CPU only; Python standard library.

This checks stored metric tables, not the underlying experiments. Missing pairs,
duplicate rows, or inconsistent voxel quotas fail rather than being averaged away.
"""
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SCENES = {"bonsai", "kitchen", "room", "train"}
PAIRS = {(scene, seed) for scene in SCENES for seed in (1, 2)}


def reject_constant(value):
    raise ValueError(f"Non-standard JSON constant: {value}; use null for unavailable data")


def load(name):
    return json.loads((RESULTS / name).read_text(), parse_constant=reject_constant)


def unique(rows, keys):
    result = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        if key in result:
            raise ValueError(f"Duplicate key: {key}")
        result[key] = row
    return result


def paired_difference(a, b, metric):
    if set(a) != PAIRS or set(b) != PAIRS:
        raise ValueError("Comparison requires exactly four scenes x two seeds in both arms")
    delta = [a[k][metric] - b[k][metric] for k in sorted(PAIRS)]
    return mean(delta), sum(d > 0 for d in delta)


def main():
    files = sorted(RESULTS.rglob("*.json"))
    for path in files:
        load(path.relative_to(RESULTS))
    print(f"Parsed {len(files)} strict JSON files. Summaries use stored metrics, not new runs.\n")

    memory = load("flow4dgs/memory_options.json")["rows"]
    for arm in ("options_off", "options_on"):
        rows = [r for r in memory if r["arm"] == arm]
        print(f"Flow4DGS {arm}: {sum(r['completed'] for r in rows)}/{len(rows)} complete")
    peaks = [r["profiled_peak_allocated_bytes"] / 2**30 for r in memory
             if r["profiled_peak_allocated_bytes"] is not None]
    print(f"  retained profiler peak: {min(peaks):.2f}–{max(peaks):.2f} GiB")

    storage = [load(f"flow4dgs/b1_posthoc_storage_r{i}.json")["results"] for i in (1, 2, 3)]
    dense = mean(r["dense"]["center_bytes"] for r in storage)
    compressed = mean(r["fb1_fb2"]["center_bytes"] for r in storage)
    print(f"Flow4DGS modeled centre-bank reduction (ratio of means): {100 * (1 - compressed/dense):.1f}%")
    for r in storage:
        for field in ("psnr", "ssim", "lpips", "dyn_psnr", "dyn_ssim", "dyn_lpips"):
            if r["dense"][field] != r["fb1_fb2"][field]:
                raise ValueError(f"Lossless scheme has differing stored {field}")
        if r["fb1_fb2"]["max_center_error_alive_m"] != 0:
            raise ValueError("Lossless scheme has nonzero alive-centre error")
    print("  stored metrics match; pixel-level render equality cannot be rechecked here")

    cells = load("taming_score_arms.json")["cells"]
    arms = {name: unique([r for r in cells if r["arm"] == name], ("scene", "seed"))
            for name in {r["arm"] for r in cells}}
    print("\nTaming at 35% retained budget (paired test-view PSNR):")
    for a, b in (("taming_grow_trace_prune", "taming"), ("trace", "trace_grow_taming_prune"),
                 ("trace_grow_taming_prune", "taming"), ("trace", "taming_grow_trace_prune"),
                 ("grad", "taming"), ("grad", "trace"), ("taming_grow_trace_prune", "grad"), ("uniform", "taming")):
        delta, wins = paired_difference(arms[a], arms[b], "psnr")
        print(f"  {a} - {b}: {delta:+.4f} dB, {wins}/8 positive pairs")

    post = load("posthoc_prune_rules.json")["rows"]
    print("\nFinished Taming models, no fine-tuning:")
    for share in (10, 20, 30):
        group = {name: unique([r for r in post if r["rule"] == f"{name}_low{share}%"], ("scene", "seed"))
                 for name in ("trace", "taming", "opacity", "random")}
        for name, rows in group.items():
            if set(rows) != PAIRS:
                raise ValueError(f"Incomplete post-hoc pairs: {name}, {share}%")
        print(f"  {share}% removal: " + ", ".join(f"{k} {mean(r['dpsnr'] for r in v.values()):+.3f} dB"
                                                  for k, v in group.items()))
        if share == 20:
            for baseline in ("opacity", "taming"):
                delta, wins = paired_difference(group["trace"], group[baseline], "dpsnr")
                print(f"    trace - {baseline}: {delta:+.3f} dB, {wins}/8 positive pairs")

    rows = [r for r in load("gslam_submap_compression.json")["rows"] if r["colour_fix"] and r["refine_iters"] == 50]
    refs = unique([r for r in rows if r["selection"] == "none"], ("scene",))
    selections = ("safe_final_voxel", "contrib_voxel", "contribmax_voxel", "hybrid_voxel", "opacity_voxel", "random_voxel")
    print("\nGaussian-SLAM: corrected, 50 iterations, mapping views; dB vs refine-only:")
    for share in (0.25, 0.5):
        for scene in ("room0", "office0", "room1"):
            arms_gs = unique([r for r in rows if r["scene"] == scene and r["nominal_share"] == share
                              and r["selection"] in selections], ("selection",))
            fractions = {r["removed"] for r in arms_gs.values()}
            if len(fractions) != 1:
                raise ValueError(f"Unmatched quotas: {scene}, {share}")
            ref = refs[(scene,)]["psnr"]
            detail = ", ".join(f"{k[0]} {r['psnr']-ref:+.3f}" for k, r in arms_gs.items())
            print(f"  {scene}, actual removal {100 * next(iter(fractions)):.2f}%: {detail}")

    sizes = load("gslam_storage_summary.json")["checkpoint_gib_rounded"]
    print(f"Room0 checkpoint saving from rounded GiB: {100*(1-sizes['trace_voxel_25']/sizes['refine_only']):.1f}%")
    last = load("splatam_memprof_room1.json")["rows"][-1]
    print(f"SplaTAM final sampled frame {last['frame']}: keyframes {last['keyframe_bytes']/2**30:.2f} GiB, "
          f"Gaussian params + tracked state {(last['param_bytes']+last['variable_bytes'])/2**30:.2f} GiB")
    lsg = load("lsg_kitti07_frontend.json")["rows"]
    print(f"LSG-SLAM front-end maximum: {max(r['peak_alloc_gib'] for r in lsg):.2f} GiB")


if __name__ == "__main__":
    main()
