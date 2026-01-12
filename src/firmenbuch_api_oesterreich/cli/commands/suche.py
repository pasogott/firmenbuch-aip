"""Such-Befehle für Firmen und Urkunden."""

from typing import Annotated, Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...models.request_models import SucheFirmaRequest, SucheUrkundeRequest
from ...services.auszug import suche_firma, suche_urkunde
from ..common import ensure_list, extract_response, resolve_api_key
from ..console import (
    OutputFormat,
    console,
    print_error,
    print_firma_table,
    print_json,
    print_urkunden_table,
    print_warning,
)

app = typer.Typer(help="Firmen und Urkunden suchen")


@app.command("firma")
def firma(
    suchbegriff: Annotated[
        str,
        typer.Argument(help="Suchbegriff (mit * für Wildcards)")
    ],
    suchbereich: Annotated[
        int,
        typer.Option("--bereich", "-b", min=1, max=6, help="Suchbereich 1-6")
    ] = 1,
    exakt: Annotated[
        bool,
        typer.Option("--exakt", "-e", help="Exakte Suche (sonst phonetisch)")
    ] = False,
    gericht: Annotated[
        Optional[str],
        typer.Option("--gericht", "-g", help="3-stellige Gerichtsnummer")
    ] = None,
    rechtsform: Annotated[
        Optional[str],
        typer.Option("--rechtsform", "-r", help="Rechtsform (z.B. GES, AG)")
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
    ] = 50,
) -> None:
    """
    Sucht nach Firmen im Firmenbuch.
    
    Suchbereiche:
    
    - 1: Eingetragene und gelöschte Firmen
    - 2: Historische Firmenwortlaute  
    - 3: Keine Einschränkung
    - 4: Prüfung Firmenausschließlichkeit
    - 5: Firmen in Arbeitsversion
    - 6: Abgewiesene Neueintragungen
    
    Beispiele:
    
        fb suche firma "Musterfirma*"
        
        fb suche firma "Software" --gericht 007 --rechtsform GES
        
        fb suche firma "Mayer" -e -b 3
    """
    key = resolve_api_key(api_key)
    
    request = SucheFirmaRequest(
        firmenwortlaut=suchbegriff,
        exaktesuche=exakt,
        suchbereich=suchbereich,
        gericht=gericht,
        rechtsform=rechtsform,
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Suche nach '{suchbegriff}'...", total=None)
        
        try:
            result = suche_firma(key, request)
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    # Ergebnisse extrahieren
    response = extract_response(result, "SUCHEFIRMARESPONSE")
    ergebnisse = ensure_list(response.get("ERGEBNIS"))
    
    if not ergebnisse:
        print_warning("Keine Firmen gefunden")
        return
    
    # Limit anwenden
    ergebnisse = ergebnisse[:limit]
    
    if output == OutputFormat.JSON:
        print_json(ergebnisse)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_firma_table(ergebnisse)


@app.command("urkunde")
def urkunde(
    fnr: Annotated[
        str,
        typer.Argument(help="Firmenbuchnummer mit Prüfbuchstabe")
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
    Sucht Urkunden zu einer Firma.
    
    Beispiele:
    
        fb suche urkunde 160573m
        
        fb suche urkunde "629 a" -o json
    """
    key = resolve_api_key(api_key)
    
    request = SucheUrkundeRequest(fnr=fnr)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Suche Urkunden für {fnr}...", total=None)
        
        try:
            result = suche_urkunde(key, request)
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    # Ergebnisse extrahieren
    response = extract_response(result, "SUCHEURKUNDERESPONSE")
    ergebnisse = ensure_list(response.get("ERGEBNIS"))
    
    if not ergebnisse:
        print_warning("Keine Urkunden gefunden")
        return
    
    if output == OutputFormat.JSON:
        print_json(ergebnisse)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_urkunden_table(ergebnisse)
