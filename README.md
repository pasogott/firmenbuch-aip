# Firmenbuch WebServices API

Diese API ermöglicht den Zugriff auf das österreichische Firmenbuch. Hier sind die verfügbaren Endpunkte:

## 1. Firmenbuchauszug abrufen (AUSZUG_V2)

- **Endpoint**: `/auszug/v2`
- **Beschreibung**: Ermöglicht das Abrufen eines Firmenbuchauszugs
- **Parameter**:
  - `FNR`: Firmenbuchnummer mit Prüfbuchstaben (z.B. "000187a") [**required**]
  - `STICHTAG`: Datum für den Auszug [**required**]
  - `UMFANG`: Art des Auszugs ("aktueller Auszug", "historischer Auszug") [**required**]

### Beispiel Request/Response

```xml
<!-- Request -->
<AUSZUG_V2_REQUEST xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugRequest">
    <FNR>160573m</FNR>
    <STICHTAG>2024-03-20</STICHTAG>
    <UMFANG>aktueller Auszug</UMFANG>
</AUSZUG_V2_REQUEST>

<!-- Response -->
<AUSZUG_V2_RESPONSE xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugResponse">
    <FNR>160573m</FNR>
    <STICHTAG>2024-03-20</STICHTAG>
    <UMFANG>aktueller Auszug</UMFANG>
    <!-- Weitere Details des Auszugs -->
</AUSZUG_V2_RESPONSE>
```

## 2. Firmensuche (SUCHE_FIRMA)

- **Endpoint**: `/suche/firma`
- **Beschreibung**: Sucht nach Firmen im Firmenbuch
- **Parameter**:
  - `FIRMENWORTLAUT`: Name der Firma (mit \* für Teilübereinstimmungen) [**required**]
  - `EXAKTESUCHE`: Boolean für exakte oder phonetische Suche [**required**]
  - `SUCHBEREICH`: Suchbereich (1-6) [**required**]
    - `1`: Eingetragene und gelöschte Firmen (keine Zweigniederlassungen)
    - `2`: Historische Firmenwortlaute (keine Zweigniederlassungen)
    - `3`: Keine Einschränkung
    - `4`: Eingetragene Firmenwortlaute (Prüfung Firmenausschließlichkeit)
    - `5`: Firmen in Arbeitsversion
    - `6`: Abgewiesene Neueintragungen
  - `GERICHT`: 3-stellige Gerichtsnummer [optional]
  - `RECHTSFORM`: 3-stellige Rechtsform (z.B. "GES") [optional]
  - `RECHTSEIGENSCHAFT`: Spezielle Rechtseigenschaft [optional]
  - `ORTNR`: Ortsnummer (5-stellig für Gemeinde, 3-stellig für Bezirk, 1-stellig für Bundesland) [optional]

### Beispiel Request/Response

```xml
<!-- Request -->
<SUCHEFIRMAREQUEST xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaRequest">
    <FIRMENWORTLAUT>Bundesrechen*</FIRMENWORTLAUT>
    <EXAKTESUCHE>false</EXAKTESUCHE>
    <SUCHBEREICH>1</SUCHBEREICH>
    <GERICHT>007</GERICHT>
    <RECHTSFORM>GES</RECHTSFORM>
</SUCHEFIRMAREQUEST>

<!-- Response -->
<SUCHEFIRMARESPONSE xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaResponse"
    REQUEST_FIRMENWORTLAUT="Bundesrechen*"
    REQUEST_EXAKTESUCHE="false"
    REQUEST_SUCHBEREICH="1">
    <ERGEBNIS>
        <FNR>160573m</FNR>
        <STATUS></STATUS>
        <NAME>Bundesrechenzentrum Gesellschaft</NAME>
        <NAME>mit beschränkter Haftung</NAME>
        <SITZ>Wien</SITZ>
        <RECHTSFORM>
            <CODE>GES</CODE>
            <TEXT>Gesellschaft mit beschränkter Haftung</TEXT>
        </RECHTSFORM>
        <RECHTSEIGENSCHAFT></RECHTSEIGENSCHAFT>
        <GERICHT>
            <CODE>007</CODE>
            <TEXT>Handelsgericht Wien</TEXT>
        </GERICHT>
    </ERGEBNIS>
</SUCHEFIRMARESPONSE>
```

