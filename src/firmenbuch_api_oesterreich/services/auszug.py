# services/auszug.py

import httpx
import xmltodict
from lxml import etree

from ..config import API_URL, AUSZUG_NAMESPACE, AUSZUG_SOAP_ACTION
from ..models.request_models import (
    AuszugRequest,
    SucheFirmaRequest,
    SucheUrkundeRequest,
    UrkundeRequest,
    VeraenderungenFirmaRequest,
    VeraenderungenUrkundeRequest,
)
from ..utils.xml_utils import xml_to_json


def _clean_namespaces(data: dict) -> dict:
    """
    Entfernt Namespaces aus der XML-Response und bereinigt die Struktur.

    Args:
        data (dict): Die zu bereinigende XML-Response

    Returns:
        dict: Die bereinigte Response ohne Namespaces
    """
    if isinstance(data, dict):
        # Entferne @-Attribute und füge sie als normale Schlüssel hinzu
        cleaned = {}
        for key, value in data.items():
            # Entferne Namespace-Präfixe
            clean_key = key.split(":")[-1] if ":" in key else key

            # Entferne @-Präfix von Attributen
            if clean_key.startswith("@"):
                clean_key = clean_key[1:]

            # Rekursiv bereinigen
            if isinstance(value, (dict, list)):
                cleaned[clean_key] = _clean_namespaces(value)
            else:
                cleaned[clean_key] = value
        return cleaned
    elif isinstance(data, list):
        return [_clean_namespaces(item) for item in data]
    return data


def _xml_to_json(xml_element: etree._Element) -> dict:
    """
    Konvertiert ein XML-Element in ein JSON-Objekt.

    Args:
        xml_element (etree._Element): Das XML-Element

    Returns:
        dict: Das konvertierte JSON-Objekt
    """
    xml_string = etree.tostring(xml_element, encoding="unicode")
    json_data = xmltodict.parse(xml_string)
    return _clean_namespaces(json_data)


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
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:fb="{AUSZUG_NAMESPACE}"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <soap:Header/>
        <soap:Body>
            <fb:AUSZUG_V2_REQUEST>
                <fb:FNR>{request.fnr}</fb:FNR>
                <fb:STICHTAG>{request.stichtag}</fb:STICHTAG>
                <fb:UMFANG>{request.umfang.value}</fb:UMFANG>
            </fb:AUSZUG_V2_REQUEST>
        </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api_key,
        "SOAPAction": AUSZUG_SOAP_ACTION,
    }

    try:
        response = httpx.post(API_URL, content=envelope, headers=headers)
        response.raise_for_status()
        return xml_to_json(response.content)
    except httpx.HTTPStatusError as e:
        print(f"\nServer-Antwort (Status {e.response.status_code}):")
        print(e.response.text)
        raise


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
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:fb="{SUCHE_FIRMA_NAMESPACE}">
        <soap:Header/>
        <soap:Body>
            <fb:SUCHEFIRMAREQUEST>
                <fb:FIRMENWORTLAUT>{request.firmenwortlaut}</fb:FIRMENWORTLAUT>
                <fb:EXAKTESUCHE>{str(request.exaktesuche).lower()}</fb:EXAKTESUCHE>
                <fb:SUCHBEREICH>{request.suchbereich}</fb:SUCHBEREICH>
                {f"<fb:GERICHT>{request.gericht}</fb:GERICHT>" if request.gericht else ""}
                {f"<fb:RECHTSFORM>{request.rechtsform}</fb:RECHTSFORM>" if request.rechtsform else ""}
                {f"<fb:RECHTSEIGENSCHAFT>{request.rechtseigenschaft}</fb:RECHTSEIGENSCHAFT>" if request.rechtseigenschaft else ""}
                {f"<fb:ORTNR>{request.ortnr}</fb:ORTNR>" if request.ortnr else ""}
            </fb:SUCHEFIRMAREQUEST>
        </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api_key,
    }

    response = httpx.post(API_URL, content=envelope, headers=headers)
    response.raise_for_status()
    xml_response = etree.fromstring(response.content)
    return _xml_to_json(xml_response)


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
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:fb="{SUCHE_URKUNDE_NAMESPACE}">
        <soap:Header/>
        <soap:Body>
            <fb:SUCHEURKUNDEREQUEST>
                {f"<fb:FNR>{request.fnr}</fb:FNR>" if request.fnr else ""}
                {f"<fb:AZ>{request.az}</fb:AZ>" if request.az else ""}
            </fb:SUCHEURKUNDEREQUEST>
        </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api_key,
    }

    response = httpx.post(API_URL, content=envelope, headers=headers)
    response.raise_for_status()
    xml_response = etree.fromstring(response.content)
    return _xml_to_json(xml_response)


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
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:fb="{VERAENDERUNGEN_FIRMA_NAMESPACE}">
        <soap:Header/>
        <soap:Body>
            <fb:VERAENDERUNGENFIRMAREQUEST>
                <fb:VON>{request.von}</fb:VON>
                <fb:BIS>{request.bis}</fb:BIS>
                {f"<fb:GERICHT>{request.gericht}</fb:GERICHT>" if request.gericht else ""}
                {f"<fb:RECHTSFORM>{request.rechtsform}</fb:RECHTSFORM>" if request.rechtsform else ""}
                {f"<fb:ARTDERVERAENDERUNG>{request.art_der_veraenderung}</fb:ARTDERVERAENDERUNG>" if request.art_der_veraenderung else ""}
            </fb:VERAENDERUNGENFIRMAREQUEST>
        </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api_key,
    }

    response = httpx.post(API_URL, content=envelope, headers=headers)
    response.raise_for_status()
    xml_response = etree.fromstring(response.content)
    return _xml_to_json(xml_response)


def get_veraenderungen_urkunde(
    api_key: str, request: VeraenderungenUrkundeRequest
) -> dict:
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
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:fb="{VERAENDERUNGEN_URKUNDE_NAMESPACE}">
        <soap:Header/>
        <soap:Body>
            <fb:VERAENDERUNGENURKUNDEREQUEST>
                <fb:FNR>{request.fnr}</fb:FNR>
            </fb:VERAENDERUNGENURKUNDEREQUEST>
        </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api_key,
    }

    response = httpx.post(API_URL, content=envelope, headers=headers)
    response.raise_for_status()
    xml_response = etree.fromstring(response.content)
    return _xml_to_json(xml_response)


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
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:fb="{URKUNDE_NAMESPACE}">
        <soap:Header/>
        <soap:Body>
            <fb:URKUNDEREQUEST>
                <fb:FNR>{request.fnr}</fb:FNR>
                <fb:AZ>{request.az}</fb:AZ>
            </fb:URKUNDEREQUEST>
        </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api_key,
    }

    response = httpx.post(API_URL, content=envelope, headers=headers)
    response.raise_for_status()
    xml_response = etree.fromstring(response.content)
    return _xml_to_json(xml_response)
