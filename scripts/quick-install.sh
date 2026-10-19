#!/usr/bin/env bash
# CaeliGlow one-command installer for Arch/CachyOS (Noctalia-docs style).
#
#   curl -fsSL https://raw.githubusercontent.com/mockifylab/CaeliGlow/main/scripts/quick-install.sh | bash
#
# Safety guarantees (same rules as every CaeliGlow script):
#   * ADDITIVE ONLY: dependencies go in via `pacman -S --needed`; nothing is ever removed.
#   * Never touches boot/EFI/partitions or personal files.
#   * Installs under /usr/local with the binary renamed to `caeliglow`, so it can
#     never shadow or overwrite the distro-packaged /usr/bin/noctalia on your PATH.
#   * Re-running the command updates the checkout and reinstalls (idempotent).
#
# Env knobs: CAELIGLOW_REPO, CAELIGLOW_BRANCH (default main), CAELIGLOW_SRC
set -euo pipefail

REPO="${CAELIGLOW_REPO:-https://github.com/mockifylab/CaeliGlow.git}"
BRANCH="${CAELIGLOW_BRANCH:-main}"
SRC="${CAELIGLOW_SRC:-$HOME/src/CaeliGlow}"
PREFIX="/usr/local"

if [[ "${EUID}" -eq 0 ]]; then
  echo "error: do not run this script as root; it calls sudo only where needed." >&2
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo ">> git not found; installing it (additive only)."
  sudo pacman -S --needed --noconfirm git
fi

echo ">> Fetching CaeliGlow ($BRANCH) with the pinned Noctalia submodule into $SRC"
if [[ -d "$SRC/.git" ]]; then
  git -C "$SRC" fetch --depth 1 origin "$BRANCH"
  git -C "$SRC" checkout "$BRANCH"
  git -C "$SRC" reset --hard "origin/$BRANCH"
  git -C "$SRC" submodule update --init --recursive
else
  git clone --depth 1 --branch "$BRANCH" --recurse-submodules --shallow-submodules "$REPO" "$SRC"
fi

echo ">> Installing build dependencies (additive only; no removals)."
"$SRC/scripts/install-deps.sh"

echo ">> Applying the CaeliGlow patch series to the pinned Noctalia tree"
cd "$SRC/upstream/noctalia"
# In a fresh clone the submodule .git is a gitfile, so we apply the series inline
# instead of scripts/apply-patches.sh (which expects a full development clone).
if git log -5 --format='%s' 2>/dev/null | grep -qE '^caeliglow:'; then
  echo "   (series already applied — skipping)"
else
  while IFS= read -r p; do
    [[ "$p" =~ ^[[:space:]]*(#|$) ]] && continue
    echo "   + $p"
    git am --3way "$SRC/patches/$p"
  done < "$SRC/patches/series"
fi

VER="$(tr -d '[:space:]' < "$SRC/VERSION")"
echo ">> Building CaeliGlow v$VER (release, prefix $PREFIX)"
just configure release "$PREFIX"
just build release

echo ">> Installing into $PREFIX (the only step that needs root)."
sudo meson install -C "$PWD/build-release" --no-rebuild

# Ship under the CaeliGlow name so we never shadow the distro `noctalia` binary.
if [[ -f "$PREFIX/bin/noctalia" ]]; then
  sudo mv -f "$PREFIX/bin/noctalia" "$PREFIX/bin/caeliglow"
fi
DESK="$PREFIX/share/applications/dev.noctalia.Noctalia.desktop"
if [[ -f "$DESK" ]]; then
  sudo sed -i -e 's|^Exec=.*|Exec='"$PREFIX"'/bin/caeliglow|' \
              -e '/^TryExec=/d' -e 's|^Name=.*|Name=CaeliGlow|' "$DESK"
  sudo mv -f "$DESK" "$PREFIX/share/applications/caeliglow.desktop"
fi

echo ">> Installed. Summary:"
echo "   binary : $PREFIX/bin/caeliglow   (distro noctalia at /usr/bin/noctalia untouched)"
echo "   config : ~/.config/caeliglow     (its own namespace; never reads ~/.config/noctalia)"
echo "   state  : ~/.local/state/caeliglow"
echo "   log    : ~/.cache/caeliglow/caeliglow.log"
echo
echo "To run it inside your existing Hyprland session, start it instead of (or alongside,"
echo "with its own sockets) the distro shell, e.g.:"
echo "   /usr/local/bin/caeliglow"
echo "To remove everything again:   bash <(curl -fsSL https://raw.githubusercontent.com/mockifylab/CaeliGlow/main/scripts/uninstall.sh)"
