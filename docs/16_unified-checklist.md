# 16 — Unified Implementation Checklist (Definition of Done)

**Single source of truth.** Every item must be ✅ before recording videos.

## Phase 0 — Repo & Environment (30 min)

- [ ] `git init` + `.gitignore` (doc 13) committed
- [ ] `requirements.txt` created + `venv` works
- [ ] `python part1_obb.py --help` shows usage
- [ ] `python part2_packing.py --help` shows usage
- [ ] All 4 input files present, readable, sizes match doc 01
- [ ] GitHub remote added + `main` pushed

## Phase 1 — Part 1 (OBB)

### Code
- [ ] `part1_obb.py` loads mesh via Open3D (fallback Trimesh)
- [ ] `compute_obb()` returns `(center, R, extents)` using `get_oriented_bounding_box()`
- [ ] Dims sorted L≥W≥H, volume printed to 2 decimals
- [ ] `visualize()` shows mesh + red OBB LineSet in `draw_geometries`
- [ ] `--all` flag loops 3 files, writes `outputs/part1_results.json`
- [ ] No `print()` — uses `logging.info`
- [ ] Type hints + Google docstrings on all public fns
- [ ] `ruff format .` + `ruff check .` pass

### Tests (doc 10)
- [ ] T1.1: All 3 load, vertices >100
- [ ] T1.2: OBB extents >0, R orthonormal
- [ ] T1.3: Cube dims equal within 2%
- [ ] T1.4: Cylinder two dims equal within 3%
- [ ] T1.5: Teapot `vol_OBB < vol_AABB`
- [ ] T1.6: Deterministic (two runs = same dims)

### Video 1 Recording
- [ ] OBS: Window Capture (terminal + 3D viewer), 720p, 30fps
- [ ] Terminal visible: command + output dims/volume for all 3
- [ ] 3D window: rotate each OBB 360°, pause to show tight fit
- [ ] Show `outputs/part1_results.json` in editor at end
- [ ] File <200MB, plays in incognito Drive link

### Git
- [ ] Branch `feature/part1-obb` → commits like `feat(part1): ...`
- [ ] PR #1 passes tests + lint → merge → tag `v1.0-part1`

## Phase 2 — Part 2 (Packing)

### Code
- [ ] `part2_packing.py` loads `Item List.json` via `argparse`
- [ ] Sorts items by volume desc (largest first)
- [ ] `generate_candidates()` uses corner-point method
- [ ] `find_position()` tries 6 unique rotations per candidate
- [ ] Checks: bounds → overlap → support (≥70% or center+2 corners)
- [ ] Places all 20 or logs unplaced with reason
- [ ] `animate()` shows sequential add (0.6s/frame), master wireframe
- [ ] Colors by `type` field, legend or title shows current item
- [ ] Writes `outputs/part2_placements.json`
- [ ] `ruff format .` + `ruff check .` pass

### Tests (doc 10)
- [ ] T2.1: JSON loads 20 items, dims >0
- [ ] T2.2: 20 placed, 0 unplaced
- [ ] T2.3: All inside 100³ (x+dx≤100 etc.)
- [ ] T2.4: Zero pairwise overlaps (190 pairs)
- [ ] T2.5: All z>0 pass support check
- [ ] T2.6: Deterministic (two runs = identical placements)

### Video 2 Recording
- [ ] OBS same settings
- [ ] Terminal: command → placement log scrolling
- [ ] 3D window: blocks appear one-by-one, no intersections
- [ ] Final rotate: show floor filled, tight packing
- [ ] Show `outputs/part2_placements.json` at end
- [ ] File <200MB, incognito Drive works

### Git
- [ ] Branch `feature/part2-packing` → commits like `feat(part2): ...`
- [ ] PR #2 passes tests + lint → merge → tag `v1.0-part2`

## Phase 3 — Final Submission (15 min)

- [ ] Both Drive links: `Anyone with link → Viewer` + tested incognito
- [ ] Submission email/template (doc 12) filled
- [ ] `README.md` run commands copy-paste work on fresh clone
- [ ] No secrets, no personal data in any file/video
- [ ] Code is **simple, readable, human-like** (doc 14)

---

## Quick Commands Reference

```powershell
# Fresh verify
git clone <repo> && cd <repo>
python -m venv venv && .\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Part 1
python part1_obb.py --all --view
pytest tests/test_obb.py -v

# Part 2
python part2_packing.py --items "Item List.json"
pytest tests/test_packing.py -v

# Lint/format
ruff format . && ruff check .
```

---

## If Something Fails — Decision Tree

| Symptom | First Fix |
|---------|-----------|
| OBB volume == AABB volume | You used `get_axis_aligned_bounding_box()` → switch to `get_oriented_bounding_box()` |
| Teapot dims jump between runs | Fix PCA sign: `eigvecs[:, i] *= np.sign(eigvecs[0, i])` |
| Item floats in video | Raise `SUPPORT_THRESH` to 0.8, add center+corner check |
| Matplotlib animation flickers | `blit=False`, `ax.cla()` each frame, or use Open3D `AxisAlignedBoundingBox` for boxes |
| Open3D window won't open | Use Trimesh for OBB, Matplotlib for screenshots; video shows screenshots |
| Only 19 items place | Check rotation dedup + candidate dedup; log every tried `(cand, rot)` |

---

**Green light = all ✅.** Then record, upload, submit.