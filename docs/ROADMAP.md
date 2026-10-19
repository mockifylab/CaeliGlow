# CaeliGlow Roadmap

CaeliGlow stays intentionally small. This roadmap is about **deepening the shipped
interactions** and **hardening the delivery pipeline**, not about growing a fork.

Legend: ✅ shipped · 🚧 in progress · 📌 planned · 💡 ideas

## 1.0.0 — Foundation ✅ shipped

- ✅ Bar hover: Caelestia-style scale "pop", Noctalia widgets preserved (patch 0001).
- ✅ Bottom-edge launcher reveal via HotCorners dwell (patch 0002).
- ✅ Right-edge power → native SessionPanel; original power entries hidden-by-default,
  restorable (patch 0003).
- ✅ Native Settings › CaeliGlow About + live GitHub update check via HttpClient, on the
  tested semver model (patch 0004).
- ✅ Repo pipeline: pinned v5.3.0 submodule, `git am` patch series, build/install/rollback
  scripts, tested logic, docs, brand identity, CI.

## 1.1.0 — Animated brand identity

- ✅ Original crescent-and-sparkle mark, redrawn as **animated** assets: static
  `logo.svg`/`logo.png`, `logo-animated.gif`/`.svg`, wordmark, and a cinematic animated
  hero + social preview, all generated from `scripts/gen_brand_assets.py` /
  `scripts/gen_hero.py`.
- ✅ **Animated logo rendered in-shell** in Settings › About — bundled GIF decoded to GPU
  textures and cycled by a self-re-arming timer (Noctalia's sticker mechanism), with clean
  teardown and a static fallback (extends patch 0004).
- ✅ Version read from the root `VERSION` file at configure time (single source of truth).

## 1.3.0 — Interactions you can actually see ✅ shipped

The pivot: the signature features are now **on by default** and genuinely visible.

- ✅ **Bar hover opens the widget's panel** (patch 0005) — hovering any widget reveals its
  panel with Noctalia's native animation and closes it on leave; generic (built-in, user
  and plugin widgets), with a dwell guard and hover-ownership conflict arbitration.
- ✅ **Right-edge CaeliGlow power pill** (patch 0006) — new `caeliglow_power` action, a
  floating animated session pill with confirm countdowns; the `AnimatedImage` idle→hover
  GIF driver becomes shared infrastructure.
- ✅ **Edges on by default** (patch 0006) — `hot_corners.enabled=true`, bottom→launcher,
  right→power pill; no config merge needed to see them.
- ✅ **Animated launcher avatar + branded About page** (patch 0007) — the crescent mark in
  the launcher; a full Settings › About page (hero, version, live update check, feature
  summary, project links, credits).
- ✅ Verified: debug rebuild + `meson test` 153/153 + nested-Hyprland smoke test.

## 1.4.0 — CaeliGlow's own namespace (current) ✅ shipped

- ✅ **Own config/state/data directories** (patch 0008): `~/.config/caeliglow/`,
  `~/.local/state/caeliglow/`, `~/.local/share/caeliglow/` — first run starts on
  CaeliGlow's compiled-in defaults; the user's Noctalia directories are never read,
  migrated or written.
- ✅ **Own runtime sockets** (`caeliglow-*.sock/.lock`, dmenu socket): CaeliGlow can run
  side-by-side with a live stock Noctalia without IPC cross-talk or lock contention.
- ✅ Own log (`$XDG_CACHE_HOME/caeliglow/caeliglow.log`) and calendar cache; new
  `CAELIGLOW_*_HOME` env overrides; `config replay` follows the new layout.
- ✅ Verified: debug rebuild + `meson test` 153/153 + full `0001→0008` series applies
  onto pristine v5.3.0 (byte-identical reconstruction).

## 1.5 — On-device confidence

- 📌 **Live desktop verification** across the matrix: single/multi-monitor, fractional
  scaling, high-DPI. Capture the results into `docs/PATCHES.md`.
- 📌 Per-gesture motion tuning: expose hover/dwell curve + strip geometry so the "feel"
  is configurable, not hardcoded.
- 📌 Edge-trigger configurability: let bottom/right actions be remapped to more of
  Noctalia's native `triggerShellAction` targets (control center, overview, window switcher).

## 1.6 — Updates, safely automated

- 📌 **One-click install of a newer release** — download the asset, verify a checksum, and
  stage via the existing `/usr/local` path. Explicit, reversible, never auto-executed.
- 📌 Channel selection (stable vs pre-release) surfaced in Settings.
- 📌 Optional "what's new" panel sourced from release notes as text.

## 1.7 — Polish & reach

- 💡 Theme-aware accent for the glow (tie the brand palette to Noctalia's active palette).
- 💡 Haptics-adjacent micro-feedback (respect reduced-motion setting).
- 💡 Packaging convenience: `pkgbuild/` recipe for a native Arch/CachyOS package that
  still installs to its own prefix and never clobbers upstream `noctalia`.

## Working on the upstream relationship

- 📌 Rebase the patch series onto each new Noctalia minor promptly; drop any patch that
  upstream has since implemented natively.
- 💡 Where a CaeliGlow behavior is generically useful, propose it upstream to Noctalia
  and remove the local patch once accepted.

## Out of scope (by design)

- Rewriting Noctalia's widgets, theme, or launcher.
- Copying Caelestia code/assets (license-incompatible).
- Anything that removes packages, touches boot/EFI/partitions, or overwrites the distro
  `noctalia` binary.

---

Priorities are driven by real desktop use. If you want a line item to move up, open an
issue with your setup and use case. See [CONTRIBUTING.md](../CONTRIBUTING.md).
