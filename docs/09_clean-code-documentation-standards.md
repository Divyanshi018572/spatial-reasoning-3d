# 09 — Clean Code & Documentation Standards

## 1. Style
- PEP8, 88–100 col limit, `black` or `ruff format` before every commit/record.
- Type hints on all functions: `def find_position(dims: tuple[float,float,float], ...) -> tuple[...] | None:`
- Docstrings (Google style): 1-line summary + Args/Returns/Example for public functions.
- No magic numbers: `MASTER_SIZE=100`, `SUPPORT_THRESH=0.7`, `EPS=1e-9` as named constants.

## 2. Structure
- One responsibility per function (max ~40 lines). `part1_obb.py` ≤250 lines, `part2_packing.py` ≤350 lines.
- `utils/` holds reusable math; no copy-pasted overlap logic.
- CLI via `argparse` with `--help` text + examples.

## 3. Naming
- Files: `snake_case.py`. Functions: `verb_noun` (`compute_obb`, `is_supported`). Vars: `placed_dims`, not `pd`.
- JSON keys match assignment language: `id`, `dims`, `pos`, `placed_dims`, `volume`.

## 4. Logging (Not Print-Spam)
```python
import logging
log = logging.getLogger("part1")
log.info("CUBE.obj dims=%s vol=%.2f", dims, vol)
log.warning("UNPLACED id=%s", item_id)
```
- INFO for placements/results, WARNING for fallbacks, ERROR with traceback for fatal.

## 5. Comments
- Explain WHY (e.g. `# lowest-Z first enforces gravity`) not WHAT (`# loop`). No commented-out code.
- Reference PDF rules: `# Rule 2: gravity — floor or ≥70% support`.

## 6. Documentation Required
- [ ] Top-of-file header: purpose + usage example + input/output.
- [ ] `README.md` run commands must actually work (copy-paste tested).
- [ ] `outputs/part1_results.json` + `part2_placements.json` are human-readable (indent=2).
- [ ] Video narration mentions function names so evaluator maps video → code.

## 7. Example Header
```python
"""Part 1 — OBB measurement.
Usage: python part1_obb.py --input CUBE.obj
Outputs: console dims+volume, outputs/part1_results.json, 3D viewer.
"""
```
