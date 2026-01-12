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

## Befehle

```bash
# Hilfe & Meta
firmenbuchat help
firmenbuchat version
firmenbuchat info

# Konfiguration
firmenbuchat config set-key [API_KEY]
firmenbuchat config show
firmenbuchat config path
firmenbuchat config delete [--force]

# Firmenbuchauszug
firmenbuchat auszug <FNR> [--stichtag YYYY-MM-DD] [--umfang "Kurzinformation"|"aktueller Auszug"|"historischer Auszug"]

# Firmensuche
firmenbuchat suche firma <SUCHBEGRIFF> [--bereich 1-6] [--exakt] [--gericht 007] [--rechtsform GES]

# Urkundensuche
firmenbuchat suche urkunde <FNR> [--output table|json|raw] [--limit 50] [--offset 0]

# Urkunden
firmenbuchat urkunde info <URKUNDEN_KEY>
firmenbuchat urkunde download <URKUNDEN_KEY> [--output PATH]

# Veränderungen
firmenbuchat veraenderungen firmen [--von YYYY-MM-DD] [--bis YYYY-MM-DD] [--gericht 007] [--rechtsform GES]
firmenbuchat veraenderungen urkunden [--von YYYY-MM-DD] [--bis YYYY-MM-DD]

# Diagnose
firmenbuchat doctor [--env-file PATH]
```

## Globale Optionen

- `-o, --output`: `table` (default), `json`, `raw`
- `-k, --api-key`: API-Key direkt übergeben
- `-e, --env-file`: Pfad zu `.env` Datei
- `--limit`: Anzahl Ergebnisse (Tabellen)
- `--offset`: Start-Offset

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
