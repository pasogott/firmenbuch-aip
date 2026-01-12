"""Doctor-Befehl für Setup-Diagnose."""

from pathlib import Path
from typing import Optional

import httpx
import typer
from rich.panel import Panel

from ...config import API_URL, DEFAULT_ENV_PATH, get_env_api_key, load_env_file
from ..config_store import get_api_key_from_config
from ..console import console, print_success, print_warning

app = typer.Typer(help="Setup-Diagnose und Checks")


@app.callback(invoke_without_command=True)
def doctor(
    env_file: Optional[Path] = typer.Option(
        None,
        "--env-file",
        "-e",
        help="Alternative .env Datei für den Check",
    ),
) -> None:
    """Prüft Setup, API-Key und Netzwerkzugriff."""
    console.print(Panel("🩺 Firmenbuch CLI Doctor", style="bold blue"))

    if env_file:
        load_env_file(env_file)

    # 1. Env-File check
    if env_file:
        if env_file.exists():
            print_success(f".env Datei gefunden: {env_file}")
        else:
            print_warning(f".env Datei nicht gefunden: {env_file}")
    else:
        if DEFAULT_ENV_PATH.exists():
            print_success(f"Standard .env gefunden: {DEFAULT_ENV_PATH}")
        else:
            print_warning("Keine .env Datei im Projekt gefunden")

    # 2. API-Key check (env / config)
    api_key = get_env_api_key() or get_api_key_from_config()
    if api_key:
        masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        print_success(f"API-Key gefunden: {masked}")
    else:
        print_warning("Kein API-Key gefunden (ENV oder config)")

    # 3. API URL erreichbar?
    try:
        response = httpx.get(API_URL, timeout=5)
        if response.status_code < 500:
            print_success(f"API erreichbar ({response.status_code})")
        else:
            print_warning(f"API antwortet mit {response.status_code}")
    except Exception as e:
        print_warning(f"API nicht erreichbar: {e}")

    # 4. WSDL erreichbar
    try:
        wsdl_url = f"{API_URL}/fbw.wsdl"
        response = httpx.get(wsdl_url, timeout=5)
        if response.status_code == 200:
            print_success("WSDL erreichbar")
        else:
            print_warning(f"WSDL Status {response.status_code}")
    except Exception as e:
        print_warning(f"WSDL nicht erreichbar: {e}")
