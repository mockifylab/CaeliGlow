# Changelog

All notable changes to CaeliGlow are documented here. The format follows
Keep-a-Changelog; CaeliGlow uses Semantic Versioning. CaeliGlow's version is read
from the single canonical `VERSION` file.

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
