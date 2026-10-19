# CaeliGlow 1.4.0

**CaeliGlow** — a polished, **Noctalia-based** desktop shell for **CachyOS + Hyprland**.
A small, documented **patch series over a pinned Noctalia `v5.3.0`**, rebuilt from source.
It keeps *everything* that makes Noctalia feel like Noctalia and adds a handful of
distinct, **visible-by-default** interactions.

> **Not a rewrite, not a plugin.** Additive by default, reversible in one command, and it
> never overwrites your distro `noctalia` package or touches boot/EFI/partitions.

## What's new in 1.4.0

- **CaeliGlow now has its own configuration and customization — by default.** It no
  longer reads or writes Noctalia's `~/.config/noctalia` / `~/.local/state/noctalia`
  directories. Everything lives in CaeliGlow's own namespace:
  `~/.config/caeliglow/`, `~/.local/state/caeliglow/`, `~/.local/share/caeliglow/`.
  A first run starts on CaeliGlow's own compiled-in defaults — hover-to-open panels,
  power pill, launcher avatar — so out of the box it *is* CaeliGlow, not a relabeled
  Noctalia session. Your stock Noctalia config is never read, migrated or touched.
- **Own runtime sockets** (`caeliglow-*.sock/.lock`): CaeliGlow can run side-by-side
  with a live Noctalia without the two shells talking to (or locking out) each other.
- **Own log & caches**: `~/.cache/caeliglow/caeliglow.log`, calendar cache under
  `~/.cache/caeliglow/`. New `CAELIGLOW_CONFIG_HOME` / `CAELIGLOW_STATE_HOME` /
  `CAELIGLOW_DATA_HOME` env overrides (patch 0008).

## What's new in 1.3.0 (still in this release)

- **Hover a bar widget → its panel opens.** This is the headline change. Instead of the
  old icon "pop", hovering *any* widget now reveals that widget's own panel with Noctalia's
  native attached slide/grow animation and closes it when you leave (with a short grace
  window so you can move into the panel). It's driven from each widget's existing
  left-click gesture, so it works the same for built-in, user-added and plugin widgets —
  no per-widget wiring — and it deliberately stays out of the way of click- and
  edge-opened panels.
- **The signature edges are on out of the box.** No config merge needed: hovering the
  **bottom edge** reveals the launcher and hovering the **right edge** opens the CaeliGlow
  **power pill** (Logout · Power · animated logo · Lock · Restart, with confirm countdowns).
- **A real Settings › About page.** Noctalia's global Settings › About is now a full
  branded page: an animated crescent-moon hero with the CaeliGlow name, tagline and
  version, a live **Check for updates** card, a "What CaeliGlow adds" summary, project
  links (repository / releases / report-an-issue) and a Credits & license block.
- **Animated launcher avatar.** With no personal avatar set, the launcher shows the
  CaeliGlow mark, animating idle→hover; set your own and it takes over cleanly.

## The CaeliGlow feature set

### Bar hover → open the widget's panel (patch 0005)
Hover any bar widget and its panel glides open (Noctalia's own reveal animation); leave
and it closes after a grace period. Config-driven, so every widget type — including user
and plugin widgets — follows the same rule. The 1.0/1.1 icon-zoom (patch 0001) is retired.

### Bottom edge → launcher (patch 0002, on by default)
A wide, centered bottom-edge strip. Hover + dwell reveals the **existing** Noctalia
launcher via Noctalia's own HotCorners dwell engine.

### Right edge → CaeliGlow power pill (patches 0003 + 0006, on by default)
A full-height right-edge trigger. The new `caeliglow_power` action opens a floating,
animated session pill; the older `power` action (Noctalia's native SessionPanel) still
works if you set it explicitly. Original duplicate power entries are hidden by default
and are restorable in config.

### Animated launcher + branded About (patches 0004 + 0007)
Settings › About is headed by the **animated crescent-moon mark** (twinkling, rendered
in-shell from a bundled GIF) and now presents a full branded page with version, base
version, a **live "Check for updates"** button (through Noctalia's async HTTP client +
a fully unit-tested semver state machine), project links and attribution. The launcher
carries the same animated mark as its avatar.

### Own config & runtime namespace (patch 0008)
All persistent state and runtime IPC live under `caeliglow` paths, isolated from stock
Noctalia in both directions — safe to install, safe to run beside, safe to remove.

## Configuration

The signature interactions are enabled by **compiled-in defaults** — a stock CaeliGlow
build shows them with no config changes. CaeliGlow keeps its configuration in **its own
namespace**: `~/.config/caeliglow/config.toml` (path check:
`noctalia --print-config-path` — since 1.4.0 this resolves under `caeliglow/`). Tune it
with the additive blocks in
[`config/caeliglow.example.toml`](config/caeliglow.example.toml) — do not replace the
whole file, and note your old `~/.config/noctalia/` stays untouched and unused.

## Build & install

```sh
git clone --recursive https://github.com/mockifylab/CaeliGlow.git
cd CaeliGlow
sudo ./scripts/install-deps.sh          # additive only, no removals
./scripts/build.sh release /usr/local
sudo ./scripts/install.sh release /usr/local
```

See [docs/BUILDING.md](docs/BUILDING.md) and [docs/UPDATING.md](docs/UPDATING.md).

## Verification

- Patches 0001–0008 rebuild + relink cleanly against the pinned tree.
- Noctalia `meson test` suite: **153/153 pass, 0 fail**.
- Version/update logic unit tests pass (locally and in CI).
- Nested Hyprland smoke test: the shell starts and runs stable with hover-to-open,
  edge actions, the power pill and the About page active; the host session is untouched.
- Full `0001→0008` series applies onto a pristine v5.3.0 via `git am --3way`,
  reconstructing the tree byte-for-byte.
- Example config validates against the patched binary.
- **On-device smoke test** (live Hyprland, multi-monitor/fractional scaling) is still to
  be run on your hardware — see the checklist in [docs/PATCHES.md](docs/PATCHES.md).

## License & attribution

CaeliGlow original code, docs and brand assets are **MIT** (© 2026 Aasif / mockifylab),
built on **Noctalia** (MIT, © 2026 noctalia-dev). CaeliGlow copies **no** Caelestia
(GPL-3.0) code or assets — "Caelestia-style" means independently re-implemented behavior
only. No affiliation with or endorsement by Noctalia or Caelestia. Details:
[docs/ATTRIBUTION.md](docs/ATTRIBUTION.md).

---

**Full changelog:** [CHANGELOG.md](CHANGELOG.md) · **Docs:** [docs/](docs/)
