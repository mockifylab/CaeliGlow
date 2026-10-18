# Security Policy

CaeliGlow is a desktop shell customization. It runs with your session privileges and can
launch power actions, so we take its trust boundaries seriously.

## Reporting a vulnerability

**Please do not open a public issue for security problems.** Report privately via GitHub's
*"Report a vulnerability"* feature on
[mockifylab/CaeliGlow](https://github.com/mockifylab/CaeliGlow/security), or email the
maintainer through the contact on that page. We aim to acknowledge within a few days and
will coordinate disclosure.

## Threat model & current safeguards

### Update checker (Settings › About, patch 0004)
- Queries **only** `https://api.github.com/repos/mockifylab/CaeliGlow/releases` over HTTPS
  via Noctalia's existing `HttpClient`. No other hosts, no credentials sent.
- **Respects offline mode** — when `shell.offlineMode` is set, no request is made at all.
- JSON is parsed defensively; malformed/unexpected payloads resolve to an *error* state,
  never a crash or an arbitrary action.
- **Release notes are rendered as plain text and are never executed, sourced, or used to
  build shell commands.** Version comparison uses a strict semver model (unit-tested).
- HTTP status mapping is conservative: transport failure → offline; `403`/`429` → rate
  limited; other non-2xx → error. A future release is only ever *displayed* — this build
  ships **no automatic install/execution** of updates.

### Edge / power actions (patches 0002, 0003)
- The right-edge `power` action opens Noctalia's **own** SessionPanel; destructive actions
  keep the built-in **confirm countdown**, and commands resolve through Noctalia's
  `SessionActionRunner`/logind — CaeliGlow adds no new privileged execution path.
- Bottom-edge reveal reuses the existing launcher trigger; it introduces no new IPC surface.

### Build & install safety
- **Additive installs only.** `scripts/install-deps.sh` uses `pacman -S --needed`; it never
  removes packages. `install.sh` targets `/usr/local` and does **not** overwrite the distro
  `noctalia` at `/usr/bin`. No boot loader, EFI, partition or disk operations are performed
  by any script — keeping dual-boot / fallback intact.
- **Rollback is trivial and non-destructive:** `scripts/rollback.sh` and
  `scripts/reset-patches.sh` restore a clean state.

### Licensing as a safety property
- No code or assets are copied from Caelestia (GPL-3.0) or other non-compatible sources.
  This is both a legal and a supply-chain control: the only third-party code you run is the
  pinned, MIT-licensed Noctalia upstream plus CaeliGlow's own patch series.

## Hardening the patch supply chain

- The Noctalia submodule is pinned to an exact commit/tag (`v5.3.0`), so builds are
  reproducible against a known upstream.
- The entire product delta is a small, reviewable `patches/` series — audit it directly
  instead of trusting a large fork.

## Version support

| Version | Supported |
|---------|-----------|
| 1.0.0   | ✅ |

Security fixes are shipped in patch releases; subscribe to releases to be notified.