## 3. Urkundensuche (SUCHE_URKUNDE)

- **Endpoint**: `/suche/urkunde`
- **Beschreibung**: Sucht nach Urkunden im Firmenbuch
- **Parameter**:
  - `FNR`: Firmenbuchnummer mit Prüfbuchstaben [**required** wenn AZ nicht angegeben]
  - `AZ`: Aktenzeichen [**required** wenn FNR nicht angegeben]
  - Hinweis: Entweder FNR ODER AZ muss angegeben werden

### Beispiel Request/Response

```xml
<!-- Request -->
<SUCHEURKUNDEREQUEST xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeRequest">
    <FNR>160573m</FNR>
</SUCHEURKUNDEREQUEST>

<!-- Response -->
<SUCHEURKUNDERESPONSE xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeResponse">
    <ERGEBNIS>
        <FNR>160573m</FNR>
        <AZ>007 61 Fr 2164/15 w</AZ>
        <DATUM>2015-06-15</DATUM>
        <TYP>Eintragung</TYP>
    </ERGEBNIS>
</SUCHEURKUNDERESPONSE>
```

## 4. Firmenveränderungen (VERAENDERUNGEN_FIRMA)

- **Endpoint**: `/veraenderungen/firma`
- **Beschreibung**: Ruft Firmenveränderungen für einen Zeitraum ab
- **Parameter**:
  - `VON`: Beginndatum [**required**]
  - `BIS`: Enddatum [**required**]
  - `GERICHT`: 3-stellige Gerichtsnummer [optional]
  - `RECHTSFORM`: 3-stellige Rechtsform [optional]
  - `ARTDERVERAENDERUNG`: Art der Veränderung (z.B. "FIRMENBEZEICHNUNG", "FIRMENSITZ", etc.) [optional]

### Beispiel Request/Response

```xml
<!-- Request -->
<VERAENDERUNGENFIRMAREQUEST xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaRequest">
    <VON>2024-03-01</VON>
    <BIS>2024-03-20</BIS>
    <GERICHT>007</GERICHT>
    <ARTDERVERAENDERUNG>FIRMENBEZEICHNUNG</ARTDERVERAENDERUNG>
</VERAENDERUNGENFIRMAREQUEST>

<!-- Response -->
<VERAENDERUNGENFIRMARESPONSE xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaResponse">
    <ERGEBNIS>
        <FNR>160573m</FNR>
        <DATUM>2024-03-15</DATUM>
        <ART>FIRMENBEZEICHNUNG</ART>
        <DETAILS>Änderung der Firmenbezeichnung</DETAILS>
    </ERGEBNIS>
</VERAENDERUNGENFIRMARESPONSE>
```

## 5. Urkundenveränderungen (VERAENDERUNGEN_URKUNDE)

- **Endpoint**: `/veraenderungen/urkunde`
- **Beschreibung**: Ruft Urkundenveränderungen ab

### Beispiel Request/Response

```xml
<!-- Request -->
<VERAENDERUNGENURKUNDEREQUEST xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenUrkundeRequest">
    <FNR>160573m</FNR>
</VERAENDERUNGENURKUNDEREQUEST>

<!-- Response -->
<VERAENDERUNGENURKUNDERESPONSE xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenUrkundeResponse">
    <ERGEBNIS>
        <FNR>160573m</FNR>
        <AZ>007 61 Fr 2164/15 w</AZ>
        <DATUM>2024-03-15</DATUM>
        <TYP>Änderung</TYP>
    </ERGEBNIS>
</VERAENDERUNGENURKUNDERESPONSE>
```

## 6. Urkundenabruf (URKUNDE)

- **Endpoint**: `/urkunde`
- **Beschreibung**: Ruft eine spezifische Urkunde ab

### Beispiel Request/Response

```xml
<!-- Request -->
<URKUNDEREQUEST xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeRequest">
    <FNR>160573m</FNR>
    <AZ>007 61 Fr 2164/15 w</AZ>
</URKUNDEREQUEST>

<!-- Response -->
<URKUNDERESPONSE xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeResponse">
    <FNR>160573m</FNR>
    <AZ>007 61 Fr 2164/15 w</AZ>
    <DATUM>2015-06-15</DATUM>
    <TYP>Eintragung</TYP>
    <INHALT>
        <!-- Inhalt der Urkunde -->
    </INHALT>
</URKUNDERESPONSE>
```

