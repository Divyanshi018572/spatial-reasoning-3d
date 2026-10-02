# 13 — Git Workflow & Commit Standards

## 1. Branching Model (Simple, Linear)

```
main ──────────────────────────────────────────►
  │
  ├─ feature/part1-obb ──────► (PR #1) ──►
  │
  └─ feature/part2-packing ──► (PR #2) ──►
```

- **main** = always deployable, tagged per deliverable
- **feature/** branches = one per Part, short-lived (<2 days)
- No develop/release branches — overkill for this scope

## 2. Commit Convention (Conventional Commits — Minimal)

```
<type>(<scope>): <subject>

<body (optional)>
```

| Type | When |
|------|------|
| `feat` | New user-visible function (e.g. `feat(part1): add OBB computation`) |
| `fix` | Bug fix (e.g. `fix(part2): correct support check for z=0`) |
| `refactor` | Code restructure, no behavior change |
| `docs` | Markdown/docstring updates only |
| `test` | Adding/adjusting tests |
| `chore` | Tooling, deps, .gitignore, CI |

**Subject rules:** Imperative mood, ≤72 chars, no period.  
Examples:
- `feat(part1): compute oriented bounding box via Open3D`
- `fix(part2): handle cube rotation duplicates in candidate gen`
- `docs: add setup runbook for Windows PowerShell`
- `test: add pairwise overlap validation for 20 items`

## 3. PR Checklist (Every PR Must Pass)

- [ ] Single logical change (one Part or one fix)
- [ ] All tests pass: `pytest -v`
- [ ] Code formatted: `ruff format .` (or `black .`)
- [ ] Lint clean: `ruff check .` (or `flake8`)
- [ ] Type hints on new public functions
- [ ] Docstring on new public functions (Google style)
- [ ] No `print()` in library code — use `logging`
- [ ] No hard-coded paths — use `argparse`
- [ ] Updated `README.md` if CLI changed
- [ ] `outputs/` ignored, no `.mp4` committed

## 4. Local Workflow Commands

```powershell
# Start feature
git checkout main && git pull
git checkout -b feature/part1-obb

# Work + commit often (small, atomic)
git add part1_obb.py utils/geom_utils.py
git commit -m "feat(part1): compute OBB via Open3D PCA"

# Push + PR
git push -u origin feature/part1-obb
# Open PR on GitHub → fill template → request review (or self-merge after checks)

# After PR merged
git checkout main && git pull
git branch -d feature/part1-obb
```

## 5. Tags for Deliverables

```bash
git tag -a v1.0-part1 -m "Part 1 complete: OBB on 3 objects"
git tag -a v1.0-part2 -m "Part 2 complete: 20 items packed in 100³"
git push origin --tags
```

## 6. .gitignore (Commit This First)

```gitignore
# Python
__pycache__/
*.py[cod]
venv/
.env

# Outputs
outputs/
*.json
screenshots/
*.mp4
*.mkv
*.gif

# IDE
.vscode/
.idea/
*.swp

# OS
Thumbs.db
.DS_Store
```

## 7. Remote Repo Setup (When You Provide URL)

```bash
git remote add origin <YOUR_REPO_URL>
git push -u origin main
# Then feature branches as above
```

## 8. Why This Works for Internship

- Reviewer sees **clear history**: `feat(part1)...` → `feat(part2)...` → tags
- Each PR = one reviewable unit (Part 1, then Part 2)
- No merge conflicts (linear, sequential)
- Tags map directly to video deliverables