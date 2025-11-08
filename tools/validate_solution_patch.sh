#!/usr/bin/env bash
set -euo pipefail
PATCH="${1:-/app/artifacts/solution.patch}"
: "${TARGET_FILES_CSV:?TARGET_FILES_CSV not set}"
python3 tools/guard_solution_patch.py "$PATCH"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git apply --check "$PATCH"
fi
echo "OK: solution patch passed guards"
