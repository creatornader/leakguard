# Changelog

All notable changes to leakguard are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-05-17

### Fixed

- Override catalog files no longer have to duplicate the `name:` field when extending an existing class by `id`. The base catalog's name is inherited automatically; truly-new classes (no matching `id` in the base) default `name` to the `id`. Surfaced when wiring leakguard into a real repo whose `leakguard.yaml` extended `cross-project-codenames` with only `id` + `patterns`.

## [0.1.0] - 2026-05-17

### Added

- Initial spike. Python package + console script (`leakguard scan`, `leakguard init`, `leakguard list-classes`).
- YAML catalog format with user override + merge semantics. Override files extend by default; pass `replace: true` to swap the base entry entirely. `ignore_paths` from base + override are concatenated and deduped.
- Starter catalog with 13 leak classes: 10 generic (default-on) and 3 user-extensible (no defaults shipped). See [`docs/leak-classes.md`](docs/leak-classes.md) for the taxonomy.
- `--exclude GLOB` CLI flag stacks with catalog `ignore_paths`.
- Pre-commit framework integration via `.pre-commit-hooks.yaml`.
- 7 smoke tests covering catalog load, scan, ignore, and override-merge paths.
- Apache 2.0 license.

[0.1.1]: https://github.com/creatornader/leakguard/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/creatornader/leakguard/releases/tag/v0.1.0
