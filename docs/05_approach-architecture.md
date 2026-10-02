# 05 — Approach & Architecture

## 1. Overall Approach
1. **Verify → Measure → Pack → Visualize → Validate → Record.** No ML, no over-engineering.
2. Two standalone scripts sharing a `utils/` helper for logging + JSON I/O. Either script runs alone (evaluator may run only one).
3. Heuristics over optimal solvers — explainable in 2-minute video.

## 2. Repo Structure (Final)
```text
part1_obb.py              # CLI: python part1_obb.py --input CUBE.obj
part2_packing.py          # CLI: python part2_packing.py --items "Item List.json" --master 100 100 100
utils/
  __init__.py
  io_utils.py             # load_mesh, load_items, save_json
  geom_utils.py           # volume, overlap, support check
  vis_utils.py            # draw_obb, draw_packing
requirements.txt
outputs/
  part1_results.json
  part2_placements.json
  screenshots/
tests/
  test_obb.py
  test_packing.py
docs/ (you are here)
README.md
```

## 3. Data Flow

### Part 1
```text
.obj file → trimesh/open3d load → vertices (Nx3) → OBB (center,R,extent)
→ sorted L,W,H + volume → console + part1_results.json → viewer (mesh + red OBB lines)
```

### Part 2
```text
Item List.json → list[{id,dims}] → sort by volume desc
→ for each item: gen candidates → bounds/overlap/support check → pick (x,y,z,rot_dims)
→ placements list → validate all → animate 1-by-1 → part2_placements.json
```

## 4. Key Functions (Signatures)

```python
# part1
def load_mesh(path: str) -> tuple[mesh, vertices]: ...
def compute_obb(vertices: np.ndarray) -> tuple[center, R, extents]: ...
def obb_volume_and_dims(extents) -> tuple[volume, L, W, H]: ...
def visualize(mesh, obb) -> None: ...

# part2
def load_items(json_path: str) -> list[Item]: ...
def boxes_overlap(a: Box, b: Box) -> bool: ...
def is_supported(candidate: Box, placed: list[Box], tol=1e-6) -> bool: ...
def find_position(item_dims, placed, master) -> tuple[x,y,z,rot_dims] | None: ...
def pack_all(items, master) -> list[Placement]: ...
def animate(placements, master) -> None: ...
```

Types: `Box = (x,y,z,dx,dy,dz)`, `Placement = {id, dims, pos:[x,y,z], placed_dims:[dx,dy,dz]}`.

## 5. Error Handling Strategy
- Missing file → `FileNotFoundError` with helpful path + `sys.exit(2)`.
- Empty/degenerate mesh → log + skip, do not crash whole batch.
- Unplaceable item → return `None`, log item id + tried rotations, continue with rest (report fill).
- All errors go to `stderr` via `logging`, not bare `print`.

## 6. Logging
- `logging.basicConfig(level=INFO, format=%(levelname)s %(name)s: %(message)s)`
- Part 1 logs: `INFO part1: CUBE.obj dims=[..] vol=..`
- Part 2 logs: `INFO part2: placed id=8 at (0,0,0) rot=[30,30,30]`
