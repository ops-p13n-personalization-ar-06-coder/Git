```markdown
# AGENTS.md — Codex Agent Contract (Python solution.patch)

This repository defines a strict contract for agents that generate **code-only solution patches** for Python projects using a Mars-style workflow.

## Intent

Create a minimal fix so that:
- baseline (upstream) tests still pass,
- new tests added by `test.patch` fail on the base commit and pass after the fix,
- output is exactly two fenced blocks: `VERIFICATION_LOG` and `solution.patch`.

No edits to tests or build files are allowed.

---

## Environment assumptions

- Running in a Linux container with Python and Git (e.g. `public.ecr.aws/x8v8d7g8/mars-base:latest`).
- Working directory root: `/app`.
- Target repository will be cloned to: `/app/work/repo`.
- Tests patch is provided at: `/app/artifacts/test.patch` (unified diff, LF).
- Optional env file: `/app/profile.env` with:
```

REPO_URL=<url>
BASE_SHA=<commit>
TARGET_FILES_CSV=<comma,separated,paths/to/edit/only>

```
If `/app/profile.env` exists, source it. Otherwise require these three inputs from the task.

---

## Hard rules (must follow)

- Edit only paths listed in `TARGET_FILES_CSV`. Nothing else.
- Never modify: `mars_base_ok/**`, `mars_new/**`, `tests/**`, `test.sh`, `Dockerfile`, `pyproject.*`, `setup.*`, `__init__.py`.
- All code edits must be comment-free, ASCII-only, with LF newlines.
- Preserve public API, error families, and formatting unless the problem explicitly requires change.
- Use `pytest -c /dev/null`. Do not run tests in Docker build. Do not run `docker` inside the container.
- Work in git worktrees and keep `/app/work/repo` pristine.
- Abort if new tests pass on the base (tests must fail first).

---

## Canonical one-shot protocol (execute silently)

### [0] Preflight
1. `set -euo pipefail`
2. Ensure `/app/profile.env` is sourced if present; otherwise use task-provided `REPO_URL`, `BASE_SHA`, `TARGET_FILES_CSV`.
3. `git clone "$REPO_URL" /app/work/repo && cd /app/work/repo && git checkout -q "$BASE_SHA"`
4. Reset worktrees: remove `/tmp/solve`, `/tmp/verify-sol` if present; `git worktree add -f /tmp/solve "$BASE_SHA"`.

### [1] Materialize tests and reproduce (must FAIL on base)
1. In `/tmp/solve`, write verbatim `/app/artifacts/test.patch` (LF; must start with `diff --git`).
2. `git apply --check test.patch && git apply test.patch`
3. `chmod +x test.sh || true`
4. `python3 -m pip install --no-cache-dir -e . pytest >/dev/null 2>&1 || true`
5. Run baseline: `PYTHONPATH=. ./test.sh base`
6. Run new: `set +e; PYTHONPATH=. ./test.sh new; RC_BEFORE=$?; set -e`
7. If `RC_BEFORE == 0`, stop (tests are not failing on base).

### [2] Implement minimal fix (only `TARGET_FILES_CSV`)
- Make the smallest possible change to satisfy the behavioral spec.
- Keep edits local (small helper in the same file allowed).
- Do not duplicate logic already handled downstream.
- Do not change return types unless explicitly required by the spec.
- Ensure files end with a trailing newline.

### [3] Stage and test
- `git reset`
- `git add $(echo "$TARGET_FILES_CSV" | tr ',' ' ')`
- `PYTHONPATH=. ./test.sh base`
- `PYTHONPATH=. ./test.sh new`

### [4] Build `/app/artifacts/solution.patch` and guard it
- `git --no-pager diff --cached --name-only > /tmp/changed.txt`
- Ensure every path in `/tmp/changed.txt` is in `TARGET_FILES_CSV`; else fail.
- `git -c core.filemode=false diff --cached --no-color > /app/artifacts/solution.patch`
- Validate `solution.patch`:
- non-empty,
- ASCII-only,
- no CRLF,
- unified diff containing `diff --git`,
- does not reference tests, `test.sh`, `Dockerfile`, or metadata files,
- changed paths are a subset of `TARGET_FILES_CSV`.

### [5] Clean verify (forward and reverse)
1. `git worktree add -f /tmp/verify-sol "$BASE_SHA"`
2. Copy both patches to `/tmp/verify-sol`.
3. Apply `test.patch`; run base/new; record `RC_BEFORE`.
4. Forward-apply `solution.patch`; run base/new (both must pass).
5. Reverse-apply check: `git apply -R --check solution.patch`.

---

## Output protocol (strict)

Return exactly two fenced blocks and nothing else:

### 1) VERIFICATION_LOG
- list of changed files,
- `RC_BEFORE`,
- base/new pass status before vs after,
- `forward-apply OK` and `reverse-apply OK`,
- sha256 of `/app/artifacts/solution.patch`.

### 2) solution.patch
- the full unified diff from step [4], beginning with:
```

diff --git a/<path> b/<path>
--- a/<path>
+++ b/<path>
@@ ...

```

---

## Optional in-repo guard

If present, agents may run:
```

TARGET_FILES_CSV="$TARGET_FILES_CSV" /app/guard/tools/validate_solution_patch.sh /app/artifacts/solution.patch

```
This catches corrupt patches, CRLF, non-ASCII, and unauthorized paths.

---

## Common failure handling

- New tests pass on base: stop (tests are not hard enough).
- Patch touches forbidden paths: restage only allowed files.
- CRLF or non-ASCII: regenerate with LF and ASCII only.
- Not a unified diff: output a real `git diff` style patch with `diff --git`.

---

## Notes

- Keep files ending with a trailing newline.
- Parametrized tests in `test.patch` are encouraged, but agents must not modify tests.
- TypeScript can mirror this contract with a Node test runner; not required here.
```
