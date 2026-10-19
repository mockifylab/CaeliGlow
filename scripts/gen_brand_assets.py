#!/usr/bin/env python3
# CaeliGlow brand asset generator — crescent-moon + sparkle logo.
#
# Recreates the CaeliGlow mark: a blue->violet->gold crescent moon cradling a
# large 4-point sparkle star, with small gold sparkles twinkling around it. The
# stars animate (twinkle + gentle pulse/rotate). Original artwork.
#
# Outputs (into docs/brand/assets/ unless OUT_DIR is set):
#   logo.svg             static mark (t=0), transparent, NO text
#   logo-animated.svg    SMIL twinkle version (browsers / web)
#   logo-animated.gif    looping animation (GitHub README / shell asset)
#   logo.png             static 512px PNG (transparent)
#   wordmark.svg         mark + "CaeliGlow" text lockup
#   frames/*.svg|png     scratch
#
# Toolchain: rsvg-convert + ImageMagick 'magick'.
# Run from repo root:  python3 scripts/gen_brand_assets.py

import math
import os
import shutil
import subprocess

OUT_DIR = os.environ.get("OUT_DIR", os.path.join("docs", "brand", "assets"))
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
S = 512
STEPS = 44
DELAY = 5  # centiseconds -> ~20 fps

# palette
NAVY = "#141a4d"
BLUE = "#3b49c9"
VIOLET = "#8b7cf6"
LILAC = "#c9bcff"
GOLD = "#f5c86b"
GOLD_HI = "#ffe6a8"
WHITE = "#ffffff"


def star_path(cx, cy, R, c_frac=0.16):
    """A 4-point sparkle with concave (curved) sides."""
    c = R * c_frac
    return (
        f"M {cx:.1f},{cy-R:.1f} "
        f"Q {cx+c:.1f},{cy-c:.1f} {cx+R:.1f},{cy:.1f} "
        f"Q {cx+c:.1f},{cy+c:.1f} {cx:.1f},{cy+R:.1f} "
        f"Q {cx-c:.1f},{cy+c:.1f} {cx-R:.1f},{cy:.1f} "
        f"Q {cx-c:.1f},{cy-c:.1f} {cx:.1f},{cy-R:.1f} Z")


# big star sits in the crescent's opening (right of centre)
BIG = (300, 256, 96)
# small gold sparkles around the opening (x, y, R, twinkle phase, cycles)
SMALLS = [
    (432, 150, 26, 0.0, 3),
    (250, 366, 20, 1.7, 2),
    (452, 344, 30, 3.3, 4),
    (392, 250, 14, 4.9, 3),
]

