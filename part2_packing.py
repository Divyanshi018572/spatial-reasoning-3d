"""Part 2 — 3D Bin Packing (Tetris).

Usage:
    python part2_packing.py --items "Item List.json" --master 100 100 100 [--support 0.7] [--animate]

Outputs:
    - Console: placement table (id, pos, dims)
    - JSON: detailed placements
    - Animation: Matplotlib GIF showing sequential stacking
    - Interactive: Matplotlib 3D view of final packing
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from utils.io_utils import load_items, save_json
from utils.geom_utils import (find_position, fits_in_master, generate_candidates,
                              unique_rotations)
from utils.vis_utils import animate_packing, show_packing_interactive

log = logging.getLogger(__name__)

DEFAULT_MASTER = (100.0, 100.0, 100.0)
DEFAULT_SUPPORT = 0.7


def pack_all(items: list[dict],
             master: tuple[float, float, float] = DEFAULT_MASTER,
             support_thresh: float = DEFAULT_SUPPORT) -> list[dict]:
    """Place all items using greedy lowest-Z first-fit with rotations.

    Args:
        items: List of dicts with 'id', 'dims', 'type'
        master: (width, depth, height) of container
        support_thresh: fraction of bottom area that must be supported

    Returns:
        List of placement dicts with 'id', 'pos', 'placed_dims', 'type'
    """
    # Sort by volume descending (largest first), then max side descending
    sorted_items = sorted(items, key=lambda x: (
        -x["dims"][0] * x["dims"][1] * x["dims"][2],
        -max(x["dims"])
    ))

    placed: list[tuple[float, float, float, float, float, float]] = []
    placements = []

    for item in sorted_items:
        item_id = item["id"]
        item_dims = tuple(item["dims"])
        item_type = item.get("type", "unknown")

        result = find_position(item_dims, placed, master, support_thresh)

        if result is None:
            log.warning("Item %s (%s) UNPLACEABLE — tried all positions/rotations", item_id, item_dims)
            placements.append({
                "id": item_id,
                "type": item_type,
                "dims": item_dims,
                "pos": None,
                "placed_dims": None,
                "placed": False
            })
            continue

        pos, rot_dims = result
        box = (*pos, *rot_dims)
        placed.append(box)

        placement = {
            "id": item_id,
            "type": item_type,
            "dims": item_dims,
            "pos": list(pos),
            "placed_dims": list(rot_dims),
            "placed": True
        }
        placements.append(placement)

        log.info("Placed id=%s type=%s at %s with dims %s", item_id, item_type, pos, rot_dims)

    return placements


def validate_placements(placements: list[dict], master: tuple[float, float, float]) -> tuple[bool, list[str]]:
    """Validate all placements: bounds, no overlap, support."""
    from utils.geom_utils import boxes_overlap, is_supported

    errors = []
    placed_boxes = [p for p in placements if p.get("placed")]
    boxes = [(p["pos"][0], p["pos"][1], p["pos"][2],
              p["placed_dims"][0], p["placed_dims"][1], p["placed_dims"][2])
             for p in placed_boxes]

    # Bounds check
    mx, my, mz = master
    for p in placed_boxes:
        x, y, z = p["pos"]
        dx, dy, dz = p["placed_dims"]
        if not (x >= 0 and y >= 0 and z >= 0 and
                x + dx <= mx + 1e-6 and y + dy <= my + 1e-6 and z + dz <= mz + 1e-6):
            errors.append(f"Item {p['id']}: out of bounds at {p['pos']} with dims {p['placed_dims']}")

    # Overlap check
    for i, a in enumerate(boxes):
        for j, b in enumerate(boxes[i+1:], i+1):
            if boxes_overlap(a, b):
                errors.append(f"Overlap: item {placed_boxes[i]['id']} vs {placed_boxes[j]['id']}")

    # Support check
    for i, p in enumerate(placed_boxes):
        pos = tuple(p["pos"])
        dims = tuple(p["placed_dims"])
        other_boxes = boxes[:i] + boxes[i+1:]
        if not is_supported(pos, dims, other_boxes, support_thresh=DEFAULT_SUPPORT):
            errors.append(f"Item {p['id']}: not supported at {pos}")

    return len(errors) == 0, errors


def print_summary(placements: list[dict], master: tuple[float, float, float]):
    """Print summary table."""
    placed = [p for p in placements if p.get("placed")]
    unplaced = [p for p in placements if not p.get("placed")]

    total_vol = sum(p["placed_dims"][0] * p["placed_dims"][1] * p["placed_dims"][2] for p in placed)
    master_vol = master[0] * master[1] * master[2]
    fill_pct = 100 * total_vol / master_vol

    print(f"\n{'='*60}")
    print(f"PACKING SUMMARY")
    print(f"{'='*60}")
    print(f"Master box: {master[0]} x {master[1]} x {master[2]} (vol={master_vol:.0f})")
    print(f"Items placed: {len(placed)} / {len(placements)}")
    print(f"Fill volume: {total_vol:.0f} / {master_vol:.0f} ({fill_pct:.1f}%)")

    if unplaced:
        print(f"\nUNPLACED ({len(unplaced)}):")
        for p in unplaced:
            print(f"  id={p['id']} type={p['type']} dims={p['dims']}")

    print(f"\nPLACEMENTS:")
    print(f"{'ID':>3}  {'Type':>14}  {'Pos (x,y,z)':>25}  {'Dims (dx,dy,dz)':>20}")
    print("-" * 70)
    for p in placed:
        pos_str = f"({p['pos'][0]:.1f},{p['pos'][1]:.1f},{p['pos'][2]:.1f})"
        dims_str = f"({p['placed_dims'][0]:.1f},{p['placed_dims'][1]:.1f},{p['placed_dims'][2]:.1f})"
        print(f"{p['id']:>3}  {p['type']:>14}  {pos_str:>25}  {dims_str:>20}")


def main():
    parser = argparse.ArgumentParser(description="Part 2: 3D Bin Packing")
    parser.add_argument("--items", required=True, help="Path to Item List.json")
    parser.add_argument("--master", nargs=3, type=float, default=DEFAULT_MASTER,
                        help="Master box dimensions (W D H)")
    parser.add_argument("--support", type=float, default=DEFAULT_SUPPORT,
                        help="Support threshold (0-1)")
    parser.add_argument("--output", default="outputs/part2_placements.json",
                        help="Output JSON path")
    parser.add_argument("--animate", action="store_true",
                        help="Save animation GIF")
    parser.add_argument("--animate-out", default="outputs/packing_animation.gif",
                        help="Animation output path")
    parser.add_argument("--show", action="store_true",
                        help="Show interactive 3D view at end")
    parser.add_argument("--verbose", "-v", action="store_true", help="Debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    items = load_items(args.items)
    master = tuple(args.master)

    log.info("Packing %d items into %s with support=%.1f", len(items), master, args.support)

    placements = pack_all(items, master, args.support)

    valid, errors = validate_placements(placements, master)
    if valid:
        log.info("All validations PASSED")
    else:
        log.error("VALIDATION ERRORS:")
        for e in errors:
            log.error("  %s", e)

    print_summary(placements, master)

    save_json(placements, args.output)

    if args.animate:
        placed_only = [p for p in placements if p.get("placed")]
        if placed_only:
            animate_packing(placed_only, master, args.animate_out)

    if args.show:
        placed_only = [p for p in placements if p.get("placed")]
        if placed_only:
            show_packing_interactive(placed_only, master)

    log.info("Done. Results saved to %s", args.output)


if __name__ == "__main__":
    main()