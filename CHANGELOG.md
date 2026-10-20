# Changelog

All notable changes to CaeliGlow are documented here. The format follows
Keep-a-Changelog; CaeliGlow uses Semantic Versioning. CaeliGlow's version is read
from the single canonical `VERSION` file.

## [Unreleased]

_(nothing pending)_

## [1.6.0] - 2026-10-20

CaeliGlow 1.6.0 is the polish release: the launcher and power menu gain real sizing and
presentation controls, panel motion grows to ten fluid presets with a shell-wide
reduced-motion switch, the icon set settles into one cohesive outlined house style, and
external-monitor brightness finally works out of the box. Delivered as patches
**0017** (brightness) and **0018** (UI layer) over the same pinned Noctalia v5.3.0.

### Added
- **External-monitor brightness, out of the box (patch 0017).** `enable_ddcutil` is now
  **tri-state** (unset = auto). In auto mode DDC/CI is authoritative: connectors with no
  kernel sysfs backlight are discovered from `ddcutil` even when the compositor does not
  expose them (nested sessions, hot-docked externals); an explicit `true`/`false` keeps
  the old behaviour both ways. New IPC commands **`brightness-rescan`** (re-run discovery
  and report targets) and **`brightness-status`** (separate "no sysfs backlight" from
  "DDC disabled / undiscovered"). A startup warn-once fires when a legacy
  `~/.config/noctalia` exists but the CaeliGlow namespace has no `[brightness]` config —
  the old namespace is never read or rewritten. Verified on an HP LA2306 on DP-5
  (`brightness-set DP-5 55` confirmed via `ddcutil getvcp 0x10`, restored to 68).
- **Ten motion presets + reduced motion (patch 0018).** `motion` now spans
  classic · soft · fizzy · morphy · gentle · glide · fluid · snappy · bounce · calm, plus a
  shell-wide `reduce_motion` switch; all in Settings › CaeliGlow.
- **Power-menu Settings subsection (patch 0018).** Presentation (edge-attached /
  floating), concavity radius, pill width, overall scale, icon size and gap.
- **Launcher length control (patch 0018).** `shell.launcher.height` alongside `width`,
  plus a floating/attached setting (attached is now the default).

### Changed
- **Power pill is borderless** and its trigger / opening direction follow the pill's
  left/right `power_edge`.
- **Cohesive outlined icon house style (patch 0018).** Stray filled glyphs dropped from
  state aliases, the unresolved `file-lock` glyph fixed, and glyph buttons get a small
  centered hover lift that snaps flat under reduced motion.
- **New attached logo assets** wired into the panel and a polished About card.
- `scripts/quick-install.sh` restarts the running shell in place after installing, so
  "Install now" updates the *live* session — no logout needed.

### Verified in this release
- Full debug rebuild + link clean; `meson test` **154/154 pass, 0 fail** (new
  `glyph_registry` guard + brightness coverage; `config_schema_roundtrip` exercises every
  new setting).
- Series `0001→0018` applies cleanly onto a pristine v5.3.0 via `git am --3way`,
  reconstructing the tree byte-for-byte.

## [1.5.1] - 2026-10-19

The update card in Settings → About now tells you *what* you are getting and gives
you the button to get it.

### Changed
- **About update card (patch 0016).** When a newer release is found, the card shows
  the “what’s new” text from the release notes (rendered strictly as plain text —
  never parsed or executed) with a prominent **“Install vX now”** button beneath it.
  The button is one-shot: it disappears once the installer terminal is launched.
- **Submodule pointer back to the pristine pin `a33122c42` (v5.3.0).** Releases must
  record the *pinned upstream* commit — fresh clones get Noctalia from upstream and
  apply `patches/series` (0001→0016) themselves, exactly as docs/PATCHES.md promises.
  Development continues on the local `caeliglow-dev` branch.
- `scripts/quick-install.sh` now documents **CaeliGlow-only** Hyprland Lua autostart
  (the dual-session branch is optional, not the default advice).

### Verified in this release
- Full debug rebuild + link clean; `meson test` **153/153 pass, 0 fail**.
- Series `0001→0016` applies cleanly onto a pristine v5.3.0 via `git am --3way` and
  the resulting tree is byte-identical to the development branch.

## [1.5.0] - 2026-10-19

