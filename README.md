# 🇦🇹 Firmenbuch CLI

Moderne CLI für das österreichische Firmenbuch - Zugriff auf die offiziellen High-Value Dataset WebServices.

```
$ fb suche firma "Software*" --rechtsform GES

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
uv pip install git+https://github.com/pasogott/firmenbuch-aip.git

# Oder mit pip
pip install git+https://github.com/pasogott/firmenbuch-aip.git

# Für Entwicklung
git clone https://github.com/pasogott/firmenbuch-aip.git
cd firmenbuch-aip
uv venv && source .venv/bin/activate
uv pip install -e .
```

---

## 🔑 API-Key einrichten

Du benötigst einen API-Key von JustizOnline. Siehe [API-Key erhalten](docs/API-KEY.md) für Details.

```bash
# API-Key sicher speichern (interaktiv)
fb config set-key

# Oder als Umgebungsvariable
export FIRMENBUCH_API_KEY="dein-key"

# Oder eigene .env Datei verwenden
fb --env-file /pfad/zu/deiner.env suche firma "Muster*"
```

---

## 💻 Verwendung

### Firmensuche

```bash
# Einfache Suche
fb suche firma "Musterfirma*"

# Mit Filtern
fb suche firma "Software" --rechtsform GES --gericht 007

# Als JSON ausgeben
fb suche firma "Test*" -o json
```

### Firmenbuchauszug

```bash
# Kurzinformation (Standard)
fb auszug 160573m

# Mit Stichtag
fb auszug 160573m --stichtag 2024-01-01

# Vollständiger Auszug als JSON
fb auszug 160573m -u "aktueller Auszug" -o json
```

### Urkunden

```bash
# Urkunden einer Firma suchen
fb suche urkunde 160573m

# Urkunde herunterladen
fb urkunde download "304188_0070711322495_000___000_30_7730290_PDF"

# Mit eigenem Dateinamen
fb urkunde download "..." -o jahresabschluss.pdf
```

### Veränderungen

```bash
# Firmenänderungen der letzten 7 Tage
fb veraenderungen firmen

# Für bestimmten Zeitraum
fb veraenderungen firmen --von 2024-01-01 --bis 2024-01-31

# Nur bestimmte Rechtsformen
fb veraenderungen firmen -r AG -g 007
```

### Konfiguration

```bash
# API-Key setzen
fb config set-key

# Aktuelle Config anzeigen
fb config show

# API-Infos und Hilfe
fb info

# Diagnose
fb doctor
```

---

## 📋 Alle Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `fb auszug FNR` | Firmenbuchauszug abrufen |
| `fb suche firma SUCHBEGRIFF` | Nach Firmen suchen |
| `fb suche urkunde FNR` | Urkunden einer Firma suchen |
| `fb urkunde download KEY` | Urkunde herunterladen |
| `fb urkunde info KEY` | Urkunden-Metadaten anzeigen |
| `fb veraenderungen firmen` | Firmenänderungen abfragen |
| `fb veraenderungen urkunden` | Urkundenänderungen abfragen |
| `fb config set-key` | API-Key speichern |
| `fb config show` | Konfiguration anzeigen |
| `fb doctor` | Setup-Diagnose |
| `fb info` | API-Infos und Hilfe |

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
