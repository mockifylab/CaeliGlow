# CaeliGlow Asset Inventory

All brand assets live in `docs/brand/assets/`. The **logo mark is a crescent moon
cradling a large 4-point sparkle star, ringed by smaller twinkling gold sparkles** —
a "glow in the night sky" motif. Vector/scene sources are the generator scripts;
raster and GIF exports are derived and safe to regenerate.

| File | Type | Dimensions / size | Purpose | Regenerate / notes |
|------|------|-------------------|---------|--------------------|
| `logo.svg` | SVG | 512×512 viewBox | Static square mark (transparent, no text) | `scripts/gen_brand_assets.py` |
| `logo.png` | PNG | 512×512, transparent | Favicon, avatar, app icon | `scripts/gen_brand_assets.py` |
| `logo-animated.gif` | GIF | 256×256, ~140 KB | **Animated mark** — twinkling stars + pulsing sparkle | `scripts/gen_brand_assets.py` |
| `logo-animated.svg` | SVG (SMIL) | 512×512 | Same animation for browsers/web | `scripts/gen_brand_assets.py` |
| `wordmark.svg` | SVG | 560×128 viewBox | README/headers title lockup (mark + "CaeliGlow") | `scripts/gen_brand_assets.py` |
| `hero-animated.gif` | GIF | 1000×563, ~516 KB | **Animated GitHub hero** — cinematic moon scene, twinkling stars | `scripts/gen_hero.py` |
| `hero.png` | PNG | 1280 wide | Static hero (fallback / where GIF not wanted) | `scripts/gen_hero.py` |
| `hero-source.png` | PNG | 1672×941 | Authored source scene the hero is derived from | keep as the regeneration source |
| `social-preview.png` | PNG | 1280×640, ~816 KB | GitHub repo "Social preview" (Settings → Social preview) | `scripts/gen_hero.py`; ≤ 1 MB, sRGB |

## In-shell asset

- `upstream/noctalia/assets/caeliglow/logo-animated.gif` — a **128px** variant of the
  animated mark, bundled with the shell and rendered in the Settings › About header
  (installed automatically via Noctalia's `install_subdir('assets', …)`). It is a copy
  of `logo-animated.gif` resized for a small resident-memory footprint (~2 MB of
  decoded frames while About is open, freed on close).

## Regenerating

```sh
python3 scripts/gen_brand_assets.py     # mark, wordmark, logo GIF/PNG/SVG
python3 scripts/gen_hero.py             # hero GIF/PNG + social-preview (needs hero-source.png)
# refresh the in-shell variant after changing the mark:
magick docs/brand/assets/logo-animated.gif -coalesce -resize 128x128 \
  -layers Optimize upstream/noctalia/assets/caeliglow/logo-animated.gif
```

## Provenance & licensing

- All assets are **original CaeliGlow artwork**, MIT-licensed with the code.
- They intentionally reuse **no** Noctalia or Caelestia logos/artwork. The crescent-and-
  sparkle mark is drawn from scratch (vector) / authored as an original scene; it is not
  derived from any upstream icon.
- If you export new raster sizes, keep total ≤ 1 MB and sRGB for GitHub.

## Palette tokens

Deep-night `#141A4D` `#0B1020` `#12172B` · crescent blue→violet `#3B49C9` → `#8B7CF6` →
`#C9BCFF` · sparkle gold `#F5C86B` / `#FFE6A8` · aurora accents `#4FE0C4` · text
`#EAF0FF` `#B9C4E8` `#7E8AB5`. See `brand-guidelines.md`.
