# 11 — Setup & Runbook (End-to-End Commands)

Windows PowerShell (current env `win32`).

## 1. Setup (Once)
```powershell
# 1. Verify Python
python --version  # need 3.9+

# 2. Venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install
pip install --upgrade pip
pip install open3d trimesh numpy scipy matplotlib pytest
# freeze
pip freeze > requirements.txt

# 4. Verify inputs exist
dir "D:\company assignments\computer vision internship"
```

## 2. Run Part 1
```powershell
.\venv\Scripts\Activate.ps1
python part1_obb.py --input CUBE.obj
python part1_obb.py --input CYLINDER.obj
python part1_obb.py --input TEAPOT.obj
# or batch:
python part1_obb.py --all --input-dir "." --output outputs/part1_results.json
# expect: console Dims + Volume + 3D window with red OBB
```

## 3. Run Part 2
```powershell
.\venv\Scripts\Activate.ps1
python part2_packing.py --items "Item List.json" --master 100 100 100
# expect: console table id -> (x,y,z) + animated 3D window + outputs/part2_placements.json
```

## 4. Run Tests
```powershell
pytest tests/ -v
```

## 5. Record Videos (OBS)
1. OBS → Source: Window Capture (Terminal + 3D viewer only), 720p, 30fps.
2. Video 1: clear terminal → run Part 1 3x → rotate each OBB view 10s → show `part1_results.json`.
3. Video 2: run Part 2 → capture sequential stacking → rotate final pack → show `part2_placements.json`.
4. Export MP4, <200MB each, test play locally.

## 6. Upload & Submit
1. Drive → New Folder `YourName_3DVision_Assignment` → Upload MP4s.
2. Share → General access: `Anyone with the link` → Role: Viewer → Copy link.
3. Test link in incognito window.
4. Submit: Drive links + GitHub/code zip + 2-line summary (stack used, fill % / OBB volumes).
