"""Gemeinsame CLI-Hilfsfunktionen."""

from typing import Any

import typer

from ..config import get_env_api_key
from .config_store import get_api_key_from_config
from .console import print_error


def resolve_api_key(api_key: str | None) -> str:
    """Ermittelt den API-Key aus Parametern, Config oder ENV."""
    if api_key:
        return api_key

    env_key = get_env_api_key()
    if env_key:
        return env_key

    config_key = get_api_key_from_config()
    if config_key:
        return config_key

    print_error(
        "Kein API-Key gefunden!\n\n"
        "Setze den Key mit: firmenbuchat config set-key\n"
        "Oder übergib ihn mit: --api-key KEY"
    )
    raise typer.Exit(1)


def extract_response(result: dict, response_key: str) -> dict:
    """Extrahiert das Response-Objekt aus der SOAP-Hülle."""
    return result.get("Envelope", {}).get("Body", {}).get(response_key, {})


def ensure_list(value: Any) -> list:
    """Sorgt dafür, dass ein Wert als Liste vorliegt."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    return [value]
