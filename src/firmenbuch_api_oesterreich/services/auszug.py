# services/auszug.py

from ..config import (
    AUSZUG_NAMESPACE,
    AUSZUG_SOAP_ACTION,
    SUCHE_FIRMA_NAMESPACE,
    SUCHE_URKUNDE_NAMESPACE,
    URKUNDE_NAMESPACE,
    VERAENDERUNGEN_FIRMA_NAMESPACE,
    VERAENDERUNGEN_URKUNDE_NAMESPACE,
)
from ..models.request_models import (
    AuszugRequest,
    SucheFirmaRequest,
    SucheUrkundeRequest,
    UrkundeRequest,
    VeraenderungenFirmaRequest,
    VeraenderungenUrkundeRequest,
)
from .soap_client import build_envelope, send_soap_request


def _optional_tag(tag: str, value: str | None) -> str:
    if value is None or value == "":
        return ""
    return f"<fb:{tag}>{value}</fb:{tag}>"


def get_auszug(api_key: str, request: AuszugRequest) -> dict:
    """
    Ruft einen Firmenbuchauszug ab.

    Args:
        api_key (str): Der API-Schlüssel für die Authentifizierung
        request (AuszugRequest): Die Anfrage-Parameter

    Returns:
        dict: JSON-Response mit dem Firmenbuchauszug

    Raises:
        HTTPError: Bei Fehlern in der HTTP-Kommunikation
    """
    body = (
        "  <fb:AUSZUG_V2_REQUEST>\n"
        f"    <fb:FNR>{request.fnr}</fb:FNR>\n"
        f"    <fb:STICHTAG>{request.stichtag}</fb:STICHTAG>\n"
        f"    <fb:UMFANG>{request.umfang.value}</fb:UMFANG>\n"
        "  </fb:AUSZUG_V2_REQUEST>"
    )

    envelope = build_envelope(AUSZUG_NAMESPACE, body)
    return send_soap_request(api_key, envelope, AUSZUG_SOAP_ACTION)


def suche_firma(api_key: str, request: SucheFirmaRequest) -> dict:
    """
    Sucht nach Firmen im Firmenbuch.

    Args:
        api_key (str): Der API-Schlüssel für die Authentifizierung
        request (SucheFirmaRequest): Die Anfrage-Parameter

    Returns:
        dict: JSON-Response mit den Suchergebnissen

    Raises:
        HTTPError: Bei Fehlern in der HTTP-Kommunikation
    """
    lines = [
        "  <fb:SUCHEFIRMAREQUEST>",
        f"    <fb:FIRMENWORTLAUT>{request.firmenwortlaut}</fb:FIRMENWORTLAUT>",
        f"    <fb:EXAKTESUCHE>{str(request.exaktesuche).lower()}</fb:EXAKTESUCHE>",
        f"    <fb:SUCHBEREICH>{request.suchbereich}</fb:SUCHBEREICH>",
    ]

    for tag, value in (
        ("GERICHT", request.gericht),
        ("RECHTSFORM", request.rechtsform),
        ("RECHTSEIGENSCHAFT", request.rechtseigenschaft),
        ("ORTNR", request.ortnr),
    ):
        optional = _optional_tag(tag, value)
        if optional:
            lines.append(f"    {optional}")

    lines.append("  </fb:SUCHEFIRMAREQUEST>")
    body = "\n".join(lines)

    envelope = build_envelope(SUCHE_FIRMA_NAMESPACE, body)
    return send_soap_request(api_key, envelope)


