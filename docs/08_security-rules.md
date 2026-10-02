# 08 — Security Rules

Applies to all code + videos + Drive sharing. Keep it minimal but enforced.

## 1. Input Safety
- [ ] Never use `eval()` / `exec()` on JSON or mesh paths.
- [ ] Validate `Item List.json`: must be list, each `dims` len 3, all `>0` and finite. Reject otherwise with clear error.
- [ ] Validate `.obj` path: must exist, extension `.obj`, size `<200MB`. Resolve with `Path.resolve()`; reject path traversal (`..`) outside project dir.
- [ ] Clamp Master Box to positive ints; reject `0` / negative.

## 2. Dependency Safety
- [ ] Pin versions in `requirements.txt`; install in `venv`, never system-wide with `--break-system-packages`.
- [ ] No downloading models / remote code at runtime. All libs from PyPI only.
- [ ] Before recording, run `pip list` to prove no private packages.

## 3. Secrets & Privacy
- [ ] No API keys, passwords, or personal data in code, logs, or videos.
- [ ] Videos must NOT show email, Drive file list, or other candidates. Record only terminal + 3D window (crop in OBS).
- [ ] Drive links: `Anyone with link → Viewer` only (never Editor). Test in incognito.

## 4. File System Safety
- [ ] Scripts only write to `outputs/` — never overwrite inputs (`*.obj`, `*.json` are read-only).
- [ ] Use `argparse` paths; no hard-coded `C:\Users\...` absolute paths.
- [ ] Large outputs (videos) stay out of git: add `*.mp4`, `*.mkv`, `outputs/screenshots/` to `.gitignore` if using git.

## 5. Code Execution Safety
- [ ] `open3d.visualization` opens local window only — no network port.
- [ ] Matplotlib uses inline/local backend; do not enable web server mode.
- [ ] Log placement coords, not full system paths.

## 6. Pre-Submit Security Check
- [ ] `grep -r "password\|api_key\|token" --include="*.py" .` returns nothing.
- [ ] Inputs unchanged (compare file sizes to Section 01 inventory).
- [ ] Drive link opens in incognito without login.
