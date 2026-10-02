# 03 — Tech Stack

## 1. Language
- **Python 3.11** — required by assignment (`Write a Python script`). Best wheel support for Open3D + Trimesh on Windows.

## 2. Core Libraries (Pinned in `requirements.txt`)

| Library | Version pin (example) | Used For |
|---------|----------------------|----------|
| `open3d` | `>=0.18` | Part 1: load `.obj`, `get_oriented_bounding_box()`, visualize mesh+OBB |
| `trimesh` | `>=4.0` | Part 1 fallback: `bounding_box_oriented`, mesh stats; Part 2: box helpers |
| `numpy` | `>=1.26` | All math: extents, volumes, overlap checks, rotations |
| `scipy` | `>=1.12` | Optional: convex hull / spatial checks |
| `matplotlib` | `>=3.8` | Part 2: 3D voxel/block animation + Master Box wireframe |
| `plotly` (optional) | `>=5.20` | Alternative prettier Part 2 animation |

> OpenCV is mentioned in PDF as example but **not needed** — mesh OBB is 3D, not 2D image. Do not force OpenCV in.

## 3. Dev Tools
- `venv` + `pip` + `requirements.txt` — reproducible env
- `ruff` or `black` + `flake8` — formatting/lint (clean-code requirement)
- `pytest` — validation tests
- `OBS Studio` — screen recording at 1080p/720p, 30fps, MP4
- `VS Code` — editor

## 4. Why This Stack
- **Open3D:** Native OBB via PCA + robust viewer (`draw_geometries`). Directly satisfies Hint: rotate to fit tightly.
- **Trimesh:** Lightweight fallback, easy `extents` + `volume`, good for headless runs where Open3D GUI fails.
- **NumPy:** All AABB overlap math is vectorized box comparisons — no physics engine needed.
- **Matplotlib 3D:** Zero-GPU, offline, sufficient to show one-by-one stacking. Keeps scope tight.

## 5. `requirements.txt` Template
```text
open3d>=0.18.0
trimesh>=4.0.0
numpy>=1.26.0
scipy>=1.12.0
matplotlib>=3.8.0
pytest>=8.0.0
```

## 6. What NOT To Use
- No PyTorch/TensorFlow — no learning needed.
- No PyBullet / physics sim — overkill; analytic support check suffices and is explainable in video.
- No Docker — unnecessary for internship submission on Windows.
