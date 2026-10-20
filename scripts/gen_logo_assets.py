#!/usr/bin/env python3
# CaeliGlow logo asset generator — raster-derived from the authored source mark.
#
# The canonical brand mark is a single transparent raster source:
#   docs/brand/assets/logo-source.png   (the "three-stars" mark: a dark new-moon
#   disc cradled by a cyan crescent glow, ringed by three cyan sparkle stars).
#
# This script derives every shipped logo asset from that one source so the shell,
# the README, and the app icon never drift apart. It adds a *restrained*, seamless
# "breathing + twinkle" loop (sub-pixel scale pulse + gentle brightness shimmer)
# rather than inventing new motion, matching the calm shell motion language.
#
# Outputs
#   docs/brand/assets/
#     logo.png              static 512px transparent mark (icon / favicon / avatar)
#     logo-animated.gif     256px calm breathing loop (README / web)
#   upstream/noctalia/assets/caeliglow/   (bundled with the shell, installed via
#                                          Noctalia's install_subdir('assets', …))
#     logo.png              512px app-icon source (internal_app_metadata)
#     logo-animated.gif     128px About-hero loop (settings_content_about)
#     logo-panel-idle.gif   96px  power-pill / launcher avatar idle twinkle
#     logo-panel-hover.gif  96px  livelier pulse for pointer-hover
#
# Toolchain: ImageMagick 'magick' only. Run from repo root:
#   python3 scripts/gen_logo_assets.py
#
# MIT licensed; original CaeliGlow artwork (the source mark was authored for this
# project). No Noctalia or Caelestia logos/artwork are used.

import os
import shutil
import subprocess
import math

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "docs", "brand", "assets", "logo-source.png")
BRAND_DIR = os.path.join(REPO, "docs", "brand", "assets")
SHELL_DIR = os.path.join(REPO, "upstream", "noctalia", "assets", "caeliglow")


def run(args):
    subprocess.run(args, check=True)


def emit_loop(out_path, base, steps, delay, scale_amp, rot_amp, bright_amp):
    """Render a seamless breathing+twinkle loop from the static source.

    The scale uses 1 + amp*(0.5 - 0.5*cos(2*pi*t)) so it starts and ends at 1.0
    (always >= 1.0, no clipping of the resting size) and the rotation / brightness
    use full cosine periods — every channel is periodic over t in [0,1), so the
    GIF loops with no visible seam.
    """
    canvas = int(round(base * (1.0 + scale_amp) * 1.06))  # headroom for scale + rotation
    scratch = os.path.join(BRAND_DIR, ".logo_frames")
    if os.path.isdir(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)

    pngs = []
    for i in range(steps):
        t = i / steps
        s = 1.0 + scale_amp * (0.5 - 0.5 * math.cos(2 * math.pi * t))
        rot = rot_amp * math.sin(2 * math.pi * t)
        bright = 100.0 + bright_amp * (0.5 - 0.5 * math.cos(2 * math.pi * t))
        size = int(round(base * s))
        frame = os.path.join(scratch, f"p_{i:03d}.png")
        # Resize the mark, apply the shimmer, then center it on a transparent canvas.
        cmd = [
            "magick", SRC,
            "-background", "none", "-resize", f"{size}x{size}",
            "-modulate", f"{bright:.1f},104,100",
        ]
        if abs(rot) > 0.01:
            cmd += ["-rotate", f"{rot:.2f}"]
        cmd += ["-gravity", "center", "-extent", f"{canvas}x{canvas}", frame]
        run(cmd)
        pngs.append(frame)

    run(["magick", "-delay", str(delay), "-loop", "0", *pngs,
         "-dispose", "Background", "-layers", "OptimizeTransparency", out_path])
    shutil.rmtree(scratch)


def main():
    if not os.path.exists(SRC):
        raise SystemExit(f"missing logo source: {SRC}")
    os.makedirs(SHELL_DIR, exist_ok=True)

    # Static icon (docs + shell app-icon).
    run(["magick", SRC, "-background", "none", "-resize", "512x512",
         os.path.join(BRAND_DIR, "logo.png")])
    shutil.copyfile(os.path.join(BRAND_DIR, "logo.png"),
                    os.path.join(SHELL_DIR, "logo.png"))

    # Calm breathing loop for README/web (docs) and the About hero (shell, 128px).
    emit_loop(os.path.join(BRAND_DIR, "logo-animated.gif"),
              base=256, steps=30, delay=6, scale_amp=0.035, rot_amp=0.0, bright_amp=6.0)
    emit_loop(os.path.join(SHELL_DIR, "logo-animated.gif"),
              base=128, steps=26, delay=6, scale_amp=0.035, rot_amp=0.0, bright_amp=6.0)

    # Power-pill / launcher avatar: a calm idle twinkle and a livelier hover pulse.
    emit_loop(os.path.join(SHELL_DIR, "logo-panel-idle.gif"),
              base=96, steps=24, delay=7, scale_amp=0.03, rot_amp=0.0, bright_amp=5.0)
    emit_loop(os.path.join(SHELL_DIR, "logo-panel-hover.gif"),
              base=96, steps=20, delay=4, scale_amp=0.06, rot_amp=4.0, bright_amp=9.0)

    print("logo assets regenerated from", os.path.relpath(SRC, REPO))


if __name__ == "__main__":
    main()
