"""Part 1 — Oriented Bounding Box Measurement.

Usage:
    python part1_obb.py --input CUBE.obj [--view]
    python part1_obb.py --all --input-dir . --output outputs/part1_results.json

Outputs:
    - Console: dimensions (L x W x H) and volume for each mesh
    - JSON: detailed results per file
    - Visualization: Open3D window with mesh + red OBB (if --view)
"""

import argparse
import logging
import sys
from pathlib import Path

import numpy as np

from utils.io_utils import load_mesh, save_json
from utils.geom_utils import (compute_obb_open3d, compute_obb_trimesh,
                              compute_obb_from_vertices, sorted_extents,
                              volume_from_extents)
from utils.vis_utils import draw_obb_open3d, draw_obb_fallback

log = logging.getLogger(__name__)

DEFAULT_FILES = ["CUBE.obj", "CYLINDER.obj", "TEAPOT.obj"]


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def measure_obb(mesh, vertices: np.ndarray) -> tuple[tuple[float, float, float], float, dict]:
    """Compute OBB, return (dims, volume, metadata)."""
    # Try Open3D first
    try:
        center, R, extents = compute_obb_open3d(mesh)
        method = "open3d"
    except Exception as e:
        log.warning("Open3D OBB failed: %s", e)
        try:
            center, R, extents = compute_obb_trimesh(mesh)
            method = "trimesh"
        except Exception as e2:
            log.warning("Trimesh OBB failed: %s", e2)
            center, R, extents = compute_obb_from_vertices(vertices)
            method = "pca_fallback"

    dims = sorted_extents(extents)
    volume = volume_from_extents(dims)

    meta = {
        "method": method,
        "center": center.tolist(),
        "rotation": R.tolist(),
        "extents_raw": extents.tolist(),
    }
    return dims, volume, meta


def process_file(filepath: str, view: bool = False) -> dict:
    """Process single .obj file, return result dict."""
    path = Path(filepath)
    log.info("Processing %s", path.name)

    mesh, vertices = load_mesh(filepath)
    dims, volume, meta = measure_obb(mesh, vertices)

    result = {
        "file": path.name,
        "dimensions": {"L": dims[0], "W": dims[1], "H": dims[2]},
        "volume": volume,
        **meta
    }

    log.info("%s: L=%.2f W=%.2f H=%.2f | Volume=%.2f (method=%s)",
             path.name, dims[0], dims[1], dims[2], volume, meta["method"])

    if view:
        try:
            if meta["method"] in ("open3d", "trimesh"):
                draw_obb_open3d(mesh, np.array(meta["center"]),
                                np.array(meta["rotation"]), np.array(meta["extents_raw"]))
            else:
                draw_obb_fallback(vertices, np.array(meta["center"]),
                                  np.array(meta["rotation"]), np.array(meta["extents_raw"]))
        except Exception as e:
            log.error("Visualization failed: %s", e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Part 1: OBB Measurement")
    parser.add_argument("--input", help="Single .obj file to process")
    parser.add_argument("--all", action="store_true", help="Process all default files")
    parser.add_argument("--input-dir", default=".", help="Directory for --all mode")
    parser.add_argument("--output", default="outputs/part1_results.json", help="Output JSON path")
    parser.add_argument("--view", action="store_true", help="Show 3D visualization")
    parser.add_argument("--verbose", "-v", action="store_true", help="Debug logging")
    args = parser.parse_args()

    setup_logging(args.verbose)

    if args.all:
        files = [str(Path(args.input_dir) / f) for f in DEFAULT_FILES]
    elif args.input:
        files = [args.input]
    else:
        parser.error("Either --input or --all required")

    results = []
    for f in files:
        try:
            results.append(process_file(f, view=args.view))
        except Exception as e:
            log.error("Failed to process %s: %s", f, e)
            results.append({"file": Path(f).name, "error": str(e)})

    save_json(results, args.output)
    log.info("Done. Results saved to %s", args.output)


if __name__ == "__main__":
    main()