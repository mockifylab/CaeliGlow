# CaeliGlow Asset Inventory

All brand assets live in `docs/brand/assets/`. The **logo mark is the "three-stars"
eclipse: a dark new-moon disc cradled by a cyan crescent glow, ringed by three cyan
sparkle stars** — a "glow in the night sky" motif. Since v1.6 the canonical source is
a single authored raster, `logo-source.png`; every shipped logo asset is derived from
it by `scripts/gen_logo_assets.py` so shell, README, and app icon never drift apart.

| File | Type | Dimensions / size | Purpose | Regenerate / notes |
|------|------|-------------------|---------|--------------------|
| `logo-source.png` | PNG | 1254×1254, transparent | **Canonical mark source** (authored art) | keep as the regeneration source |
| `logo.png` | PNG | 512×512, transparent | Favicon, avatar, app icon | `scripts/gen_logo_assets.py` |
| `logo-animated.gif` | GIF | ~272px, calm breathing loop | **Animated mark** — restrained pulse + twinkle | `scripts/gen_logo_assets.py` |
| `wordmark.svg` | SVG | 560×128 viewBox | README/headers title lockup (mark + "CaeliGlow") | embeds `logo.png`; regenerate after changing it |
| `hero.png` | PNG | 1280×720 | **README hero** — eclipse mark + "CaeliGlow" wordmark over a dark code backdrop (static since v1.6.1) | `scripts/gen_hero.py` |
| `hero-source.png` | PNG | 1672×941 | Authored hero art the derivatives come from | keep as the regeneration source |
| `social-preview.png` | PNG | 1280×640, ~248 KB | GitHub repo "Social preview" (Settings → Social preview) | `scripts/gen_hero.py`; ≤ 1 MB, sRGB |
| `logo.svg`, `logo-animated.svg`, `frames/` | SVG | 512×512 | **Legacy** procedural crescent (pre-v1.6 mark) | kept for history; superseded by `logo-source.png` |

## In-shell assets (`upstream/noctalia/assets/caeliglow/`)

Written directly by `scripts/gen_logo_assets.py` (installed automatically via
Noctalia's `install_subdir('assets', …)`):

- `logo.png` — 512px app-icon source (`internal_app_metadata`).
- `logo-animated.gif` — 128px About-hero loop (`settings_content_about`).
- `logo-panel-idle.gif` / `logo-panel-hover.gif` — 96px calm twinkle and livelier
  hover pulse used by the power pill logo and the launcher avatar
  (`caeliglow::AnimatedImage`).

## Regenerating

```sh
python3 scripts/gen_logo_assets.py    # logo PNG/GIFs: docs + in-shell (from logo-source.png)
python3 scripts/gen_hero.py           # hero.png + social-preview (needs hero-source.png)
```

## Provenance & licensing

- All assets are **original CaeliGlow artwork**, MIT-licensed with the code.
- They intentionally reuse **no** Noctalia or Caelestia logos/artwork. The
  three-stars eclipse mark was authored for this project.
- If you export new raster sizes, keep total ≤ 1 MB and sRGB for GitHub.

## Palette tokens

Deep-night `#141A4D` `#0B1020` `#12172B` · crescent blue→violet `#3B49C9` → `#8B7CF6` →
`#C9BCFF` · sparkle gold `#F5C86B` / `#FFE6A8` · aurora accents `#4FE0C4` · mark cyan
`#7FE9FF` → `#28C8F0` · text `#EAF0FF` `#B9C4E8` `#7E8AB5`. See `brand-guidelines.md`.
