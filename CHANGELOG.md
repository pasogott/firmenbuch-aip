# Changelog

## [Unreleased]

## [0.2.3] - 2026-01-12

### Added
- Pre-commit hooks for Ruff, mypy, and pytest.
- CLI pagination helpers (`--limit`, `--offset`).
- `firmenbuchat` command name for the CLI.
- `doctor` diagnostics command.
- CONTRIBUTING guidelines and UV-based setup.
- Homebrew Tap support and release automation workflow.
- `.env` example and AGENTS instructions.
- `help` command showing all subcommands.

### Changed
- Centralized SOAP request handling.
- Updated docs to use `uv add` commands.
- Replaced legacy `fb` examples with `firmenbuchat`.
- SOAP retries with 60s timeout for slow endpoints.
- SOAP payloads use enum values and required fields.
- Author name corrected to Pascal SCHOTT.

## [0.2.0] - 2025-01-12

### Added
- Typer + Rich based CLI.
- API documentation split across multiple Markdown files.
