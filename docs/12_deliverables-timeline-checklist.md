# 12 — Deliverables, Timeline & Checklist

## 1. Deliverables (Exactly What PDF Asks)

| # | Deliverable | Format | Must Show |
|---|-------------|--------|-----------|
| D1 | Part 1 video | Drive link (View) | Script reading `CUBE.obj`, `CYLINDER.obj`, `TEAPOT.obj` + tight rotating OBB + terminal Volume/Dims |
| D2 | Part 2 video | Drive link (View) | Blocks stacking one-by-one into 100³ Master Box + coords log |
| D3 (implied) | Code | `.py` + `requirements.txt` | `part1_obb.py`, `part2_packing.py` ingesting given files, no hard-coding |
| D4 (recommended) | Results JSON | files | `part1_results.json`, `part2_placements.json` |

## 2. Timeline (3–4 Days)

- **Day 0 (2h):** Setup + confirm inputs + read docs 01–05.
- **Day 1 (4–6h):** Implement Part 1 per doc 06 → pass tests T1.1–T1.6 → record Video 1.
- **Day 2–3 (6–10h):** Implement Part 2 per doc 07 → pass tests T2.1–T2.6 → record Video 2.
- **Day 3–4 (2h):** Security check (doc 08) + clean-code pass (doc 09) + upload + submit.

Fast-track (experienced): Day 1 both scripts, Day 2 videos + submit.

## 3. Pre-Submit Checklist (All Must Be Ticked)

### Part 1
- [ ] Uses OBB API, not AABB-only
- [ ] All 3 OBJs produce Volume + LxWxH in console
- [ ] Viewer shows tight red box, rotated to prove fit
- [ ] Video shows file being read (terminal command visible)

### Part 2
- [ ] Script takes `Item List.json` path as input (not hard-coded list)
- [ ] Master is exactly 100x100x100
- [ ] 20/20 placed, no overlap (tested pairwise)
- [ ] No floating boxes (support check passes)
- [ ] Animation stacks sequentially, not all-at-once

### Submission
- [ ] Both Drive links are `Anyone with link can View` + tested incognito
- [ ] Videos show only terminal + 3D window (no personal data)
- [ ] Code runs copy-paste per doc 11 on fresh venv
- [ ] `requirements.txt` present, versions pinned

## 4. Submission Message Template
```text
Subject: Computer Vision Internship — 3D Assignment (Your Name)

Part 1 Video (OBB — Cube/Cylinder/Teapot): <drive-link-1>
Part 2 Video (Packing — 20 items in 100³): <drive-link-2>
Code: <github-link or zip>

Stack: Python 3.11, Open3D, Trimesh, NumPy, Matplotlib
Part 1: OBB via PCA (get_oriented_bounding_box), Vol=...
Part 2: Largest-first + lowest-Z corner fit, 6 rotations, 20/20 placed, fill=16.5%, support≥70%
```
