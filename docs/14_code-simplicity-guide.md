# 14 — Code Simplicity Guide (Human-Readable, Clean)

**Goal:** Code that a reviewer reads once and understands. No cleverness. No abstraction for its own sake.

## 1. Golden Rules

| Rule | Do | Don't |
|------|-----|-------|
| **One thing per function** | `def compute_obb(vertices): ...` | `def load_and_compute_and_visualize(): ...` |
| **Names explain intent** | `placed_boxes`, `support_threshold` | `pb`, `th`, `data` |
| **Flat over nested** | Return early, avoid `else` blocks | 4+ indentation levels |
| **Explicit over implicit** | `if z == 0: return True` | `return not z` |
| **Constants at top** | `MASTER_SIZE = 100` | `if x + dx > 100:` scattered |
| **Stdlib first** | `itertools.permutations` | Custom permutation recursion |

## 2. Function Template (Copy This)

```python
def find_position(item_dims: tuple[float, float, float],
                  placed: list[Box],
                  master: tuple[float, float, float],
                  support_thresh: float = 0.7) -> Placement | None:
    """
    Find lowest valid (x,y,z) for item_dims among candidate corners.

    Args:
        item_dims: (dx, dy, dz) of item in its local orientation.
        placed: Already-placed boxes as (x, y, z, dx, dy, dz).
        master: (W, D, H) of container.
        support_thresh: Fraction of bottom area that must rest on floor/boxes.

    Returns:
        Placement dict or None if no fit.
    """
    candidates = generate_candidates(placed, master)
    for cand in sorted(candidates, key=lambda c: (c[2], c[1], c[0])):  # lowest Z first
        for rot_dims in unique_rotations(item_dims):
            if fits_in_master(cand, rot_dims, master):
                if not overlaps_any(cand, rot_dims, placed):
                    if is_supported(cand, rot_dims, placed, support_thresh):
                        return make_placement(cand, rot_dims)
    return None
```

- **One screen** (≤50 lines). If longer → extract helpers.
- **Docstring tells WHY + types**, not line-by-line WHAT.

## 3. Data Structures (Simple, No Classes Unless Needed)

```python
# Just tuples + type aliases — no dataclasses, no Pydantic
Box = tuple[float, float, float, float, float, float]  # x, y, z, dx, dy, dz
Placement = dict  # {"id": int, "pos": [x,y,z], "placed_dims": [dx,dy,dz]}

# Example
placed: list[Box] = [(0, 0, 0, 30, 30, 30), (30, 0, 0, 30, 30, 30)]
```

## 4. Helpers — One Job Each

```python
def volume(dims): return dims[0] * dims[1] * dims[2]

def sorted_dims(dims): return tuple(sorted(dims, reverse=True))

def unique_rotations(dims):
    """All 6 axis permutations, deduped for cubes."""
    seen = set()
    for perm in itertools.permutations(dims):
        if perm not in seen:
            seen.add(perm)
            yield perm

def boxes_overlap(a: Box, b: Box) -> bool:
    ax, ay, az, adx, ady, adz = a
    bx, by, bz, bdx, bdy, bdz = b
    return not (ax + adx <= bx or bx + bdx <= ax or
                ay + ady <= by or by + bdy <= ay or
                az + adz <= bz or bz + bdz <= az)
```

## 5. Logging — Informative, Not Noisy

```python
import logging
log = logging.getLogger(__name__)

log.info("Placed item %s at %s with dims %s", item_id, pos, rot_dims)
log.warning("Item %s unplaceable — tried %d positions", item_id, tried)
```

No `print()`. No `f"..."` in log calls (use `%` formatting for lazy eval).

## 6. Main Scripts — Thin Wrappers

```python
# part1_obb.py
def main():
    args = parse_args()  # argparse
    for path in args.inputs:
        mesh = load_mesh(path)
        dims, vol = measure_obb(mesh)
        log.info("%s: %.2f x %.2f x %.2f | Vol=%.2f", path, *dims, vol)
        if args.view:
            visualize(mesh, dims)
        save_result(args.output, path, dims, vol)

if __name__ == "__main__":
    main()
```

- **All logic in functions**, `__main__` only wires I/O.
- Same for `part2_packing.py`.

## 7. Imports — Grouped, No Wildcards

```python
# stdlib
import argparse
import itertools
import json
import logging
from pathlib import Path

# third-party
import numpy as np
import open3d as o3d
import trimesh

# local
from utils.io_utils import load_mesh, load_items, save_json
from utils.geom_utils import compute_obb, boxes_overlap
from utils.vis_utils import draw_obb, animate_packing
```

## 8. Anti-Patterns To Avoid

| Anti-pattern | Fix |
|--------------|-----|
| `except: pass` | Catch specific exception, log, re-raise or handle |
| Magic numbers | `SUPPORT_THRESH = 0.7` at module top |
| `for i in range(len(x))` | `for item in x:` or `enumerate(x)` |
| Mutating args | Return new values; don't modify `placed` in place inside helper |
| Global state | Pass `placed`, `master`, `config` as parameters |

## 9. Reviewer Mental Model Check

After writing a function, ask:
- Can I explain this in one sentence to a peer?
- Does the name match what it *actually* returns?
- If I read this in 6 months, will I know why `support_thresh=0.7`?

If no → simplify.

## 10. File Length Targets

| File | Max Lines |
|------|-----------|
| `part1_obb.py` | 120 |
| `part2_packing.py` | 180 |
| Each `utils/*.py` | 100 |
| Tests | 80 each |

Exceed? You're doing too much in one file — split.