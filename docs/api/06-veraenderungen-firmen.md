# Veränderungen Firmen

Ruft Firmenänderungen in einem bestimmten Zeitraum ab.

---

## Namespace

```
Request:  ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaRequest
Response: ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaResponse
```

---

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|-----------|-----|:-------:|--------------|
| `VON` | date | ✅ | Startdatum (`YYYY-MM-DD`) |
| `BIS` | date | ✅ | Enddatum (`YYYY-MM-DD`) |
| `GERICHT` | string | ❌ | 3-stellige Gerichtsnummer (z.B. `007`) |
| `RECHTSFORM` | string | ❌ | Rechtsform-Code (z.B. `AG`, `GES`) |

---

## Request

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:ver="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaRequest">
   <soap:Header/>
   <soap:Body>
      <ver:VERAENDERUNGENFIRMAREQUEST>
         <ver:VON>2014-11-25</ver:VON>
         <ver:BIS>2014-11-25</ver:BIS>
         <!--Optional:-->
         <ver:GERICHT>007</ver:GERICHT>
         <!--Optional:-->
         <ver:RECHTSFORM>AG</ver:RECHTSFORM>
      </ver:VERAENDERUNGENFIRMAREQUEST>
   </soap:Body>
</soap:Envelope>
```

---

## Response

### Attribute

| Attribut | Beschreibung |
|----------|--------------|
| `VON` | Verwendetes Startdatum |
| `BIS` | Verwendetes Enddatum |
| `GERICHT` | Verwendetes Gericht (falls angegeben) |
| `RECHTSFORM` | Verwendete Rechtsform (falls angegeben) |

### Beispiel

```xml
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
   <env:Header/>
   <env:Body>
      <ns9:VERAENDERUNGENFIRMARESPONSE 
         ns9:BIS="2014-11-25" 
         ns9:GERICHT="007" 
         ns9:RECHTSFORM="AG" 
         ns9:VON="2014-11-25"
         xmlns:ns9="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaResponse">
         
         <ns9:VERAENDERUNG>
            <ns9:FNR>73589 w</ns9:FNR>
            <ns9:VNR>032</ns9:VNR>
            <ns9:VOLLZUGSDATUM>2014-11-25</ns9:VOLLZUGSDATUM>
            <ns9:ARTDERVERAENDERUNG>Änderung</ns9:ARTDERVERAENDERUNG>
         </ns9:VERAENDERUNG>
         
         <ns9:VERAENDERUNG>
            <ns9:FNR>257770 z</ns9:FNR>
            <ns9:VNR>012</ns9:VNR>
            <ns9:VOLLZUGSDATUM>2014-11-25</ns9:VOLLZUGSDATUM>
            <ns9:ARTDERVERAENDERUNG>Änderung</ns9:ARTDERVERAENDERUNG>
         </ns9:VERAENDERUNG>
         
         <ns9:VERAENDERUNG>
            <ns9:FNR>200922 z</ns9:FNR>
            <ns9:VNR>025</ns9:VNR>
            <ns9:VOLLZUGSDATUM>2014-11-25</ns9:VOLLZUGSDATUM>
            <ns9:ARTDERVERAENDERUNG>Änderung</ns9:ARTDERVERAENDERUNG>
         </ns9:VERAENDERUNG>
         
         <!-- ... weitere Veränderungen ... -->
         
      </ns9:VERAENDERUNGENFIRMARESPONSE>
   </env:Body>
</env:Envelope>
```

### Veränderungs-Felder

| Feld | Beschreibung |
|------|--------------|
| `FNR` | Firmenbuchnummer |
| `VNR` | Versionsnummer der Eintragung |
| `VOLLZUGSDATUM` | Datum der Änderung |
| `ARTDERVERAENDERUNG` | Art der Veränderung |

### Arten der Veränderung

| Wert | Beschreibung |
|------|--------------|
| `Änderung` | Bestehende Daten wurden geändert |
| `Neueintragung` | Neue Firma eingetragen |
| `Löschung` | Firma wurde gelöscht |

---

## Anwendungsfall

Dieser Endpunkt ist ideal für:

- **Monitoring**: Änderungen bei bestimmten Gerichten verfolgen
- **Daten-Synchronisation**: Lokale Datenbank aktuell halten
- **Compliance**: Änderungen bei Geschäftspartnern überwachen

---

## Mögliche Fehler

| Fehler | Ursache |
|--------|---------|
| `BIS-Datum darf nicht vor dem VON-Datum liegen` | Ungültiger Datumsbereich |

---

## XSD-Schema

- Request: [`veraenderungenFirmaRequest.xsd`](../veraenderungenFirmaRequest.xsd)
- Response: [`veraenderungenFirmaResponse.xsd`](../veraenderungenFirmaResponse.xsd)
