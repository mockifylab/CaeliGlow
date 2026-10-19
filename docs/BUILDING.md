# Building CaeliGlow from source

CaeliGlow builds **Noctalia from source** with its own `meson` + `just` toolchain,
after applying the `patches/` series. It is verified on **CachyOS + Hyprland**; any
Arch-based distro with the packages below should work.

## Prerequisites

C++23 compiler (GCC 13+ / Clang 16+), meson, ninja, just, and Noctalia's dependency
set. On Arch/CachyOS the fastest path is the additive install script (it never
removes packages and never touches boot/EFI/partitions):

```sh
sudo ./scripts/install-deps.sh
```

Equivalent manual list (Arch):
`meson ninja gcc just wayland wayland-protocols libglvnd freetype2 fontconfig cairo
pango harfbuzz libxkbcommon glib2 libsecret libsodium sdbus-cpp libpipewire
wireplumber polkit pam curl libwebp libjxl libsndfile librsvg libqalculate libxml2
md4c tomlplusplus libical nlohmann-json stb jemalloc`

## Steps

```sh
git clone --recursive https://github.com/mockifylab/CaeliGlow.git
cd CaeliGlow

./scripts/build.sh release /usr/local     # apply patches + build (build-release/)
sudo ./scripts/install.sh release /usr/local
```

`build.sh` performs: `git submodule` pin check → `scripts/apply-patches.sh` →
`just configure release <prefix>` → `just build release`. The binary lands at
`upstream/noctalia/build-release/noctalia` before you install it, so you can run it
directly first:

```sh
./upstream/noctalia/build-release/noctalia --version
```

## One-command install

For day-to-day use there is a scripted installer — one line, no clone needed:

```sh
curl -fsSL https://raw.githubusercontent.com/mockifylab/CaeliGlow/main/scripts/quick-install.sh | bash
```

`scripts/quick-install.sh` clones the repo (pinned submodule included), installs
dependencies additively, applies the patch series, builds a release and installs it
under `/usr/local` — the binary is renamed to **`caeliglow`** so it never shadows the
distro `noctalia` on your `PATH`. It also registers a **CaeliGlow entry in the greeter**
(`/usr/local/bin/caeliglow-session` + `share/wayland-sessions/caeliglow.desktop`, opt out
with `CAELIGLOW_SESSION_ENTRY=0`); branch your Hyprland Lua autostart on `CAELIGLOW_SESSION`
so the default session keeps launching `/usr/bin/noctalia`. Remove everything again with
`scripts/uninstall.sh` (same URL pattern; add `--purge` to also delete `~/.config/caeliglow`
and friends).

## Pacman-native package (AUR-ready)

`pkgbuild/PKGBUILD` builds the exact same recipe as an Arch package named `caeliglow`:

```sh
cd pkgbuild && makepkg -si          # build + install through pacman
sudo pacman -R caeliglow            # clean removal, files tracked by pacman
```

The package deliberately installs under `/usr/local` (binary `caeliglow`, own desktop
entry) so it can never file-conflict with the packaged `noctalia` under `/usr`.
Once the directory is submitted to the AUR, `paru -S caeliglow` becomes the literal
one-command install.

## Debug / iterate

```sh
./scripts/apply-patches.sh
cd upstream/noctalia
just configure debug /usr/local && just build debug && just test debug
cd ../..
./scripts/reset-patches.sh         # back to a clean pinned tree
```

## Verified baseline (Noctalia v5.3.0, unpatched)

On the reference machine the **unmodified** v5.3.0 tree configured with meson 1.12,
built in ~12 min (770 targets), linked a working `noctalia` binary, and passed the
full unit suite: **153/153 OK, 0 failures**. CaeliGlow patch 0001 rebuilt and
re-linked incrementally (bar.cpp) without errors.

## Run / test notes

- Launching CaeliGlow replaces the running shell. On a live desktop, start it from a
  TTY or a fresh Hyprland instance rather than over your current session.
- Noctalia ships runtime assets; install the full tree (`meson install`), not just
  the binary.
