"""Auszug-Befehl für Firmenbuchauszüge."""

from datetime import datetime
from typing import Annotated, Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from ...models.request_models import AuszugRequest, AuszugUmfang
from ...services.auszug import get_auszug
from ..console import (
    OutputFormat,
    console,
    print_auszug,
    print_error,
    print_json,
)
from .config import get_api_key_from_config

app = typer.Typer(help="Firmenbuchauszüge abrufen")


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


@app.callback(invoke_without_command=True)
def auszug(
    ctx: typer.Context,
    fnr: Annotated[
        str,
        typer.Argument(help="Firmenbuchnummer mit Prüfbuchstabe (z.B. 160573m)")
    ],
    stichtag: Annotated[
        Optional[datetime],
        typer.Option(
            "--stichtag", "-s",
            formats=["%Y-%m-%d"],
            help="Stichtag (YYYY-MM-DD), Standard: heute"
        )
    ] = None,
    umfang: Annotated[
        str,
        typer.Option(
            "--umfang", "-u",
            help="Umfang: Kurzinformation, aktueller Auszug, historischer Auszug"
        )
    ] = "Kurzinformation",
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
    Ruft einen Firmenbuchauszug ab.
    
    Beispiele:
    
        fb auszug 160573m
        
        fb auszug 160573m --stichtag 2024-01-01
        
        fb auszug 160573m -u "aktueller Auszug" -o json
    """
    key = get_api_key(api_key)
    
    # Stichtag default: heute
    if stichtag is None:
        stichtag = datetime.now()
    
    # Umfang zu Enum
    try:
        umfang_enum = AuszugUmfang(umfang)
    except ValueError:
        print_error(f"Ungültiger Umfang: {umfang}")
        raise typer.Exit(1)
    
    request = AuszugRequest(
        fnr=fnr,
        stichtag=stichtag.date() if isinstance(stichtag, datetime) else stichtag,
        umfang=umfang_enum
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Lade Auszug für {fnr}...", total=None)
        
        try:
            result = get_auszug(key, request)
        except Exception as e:
            print_error(str(e))
            raise typer.Exit(1)
    
    if output == OutputFormat.JSON:
        print_json(result)
    elif output == OutputFormat.RAW:
        console.print(result)
    else:
        print_auszug(result)
