# Veränderungen Urkunden

Ruft Urkundenänderungen in einem bestimmten Zeitraum ab.

---

## Namespace

```
Request:  ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenUrkundeRequest
Response: ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenUrkundeResponse
```

---

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|-----------|-----|:-------:|--------------|
| `VON` | date | ✅ | Startdatum (`YYYY-MM-DD`) |
| `BIS` | date | ✅ | Enddatum (`YYYY-MM-DD`) |

---

## Request

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:ver="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenUrkundeRequest">
   <soap:Header/>
   <soap:Body>
      <ver:VERAENDERUNGENURKUNDEREQUEST>
         <ver:VON>2014-11-25</ver:VON>
         <ver:BIS>2014-11-25</ver:BIS>
      </ver:VERAENDERUNGENURKUNDEREQUEST>
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

### Beispiel

```xml
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
   <env:Header/>
   <env:Body>
      <ns11:VERAENDERUNGENURKUNDERESPONSE 
         ns11:BIS="2014-11-25" 
         ns11:VON="2014-11-25"
         xmlns:ns11="ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenUrkundeResponse">
         
         <ns11:VERAENDERUNG>
            <ns11:KEY>425421_0070731417628_000___001__9637795_PDF</ns11:KEY>
            <ns11:DOKUMENTART>
               <ns11:CODE>42</ns11:CODE>
               <ns11:TEXT>Gesellschaftsvertrag</ns11:TEXT>
            </ns11:DOKUMENTART>
            <ns11:VOLLZUGSDATUM>2014-11-25</ns11:VOLLZUGSDATUM>
            <ns11:CONTENTTYPE>application/pdf</ns11:CONTENTTYPE>
            <ns11:DATEIENDUNG>pdf</ns11:DATEIENDUNG>
         </ns11:VERAENDERUNG>
         
         <ns11:VERAENDERUNG>
            <ns11:KEY>425311_0070731417585_000_A_GF_000__9630769_PDF</ns11:KEY>
            <ns11:DOKUMENTART>
               <ns11:CODE>61</ns11:CODE>
               <ns11:TEXT>Musterzeichnung</ns11:TEXT>
            </ns11:DOKUMENTART>
            <ns11:VOLLZUGSDATUM>2014-11-25</ns11:VOLLZUGSDATUM>
            <ns11:CONTENTTYPE>application/pdf</ns11:CONTENTTYPE>
            <ns11:DATEIENDUNG>pdf</ns11:DATEIENDUNG>
         </ns11:VERAENDERUNG>
         
         <!-- ... weitere Veränderungen ... -->
         
      </ns11:VERAENDERUNGENURKUNDERESPONSE>
   </env:Body>
</env:Envelope>
```

### Veränderungs-Felder

| Feld | Beschreibung |
|------|--------------|
| `KEY` | Eindeutiger Schlüssel zum Abrufen der Urkunde |
| `DOKUMENTART.CODE` | Dokumentart-Code |
| `DOKUMENTART.TEXT` | Dokumentart-Bezeichnung |
| `VOLLZUGSDATUM` | Datum der Änderung |
| `CONTENTTYPE` | MIME-Type der Urkunde |
| `DATEIENDUNG` | Dateiendung |

### Dokumentarten (Auswahl)

| Code | Beschreibung |
|:----:|--------------|
| `42` | Gesellschaftsvertrag |
| `48` | Jahresabschluss |
| `61` | Musterzeichnung |

---

## Nächster Schritt

Verwende den `KEY` aus dem Ergebnis, um die Urkunde mit dem [Urkunde-Endpunkt](05-urkunde.md) herunterzuladen.

---

## Anwendungsfall

Dieser Endpunkt ist ideal für:

- **Jahresabschluss-Monitoring**: Neue Jahresabschlüsse automatisch erkennen
- **Dokumenten-Archivierung**: Neue Urkunden automatisch herunterladen
- **Due Diligence**: Änderungen bei Zielunternehmen verfolgen

---

## Mögliche Fehler

| Fehler | Ursache |
|--------|---------|
| `BIS-Datum darf nicht vor dem VON-Datum liegen` | Ungültiger Datumsbereich |

---

## XSD-Schema

- Request: [`veraenderungenUrkundenRequest.xsd`](../veraenderungenUrkundenRequest.xsd)
- Response: [`veraenderungenUrkundenResponse.xsd`](../veraenderungenUrkundenResponse.xsd)
