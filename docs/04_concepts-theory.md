# 04 — Concepts & Theory (What Evaluator Wants To Hear)

## 1. 3D Mesh Basics
- `.obj` stores vertices `(x,y,z)` + faces. Scanner output = raw mesh, may be dense, non-watertight.
- **Point cloud** = vertices only. **Mesh** = vertices + connectivity. Both can yield a bounding box.

## 2. AABB vs OBB (Core Distinction for Part 1)
- **AABB (Axis-Aligned Bounding Box):** Sides parallel to world X/Y/Z. Computed via `min/max` of vertices. Fast but loose if object is rotated. PDF explicitly says **do NOT do this**.
- **OBB (Oriented Bounding Box):** Box allowed to rotate (position + rotation matrix `R` + extents). Minimizes volume.
  - How: Compute mean → covariance → PCA eigenvectors = box axes → project points → take min/max along each axis → size + center + `R`.
  - Open3D: `obb = mesh.get_oriented_bounding_box()` returns `center`, `R`, `extent`.
  - Metric: `Volume = L*W*H`, `Dims = sorted(extent, descending)`.
- **Demo talking point:** Show AABB vs OBB volume on Teapot — OBB must be smaller.

## 3. Volume & Dimensions
- `extents = [dx, dy, dz]` along OBB local axes. Sort `L≥W≥H` for consistent reporting.
- Cube check: all three ≈ equal. Cylinder check: two ≈ diameter, one ≈ height.

## 4. 3D Bin Packing (Part 2 Theory)
- **Problem:** Place 20 boxes in 100³ container minimizing waste. NP-hard — optimal solver is out-of-scope; greedy heuristic is expected and acceptable.
- **Our heuristic:**
  1. **Sort:** Largest volume first (Decreasing) — big crates/panels anchor the floor.
  2. **Candidate positions:** Origin + all `right/top/front` corners of placed boxes (corner-point method).
  3. **Order:** Lowest `z`, then lowest `y`, then lowest `x` — enforces gravity + tightness.
  4. **Rotations:** Try up to 6 permutations of `(dx,dy,dz)` at each candidate.
- **Rule 1 — No overlap:** Two AABBs overlap iff intervals overlap on ALL 3 axes. Test with separating-axis check.
- **Rule 2 — Gravity/support:** `z==0` = floor-supported. Else require support area: e.g. ≥70% of bottom face covered by tops of boxes at `z_below == z`, or center + 4 corners projected down hit a supporting box.
- **Rule 3 — Tightness:** Lowest-Z + corner-point implicitly minimizes height and gaps. Report fill % = `sum(item_vol)/1e6`.

## 5. Visualization Concepts
- Part 1: Mesh (shaded) + OBB as red `LineSet` (12 edges). Rotate camera to prove tightness.
- Part 2: Master Box wireframe + colored solid cuboids per `type`. Animate `i=1..20` sequential add. Color map by type (e.g. flat_panel=blue, beam=orange).

## 6. One-Line Explanations For Video
- Part 1: I compute covariance of vertices, get principal axes, project to get minimal rotating box.
- Part 2: I sort by volume, try lowest feasible corner with 6 rotations, reject overlaps and floating placements.
