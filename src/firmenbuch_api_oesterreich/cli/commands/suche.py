"""Such-Befehle für Firmen und Urkunden."""

from typing import Annotated, Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...models.request_models import SucheFirmaRequest, SucheUrkundeRequest
from ...services.auszug import suche_firma, suche_urkunde
from ..console import (
    OutputFormat,
    console,
    print_error,
    print_firma_table,
    print_json,
    print_urkunden_table,
    print_warning,
)
from .config import get_api_key_from_config

app = typer.Typer(help="Firmen und Urkunden suchen")


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
    key = get_api_key(api_key)
    
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
    response = result.get("Envelope", {}).get("Body", {}).get("SUCHEFIRMARESPONSE", {})
    ergebnisse = response.get("ERGEBNIS", [])
    
    # Einzelergebnis in Liste umwandeln
    if isinstance(ergebnisse, dict):
        ergebnisse = [ergebnisse]
    
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
    key = get_api_key(api_key)
    
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
    response = result.get("Envelope", {}).get("Body", {}).get("SUCHEURKUNDERESPONSE", {})
    ergebnisse = response.get("ERGEBNIS", [])
    
    # Einzelergebnis in Liste umwandeln
    if isinstance(ergebnisse, dict):
        ergebnisse = [ergebnisse]
    
    if not ergebnisse:
        print_warning("Keine Urkunden gefunden")
        return
    
    if output == OutputFormat.JSON:
        print_json(ergebnisse)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_urkunden_table(ergebnisse)
