# 🔑 API-Key erhalten

Um die Firmenbuch-API nutzen zu können, benötigst du einen API-Key von JustizOnline.

---

## Schritt-für-Schritt Anleitung

### 1. JustizOnline API-Portal aufrufen

Gehe zur offiziellen Registrierungsseite:

👉 **[justiz.gv.at API-Registrierung](https://www.justiz.gv.at/service/datenschutz/justizonline-api.2c94848b8b511b7a018c6a8e30e1045c.de.html)**

### 2. Registrierung

- Fülle das Registrierungsformular aus
- Gib deine Kontaktdaten und den Verwendungszweck an
- Die Firmenbuch-API ist Teil der **High-Value Datasets (HVD)**

### 3. API-Key erhalten

Nach erfolgreicher Registrierung erhältst du:

- Einen **API-Key** (lange alphanumerische Zeichenkette)
- Zugang zur WSDL-Dokumentation
- Informationen zu Rate-Limits

### 4. API-Key in der CLI speichern

```bash
# Interaktiv (empfohlen - Key wird nicht im Terminal angezeigt)
fb config set-key

# Oder direkt
fb config set-key "dein-api-key-hier"

# Prüfen ob gespeichert
fb config show
```

### 5. Alternativ: Umgebungsvariable oder .env Datei

Du kannst den Key auch als Umgebungsvariable setzen:

```bash
# In ~/.bashrc oder ~/.zshrc
export FIRMENBUCH_API_KEY="dein-api-key-hier"

# Oder in .env Datei im Projektverzeichnis
echo "FIRMENBUCH_API_KEY=dein-api-key-hier" > .env
```

Wenn du eine andere `.env` Datei verwenden möchtest:

```bash
fb --env-file /pfad/zu/deiner.env suche firma "Muster*"
```

---

## API-Key Sicherheit

⚠️ **Wichtig:** Behandle deinen API-Key wie ein Passwort!

- Teile ihn nicht öffentlich
- Committe ihn nicht in Git-Repositories
- Die CLI speichert ihn in `~/.config/firmenbuch/config` mit Leserechten nur für dich

---

## Kosten

Die Firmenbuch High-Value Dataset API ist **kostenlos** nutzbar.

> Die HVD-Verordnung der EU verpflichtet öffentliche Stellen, bestimmte Datensätze 
> kostenlos und maschinenlesbar bereitzustellen. Das Firmenbuch gehört dazu.

---

## Probleme?

### Kein API-Key erhalten?

- Prüfe deinen Spam-Ordner
- Kontaktiere: firmenbuch@brz.gv.at

### API-Key funktioniert nicht?

```bash
# Prüfe ob Key korrekt gespeichert
fb config show

# Teste mit direkter Angabe
fb suche firma "Test*" --api-key "dein-key"
```

### Rate-Limit erreicht?

Die API hat Limits für Anfragen pro Zeiteinheit. Warte einige Minuten und versuche es erneut.

---

## Weiterführende Links

- **API-Dokumentation:** [docs/api/](api/01-uebersicht.md)
- **WSDL:** https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl
- **Kontakt:** firmenbuch@brz.gv.at
