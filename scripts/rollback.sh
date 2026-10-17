#!/usr/bin/env bash
# Roll CaeliGlow back to ordinary Noctalia. Two independent, safe steps:
#   1) Uninstall the files this build installed under its prefix (meson uninstall).
#   2) Reset the Noctalia submodule tree so the patch series is removed.
# Your pacman-packaged /usr/bin/noctalia is NEVER touched, so ordinary Noctalia
# keeps working throughout. No package removals, no disk/boot operations.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-release}"
PREFIX="${2:-/usr/local}"
NOCTALIA_DIR="${CAELIGLOW_NOCTALIA_DIR:-$HERE/upstream/noctalia}"

if [[ -f "$NOCTALIA_DIR/build-$MODE/build.ninja" ]]; then
  echo ">> Uninstalling CaeliGlow files from $PREFIX ..."
  if [[ "$PREFIX" != "$HOME"* ]]; then
    sudo ninja -C "$NOCTALIA_DIR/build-$MODE" uninstall || true
  else
    ninja -C "$NOCTALIA_DIR/build-$MODE" uninstall || true
  fi
else
  echo ">> No build-$MODE present; skipping uninstall step."
fi

echo ">> Resetting patched submodule tree to clean Noctalia ..."
"$HERE/scripts/reset-patches.sh" || true

echo ">> Rollback complete. Ordinary Noctalia (/usr/bin/noctalia) is unchanged and remains your shell."
