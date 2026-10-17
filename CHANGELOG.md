# Changelog

All notable changes to CaeliGlow are documented here. The format follows
Keep-a-Changelog; CaeliGlow uses Semantic Versioning. CaeliGlow's version is read
from the single canonical `VERSION` file.

## [1.0.0] - unreleased (development)

Initial CaeliGlow release, built as a patch series over **Noctalia v5.3.0 (MIT)**.

### Added
- **Patch pipeline & repo:** Noctalia pinned as a submodule at `v5.3.0`; `patches/`
  series applied with `git am --3way`; `scripts/build.sh`, `install.sh`,
  `apply-patches.sh`, `reset-patches.sh`, `rollback.sh`, `install-deps.sh`.
- **Bar hover (patch 0001):** Caelestia-style scale "pop" on widget hover — an
  independent re-implementation. Noctalia's widget contents, layout, accordion
  expansion and fill highlight are preserved. *Compiled-verified.*
- **Update-checker + version logic (core of feature #5):** canonical version source
  and a full update decision state machine (checking / up-to-date / update-available
  / no-releases / offline / rate-limited / error) with tolerant GitHub-release JSON
  parsing and a conservative stable channel. *Unit-tested: all scenarios pass.*
- **Docs:** README, `docs/BUILDING.md`, `docs/PATCHES.md`, `docs/UPDATING.md`,
  `docs/ATTRIBUTION.md`. **License policy enforced:** MIT for CaeliGlow; no Caelestia
  (GPL-3.0) code/assets copied; Noctalia attribution preserved.
- **CI:** build + test workflow (see `.github/workflows/`).

### Verified in this environment
- Unmodified Noctalia v5.3.0: configures (meson 1.12), builds (~12 min, 770
  targets), links a working `noctalia` binary, **unit tests 153/153 pass**.
- CaeliGlow patch 0001 rebuilds + relinks with no errors.
- Standalone update/version unit tests compile and pass.

### Not yet in 1.0.0 (planned, tracked in docs/PATCHES.md)
- Bottom-edge launcher reveal (extend `hot_corners`).
- Right-edge power controls + removal of the duplicate original power entry.
- Native Settings "CaeliGlow About" UI wiring around the (already-tested) update logic.
- Desktop (on-screen) behavioral verification of each feature.

### Known limitations
- Runtime visuals require launching the shell on Hyprland; they were intentionally
  not run over the author's live session. Multi-monitor / fractional-scaling hover
  stability should be re-checked on end-user hardware.