DEFS = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
<defs>
<linearGradient id="moon" x1="0.15" y1="0.05" x2="0.85" y2="0.95">
<stop offset="0%" stop-color="{NAVY}"/>
<stop offset="42%" stop-color="{BLUE}"/>
<stop offset="78%" stop-color="{VIOLET}"/>
<stop offset="100%" stop-color="{LILAC}"/>
</linearGradient>
<radialGradient id="bigstar" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{WHITE}"/>
<stop offset="45%" stop-color="{LILAC}"/>
<stop offset="100%" stop-color="{VIOLET}"/>
</radialGradient>
<radialGradient id="bigness" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{LILAC}" stop-opacity="0.55"/>
<stop offset="60%" stop-color="{VIOLET}" stop-opacity="0.18"/>
<stop offset="100%" stop-color="{VIOLET}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="goldness" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{GOLD_HI}" stop-opacity="0.7"/>
<stop offset="100%" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<mask id="crescent">
<rect width="{S}" height="{S}" fill="#000"/>
<circle cx="248" cy="256" r="206" fill="#fff"/>
<circle cx="356" cy="230" r="200" fill="#000"/>
</mask>
</defs>'''

TAIL = "</svg>"


def frame_body(t, hover=False):
    """Scene body for t in [0,1) (transparent background).

    hover=False -> the calm idle twinkle (used for the About logo + panel idle).
    hover=True  -> a clearly different, livelier motion for the power-panel logo on
    pointer hover: the big star makes a full seamless 360-degree turn, the glow
    pulses faster and brighter, and the small sparkles twinkle at double rate.
    """
    out = []
    # crescent moon
    out.append(f'<rect width="{S}" height="{S}" fill="url(#moon)" mask="url(#crescent)"/>')
    # warm glow on the two horn tips
    out.append(f'<circle cx="352" cy="112" r="30" fill="url(#goldness)"/>')
    out.append(f'<circle cx="356" cy="392" r="22" fill="url(#goldness)"/>')

    # big star: gentle pulse + small oscillating rotation (idle), or a full turn
    # + stronger pulse/glow (hover). Both are seamless over t in [0,1).
    bx, by, bR = BIG
    if hover:
        pulse = 1 + 0.12 * math.sin(math.tau * 3 * t)
        rot = 360.0 * t
        glow = 0.6 + 0.4 * (0.5 + 0.5 * math.sin(math.tau * 3 * t))
    else:
        pulse = 1 + 0.06 * math.sin(math.tau * 2 * t)
        rot = 6 * math.sin(math.tau * t)
        glow = 0.45 + 0.25 * (0.5 + 0.5 * math.sin(math.tau * 2 * t))
    out.append(f'<g transform="translate({bx},{by}) rotate({rot:.1f}) scale({pulse:.3f})">')
    out.append(f'<circle r="{bR*1.5:.0f}" fill="url(#bigness)" opacity="{glow:.2f}"/>')
    out.append(f'<path d="{star_path(0, 0, bR)}" fill="url(#bigstar)"/>')
    out.append('</g>')

    # small gold sparkles: twinkle (opacity + scale), staggered phases; livelier on hover
    for (x, y, r, ph, cyc) in SMALLS:
        rate = cyc * 2 if hover else cyc
        tw = 0.5 + 0.5 * math.sin(math.tau * rate * t + ph)
        op = (0.45 + 0.55 * tw) if hover else (0.35 + 0.6 * tw)
        sc = (0.75 + 0.6 * tw) if hover else (0.7 + 0.5 * tw)
        out.append(f'<g transform="translate({x},{y}) scale({sc:.3f})" opacity="{min(1,op):.2f}">')
        out.append(f'<circle r="{r*1.6:.0f}" fill="url(#goldness)"/>')
        out.append(f'<path d="{star_path(0, 0, r)}" fill="{GOLD}"/>')
        out.append('</g>')
    return "".join(out)


def write_frame_svg(idx):
    svg = DEFS + frame_body(idx / STEPS) + TAIL
    p = os.path.join(FRAMES_DIR, f"f_{idx:03d}.svg")
    with open(p, "w") as f:
        f.write(svg)
    return p


def smil_svg():
    """Self-contained SMIL twinkle for browsers/web."""
    bx, by, bR = BIG
    parts = [DEFS,
             '<rect width="%d" height="%d" fill="url(#moon)" mask="url(#crescent)"/>' % (S, S),
             f'<circle cx="352" cy="112" r="30" fill="url(#goldness)"/>',
             f'<g transform="translate({bx},{by})">',
             f'<path d="{star_path(0, 0, bR)}" fill="url(#bigstar)">',
             '<animateTransform attributeName="transform" type="rotate" '
             'values="-6;6;-6" dur="9s" repeatCount="indefinite"/>',
             '<animate attributeName="opacity" values="1;0.85;1" dur="3s" repeatCount="indefinite"/>',
             '</path></g>']
    for (x, y, r, ph, cyc) in SMALLS:
        dur = round(6.0 / cyc, 2)
        parts.append(f'<g transform="translate({x},{y})">')
        parts.append(f'<path d="{star_path(0, 0, r)}" fill="{GOLD}">')
        parts.append('<animate attributeName="opacity" values="0.35;1;0.35" '
                     f'dur="{dur}s" repeatCount="indefinite"/>')
        parts.append('<animateTransform attributeName="transform" type="scale" '
                     'values="0.7;1.2;0.7" ' f'dur="{dur}s" repeatCount="indefinite"/>')
        parts.append('</path></g>')
    parts.append(TAIL)
    return "".join(parts)


def wordmark_svg(mark):
    nested = mark.replace(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" '
        f'viewBox="0 0 {S} {S}">',
        f'<svg x="2" y="4" width="120" height="120" viewBox="0 0 {S} {S}">', 1)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="560" height="128" '
        'viewBox="0 0 560 128" role="img" aria-label="CaeliGlow wordmark">'
        '<defs><linearGradient id="wm" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{BLUE}"/>'
        f'<stop offset="55%" stop-color="{VIOLET}"/>'
        f'<stop offset="100%" stop-color="{LILAC}"/></linearGradient></defs>'
        + nested +
        '<text x="140" y="74" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif" '
        'font-size="54" font-weight="700" letter-spacing="0.5" fill="#EAF0FF">Caeli'
        f'<tspan fill="url(#wm)">Glow</tspan></text>'
        '<text x="142" y="100" font-family="Inter, Segoe UI, Helvetica Neue, Arial, sans-serif" '
        f'font-size="15" font-weight="500" letter-spacing="4.5" fill="{VIOLET}">'
        'NOCTALIA DESKTOP SHELL</text></svg>')


def emit_gif(out_name, hover, size, steps, delay):
    """Render `steps` frames of the mark (idle or hover motion) into a small
    transparent looping GIF at `size` px, for use as a bundled shell asset."""
    scratch = os.path.join(FRAMES_DIR, out_name)
    if os.path.isdir(scratch):
        shutil.rmtree(scratch)
    os.makedirs(scratch)
    pngs = []
    for i in range(steps):
        svg = DEFS + frame_body(i / steps, hover=hover) + TAIL
        sp = os.path.join(scratch, f"p_{i:03d}.svg")
        pp = os.path.join(scratch, f"p_{i:03d}.png")
        with open(sp, "w") as f:
            f.write(svg)
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), sp, "-o", pp], check=True)
        pngs.append(pp)
    subprocess.run(
        ["magick", "-delay", str(delay), "-loop", "0", *pngs,
         "-dispose", "Background", "-layers", "OptimizeTransparency",
         os.path.join(OUT_DIR, out_name)], check=True)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if os.path.isdir(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR)
    os.makedirs(FRAMES_DIR)

    for i in range(STEPS):
        write_frame_svg(i)
    for i in range(STEPS):
        svg = os.path.join(FRAMES_DIR, f"f_{i:03d}.svg")
        png = os.path.join(FRAMES_DIR, f"f_{i:03d}.png")
        subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", svg, "-o", png], check=True)

    with open(os.path.join(OUT_DIR, "logo.svg"), "w") as f:
        f.write(DEFS + frame_body(0.0) + TAIL)
    with open(os.path.join(OUT_DIR, "logo-animated.svg"), "w") as f:
        f.write(smil_svg())

    frames = [os.path.join(FRAMES_DIR, f"f_{i:03d}.png") for i in range(STEPS)]
    subprocess.run(
        ["magick", "-delay", str(DELAY), "-loop", "0", *frames,
         "-dispose", "Background", "-layers", "OptimizeTransparency",
         os.path.join(OUT_DIR, "logo-animated.gif")], check=True)
    subprocess.run(
        ["rsvg-convert", "-w", "512", "-h", "512",
         os.path.join(OUT_DIR, "logo.svg"), "-o",
         os.path.join(OUT_DIR, "logo.png")], check=True)

    with open(os.path.join(OUT_DIR, "logo.svg")) as f:
        mark = f.read()
    with open(os.path.join(OUT_DIR, "wordmark.svg"), "w") as f:
        f.write(wordmark_svg(mark))

    # Power-panel logo: two small (96px) transparent GIFs sharing the mark, one for
    # the calm idle state and one for the livelier pointer-hover state.
    emit_gif("logo-panel-idle.gif", hover=False, size=96, steps=30, delay=6)
    emit_gif("logo-panel-hover.gif", hover=True, size=96, steps=30, delay=3)
    print("moon logo assets generated")


if __name__ == "__main__":
    main()
