"""Config-Befehle für API-Key Management."""

from typing import Annotated, Optional

import typer
from rich.prompt import Prompt

from ..config_store import (
    delete_config,
    get_api_key_from_config,
    get_config_file,
    save_api_key_to_config,
)
from ..console import console, print_error, print_info, print_success, print_warning

app = typer.Typer(help="Konfiguration verwalten")


@app.command("set-key")
def set_key(
    api_key: Annotated[
        Optional[str],
        typer.Argument(help="Der API-Key (wird interaktiv abgefragt wenn nicht angegeben)")
    ] = None,
) -> None:
    """Speichert den API-Key für zukünftige Aufrufe."""
    if api_key is None:
        api_key = Prompt.ask(
            "[cyan]API-Key eingeben[/cyan]",
            password=True,
            console=console
        )
    
    if not api_key:
        print_error("API-Key darf nicht leer sein")
        raise typer.Exit(1)
    
    save_api_key_to_config(api_key)
    print_success(f"API-Key gespeichert in {get_config_file()}")


@app.command("show")
def show() -> None:
    """Zeigt die aktuelle Konfiguration."""
    config_file = get_config_file()
    
    console.print("\n[bold]📁 Konfiguration[/bold]\n")
    
    if config_file.exists():
        api_key = get_api_key_from_config()
        if api_key:
            masked = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
            console.print(f"  [dim]Config-Datei:[/dim] {config_file}")
            console.print(f"  [dim]API-Key:[/dim] {masked}")
        else:
            print_warning("Keine API-Key in Config gefunden")
    else:
        print_info(f"Keine Config-Datei gefunden: {config_file}")
        print_info("Nutze 'fb config set-key' um einen API-Key zu setzen")


@app.command("path")
def show_path() -> None:
    """Zeigt den Pfad zur Config-Datei."""
    console.print(str(get_config_file()))


@app.command("delete")
def delete(
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Ohne Bestätigung löschen")
    ] = False,
) -> None:
    """Löscht die gespeicherte Konfiguration."""
    config_file = get_config_file()
    
    if not config_file.exists():
        print_info("Keine Konfiguration vorhanden")
        return
    
    if not force:
        confirm = Prompt.ask(
            "[yellow]Konfiguration wirklich löschen?[/yellow]",
            choices=["y", "n"],
            default="n",
            console=console
        )
        if confirm != "y":
            print_info("Abgebrochen")
            return
    
    delete_config()
    print_success("Konfiguration gelöscht")
