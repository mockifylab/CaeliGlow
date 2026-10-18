# CaeliGlow Roadmap

CaeliGlow stays intentionally small. This roadmap is about **deepening the four shipped
interactions** and **hardening the delivery pipeline**, not about growing a fork.

Legend: ✅ shipped · 🚧 in progress · 📌 planned · 💡 ideas

## 1.0.0 — Foundation (current)

- ✅ Bar hover: Caelestia-style scale "pop", Noctalia widgets preserved (patch 0001).
- ✅ Bottom-edge launcher reveal via HotCorners dwell (patch 0002).
- ✅ Right-edge power → native SessionPanel; original power entries hidden-by-default,
  restorable (patch 0003).
- ✅ Native Settings › CaeliGlow About + live GitHub update check via HttpClient, on the
  tested semver model (patch 0004).
- ✅ Repo pipeline: pinned v5.3.0 submodule, `git am` patch series, build/install/rollback
  scripts, tested logic, docs, brand identity, CI.

## 1.1 — On-device confidence

- 📌 **Live desktop verification** across the matrix: single/multi-monitor, fractional
  scaling, high-DPI. Capture the results into `docs/PATCHES.md`.
- 📌 Per-gesture motion tuning: expose hover/dwell curve + strip geometry so the "feel"
  is configurable, not hardcoded.
- 📌 Edge-trigger configurability: let bottom/right actions be remapped to more of
  Noctalia's native `triggerShellAction` targets (control center, overview, window switcher).

## 1.2 — Updates, safely automated

- 📌 **One-click install of a newer release** — download the asset, verify a checksum, and
  stage via the existing `/usr/local` path. Explicit, reversible, never auto-executed.
- 📌 Channel selection (stable vs pre-release) surfaced in Settings.
- 📌 Optional "what's new" panel sourced from release notes as text.

## 1.3 — Polish & reach

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
