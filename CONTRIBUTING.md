# Contributing to CaeliGlow

Thanks for helping make a Noctalia-based shell a little more alive. CaeliGlow is a
**patch series over a pinned upstream**, so contributing has a specific shape. Please
read this before opening a PR.

## The golden rules

1. **Preserve Noctalia.** If upstream already provides behavior, keep it. Add or replace
   only the specific interactions the project is about.
2. **Stay additive & reversible.** New config fields must have safe defaults; the shell
   must behave like plain Noctalia when CaeliGlow config is absent.
3. **License integrity is absolute.** Do **not** copy code or assets from Caelestia
   (GPL-3.0) or any non-MIT-compatible source. "Caelestia-style" = independently
   re-implemented behavior only. Everything here stays **MIT**.
4. **One patch, one concern.** Changes ship as numbered patches in `patches/`, not as
   edits to a forked tree.

## How the repo is structured

- `upstream/noctalia/` — the Noctalia **submodule**, pinned to a release tag. You do not
  commit directly to it in the public repo.
- `patches/NNNN-*.patch` — the actual CaeliGlow delta, applied with `git am --3way`.
- `patches/series` — ordered list of patches.
- `src/caeliglow/` — pure, standalone-tested logic (version/update model) shared by the
  patches.
- `tests/` — logic unit tests (run in CI + locally).
- `scripts/` — build/install/apply/reset/rollback helpers.

## Making a change

```sh
git clone --recursive https://github.com/mockifylab/CaeliGlow.git
cd CaeliGlow
./scripts/apply-patches.sh            # tree now = v5.3.0 + all patches
# edit files under upstream/noctalia/ ...
cd upstream/noctalia
just configure debug && just build debug && just test debug
```

When your change is ready, produce a patch on top of the series:

```sh
# from upstream/noctalia, commit your single logical change:
git add -A && git commit -m "caeliglow: <what & why>"
git format-patch -1 -o ../../patches --start-number <nextN>
# append the filename to ../../patches/series
```

Keep each patch independently reviewable. Regenerate the series so it applies cleanly onto
a **pristine** pinned tree (the CI and `reset-patches.sh` rely on this).

## Definition of done

- [ ] Builds cleanly (incremental rebuild + link, no new warnings beyond baseline).
- [ ] `meson test` still passes (report the pass count).
- [ ] Logic changes have a matching case in `tests/test_update_model.cpp` (or a new test).
- [ ] `config` additions round-trip and pass `noctalia config validate`.
- [ ] Full series applies onto a pristine v5.3.0 via `git am --3way`.
- [ ] Docs updated: `docs/PATCHES.md`, `CHANGELOG.md`, README feature table if user-facing.
- [ ] No copied GPL/Caelestia material; attribution intact.

## Style

- Match surrounding Noctalia C++ style (C++23, its formatting and idioms).
- Comments: concise, explain *why*; no narration of obvious code.
- Prefer reusing Noctalia subsystems (HotCorners, SessionPanel, HttpClient, Settings
  registry) over new bespoke surfaces.

## Proposing bigger ideas

Open an issue first to discuss scope. This project deliberately stays small; a feature
that duplicates or forks upstream behavior will likely be declined in favor of an upstream
PR.

## Reporting bugs & security

- General bugs: GitHub issues, with your Noctalia/CaeliGlow versions and config.
- **Security:** see [SECURITY.md](SECURITY.md) — please do not file publicly.

By contributing you confirm your changes are MIT-licensed and contain no third-party
GPL/copyleft code.
