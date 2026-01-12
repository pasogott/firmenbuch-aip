"""SOAP-Client und Hilfsfunktionen für Firmenbuch WebServices."""

from __future__ import annotations

import time

import httpx
from lxml import etree

from ..config import API_URL, REQUEST_TIMEOUT
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

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            response = httpx.post(
                API_URL,
                content=envelope,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            xml_root = etree.fromstring(response.content)
            _check_for_soap_fault(xml_root)
            return xml_to_json(response.content)
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.HTTPStatusError) as exc:
            last_error = exc
            if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code < 500:
                raise
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise

    raise last_error or RuntimeError("Unbekannter SOAP-Fehler")
