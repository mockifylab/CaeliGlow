# Updating, backup and rollback

CaeliGlow is designed to be reversible and to never clobber your distro's
`noctalia` package (which lives at `/usr/bin/noctalia`). CaeliGlow installs under
`/usr/local`, so ordinary Noctalia keeps working the whole time.

## How the update checker works

The About section checks CaeliGlow's public GitHub **releases** and compares them to
the installed version. Guarantees (implemented in `src/caeliglow/update_model.hpp`):

- Public, unauthenticated GET only — **no** user config, tokens, or machine
  identifiers are sent.
- It **never** runs remote code and never silently installs. The user explicitly
  initiates any update, which then: (1) explains what will change, (2) backs up,
  (3) validates the release/tag, (4) rebuilds from source, (5) offers rollback.
- Release notes are treated as **plain text** (never executed/HTML-injected).
- Distinct UI states: checking · up-to-date · update available · offline ·
  rate-limited · error. If current: "You're using the latest CaeliGlow release."

## Manual update flow (recommended today)

```sh
cd CaeliGlow
git fetch --tags --recurse-submodules=no
git checkout v1.1.0                       # the CaeliGlow release you want
git submodule update --init --recursive   # move Noctalia to that pinned commit
./scripts/build.sh release /usr/local
sudo ./scripts/install.sh release /usr/local
```

## Before any change: back up your config

Since 1.4.0 CaeliGlow keeps its configuration in **its own namespace** — your stock
Noctalia directories are never read or written. Back up what CaeliGlow owns:

```sh
cp -a ~/.config/caeliglow ~/.config/caeliglow.bak.$(date +%F-%H%M%S) 2>/dev/null || true
cp -a ~/.local/state/caeliglow ~/.local/state/caeliglow.bak.$(date +%F-%H%M%S) 2>/dev/null || true
```

Restore with:
```sh
rm -rf ~/.config/caeliglow && mv ~/.config/caeliglow.bak.<stamp> ~/.config/caeliglow
```
(CaeliGlow does not rewrite your `settings.toml`/`state.toml` unless you enable an
edge-hover feature; these backups let you undo safely. `~/.config/noctalia` belongs to
your Noctalia install and CaeliGlow leaves it completely alone.)

## Roll back to ordinary Noctalia

```sh
./scripts/rollback.sh release /usr/local
```
This uninstalls the `/usr/local` CaeliGlow files and resets the patched tree. Your
`/usr/bin/noctalia` package is untouched, so logging out and back in returns you to
standard Noctalia immediately.

## Verify what is running

```sh
which noctalia            # /usr/local/bin/noctalia (CaeliGlow) vs /usr/bin/noctalia (distro)
noctalia --version
```
