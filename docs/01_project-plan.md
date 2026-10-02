# 01 — Project Plan (Master)

## 1. Objective
Deliver 2 working Python scripts + 2 screen-recorded videos exactly as specified in `Assignment Details.pdf`.

## 2. Scope

### In-scope
- Part 1: `part1_obb.py` — load 3 `.obj`, compute OBB, print Volume + LxWxH, visualize mesh + OBB.
- Part 2: `part2_packing.py` — load `Item List.json`, place 20 items in 100³ box, enforce no-overlap + gravity, animate stacking.
- Docs, tests, videos, Drive links.

### Out-of-scope
- No ML training, no UI web app, no physics engine (Bullet/PyBullet) unless needed for validation.
- No modification of input `.obj` / `.json` semantics.

## 3. Inputs Inventory (Verified Locally)
- `CUBE.obj` (16.8 MB) + `CUBE (1).obj` (duplicate — use `CUBE.obj` only)
- `CYLINDER.obj` (6.5 MB) — PDF typo calls it `CYLINER.obj`
- `TEAPOT.obj` (4.9 MB)
- `Item List.json` — 20 items (see Section 6)

## 4. Milestones
- **M0 Setup (0.5 day):** Env + verify files load.
- **M1 Part 1 Done (1 day):** OBB values correct, visualization works, video 1 recorded.
- **M2 Part 2 Done (1.5–2 days):** All 20 placed, no overlap, supported, animation works, video 2 recorded.
- **M3 Polish + Submit (0.5 day):** Tests pass, README + Drive links, final check.

Total: **3–4 days** at relaxed pace, **1–2 days** if full-time.

## 5. File Map (To Be Created)
```text
./
  README.md
  requirements.txt
  part1_obb.py
  part2_packing.py
  Item List.json (given, do not rename)
  CUBE.obj / CYLINDER.obj / TEAPOT.obj (given)
  outputs/
    part1_results.json
    part2_placements.json
    screenshots/
  docs/ (this plan set)
```

## 6. Item List Summary (From File)
- 3x standard_box [20,20,20] (id 1-3)
- 2x flat_panel [50,50,10] (id 4-5)
- 2x long_beam [10,10,60] (id 6-7)
- 2x large_crate [30,30,30] (id 8-9)
- 4x medium_cube [15,15,15] (id 10-13)
- 4x small_filler [5,5,5] (id 14-17)
- 2x long_box [40,10,10] (id 18-19)
- 1x flat_box [25,25,10] (id 20)
- Total volume ≈ 164,500 / 1,000,000 = ~16.5% fill → all 20 MUST fit; focus is correctness of constraints, not ultra-optimal density.

## 7. Success Criteria
- Part 1 uses OBB API (`get_oriented_bounding_box` / `bounding_box_oriented`), prints sorted L≥W≥H + volume, shows red tight box in viewer.
- Part 2 reads JSON at runtime, outputs 20x (x,y,z,placed_dims), passes overlap + bounds + support checks, animation shows sequential stacking.
- 2 Drive videos are public-viewable and clearly show terminal + 3D window.

## 8. Risks + Mitigations
| Risk | Mitigation |
|------|------------|
| Large OBJ slow to load | Use trimesh + decimation for preview; keep original for measurement |
| OBB unstable on teapot | Use vertex-based OBB; fallback to convex-hull OBB |
| Packing fails / floats | Sort largest-first, lowest-Z candidate order, enforce support % |
| Video too large / private link | 720p OBS, test link in incognito |
