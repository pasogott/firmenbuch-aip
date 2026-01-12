# Fehlerbehandlung

Alle API-Fehler werden als SOAP Fault zurückgegeben.

---

## SOAP Fault Format

```xml
<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">
   <env:Header/>
   <env:Body>
      <env:Fault>
         <env:Code>
            <env:Value>env:Receiver</env:Value>
         </env:Code>
         <env:Reason>
            <env:Text xml:lang="en">Fehlermeldung hier</env:Text>
         </env:Reason>
      </env:Fault>
   </env:Body>
</env:Envelope>
```

---

## Fehler nach Endpunkt

### Auszug V2

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `Stichtag darf nicht in der Zukunft sein` | STICHTAG liegt nach heute | Datum auf heute oder früher setzen |
| `Firmenbuchnummer ist ungültig!` | FNR-Format falsch | Format prüfen: max. 6 Ziffern + Prüfbuchstabe |

### Firmensuche

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `Der Suchbereich ist ungültig!` | SUCHBEREICH nicht 1-6 | Wert zwischen 1 und 6 wählen |

### Urkundensuche

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `Firmenbuchnummer ist ungültig! (max. 6 Ziffern plus Prüfzeichen)` | FNR-Format falsch | Format prüfen |

### Urkunde abrufen

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `Der Parameter "KEY" ist ungültig` | KEY existiert nicht oder ist falsch | KEY aus Urkundensuche verwenden |

### Veränderungen (Firmen & Urkunden)

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `BIS-Datum darf nicht vor dem VON-Datum liegen` | BIS < VON | Datumsreihenfolge korrigieren |

---

## HTTP-Fehler

Zusätzlich zu SOAP Faults können HTTP-Fehler auftreten:

| HTTP Status | Bedeutung | Lösung |
|:-----------:|-----------|--------|
| `401` | Unauthorized | API-Key prüfen (Header `X-API-KEY`) |
| `403` | Forbidden | Berechtigungen prüfen |
| `500` | Internal Server Error | Später erneut versuchen |
| `503` | Service Unavailable | Service vorübergehend nicht verfügbar |

---

## Fehlerbehandlung in Code

### Python

```python
import requests
from xml.etree import ElementTree as ET

response = requests.post(url, data=soap_request, headers=headers)

# HTTP-Fehler prüfen
if response.status_code != 200:
    print(f"HTTP Error: {response.status_code}")
    return

# SOAP Fault prüfen
root = ET.fromstring(response.text)
fault = root.find('.//{http://www.w3.org/2003/05/soap-envelope}Fault')

if fault is not None:
    reason = fault.find('.//{http://www.w3.org/2003/05/soap-envelope}Text')
    print(f"SOAP Fault: {reason.text}")
    return

# Erfolgreiche Response verarbeiten
# ...
```

### JavaScript/TypeScript

```typescript
async function callApi(soapRequest: string): Promise<any> {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/soap+xml;charset=UTF-8',
      'X-API-KEY': apiKey
    },
    body: soapRequest
  });

  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status}`);
  }

  const text = await response.text();
  
  // SOAP Fault prüfen
  if (text.includes('<env:Fault>')) {
    const match = text.match(/<env:Text[^>]*>([^<]+)<\/env:Text>/);
    throw new Error(`SOAP Fault: ${match?.[1] ?? 'Unknown error'}`);
  }

  return text;
}
```

---

## Best Practices

1. **Immer HTTP-Status prüfen** vor dem Parsen der Response
2. **SOAP Faults explizit behandeln** - nicht als XML-Parsing-Fehler durchfallen lassen
3. **Retry-Logik implementieren** für temporäre Fehler (5xx)
4. **Logging** aller Fehler für Debugging
5. **Timeouts setzen** um hängende Requests zu vermeiden
