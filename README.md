<div align="center">

<img src="docs/brand/assets/hero-animated.gif" alt="CaeliGlow — a crescent moon and twinkling stars over a night dreamscape" width="100%" />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/brand/assets/wordmark.svg" />
  <img src="docs/brand/assets/wordmark.svg" alt="CaeliGlow" width="380" />
</picture>

**A polished, Noctalia-based desktop shell for CachyOS + Hyprland.**

[![Version](https://img.shields.io/badge/version-1.4.0-8B7CF6?style=flat-square)](https://github.com/mockifylab/CaeliGlow/releases)
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
- **Visible by default.** The signature interactions are on out of the box via compiled-in defaults; every one is additive and overridable in config.
- **Its own identity, its own files.** Since 1.4.0 CaeliGlow keeps config, state and runtime sockets in its **own `caeliglow` namespace** — it never reads or writes your Noctalia directories, and the two shells can run side by side.
- **Respectful of your machine.** Builds and installs under `/usr/local`, never overwrites the distro `noctalia` package, never touches boot/EFI/partitions.
- **Independently re-implemented.** Inspired by the *feel* of [Caelestia Shell](https://github.com/caelestia-dots/shell)'s edges/hover — with **zero** Caelestia code or assets copied (it's GPL-3.0). CaeliGlow is **MIT** and **unaffiliated**.

*Want the 30-second design story? Read the [project overview → docs/OVERVIEW.md](docs/OVERVIEW.md).*

## What it changes

| Area | What you get | Verification |
|------|--------------|--------------|
| **Bar hover** | Hovering **any** bar widget opens *that widget's* panel with Noctalia's native reveal animation, and it closes when you leave. Driven from each widget's own left-click gesture, so built-in, user and plugin widgets all follow the same rule (per-item widgets stay inert). The old icon-zoom is gone. | ✅ Compiled + `meson test` 153/153 + nested smoke |
| **Bottom edge** | A wide, centered bottom-edge strip (on by default); hover + dwell reveals the **existing** Noctalia launcher. | ✅ Compiled + config-tested |
| **Right edge** | A full-height right-edge strip (on by default) whose `caeliglow_power` action opens the floating, animated **CaeliGlow power pill** (Logout · Power · animated logo · Lock · Restart + confirm countdown). The native SessionPanel `power` action still works if you set it. Duplicate original power entries are hidden by default (restorable). | ✅ Compiled + `meson test` 153/153 |
| **Settings › About** | A full **branded** native "CaeliGlow" page headed by the **animated crescent-moon mark**: hero + version, a live **Check for updates**, a "what CaeliGlow adds" summary, project links and attribution. | ✅ Compiled + `meson test` 153/153 |
| **Launcher** | Search moves to the top and, with no personal avatar set, the launcher shows the **animated** CaeliGlow mark as its avatar (a real avatar takes over cleanly). | ✅ Compiled + `meson test` 153/153 |
| **Own namespace** | Since 1.4.0: config in `~/.config/caeliglow/`, state in `~/.local/state/caeliglow/`, sockets/lock as `caeliglow-*`, log in `~/.cache/caeliglow/`. First run starts on CaeliGlow's own defaults; your `~/.config/noctalia` is never read or touched. | ✅ Compiled + `meson test` 153/153 |

## What it deliberately leaves unchanged

- Noctalia's bar widget contents and their core functionality (hover just *opens* the
  panel a click already opened — no widget is replaced).
- The launcher's app-provider behavior and results (only its avatar and search position change).
- The theme / palette system and all general settings.
- Ordinary Noctalia behavior everywhere not listed above.

---

## Quick start

> Requires **CachyOS / Arch** and **Hyprland (Wayland)**. All installs are additive
> (`pacman -S --needed`) — no removals, no boot/EFI/partition changes.

**One command** — the `pacman -S`-style experience, straight from this repo:

```sh
curl -fsSL https://raw.githubusercontent.com/mockifylab/CaeliGlow/main/scripts/quick-install.sh | bash
```

It fetches the pinned Noctalia submodule, applies the whole CaeliGlow patch series,
builds a **release**, and installs it as `/usr/local/bin/caeliglow` — under its **own
name**, so it never shadows or overwrites your distro `noctalia`. A **CaeliGlow session
entry appears in your greeter**: pick it to boot the CaeliGlow shell, pick any other
entry to stay on distro Noctalia (one Lua autostart branch handles both):

```lua
if os.getenv("CAELIGLOW_SESSION") == "1" then hl.exec_cmd("/usr/local/bin/caeliglow")
else hl.exec_cmd("/usr/bin/noctalia") end
```

Undo it any time with:

```sh
curl -fsSL https://raw.githubusercontent.com/mockifylab/CaeliGlow/main/scripts/uninstall.sh | bash
```

**Pacman-native path** — install and remove like any Arch package (`sudo pacman -R caeliglow`):

```sh
cd pkgbuild && makepkg -si      # from a clone of this repo
paru -S caeliglow               # once caeliglow is published to the AUR (pkgbuild/ is AUR-ready)
```

**Manual step-by-step** (what the one-liner does under the hood):

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

Point your Hyprland autostart at `/usr/local/bin/caeliglow` (or `/usr/local/bin/noctalia`
after a manual `scripts/install.sh`, which keeps the upstream binary name). Because the
packaged `/usr/bin/noctalia` is untouched, you can always fall back. Restore ordinary
Noctalia with `./scripts/uninstall.sh` (quick-install) or `./scripts/rollback.sh release /usr/local`.

Full walkthrough: **[docs/BUILDING.md](docs/BUILDING.md)**.

## The new behaviors (on by default)

CaeliGlow's signature interactions ship **enabled by compiled-in defaults** — a stock build
shows them with no config. CaeliGlow keeps its configuration in **its own namespace**
(`~/.config/caeliglow/config.toml` — print with `noctalia --print-config-path`); everything
below is **optional** tuning, merged into that file and keeping the rest as-is. Your
`~/.config/noctalia` is never read or written. A complete, validated sample is in
[`config/caeliglow.example.toml`](config/caeliglow.example.toml):

```toml
[hot_corners]
enabled = true          # default: true
delay_ms = 120          # hold time before the edge fires; 0 = fire on enter

[hot_corners.bottom_edge]
action = "launcher"         # 0002 — bottom-edge reveal (default)

[hot_corners.right_edge]
action = "caeliglow_power"  # 0006 — animated power pill (default); "power" = SessionPanel
```

Bar hover-to-open-panel needs no config — it reads each widget's own left-click gesture.
See [docs/PATCHES.md](docs/PATCHES.md) for how it stays out of the way of click/edge panels.

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
  working `noctalia`; CaeliGlow patches 0001–0008 rebuild and relink with no errors.
- **Regression suite:** full `meson test` → **153/153 OK, 0 fail** (includes config
  schema round-trip, CLI validate, override mutation — which exercise the new
  `hot_corners` fields).
- **Logic unit tests:** version-comparison + update state machine compile and pass
  standalone (and in CI).
- **Series integrity:** `0001→…→0008` apply cleanly onto a pristine v5.3.0 via
  `git am --3way`, reconstructing the tree byte-for-byte.
- **Nested smoke test:** the patched shell starts and runs stable inside a nested Hyprland
  window with hover-to-open, edges, the power pill and the About page active — the host
  session is untouched.
- **Not yet done in this environment:** a full live-desktop checklist on real hardware
  (multi-monitor / fractional-scaling edges) is still worth running on your exact setup —
  see [docs/PATCHES.md](docs/PATCHES.md).

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

**Version 1.4.0** · Developer **Aasif** · [github.com/mockifylab/CaeliGlow](https://github.com/mockifylab/CaeliGlow)

*Made with care for the CachyOS + Hyprland community.*

</div>
