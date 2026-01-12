# API Übersicht

> **Version:** 1.2 | **Stand:** 24.04.2025 | **Kontakt:** firmenbuch@brz.gv.at

Die FBW-WebServices ermöglichen den programmatischen Zugriff auf das österreichische Firmenbuch. Es handelt sich um einen **High-Value Dataset (HVD)** der über SOAP-Schnittstellen bereitgestellt wird.

---

## Basis-URL

```
https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws
```

## WSDL

```
https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl
```

---

## Verfügbare Endpunkte

| Endpunkt | Beschreibung | Dokumentation |
|----------|--------------|---------------|
| **Auszug V2** | Firmenbuchauszug abrufen | [→ Details](02-auszug.md) |
| **Firmensuche** | Nach Firmen suchen | [→ Details](03-firmensuche.md) |
| **Urkundensuche** | Urkunden zu einer Firma suchen | [→ Details](04-urkundensuche.md) |
| **Urkunde abrufen** | Einzelne Urkunde herunterladen | [→ Details](05-urkunde.md) |
| **Veränderungen Firmen** | Firmenänderungen in Zeitraum | [→ Details](06-veraenderungen-firmen.md) |
| **Veränderungen Urkunden** | Urkundenänderungen in Zeitraum | [→ Details](07-veraenderungen-urkunden.md) |

---

## Authentifizierung

Für jeden API-Aufruf sind folgende HTTP-Header erforderlich:

```http
X-API-KEY: <dein-api-key>
Content-Type: application/soap+xml;charset=UTF-8
```

> 💡 Den API-Key erhältst du von JustizOnline.

---

## SOAP-Version

Es wird **SOAP 1.2** verwendet. Alle Requests verwenden den Namespace:

```xml
xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
```

---

## Fehlerbehandlung

Fehler werden als SOAP Fault zurückgegeben:

```xml
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
   <env:Body>
      <env:Fault>
         <env:Code>
            <env:Value>env:Receiver</env:Value>
         </env:Code>
         <env:Reason>
            <env:Text xml:lang="en">Fehlermeldung</env:Text>
         </env:Reason>
      </env:Fault>
   </env:Body>
</env:Envelope>
```

Siehe [Fehlerbehandlung](08-fehlerbehandlung.md) für eine vollständige Liste.

---

## Änderungsverzeichnis

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.0 | 16.01.2025 | Ersterstellung |
| 1.1 | 20.03.2025 | Erweiterung um Kapitel "HEADER", SOAP 1.1 entfernt |
| 1.2 | 24.04.2025 | Anpassungen im Kapitel "HEADER" |
