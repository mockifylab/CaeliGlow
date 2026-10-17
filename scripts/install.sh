#!/usr/bin/env bash
# Install a built CaeliGlow to a prefix using Noctalia's meson installer.
#
# IMPORTANT (safety):
#   * Default prefix is /usr/local. The pacman-packaged Noctalia lives at
#     /usr/bin/noctalia; installing to /usr/local/bin does NOT overwrite it, so
#     you can try CaeliGlow and roll back without touching your distro package.
#   * This never removes packages and never touches boot/EFI/partitions.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-release}"
PREFIX="${2:-/usr/local}"
NOCTALIA_DIR="${CAELIGLOW_NOCTALIA_DIR:-$HERE/upstream/noctalia}"

BIN="$NOCTALIA_DIR/build-$MODE/noctalia"
if [[ ! -x "$BIN" ]]; then
  echo "error: $BIN not found. Run scripts/build.sh $MODE $PREFIX first." >&2
  exit 1
fi

if [[ "$PREFIX" != "$HOME"* ]]; then
  echo ">> Prefix $PREFIX requires root; using sudo (this is the only place CaeliGlow needs it)."
  echo ">> Refusing to install into /usr (distro-owned). If you want that, pass a prefix explicitly."
  case "$PREFIX" in
    /usr) echo "error: refusing to install to /usr (pacman-owned). Use /usr/local or \$HOME/.local." >&2; exit 1;;
  esac
  sudo meson install --no-rebuild -C "$NOCTALIA_DIR/build-$MODE"
else
  meson install --no-rebuild -C "$NOCTALIA_DIR/build-$MODE"
fi

echo ">> Installed CaeliGlow to $PREFIX"
echo ">> Start it as your shell (do not remove your pacman noctalia):"
echo "     $PREFIX/bin/noctalia   # or set it in your Hyprland/Noctalia autostart"
