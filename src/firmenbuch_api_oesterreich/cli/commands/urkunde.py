"""Urkunde-Befehle zum Abrufen und Herunterladen von Dokumenten."""

import base64
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..console import (
    OutputFormat,
    console,
    print_error,
    print_json,
    print_success,
)
from .config import get_api_key_from_config

app = typer.Typer(help="Urkunden abrufen und herunterladen")


def get_api_key(api_key: Optional[str]) -> str:
    """Holt den API-Key aus Parameter oder Config."""
    if api_key:
        return api_key
    
    key = get_api_key_from_config()
    if not key:
        print_error(
            "Kein API-Key gefunden!\n\n"
            "Setze den Key mit: fb config set-key\n"
            "Oder übergib ihn mit: --api-key KEY"
        )
        raise typer.Exit(1)
    return key


def fetch_urkunde(api: str, key: str) -> dict:
    """Lädt eine Urkunde vom Server."""
    from ...config import API_URL, URKUNDE_NAMESPACE
    import httpx
    from ...utils.xml_utils import xml_to_json
    
    envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                   xmlns:fb="{URKUNDE_NAMESPACE}">
        <soap:Header/>
        <soap:Body>
            <fb:URKUNDEREQUEST>
                <fb:KEY>{key}</fb:KEY>
            </fb:URKUNDEREQUEST>
        </soap:Body>
    </soap:Envelope>
    """
    
    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "X-API-KEY": api,
    }
    
    response = httpx.post(API_URL, content=envelope, headers=headers)
    response.raise_for_status()
    
    return xml_to_json(response.content)


@app.command("info")
def info(
    key: Annotated[
        str,
        typer.Argument(help="Urkunden-Key (aus Urkundensuche)")
    ],
    api_key: Annotated[
        Optional[str],
        typer.Option("--api-key", "-k", envvar="FIRMENBUCH_API_KEY", help="API-Key")
    ] = None,
    output: Annotated[
        OutputFormat,
        typer.Option("--output", "-o", help="Ausgabeformat")
    ] = OutputFormat.TABLE,
) -> None:
    """
    Zeigt Metadaten einer Urkunde.
    
    Beispiele:
    
        fb urkunde info "304188_0070711322495_000___000_30_7730290_XML"
    """
    api = get_api_key(api_key)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Lade Urkunde...", total=None)
        
        try:
            result = fetch_urkunde(api, key)
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    # Metadaten extrahieren
    response_data = result.get("Envelope", {}).get("Body", {}).get("URKUNDERESPONSE", {})
    metadaten = response_data.get("METADATEN", {})
    
    if output == OutputFormat.JSON:
        print_json(metadaten)
    else:
        console.print("\n[bold]📄 Urkunden-Metadaten[/bold]\n")
        
        for key_name, value in metadaten.items():
            if isinstance(value, dict):
                value = value.get("TEXT", value.get("CODE", str(value)))
            console.print(f"  [dim]{key_name}:[/dim] {value}")


@app.command("download")
def download(
    key: Annotated[
        str,
        typer.Argument(help="Urkunden-Key (aus Urkundensuche)")
    ],
    output_path: Annotated[
        Optional[Path],
        typer.Option("--output", "-o", help="Ausgabepfad (Standard: automatisch)")
    ] = None,
    api_key: Annotated[
        Optional[str],
        typer.Option("--api-key", "-k", envvar="FIRMENBUCH_API_KEY", help="API-Key")
    ] = None,
) -> None:
    """
    Lädt eine Urkunde herunter.
    
    Beispiele:
    
        fb urkunde download "304188_..._PDF"
        
        fb urkunde download "304188_..._PDF" -o jahresabschluss.pdf
    """
    api = get_api_key(api_key)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Lade Urkunde...", total=None)
        
        try:
            result = fetch_urkunde(api, key)
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    # Dokument extrahieren
    response_data = result.get("Envelope", {}).get("Body", {}).get("URKUNDERESPONSE", {})
    dokument = response_data.get("DOKUMENT", {})
    metadaten = response_data.get("METADATEN", {})
    
    content_b64 = dokument.get("CONTENT")
    if not content_b64:
        print_error("Kein Dokument-Inhalt gefunden")
        raise typer.Exit(1)
    
    # Base64 dekodieren
    try:
        content = base64.b64decode(content_b64)
    except Exception as e:
        print_error(f"Fehler beim Dekodieren: {e}")
        raise typer.Exit(1)
    
    # Dateiname generieren
    if output_path is None:
        fnr = metadaten.get("FNR", "urkunde").replace(" ", "_")
        ext = dokument.get("DATEIENDUNG", "bin")
        dokumentart = metadaten.get("DOKUMENTART", {})
        if isinstance(dokumentart, dict):
            dokumentart = dokumentart.get("TEXT", "").replace(" ", "_").replace("/", "_")
        else:
            dokumentart = ""
        
        if dokumentart:
            output_path = Path(f"{fnr}_{dokumentart}.{ext}")
        else:
            output_path = Path(f"{fnr}.{ext}")
    
    # Speichern
    output_path.write_bytes(content)
    
    size_kb = len(content) / 1024
    print_success(f"Gespeichert: {output_path} ({size_kb:.1f} KB)")
