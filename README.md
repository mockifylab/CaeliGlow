<div align="center">

<img src="docs/brand/assets/hero-animated.gif" alt="CaeliGlow — a crescent moon and twinkling stars over a night dreamscape" width="100%" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/brand/assets/wordmark.svg" />
  <img src="docs/brand/assets/wordmark.svg" alt="CaeliGlow" width="380" />
</picture>

**A polished, Noctalia-based desktop shell for CachyOS + Hyprland.**

[![Version](https://img.shields.io/badge/version-1.1.0-8B7CF6?style=flat-square)](https://github.com/mockifylab/CaeliGlow/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-4FE0C4?style=flat-square)](LICENSE)
[![Built on Noctalia v5.3.0](https://img.shields.io/badge/built%20on-Noctalia%20v5.3.0-F5C86B?style=flat-square)](https://github.com/noctalia-dev/noctalia)
[![Platform](https://img.shields.io/badge/CachyOS%20%C2%B7%20Hyprland%20%C2%B7%20Wayland-12172B?style=flat-square)](#supported-environment)
[![CI](https://img.shields.io/badge/CI-build--and--test-7E8AB5?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/mockifylab/CaeliGlow/actions)

*A few careful refinements over the shell you already love — nothing more, nothing lost.*

</div>

---

## Why CaeliGlow

Noctalia is already a beautiful native Wayland shell. **CaeliGlow doesn't replace it.**
It layers a small, fully-documented **patch series** over a *pinned* Noctalia release and
rebuilds it as its own shell — adding the edge-glow interactions and self-updating polish
that make the desktop feel alive, while keeping **every** Noctalia widget, theme, launcher
and setting exactly as upstream intended.

- **Not a rewrite. Not a plugin.** A reviewed patch series on a pinned upstream → trivially auditable, trivially reversible.
- **Additive by default.** Every feature is opt-in via config; with the config absent, CaeliGlow behaves identically to plain Noctalia.
- **Respectful of your machine.** Builds and installs under `/usr/local`, never overwrites the distro `noctalia` package, never touches boot/EFI/partitions.
- **Independently re-implemented.** Inspired by the *feel* of [Caelestia Shell](https://github.com/caelestia-dots/shell)'s edges/hover — with **zero** Caelestia code or assets copied (it's GPL-3.0). CaeliGlow is **MIT** and **unaffiliated**.

*Want the 30-second design story? Read the [project overview → docs/OVERVIEW.md](docs/OVERVIEW.md).*

## What it changes

| Area | What you get | Verification |
|------|--------------|--------------|
| **Bar hover** | A Caelestia-style scale "pop" as you hover bar widgets — Noctalia's contents, layout, accordion expansion and fill highlight all preserved. | ✅ Compiled + relinked |
| **Bottom edge** | An optional wide, centered bottom-edge strip; hover + dwell reveals the **existing** Noctalia launcher. | ✅ Compiled + config-tested |
| **Right edge** | An optional thin, full-height right-edge strip whose `power` action opens Noctalia's own **SessionPanel** (labeled Shut Down / Restart / Suspend / Log Out + confirm countdown). Duplicate original power entries are hidden by default (restorable). | ✅ Compiled + `meson test` 153/153 |
| **Settings › About** | A native "CaeliGlow" About section headed by the **animated crescent-moon mark** (twinkling stars, rendered in-shell from a bundled GIF), with version, Noctalia base, MIT attribution and a live **Check for updates** against GitHub releases. | ✅ Compiled + `meson test` |

## What it deliberately leaves unchanged

- Noctalia's bar, widgets, their appearance and functionality.
- The launcher UI (the same launcher is revealed by the edge trigger).
- The theme / palette system and all general settings.
- Ordinary Noctalia behavior everywhere not listed above.

---

## Quick start

> Requires **CachyOS / Arch** and **Hyprland (Wayland)**. All installs are additive
> (`pacman -S --needed`) — no removals, no boot/EFI/partition changes.

```sh
# 1) Clone with the pinned Noctalia submodule
git clone --recursive https://github.com/mockifylab/CaeliGlow.git
cd CaeliGlow

# 2) Install build dependencies (additive only)
sudo ./scripts/install-deps.sh

# 3) Apply the patch series + build
./scripts/build.sh release /usr/local

# 4) Install under /usr/local (does NOT overwrite /usr/bin/noctalia)
sudo ./scripts/install.sh release /usr/local
```

Point your Hyprland autostart at `/usr/local/bin/noctalia`. Because the packaged
`/usr/bin/noctalia` is untouched, you can always fall back. Restore ordinary Noctalia
with `./scripts/rollback.sh release /usr/local`.

Full walkthrough: **[docs/BUILDING.md](docs/BUILDING.md)**.

## Enable the new behaviors

CaeliGlow features are opt-in. Merge these **additive** blocks into your existing
Noctalia TOML config (`noctalia --print-config-path`), keeping the rest of your config
as-is. A complete, validated sample is in [`config/caeliglow.example.toml`](config/caeliglow.example.toml):

```toml
[hot_corners]
enabled = true
delay_ms = 120          # hold time before the edge fires; 0 = fire on enter

[hot_corners.bottom_edge]
action = "launcher"     # 0002 — bottom-edge reveal

[hot_corners.right_edge]
action = "power"        # 0003 — right-edge → Noctalia SessionPanel
```

Update flow and rollback: **[docs/UPDATING.md](docs/UPDATING.md)**.

## Architecture

Modern **Noctalia (v5.x) is a native C++ Wayland shell** — its own scene graph, GLES
renderer, Pango/Cairo text and a poll-based main loop. It is **not** a Quickshell/QML
app. CaeliGlow therefore patches C++ source and rebuilds with Noctalia's own
`meson` + `just` + `ninja` toolchain.

```
patches/  --git am-->  upstream/noctalia (submodule @ v5.3.0)  --meson/ninja-->  noctalia
```

The submodule stays pinned at **`v5.3.0`**; the patch files under `patches/` are the
*only* CaeliGlow changes, so rebasing onto a newer Noctalia is a per-patch `git am` retry.
Per-patch rationale and safety notes: **[docs/PATCHES.md](docs/PATCHES.md)**.

## Verification & testing

Honesty about what "done" means here:

- **Reproducible build:** unmodified Noctalia v5.3.0 configures, builds and links a
  working `noctalia`; CaeliGlow patches 0001–0004 rebuild and relink with no errors.
- **Regression suite:** full `meson test` → **153/153 OK, 0 fail** (includes config
  schema round-trip, CLI validate, override mutation — which exercise the new
  `hot_corners` fields).
- **Logic unit tests:** version-comparison + update state machine compile and pass
  standalone (and in CI).
- **Series integrity:** `0001→0002→0003→0004` apply cleanly onto a pristine v5.3.0 via
  `git am --3way`.
- **Not yet done in this environment:** a live-desktop smoke test on real hardware was
  intentionally not run (a second shell over an active Hyprland session was avoided).
  Please run the on-device checklist in [docs/PATCHES.md](docs/PATCHES.md) on your setup,
  and re-check multi-monitor / fractional-scaling edges on your exact displays.

## Roadmap

Planned next: live per-gesture motion tuning, multi-monitor edge hardening, and an
optional auto-update installer wired to the same update model. See
**[docs/ROADMAP.md](docs/ROADMAP.md)**.

## Development

```sh
./scripts/apply-patches.sh                 # patch the pinned tree
# edit upstream/noctalia/ ...
(cd upstream/noctalia && just configure debug && just build debug && just test debug)
./scripts/reset-patches.sh                 # back to clean Noctalia
```

Contributions welcome — see **[CONTRIBUTING.md](CONTRIBUTING.md)**. Report issues via the
GitHub tracker; for security matters see **[SECURITY.md](SECURITY.md)**.

## Repo layout

```
CaeliGlow/
├── patches/            # the ONLY CaeliGlow changes (git-am series) + patches/series
├── upstream/noctalia/  # Noctalia submodule, pinned to v5.3.0
├── src/caeliglow/      # standalone-tested update/version logic (headers)
├── tests/              # logic unit tests (run in CI + locally)
├── scripts/            # build / install / apply / reset / rollback / install-deps
├── config/             # caeliglow.example.toml (validated)
├── docs/               # BUILDING · PATCHES · UPDATING · ATTRIBUTION · ROADMAP · brand/
└── .github/workflows/  # build-and-test CI
```

## Licensing & attribution

- **CaeliGlow** original code, docs and brand assets: **MIT** — © 2026 Aasif / mockifylab.
- Built on **Noctalia** — **MIT**, © 2026 noctalia-dev. Upstream copyright/license is
  preserved for all Noctalia-derived sources.
- **Caelestia Shell** is **GPL-3.0**. CaeliGlow copies **no** Caelestia code or assets;
  "Caelestia-style" means independently re-implemented behavior only.
- There is **no affiliation with, sponsorship by, or endorsement from** Noctalia or Caelestia.

Full text: **[docs/ATTRIBUTION.md](docs/ATTRIBUTION.md)** · **[LICENSE](LICENSE)**.

---

<div align="center">

**Version 1.1.0** · Developer **Aasif** · [github.com/mockifylab/CaeliGlow](https://github.com/mockifylab/CaeliGlow)

*Made with care for the CachyOS + Hyprland community.*

</div>
