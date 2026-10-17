#!/usr/bin/env bash
# Build CaeliGlow: apply the patch series to the pinned Noctalia tree, then build
# with Noctalia's own meson/just toolchain. Nothing is installed here; the output
# binary is left under upstream/noctalia/build-<mode>/noctalia for review.
#
# Usage: scripts/build.sh [release|debug] [prefix]
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-release}"
PREFIX="${2:-/usr/local}"
NOCTALIA_DIR="${CAELIGLOW_NOCTALIA_DIR:-$HERE/upstream/noctalia}"

if [[ ! -d "$NOCTALIA_DIR/.git" ]]; then
  echo "error: Noctalia submodule missing. Run: git submodule update --init --recursive" >&2
  exit 1
fi

# Ensure the tree is patched (skip if already applied).
if [[ -s "$HERE/patches/series" ]] && ! (cd "$NOCTALIA_DIR" && git log -5 --format='%s' | grep -qE '^caeliglow:'); then
  "$HERE/scripts/apply-patches.sh"
fi

VER="$(tr -d '[:space:]' < "$HERE/VERSION")"
echo ">> Building CaeliGlow v$VER ($MODE) with prefix $PREFIX"
cd "$NOCTALIA_DIR"
just configure "$MODE" "$PREFIX"
just build "$MODE"

echo ">> Build complete: $NOCTALIA_DIR/build-$MODE/noctalia"
"$NOCTALIA_DIR/build-$MODE/noctalia" --version || true
