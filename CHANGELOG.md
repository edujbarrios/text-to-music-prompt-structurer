# Changelog

All notable changes to this project are documented here. The project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.3.0] - 2026-10-13

### Added

- Conservative extraction of explicit negative instrumentation and production constraints to Suno's Exclude field.
- Public `extract_negative_constraints()` utility and `NegativeConstraints` result type.
- Non-destructive `validate_suno_prompt()` preflight with structured findings, warnings and optional user-defined length budgets.
- CLI `--check`, `--no-auto-exclude`, `--max-style-chars`, and `--max-lyrics-chars` switches.
- More robust detection of vocal language in context, including multilingual instructions and genre false positives.
- Expanded regression tests and workflow documentation for automated PyPI publishing.

### Fixed

- Prevent excluded musical features from reappearing in the positive Suno style description.
- Preserve the first explicit spelling and order of deduplicated exclusions.

### Documentation

- Reframed the project as an advanced AI/NLP/LLM-informed prompting system for Suno.


## [0.2.0] - 2026-10-13

### Added

- Suno Custom/Advanced field model with separate Style of Music, Lyrics, Exclude, Title, Instrumental, Vocal Gender and optional lyric brief.
- Structured section labels with per-section lyric lines and performance cues.
- Suno and JSON CLI modes, user-provided lyric files, exclusions and instrumentation toggles.
- Preservation of the original creative direction when building Suno-facing prompts.
- Documentation and contract tests based on official Suno creation guidance.

### Changed

- CLI defaults to paste-ready Suno fields; use `--format legacy` for previous labeled output.
- `format_for_suno()` now renders Suno field values instead of the legacy analysis format.

### Unchanged

- `MusicPromptEngine.process()`, `format_prompt()` and Suno aliases preserve the existing API.

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

[Unreleased]: https://github.com/edujbarrios/text-to-music-prompt-structurer/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/edujbarrios/text-to-music-prompt-structurer/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/edujbarrios/text-to-music-prompt-structurer/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/edujbarrios/text-to-music-prompt-structurer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/edujbarrios/text-to-music-prompt-structurer/releases/tag/v0.1.0

