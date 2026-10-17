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

## Planned — Bottom-edge launcher reveal
- **Approach:** extend `src/shell/hot_corners/` (which already provides dwell
  enter/leave trigger surfaces anchored to screen edges, calling
  `triggerShellAction("launcher")`) with a wider bottom-center edge zone and an
  open-only (non-toggle) launcher action, plus a `[hot_corners].bottom_edge` config.
- **Status:** not yet implemented. Tracked so it can be built and verified in a
  follow-up stage.

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
