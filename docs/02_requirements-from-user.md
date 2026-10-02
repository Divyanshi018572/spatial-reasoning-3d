# 02 — Requirements From Your Side

This is everything **YOU** must provide / confirm. Nothing proceeds without these.

## 1. Files (Already Present — Confirm)
- [ ] `CUBE.obj` — use this, ignore `CUBE (1).obj` duplicate
- [ ] `CYLINDER.obj`
- [ ] `TEAPOT.obj`
- [ ] `Item List.json` — do NOT rename, do NOT hard-code values elsewhere
- [ ] `Assignment Details.pdf` — source of truth

> If Drive folder has newer versions, overwrite local copies and note version/date.

## 2. Machine / OS
- [ ] Windows 10/11 (current env is `win32`), 8GB+ RAM (16GB recommended — CUBE.obj is 16MB dense)
- [ ] Python 3.9, 3.10, or 3.11 (3.11 recommended for Open3D wheels)
- [ ] ~2GB free disk for venv + outputs + videos
- [ ] GPU not required; integrated graphics OK for Open3D/Matplotlib

## 3. Accounts / Access
- [ ] Google account for Drive upload with `Anyone with link can View`
- [ ] GitHub (optional) if you want to share code link
- [ ] No paid APIs, no keys needed

## 4. Software To Install
- [ ] Python + `pip` + `venv`
- [ ] Screen recorder: OBS Studio (recommended) or Xbox Game Bar (`Win+G`)
- [ ] 3D quick viewer (optional): Windows 3D Viewer / MeshLab / Blender to sanity-check OBJs
- [ ] Code editor: VS Code + Python extension

## 5. Decisions You Must Make (Reply With Choice)
1. **Library for Part 1:** `A) Open3D (Recommended)` vs `B) Trimesh` — we default to Open3D for visualization + Trimesh as fallback. Confirm OK.
2. **Visualization for Part 2:** `A) Matplotlib 3D (Recommended, offline, simple)` vs `B) Plotly (prettier, heavier)` — default A.
3. **Rotation allowed in packing?** Default YES — 6 axis-aligned rotations. If evaluator expects no-rotation, say so (changes results).
4. **Video style:** Single video covering both parts, or 2 separate videos? PDF asks for video(s) per part — default 2 separate.

## 6. Constraints To Respect
- Do not rename inputs; script must accept path args.
- Do not commit videos to git (too large) — Drive links only.
- Do not share Drive link as Restricted — must test in incognito window.

## 7. What To Send Me When Ready
- Python version (`python --version`)
- Choices for items 5.1–5.4 above
- Confirmation that all 4 input files open correctly
