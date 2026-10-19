# CaeliGlow patch series

CaeliGlow = a small, reviewable series of patches applied to a **pinned Noctalia
release** (currently **v5.3.0**, commit `a33122c4`), then built from source. This
file documents each patch, its rationale, its blast radius, and its verification
status. Patches are applied in `patches/series` order by `scripts/apply-patches.sh`
(via `git am --3way`). Regenerate any patch after editing the submodule tree:

```sh
cd upstream/noctalia
git add <files> && git commit -m "caeliglow: <what>"
git format-patch -1 -o ../../patches --start-number <N>
git reset --hard a33122c4          # return the submodule to its pinned commit
```

## Status legend
- **compiled** — the change builds with Noctalia's meson/ninja toolchain (verified here).
- **unit-tested** — covered by an automated test that was actually run and passed.
- **desktop-tested** — visually/behaviorally verified by launching the shell on Hyprland.

---

## 0001 — Bar hover: Caelestia-style scale "pop"
- **Superseded in 1.3.0 by [0005](#0005--bar-hover-opens-the-widgets-panel-replaces-0001-pop)**:
  the icon-zoom "pop" is removed and replaced by hover-to-open-panel. This patch is kept
  in the series history for honest provenance; its `setScale()` pop is reverted by 0005.
- **Files:** `src/shell/bar/bar.cpp`
- **What:** extends `Bar::animateWidgetHoverHighlight()` so the hovered widget's
  layout-bounds node gets a render-only `setScale()` "pop" toward the pointer,
  with a slight overshoot (`Easing::EaseOutBack`) on enter, settling to exactly
  1.0 on leave. Noctalia's existing fill-tint and accordion-expansion behavior is
  left intact; no widget contents, layout, or styling are replaced.
- **Why:** this is an **independent re-implementation** of the observed
  Caelestia "lively hover" feel. No Caelestia GPL code or assets are copied.
- **Blast radius:** low. `setScale()` is a paint transform (origin defaults to the
  node center), so it does not fight flex layout or hit-testing.
- **Status:** **compiled** (incremental rebuild + link succeeded). Not desktop-tested
  here (launching a second shell over the live session was intentionally avoided).
- **Tunable:** `kWidgetHoverPopScale` (currently `1.06`). A follow-up can expose it
  in `[bar.hover]` config and honor reduced-motion (the shared `animate()` already
  respects the global motion setting).

## 0002 — Bottom-edge launcher reveal
- **Files:** `src/shell/hot_corners/hot_corners.{h,cpp}`,
  `src/config/config_types.h`, `src/config/schema/config_schema.cpp`
- **What:** adds an optional wide, centered bottom-edge trigger strip to the existing
  `HotCorners` subsystem. On pointer enter + configurable dwell (`delay_ms`), it fires
  the existing `"launcher"` shell action, revealing the **same Noctalia launcher**
  panel; leaving the strip disarms the timer (no stuck state). It reuses the corner
  arming code (position `4`), so enter/leave/focus handling matches what already
  ships.
- **Config (opt-in, off by default so ordinary Noctalia is unchanged):**
  ```toml
  [hot_corners]
  enabled = true
  delay_ms = 120
  edge_width = 0            # 0 = auto (~25% of the screen)
  [hot_corners.bottom_edge]
  action = "launcher"
  ```
- **Correctness:** anchored Bottom+Left+Right with a fixed width so the compositor
  centers it per-output — behaves across multi-monitor and fractional scaling.
- **Intentional difference from Caelestia:** Noctalia's launcher is a floating panel,
  not a bar-docked surface, so Caelestia's exact concave-to-edge morph is not
  reproduced; the reveal is Noctalia's own panel open animation. This is a documented,
  independent re-implementation (no Caelestia GPL code/assets).
- **Status:** **compiled** (full incremental rebuild + link, 287 targets) and
  **config-tested** (`config_schema_roundtrip`, `cli_schema`, `config_migration`,
  `config_validate_cli`, `config_widget`, `config_override_mutation` all pass: 6/6).
  Not desktop-tested here (second-shell launch avoided over the live session).

## 0003 — Right-edge power controls (+ hide the original power entries)
- **Files:** `src/shell/hot_corners/hot_corners.{h,cpp}`,
  `src/config/config_types.h`, `src/config/schema/config_schema.cpp`,
  `src/app/application_services.cpp`
- **What:** adds an optional thin, full-height trigger strip along the **right edge**
  (mirrors the 0002 bottom-edge mechanism, reusing the same dwell/enter/leave arming as
  position `5`). A new shell action `"power"` opens Noctalia's **own SessionPanel**
  (`m_panelManager.togglePanel("session")`) — which already renders labeled action
  buttons and a **confirm countdown** for destructive actions and resolves every command
  through `SessionActionRunner`/logind (no hard-coded paths). By reusing the shipped
  SessionPanel we get hover labels + confirmation for free and add zero new UI surface.
- **Remove the original power entries:** the compiled-in defaults for
  `control_center.show_session_button` and `shell.launcher.show_session_button` are
  flipped to `false`, so the old header/toolbar power buttons are gone in a CaeliGlow
  build. They stay fully **restorable** in Settings (toggle them back on).
- **Config (opt-in, off by default so ordinary Noctalia is unchanged):**
  ```toml
  [hot_corners]
  enabled = true
  delay_ms = 120
  right_edge_width = 0        # 0 = auto (12 px thick)
  [hot_corners.right_edge]
  action = "power"
  ```
- **Correctness:** anchored Top+Bottom+Right so the compositor stretches the strip to the
  full output height per-output — correct across multi-monitor and fractional scaling.
  New config fields participate in `operator==`, so edits trigger a `hotCorners` reload
  and rebuild the surfaces.
- **Independent re-implementation:** behavior modeled on Caelestia's edge power strip,
  built from scratch on Noctalia's own subsystems; no Caelestia GPL code/assets.
- **Status:** **compiled** (full incremental rebuild + link, 210 targets) and
  **regression-tested** (`meson test` suite: **153/153 OK, 0 fail**, incl.
  `config_schema_roundtrip`, `config_validate_cli`, `config_override_mutation`).
  Series 0001→0002→0003 verified to apply cleanly onto a pristine v5.3.0 via
  `git am --3way`. Not desktop-tested here (a second shell over the live Hyprland
  session was intentionally avoided).

## 0004 — Native Settings "CaeliGlow About": animated logo + live update checker
- **What:** a new native Settings section (id `about`, label "CaeliGlow") added to
  Noctalia's Settings window. Its header shows the **animated crescent-moon mark**
  (twinkling stars), the CaeliGlow version (`-DCAELIGLOW_VERSION`), the Noctalia base
  version (`-DNOCTALIA_VERSION`) and MIT attribution, plus a **live "Check for updates"
  button**.
- **Animated logo:** a bundled GIF (`assets/caeliglow/logo-animated.gif`, a 128px variant
  of the brand mark) is decoded once into GPU textures and cycled frame-by-frame by a
  self-re-arming `Timer` — the same mechanism Noctalia's own desktop-sticker widget uses
  (`decodeAnimatedGif` + `Image::setExternalTexture`). The `Image` node is re-attached on
  every content rebuild; the loop stops when you leave the section and the textures are
  freed when the window closes. If the GIF can't be decoded it falls back to the static
  first frame.
- **How the update check works:** the button calls `SettingsWindow::checkForUpdates()`,
  which uses Noctalia's existing async `HttpClient` (owned by `Application`, injected via
  `setHttpClient`) to `GET` the `mockifylab/CaeliGlow` GitHub releases endpoint. The
  response is fed to the already unit-tested `caeliglow::update_model::evaluate()`
  semver state machine; the result is rendered back through a content rebuild.