CaeliGlow docks to the screen. The launcher and side panels now join the screen
edges with concave corners (the Caelestia-style fitted look), panel opening gets a
spring physics you can feel — and all of it is controlled from a dedicated CaeliGlow
section in Settings.

### Added
- **Bottom-docked launcher with concave screen-edge corners (patch 0009).** The
  compiled default is now the signature layout: bottom bar, launcher attached
  edge-to-edge; the corners where it meets the screen edges curve inward and the
  panel visually melts into the edge.
- **Right-edge docking for panels (patch 0012).** The session pill docks flush to
  the right screen edge with the same concave treatment (`Panel::dockToScreenEdge()`).
- **`[caeliglow]` config section (patch 0011).** `motion` = classic / soft / fizzy /
  morphy, `duration_ms` (80–1500), `elasticity` (0–1), `hover_open`, `power_edge`
  (left / right) — all validated through the schema and all exposed in Settings.
- **Fizzy & morphy spring animations (patches 0011–0012).** Opens use an elastic
  damped-sine easing plus a squash-and-stretch pulse (stronger for morphy); closes
  reuse 60% of the duration. No more linear slide — and every parameter is configurable.
- **CaeliGlow section in Settings (patch 0013).** Motion picker, duration/elasticity
  sliders, hover-to-open toggle and session-pill edge selector, themed and styled
  exactly like the global settings UI.
- **Launcher settings button is now the animated CaeliGlow logo (patch 0014).**
- **Settings → About “Install vX now” (patch 0015).** An available update installs
  in place: the quick-install one-liner runs in a terminal window and replaces the
  running version; config and state are untouched.

### Fixed
- **Bottom/right edge hover flicker (patch 0010).** Hot-corner triggers are now
  open-only with a 400 ms cooldown, so a panel covering its own trigger no longer
  toggles closed and back as the pointer re-enters.

### Changed
- Every user-facing “Noctalia” string in the UI is now CaeliGlow (patch 0014);
  identifiers (app id, palette keys, noctalia.dev URLs, greeter commands) are kept
  so system integration and existing configs keep working. The About sidebar entry
  is now “About” — the brand section owns the CaeliGlow name.
- One-command install: `scripts/quick-install.sh` (clone → patch series → release build →
  `/usr/local/bin/caeliglow`), with `scripts/uninstall.sh` as its symmetric remover.
- `pkgbuild/PKGBUILD`: AUR-ready Arch package `caeliglow` (installs/removes via pacman,
  zero file overlap with the distro `noctalia` package).
- README / docs/BUILDING.md document both install paths.

### Verified in this release
- Full debug rebuild + link clean; `meson test` **153/153 pass, 0 fail** (schema
  round-trip probe extended to cover all `[caeliglow]` fields).
- Series `0001→0015` applies cleanly onto a pristine v5.3.0 via `git am --3way` and
  the resulting tree is byte-identical to the development branch.

## [1.4.0] - 2026-10-19

CaeliGlow gets its own home: configuration, state and runtime live in a dedicated
`caeliglow` namespace instead of borrowing Noctalia's directories.

### Changed
- **Own configuration namespace (patch 0008).** CaeliGlow now reads and writes
  `~/.config/caeliglow/` (config), `~/.local/state/caeliglow/` (settings/state/plugin
  data) and `~/.local/share/caeliglow/` (user data) by default — never your stock
  Noctalia directories. On a first run the shell starts directly on CaeliGlow's own
  compiled-in defaults (hover-to-open panels, power pill, launcher avatar), so it is
  CaeliGlow out of the box rather than "your Noctalia config, relabeled". The user's
  `~/.config/noctalia` is never read, migrated, or modified.
- **Own runtime sockets.** The IPC socket, single-instance lock and dmenu socket are
  named `caeliglow-*` under `$XDG_RUNTIME_DIR`, so CaeliGlow can run side-by-side with
  a live stock Noctalia without talking to (or being blocked by) it.
- **Own log and caches.** Log file: `$XDG_CACHE_HOME/caeliglow/caeliglow.log`;
  calendar cache: `$XDG_CACHE_HOME/caeliglow/calendar/`.
