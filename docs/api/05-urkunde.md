# Urkunde abrufen

Lädt eine spezifische Urkunde herunter.

---

## Namespace

```
Request:  ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeRequest
Response: ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeResponse
```

---

## Parameter

| Parameter | Typ | Pflicht | Beschreibung |
|-----------|-----|:-------:|--------------|
| `KEY` | string | ✅ | Eindeutiger Schlüssel der Urkunde (aus [Urkundensuche](04-urkundensuche.md)) |

---

## Request

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:urk="ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeRequest">
   <soap:Header/>
   <soap:Body>
      <urk:URKUNDEREQUEST>
         <urk:KEY>304188_0070711322495_000___000_30_7730290_XML</urk:KEY>
      </urk:URKUNDEREQUEST>
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
      <ns7:URKUNDERESPONSE 
         ns7:STICHTAG="2015-12-23"
         xmlns:ns7="ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeResponse">
         
         <ns7:METADATEN>
            <ns7:KEY>304188_0070711322495_000___000_30_7730290_XML</ns7:KEY>
            <ns7:URKID>7730290</ns7:URKID>
            <ns7:FNR>304188 k</ns7:FNR>
            <ns7:AZ>007 071 Fr 22495/13 p</ns7:AZ>
            <ns7:DOKUMENTART>
               <ns7:CODE>48</ns7:CODE>
               <ns7:TEXT>Jahresabschluss</ns7:TEXT>
            </ns7:DOKUMENTART>
            <ns7:DOKUMENTENDATUM>2012-12-31</ns7:DOKUMENTENDATUM>
            <ns7:ZNR>000</ns7:ZNR>
            <ns7:PNR/>
            <ns7:FKEN/>
            <ns7:UNR>000</ns7:UNR>
            <ns7:DKZ>30</ns7:DKZ>
            <ns7:VNR>006</ns7:VNR>
            <ns7:BEMERKUNG/>
            <ns7:STICHTAG>2012-12-31</ns7:STICHTAG>
            <ns7:GKL>K</ns7:GKL>
            <ns7:VON>2013-11-13</ns7:VON>
            <ns7:OEFFENTLICH>true</ns7:OEFFENTLICH>
         </ns7:METADATEN>
         
         <ns7:DOKUMENT>
            <ns7:CONTENTTYPE>application/xml</ns7:CONTENTTYPE>
            <ns7:DATEIENDUNG>xml</ns7:DATEIENDUNG>
            <ns7:CONTENT>PD94bWwgdm... (Base64-kodiert)</ns7:CONTENT>
         </ns7:DOKUMENT>
         
      </ns7:URKUNDERESPONSE>
   </env:Body>
</env:Envelope>
```

### Metadaten-Felder

| Feld | Beschreibung |
|------|--------------|
| `KEY` | Eindeutiger Schlüssel |
| `URKID` | Urkunden-ID |
| `FNR` | Firmenbuchnummer |
| `AZ` | Aktenzeichen |
| `DOKUMENTART.CODE` | Dokumentart-Code |
| `DOKUMENTART.TEXT` | Dokumentart-Bezeichnung |
| `DOKUMENTENDATUM` | Datum des Dokuments |
| `STICHTAG` | Stichtag |
| `GKL` | Größenklasse (`K` = Klein, `M` = Mittel, `G` = Groß) |
| `VON` | Gültig ab Datum |
| `OEFFENTLICH` | Öffentlich einsehbar (`true`/`false`) |

### Dokument-Felder

| Feld | Beschreibung |
|------|--------------|
| `CONTENTTYPE` | MIME-Type (`application/pdf`, `application/xml`) |
| `DATEIENDUNG` | Dateiendung (`pdf`, `xml`) |
| `CONTENT` | **Base64-kodierter** Dateiinhalt |

---

## Verarbeitung des Dokuments

Der `CONTENT` ist Base64-kodiert und muss dekodiert werden:

### Python

```python
import base64

content_base64 = "PD94bWwgdm..."  # aus Response
content_bytes = base64.b64decode(content_base64)

# Als Datei speichern
with open("jahresabschluss.pdf", "wb") as f:
    f.write(content_bytes)
```

### Bash

```bash
echo "PD94bWwgdm..." | base64 -d > jahresabschluss.pdf
```

---

## Mögliche Fehler

| Fehler | Ursache |
|--------|---------|
| `Der Parameter "KEY" ist ungültig` | Ungültiger oder nicht existierender Urkunden-Key |

---

## XSD-Schema

- Request: [`urkundeRequest.xsd`](../urkundeRequest.xsd)
- Response: [`urkundeResponse.xsd`](../urkundeResponse.xsd)
