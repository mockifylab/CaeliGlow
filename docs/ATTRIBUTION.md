# Credits, licensing and attribution

## CaeliGlow
- **License:** MIT — Copyright © 2026 Aasif (mockifylab). See `LICENSE`.
- **Developer:** Aasif · **Repo:** https://github.com/mockifylab/CaeliGlow
- CaeliGlow is an **independent customization built on Noctalia**. It is **not**
  affiliated with, sponsored by, or endorsed by Noctalia, Caelestia, or CachyOS.

## Noctalia (upstream base)
- Project: https://github.com/noctalia-dev/noctalia
- **License: MIT** — Copyright © 2026 noctalia-dev.
- CaeliGlow pins Noctalia **v5.3.0** (`a33122c4`) and applies a small patch series.
  Noctalia's MIT license and copyright notices are **preserved** for all
  Noctalia-derived sources. CaeliGlow's own additions are MIT as well, so the two
  licenses are compatible.

## Caelestia Shell (behavioral reference only)
- Project: https://github.com/caelestia-dots/shell
- **License: GNU GPL-3.0** (copyleft).
- **CaeliGlow copies no Caelestia code, assets, names, or styling.** Every
  "Caelestia-style" behavior in CaeliGlow is an **independent re-implementation** of
  observed interaction (timing, easing, reveal/conceal) written against Noctalia's
  architecture.

### Why we do not copy Caelestia code
GPL-3.0 is a strong-copyleft license. Derivative works that incorporate GPL-3.0 code
must be distributed under GPL-3.0, which is incompatible with shipping CaeliGlow as
an MIT, Noctalia-based project. Re-implementing behavior from observation avoids
that conflict: **interfaces, ideas, and observed UX behavior are not copyrightable**,
whereas code and assets are. If a future release ever needs to incorporate GPL
material, the project's license would have to change accordingly — this would be
decided and documented explicitly before any such inclusion.

## Third-party components
CaeliGlow inherits Noctalia's vendored dependencies (Luau, Wuffs, fzy, Material
Color Utilities) and system libraries under their own licenses; Noctalia's
`CREDITS.md` and license files remain authoritative for those and are shipped with
the source tree.
