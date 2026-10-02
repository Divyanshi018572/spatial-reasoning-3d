# 10 — Testing & Validation

Run these BEFORE recording. All must pass.

## 1. Part 1 Tests (`tests/test_obb.py`)

| # | Test | How | Pass Criteria |
|---|------|-----|---------------|
| T1.1 | All files load | `load_mesh` on 3 OBJs | vertices >100 each, no NaN |
| T1.2 | OBB valid | `compute_obb` | extents >0, `R` orthonormal (`R@R.T≈I`, `det≈1`) |
| T1.3 | Cube square | CUBE extents | `max/min <1.02` |
| T1.4 | Cylinder round | CYLINDER extents | two dims within 3% |
| T1.5 | OBB tighter | Teapot | `vol_OBB < vol_AABB` |
| T1.6 | Determinism | run twice | same dims within 1e-6 |

```bash
pytest tests/test_obb.py -v
```

## 2. Part 2 Tests (`tests/test_packing.py`)

| # | Test | How | Pass Criteria |
|---|------|-----|---------------|
| T2.1 | JSON ingest | load `Item List.json` | 20 items, all dims>0 |
| T2.2 | All placed | `pack_all` | 20 placed, 0 unplaced |
| T2.3 | Bounds | each box | `x+dx≤100` etc. |
| T2.4 | No overlap | 190 pairs | `boxes_overlap==False` for all |
| T2.5 | Supported | each `z>0` | `is_supported==True` (≥0.7) |
| T2.6 | Determinism | run twice | identical placements |

```bash
pytest tests/test_packing.py -v
```

## 3. Manual Visual Checks
- [ ] Part 1 viewer: red box hugs mesh, no big empty margin; rotate 360° in video.
- [ ] Part 2 animation: blocks appear 1-by-1, none flicker/intersect, final fill looks compact, floor layer filled first.
- [ ] Console visible in recording shows dims + coords (proof, not just visuals).

## 4. Failure Playbook
- OBB looks loose → you used AABB by mistake; switch to `get_oriented_bounding_box`.
- Teapot OBB flips between runs → fix random seed / use all vertices, not sampled subset.
- Item floats → raise `SUPPORT_THRESH` to 0.8 or require center support.
- Item unplaced though space exists → check rotation permutations + candidate dedup logic.
- Viewer crashes (Open3D GUI) → fallback to Trimesh + Matplotlib screenshot path.
