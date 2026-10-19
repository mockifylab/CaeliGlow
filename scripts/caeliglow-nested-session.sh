#!/usr/bin/env bash
# CaeliGlow v1.4.0 test launcher.
# Starts a nested Hyprland compositor in a window on your CURRENT desktop and
# runs the patched CaeliGlow shell inside it. Fully isolated: your live
# /usr/bin/noctalia keeps running untouched. Close the nested window (or the
# terminal it was started from) to end the test session.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TREE="$HERE/upstream/noctalia"
BIN="$TREE/build-debug/noctalia"
CONF="$HERE/test/hyprland-nested.conf"
LOG="$HERE/test/nested-hyprland.log"

if [[ ! -x "$BIN" ]]; then
  echo "error: CaeliGlow binary not found at: $BIN" >&2
  echo "       Build it first: scripts/build.sh debug" >&2
  exit 1
fi

if [[ -z "${WAYLAND_DISPLAY:-}" ]]; then
  echo "error: no WAYLAND_DISPLAY in the environment; a running Wayland session is" >&2
  echo "       required to open a nested compositor window." >&2
  exit 1
fi

# Restore the animated-logo asset into the shell's runtime asset path.
export NOCTALIA_ASSETS_DIR="$TREE/assets"
export CAELIGLOW_TEST=1

mkdir -p "$HERE/test"
echo ">> Starting nested Hyprland (CaeliGlow v1.4.0). Log: $LOG"
echo ">> Assets dir: $NOCTALIA_ASSETS_DIR"
# Hyprland 0.56+ removed the --nested flag: nesting is done by forcing the
# wayland backend, which opens the compositor as a window under the host.
# exec-once in the config launches noctalia inside the nested session so it
# picks up the nested Wayland socket.
export HYPRLAND_BACKEND=wayland
exec Hyprland --config "$CONF" 2>&1 | tee "$LOG"
