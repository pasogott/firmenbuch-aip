"""XML Utility Funktionen für die Firmenbuch API."""

import xmltodict
from lxml import etree


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


def xml_to_json(xml_content: bytes | str) -> dict:
    """
    Konvertiert XML-Content in ein bereinigtes JSON-Objekt.

    Args:
        xml_content (bytes | str): Der XML-Content als Bytes oder String

    Returns:
        dict: Das bereinigte JSON-Objekt ohne Namespaces
    """
    if isinstance(xml_content, bytes):
        xml_element = etree.fromstring(xml_content)
    else:
        xml_element = etree.fromstring(xml_content.encode())

    xml_string = etree.tostring(xml_element, encoding="unicode")
    json_data = xmltodict.parse(xml_string)
    return _clean_namespaces(json_data)