def suche_urkunde(api_key: str, request: SucheUrkundeRequest) -> dict:
    """
    Sucht nach Urkunden im Firmenbuch.

    Args:
        api_key (str): Der API-Schlüssel für die Authentifizierung
        request (SucheUrkundeRequest): Die Anfrage-Parameter

    Returns:
        dict: JSON-Response mit den Suchergebnissen

    Raises:
        HTTPError: Bei Fehlern in der HTTP-Kommunikation
    """
    body = (
        "  <fb:SUCHEURKUNDEREQUEST>\n"
        f"    {f'<fb:FNR>{request.fnr}</fb:FNR>' if request.fnr else ''}\n"
        f"    {f'<fb:AZ>{request.az}</fb:AZ>' if request.az else ''}\n"
        "  </fb:SUCHEURKUNDEREQUEST>"
    )

    envelope = build_envelope(SUCHE_URKUNDE_NAMESPACE, body)
    return send_soap_request(api_key, envelope)


def get_veraenderungen_firma(api_key: str, request: VeraenderungenFirmaRequest) -> dict:
    """
    Ruft Firmenveränderungen für einen Zeitraum ab.

    Args:
        api_key (str): Der API-Schlüssel für die Authentifizierung
        request (VeraenderungenFirmaRequest): Die Anfrage-Parameter

    Returns:
        dict: JSON-Response mit den Firmenveränderungen

    Raises:
        HTTPError: Bei Fehlern in der HTTP-Kommunikation
    """
    lines = [
        "  <fb:VERAENDERUNGENFIRMAREQUEST>",
        f"    <fb:VON>{request.von}</fb:VON>",
        f"    <fb:BIS>{request.bis}</fb:BIS>",
    ]

    for tag, value in (
        ("GERICHT", request.gericht),
        ("RECHTSFORM", request.rechtsform),
        ("ARTDERVERAENDERUNG", request.art_der_veraenderung),
    ):
        optional = _optional_tag(tag, value)
        if optional:
            lines.append(f"    {optional}")

    lines.append("  </fb:VERAENDERUNGENFIRMAREQUEST>")
    body = "\n".join(lines)

    envelope = build_envelope(VERAENDERUNGEN_FIRMA_NAMESPACE, body)
    return send_soap_request(api_key, envelope)


def get_veraenderungen_urkunde(api_key: str, request: VeraenderungenUrkundeRequest) -> dict:
    """
    Ruft Urkundenveränderungen ab.

    Args:
        api_key (str): Der API-Schlüssel für die Authentifizierung
        request (VeraenderungenUrkundeRequest): Die Anfrage-Parameter

    Returns:
        dict: JSON-Response mit den Urkundenveränderungen

    Raises:
        HTTPError: Bei Fehlern in der HTTP-Kommunikation
    """
    body = (
        "  <fb:VERAENDERUNGENURKUNDEREQUEST>\n"
        f"    <fb:VON>{request.von}</fb:VON>\n"
        f"    <fb:BIS>{request.bis}</fb:BIS>\n"
        "  </fb:VERAENDERUNGENURKUNDEREQUEST>"
    )

    envelope = build_envelope(VERAENDERUNGEN_URKUNDE_NAMESPACE, body)
    return send_soap_request(api_key, envelope)


def get_urkunde(api_key: str, request: UrkundeRequest) -> dict:
    """
    Ruft eine spezifische Urkunde ab.

    Args:
        api_key (str): Der API-Schlüssel für die Authentifizierung
        request (UrkundeRequest): Die Anfrage-Parameter

    Returns:
        dict: JSON-Response mit der Urkunde

    Raises:
        HTTPError: Bei Fehlern in der HTTP-Kommunikation
    """
    if request.key:
        request_body = "\n".join(
            [
                "  <fb:URKUNDEREQUEST>",
                f"    <fb:KEY>{request.key}</fb:KEY>",
                "  </fb:URKUNDEREQUEST>",
            ]
        )
    else:
        request_body = (
            "  <fb:URKUNDEREQUEST>\n"
            f"    <fb:FNR>{request.fnr}</fb:FNR>\n"
            f"    <fb:AZ>{request.az}</fb:AZ>\n"
            "  </fb:URKUNDEREQUEST>"
        )

    envelope = build_envelope(URKUNDE_NAMESPACE, request_body)
    return send_soap_request(api_key, envelope)
