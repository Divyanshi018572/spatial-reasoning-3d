"""Tests for Part 1: OBB Measurement."""

import pytest
import numpy as np

from utils.geom_utils import (compute_obb_from_vertices, sorted_extents,
                              volume_from_extents, aabb_from_obb)


def test_sorted_extents():
    assert sorted_extents(np.array([1.0, 3.0, 2.0])) == (3.0, 2.0, 1.0)
    assert sorted_extents(np.array([5.0, 5.0, 5.0])) == (5.0, 5.0, 5.0)


def test_volume():
    assert volume_from_extents((2.0, 2.0, 2.0)) == 8.0
    assert volume_from_extents((3.0, 4.0, 5.0)) == 60.0


def test_obb_pca_deterministic():
    """PCA-based OBB should be deterministic (same input = same output)."""
    np.random.seed(42)
    vertices = np.random.rand(100, 3) * 10

    center1, R1, extents1 = compute_obb_from_vertices(vertices)
    center2, R2, extents2 = compute_obb_from_vertices(vertices)

    np.testing.assert_allclose(center1, center2)
    np.testing.assert_allclose(np.abs(R1), np.abs(R2))  # sign may flip but abs same
    np.testing.assert_allclose(sorted(extents1), sorted(extents2))


def test_obb_cube():
    """Cube vertices should yield equal extents."""
    # Unit cube centered at origin
    vertices = np.array([
        [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5],
        [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5],
        [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5],
        [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5]
    ])
    center, R, extents = compute_obb_from_vertices(vertices)
    dims = sorted_extents(extents)
    # All sides should be 1.0
    assert all(abs(d - 1.0) < 1e-6 for d in dims)


def test_aabb_from_obb():
    """AABB of a rotated box should contain all corners."""
    center = np.array([0.0, 0.0, 0.0])
    R = np.eye(3)
    extents = np.array([2.0, 3.0, 4.0])
    amin, amax = aabb_from_obb(center, R, extents)
    np.testing.assert_allclose(amin, [-1.0, -1.5, -2.0])
    np.testing.assert_allclose(amax, [1.0, 1.5, 2.0])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])