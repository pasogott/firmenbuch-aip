"""Rich console setup and output helpers."""

import json
from enum import Enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Globale Console-Instanz
console = Console()
err_console = Console(stderr=True)


class OutputFormat(str, Enum):
    """Ausgabeformate."""

    TABLE = "table"
    JSON = "json"
    RAW = "raw"


def print_error(message: str, title: str = "Fehler") -> None:
    """Gibt eine Fehlermeldung aus."""
    err_console.print(Panel(Text(message, style="red"), title=f"❌ {title}", border_style="red"))


def print_success(message: str) -> None:
    """Gibt eine Erfolgsmeldung aus."""
    console.print(f"[green]✓[/green] {message}")


def print_warning(message: str) -> None:
    """Gibt eine Warnung aus."""
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_info(message: str) -> None:
    """Gibt eine Info-Meldung aus."""
    console.print(f"[blue]ℹ[/blue] {message}")


def print_json(data: Any) -> None:
    """Gibt Daten als formatiertes JSON aus."""
    console.print_json(json.dumps(data, ensure_ascii=False, default=str))


def create_table(title: str, columns: list[tuple[str, str]]) -> Table:
    """Erstellt eine Rich-Tabelle."""
    table = Table(title=title, show_header=True, header_style="bold cyan")
    for col_name, col_style in columns:
        table.add_column(col_name, style=col_style)
    return table


def print_firma_table(firmen: list[dict], total: int | None = None) -> None:
    """Gibt Firmen als Tabelle aus."""
    total_label = f" / {total}" if total is not None else ""
    table = create_table(
        f"🏢 {len(firmen)} Firmen{total_label}",
        [
            ("FNR", "cyan"),
            ("Name", "white"),
            ("Sitz", "dim"),
            ("Rechtsform", "green"),
            ("Gericht", "dim"),
        ],
    )

    for firma in firmen:
        name = firma.get("NAME", "")
        if isinstance(name, list):
            name = " ".join(name)

        rechtsform = firma.get("RECHTSFORM", {})
        if isinstance(rechtsform, dict):
            rechtsform = rechtsform.get("TEXT", rechtsform.get("CODE", ""))

        gericht = firma.get("GERICHT", {})
        if isinstance(gericht, dict):
            gericht = gericht.get("TEXT", gericht.get("CODE", ""))

        table.add_row(
            firma.get("FNR", ""),
            name,
            firma.get("SITZ", ""),
            rechtsform,
            gericht,
        )

    console.print(table)


def print_urkunden_table(urkunden: list[dict], total: int | None = None) -> None:
    """Gibt Urkunden als Tabelle aus."""
    total_label = f" / {total}" if total is not None else ""
    table = create_table(
        f"📄 {len(urkunden)} Urkunden{total_label}",
        [
            ("Key", "dim"),
            ("Dokumentart", "white"),
            ("Datum", "cyan"),
            ("Typ", "green"),
            ("Größe", "dim"),
        ],
    )

    for urkunde in urkunden:
        dokumentart = urkunde.get("DOKUMENTART", {})
        if isinstance(dokumentart, dict):
            dokumentart = dokumentart.get("TEXT", dokumentart.get("CODE", ""))

        groesse = urkunde.get("GROESSE", "")
        if groesse:
            groesse = f"{int(groesse) / 1024:.1f} KB"

        key = urkunde.get("KEY", "")
        if len(key) > 30:
            key = key[:27] + "..."

        table.add_row(
            key,
            dokumentart,
            urkunde.get("STICHTAG", urkunde.get("EINGEREICHT", "")),
            urkunde.get("DATEIENDUNG", "").upper(),
            groesse,
        )

    console.print(table)


def print_auszug(auszug: dict) -> None:
    """Gibt einen Firmenbuchauszug formatiert aus."""
    response = auszug.get("Envelope", {}).get("Body", {}).get("AUSZUG_V2_RESPONSE", {})

    # Header-Info
    console.print(
        Panel(
            f"[cyan]FNR:[/cyan] {response.get('FNR', 'N/A')}\n"
            f"[cyan]Stichtag:[/cyan] {response.get('STICHTAG', 'N/A')}\n"
            f"[cyan]Umfang:[/cyan] {response.get('UMFANG', 'N/A')}\n"
            f"[cyan]Abfragezeitpunkt:[/cyan] {response.get('ABFRAGEZEITPUNKT', 'N/A')}",
            title="📋 Firmenbuchauszug",
            border_style="blue",
        )
    )

    firma = response.get("FIRMA", {})
    if not firma:
        return

    # Firmenbezeichnung
    bezeichnung = firma.get("FI_DKZ02", {})
    if bezeichnung:
        name_parts = bezeichnung.get("BEZEICHNUNG", [])
        if isinstance(name_parts, str):
            name_parts = [name_parts]
        console.print(f"\n[bold]🏢 {' '.join(name_parts)}[/bold]")

    # Adresse
    adresse = firma.get("FI_DKZ03", {})
    if adresse:
        console.print("\n📍 [dim]Geschäftsanschrift:[/dim]")
        console.print(f"   {adresse.get('STELLE', '')}")
        console.print(f"   {adresse.get('PLZ', '')} {adresse.get('ORT', '')}")


def print_veraenderungen_table(
    veraenderungen: list[dict],
    titel: str = "Veränderungen",
    total: int | None = None,
) -> None:
    """Gibt Veränderungen als Tabelle aus."""
    total_label = f" / {total}" if total is not None else ""
    table = create_table(
        f"📊 {len(veraenderungen)} {titel}{total_label}",
        [
            ("FNR/Key", "cyan"),
            ("Datum", "white"),
            ("Art", "green"),
            ("VNR", "dim"),
        ],
    )

    for v in veraenderungen:
        table.add_row(
            v.get("FNR", v.get("KEY", ""))[:30],
            v.get("VOLLZUGSDATUM", ""),
            v.get("ARTDERVERAENDERUNG", v.get("DOKUMENTART", {}).get("TEXT", "")),
            v.get("VNR", ""),
        )

    console.print(table)