- **Version source:** `CAELIGLOW_VERSION` is read from the repository-root `VERSION` file
  at configure time (meson `run_command`), so `VERSION` is the single source of truth.
- **Safety:** gated by `shell.offlineMode` (no network when enabled); non-2xx / 403 /
  429 / transport failures map to error/rate-limited/offline states; release notes are
  shown as **plain text and never executed**; the callback runs on the main loop and
  `SettingsWindow` is a long-lived `Application` member (lifetime-safe `this` capture).
- **Files:** `src/caeliglow/{version,update_model,meta}.hpp` (vendored + new meta),
  `src/shell/settings/settings_content_about.{h,cpp}` (new), the bundled
  `assets/caeliglow/logo-animated.gif`, plus registration edits in
  `settings_registry.{h,cpp}` (section 24→25), `settings_window.{h,cpp}`,
  `settings_window_scene.cpp`, `settings_content.cpp`, `application_ui.cpp`,
  `meson.build`, `assets/translations/en.json`.
- **Status:** **compiled** (clean from-scratch debug build, 283 targets linked into
  `noctalia`; new `settings_content_about.cpp.o` in `libnoctalia_core.a`) and
  **regression-tested** (`meson test`: **153/153 OK, 0 fail**). Series
  0001→0002→0003→0004 (binary GIF included) verified to apply cleanly onto a pristine
  v5.3.0 via `git am --3way`. Not desktop-tested here (a second shell over the live
  Hyprland session was intentionally avoided).

