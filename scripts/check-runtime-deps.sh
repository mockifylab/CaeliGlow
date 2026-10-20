#!/usr/bin/env bash
# CaeliGlow runtime dependency gate.
#
# Catch "error while loading shared libraries" startup failures BEFORE they
# happen on a live desktop. Those loader errors fire before the shell's own
# logger starts, so they are invisible in ~/.cache/caeliglow/caeliglow.log —
# this check resolves every shared library of the built/installed binary and
# reports any "not found" entry with the pacman package that provides it.
#
#   ./scripts/check-runtime-deps.sh [path-to-binary]
#
# Default binary order: explicit argument, $CAELIGLOW_BIN, /usr/local/bin/caeliglow,
# upstream/noctalia/build-release/noctalia. Exit 0 = all libraries resolve.
set -euo pipefail

find_binary() {
  if [[ $# -ge 1 && -n "${1:-}" ]]; then
    printf '%s\n' "$1"
    return 0
  fi
  if [[ -n "${CAELIGLOW_BIN:-}" ]]; then
    printf '%s\n' "$CAELIGLOW_BIN"
    return 0
  fi
  local candidate
  for candidate in /usr/local/bin/caeliglow \
                   upstream/noctalia/build-release/noctalia \
                   upstream/noctalia/build-debug/noctalia; do
    if [[ -x "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done
  return 1
}

BIN="$(find_binary "$@")" || {
  echo "error: no CaeliGlow binary found; build it first or pass its path." >&2
  exit 1
}

if ! command -v ldd >/dev/null 2>&1; then
  echo "error: ldd not available (glibc); cannot verify shared libraries." >&2
  exit 1
fi

echo ">> Checking shared-library resolution for: $BIN"
MISSING="$(ldd "$BIN" 2>/dev/null | grep 'not found' || true)"
if [[ -n "$MISSING" ]]; then
  echo "error: $BIN has unresolved shared libraries:" >&2
  printf '%s\n' "$MISSING" >&2
  # Map each missing soname back to its pacman package so the fix is one command.
  FILES="$(printf '%s\n' "$MISSING" | awk '{print $1}' | sort -u)"
  echo ">> Missing libraries and their pacman providers:" >&2
  declare -A REPORTED=()
  while IFS= read -r so; do
    [[ -z "$so" ]] && continue
    PKGS="$(pacman -F --quiet "$so" 2>/dev/null | awk -F/ '{print $1}' | sort -u | paste -sd' ' - || true)"
    if [[ -n "$PKGS" && -z "${REPORTED[$PKGS]:-}" ]]; then
      REPORTED["$PKGS"]=1
      echo "   $so -> sudo pacman -S --needed $PKGS" >&2
    fi
  done <<< "$FILES"
  echo "note: 'pacman -F' needs an updated file database (sudo pacman -Fy)." >&2
  echo "note: if a provider was installed as a dependency and later orphan-" >&2
  echo "      removed, re-mark it explicit: sudo pacman -D --asexplicit <pkg>." >&2
  exit 1
fi

# Smoke-launch the loader path itself: --version exits before any Wayland
# connection is attempted, so it proves the binary actually starts.
if "$BIN" --version >/dev/null 2>&1; then
  echo ">> OK: all shared libraries resolve and the binary launches (--version)."
else
  echo "error: all libraries resolved but '$BIN --version' failed; see output above." >&2
  "$BIN" --version || true
  exit 1
fi
