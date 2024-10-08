# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [TBD] - TBD

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [v0.1.5] - 2024-10-08

### Added

- Coverage shield is now in readme
- Add `-s / --system` option to `ask` command to specify the system prompt.
    - Allow piping content to Whisper as the `prompt` argument.
    - e.g: `git diff | whisper -s "Describe these changes"`

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [v1.0.4] - 2024-10-07

### Added

- 80% test coverage.

### Changed

- Updated readme to inclue donation options :)
- Updated the CLI command organization for the project.
    - Command groups are contained inside the `cli` directory.
    - The `ask` group is the "main" command with other commands nested below it.  This allows us to use `ask` as the default command if none is specified.

### Deprecated

### Removed

### Fixed

### Security

## [0.1.3] - 2024-10-01

### Added

- Added support for Mistral, Fireworks and Azure OpenAI.
- Added `--copy/--no-copy` option to the `ask` command to copy the output to the clipboard.

### Changed

### Deprecated

### Removed

### Fixed

- Better printing of the configuration file and themes.

### Security


## [0.1.2] - 2024-10-01

### Added

- Anthropic Integration [#6](https://github.com/syn54x/just-whisper/pull/6)

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.1] - 2024-10-01

### Added

- Add github-pages documentation using mkdocs [#2](https://github.com/syn54x/just-whisper/pull/2)


### Changed

- Update `pyproject.toml` to specify Python version >= 3.10.
- Update `pyproject.toml` to specify `uv` as the build system [#3](https://github.com/syn54x/just-whisper/pull/3).

### Deprecated

### Removed

### Fixed

- Fix str has no snippet [#3](https://github.com/syn54x/just-whisper/issues/3)

### Security

## [0.1.0] - 2024-09-30

### Added

- Initial setup of the project structure.
- Basic command-line interface for the Whisper application.
- Project initialization with basic configuration and dependencies as specified in `pyproject.toml`.
- Implementation of Whisper CLI commands in `src/whisper/__init__.py` (startLine: 27, endLine: 92).
- Configuration management commands in `src/whisper/config.py` (startLine: 1, endLine: 36).

### Changed

### Deprecated

### Removed

### Fixed

### Security
