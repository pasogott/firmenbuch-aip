# Auszug V2

Ruft einen Firmenbuchauszug ab.

---

## Namespace

```
Request:  ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugRequest
Response: ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugResponse
```

---

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|-----------|-----|:-------:|--------------|
| `FNR` | string | ✅ | Firmenbuchnummer mit Prüfbuchstabe (z.B. `5h`, `160573m`) |
| `STICHTAG` | date | ✅ | Stichtag im Format `YYYY-MM-DD` |
| `UMFANG` | string | ✅ | Art des Auszugs (siehe unten) |

### Umfang-Optionen

| Wert | Beschreibung |
|------|--------------|
| `Kurzinformation` | Nur grundlegende Informationen |
| `aktueller Auszug` | Vollständiger aktueller Stand |
| `historischer Auszug` | Mit historischen Daten |

---

## Request

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:aus="ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugRequest">
   <soap:Header/>
   <soap:Body>
      <aus:AUSZUG_V2_REQUEST>
         <aus:FNR>5h</aus:FNR>
         <aus:STICHTAG>2015-12-22</aus:STICHTAG>
         <aus:UMFANG>Kurzinformation</aus:UMFANG>
      </aus:AUSZUG_V2_REQUEST>
   </soap:Body>
</soap:Envelope>
```

---

## Response

### Attribute

| Attribut | Beschreibung |
|----------|--------------|
| `ABFRAGEZEITPUNKT` | Zeitstempel der Abfrage |
| `FNR` | Firmenbuchnummer (formatiert) |
| `PRUEFSUMME` | MD5-Prüfsumme des Auszugs |
| `STICHTAG` | Verwendeter Stichtag |
| `UMFANG` | Verwendeter Umfang |

### Beispiel

```xml
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
   <env:Header/>
   <env:Body>
      <ns6:AUSZUG_V2_RESPONSE 
         ns6:ABFRAGEZEITPUNKT="2025-01-16T14:03:33.146+01:00" 
         ns6:FNR="58468 h" 
         ns6:PRUEFSUMME="452407D2F7C4C4A3ED83D51DFB961E82" 
         ns6:STICHTAG="2020-11-10" 
         ns6:UMFANG="Kurzinformation"
         xmlns:ns6="ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugResponse">
         
         <ns6:FIRMA>
            <!-- Firmenbezeichnung -->
            <ns6:FI_DKZ02 ns6:AUFRECHT="true" ns6:VNR="001">
               <ns6:BEZEICHNUNG>EDV-Technik Dipl.-Ing. Went</ns6:BEZEICHNUNG>
               <ns6:BEZEICHNUNG>Gesellschaft m.b.H.</ns6:BEZEICHNUNG>
            </ns6:FI_DKZ02>
            
            <!-- Geschäftsanschrift -->
            <ns6:FI_DKZ03 ns6:AUFRECHT="true" ns6:VNR="034">
               <ns6:STELLE>Kärntner Straße 337</ns6:STELLE>
               <ns6:STAAT>AUT</ns6:STAAT>
               <ns6:PLZ>8054</ns6:PLZ>
               <ns6:ORT>Graz</ns6:ORT>
               <ns6:ZUSTELLBAR>true</ns6:ZUSTELLBAR>
            </ns6:FI_DKZ03>
            
            <!-- ... weitere Firmendaten ... -->
         </ns6:FIRMA>
      </ns6:AUSZUG_V2_RESPONSE>
   </env:Body>
</env:Envelope>
```

---

## Mögliche Fehler

| Fehler | Ursache |
|--------|---------|
| `Stichtag darf nicht in der Zukunft sein` | Der angegebene Stichtag liegt in der Zukunft |
| `Firmenbuchnummer ist ungültig!` | FNR-Format nicht korrekt |

---

## XSD-Schema

- Request: [`auszugRequest_v2.xsd`](../auszugRequest_v2.xsd)
- Response: [`auszugResponse_v2.xsd`](../auszugResponse_v2.xsd)
