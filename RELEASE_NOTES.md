# CaeliGlow 1.6.1

**CaeliGlow** — a polished, **Noctalia-based** desktop shell for **CachyOS + Hyprland**.
A small, documented **patch series over a pinned Noctalia `v5.3.0`**, rebuilt from source.
It keeps *everything* that makes Noctalia feel like Noctalia and adds a handful of
distinct, **visible-by-default** interactions.

> **Not a rewrite, not a plugin.** Additive by default, reversible in one command, and it
> never overwrites your distro `noctalia` package or touches boot/EFI/partitions.

## What's new in 1.6.1

Updates stop feeling like a shell command and start feeling like part of the shell.

- **In-place updates, no terminal, live progress (patch 0019).** Settings › About →
  **"Install vX now"** now does the whole job without ever opening a terminal window.
  It downloads the new release, rebuilds it, and applies it while a **live progress bar
  and phase label** track the real download / build / install steps, then **restarts the
  running CaeliGlow into the new version** automatically — your settings and state are
  kept. The installer runs fully detached so it survives that restart.
- **Root, politely.** When the updater needs to install build dependencies or run
  `meson install`, it raises a normal **polkit password prompt** (`pkexec`) instead of
  borrowing a terminal; from a terminal it still just uses `sudo`.
- **A new GitHub hero.** The repository header now shows a single authored **eclipse +
  wordmark** image instead of the older animated crescent scene.

## What's new in 1.6.0

The polish release — everything you can see and touch gets more control, and the one thing
that never worked now does.

- **External-monitor brightness just works (patch 0017).** The DDC/CI switch is now
  three-way: leave it unset and CaeliGlow auto-discovers any monitor that has no kernel
  backlight — even in a nested session or hot-docked — keyed by its DRM connector, while
  an explicit on/off still forces behaviour either way. Two new commands: **`brightness-rescan`**
  re-runs discovery and tells you what it found; **`brightness-status`** separates "there is
  no sysfs backlight" from "DDC is off / undiscovered". Verified live on an HP LA2306 over
  DisplayPort. (If you still have an old `~/.config/noctalia`, CaeliGlow warns you once that
  its brightness settings weren't migrated — it never touches the old files.)
- **Ten motion presets + reduced motion (patch 0018).** Panel open/close now offers
  Classic · Soft · Fizzy · Morphy · **Gentle · Glide · Fluid · Snappy · Bounce · Calm**, plus a
  shell-wide **reduce-motion** switch that flattens every bounce and hover embellishment.
- **A real Power-menu section in Settings (patch 0018).** The power pill is now borderless
  and fully tunable — presentation (edge-attached or floating), concavity radius, width,
  overall scale, icon size and gap — and its trigger and opening direction follow whichever
  screen edge it docks to.
- **Launcher sizing (patch 0018).** The launcher is **attached by default** and now has
  independent **length and width** controls plus card-outline polish.
- **One cohesive outlined icon set (patch 0018).** Stray filled glyphs are gone from state
  icons, a broken icon is fixed, and glyph buttons get a subtle centered hover lift that
  stays flat when reduce-motion is on.
- **Fresh logo + About card**, and quick-install now **restarts your live session** after an
  in-place update — no logout.

## What's new in 1.5.1 (still in this release)

- **The About update card does what it says.** When a newer release is found it now
  shows the **what's-new text** from the release notes and a prominent
  **"Install vX now"** button right under it — one click updates the system in place
  (patch 0016). The button is one-shot: it vanishes once the installer launches.
- Coming from 1.4.x? That build predates the install button, so the **one-time** jump
  is the same single command:
  `curl -fsSL https://raw.githubusercontent.com/mockifylab/CaeliGlow/main/scripts/quick-install.sh | bash`
  After that, every future update is the button.

## What's new in 1.5.0 (still in this release)

- **The launcher is docked to the bottom edge.** No more floating panel: it sits flush
  against the bottom of the screen with **concave screen-edge corners** — the curves bend
  *into* the display so the panel and the edge read as one surface (patch 0009).
- **Right-edge panels dock the same way.** The power pill (and any edge-docked panel)
  opens flush to the screen edge with matching concave corners, Caelestia-panel style —
  re-implemented from scratch, no GPL code or assets (patch 0012). **New setting:** the
  pill can dock to the **left or right** edge (`power_edge`).
- **Fizzy & Morphy spring motion.** Opening panels no longer slide linearly — they pop
  with elastic, fluid spring easing and a squash-and-stretch pulse keyed to the reveal
  edge. Four motion styles (Classic · Soft · Fizzy · Morphy) with duration and elasticity
  controls, all config-driven (patch 0011).
- **A real CaeliGlow section in Settings.** Global Settings › **CaeliGlow** (sparkles
  icon, theme-aware like every other section): motion style, duration, elasticity
  (shown only for Fizzy/Morphy), hover-to-open toggle, and the pill's dock edge — every
  CaeliGlow behavior now has a control (patch 0013).
- **Edge-hover flicker fixed.** The bottom/right triggers no longer re-fire while you
  move back into a panel you just opened — open panels stay open, and a short re-trigger
  cooldown stops the open/close stutter (patch 0010).
- **Fully CaeliGlow-branded UI.** The launcher's settings button is now the animated
  CaeliGlow logo (idle animation, hover spin), and every remaining user-facing
  "Noctalia" string — notifications, settings text, window title, icon — reads
  **CaeliGlow** (patch 0014).
- **Updates install in place.** Settings › About → "Install vX now" runs the
  CaeliGlow quick-install in a terminal: the new release replaces the running one,
  keeping your settings and state. One explicit click, no manual commands (patch 0015).

## What's new in 1.4.0 (still in this release)

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

### Edge-docked surfaces & spring motion (patches 0009–0013)
The launcher docks to the bottom edge and the pill docks to a screen edge (left or
right), both with concave screen-edge corners. Panels open with elastic spring easing
and a squash-and-stretch pulse — Classic/Soft/Fizzy/Morphy, all tunable from the new
Settings › CaeliGlow section (`[caeliglow]` in `config.toml`).

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

- Patches 0001–0019 rebuild + relink cleanly against the pinned tree.
- Noctalia `meson test` suite: **155/155 pass, 0 fail** (with the `[caeliglow]` schema
  round-trip probe and the update/install-progress parser tests added).
- Version/update logic unit tests pass (locally and in CI).
- Nested Hyprland smoke test: the shell starts and runs stable with hover-to-open,
  edge actions, the power pill and the About page active; the host session is untouched.
- Full `0001→0019` series applies onto a pristine v5.3.0 via `git am --3way`,
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
