"""Zentrale Konfigurationsdatei für die Firmenbuch API."""

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

# Lade .env Datei aus dem Projektroot
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# API Konfiguration
API_URL: Final[str] = "https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws"
API_KEY: Final[str] = os.getenv("FIRMENBUCH_API_KEY", "")

if not API_KEY:
    raise ValueError(
        "FIRMENBUCH_API_KEY muss in der .env Datei oder als Umgebungsvariable gesetzt sein"
    )

# SOAP Namespaces
AUSZUG_NAMESPACE: Final[str] = "ns://firmenbuch.justiz.gv.at/Abfrage/v2/AuszugRequest"
SUCHE_FIRMA_NAMESPACE: Final[str] = (
    "ns://firmenbuch.justiz.gv.at/Abfrage/SucheFirmaRequest"
)
SUCHE_URKUNDE_NAMESPACE: Final[str] = (
    "ns://firmenbuch.justiz.gv.at/Abfrage/SucheUrkundeRequest"
)
VERAENDERUNGEN_FIRMA_NAMESPACE: Final[str] = (
    "ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenFirmaRequest"
)
VERAENDERUNGEN_URKUNDE_NAMESPACE: Final[str] = (
    "ns://firmenbuch.justiz.gv.at/Abfrage/VeraenderungenUrkundeRequest"
)
URKUNDE_NAMESPACE: Final[str] = "ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeRequest"

# SOAP Actions
AUSZUG_SOAP_ACTION: Final[str] = f"{AUSZUG_NAMESPACE}/AUSZUG_V2_REQUEST"
SUCHE_FIRMA_SOAP_ACTION: Final[str] = f"{SUCHE_FIRMA_NAMESPACE}/SUCHEFIRMAREQUEST"
SUCHE_URKUNDE_SOAP_ACTION: Final[str] = f"{SUCHE_URKUNDE_NAMESPACE}/SUCHEURKUNDEREQUEST"
VERAENDERUNGEN_FIRMA_SOAP_ACTION: Final[str] = (
    f"{VERAENDERUNGEN_FIRMA_NAMESPACE}/VERAENDERUNGENFIRMAREQUEST"
)
VERAENDERUNGEN_URKUNDE_SOAP_ACTION: Final[str] = (
    f"{VERAENDERUNGEN_URKUNDE_NAMESPACE}/VERAENDERUNGENURKUNDEREQUEST"
)
URKUNDE_SOAP_ACTION: Final[str] = f"{URKUNDE_NAMESPACE}/URKUNDEREQUEST"
