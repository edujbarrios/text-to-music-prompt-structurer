# Changelog

All notable changes to this project are documented here. The project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.1] - 2026-07-15

### Added

- Expanded recognition for contemporary and global music genres.
- Structured voice type, vocal tone, vocal technique, and language output.

### Fixed

- Load bundled vocabulary files from the installed package so the CLI and Python API work outside the repository.
- Include the complete genre and vocal vocabularies in built distributions.

### Changed

- Document exact CLI and Python output and display the published PyPI version badge.

## [0.1.0] - 2026-07-15

### Added

- Structured detection of genres, moods, tempo, BPM, keys, instruments, production, vocals, languages, energy, rhythm, structure, and eras.
- Neutral `MusicPrompt` and `MusicPromptEngine` public API.
- Suno-compatible text formatting and backward-compatible API aliases.
- Installable `text-to-music-prompt` command.
- Bundled, extensible JSON vocabularies.
- Typed-package marker, automated tests, linting, and cross-platform CI.

[Unreleased]: https://github.com/edujbarrios/text-to-music-prompt-structurer/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/edujbarrios/text-to-music-prompt-structurer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/edujbarrios/text-to-music-prompt-structurer/releases/tag/v0.1.0

