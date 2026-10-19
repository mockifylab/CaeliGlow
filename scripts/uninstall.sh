#!/usr/bin/env bash
# Remove a CaeliGlow quick-install from the system. Symmetric counterpart of
# scripts/quick-install.sh. Nothing is ever removed from /usr (pacman-owned) and
# your ~/.config / ~/.local data for BOTH noctalia and caeliglow are kept unless
# you pass --purge.
#
#   bash scripts/uninstall.sh            # remove programs/files under the prefix
#   bash scripts/uninstall.sh --purge    # also remove ~/.config/caeliglow & friends
#
# Packages installed on the pacman path (pkgbuild/PKGBUILD) are removed with:
#   sudo pacman -R caeliglow
set -euo pipefail

PREFIX="${CAELIGLOW_PREFIX:-/usr/local}"
PURGE=0
[[ "${1:-}" == "--purge" ]] && PURGE=1

if [[ "${EUID}" -eq 0 ]]; then
  echo "error: do not run as root; the script calls sudo itself." >&2
  exit 1
fi

case "$PREFIX" in
  /usr|/usr/bin|/usr/share)
    echo "error: refusing to touch the distro-owned prefix $PREFIX." >&2
    exit 1;;
esac

echo ">> Removing CaeliGlow files under $PREFIX (distro noctalia is never touched)."
sudo rm -f \
  "$PREFIX/bin/caeliglow" \
  "$PREFIX/bin/noctalia" \
  "$PREFIX/share/applications/caeliglow.desktop" \
  "$PREFIX/share/applications/dev.noctalia.Noctalia.desktop" \
  "$PREFIX/share/icons/hicolor/scalable/apps/noctalia.svg" \
  "$PREFIX/share/wayland-sessions/caeliglow.desktop" \
  "$PREFIX/bin/caeliglow-session"
sudo rm -rf "$PREFIX/share/noctalia"
# Remove now-empty directories created by the install (rmdir fails on non-empty: safe).
sudo rmdir \
  "$PREFIX/share/wayland-sessions" \
  "$PREFIX/share/icons/hicolor/scalable/apps" \
  "$PREFIX/share/icons/hicolor/scalable" \
  "$PREFIX/share/icons/hicolor" \
  "$PREFIX/share/icons" \
  "$PREFIX/share/applications" \
  2>/dev/null || true

if [[ "$PURGE" -eq 1 ]]; then
  echo ">> --purge: removing CaeliGlow user data (your noctalia data is kept)."
  rm -rf "$HOME/.config/caeliglow" "$HOME/.local/state/caeliglow" \
         "$HOME/.local/share/caeliglow" "$HOME/.cache/caeliglow"
fi

echo ">> Done. /usr/bin/noctalia and all pacman packages are untouched."
