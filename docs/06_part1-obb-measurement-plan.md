# 06 — Part 1 Implementation Plan (OBB Measurement)

Strictly follows PDF Part 1: read 3 files → OBB → Volume + LxWxH → visualize.

## Step 1 — Load Mesh (Substeps)
1.1. CLI: `python part1_obb.py --input CUBE.obj [--viewer open3d]`
1.2. Try Open3D first: `o3d.io.read_triangle_mesh(path)`; check `has_vertices()`.
1.3. Fallback to Trimesh: `trimesh.load(path, force='mesh')`.
1.4. Log: vertex count, face count, `is_watertight`, AABB for reference only.
1.5. Normalize: convert to `np.ndarray (N,3)` float64; remove NaN/inf rows.

## Step 2 — Compute OBB (Substeps)
2.1. **Primary:** `obb = mesh.get_oriented_bounding_box()` (Open3D) — robust PCA inside.
2.2. **Fallback:** `trimesh` → `mesh.bounding_box_oriented` → `extents`, `transform`.
2.3. Extract: `center = obb.center`, `R = obb.R`, `extents = obb.extent`.
2.4. Sort dims descending: `L,W,H = sorted(extents, reverse=True)`.
2.5. Volume: `V = L*W*H`.
2.6. Save per file: `{file, L,W,H, volume, center:[..], R:[3x3]}` to `outputs/part1_results.json`.
2.7. Console output example:
```text
CUBE.obj: Dims (LxWxH) = 20.00 x 20.00 x 20.00 | Volume = 8000.00
```

## Step 3 — Visualize (Substeps)
3.1. Build OBB LineSet: `o3d.geometry.LineSet.create_from_oriented_bounding_box(obb)`; paint red.
3.2. Show: `o3d.visualization.draw_geometries([mesh, obb_lines], window_name=file)`.
3.3. In video: rotate view, zoom to show gap is minimal; toggle AABB (gray) vs OBB (red) to prove OBB tighter — optional but convincing.
3.4. Headless fallback: save screenshot via `vis.capture_screen_image()` or matplotlib 3D scatter of vertices + box edges.

## Step 4 — Batch + Edge Cases
4.1. Loop over `["CUBE.obj","CYLINDER.obj","TEAPOT.obj"]` in one run with `--all` flag.
4.2. Handle: duplicate `CUBE (1).obj` — document to use `CUBE.obj` only.
4.3. Handle: large CUBE (16MB) — downsample only for display, never for measurement.
4.4. Handle: non-manifold teapot — use vertex OBB, not voxelization.

## Step 5 — Validation (Must Pass Before Recording)
- [ ] Cube: `L≈W≈H` within 2%.
- [ ] Cylinder: two dims equal (diameter) within 3%, third distinct (height).
- [ ] Teapot: `vol_OBB < vol_AABB` (prove with numbers in console).
- [ ] All 3 print Volume + Dims without crash.

## Pseudocode
```python
for f in FILES:
    verts = load_mesh(f)
    center, R, ext = compute_obb(verts)
    L,W,H = sorted(ext, reverse=True)
    print(f"{f}: {L:.2f} x {W:.2f} x {H:.2f} | V={L*W*H:.2f}")
    visualize(f, center, R, ext)
```
