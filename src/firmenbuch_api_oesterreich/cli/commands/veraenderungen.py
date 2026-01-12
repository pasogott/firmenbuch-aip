"""Veränderungs-Befehle für Firmen und Urkunden."""

from datetime import datetime, timedelta
from typing import Annotated, Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...models.request_models import (
    VeraenderungenFirmaRequest,
    VeraenderungenUrkundeRequest,
)
from ...services.auszug import get_veraenderungen_firma, get_veraenderungen_urkunde
from ..common import ensure_list, extract_response, resolve_api_key
from ..console import (
    OutputFormat,
    console,
    print_error,
    print_json,
    print_veraenderungen_table,
    print_warning,
)
from ..pager import paginate

app = typer.Typer(help="Veränderungen abfragen")


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
    offset: Annotated[
        int,
        typer.Option("--offset", help="Start-Offset für Ergebnisse")
    ] = 0,
) -> None:
    """
    Ruft Firmenveränderungen für einen Zeitraum ab.
    
    Beispiele:
    
        fb veraenderungen firmen
        
        fb veraenderungen firmen --von 2024-01-01 --bis 2024-01-31
        
        fb veraenderungen firmen -g 007 -r AG
    """
    key = resolve_api_key(api_key)
    
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
    response = extract_response(result, "VERAENDERUNGENFIRMARESPONSE")
    veraenderungen = ensure_list(response.get("VERAENDERUNG"))
    
    if not veraenderungen:
        print_warning("Keine Veränderungen gefunden")
        return
    
    total = len(veraenderungen)
    veraenderungen = paginate(veraenderungen, limit=limit, offset=offset)

    if output == OutputFormat.JSON:
        print_json(veraenderungen)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_veraenderungen_table(veraenderungen, "Firmenveränderungen", total=total)


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
    offset: Annotated[
        int,
        typer.Option("--offset", help="Start-Offset für Ergebnisse")
    ] = 0,
) -> None:
    """
    Ruft Urkundenveränderungen für einen Zeitraum ab.
    
    Beispiele:
    
        fb veraenderungen urkunden
        
        fb veraenderungen urkunden --von 2024-01-01 --bis 2024-01-31
    """
    key = resolve_api_key(api_key)
    
    # Defaults
    if bis is None:
        bis = datetime.now()
    if von is None:
        von = bis - timedelta(days=7)
    
    request = VeraenderungenUrkundeRequest(
        von=von.date() if isinstance(von, datetime) else von,
        bis=bis.date() if isinstance(bis, datetime) else bis,
    )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Lade Veränderungen {von.date()} - {bis.date()}...", total=None)
        
        try:
            result = get_veraenderungen_urkunde(key, request)
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    # Ergebnisse extrahieren
    response_data = extract_response(result, "VERAENDERUNGENURKUNDERESPONSE")
    veraenderungen = ensure_list(response_data.get("VERAENDERUNG"))
    
    if not veraenderungen:
        print_warning("Keine Veränderungen gefunden")
        return
    
    total = len(veraenderungen)
    veraenderungen = paginate(veraenderungen, limit=limit, offset=offset)

    if output == OutputFormat.JSON:
        print_json(veraenderungen)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_veraenderungen_table(veraenderungen, "Urkundenveränderungen", total=total)