## Hinweise

- Alle Endpunkte erwarten XML-Requests und liefern XML-Responses
- Die API verwendet Namespaces für die verschiedenen Request/Response-Typen
- Die Versionierung der Endpunkte ist in den XSD-Dateien dokumentiert
- Für detaillierte Informationen zu den Response-Strukturen siehe die entsprechenden Response-XSD-Dateien

## Suchbereiche für Firmensuche

1. Eingetragene und gelöschte Firmen (keine Zweigniederlassungen)
2. Historische Firmenwortlaute (keine Zweigniederlassungen)
3. Keine Einschränkung
4. Eingetragene Firmenwortlaute (Prüfung Firmenausschließlichkeit)
5. Firmen in Arbeitsversion
6. Abgewiesene Neueintragungen

## Beispiel-Responses

### Firmensuche Response

```xml
<SUCHEFIRMARESPONSE
    xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaResponse"
    REQUEST_FIRMENWORTLAUT="Bundesrechen*"
    REQUEST_EXAKTESUCHE="false"
    REQUEST_SUCHBEREICH="1">
    <ERGEBNIS>
        <FNR>160573m</FNR>
        <STATUS></STATUS>
        <NAME>Bundesrechenzentrum Gesellschaft</NAME>
        <NAME>mit beschränkter Haftung</NAME>
        <SITZ>Wien</SITZ>
        <RECHTSFORM>
            <CODE>GES</CODE>
            <TEXT>Gesellschaft mit beschränkter Haftung</TEXT>
        </RECHTSFORM>
        <RECHTSEIGENSCHAFT></RECHTSEIGENSCHAFT>
        <GERICHT>
            <CODE>007</CODE>
            <TEXT>Handelsgericht Wien</TEXT>
        </GERICHT>
    </ERGEBNIS>
</SUCHEFIRMARESPONSE>
```

### Firmenbuchauszug Response

```xml
<AUSZUG_V2_RESPONSE
    xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugResponse">
    <FNR>160573m</FNR>
    <STICHTAG>2024-03-20</STICHTAG>
    <UMFANG>aktueller Auszug</UMFANG>
    <!-- Weitere Details des Auszugs -->
</AUSZUG_V2_RESPONSE>
```

### Urkundensuche Response

```xml
<SUCHEURKUNDERESPONSE
    xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeResponse">
    <ERGEBNIS>
        <FNR>160573m</FNR>
        <AZ>007 61 Fr 2164/15 w</AZ>
        <DATUM>2015-06-15</DATUM>
        <TYP>Eintragung</TYP>
    </ERGEBNIS>
</SUCHEURKUNDERESPONSE>
```

### Firmenveränderungen Response

```xml
<VERAENDERUNGENFIRMARESPONSE
    xmlns="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaResponse">
    <ERGEBNIS>
        <FNR>160573m</FNR>
        <DATUM>2024-03-15</DATUM>
        <ART>FIRMENBEZEICHNUNG</ART>
        <DETAILS>Änderung der Firmenbezeichnung</DETAILS>
    </ERGEBNIS>
</VERAENDERUNGENFIRMARESPONSE>
```

## CLI-Befehle

Die API kann auch über die Kommandozeile verwendet werden. Hier sind die verfügbaren Befehle:

### Firmenbuchauszug abrufen

```bash
python auszug.py auszug --api-key "dein-api-key" --fnr "000187a" --stichtag "2024-03-20" --umfang "Kurzinformation"
```

Parameter:

- `--api-key`: API-Schlüssel für die Authentifizierung [**required**]
- `--fnr`: Firmenbuchnummer mit Prüfbuchstaben (z.B. "000187a") [**required**]
- `--stichtag`: Datum für den Auszug im Format YYYY-MM-DD [**required**]
- `--umfang`: Art des Auszugs (Standard: "Kurzinformation")
  - `Kurzinformation`: Nur grundlegende Informationen
  - `aktueller Auszug`: Aktueller Stand
  - `historischer Auszug`: Mit historischen Daten

### Firmensuche

```bash
python auszug.py suche-firma --api-key "dein-api-key" --firmenwortlaut "Musterfirma*" --exaktesuche --suchbereich 1
```

Parameter:

