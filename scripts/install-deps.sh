#!/usr/bin/env bash
# CaeliGlow build dependencies (Arch/CachyOS).
# ADDITIVE ONLY: this script never removes packages and never touches boot/EFI/partitions.
# Mirrors the Noctalia 5.3.0 ARCH dependency set from upstream BUILDING.md, plus ninja.
set -euo pipefail

DEPS=(
  meson ninja gcc just
  wayland wayland-protocols libglvnd
  freetype2 fontconfig cairo pango harfbuzz
  libxkbcommon glib2 libsecret libsodium
  sdbus-cpp libpipewire wireplumber polkit
  pam curl libwebp libjxl libsndfile librsvg
  libqalculate libxml2 md4c tomlplusplus libical
  nlohmann-json stb jemalloc
)

echo ">> Installing (only-if-needed) build dependencies; no removals performed."
sudo pacman -S --needed --noconfirm "${DEPS[@]}"

echo ">> Dependency install complete."
