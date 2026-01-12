# SKILL.md — Firmenbuch CLI

## Zweck
CLI für den Zugriff auf die österreichischen Firmenbuch-WebServices (HVD).

## Installation (UV)

```bash
uv add git+https://github.com/pasogott/firmenbuch-aip.git
```

## Installation (Homebrew)

```bash
brew tap pasogott/tap
brew install firmenbuchat
```

## Dev-Setup

```bash
git clone https://github.com/pasogott/firmenbuch-aip.git
cd firmenbuch-aip
uv venv && source .venv/bin/activate
uv add --editable .
uv add --dev ruff mypy pytest pytest-mock pre-commit
pre-commit install
```

## Authentifizierung

- API-Key von JustizOnline erforderlich
- Speichern via CLI oder ENV:

```bash
firmenbuchat config set-key
export FIRMENBUCH_API_KEY="dein-key"
```

## .env Datei verwenden

```bash
cp .env.example .env
firmenbuchat --env-file /pfad/zu/deiner.env suche firma "Muster*"
```

## Hauptbefehle

```bash
firmenbuchat auszug 160573m
firmenbuchat suche firma "Musterfirma*"
firmenbuchat suche urkunde 160573m
firmenbuchat urkunde info "URKUNDEN_KEY"
firmenbuchat urkunde download "URKUNDEN_KEY"
firmenbuchat veraenderungen firmen --von 2024-01-01 --bis 2024-01-31
firmenbuchat veraenderungen urkunden --von 2024-01-01 --bis 2024-01-31
firmenbuchat doctor
```

## Hilfe

```bash
firmenbuchat help
```

## Globale Optionen

- `-o, --output`: `table` (default), `json`, `raw`
- `-k, --api-key`: API-Key direkt übergeben
- `-e, --env-file`: Pfad zu `.env` Datei
- `--limit`: Anzahl Ergebnisse (Tabellen)
- `--offset`: Start-Offset

## Linting & Tests

```bash
ruff check .
ruff format .
pytest -q
```

## Projektstruktur

```
firmenbuch-aip/
├── src/firmenbuch_api_oesterreich/
│   ├── cli/
│   ├── services/
│   ├── models/
│   └── utils/
├── docs/
├── tests/
├── pyproject.toml
├── CHANGELOG.md
└── CONTRIBUTING.md
```