- `--api-key`: API-Schlüssel für die Authentifizierung [**required**]
- `--firmenwortlaut`: Name der Firma (mit \* für Teilübereinstimmungen) [**required**]
- `--exaktesuche`: Flag für exakte Suche (ohne Flag: phonetische Suche) [**required**]
- `--suchbereich`: Suchbereich (1-6) [**required**]
- `--gericht`: 3-stellige Gerichtsnummer (optional)
- `--rechtsform`: 3-stellige Rechtsform (z.B. "GES") (optional)
- `--rechtseigenschaft`: Spezielle Rechtseigenschaft (optional)
- `--ortnr`: Ortsnummer (optional)
  - 5-stellig für Gemeinde
  - 3-stellig für Bezirk
  - 1-stellig für Bundesland

### Urkundensuche

```bash
python auszug.py suche-urkunde --api-key "dein-api-key" --fnr "000187a"
# oder
python auszug.py suche-urkunde --api-key "dein-api-key" --az "12345"
```

Parameter:

- `--api-key`: API-Schlüssel für die Authentifizierung [**required**]
- `--fnr`: Firmenbuchnummer mit Prüfbuchstaben (optional)
- `--az`: Aktenzeichen (optional)
  - Mindestens einer der beiden Parameter muss angegeben werden

### Firmenveränderungen abrufen

```bash
python auszug.py veraenderungen-firma --api-key "dein-api-key" --von "2024-01-01" --bis "2024-03-20"
```

Parameter:

- `--api-key`: API-Schlüssel für die Authentifizierung [**required**]
- `--von`: Beginndatum im Format YYYY-MM-DD [**required**]
- `--bis`: Enddatum im Format YYYY-MM-DD [**required**]
- `--gericht`: 3-stellige Gerichtsnummer (optional)
- `--rechtsform`: 3-stellige Rechtsform (optional)
- `--art-der-veraenderung`: Art der Veränderung (optional)
  - `NEU`: Neue Eintragungen
  - `AEND`: Änderungen
  - `LOESCH`: Löschungen

### Urkundenveränderungen abrufen

```bash
python auszug.py veraenderungen-urkunde --api-key "dein-api-key" --fnr "000187a"
```

Parameter:

- `--api-key`: API-Schlüssel für die Authentifizierung [**required**]
- `--fnr`: Firmenbuchnummer mit Prüfbuchstaben [**required**]

### Urkunde abrufen

```bash
python auszug.py urkunde --api-key "dein-api-key" --fnr "000187a" --az "12345"
```

Parameter:

- `--api-key`: API-Schlüssel für die Authentifizierung [**required**]
- `--fnr`: Firmenbuchnummer mit Prüfbuchstaben [**required**]
- `--az`: Aktenzeichen [**required**]

### Hilfe anzeigen

Für eine Übersicht aller verfügbaren Befehle:

```bash
python auszug.py --help
```

Für detaillierte Hilfe zu einem bestimmten Befehl:

```bash
python auszug.py auszug --help
python auszug.py suche-firma --help
# usw.
```

## Installation und Verwendung

### Installation mit uv

1. Installiere uv (falls noch nicht vorhanden):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Erstelle eine virtuelle Umgebung und aktiviere sie:

```bash
uv venv
source .venv/bin/activate  # Unter Linux/macOS
# oder
.venv\Scripts\activate  # Unter Windows
```

3. Installiere die Abhängigkeiten:

```bash
uv pip install -r requirements.txt
```

### Verwendung

Die API kann auf zwei Arten verwendet werden:

1. Als Python-Modul:

```python
from firmenbuch_api_oesterreich.services.auszug import get_auszug
from firmenbuch_api_oesterreich.models.request_models import AuszugRequest

request = AuszugRequest(
    fnr="000187a",
    stichtag="2024-03-20",
    umfang="Kurzinformation"
)
result = get_auszug("dein-api-key", request)
```

2. Über die Kommandozeile:

```bash
# Aktiviere die virtuelle Umgebung
source .venv/bin/activate  # Unter Linux/macOS
# oder
.venv\Scripts\activate  # Unter Windows

# Führe die Befehle aus
python -m firmenbuch_api_oesterreich.services.auszug auszug --api-key "dein-api-key" --fnr "000187a" --stichtag "2024-03-20"
```
