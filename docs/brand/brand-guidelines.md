# CaeliGlow Brand Guidelines

CaeliGlow is a calm, premium, night-sky aesthetic: **a soft aurora glow over a deep
indigo night**. It signals "Noctalia, but warmer and more alive" — restrained motion,
luminous accents, generous negative space. Never loud, never busy.

## Name

- Written as one word: **CaeliGlow** (capital **C**, capital **G**).
- "Caeli" (Latin, *of the sky*) + "Glow". Never "Caeli Glow", "Caeliglow", or "CG".
- Tagline (when needed): *A polished Noctalia desktop shell for CachyOS + Hyprland.*

## Logo

- **Primary mark** — `assets/logo.svg`: the aurora "C" arc with a single star on a
  rounded night plate. Use when a square icon is needed (app icon, favicon, avatars).
- **Wordmark lockup** — `assets/wordmark.svg`: mark + "CaeliGlow" + eyebrow. Use for
  headers, README hero, titles.
- **Hero / social preview** — `assets/social-preview.png` (1280×731, <1 MB): the wide
  banner for the README and GitHub "Social preview" setting.

Rules:

- Keep clear space equal to the height of the arc around the mark.
- Minimum on-screen size for the mark: **32 px**. Below that, drop the plate border.
- Never recolor the arc gradients, stretch, rotate, add drop shadows, or place the
  wordmark on a busy photo without a dark scrim.
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

The three aurora colors form the signature gradient **Teal → Violet → Amber** (used
left-to-right / top-to-bottom). Always use all three together in the mark; a single
one may be used for a small accent.

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