---

## 0005 — Bar hover opens the widget's panel (replaces 0001 pop)
- **Files:** `src/shell/bar/bar.{h,cpp}`, `src/shell/bar/bar_instance.h`,
  `src/shell/bar/widget.{h,cpp}`, `src/shell/panel/panel_manager.h`
- **What:** hovering a bar widget now **opens that widget's own panel** using Noctalia's
  native attached-reveal animation, and closes it when the pointer leaves (after a short
  grace so you can travel into the panel). The old `setScale()` icon "pop" from 0001 is
  removed (`kWidgetHoverPopScale` deleted).
- **Generic by construction:** the reveal is keyed entirely off each widget's already
  resolved left-click gesture. `Widget::boundHoverPanel()` reads `Gesture::Left`; if it is
  an anchored-panel verb (`isAnchoredPanelVerb`) it returns the target `panelId`+`context`,
  and `Widget::hoverOpenBoundPanel()` opens it. So built-in, user-added and plugin widgets
  all follow the same rule with **zero per-widget code**, and widgets whose left-click is
  not a panel toggle (caffeine, theme, etc.) or per-item widgets without a whole-widget
  binding (workspaces, taskbar, tray) correctly do nothing on hover.
- **Dwell + close-watch state machine (`Bar`):** `handleWidgetHoverReveal()` (called from
  the bar hover-change callback) starts a one-shot **140 ms dwell** timer before opening,
  so a fast pass-through the bar doesn't fire panels. `beginHoverRevealCloseWatch()` runs
  a **170 ms repeating** guard that keeps the panel while the pointer is on the revealed
  widget *or* inside the panel (`PanelManager::isPointerInsidePanel()`), and otherwise
  closes it. `Bar::clearHoverReveal()` tears the state down.
- **Conflict arbitration:** `hoverRevealPanelId` records *ownership* — the hover flow only
  ever auto-closes the panel it opened, never a click- or edge-opened one. Layered on
  PanelManager's single-active-panel model (opening B closes A), this keeps widget-hover,
  bottom-edge launcher and right-edge power from stacking into a mess: exactly one reveal
  is active at a time.
- **Status:** **compiled + regression-tested** (`meson test` 153/153) and **nested-
  session smoke-tested** (shell starts and runs stable; hover wiring live).

## 0006 — CaeliGlow right-edge power pill + on-by-default edges + animated core
- **Files:** `src/caeliglow/animated_image.{h,cpp}` (new),
  `src/shell/session/caeliglow_power_panel.{h,cpp}` (new),
  `src/shell/hot_corners/hot_corners.cpp`, `src/config/config_types.h`,
  `src/config/schema/config_schema.cpp`, `src/app/application_services.cpp`,
  `src/app/application_ui.cpp`, `meson.build`,
  `assets/caeliglow/logo-panel-idle.gif`, `assets/caeliglow/logo-panel-hover.gif` (new)
- **What:** a new shell action `caeliglow_power` opens a center-right floating session
  pill (Logout · Power · animated logo · Lock · Restart) with the native confirm countdown
  on destructive entries. `AnimatedImage` is a reusable idle→hover GIF driver (load per
  slot, attach/detach to an `Image`, advance on frame tick) shared by the pill and the
  launcher avatar.
- **On by default:** `HotCornersConfig.enabled` defaults to `true`, with
  `rightEdge.action = "caeliglow_power"` and `bottomEdge.action = "launcher"`; other
  corners stay inert (`Corner.action` default `"none"`). The original `"power"` action
  (native SessionPanel) is preserved for anyone who sets it explicitly.
- **Registration:** the pill panel is registered in `application_ui.cpp` under
  `"caeliglow:power"`; `application_services.cpp` dispatches `"caeliglow_power"` to it.
  `config_schema.cpp` documents/validates the right-edge actions.
