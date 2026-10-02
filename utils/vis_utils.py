"""Visualization utilities for OBB and packing."""

import logging
from typing import Sequence

import numpy as np

try:
    import open3d as o3d
    OPEN3D_AVAILABLE = True
except ImportError:
    OPEN3D_AVAILABLE = False

log = logging.getLogger(__name__)


def draw_obb_open3d(mesh, center: np.ndarray, R: np.ndarray, extents: np.ndarray):
    """Visualize mesh + OBB using Open3D."""
    if not OPEN3D_AVAILABLE:
        raise RuntimeError("Open3D not available")

    # OBB as red LineSet
    obb = o3d.geometry.OrientedBoundingBox(center, R, extents)
    obb_lines = o3d.geometry.LineSet.create_from_oriented_bounding_box(obb)
    obb_lines.paint_uniform_color([1.0, 0.0, 0.0])  # red

    # Mesh (already loaded)
    o3d.visualization.draw_geometries([mesh, obb_lines],
                                       window_name="OBB Visualization",
                                       width=1024, height=768)


def draw_obb_fallback(vertices: np.ndarray, center: np.ndarray, R: np.ndarray, extents: np.ndarray,
                      output_path: str = "outputs/obb_screenshot.png"):
    """Fallback: save matplotlib 3D screenshot of vertices + OBB."""
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Sample vertices for speed
    if len(vertices) > 5000:
        idx = np.random.choice(len(vertices), 5000, replace=False)
        verts_sample = vertices[idx]
    else:
        verts_sample = vertices

    ax.scatter(verts_sample[:, 0], verts_sample[:, 1], verts_sample[:, 2],
               s=1, alpha=0.5, c='gray', label='Mesh vertices')

    # OBB corners
    local_corners = np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0],
        [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]
    ]) - 0.5
    local_corners *= extents
    world_corners = center + local_corners @ R.T

    # OBB edges
    edges = [
        (0, 1), (0, 2), (1, 3), (2, 3),
        (4, 5), (4, 6), (5, 7), (6, 7),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    for i, j in edges:
        ax.plot([world_corners[i, 0], world_corners[j, 0]],
                [world_corners[i, 1], world_corners[j, 1]],
                [world_corners[i, 2], world_corners[j, 2]],
                'r-', linewidth=2)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('OBB (Red) + Mesh Vertices (Gray)')
    ax.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    log.info("Saved OBB screenshot to %s", output_path)


def animate_packing(placements: list[dict],
                    master: tuple[float, float, float],
                    output_path: str = "outputs/packing_animation.gif"):
    """Animate sequential packing using Matplotlib 3D."""
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Master wireframe
    mx, my, mz = master
    master_corners = np.array([
        [0, 0, 0], [mx, 0, 0], [0, my, 0], [mx, my, 0],
        [0, 0, mz], [mx, 0, mz], [0, my, mz], [mx, my, mz]
    ])
    master_edges = [
        (0, 1), (0, 2), (1, 3), (2, 3),
        (4, 5), (4, 6), (5, 7), (6, 7),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    # Color map by type
    type_colors = {
        'standard_box': 'tab:blue',
        'flat_panel': 'tab:cyan',
        'long_beam': 'tab:orange',
        'large_crate': 'tab:red',
        'medium_cube': 'tab:green',
        'small_filler': 'tab:purple',
        'long_box': 'tab:brown',
        'flat_box': 'tab:pink',
    }

    def draw_box(ax, pos, dims, color, alpha=0.7):
        x, y, z = pos
        dx, dy, dz = dims
        corners = np.array([
            [x, y, z], [x+dx, y, z], [x, y+dy, z], [x+dx, y+dy, z],
            [x, y, z+dz], [x+dx, y, z+dz], [x, y+dy, z+dz], [x+dx, y+dy, z+dz]
        ])
        faces = [
            [corners[i] for i in [0, 1, 3, 2]],
            [corners[i] for i in [4, 5, 7, 6]],
            [corners[i] for i in [0, 1, 5, 4]],
            [corners[i] for i in [2, 3, 7, 6]],
            [corners[i] for i in [0, 2, 6, 4]],
            [corners[i] for i in [1, 3, 7, 5]],
        ]
        poly = Poly3DCollection(faces, alpha=alpha, facecolor=color, edgecolor='k', linewidth=0.5)
        ax.add_collection3d(poly)

    def init():
        ax.clear()
        # Master wireframe
        for i, j in master_edges:
            ax.plot([master_corners[i, 0], master_corners[j, 0]],
                    [master_corners[i, 1], master_corners[j, 1]],
                    [master_corners[i, 2], master_corners[j, 2]],
                    'k--', linewidth=1, alpha=0.5)
        ax.set_xlim(0, mx)
        ax.set_ylim(0, my)
        ax.set_zlim(0, mz)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        return []

    def animate(frame):
        init()
        for i in range(frame + 1):
            p = placements[i]
            color = type_colors.get(p.get('type', ''), 'gray')
            draw_box(ax, p['pos'], p['placed_dims'], color)
        ax.set_title(f"Packed {frame + 1}/{len(placements)} — ID {placements[frame]['id']}")
        return []

    anim = FuncAnimation(fig, animate, frames=len(placements),
                         init_func=init, interval=600, blit=False, repeat=False)
    anim.save(output_path, writer='pillow', fps=2)
    plt.close()
    log.info("Saved packing animation to %s", output_path)


def show_packing_interactive(placements: list[dict], master: tuple[float, float, float]):
    """Show final packing state interactively (Matplotlib)."""
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    mx, my, mz = master
    master_corners = np.array([
        [0, 0, 0], [mx, 0, 0], [0, my, 0], [mx, my, 0],
        [0, 0, mz], [mx, 0, mz], [0, my, mz], [mx, my, mz]
    ])
    master_edges = [
        (0, 1), (0, 2), (1, 3), (2, 3),
        (4, 5), (4, 6), (5, 7), (6, 7),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    for i, j in master_edges:
        ax.plot([master_corners[i, 0], master_corners[j, 0]],
                [master_corners[i, 1], master_corners[j, 1]],
                [master_corners[i, 2], master_corners[j, 2]],
                'k--', linewidth=1, alpha=0.5)

    type_colors = {
        'standard_box': 'tab:blue',
        'flat_panel': 'tab:cyan',
        'long_beam': 'tab:orange',
        'large_crate': 'tab:red',
        'medium_cube': 'tab:green',
        'small_filler': 'tab:purple',
        'long_box': 'tab:brown',
        'flat_box': 'tab:pink',
    }

    def draw_box(ax, pos, dims, color, alpha=0.7):
        x, y, z = pos
        dx, dy, dz = dims
        corners = np.array([
            [x, y, z], [x+dx, y, z], [x, y+dy, z], [x+dx, y+dy, z],
            [x, y, z+dz], [x+dx, y, z+dz], [x, y+dy, z+dz], [x+dx, y+dy, z+dz]
        ])
        faces = [
            [corners[i] for i in [0, 1, 3, 2]],
            [corners[i] for i in [4, 5, 7, 6]],
            [corners[i] for i in [0, 1, 5, 4]],
            [corners[i] for i in [2, 3, 7, 6]],
            [corners[i] for i in [0, 2, 6, 4]],
            [corners[i] for i in [1, 3, 7, 5]],
        ]
        poly = Poly3DCollection(faces, alpha=alpha, facecolor=color, edgecolor='k', linewidth=0.5)
        ax.add_collection3d(poly)

    for p in placements:
        color = type_colors.get(p.get('type', ''), 'gray')
        draw_box(ax, p['pos'], p['placed_dims'], color)

    ax.set_xlim(0, mx)
    ax.set_ylim(0, my)
    ax.set_zlim(0, mz)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Final Packing — {len(placements)} items in {master[0]}³")
    plt.show()