- New environment overrides `CAELIGLOW_CONFIG_HOME` / `CAELIGLOW_STATE_HOME` /
  `CAELIGLOW_DATA_HOME` (legacy `NOCTALIA_*_HOME` still honored as an explicit
  escape hatch). Support-report replay (`config replay`) reconstructs the new layout.

### Verified in this release
- Full debug rebuild + link clean; `meson test` **153/153 pass, 0 fail** (updated
  path assertions in log / ipc / config-override tests).
- Series `0001→0008` applies cleanly onto a pristine v5.3.0 via `git am --3way`,
  reconstructing the developed tree byte-for-byte.

## [1.3.0] - 2026-10-19

Interactions you can actually see, on by default.

### Added
- **Hover-to-open-panel on the bar (patch 0005).** Hovering *any* bar widget now opens
  that widget's own panel with Noctalia's native attached-reveal animation, and closes
  it when you leave (short grace so you can travel into the panel). It is driven entirely
  from each widget's already-resolved left-click gesture (`Gesture::Left` →
  `panel-toggle <id>`), so it works uniformly for built-in, user-added and plugin widgets
  with zero per-widget code, and correctly does nothing for per-item widgets (workspaces,
  taskbar, tray). A 140 ms dwell guard stops accidental fires; PanelManager's
  single-active-panel model plus hover *ownership* means the hover flow only ever
  auto-closes a panel it opened itself, so it never fights a click- or edge-opened panel.
- **CaeliGlow right-edge power pill (patch 0006).** A new `caeliglow_power` shell action
  opens a center-right floating session pill — Logout / Power / animated logo / Lock /
  Restart — with the built-in confirm countdown on destructive entries and a hover-animated
  logo (`AnimatedImage`, a reusable idle→hover GIF driver). The original `power` action
  (native SessionPanel) is still available if you set it explicitly.
- **Animated launcher avatar (patch 0007).** When you have no personal avatar set, the
  launcher shows the CaeliGlow crescent mark, idle→hover animated; a real avatar takes over
  automatically and the loop detaches on close.
- **Full branded Settings › About page (patch 0007).** The About section is no longer two
  lines in a box: a centered animated-logo hero with name, tagline and version, a
  Release & updates card (live check), a "What CaeliGlow adds" summary, project links
  (repository / releases / report-an-issue via `xdg-open`), and a Credits & license block.

### Changed
- **Edge interactions are ON by default.** `hot_corners.enabled` now defaults to `true`
  with `bottom_edge.action = "launcher"` and `right_edge.action = "caeliglow_power"`, so a
  fresh CaeliGlow build shows its signature interactions without any config merge. Other
  corners stay inert (`"none"`).
- **Launcher layout polish.** Search bar moves to the top and the app provider prefix is
  `>` (was bottom / `/`).
- **Bar hover no longer zooms the icon.** The 1.0.x/1.1.x scale "pop" from patch 0001 is
  replaced by hover-to-open-panel (patch 0005); `kWidgetHoverPopScale` is gone.

### Verified in this release
- Full debug rebuild + link clean; `meson test` **153/153 pass, 0 fail**.
- Nested Hyprland smoke test: patched shell starts and runs stable with the new hover,
  edge, power-pill and About code active — no crashes; the host session is untouched.
- Series `0001→0007` applies cleanly onto a pristine v5.3.0 via `git am --3way`.

## [1.1.0] - 2026-10-18

Brand refresh + the animated mark rendered in-shell.

### Added
- **New crescent-moon identity:** the logo is now an original animated mark — a
  blue→violet crescent cradling a 4-point sparkle star, ringed by twinkling gold
  sparkles. Ships as static (`logo.svg`/`logo.png`), animated (`logo-animated.gif`/
  `.svg`), a wordmark, and a cinematic animated hero (`hero-animated.gif`) plus a
  GitHub social-preview. All generated from `scripts/gen_brand_assets.py` and
  `scripts/gen_hero.py` (original artwork; no upstream logos reused).
- **Animated logo in Settings › About (extends patch 0004):** the About header now
  shows the crescent-moon mark with its stars actually twinkling *inside the shell*.
  A bundled 128px GIF is decoded once into GPU textures and cycled by a self-re-arming
  `Timer`, mirroring Noctalia's own desktop-sticker GIF playback. Frames persist across
  content rebuilds (the `Image` node is re-attached each rebuild), the timer stops when
  you leave the section, and textures are freed when the window closes. Falls back to
  the static first frame if the GIF can't be decoded.

