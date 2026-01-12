"""Veränderungs-Befehle für Firmen und Urkunden."""

from datetime import datetime, timedelta
from typing import Annotated, Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...models.request_models import VeraenderungenFirmaRequest
from ...services.auszug import get_veraenderungen_firma
from ..console import (
    OutputFormat,
    console,
    print_error,
    print_json,
    print_veraenderungen_table,
    print_warning,
)
from .config import get_api_key_from_config

app = typer.Typer(help="Veränderungen abfragen")


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


@app.command("firmen")
def firmen(
    von: Annotated[
        Optional[datetime],
        typer.Option(
            "--von", "-v",
            formats=["%Y-%m-%d"],
            help="Startdatum (Standard: vor 7 Tagen)"
        )
    ] = None,
    bis: Annotated[
        Optional[datetime],
        typer.Option(
            "--bis", "-b",
            formats=["%Y-%m-%d"],
            help="Enddatum (Standard: heute)"
        )
    ] = None,
    gericht: Annotated[
        Optional[str],
        typer.Option("--gericht", "-g", help="3-stellige Gerichtsnummer")
    ] = None,
    rechtsform: Annotated[
        Optional[str],
        typer.Option("--rechtsform", "-r", help="Rechtsform (z.B. AG, GES)")
    ] = None,
    api_key: Annotated[
        Optional[str],
        typer.Option("--api-key", "-k", envvar="FIRMENBUCH_API_KEY", help="API-Key")
    ] = None,
    output: Annotated[
        OutputFormat,
        typer.Option("--output", "-o", help="Ausgabeformat")
    ] = OutputFormat.TABLE,
    limit: Annotated[
        int,
        typer.Option("--limit", "-l", help="Max. Anzahl Ergebnisse")
    ] = 100,
) -> None:
    """
    Ruft Firmenveränderungen für einen Zeitraum ab.
    
    Beispiele:
    
        fb veraenderungen firmen
        
        fb veraenderungen firmen --von 2024-01-01 --bis 2024-01-31
        
        fb veraenderungen firmen -g 007 -r AG
    """
    key = get_api_key(api_key)
    
    # Defaults
    if bis is None:
        bis = datetime.now()
    if von is None:
        von = bis - timedelta(days=7)
    
    request = VeraenderungenFirmaRequest(
        von=von.date() if isinstance(von, datetime) else von,
        bis=bis.date() if isinstance(bis, datetime) else bis,
        gericht=gericht,
        rechtsform=rechtsform,
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Lade Veränderungen {von.date()} - {bis.date()}...", total=None)
        
        try:
            result = get_veraenderungen_firma(key, request)
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    # Ergebnisse extrahieren
    response = result.get("Envelope", {}).get("Body", {}).get("VERAENDERUNGENFIRMARESPONSE", {})
    veraenderungen = response.get("VERAENDERUNG", [])
    
    # Einzelergebnis in Liste umwandeln
    if isinstance(veraenderungen, dict):
        veraenderungen = [veraenderungen]
    
    if not veraenderungen:
        print_warning("Keine Veränderungen gefunden")
        return
    
    # Limit anwenden
    veraenderungen = veraenderungen[:limit]
    
    if output == OutputFormat.JSON:
        print_json(veraenderungen)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_veraenderungen_table(veraenderungen, "Firmenveränderungen")


@app.command("urkunden")
def urkunden(
    von: Annotated[
        Optional[datetime],
        typer.Option(
            "--von", "-v",
            formats=["%Y-%m-%d"],
            help="Startdatum (Standard: vor 7 Tagen)"
        )
    ] = None,
    bis: Annotated[
        Optional[datetime],
        typer.Option(
            "--bis", "-b",
            formats=["%Y-%m-%d"],
            help="Enddatum (Standard: heute)"
        )
    ] = None,
    api_key: Annotated[
        Optional[str],
        typer.Option("--api-key", "-k", envvar="FIRMENBUCH_API_KEY", help="API-Key")
    ] = None,
    output: Annotated[
        OutputFormat,
        typer.Option("--output", "-o", help="Ausgabeformat")
    ] = OutputFormat.TABLE,
    limit: Annotated[
        int,
        typer.Option("--limit", "-l", help="Max. Anzahl Ergebnisse")
    ] = 100,
) -> None:
    """
    Ruft Urkundenveränderungen für einen Zeitraum ab.
    
    Beispiele:
    
        fb veraenderungen urkunden
        
        fb veraenderungen urkunden --von 2024-01-01 --bis 2024-01-31
    """
    key = get_api_key(api_key)
    
    # Defaults
    if bis is None:
        bis = datetime.now()
    if von is None:
        von = bis - timedelta(days=7)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Lade Veränderungen {von.date()} - {bis.date()}...", total=None)
        
        try:
            from ...config import API_URL, VERAENDERUNGEN_URKUNDE_NAMESPACE
            import httpx
            from ...utils.xml_utils import xml_to_json
            
            envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                           xmlns:fb="{VERAENDERUNGEN_URKUNDE_NAMESPACE}">
                <soap:Header/>
                <soap:Body>
                    <fb:VERAENDERUNGENURKUNDEREQUEST>
                        <fb:VON>{von.date()}</fb:VON>
                        <fb:BIS>{bis.date()}</fb:BIS>
                    </fb:VERAENDERUNGENURKUNDEREQUEST>
                </soap:Body>
            </soap:Envelope>
            """
            
            headers = {
                "Content-Type": "application/soap+xml;charset=UTF-8",
                "X-API-KEY": key,
            }
            
            response = httpx.post(API_URL, content=envelope, headers=headers)
            response.raise_for_status()
            result = xml_to_json(response.content)
            
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    # Ergebnisse extrahieren
    response_data = result.get("Envelope", {}).get("Body", {}).get("VERAENDERUNGENURKUNDERESPONSE", {})
    veraenderungen = response_data.get("VERAENDERUNG", [])
    
    # Einzelergebnis in Liste umwandeln
    if isinstance(veraenderungen, dict):
        veraenderungen = [veraenderungen]
    
    if not veraenderungen:
        print_warning("Keine Veränderungen gefunden")
        return
    
    # Limit anwenden
    veraenderungen = veraenderungen[:limit]
    
    if output == OutputFormat.JSON:
        print_json(veraenderungen)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_veraenderungen_table(veraenderungen, "Urkundenveränderungen")
