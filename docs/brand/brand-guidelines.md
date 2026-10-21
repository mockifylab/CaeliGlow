# CaeliGlow Brand Guidelines

CaeliGlow is a calm, premium, night-sky aesthetic: **a luminous crescent moon cradling
a glowing star, over a deep indigo night**. It signals "Noctalia, but warmer and more
alive" — restrained motion, luminous accents, generous negative space. Never loud, never
busy.

## Name

- Written as one word: **CaeliGlow** (capital **C**, capital **G**).
- "Caeli" (Latin, *of the sky*) + "Glow". Never "Caeli Glow", "Caeliglow", or "CG".
- Tagline (when needed): *A polished Noctalia desktop shell for CachyOS + Hyprland.*

## Logo

The mark is a **crescent moon** (deep-navy → blue → violet gradient, warm gold tips on
the two horns) cradling a large **4-point sparkle star** (white core fading to violet),
ringed by smaller **twinkling gold sparkles**. It reads as "a glow in the night sky."

- **Static mark** — `assets/logo.svg` / `assets/logo.png`: transparent, no text. Use
  wherever a square icon is needed (app icon, favicon, avatars).
- **Animated mark** — `assets/logo-animated.gif` / `assets/logo-animated.svg`: the same
  scene with the stars twinkling and the central sparkle pulsing. Use in motion contexts
  (README, web) and **in-shell** — a 128px variant is bundled and rendered in Settings ›
  About.
- **Wordmark lockup** — `assets/wordmark.svg`: mark + "CaeliGlow" + eyebrow. Use for
  headers, README, titles.
- **Hero / social preview** — `assets/hero.png` (README hero, 1280×720) and
  `assets/social-preview.png` (1280×640, <1 MB, for the GitHub "Social preview" setting):
  the eclipse mark with the "CaeliGlow" wordmark over a dark code backdrop (static
  since v1.6.1; the earlier animated crescent-scene hero was retired).

Rules:

- Keep clear space around the mark equal to the height of the crescent's opening.
- Minimum on-screen size for the mark: **32 px**. Below that, use the static PNG.
- The animation is **subtle** — twinkle + gentle pulse only. Never spin, bounce, or add
  busy motion; it must stay calm.
- Never recolor the crescent/sparkle gradients, stretch, rotate, add drop shadows, or
  place the wordmark on a busy photo without a dark scrim.
- Never reuse **Noctalia's** or **Caelestia's** logos; CaeliGlow is an independent,
  unaffiliated customization (see `docs/ATTRIBUTION.md`).

## Color

| Role | Hex | Name | Use |
|------|-----|------|-----|
| Background | `#0B1020` | Night | Primary canvas / plates |
| Surface | `#12172B` | Deep night | Cards, panels |
| Hairline | `#1D2547` | Faint indigo | Borders, dividers |
| Aurora Teal | `#4FE0C4` | Glow-cyan | Accent start, positive |
| Aurora Violet | `#8B7CF6` | Glow-violet | Accent mid, links |
| Aurora Amber | `#F5C86B` | Glow-gold | Accent end, stars, highlights |
| Text | `#EAF0FF` | Moonlight | Primary text |
| Text muted | `#B9C4E8` | Haze | Secondary text |
| Text dim | `#7E8AB5` | Slate | Eyebrows, captions |

The crescent runs **navy → blue → violet** (`#141A4D` → `#3B49C9` → `#8B7CF6`); the
sparkles are **gold** (`#F5C86B` / `#FFE6A8`) with the central star fading **white →
violet**. The aurora trio **Teal → Violet → Amber** remains the general UI accent ramp
(links, highlights, badges); a single one may be used for a small accent.

## Typography

- **UI / headings:** Inter (fallback: Segoe UI, Helvetica Neue, Arial). Wordmark is
  700 weight.
- **Eyebrows / labels:** Inter 500, +4 tracking, `#7E8AB5`.
- **Code / terminals:** any monospaced JetBrains Mono / Cascadia / monospace.
- No proprietary font files are shipped; all faces above are system/web-safe fallbacks.

## Voice

Clear, precise, quietly confident. Technical honesty over hype: we state what is
*verified* vs *planned*, name what we preserve (Noctalia's widgets), and never claim
affiliation. Prefer short declarative sentences. "Additive, reversible, respectful of
your system" is the throughline.

## What the brand is NOT

- Not a rewrite of Noctalia, and not a plugin — it is a **patch series** over a pinned
  upstream. The brand should read as a *refinement*, not a replacement.
- Not derived from Caelestia's artwork — the visual identity here is original.
