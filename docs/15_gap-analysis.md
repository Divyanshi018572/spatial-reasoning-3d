# 15 — Gap Analysis: What's Missing / What You Didn't Mention

Read this **before coding**. These are implicit requirements or risks the PDF implies but doesn't spell out.

## 1. Implicit Requirements From PDF (Not Explicitly Stated)

| # | Gap | Why It Matters | Our Handling |
|---|-----|----------------|--------------|
| G1 | **Units** — Are OBJ vertices in mm, cm, meters? | Volume/dims meaningless without units | Assume **mm** (typical scanner). Document in results. Add `--unit-scale` CLI if needed. |
| G2 | **Coordinate system** — OBJ may not be centered at origin | OBB center could be far from (0,0,0) | OBB is translation-invariant. Visualization must show mesh + box together. |
| G3 | **Mesh quality** — Non-manifold, duplicate verts, holes | `get_oriented_bounding_box` works on vertices; robust | Use vertex array directly; skip mesh repair. |
| G4 | **Rotation allowed in packing?** | PDF says "place items" — doesn't forbid rotation | **Default: YES (6 axis permutations)**. Document in video. If evaluator expects fixed orientation, we'll know from feedback. |
| G5 | **Item types matter?** | `type` field in JSON (standard_box, flat_panel...) | Used only for **color coding** in visualization. Not for placement rules. |
| G6 | **Determinism** — Same run = same output | Evaluator may re-run | Fixed candidate order (sorted), no random. Document seed if any. |
| G7 | **Partial credit** — What if 19/20 place? | PDF says "place 20 items" | We log unplaced, continue, report fill%. Video shows 20 or explains gap. |
| G8 | **Video format/size** | "Upload to Google Drive" — no specs | 720p MP4, <200MB, 30fps. Test incognito. |
| G9 | **Code submission format** | PDF doesn't specify | Provide GitHub + zip fallback. Include `requirements.txt`. |

## 2. Things You Didn't Tell Me (But I Assumed)

| # | Assumption | Confirm or Correct |
|---|------------|-------------------|
| A1 | You have **Windows 10/11** with admin to install Python/OBS | ✅ / ❌ |
| A2 | You can **run Open3D GUI** (needs OpenGL 3.3+) | ✅ / ❌ — if ❌, we use Trimesh+Matplotlib screenshots |
| A3 | You're **comfortable with Git + GitHub** (for PR workflow) | ✅ / ❌ — if ❌, simplify to zip upload |
| A4 | You want **two separate videos** (Part 1, Part 2) | ✅ / ❌ — PDF says "video" singular but implies both |
| A5 | **Rotation allowed** in Part 2 packing | ✅ / ❌ — if ❌, remove permutation logic |
| A6 | **Support threshold** — 70% area or center-point? | Default 70% area; confirm |
| A7 | **Evaluation environment** — Will they run your code or only watch videos? | Assume **both**: code must run clean on fresh venv |

## 3. Technical Risks Not Yet Addressed

| Risk | Likelihood | Mitigation in Plan |
|------|------------|-------------------|
| R1 | Open3D fails to open window (headless CI / WSL) | Fallback: Trimesh OBB + Matplotlib static screenshots |
| R2 | CUBE.obj (16MB) loads slowly / OOM | Use `trimesh.load(..., process=False)` + vertex sampling for display only |
| R3 | Teapot OBB flips between runs (PCA sign ambiguity) | Force deterministic: sort eigenvectors by eigenvalue desc, fix sign by first component >0 |
| R4 | Packing order matters — greedy may leave gaps | Sort by volume desc + max-side desc; document as heuristic |
| R5 | Support check false positive (edge contact) | Require ≥4 corners OR center + 2 opposite corners supported |
| R6 | Video recording captures wrong monitor / audio | OBS: Window Capture (not Display), disable mic |

## 4. Deliverable Gaps (PDF vs Our Plan)

| PDF Says | We Added | Reason |
|----------|----------|--------|
| "Python script" | Two CLIs with `argparse` | Reproducible, evaluator can test |
| "Upload video to Drive" | Two videos + incognito test | Avoids "access denied" |
| "Oriented bounding box" | OBB via PCA + visualization | Not AABB — core requirement |
| "Stacking simulation" | One-by-one animation + support check | "Gravity" = sequential placement |
| (Nothing about code) | Git workflow, tests, lint, tags | Professional standard; reviewer sees process |

## 5. Action Items For You (Reply To These)

1. **Confirm A1–A7 above** — especially A2 (Open3D GUI works?) and A5 (rotation allowed?).
2. **Share GitHub repo URL** when ready — I'll add remote + push initial commit.
3. **Decide video style**: narrated (mic) vs silent with on-screen text? Silent + text is safer.
4. **Unit preference**: mm/cm/m for output? Default mm.

## 6. What We'll Discover During Implementation (Expect These)

- Cylinder may have **open ends** (no caps) — OBB still works on vertices.
- Teapot may have **interior vertices** (spout/handle hollow) — OBB uses all verts = tight.
- `Item List.json` dims might be **integers but placement needs float** — we use float throughout.
- Matplotlib 3D animation may **flicker** — fix: `blit=False`, `ax.cla()` per frame, or use Open3D boxes.

---

**Bottom line:** Plan covers PDF + professional guardrails. Your confirmations on A1–A7 + repo URL = green light to code.