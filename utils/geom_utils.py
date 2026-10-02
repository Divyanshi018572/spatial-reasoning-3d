"""Geometry utilities: OBB, volume, overlap, support checks."""

import itertools
import logging
from typing import Sequence

import numpy as np

log = logging.getLogger(__name__)

# Type aliases
Box = tuple[float, float, float, float, float, float]  # x, y, z, dx, dy, dz
Extents = tuple[float, float, float]  # L, W, H (sorted descending)


def compute_obb_open3d(mesh) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute OBB using Open3D. Returns (center, R, extents)."""
    obb = mesh.get_oriented_bounding_box()
    center = np.asarray(obb.center, dtype=np.float64)
    R = np.asarray(obb.R, dtype=np.float64)
    extents = np.asarray(obb.extent, dtype=np.float64)
    return center, R, extents


def compute_obb_trimesh(mesh) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute OBB using Trimesh. Returns (center, R, extents)."""
    obb = mesh.bounding_box_oriented
    center = np.asarray(obb.centroid, dtype=np.float64)
    R = np.asarray(obb.transform[:3, :3], dtype=np.float64)
    extents = np.asarray(obb.extents, dtype=np.float64)
    return center, R, extents


def compute_obb_from_vertices(vertices: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fallback: compute OBB from vertices using PCA (deterministic)."""
    # Center
    center = vertices.mean(axis=0)
    centered = vertices - center

    # Covariance + eigenvectors
    cov = centered.T @ centered / len(centered)
    eigvals, eigvecs = np.linalg.eigh(cov)

    # Sort by eigenvalue descending (largest variance first)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    # Fix sign ambiguity for determinism: first non-zero component positive
    for i in range(3):
        if eigvecs[0, i] < 0:
            eigvecs[:, i] *= -1

    R = eigvecs  # columns are principal axes
    projected = centered @ R
    mins = projected.min(axis=0)
    maxs = projected.max(axis=0)
    extents = maxs - mins
    center = center + R @ ((mins + maxs) / 2)

    return center, R, extents


def sorted_extents(extents: np.ndarray) -> Extents:
    """Return extents sorted L >= W >= H."""
    return tuple(sorted(extents, reverse=True))  # type: ignore[return-value]


def volume_from_extents(extents: Extents) -> float:
    """Volume = L * W * H."""
    return extents[0] * extents[1] * extents[2]


def aabb_from_obb(center: np.ndarray, R: np.ndarray, extents: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Get AABB min/max of an OBB in world coordinates."""
    # 8 corners in local space
    local_corners = np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0],
        [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]
    ]) - 0.5
    local_corners *= extents
    world_corners = center + local_corners @ R.T
    return world_corners.min(axis=0), world_corners.max(axis=0)


# --- Packing geometry ---

def boxes_overlap(a: Box, b: Box) -> bool:
    """True if two AABBs overlap (strict intersection)."""
    ax, ay, az, adx, ady, adz = a
    bx, by, bz, bdx, bdy, bdz = b
    return not (
        ax + adx <= bx or bx + bdx <= ax or
        ay + ady <= by or by + bdy <= ay or
        az + adz <= bz or bz + bdz <= az
    )


def unique_rotations(dims: Sequence[float]) -> list[tuple[float, float, float]]:
    """All unique axis permutations of (dx, dy, dz)."""
    seen = set()
    rotations = []
    for perm in itertools.permutations(dims):
        if perm not in seen:
            seen.add(perm)
            rotations.append(perm)
    return rotations


def fits_in_master(pos: tuple[float, float, float],
                   dims: tuple[float, float, float],
                   master: tuple[float, float, float],
                   eps: float = 1e-9) -> bool:
    """Check if box at pos with dims fits inside master."""
    x, y, z = pos
    dx, dy, dz = dims
    mx, my, mz = master
    return (x + dx <= mx + eps) and (y + dy <= my + eps) and (z + dz <= mz + eps)


def generate_candidates(placed: list[Box], master: tuple[float, float, float]) -> list[tuple[float, float, float]]:
    """Generate candidate positions: origin + all placed box corners."""
    candidates = {(0.0, 0.0, 0.0)}
    for (x, y, z, dx, dy, dz) in placed:
        candidates.add((x + dx, y, z))
        candidates.add((x, y + dy, z))
        candidates.add((x, y, z + dz))

    # Filter inside master
    mx, my, mz = master
    valid = []
    for (x, y, z) in candidates:
        if x <= mx and y <= my and z <= mz:
            valid.append((x, y, z))
    return valid


def is_supported(pos: tuple[float, float, float],
                 dims: tuple[float, float, float],
                 placed: list[Box],
                 support_thresh: float = 0.7,
                 tol: float = 1e-6) -> bool:
    """Check if box at pos is supported (floor or ≥support_thresh area on boxes below)."""
    x, y, z = pos
    dx, dy, dz = dims

    if z <= tol:
        return True  # on floor

    # Bottom face of candidate
    bottom_z = z
    bottom_area = dx * dy
    if bottom_area <= 0:
        return False

    # Find supporting boxes (tops at bottom_z)
    supporting_area = 0.0
    for (px, py, pz, pdx, pdy, pdz) in placed:
        top_z = pz + pdz
        if abs(top_z - bottom_z) <= tol:
            # Overlap in XY
            ox = max(0.0, min(x + dx, px + pdx) - max(x, px))
            oy = max(0.0, min(y + dy, py + pdy) - max(y, py))
            supporting_area += ox * oy

    if supporting_area / bottom_area >= support_thresh:
        return True

    # Fallback: center + 2 opposite corners supported
    corners = [
        (x + dx/2, y + dy/2),  # center
        (x, y),                # 4 corners
        (x + dx, y),
        (x, y + dy),
        (x + dx, y + dy),
    ]
    supported_count = 0
    for cx, cy in corners:
        for (px, py, pz, pdx, pdy, pdz) in placed:
            if abs(pz + pdz - bottom_z) <= tol:
                if px <= cx <= px + pdx and py <= cy <= py + pdy:
                    supported_count += 1
                    break
    return supported_count >= 3  # center + 2 corners


def find_position(item_dims: tuple[float, float, float],
                  placed: list[Box],
                  master: tuple[float, float, float],
                  support_thresh: float = 0.7) -> tuple[tuple[float, float, float], tuple[float, float, float]] | None:
    """Find lowest valid (pos, rotated_dims) for item.

    Returns (pos, rot_dims) or None if no fit.
    """
    candidates = generate_candidates(placed, master)
    # Sort by lowest Z, then Y, then X
    candidates.sort(key=lambda c: (c[2], c[1], c[0]))

    for pos in candidates:
        for rot_dims in unique_rotations(item_dims):
            if not fits_in_master(pos, rot_dims, master):
                continue
            candidate_box = (*pos, *rot_dims)
            if any(boxes_overlap(candidate_box, p) for p in placed):
                continue
            if not is_supported(pos, rot_dims, placed, support_thresh):
                continue
            return pos, rot_dims
    return None