- **Status:** **compiled + regression-tested** (153/153) and nested-session smoke-tested.

## 0007 — Animated launcher avatar + full branded About page
- **Files:** `src/shell/launcher/launcher_panel.{h,cpp}`, `assets/translations/en.json`,
  `src/shell/settings/settings_content_about.cpp`
- **Launcher:** when no personal avatar is set, the launcher shows the CaeliGlow crescent
  mark via `AnimatedImage` (idle→hover), driven from `onFrameTick`; a real avatar takes
  over and the loop detaches on close. Search moves to the **top** and the provider prefix
  becomes `>` (defaults set in `config_types.h` under 0006).
- **About page:** `addSettingsCaeliGlowAbout` is expanded from two lines in a box into a
  full native page: a centered **animated-logo hero** (name, tagline, version) using the
  existing `SettingsWindow::attachAboutLogo` GIF machinery, a **Release & updates** card
  (version, base version, live Check-for-updates + status), a **What CaeliGlow adds**
  summary, a **Project links** card (repository / releases / report-an-issue opened via
  `net::openInBrowser`), and a **Credits & license** block — all built from native Settings
  widgets (`addSettingsCard`, `ui::column/row/label/button/image`).
- **Safety:** links are the fixed `mockifylab/CaeliGlow` GitHub URLs from `caeliglow/meta.hpp`;
  the update check is unchanged (single unauthenticated GET, plain-text result, offline-mode
  gated).
- **Status:** **compiled + regression-tested** (153/153) and nested-session smoke-tested.

## 0008 — Own config/state/cache/socket namespace (CaeliGlow by default)
- **Files:** `src/util/file_utils.h`, `src/ipc/ipc_client.cpp`, `src/ipc/ipc_service.cpp`,
  `src/app/single_instance_lock.cpp`, `src/launcher/dmenu_socket_path.cpp`, `src/core/log.cpp`,
  `src/calendar/calendar_service.cpp`, `src/config/cli.cpp`, `src/theme/theme_service.h`,
  `tests/log_test.cpp`, `tests/ipc_service_test.cpp`, `tests/capsule_group_lane_override_test.cpp`,
  `tests/config_override_mutation_test.cpp`
- **What & why:** before 1.4.0 CaeliGlow reused Noctalia's user directories, so it rendered
  *the user's* Noctalia customization and behaved like "Noctalia with an About page". Now
  `FileUtils::configDir/stateDir/dataDir` resolve `caeliglow` by default
  (`~/.config/caeliglow`, `~/.local/state/caeliglow`, `~/.local/share/caeliglow`), with new
  `CAELIGLOW_CONFIG_HOME` / `CAELIGLOW_STATE_HOME` / `CAELIGLOW_DATA_HOME` overrides; the
  legacy `NOCTALIA_*_HOME` vars still work as an explicit escape hatch. A fresh install with
  no `~/.config/caeliglow` starts on CaeliGlow's compiled-in defaults (ConfigService already
  logs "no config files found, using defaults").
- **Runtime isolation:** IPC socket, single-instance lock and dmenu socket renamed to
  `caeliglow-*` under `$XDG_RUNTIME_DIR`, so CaeliGlow neither commands nor clashes with a
  live stock Noctalia. Log moves to `$XDG_CACHE_HOME/caeliglow/caeliglow.log`; calendar
  cache to `caeliglow/calendar`; `config replay` (support reports) reconstructs the new layout.
- **Deliberately kept:** installed asset tree (`share/noctalia/assets`, matches meson
  `install_subdir`), the binary name `noctalia`, PAM service + greeter staging names, pywalfox
  compat socket, DBus/icon-prefix identifiers — renaming those would break system integration
  with no isolation benefit. Nothing in this patch ever reads, migrates or writes the user's
  Noctalia directories.
- **Status:** **compiled + regression-tested** (153/153; path assertions updated in the
  four affected tests).

---

## Notes on safety of the model
- The submodule stays pinned at `v5.3.0`; the patches are the *only* CaeliGlow
  changes, so rebasing onto a newer Noctalia is a `git am` retry per patch.
- Nothing is installed into `/usr`; CaeliGlow builds install under `/usr/local`
  and never overwrite the distro `noctalia` package, keeping rollback trivial.
