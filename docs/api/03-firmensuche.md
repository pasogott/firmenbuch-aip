# Firmensuche

Sucht nach Firmen im Firmenbuch.

---

## Namespace

```
Request:  ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaRequest
Response: ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaResponse
```

---

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|-----------|-----|:-------:|--------------|
| `FIRMENWORTLAUT` | string | ✅ | Suchbegriff (Wildcards mit `*`) |
| `EXAKTESUCHE` | boolean | ✅ | `true` = exakt, `false` = phonetisch |
| `SUCHBEREICH` | integer | ✅ | Suchbereich 1-6 (siehe unten) |
| `GERICHT` | string | ❌ | 3-stellige Gerichtsnummer (z.B. `007`) |
| `RECHTSFORM` | string | ❌ | Rechtsform-Code (z.B. `GES`, `AG`, `OG`) |
| `RECHTSEIGENSCHAFT` | string | ❌ | Spezielle Rechtseigenschaft |
| `ORTNR` | string | ❌ | Ortsnummer (siehe unten) |

### Suchbereiche

| Wert | Beschreibung |
|:----:|--------------|
| `1` | Eingetragene und gelöschte Firmen (keine Zweigniederlassungen) |
| `2` | Historische Firmenwortlaute (keine Zweigniederlassungen) |
| `3` | Keine Einschränkung |
| `4` | Eingetragene Firmenwortlaute (Prüfung Firmenausschließlichkeit) |
| `5` | Firmen in Arbeitsversion |
| `6` | Abgewiesene Neueintragungen |

### Ortsnummer-Format

| Länge | Bedeutung |
|:-----:|-----------|
| 5-stellig | Gemeinde |
| 3-stellig | Bezirk |
| 1-stellig | Bundesland |

---

## Request

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:suc="ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaRequest">
   <soap:Header/>
   <soap:Body>
      <suc:SUCHEFIRMAREQUEST>
         <suc:FIRMENWORTLAUT>mayer</suc:FIRMENWORTLAUT>
         <suc:EXAKTESUCHE>false</suc:EXAKTESUCHE>
         <suc:SUCHBEREICH>1</suc:SUCHBEREICH>
         <suc:GERICHT></suc:GERICHT>
         <suc:RECHTSFORM></suc:RECHTSFORM>
         <suc:RECHTSEIGENSCHAFT></suc:RECHTSEIGENSCHAFT>
         <suc:ORTNR></suc:ORTNR>
      </suc:SUCHEFIRMAREQUEST>
   </soap:Body>
</soap:Envelope>
```

### Beispiele für Suchbegriffe

| Suchbegriff | Findet |
|-------------|--------|
| `mayer` | Alle Firmen mit "mayer" (phonetisch auch "maier", "meier" etc.) |
| `Bundesrechen*` | Alle Firmen die mit "Bundesrechen" beginnen |
| `*software*` | Alle Firmen die "software" enthalten |

---

## Response

### Attribute

| Attribut | Beschreibung |
|----------|--------------|
| `REQUEST_FIRMENWORTLAUT` | Verwendeter Suchbegriff |
| `REQUEST_EXAKTESUCHE` | Verwendete Suchart |
| `REQUEST_SUCHBEREICH` | Verwendeter Suchbereich |
| `REQUEST_GERICHT` | Verwendetes Gericht (falls angegeben) |
| `REQUEST_RECHTSFORM` | Verwendete Rechtsform (falls angegeben) |

### Beispiel

```xml
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
   <env:Header/>
   <env:Body>
      <ns13:SUCHEFIRMARESPONSE 
         ns13:REQUEST_EXAKTESUCHE="false" 
         ns13:REQUEST_FIRMENWORTLAUT="mayer" 
         ns13:REQUEST_SUCHBEREICH="1"
         xmlns:ns13="ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaResponse">
         
         <ns13:ERGEBNIS>
            <ns13:FNR>145733p</ns13:FNR>
            <ns13:STATUS/>
            <ns13:NAME>"A &amp; S" Mayer OEG</ns13:NAME>
            <ns13:SITZ>Wien</ns13:SITZ>
            <ns13:RECHTSFORM>
               <ns13:CODE>OG</ns13:CODE>
               <ns13:TEXT>Offene Gesellschaft</ns13:TEXT>
            </ns13:RECHTSFORM>
            <ns13:RECHTSEIGENSCHAFT/>
            <ns13:GERICHT>
               <ns13:CODE>007</ns13:CODE>
               <ns13:TEXT>Handelsgericht Wien</ns13:TEXT>
            </ns13:GERICHT>
         </ns13:ERGEBNIS>
         
         <!-- ... weitere Ergebnisse ... -->
         
      </ns13:SUCHEFIRMARESPONSE>
   </env:Body>
</env:Envelope>
```

### Ergebnis-Felder

| Feld | Beschreibung |
|------|--------------|
| `FNR` | Firmenbuchnummer |
| `STATUS` | Status der Firma (leer = aktiv) |
| `NAME` | Firmenname |
| `SITZ` | Firmensitz |
| `RECHTSFORM.CODE` | Rechtsform-Code |
| `RECHTSFORM.TEXT` | Rechtsform-Bezeichnung |
| `GERICHT.CODE` | Gerichts-Code |
| `GERICHT.TEXT` | Gerichts-Bezeichnung |

---

## Mögliche Fehler

| Fehler | Ursache |
|--------|---------|
| `Der Suchbereich ist ungültig!` | Ungültiger Wert für SUCHBEREICH (muss 1-6 sein) |

---

## XSD-Schema

- Request: [`sucheFirmaRequest.xsd`](../sucheFirmaRequest.xsd)
- Response: [`sucheFirmaResponse.xsd`](../sucheFirmaResponse.xsd)
