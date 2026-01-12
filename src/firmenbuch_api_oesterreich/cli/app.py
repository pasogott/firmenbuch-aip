"""Firmenbuch CLI - Hauptapplikation."""

import typer
from rich.console import Console
from rich.panel import Panel

from .commands import auszug, config, suche, urkunde, veraenderungen

# Haupt-App
app = typer.Typer(
    name="fb",
    help="🇦🇹 Firmenbuch CLI - Zugriff auf das österreichische Firmenbuch",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)

# Sub-Commands registrieren
app.add_typer(config.app, name="config")
app.add_typer(auszug.app, name="auszug")
app.add_typer(suche.app, name="suche")
app.add_typer(urkunde.app, name="urkunde")
app.add_typer(veraenderungen.app, name="veraenderungen")


@app.command("version")
def version() -> None:
    """Zeigt die Version an."""
    console = Console()
    console.print("[bold]firmenbuch-cli[/bold] v0.2.0")


@app.command("info")
def info() -> None:
    """Zeigt Informationen zur API und wie man einen API-Key bekommt."""
    console = Console()
    
    console.print(Panel(
        "[bold cyan]🇦🇹 Firmenbuch WebServices API[/bold cyan]\n\n"
        "Zugriff auf das österreichische Firmenbuch über die\n"
        "offiziellen High-Value Dataset (HVD) WebServices.\n\n"
        "[dim]Basis-URL:[/dim] https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws",
        title="ℹ️  Info",
        border_style="blue"
    ))
    
    console.print("\n[bold]🔑 API-Key erhalten[/bold]\n")
    console.print("  1. Gehe zu [link=https://www.justiz.gv.at/service/datenschutz/justizonline-api.2c94848b8b511b7a018c6a8e30e1045c.de.html]justiz.gv.at API-Registrierung[/link]")
    console.print("  2. Registriere dich für die Firmenbuch-API")
    console.print("  3. Speichere deinen Key mit: [cyan]fb config set-key[/cyan]")
    
    console.print("\n[bold]📚 Dokumentation[/bold]\n")
    console.print("  • API-Docs: [link=https://github.com/pasogott/firmenbuch-aip/tree/main/docs]github.com/pasogott/firmenbuch-aip/docs[/link]")
    console.print("  • WSDL: [link=https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl]justizonline.gv.at/.../fbw.wsdl[/link]")
    
    console.print("\n[bold]🚀 Schnellstart[/bold]\n")
    console.print("  [dim]# API-Key setzen[/dim]")
    console.print("  fb config set-key\n")
    console.print("  [dim]# Firma suchen[/dim]")
    console.print("  fb suche firma \"Musterfirma*\"\n")
    console.print("  [dim]# Firmenbuchauszug abrufen[/dim]")
    console.print("  fb auszug 160573m\n")


def main() -> None:
    """Einstiegspunkt für die CLI."""
    app()


if __name__ == "__main__":
    main()
