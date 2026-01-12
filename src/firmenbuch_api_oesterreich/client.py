# firmenbuch_sdk/client.py


import httpx
from lxml import etree


class SOAPFaultError(Exception):
    """Wird geworfen, wenn ein SOAP Fault auftritt."""

    def __init__(self, message: str, code: str | None = None):
        super().__init__(message)
        self.code = code


class FirmenbuchClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws",
        timeout: float = 10.0,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/soap+xml;charset=UTF-8",
            "X-API-KEY": self.api_key,
        }

    def _check_for_soap_fault(self, xml_root: etree._Element):
        fault = xml_root.find(".//{http://www.w3.org/2003/05/soap-envelope}Fault")
        if fault is not None:
            reason = fault.findtext(".//{http://www.w3.org/2003/05/soap-envelope}Text")
            code = fault.findtext(".//{http://www.w3.org/2003/05/soap-envelope}Value")
            raise SOAPFaultError(message=reason or "Unbekannter SOAP-Fehler", code=code)

    def send_soap_request(self, xml_body: str) -> etree._Element:
        response = httpx.post(
            self.base_url,
            content=xml_body.encode("utf-8"),
            headers=self.headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        xml_root = etree.fromstring(response.content)
        self._check_for_soap_fault(xml_root)

        return xml_root
