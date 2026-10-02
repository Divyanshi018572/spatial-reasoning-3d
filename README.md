# 3D Vision Internship Assignment — End-to-End Project Plan

**Source of truth:** `Assignment Details.pdf` (2 parts) + local inputs in this folder.

## Parts (Strictly In-Scope)

### Part 1 — 3D Measurement (OBB)
- **Input:** `CUBE.obj`, `CYLINDER.obj`, `TEAPOT.obj`
- **Action:** Python script with Open3D / Trimesh / OpenCV:
  1. Read each mesh
  2. Compute **Oriented Bounding Box (OBB)** — must rotate to fit tightly, NOT AABB
  3. Output **Volume + Dimensions (L x W x H)**
- **Deliverable:** Screen recording showing script reading + visualizing tight box around all 3 objects. Google Drive link with `Anyone with link can View`.

### Part 2 — 3D Tetris Packing
- **Input:** `Item List.json` (20 theoretical items, e.g. `[20,20,20]`) — script must ingest this specific file
- **Constraint:** Master Box `100 x 100 x 100`
- **Action:** Function that computes `(x,y,z)` placement for 20 items:
  - Rule 1: No overlap
  - Rule 2: Gravity / support (floor or another item)
  - Rule 3: Pack as tightly as possible
- **Deliverable:** 3D visualization showing blocks stacked one-by-one into Master Box. Google Drive link with View permission.

## Documentation Index

All detailed plans are in `docs/` — read in order:

### Core Planning (Read First)
| # | File | Purpose |
|---|------|---------|
| 01 | `docs/01_project-plan.md` | Master plan, scope, milestones, file map |
| 02 | `docs/02_requirements-from-user.md` | **What YOU must provide / confirm** |
| 03 | `docs/03_tech-stack.md` | Languages, libraries, tools + why |
| 04 | `docs/04_concepts-theory.md` | OBB vs AABB, PCA, bin-packing theory |
| 05 | `docs/05_approach-architecture.md` | Repo structure, data flow, function signatures |

### Implementation (Follow During Coding)
| # | File | Purpose |
|---|------|---------|
| 06 | `docs/06_part1-obb-measurement-plan.md` | Step-by-step Part 1 (3 OBJs → OBB) |
| 07 | `docs/07_part2-bin-packing-plan.md` | Step-by-step Part 2 (20 items → 100³) |

### Governance (Enforce Throughout)
| # | File | Purpose |
|---|------|---------|
| 08 | `docs/08_security-rules.md` | Input validation, no secrets, Drive Viewer-only |
| 09 | `docs/09_clean-code-documentation-standards.md` | PEP8, type hints, logging, docstrings |
| 10 | `docs/10_testing-validation.md` | 12 automated tests (overlap, support, OBB) |
| 11 | `docs/11_setup-runbook.md` | Venv + run + record commands for PowerShell |
| 12 | `docs/12_deliverables-timeline-checklist.md` | 2 videos + code + 3–4 day timeline + submit template |

### Process & Quality (New — Critical for Professional Output)
| # | File | Purpose |
|---|------|---------|
| 13 | `docs/13_git-workflow.md` | Branching, Conventional Commits, PR checklist, tags |
| 14 | `docs/14_code-simplicity-guide.md` | **Write simple, human-readable code** — templates, anti-patterns |
| 15 | `docs/15_gap-analysis.md` | **Implicit requirements, risks, what you didn't tell me** |
| 16 | `docs/16_unified-checklist.md` | **Single Definition of Done** — every ✅ before recording |

## Out-of-Scope (Do NOT Add)

- No AABB-only solution for Part 1 (will fail requirement).
- No hard-coded item dims in Part 2 — must parse `Item List.json`.
- No new features: no grasping, no robot arm, no web app, no training ML models.
- No 3D printing / scanner hardware work.

## Quick Start

1. Read `docs/02_requirements-from-user.md` — confirm you have everything.
2. Follow `docs/11_setup-runbook.md` to install env.
3. Implement Part 1 per `docs/06_part1-obb-measurement-plan.md`.
4. Implement Part 2 per `docs/07_part2-bin-packing-plan.md`.
5. Validate per `docs/10_testing-validation.md` and submit per `docs/12_deliverables-timeline-checklist.md`.
