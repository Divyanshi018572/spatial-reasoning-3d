"""I/O utilities for mesh and JSON loading."""

import json
import logging
from pathlib import Path
from typing import Any

import numpy as np

try:
    import open3d as o3d
    OPEN3D_AVAILABLE = True
except ImportError:
    OPEN3D_AVAILABLE = False

try:
    import trimesh
    TRIMESH_AVAILABLE = True
except ImportError:
    TRIMESH_AVAILABLE = False

log = logging.getLogger(__name__)


def load_mesh(path: str) -> tuple[Any, np.ndarray]:
    """Load mesh from .obj file, return (mesh_object, vertices_array).

    Tries Open3D first, falls back to Trimesh.
    """
    import warnings
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Mesh file not found: {path}")

    if OPEN3D_AVAILABLE:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                mesh = o3d.io.read_triangle_mesh(str(path))
            if mesh.has_vertices():
                vertices = np.asarray(mesh.vertices, dtype=np.float64)
                log.info("Loaded via Open3D: %s (verts=%d, faces=%d)", path.name, len(vertices), len(mesh.triangles))
                return mesh, vertices
            else:
                log.warning("Open3D loaded mesh but no vertices: %s", path)
        except Exception as e:
            log.warning("Open3D load failed: %s", e)

    if TRIMESH_AVAILABLE:
        try:
            mesh = trimesh.load(str(path), force="mesh", process=False)
            vertices = np.asarray(mesh.vertices, dtype=np.float64)
            log.info("Loaded via Trimesh: %s (verts=%d, faces=%d)", path.name, len(vertices), len(mesh.faces))
            return mesh, vertices
        except Exception as e:
            log.warning("Trimesh load failed: %s", e)

    raise RuntimeError(f"Failed to load mesh with Open3D or Trimesh: {path}")


def load_items(json_path: str) -> list[dict]:
    """Load item list from JSON file."""
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Item list not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Item list must be a JSON array")

    for item in data:
        if not all(k in item for k in ("id", "dims")):
            raise ValueError("Each item must have 'id' and 'dims'")
        if len(item["dims"]) != 3 or any(d <= 0 for d in item["dims"]):
            raise ValueError(f"Invalid dims for item {item['id']}: {item['dims']}")

    log.info("Loaded %d items from %s", len(data), path.name)
    return data


def save_json(data: Any, output_path: str) -> None:
    """Save data as pretty JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    log.info("Saved results to %s", path)