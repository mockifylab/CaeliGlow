#!/usr/bin/env bash
# CaeliGlow: validate that the full patches/ series applies onto the pristine Noctalia
# pin via `git am --3way` and reconstructs the caeliglow-dev tree byte-for-byte.
# Run from anywhere; all paths are derived from the repo root.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN=a33122c42
BR="$ROOT/upstream/noctalia"
WT="$(mktemp -d /tmp/caeliglow-series-validate.XXXXXX)"
cleanup() { git -C "$BR" worktree remove --force "$WT" 2>/dev/null || true; }
trap cleanup EXIT

DEV_TIP=$(git -C "$BR" rev-parse caeliglow-dev)
git -C "$BR" worktree add --detach "$WT" "$PIN" >/dev/null
cd "$WT"
git config user.name "caeliglow-validate"
git config user.email "caeliglow@local"
count=0
for p in "$ROOT"/patches/0*.patch; do
  git am --3way --quiet "$p" >/dev/null 2>&1 || git am --quiet "$p" >/dev/null
  count=$((count + 1))
done
echo "applied $count patches"

if git diff --quiet "$DEV_TIP" HEAD; then
  echo "VALIDATION OK: series result byte-identical to caeliglow-dev tip"
else
  echo "VALIDATION FAILED: tree differs"
  git diff --stat "$DEV_TIP" HEAD | head -20
  exit 1
fi
