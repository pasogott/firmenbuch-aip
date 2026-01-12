from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, validator


class AuszugUmfang(str, Enum):
    """Mögliche Werte für den UMFANG-Parameter beim Firmenbuchauszug."""

    KURZINFORMATION = "Kurzinformation"
    AKTUELLER_AUSZUG = "aktueller Auszug"
    HISTORISCHER_AUSZUG = "historischer Auszug"


class AuszugRequest(BaseModel):
    """Request-Modell für den Firmenbuchauszug."""

    fnr: str = Field(
        ..., description="Firmenbuchnummer mit Prüfbuchstaben (z.B. '000187a')"
    )
    stichtag: date = Field(..., description="Datum für den Auszug")
    umfang: AuszugUmfang = Field(
        default=AuszugUmfang.KURZINFORMATION, description="Art des Auszugs"
    )


class Suchbereich(int, Enum):
    """Mögliche Werte für den SUCHBEREICH-Parameter bei der Firmensuche."""

    EINGETRAGENE_UND_GELOESCHTE = 1
    HISTORISCHE_WORTLAUTE = 2
    KEINE_EINSCHRAENKUNG = 3
    EINGETRAGENE_WORTLAUTE = 4
    ARBEITSVERSION = 5
    ABGEWIESENE = 6


class SucheFirmaRequest(BaseModel):
    """Request-Modell für die Firmensuche."""

    firmenwortlaut: str = Field(
        ..., description="Name der Firma (mit * für Teilübereinstimmungen)"
    )
    exaktesuche: bool = Field(
        ..., description="True für exakte Suche, False für phonetische Suche"
    )
    suchbereich: Suchbereich = Field(..., description="Suchbereich (1-6)")
    gericht: Optional[str] = Field(None, description="3-stellige Gerichtsnummer")
    rechtsform: Optional[str] = Field(
        None, description="3-stellige Rechtsform (z.B. 'GES')"
    )
    rechtseigenschaft: Optional[str] = Field(
        None, description="Spezielle Rechtseigenschaft"
    )
    ortnr: Optional[str] = Field(
        None,
        description="Ortsnummer (5-stellig für Gemeinde, 3-stellig für Bezirk, 1-stellig für Bundesland)",
    )

    @validator("gericht")
    def validate_gericht(cls, v):
        if v and (not v.isdigit() or len(v) != 3):
            raise ValueError("Gerichtsnummer muss 3-stellig sein")
        return v

    @validator("rechtsform")
    def validate_rechtsform(cls, v):
        if v and len(v) != 3:
            raise ValueError("Rechtsform muss 3-stellig sein")
        return v

    @validator("ortnr")
    def validate_ortnr(cls, v):
        if v and not v.isdigit():
            raise ValueError("Ortsnummer muss numerisch sein")
        if v and len(v) not in [1, 3, 5]:
            raise ValueError(
                "Ortsnummer muss 1-stellig (Bundesland), 3-stellig (Bezirk) oder 5-stellig (Gemeinde) sein"
            )
        return v


class SucheUrkundeRequest(BaseModel):
    """Request-Modell für die Urkundensuche."""

    fnr: Optional[str] = Field(None, description="Firmenbuchnummer mit Prüfbuchstaben")
    az: Optional[str] = Field(None, description="Aktenzeichen")

    @validator("az", always=True)
    def validate_at_least_one(cls, v, values):
        if not values.get("fnr") and not v:
            raise ValueError("Entweder FNR oder AZ muss angegeben werden")
        return v


class VeraenderungArt(str, Enum):
    """Mögliche Werte für den ARTDERVERAENDERUNG-Parameter bei Firmenveränderungen."""

    FIRMENBEZEICHNUNG = "FIRMENBEZEICHNUNG"
    FIRMENSITZ = "FIRMENSITZ"
    GESELLSCHAFTER = "GESELLSCHAFTER"
    GESCHAEFTSFUEHRER = "GESCHAEFTSFUEHRER"
    KAPITAL = "KAPITAL"
    GESCHAEFTSZWEIG = "GESCHAEFTSZWEIG"
    LOESCHUNG = "LOESCHUNG"


class VeraenderungenFirmaRequest(BaseModel):
    """Request-Modell für Firmenveränderungen."""

    von: date = Field(..., description="Beginndatum")
    bis: date = Field(..., description="Enddatum")
    gericht: Optional[str] = Field(None, description="3-stellige Gerichtsnummer")
    rechtsform: Optional[str] = Field(None, description="3-stellige Rechtsform")
    art_der_veraenderung: Optional[VeraenderungArt] = Field(
        None, description="Art der Veränderung"
    )

    @validator("bis")
    def validate_date_range(cls, v, values):
        if "von" in values and v < values["von"]:
            raise ValueError("Enddatum muss nach dem Beginndatum liegen")
        return v

    @validator("gericht")
    def validate_gericht(cls, v):
        if v and (not v.isdigit() or len(v) != 3):
            raise ValueError("Gerichtsnummer muss 3-stellig sein")
        return v

    @validator("rechtsform")
    def validate_rechtsform(cls, v):
        if v and len(v) != 3:
            raise ValueError("Rechtsform muss 3-stellig sein")
        return v


class VeraenderungenUrkundeRequest(BaseModel):
    """Request-Modell für Urkundenveränderungen."""

    von: date = Field(..., description="Beginndatum")
    bis: date = Field(..., description="Enddatum")

    @validator("bis")
    def validate_date_range(cls, v, values):
        if "von" in values and v < values["von"]:
            raise ValueError("Enddatum muss nach dem Beginndatum liegen")
        return v


class UrkundeRequest(BaseModel):
    """Request-Modell für den Urkundenabruf."""

    key: Optional[str] = Field(None, description="Urkunden-Key")
    fnr: Optional[str] = Field(None, description="Firmenbuchnummer mit Prüfbuchstaben")
    az: Optional[str] = Field(None, description="Aktenzeichen")

    @validator("az", always=True)
    def validate_key_or_fnr_az(cls, v, values):
        if values.get("key"):
            return v
        if not values.get("fnr") or not v:
            raise ValueError("Entweder KEY oder FNR+AZ muss angegeben werden")
        return v
