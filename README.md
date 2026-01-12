# 🇦🇹 Firmenbuch API Österreich

Python-Client für die offiziellen FBW-WebServices des österreichischen Firmenbuchs (High-Value Dataset).

---

## 📖 Dokumentation

| Thema | Link |
|-------|------|
| **API-Übersicht** | [docs/api/01-uebersicht.md](docs/api/01-uebersicht.md) |
| **Alle Endpunkte** | [docs/README.md](docs/README.md) |
| **XSD-Schemas** | [docs/](docs/) |

### Schnellzugriff API-Endpunkte

| Endpunkt | Beschreibung | Docs |
|----------|--------------|------|
| Auszug V2 | Firmenbuchauszug abrufen | [→](docs/api/02-auszug.md) |
| Firmensuche | Nach Firmen suchen | [→](docs/api/03-firmensuche.md) |
| Urkundensuche | Urkunden einer Firma | [→](docs/api/04-urkundensuche.md) |
| Urkunde | Dokument herunterladen | [→](docs/api/05-urkunde.md) |
| Veränderungen Firmen | Änderungs-Feed | [→](docs/api/06-veraenderungen-firmen.md) |
| Veränderungen Urkunden | Urkunden-Feed | [→](docs/api/07-veraenderungen-urkunden.md) |

---

## 🚀 Installation

```bash
# Mit uv (empfohlen)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Oder mit pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 💻 Verwendung

### Als Python-Modul

```python
from firmenbuch_api_oesterreich.services.auszug import get_auszug
from firmenbuch_api_oesterreich.models.request_models import AuszugRequest

request = AuszugRequest(
    fnr="160573m",
    stichtag="2024-03-20",
    umfang="Kurzinformation"
)
result = get_auszug("dein-api-key", request)
```

### CLI

```bash
# Firmenbuchauszug abrufen
python auszug.py auszug \
  --api-key "dein-api-key" \
  --fnr "160573m" \
  --stichtag "2024-03-20" \
  --umfang "Kurzinformation"

# Firmensuche
python auszug.py suche-firma \
  --api-key "dein-api-key" \
  --firmenwortlaut "Bundesrechen*" \
  --suchbereich 1

# Hilfe anzeigen
python auszug.py --help
```

---

## 🔑 Authentifizierung

Du benötigst einen API-Key von JustizOnline. Dieser wird als HTTP-Header mitgeschickt:

```http
X-API-KEY: dein-api-key
Content-Type: application/soap+xml;charset=UTF-8
```

**Basis-URL:** `https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws`

---

## 📋 CLI-Befehle

### Firmenbuchauszug

```bash
python auszug.py auszug --api-key KEY --fnr FNR --stichtag DATUM [--umfang UMFANG]
```

| Parameter | Beschreibung |
|-----------|--------------|
| `--fnr` | Firmenbuchnummer mit Prüfbuchstabe (z.B. `160573m`) |
| `--stichtag` | Datum im Format `YYYY-MM-DD` |
| `--umfang` | `Kurzinformation`, `aktueller Auszug`, `historischer Auszug` |

### Firmensuche

```bash
python auszug.py suche-firma --api-key KEY --firmenwortlaut TEXT --suchbereich N [OPTIONS]
```

| Parameter | Beschreibung |
|-----------|--------------|
| `--firmenwortlaut` | Suchbegriff (mit `*` für Wildcards) |
| `--exaktesuche` | Flag für exakte Suche |
| `--suchbereich` | 1-6 (siehe [Dokumentation](docs/api/03-firmensuche.md)) |
| `--gericht` | 3-stellige Gerichtsnummer |
| `--rechtsform` | Rechtsform-Code (z.B. `GES`, `AG`) |

### Urkundensuche

```bash
python auszug.py suche-urkunde --api-key KEY --fnr FNR
```

### Urkunde abrufen

```bash
python auszug.py urkunde --api-key KEY --key URKUNDEN_KEY
```

### Veränderungen

```bash
# Firmenänderungen
python auszug.py veraenderungen-firma --api-key KEY --von DATUM --bis DATUM

# Urkundenänderungen  
python auszug.py veraenderungen-urkunde --api-key KEY --von DATUM --bis DATUM
```

---

## 📁 Projektstruktur

```
firmenbuch-aip/
├── README.md
├── docs/
│   ├── README.md              # Dokumentations-Index
│   ├── api/
│   │   ├── 01-uebersicht.md
│   │   ├── 02-auszug.md
│   │   ├── 03-firmensuche.md
│   │   ├── 04-urkundensuche.md
│   │   ├── 05-urkunde.md
│   │   ├── 06-veraenderungen-firmen.md
│   │   ├── 07-veraenderungen-urkunden.md
│   │   └── 08-fehlerbehandlung.md
│   ├── *.xsd                  # XML-Schemas
│   └── *.pdf                  # Original-Dokumentation
├── src/
│   └── firmenbuch_api_oesterreich/
├── pyproject.toml
└── uv.lock
```

---

## 🔗 Links

- **WSDL:** https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl
- **API-Dokumentation:** [docs/](docs/)
- **Kontakt Firmenbuch-Team:** firmenbuch@brz.gv.at

---

## 📄 Lizenz

Siehe [LICENSE](LICENSE) für Details.
