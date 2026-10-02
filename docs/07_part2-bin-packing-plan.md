# 07 — Part 2 Implementation Plan (3D Tetris Packing)

Strictly follows PDF Part 2: ingest `Item List.json` → place 20 items in 100³ → no overlap + gravity → animate.

## Step 1 — Ingest (Substeps)
1.1. CLI: `python part2_packing.py --items "Item List.json" --master 100 100 100 --support-thresh 0.7`
1.2. Load with `json.load`; validate: list len 20, each has `id:int`, `dims:[3 positive numbers]`.
1.3. Reject on: missing file, bad JSON, non-positive dims, item larger than master in all rotations → clear error.
1.4. Sort: volume descending, tie-break by max side descending. Keep original `id` for output.
1.5. Log sorted order.

## Step 2 — Placement Engine (Substeps)
2.1. Maintain `placed: list[Box]` where `Box=(x,y,z,dx,dy,dz)`.
2.2. Candidate generation:
   - Start set = `{(0,0,0)}`
   - After each placement at `(x,y,z,dx,dy,dz)`, add `(x+dx,y,z)`, `(x,y+dy,z)`, `(x,y,z+dz)`
   - Deduplicate + filter outside master.
2.3. Ordering: sort candidates by `(z, y, x)` ascending — lowest first.
2.4. Rotations: unique permutations of `(dx,dy,dz)` (6 max, fewer if cube/filler).
2.5. Feasibility checks per `(cand, rot)`:
   - **Bounds:** `x+dx<=100 and y+dy<=100 and z+dz<=100` (eps 1e-9).
   - **Overlap:** for all `p in placed`, require separated on ≥1 axis:
     ```python
     separated = (x+dx<=px or px+pdx<=x or y+dy<=py or py+pdy<=y or z+dz<=pz or pz+pdz<=z)
     ```
   - **Support:** if `z==0` → True. Else compute overlap area of bottom rect with tops of boxes where `pz+pdz==z` (±tol). Support ratio = `supported_area/(dx*dy)`. Require `>=0.7` (configurable) OR center-supported fallback.
2.6. Pick first feasible; append; log `id → (x,y,z) rot`.
2.7. If none feasible → log `UNPLACED id` + continue (should not happen at 16.5% fill).

## Step 3 — Animate One-by-One (Substeps)
3.1. Use Matplotlib 3D: fig + `ax.set_xlim(0,100)` etc., draw master wireframe cube.
3.2. Color map by `type`: standard_box, flat_panel, long_beam, large_crate, medium_cube, small_filler, long_box, flat_box.
3.3. For `i in 1..20`: add `Poly3DCollection` cuboid for placement `i`, pause 0.6s, update title `Placed {i}/20 — id={id}`.
3.4. Final view: rotate elevation/azimuth slowly for video; save `placements.json` + optional GIF via `FuncAnimation`.
3.5. Alternative: Open3D boxes if Matplotlib looks blocky — same data, different renderer.

## Step 4 — Output Format
```json
[
  {"id": 8, "dims": [30,30,30], "pos": [0,0,0], "placed_dims": [30,30,30]},
  {"id": 9, "dims": [30,30,30], "pos": [30,0,0], "placed_dims": [30,30,30]}
]
```
Plus console table + `fill_pct`, `unplaced: []`.

## Step 5 — Validation (Must Pass Before Recording)
- [ ] Count == 20 placed, 0 unplaced.
- [ ] All inside 100³.
- [ ] Pairwise overlap check passes (O(n²)=190 pairs).
- [ ] Support check passes for all `z>0`.
- [ ] Script reads `Item List.json` path arg — no hard-coded dims.

## Pseudocode
```python
items = sorted(load_items(...), key=volume, reverse=True)
placed = []
for it in items:
    for cand in sorted_candidates(placed):
        for rot in rotations(it.dims):
            if fits(cand, rot) and not overlaps(...) and supported(...):
                placed.append((cand, rot)); break
        else: continue
        break
animate(placed)
```
