#!/usr/bin/env bash
# Apply the CaeliGlow patch series onto the pinned Noctalia checkout.
# Idempotent-ish: it refuses to run if the tree is already patched, so you never
# double-apply. Use scripts/reset-patches.sh to return to a clean tree.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NOCTALIA_DIR="${CAELIGLOW_NOCTALIA_DIR:-$HERE/upstream/noctalia}"
SERIES="$HERE/patches/series"

# A populated submodule stores .git as a gitlink FILE ("gitdir: ..."), while a
# standalone clone stores it as a DIRECTORY. Test for existence, not -d, so the
# pinned submodule checkout is correctly recognised as present.
if [[ ! -e "$NOCTALIA_DIR/.git" ]]; then
  echo "error: Noctalia checkout not found at: $NOCTALIA_DIR" >&2
  echo "       Run 'git submodule update --init --recursive' first." >&2
  exit 1
fi

cd "$NOCTALIA_DIR"

# Detect an already-applied series: CaeliGlow patch commits use a 'caeliglow:' subject prefix.
if git log -5 --format='%s' 2>/dev/null | grep -qE '^caeliglow:'; then
  echo "error: patch series appears already applied to $NOCTALIA_DIR" >&2
  echo "       Run scripts/reset-patches.sh before re-applying." >&2
  exit 1
fi

echo ">> Applying patch series from $SERIES"
mapfile -t PATCHES < <(grep -vE '^\s*(#|$)' "$SERIES")
for p in "${PATCHES[@]}"; do
  echo "   + $p"
  git am --3way "$HERE/patches/$p"
done
echo ">> All $(( ${#PATCHES[@]} )) patches applied."
