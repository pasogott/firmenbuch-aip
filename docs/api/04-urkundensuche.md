# Urkundensuche

Sucht Urkunden zu einer bestimmten Firma.

---

## Namespace

```
Request:  ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeRequest
Response: ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeResponse
```

---

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|-----------|-----|:-------:|--------------|
| `FNR` | string | ✅ | Firmenbuchnummer mit Prüfbuchstabe |

---

## Request

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:suc="ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeRequest">
   <soap:Header/>
   <soap:Body>
      <suc:SUCHEURKUNDEREQUEST>
         <suc:FNR>629 a</suc:FNR>
      </suc:SUCHEURKUNDEREQUEST>
   </soap:Body>
</soap:Envelope>
```

---

## Response

### Beispiel

```xml
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
   <env:Header/>
   <env:Body>
      <ns15:SUCHEURKUNDERESPONSE 
         ns15:REQUEST_FNR="629 a"
         xmlns:ns15="ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeResponse">
         
         <ns15:ERGEBNIS>
            <ns15:KEY>000629_6380470600057_000___000_30_1310866_PDF</ns15:KEY>
            <ns15:FNR>629 a</ns15:FNR>
            <ns15:AZ>638 047 Fr 57/06 i</ns15:AZ>
            <ns15:DOKUMENTART>
               <ns15:CODE>48</ns15:CODE>
               <ns15:TEXT>Jahresabschluss</ns15:TEXT>
            </ns15:DOKUMENTART>
            <ns15:CONTENTTYPE>application/pdf</ns15:CONTENTTYPE>
            <ns15:DATEIENDUNG>pdf</ns15:DATEIENDUNG>
            <ns15:GROESSE>19343</ns15:GROESSE>
            <ns15:BEMERKUNG>31.3.2004</ns15:BEMERKUNG>
            <ns15:STICHTAG>2004-03-31</ns15:STICHTAG>
            <ns15:GKL/>
            <ns15:VNR>011</ns15:VNR>
            <ns15:EINGEREICHT>2006-01-02</ns15:EINGEREICHT>
         </ns15:ERGEBNIS>
         
         <!-- ... weitere Urkunden ... -->
         
      </ns15:SUCHEURKUNDERESPONSE>
   </env:Body>
</env:Envelope>
```

### Ergebnis-Felder

| Feld | Beschreibung |
|------|--------------|
| `KEY` | Eindeutiger Schlüssel zum Abrufen der Urkunde |
| `FNR` | Firmenbuchnummer |
| `AZ` | Aktenzeichen |
| `DOKUMENTART.CODE` | Dokumentart-Code |
| `DOKUMENTART.TEXT` | Dokumentart-Bezeichnung |
| `CONTENTTYPE` | MIME-Type (z.B. `application/pdf`) |
| `DATEIENDUNG` | Dateiendung (z.B. `pdf`, `xml`) |
| `GROESSE` | Dateigröße in Bytes |
| `BEMERKUNG` | Zusätzliche Bemerkung |
| `STICHTAG` | Stichtag der Urkunde |
| `GKL` | Größenklasse |
| `VNR` | Versionsnummer |
| `EINGEREICHT` | Einreichungsdatum |

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

## Mögliche Fehler

| Fehler | Ursache |
|--------|---------|
| `Firmenbuchnummer ist ungültig! (max. 6 Ziffern plus Prüfzeichen)` | Ungültige FNR |

---

## XSD-Schema

- Request: [`sucheUrkundeRequest.xsd`](../sucheUrkundeRequest.xsd)
- Response: [`sucheUrkundeResponse.xsd`](../sucheUrkundeResponse.xsd)
