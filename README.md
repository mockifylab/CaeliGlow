# CaeliGlow

A polished, **Noctalia-based** desktop shell for **CachyOS + Hyprland**.

CaeliGlow is **not** a rewrite and **not** a plugin. It is a small, clearly
documented **patch series applied to a pinned Noctalia release**, then built and
packaged from source as its own shell. Everything that makes Noctalia feel like
Noctalia — its bar, widgets, launcher, theme, settings and behavior — is
**preserved**. CaeliGlow adds or replaces only a few specific interactions, in
the spirit of [Caelestia Shell](https://github.com/caelestia-dots/shell)'s
edge/hover feel, but **independently re-implemented** (see
[Licensing](#licensing--attribution)).

---

## What CaeliGlow changes

| Area | Change |
|------|--------|
| **Bar hover** | Caelestia-style hover response on bar widgets (animated highlight/accordion expansion), with Noctalia's contents, layout and styling kept. |
| **Bottom edge** | A bottom-edge hover trigger reveals the **existing** Noctalia launcher (concave-to-edge reveal, dwell/debounce, safe dismiss). |
| **Right edge** | A right-edge, vertically-mounted power rail (Shut Down / Restart / Suspend / Log Out) with hover/focus labels and an explicit confirmation step for destructive actions. The duplicate original power entry is removed. |
| **Settings › About** | A native "CaeliGlow" About section (name, version, developer, GitHub) with an update checker against GitHub releases. |

## What CaeliGlow deliberately leaves unchanged

- Noctalia's bar, widgets, their appearance and functionality.
- The launcher UI (the same launcher is revealed by the edge trigger).
- The theme/palette system and general settings.
- Ordinary Noctalia behavior everywhere not listed above.

---

## Architecture note (important)

Modern **Noctalia (v5.x) is a native C++ Wayland shell** with its own scene
graph, GLES renderer and Pango/Cairo text — it is **not** a Quickshell/QML
application. CaeliGlow therefore patches C++ source and rebuilds with Noctalia's
own `meson` + `just` toolchain. CaeliGlow **1.0.0** is pinned to **Noctalia
v5.3.0**.

## Supported environment

- **OS:** CachyOS / Arch (any Arch-based distro should work)
- **Compositor:** Hyprland (Wayland)
- **Pinned upstream:** Noctalia `v5.3.0`
- **Toolchain:** C++23 compiler (GCC 13+ / Clang 16+), meson, ninja, just

## Install

```sh
git clone --recursive https://github.com/mockifylab/CaeliGlow.git
cd CaeliGlow

# 1) Build dependencies (additive only; no removals, never touches boot/EFI):
sudo ./scripts/install-deps.sh

# 2) Apply patches + build (release):
./scripts/build.sh release /usr/local

# 3) Install to /usr/local (does NOT overwrite pacman's /usr/bin/noctalia):
sudo ./scripts/install.sh release /usr/local
```

Then set `/usr/local/bin/noctalia` as your shell in your Hyprland autostart.
Because the distro package at `/usr/bin/noctalia` is untouched, you can always
fall back. See [docs/UPDATING.md](docs/UPDATING.md) for update-checker, backup
and rollback.

## Uninstall / restore ordinary Noctalia

```sh
./scripts/rollback.sh release /usr/local
```

## Documentation

- [docs/BUILDING.md](docs/BUILDING.md) — building from source in detail
- [docs/PATCHES.md](docs/PATCHES.md) — the patch series, per-patch rationale
- [docs/UPDATING.md](docs/UPDATING.md) — safe update + rollback
- [docs/ATTRIBUTION.md](docs/ATTRIBUTION.md) — credits & licensing

## Development

```sh
./scripts/apply-patches.sh        # patch the pinned tree
# edit upstream/noctalia ...
(cd upstream/noctalia && just configure debug && just build debug && just test debug)
./scripts/reset-patches.sh        # back to clean Noctalia
```

## Licensing & attribution

- CaeliGlow original code: **MIT** (Copyright © 2026 Aasif / mockifylab).
- Built on **Noctalia** — **MIT**, Copyright © 2026 noctalia-dev. Upstream
  copyright and license are preserved.
- **Caelestia Shell** is **GPL-3.0**. CaeliGlow **copies no Caelestia code or
  assets**; "Caelestia-style" refers to independently re-implemented behavior
  only. There is **no affiliation with or endorsement by** Noctalia or Caelestia.

## Known limitations

Runtime behavior was verified as far as the build/test environment allowed (see
[docs/PATCHES.md](docs/PATCHES.md) for what is unit-tested vs. desktop-tested).
Edge-reveal parity with Caelestia's exact motion is approximated, not byte-for-
byte identical, because it is an independent re-implementation on Noctalia's
architecture. Multi-monitor and fractional-scaling behavior should be re-checked
on your exact display setup.

---

**Version:** 1.0.0 · **Developer:** Aasif · **GitHub:** https://github.com/mockifylab/CaeliGlow
