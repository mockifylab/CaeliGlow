# CaeliGlow Asset Inventory

All brand assets live in `docs/brand/assets/`. Vector assets are the source of truth;
raster exports are generated from them (or, for the hero, authored separately) and are
safe to regenerate.

| File | Type | Dimensions / size | Purpose | Regenerate / notes |
|------|------|-------------------|---------|--------------------|
| `logo.svg` | SVG | 128×128 viewBox | App icon, favicon, avatar, anywhere a square mark is needed | Hand-authored; scales losslessly |
| `wordmark.svg` | SVG | 520×128 viewBox | README hero, page headers, titles | References system fonts (Inter w/ fallbacks) |
| `social-preview.png` | PNG | 1280×731, ~700 KB | GitHub repo "Social preview" + README banner | Under GitHub's 1 MB cap; sRGB, stripped metadata |

## Usage checklist

- **GitHub → Settings → Social preview:** upload `assets/social-preview.png`.
- **Repository About / description icon:** use `assets/logo.svg` (GitHub resizes it).
- **README top:** `wordmark.svg` (title lockup) over the `social-preview.png` hero.

## Provenance & licensing

- All assets are **original CaeliGlow artwork**, MIT-licensed with the code.
- They intentionally reuse **no** Noctalia or Caelestia logos/artwork. The mark is an
  abstract aurora arc, not derived from any upstream icon.
- If you export new raster sizes, keep total ≤ 1 MB and sRGB for GitHub.

## Palette tokens (for any future asset)

`#0B1020` `#12172B` `#1D2547` · aurora `#4FE0C4` → `#8B7CF6` → `#F5C86B` · text
`#EAF0FF` `#B9C4E8` `#7E8AB5`. See `brand-guidelines.md`.
