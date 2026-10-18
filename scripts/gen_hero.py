#!/usr/bin/env python3
# CaeliGlow GitHub hero generator.
#
# Takes the cinematic crescent-moon scene (docs/brand/assets/hero-source.png)
# and produces:
#   hero.png             static 1280-wide hero
#   social-preview.png   1280x640 centre crop (GitHub OG / repo social)
#   hero-animated.gif    subtle loop: twinkling gold sparkles + a "breathing"
#                        glow on the big star, screen-blended over the photo.
#
# The photo itself is not morphed (that would look bad in a 256-colour GIF);
# only small luminous overlays change per frame, so GIF delta-optimisation
# keeps the file compact.
#
# Toolchain: rsvg-convert + ImageMagick 'magick'.
# Run from repo root:  python3 scripts/gen_hero.py

import math
import os
import shutil
import subprocess

ASSETS = os.environ.get("OUT_DIR", os.path.join("docs", "brand", "assets"))
SRC = os.path.join(ASSETS, "hero-source.png")
TMP = os.path.join(ASSETS, "hero_frames")

GW, GH = 1000, 563          # animated GIF canvas
STEPS = 18
DELAY = 7                  # centiseconds (~14 fps, gentle)

# bright points, in GW x GH coordinates (scaled from the 1672x941 source)
BIG = (738, 263)            # the large star inside the crescent
SPARKS = [
    (763, 170, 22, 0.0, 3),
    (828, 344, 26, 1.6, 2),
    (535, 439, 20, 3.1, 4),
    (664, 308, 13, 4.6, 3),
    (300, 120, 15, 2.2, 2),
    (150, 300, 12, 5.2, 3),
]


def star_path(cx, cy, R, c_frac=0.16):
    c = R * c_frac
    return (f"M {cx:.1f},{cy-R:.1f} Q {cx+c:.1f},{cy-c:.1f} {cx+R:.1f},{cy:.1f} "
            f"Q {cx+c:.1f},{cy+c:.1f} {cx:.1f},{cy+R:.1f} "
            f"Q {cx-c:.1f},{cy+c:.1f} {cx-R:.1f},{cy:.1f} "
            f"Q {cx-c:.1f},{cy-c:.1f} {cx:.1f},{cy-R:.1f} Z")


def overlay_svg(t):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{GW}" height="{GH}" '
             f'viewBox="0 0 {GW} {GH}"><defs>'
             '<radialGradient id="g" cx="50%" cy="50%" r="50%">'
             '<stop offset="0%" stop-color="#fff3d6" stop-opacity="0.9"/>'
             '<stop offset="100%" stop-color="#fff3d6" stop-opacity="0"/></radialGradient>'
             '<radialGradient id="b" cx="50%" cy="50%" r="50%">'
             '<stop offset="0%" stop-color="#ffffff" stop-opacity="0.85"/>'
             '<stop offset="55%" stop-color="#c9bcff" stop-opacity="0.35"/>'
             '<stop offset="100%" stop-color="#8b7cf6" stop-opacity="0"/></radialGradient>'
             '</defs>']
    # breathing glow + tiny pulse on the big star
    pulse = 0.5 + 0.5 * math.sin(math.tau * 2 * t)
    bx, by = BIG
    parts.append(f'<circle cx="{bx}" cy="{by}" r="{70+30*pulse:.0f}" fill="url(#b)" '
                 f'opacity="{0.35+0.35*pulse:.2f}"/>')
    parts.append(f'<path d="{star_path(bx, by, 40+4*pulse)}" fill="#eef0ff" '
                 f'opacity="{0.7+0.3*pulse:.2f}"/>')
    # twinkling gold sparkles
    for (x, y, r, ph, cyc) in SPARKS:
        tw = 0.5 + 0.5 * math.sin(math.tau * cyc * t + ph)
        op = 0.15 + 0.85 * tw
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r*1.8:.0f}" fill="url(#g)" '
                     f'opacity="{op*0.5:.2f}"/>')
        parts.append(f'<path d="{star_path(x, y, r*(0.7+0.5*tw))}" fill="#ffe6a8" '
                     f'opacity="{op:.2f}"/>')
    parts.append('</svg>')
    return "".join(parts)


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    if os.path.isdir(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)

    base = os.path.join(TMP, "base.png")
    run(["magick", SRC, "-resize", f"{GW}x{GH}", base])

    for i in range(STEPS):
        ov_svg = os.path.join(TMP, f"ov_{i:02d}.svg")
        with open(ov_svg, "w") as f:
            f.write(overlay_svg(i / STEPS))
        ov_png = os.path.join(TMP, f"ov_{i:02d}.png")
        run(["rsvg-convert", "-w", str(GW), "-h", str(GH), ov_svg, "-o", ov_png])
        fr = os.path.join(TMP, f"fr_{i:02d}.png")
        run(["magick", base, ov_png, "-compose", "screen", "-composite", fr])

    frames = [os.path.join(TMP, f"fr_{i:02d}.png") for i in range(STEPS)]
    run(["magick", "-delay", str(DELAY), "-loop", "0", *frames,
         "-layers", "Optimize", os.path.join(ASSETS, "hero-animated.gif")])

    # static derivatives
    run(["magick", SRC, "-resize", "1280x", os.path.join(ASSETS, "hero.png")])
    run(["magick", SRC, "-resize", "1280x640^", "-gravity", "center",
         "-extent", "1280x640", os.path.join(ASSETS, "social-preview.png")])

    shutil.rmtree(TMP)
    print("hero assets generated")


if __name__ == "__main__":
    main()
