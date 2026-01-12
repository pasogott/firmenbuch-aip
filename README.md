# 🇦🇹 Firmenbuch CLI

Moderne CLI für das österreichische Firmenbuch - Zugriff auf die offiziellen High-Value Dataset WebServices.

```
$ firmenbuchat suche firma "Software*" --rechtsform GES

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ FNR        ┃ Name                              ┃ Sitz    ┃ Rechtsform               ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 160573m    │ Software Solutions GmbH           │ Wien    │ Gesellschaft m.b.H.      │
│ 234521a    │ Software & More GmbH              │ Graz    │ Gesellschaft m.b.H.      │
└────────────┴───────────────────────────────────┴─────────┴──────────────────────────┘
```

---

## ✨ Features

- 🎨 **Schöne Ausgabe** - Tabellen, Farben, Spinner mit Rich
- 🔐 **Sichere Key-Verwaltung** - API-Key wird sicher gespeichert
- 📊 **Flexible Formate** - Ausgabe als Tabelle, JSON oder Raw
- 💾 **Urkunden-Download** - PDFs und XMLs direkt herunterladen
- ⚡ **Schnell** - Async HTTP mit httpx

---

## 📖 Dokumentation

| Thema | Link |
|-------|------|
| **🔑 API-Key erhalten** | [docs/API-KEY.md](docs/API-KEY.md) |
| **API-Übersicht** | [docs/api/01-uebersicht.md](docs/api/01-uebersicht.md) |
| **Alle Endpunkte** | [docs/README.md](docs/README.md) |

---

## 🚀 Installation

```bash
# Mit uv (empfohlen)
uv add git+https://github.com/pasogott/firmenbuch-aip.git

# Homebrew (Tap)
brew tap pasogott/tap
brew install firmenbuchat

# Für Entwicklung
git clone https://github.com/pasogott/firmenbuch-aip.git
cd firmenbuch-aip
uv venv && source .venv/bin/activate
uv add --editable .
```

---

## 🔑 API-Key einrichten

Du benötigst einen API-Key von JustizOnline. Siehe [API-Key erhalten](docs/API-KEY.md) für Details.

```bash
# API-Key sicher speichern (interaktiv)
firmenbuchat config set-key

# Oder als Umgebungsvariable
export FIRMENBUCH_API_KEY="dein-key"

# Oder eigene .env Datei verwenden
firmenbuchat --env-file /pfad/zu/deiner.env suche firma "Muster*"
```

---

## 💻 Verwendung

### Firmensuche

```bash
# Einfache Suche
firmenbuchat suche firma "Musterfirma*"

# Mit Filtern
firmenbuchat suche firma "Software" --rechtsform GES --gericht 007

# Als JSON ausgeben
firmenbuchat suche firma "Test*" -o json
```

### Firmenbuchauszug

```bash
# Kurzinformation (Standard)
firmenbuchat auszug 160573m

# Mit Stichtag
firmenbuchat auszug 160573m --stichtag 2024-01-01

# Vollständiger Auszug als JSON
firmenbuchat auszug 160573m -u "aktueller Auszug" -o json
```

### Urkunden

```bash
# Urkunden einer Firma suchen
firmenbuchat suche urkunde 160573m

# Urkunde herunterladen
firmenbuchat urkunde download "304188_0070711322495_000___000_30_7730290_PDF"

# Mit eigenem Dateinamen
firmenbuchat urkunde download "..." -o jahresabschluss.pdf
```

### Veränderungen

```bash
# Firmenänderungen der letzten 7 Tage
firmenbuchat veraenderungen firmen

# Für bestimmten Zeitraum
firmenbuchat veraenderungen firmen --von 2024-01-01 --bis 2024-01-31

# Nur bestimmte Rechtsformen
firmenbuchat veraenderungen firmen -r AG -g 007
```

### Konfiguration

```bash
# API-Key setzen
firmenbuchat config set-key

# Aktuelle Config anzeigen
firmenbuchat config show

# API-Infos und Hilfe
firmenbuchat info

# Diagnose
firmenbuchat doctor
```

---

## 📋 Alle Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `firmenbuchat auszug FNR` | Firmenbuchauszug abrufen |
| `firmenbuchat suche firma SUCHBEGRIFF` | Nach Firmen suchen |
| `firmenbuchat suche urkunde FNR` | Urkunden einer Firma suchen |
| `firmenbuchat urkunde download KEY` | Urkunde herunterladen |
| `firmenbuchat urkunde info KEY` | Urkunden-Metadaten anzeigen |
| `firmenbuchat veraenderungen firmen` | Firmenänderungen abfragen |
| `firmenbuchat veraenderungen urkunden` | Urkundenänderungen abfragen |
| `firmenbuchat config set-key` | API-Key speichern |
| `firmenbuchat config show` | Konfiguration anzeigen |
| `firmenbuchat doctor` | Setup-Diagnose |
| `firmenbuchat info` | API-Infos und Hilfe |

### Globale Optionen

| Option | Beschreibung |
|--------|--------------|
| `-o, --output` | Ausgabeformat: `table` (Standard), `json`, `raw` |
| `-k, --api-key` | API-Key direkt übergeben |
| `-e, --env-file` | Pfad zu einer `.env` Datei |
| `--limit` | Anzahl Ergebnisse (Tabellen) |
| `--offset` | Start-Offset für Ergebnisse |
| `--help` | Hilfe anzeigen |

---

## ✅ Linting & Tests

```bash
# Dev-Tools installieren
uv add --dev ruff mypy pytest pytest-mock pre-commit

# Pre-commit Hooks aktivieren
pre-commit install

# Manuell ausführen
ruff check .
ruff format .
pytest -q
```

Weitere Infos: [CONTRIBUTING.md](CONTRIBUTING.md)

Release wird automatisch erzeugt, sobald ein Git-Tag `vX.Y.Z` gepusht wird.

## 📁 Projektstruktur

```
firmenbuch-aip/
├── src/firmenbuch_api_oesterreich/
│   ├── cli/                   # CLI mit Typer & Rich
│   │   ├── app.py
│   │   ├── console.py
│   │   └── commands/
│   ├── services/              # API-Services
│   ├── models/                # Pydantic-Models
│   └── utils/                 # Hilfsfunktionen
├── docs/
│   ├── API-KEY.md             # Wie man einen Key bekommt
│   ├── api/                   # API-Dokumentation
│   └── *.xsd                  # XML-Schemas
└── pyproject.toml
```

---

## 🔗 Links

| | |
|-|-|
| 🔑 **API-Key** | [Wie bekomme ich einen Key?](docs/API-KEY.md) |
| 📚 **Docs** | [API-Dokumentation](docs/README.md) |
| 🌐 **WSDL** | [justizonline.gv.at/.../fbw.wsdl](https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl) |
| 📧 **Kontakt** | firmenbuch@brz.gv.at |

---

## 🤝 Beitragen

Beiträge sind willkommen! Bitte öffne ein Issue oder einen Pull Request.

---

## 📄 Lizenz

MIT License - siehe [LICENSE](LICENSE) für Details.
