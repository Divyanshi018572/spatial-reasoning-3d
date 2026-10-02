"""Tests for Part 2: 3D Bin Packing."""

import pytest
import json
from pathlib import Path

from utils.geom_utils import (boxes_overlap, unique_rotations, fits_in_master,
                              generate_candidates, is_supported, find_position)


def test_boxes_overlap():
    a = (0, 0, 0, 10, 10, 10)
    b = (5, 5, 5, 10, 10, 10)  # overlaps
    c = (20, 20, 20, 10, 10, 10)  # no overlap
    assert boxes_overlap(a, b) is True
    assert boxes_overlap(a, c) is False


def test_unique_rotations():
    # Cube: only 1 unique
    assert len(unique_rotations((10, 10, 10))) == 1
    # Rectangular: 6 unique
    assert len(unique_rotations((10, 20, 30))) == 6
    # Two equal: 3 unique
    assert len(unique_rotations((10, 10, 20))) == 3


def test_fits_in_master():
    master = (100, 100, 100)
    assert fits_in_master((0, 0, 0), (50, 50, 50), master) is True
    assert fits_in_master((60, 60, 60), (50, 50, 50), master) is False
    assert fits_in_master((0, 0, 0), (101, 10, 10), master) is False


def test_generate_candidates():
    placed = [(0, 0, 0, 20, 20, 20)]
    master = (100, 100, 100)
    candidates = generate_candidates(placed, master)
    assert (0, 0, 0) in candidates
    assert (20, 0, 0) in candidates
    assert (0, 20, 0) in candidates
    assert (0, 0, 20) in candidates


def test_is_supported():
    placed = [(0, 0, 0, 30, 30, 10)]  # box at z=0..10
    # On floor
    assert is_supported((0, 0, 0), (10, 10, 10), placed) is True
    # On top of box (z=10), fully supported
    assert is_supported((0, 0, 10), (10, 10, 10), placed) is True
    # Partially supported (70% threshold)
    assert is_supported((25, 0, 10), (10, 10, 10), placed) is True  # 100% on box
    assert is_supported((30, 0, 10), (10, 10, 10), placed) is False  # 0% on box
    # Floating
    assert is_supported((0, 0, 5), (10, 10, 10), placed) is False


def test_find_position():
    placed = []
    master = (100, 100, 100)
    pos, dims = find_position((20, 20, 20), placed, master)
    assert pos == (0, 0, 0)
    assert dims == (20, 20, 20)

    # Second box should go next to first
    placed = [(0, 0, 0, 20, 20, 20)]
    pos, dims = find_position((20, 20, 20), placed, master)
    assert pos == (20, 0, 0)  # lowest Z, then Y, then X


def test_load_item_list():
    """Verify Item List.json loads correctly."""
    path = Path("Item List.json")
    if path.exists():
        with path.open() as f:
            data = json.load(f)
        assert len(data) == 20
        for item in data:
            assert "id" in item
            assert "dims" in item
            assert len(item["dims"]) == 3
            assert all(d > 0 for d in item["dims"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])