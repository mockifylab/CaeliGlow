# CaeliGlow — Project Overview

> A one-page pitch. Use it as README-adjacent context, a design-review brief, or the
> speaking notes for a 5-minute presentation. Detailed rationale lives in
> [PATCHES.md](PATCHES.md); how-tos in [BUILDING.md](BUILDING.md) / [UPDATING.md](UPDATING.md).

---

## The one-liner

**CaeliGlow is a small, documented patch series over a pinned Noctalia release that adds
the edge-glow interactions and self-updating polish a modern Hyprland desktop should
have — without touching anything else the shell already does well.**

## The problem

People who love Noctalia often want two things upstream won't prioritize:

1. **Direct-manipulation edges** — flick the pointer to the bottom to open the launcher,
   or to the right for a power rail — the fluid, "the desktop responds to me" feel that
   Caelestia popularized.
2. **Confident maintenance** — knowing your shell is current, with an in-app update check,
   and being able to update or roll back without fear of bricking the session.

Copying Caelestia is not an option: it's GPL-3.0 and a different (Quickshell) stack.
Forking Noctalia wholesale is heavy: it drifts from upstream and gets hard to maintain.

## The approach

**Fork-and-patch, done with restraint.** Noctalia is pinned as a git submodule at a known
tag (`v5.3.0`). CaeliGlow's *only* changes are a numbered series of `git am` patches under
`patches/`. Build = pin check → apply patches → `meson`/`ninja`.

Why this wins:

| Property | Benefit |
|----------|---------|
| Auditable | The whole product delta is a handful of readable patch files (currently 7). |
| Reversible | `reset-patches.sh` returns the tree to pristine upstream instantly. |
| Upgradable | Rebasing onto a new Noctalia = retry `git am` per patch, not re-merge a fork. |
| Safe on the machine | Installs to `/usr/local`; the distro `noctalia` package is never overwritten. |
| License-clean | MIT throughout; Caelestia is a *behavioral reference only* — zero code/assets copied. |

## What ships

- **Bar hover → open the widget's panel (1.3.0)** — hovering any bar widget opens *that
  widget's* panel with Noctalia's native reveal animation and closes it on leave. Driven
  from each widget's own left-click gesture, so it covers built-in, user and plugin widgets
  uniformly and stays inert for per-item widgets. The old icon-zoom is gone.
- **Bottom edge → launcher (on by default)** — a wide centered strip; hover+dwell reveals
  the *existing* launcher via Noctalia's own HotCorners dwell engine.
- **Right edge → CaeliGlow power pill (on by default)** — a full-height trigger whose
  `caeliglow_power` action opens a floating, animated session pill (Logout · Power ·
  animated logo · Lock · Restart) with confirm countdowns. The native SessionPanel `power`
  action remains available. Duplicate original power buttons are hidden by default,
  restorable in config.
- **Settings › About (full branded page) + update check** — native "CaeliGlow" section
  headed by the **animated crescent-moon mark**, now a full page: hero + version, a live
  "Check for updates" (Noctalia's async `HttpClient` → a fully unit-tested semver state
  machine), a feature summary, project links and attribution.
- **Animated launcher avatar + Brand (1.1.0)** — the launcher carries the crescent mark as
  its avatar; the identity itself (static + animated logo, wordmark, cinematic hero) is
  original artwork generated from scripts in `scripts/`.

The signature interactions ship **enabled by compiled-in defaults**, so a stock CaeliGlow
build shows them with no config; everything stays additive and overridable.

## Engineering principles

1. **Preserve by default.** If Noctalia already does it, CaeliGlow keeps it.
2. **Additive, never destructive.** New config fields have safe defaults; no removals;
   no system/boot changes.
3. **Reuse the platform.** Edges reuse HotCorners; power reuses SessionPanel; updates
   reuse HttpClient — minimal new surface area.
4. **Verified, honestly labeled.** Compile + regression + unit-test status is stated
   precisely; live-desktop testing is called out as the remaining on-device step.
5. **Attribution is non-negotiable.** MIT for CaeliGlow; Noctalia MIT preserved; Caelestia
   referenced, never copied.

## Quality bar (current evidence)

- Baseline Noctalia v5.3.0 builds and links a working binary.
- Patches 0001–0007 rebuild + relink cleanly.
- `meson test` suite: **153/153 pass, 0 fail** (config schema/validate/override cover the
  new fields).
- Standalone version/update logic tests: **all pass** (and wired into CI).
- Nested Hyprland smoke test: shell starts and runs stable with hover-to-open, edges, the
  power pill and the About page active — host session untouched.
- Full `0001→0007` series applies onto a pristine v5.3.0 via `git am --3way`.
- Example config validates against the patched binary.

## Positioning & identity

- **Name:** Caeli (of the sky) + Glow. **Look:** a soft aurora over deep-indigo night —
  calm, premium, restrained. Teal → violet → amber accents; generous negative space.
- **Voice:** precise, quietly confident, technically honest. Refinement, not replacement.
- Full identity kit: [docs/brand/brand-guidelines.md](brand/brand-guidelines.md).

## Where it goes next

Live per-gesture motion tuning, multi-monitor / fractional-scaling edge hardening, and an
optional auto-update installer on the same update model — see [ROADMAP.md](ROADMAP.md).

---

*© 2026 Aasif / mockifylab · MIT · unaffiliated with Noctalia and Caelestia.*