### Changed
- **Version is now read from the root `VERSION` file at configure time** (meson
  `run_command`) instead of a hard-coded string, so `VERSION` is the single source of
  truth for `--version`, the About section, and the update checker.
- README hero now uses the animated banner; brand guidelines + asset inventory updated
  to the crescent-and-sparkle motif.

## [1.0.0] - unreleased (development)

Initial CaeliGlow release, built as a patch series over **Noctalia v5.3.0 (MIT)**.

### Added
- **Patch pipeline & repo:** Noctalia pinned as a submodule at `v5.3.0`; `patches/`
  series applied with `git am --3way`; `scripts/build.sh`, `install.sh`,
  `apply-patches.sh`, `reset-patches.sh`, `rollback.sh`, `install-deps.sh`.
- **Bar hover (patch 0001):** Caelestia-style scale "pop" on widget hover — an
  independent re-implementation. Noctalia's widget contents, layout, accordion
  expansion and fill highlight are preserved. *Compiled-verified.*
- **Bottom-edge launcher reveal (patch 0002):** an optional wide, centered bottom-edge
  trigger strip added to Noctalia's `HotCorners`; on hover+dwell it opens the existing
  Noctalia launcher. Opt-in via `[hot_corners.bottom_edge]`. *Compiled + config-tested.*
- **Right-edge power controls (patch 0003):** an optional thin, full-height right-edge
  trigger whose new `"power"` action opens Noctalia's own SessionPanel (labeled buttons +
  confirm countdown, commands via `SessionActionRunner`/logind). The original
  Control-Center and Launcher power buttons are hidden by default (restorable in
  Settings). Opt-in via `[hot_corners.right_edge] action = "power"`.
  *Compiled (210 targets) + regression-tested (meson suite 153/153).*
- **Update-checker + version logic (core of feature #5):** canonical version source
  and a full update decision state machine (checking / up-to-date / update-available
  / no-releases / offline / rate-limited / error) with tolerant GitHub-release JSON
  parsing and a conservative stable channel. *Unit-tested: all scenarios pass.*
- **Native Settings About + live update check (patch 0004):** a "CaeliGlow" Settings
  section showing the CaeliGlow and Noctalia versions + MIT attribution, with a live
  "Check for updates" button wired through Noctalia's own async `HttpClient` to the
  GitHub releases endpoint and reported via the tested semver state machine. Gated by
  `shell.offlineMode`; release notes rendered as plain text and never executed.
  *Compiled (152 targets relinked) + regression-tested (meson suite 153/153).*
- **Docs:** README, `docs/BUILDING.md`, `docs/PATCHES.md`, `docs/UPDATING.md`,
  `docs/ATTRIBUTION.md`. **License policy enforced:** MIT for CaeliGlow; no Caelestia
  (GPL-3.0) code/assets copied; Noctalia attribution preserved.
- **CI:** build + test workflow (see `.github/workflows/`).

### Verified in this environment
- Unmodified Noctalia v5.3.0: configures (meson 1.12), builds (~12 min, 770
  targets), links a working `noctalia` binary, **unit tests 153/153 pass**.
- CaeliGlow patch 0001 rebuilds + relinks with no errors.
- CaeliGlow patches 0002 + 0003 rebuild + relink (210 targets); full `meson test`
  suite still **153/153 OK, 0 fail** (config roundtrip / CLI validate / overrides).
- CaeliGlow patch 0004 (native Settings About + live update check) rebuilds + relinks
  (152 targets; new `settings_content_about.cpp.o` in the core lib); `meson test`
  suite remains **153/153 OK, 0 fail**.
- Series 0001→0002→0003→0004 verified to apply cleanly onto a pristine v5.3.0 via
  `git am --3way`.
- Standalone update/version unit tests compile and pass.

### Not yet in 1.0.0 (planned, tracked in docs/PATCHES.md)
- Native Settings "CaeliGlow About" UI wiring around the (already-tested) update logic.
- Desktop (on-screen) behavioral verification of each feature.

### Known limitations
- Runtime visuals require launching the shell on Hyprland; they were intentionally
  not run over the author's live session. Multi-monitor / fractional-scaling hover
  stability should be re-checked on end-user hardware.
