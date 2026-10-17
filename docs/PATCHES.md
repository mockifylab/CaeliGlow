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

## Planned — Right-edge power controls (+ remove duplicate power entry)
- **Approach:** a right-edge vertically-mounted layer surface using Noctalia's own
  controls (`ui::button`, tooltips, `Style`/`Palette`) with hover/focus labels and a
  confirmation step for destructive actions, wired to `SessionActionRunner`
  (`src/shell/session/`) and logind — no hard-coded paths. Then hide the original
  power entry in the control center once verified.
- **Status:** not yet implemented.

## Planned — Native Settings "CaeliGlow About" + update checker
- **Reusable, already verified piece:** `src/caeliglow/update_model.hpp` +
  `src/caeliglow/version.hpp` implement canonical-version reading and the full
  update decision state machine (checking / up-to-date / update-available /
  no-releases / offline / rate-limited / error), with tolerant JSON handling and a
  conservative stable-release channel. These compile and pass their unit tests
  standalone (see `tests/test_update_model.cpp`).
- **Remaining work:** wire these into the native Settings GUI (`src/shell/settings/`)
  as a "CaeliGlow" section and call GitHub's public releases endpoint via Noctalia's
  existing HTTP stack, rendering release notes as plain text only.
- **Status:** logic implemented + **unit-tested**; Settings UI integration pending.

---

## Notes on safety of the model
- The submodule stays pinned at `v5.3.0`; the patches are the *only* CaeliGlow
  changes, so rebasing onto a newer Noctalia is a `git am` retry per patch.
- Nothing is installed into `/usr`; CaeliGlow builds install under `/usr/local`
  and never overwrite the distro `noctalia` package, keeping rollback trivial.
