# 📚 Dokumentation

Offizielle Schnittstellenbeschreibung der FBW-WebServices (High-Value Dataset) für das österreichische Firmenbuch.

---

## API-Dokumentation

| Dokument | Beschreibung |
|----------|--------------|
| [**Übersicht**](api/01-uebersicht.md) | Einführung, URLs, Authentifizierung |
| [**Auszug V2**](api/02-auszug.md) | Firmenbuchauszug abrufen |
| [**Firmensuche**](api/03-firmensuche.md) | Nach Firmen suchen |
| [**Urkundensuche**](api/04-urkundensuche.md) | Urkunden zu einer Firma suchen |
| [**Urkunde abrufen**](api/05-urkunde.md) | Einzelne Urkunde herunterladen |
| [**Veränderungen Firmen**](api/06-veraenderungen-firmen.md) | Firmenänderungen abfragen |
| [**Veränderungen Urkunden**](api/07-veraenderungen-urkunden.md) | Urkundenänderungen abfragen |
| [**Fehlerbehandlung**](api/08-fehlerbehandlung.md) | SOAP Faults & HTTP-Fehler |

---

## XSD-Schemas

### Request-Schemas

| Datei | Endpunkt |
|-------|----------|
| [`auszugRequest_v2.xsd`](auszugRequest_v2.xsd) | Auszug V2 |
| [`sucheFirmaRequest.xsd`](sucheFirmaRequest.xsd) | Firmensuche |
| [`sucheUrkundeRequest.xsd`](sucheUrkundeRequest.xsd) | Urkundensuche |
| [`urkundeRequest.xsd`](urkundeRequest.xsd) | Urkunde abrufen |
| [`veraenderungenFirmaRequest.xsd`](veraenderungenFirmaRequest.xsd) | Veränderungen Firmen |
| [`veraenderungenUrkundenRequest.xsd`](veraenderungenUrkundenRequest.xsd) | Veränderungen Urkunden |

### Response-Schemas

| Datei | Endpunkt |
|-------|----------|
| [`auszugResponse_v2.xsd`](auszugResponse_v2.xsd) | Auszug V2 |
| [`sucheFirmaResponse.xsd`](sucheFirmaResponse.xsd) | Firmensuche |
| [`sucheUrkundeResponse.xsd`](sucheUrkundeResponse.xsd) | Urkundensuche |
| [`urkundeResponse.xsd`](urkundeResponse.xsd) | Urkunde abrufen |
| [`veraenderungenFirmaResponse.xsd`](veraenderungenFirmaResponse.xsd) | Veränderungen Firmen |
| [`veraenderungenUrkundenResponse.xsd`](veraenderungenUrkundenResponse.xsd) | Veränderungen Urkunden |

---

## Offizielle Dokumente

| Datei | Beschreibung |
|-------|--------------|
| [`FBW-WebServices (HVD) Schnittstellenbeschreibung.pdf`](<FBW-WebServices (HVD) Schnittstellenbeschreibung.pdf>) | Original-PDF vom Firmenbuch-Team |

---

## Externe Links

- **WSDL:** https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl
- **Kontakt:** firmenbuch@brz.gv.at
