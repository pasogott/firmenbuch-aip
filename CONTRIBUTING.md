# Contributing

Danke, dass du beitragen willst!

## Voraussetzungen

- Python 3.11+
- `uv`

## Setup

```bash
# Repo klonen
git clone https://github.com/pasogott/firmenbuch-aip.git
cd firmenbuch-aip

# Virtuelle Umgebung + Dependencies
uv venv && source .venv/bin/activate
uv add --dev ruff mypy pytest pytest-mock pre-commit
```

## Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Linting & Formatting

```bash
ruff check .
ruff format .
```

## Tests

```bash
pytest -q
```

## Releases

```bash
# Version taggen und pushen (erstellt Release automatisch)
git tag v0.2.0
git push origin v0.2.0
```

## Pull Requests

- Bitte kleine, fokussierte PRs
- Tests/Formatierung vor dem Push ausführen
- Beschreibung der Änderung + Motivation
