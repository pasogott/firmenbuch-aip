"""SOAP-Client und Hilfsfunktionen für Firmenbuch WebServices."""

from __future__ import annotations

import httpx
from lxml import etree

from ..config import API_URL
from ..utils.xml_utils import xml_to_json

SOAP_ENV_NS = "http://www.w3.org/2003/05/soap-envelope"


class SOAPFaultError(Exception):
    """Wird geworfen, wenn ein SOAP Fault auftritt."""

    def __init__(self, message: str, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code


def build_envelope(namespace: str, body: str) -> str:
    """Baut ein SOAP-Envelope mit Namespace und Body."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<soap:Envelope xmlns:soap="{SOAP_ENV_NS}" xmlns:fb="{namespace}">\n'
        "  <soap:Header/>\n"
        "  <soap:Body>\n"
        f"{body}\n"
        "  </soap:Body>\n"
        "</soap:Envelope>"
    )


def _check_for_soap_fault(xml_root: etree._Element) -> None:
    """Prüft SOAP Faults und wirft eine Exception."""
    fault = xml_root.find(f".//{{{SOAP_ENV_NS}}}Fault")
    if fault is None:
        return

    reason = fault.findtext(f".//{{{SOAP_ENV_NS}}}Text")
    code = fault.findtext(f".//{{{SOAP_ENV_NS}}}Value")
    raise SOAPFaultError(message=reason or "Unbekannter SOAP-Fehler", code=code)


def send_soap_request(api_key: str, envelope: str, soap_action: str | None = None) -> dict:
    """Sendet einen SOAP-Request und gibt JSON zurück."""
    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api_key,
    }
    if soap_action:
        headers["SOAPAction"] = soap_action

    response = httpx.post(API_URL, content=envelope, headers=headers)
    response.raise_for_status()

    xml_root = etree.fromstring(response.content)
    _check_for_soap_fault(xml_root)

    return xml_to_json(response.content)
