#!/usr/bin/env bash
# Return the pinned Noctalia checkout to its clean, unpatched state and reset any
# in-progress `git am`. Safe: only touches the submodule working tree, never deletes
# it, and never runs system-wide commands.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NOCTALIA_DIR="${CAELIGLOW_NOCTALIA_DIR:-$HERE/upstream/noctalia}"

cd "$NOCTALIA_DIR"

if [[ -d "$(git rev-parse --git-path rebase-apply)" ]]; then
  echo ">> Aborting in-progress git am..."
  git am --abort || true
fi

echo ">> Hard-resetting submodule working tree to its pinned commit..."
git reset --hard '@{u}' 2>/dev/null || git reset --hard
git clean -fd -e build-debug -e build-release  # keep local build dirs, drop stray files
echo ">> Done. Tree is clean; re-run scripts/apply-patches.sh to patch again."
