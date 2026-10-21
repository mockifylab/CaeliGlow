#!/usr/bin/env python3
# CaeliGlow GitHub hero generator.
#
# Takes the authored hero art (docs/brand/assets/hero-source.png) and produces
# the static derivatives used by the repo:
#   hero.png             static 1280-wide README hero
#   social-preview.png   1280x640 centre crop (GitHub OG / repo social)
#
# Since v1.6.1 the hero is a single authored eclipse + wordmark image, so the
# README uses the static PNG (the earlier crescent-scene animation was tied to
# hand-placed sparkle coordinates that no longer match the art).
#
# Toolchain: ImageMagick 'magick'.
# Run from repo root:  python3 scripts/gen_hero.py

import os
import subprocess

ASSETS = os.environ.get("OUT_DIR", os.path.join("docs", "brand", "assets"))
SRC = os.path.join(ASSETS, "hero-source.png")


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    run(["magick", SRC, "-resize", "1280x", os.path.join(ASSETS, "hero.png")])
    run(["magick", SRC, "-resize", "1280x640^", "-gravity", "center",
         "-extent", "1280x640", "-strip", "-quality", "92",
         os.path.join(ASSETS, "social-preview.png")])
    print("hero assets generated")


if __name__ == "__main__":
    main()
