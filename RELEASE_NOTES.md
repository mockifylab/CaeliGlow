# CaeliGlow 1.0.0

The first release of **CaeliGlow** — a polished, **Noctalia-based** desktop shell for
**CachyOS + Hyprland**. CaeliGlow is a small, documented **patch series over a pinned
Noctalia `v5.3.0`**, rebuilt from source. It keeps *everything* that makes Noctalia feel
like Noctalia and adds a few specific, opt-in interactions.

> **Not a rewrite, not a plugin.** Additive by default, reversible in one command, and it
> never overwrites your distro `noctalia` package or touches boot/EFI/partitions.

## What's new

### Bar hover (patch 0001)
A Caelestia-style scale "pop" as you hover bar widgets. Noctalia's widget contents,
layout, accordion expansion and fill highlight are preserved.

### Bottom-edge launcher reveal (patch 0002)
An optional wide, centered bottom-edge strip. Hover + dwell reveals the **existing**
Noctalia launcher, built on Noctalia's own HotCorners dwell engine.

### Right-edge power controls (patch 0003)
An optional thin, full-height right-edge strip. Its new `power` action opens Noctalia's
native **SessionPanel** — labeled Shut Down / Restart / Suspend / Log Out with the
built-in confirm countdown. The duplicate original power entries (Control Center header
and Launcher toolbar) are hidden by default and are restorable in config.

### Settings › About + live update check (patch 0004)
A native "CaeliGlow" Settings section showing the CaeliGlow version, the Noctalia base
version and MIT attribution, plus a **live "Check for updates"** button. It queries the
GitHub releases endpoint through Noctalia's own async HTTP client and reports the result
via a fully unit-tested semver state machine. Honors `shell.offlineMode`; release notes
are shown as plain text and never executed.

## Configuration

All features are opt-in. Merge the additive blocks from
[`config/caeliglow.example.toml`](config/caeliglow.example.toml) into your existing
Noctalia config (`noctalia --print-config-path`) — do not replace the whole file.

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

- Patches 0001–0004 rebuild + relink cleanly against the pinned tree.
- Noctalia `meson test` suite: **153/153 pass, 0 fail**.
- Version/update logic unit tests pass (locally and in CI).
- Full `0001→0004` series applies onto a pristine v5.3.0 via `git am --3way`.
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
