"""Firmenbuch WebServices API CLI"""

import json
from datetime import date
from typing import Optional

import click

from .config import API_KEY
from .models.request_models import (
    AuszugRequest,
    AuszugUmfang,
    SucheFirmaRequest,
    SucheUrkundeRequest,
    UrkundeRequest,
    VeraenderungArt,
    VeraenderungenFirmaRequest,
    VeraenderungenUrkundeRequest,
)
from .services.auszug import (
    get_auszug,
    get_urkunde,
    get_veraenderungen_firma,
    get_veraenderungen_urkunde,
    suche_firma,
    suche_urkunde,
)


def get_api_key(ctx: click.Context, param: click.Parameter, value: str) -> str:
    """Validiert den API-Key und gibt den aus der Konfiguration zurück, wenn keiner übergeben wurde."""
    if not value and not API_KEY:
        raise click.UsageError(
            "API-Key muss als Umgebungsvariable FIRMENBUCH_API_KEY gesetzt sein"
        )
    return value or API_KEY


@click.command()
@click.option(
    "--api-key",
    callback=get_api_key,
    expose_value=False,
    help="Der API-Schlüssel für die Authentifizierung (optional, wenn FIRMENBUCH_API_KEY gesetzt ist)",
)
@click.option(
    "--fnr", required=True, help='Firmenbuchnummer mit Prüfbuchstaben (z.B. "000187a")'
)
@click.option(
    "--stichtag",
    required=True,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Datum für den Auszug (YYYY-MM-DD)",
)
@click.option(
    "--umfang",
    type=click.Choice([e.value for e in AuszugUmfang]),
    default=AuszugUmfang.KURZINFORMATION.value,
    help="Art des Auszugs (aktueller Auszug oder historischer Auszug)",
)
def get_auszug_cli(fnr: str, stichtag: date, umfang: str) -> None:
    """Ruft einen Firmenbuchauszug ab."""
    # Konvertiere den String-Wert in das entsprechende Enum
    umfang_enum = AuszugUmfang(umfang)
    request = AuszugRequest(fnr=fnr, stichtag=stichtag, umfang=umfang_enum)
    result = get_auszug(API_KEY, request)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@click.command()
@click.option(
    "--api-key", required=True, help="Der API-Schlüssel für die Authentifizierung"
)
@click.option(
    "--firmenwortlaut",
    required=True,
    help="Name der Firma (mit * für Teilübereinstimmungen)",
)
@click.option(
    "--exaktesuche",
    is_flag=True,
    help="True für exakte Suche, False für phonetische Suche",
)
@click.option(
    "--suchbereich", required=True, type=click.IntRange(1, 6), help="Suchbereich (1-6)"
)
@click.option("--gericht", help="3-stellige Gerichtsnummer")
@click.option("--rechtsform", help='3-stellige Rechtsform (z.B. "GES")')
@click.option("--rechtseigenschaft", help="Spezielle Rechtseigenschaft")
@click.option(
    "--ortnr",
    help="Ortsnummer (5-stellig für Gemeinde, 3-stellig für Bezirk, 1-stellig für Bundesland)",
)
def suche_firma_cli(
    api_key: str,
    firmenwortlaut: str,
    exaktesuche: bool,
    suchbereich: int,
    gericht: Optional[str],
    rechtsform: Optional[str],
    rechtseigenschaft: Optional[str],
    ortnr: Optional[str],
) -> None:
    """Sucht nach Firmen im Firmenbuch."""
    request = SucheFirmaRequest(
        firmenwortlaut=firmenwortlaut,
        exaktesuche=exaktesuche,
        suchbereich=suchbereich,
        gericht=gericht,
        rechtsform=rechtsform,
        rechtseigenschaft=rechtseigenschaft,
        ortnr=ortnr,
    )
    result = suche_firma(api_key, request)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@click.command()
@click.option(
    "--api-key", required=True, help="Der API-Schlüssel für die Authentifizierung"
)
@click.option("--fnr", help="Firmenbuchnummer mit Prüfbuchstaben")
@click.option("--az", help="Aktenzeichen")
def suche_urkunde_cli(api_key: str, fnr: Optional[str], az: Optional[str]) -> None:
    """Sucht nach Urkunden im Firmenbuch."""
    request = SucheUrkundeRequest(fnr=fnr, az=az)
    result = suche_urkunde(api_key, request)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@click.command()
@click.option(
    "--api-key", required=True, help="Der API-Schlüssel für die Authentifizierung"
)
@click.option(
    "--von",
    required=True,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Beginndatum (YYYY-MM-DD)",
)
@click.option(
    "--bis",
    required=True,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Enddatum (YYYY-MM-DD)",
)
@click.option("--gericht", help="3-stellige Gerichtsnummer")
@click.option("--rechtsform", help="3-stellige Rechtsform")
@click.option(
    "--art-der-veraenderung",
    type=click.Choice([e.value for e in VeraenderungArt]),
    help="Art der Veränderung",
)
def get_veraenderungen_firma_cli(
    api_key: str,
    von: date,
    bis: date,
    gericht: Optional[str],
    rechtsform: Optional[str],
    art_der_veraenderung: Optional[str],
) -> None:
    """Ruft Firmenveränderungen für einen Zeitraum ab."""
    request = VeraenderungenFirmaRequest(
        von=von,
        bis=bis,
        gericht=gericht,
        rechtsform=rechtsform,
        art_der_veraenderung=art_der_veraenderung,
    )
    result = get_veraenderungen_firma(api_key, request)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@click.command()
@click.option(
    "--api-key", required=True, help="Der API-Schlüssel für die Authentifizierung"
)
@click.option("--fnr", required=True, help="Firmenbuchnummer mit Prüfbuchstaben")
def get_veraenderungen_urkunde_cli(api_key: str, fnr: str) -> None:
    """Ruft Urkundenveränderungen ab."""
    request = VeraenderungenUrkundeRequest(fnr=fnr)
    result = get_veraenderungen_urkunde(api_key, request)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@click.command()
@click.option(
    "--api-key", required=True, help="Der API-Schlüssel für die Authentifizierung"
)
@click.option("--fnr", required=True, help="Firmenbuchnummer mit Prüfbuchstaben")
@click.option("--az", required=True, help="Aktenzeichen")
def get_urkunde_cli(api_key: str, fnr: str, az: str) -> None:
    """Ruft eine spezifische Urkunde ab."""
    request = UrkundeRequest(fnr=fnr, az=az)
    result = get_urkunde(api_key, request)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


# Hauptgruppe für alle Befehle
@click.group()
def cli():
    """Firmenbuch WebServices API CLI"""
    pass


# Befehle zur Hauptgruppe hinzufügen
cli.add_command(get_auszug_cli, name="auszug")
cli.add_command(suche_firma_cli, name="suche-firma")
cli.add_command(suche_urkunde_cli, name="suche-urkunde")
cli.add_command(get_veraenderungen_firma_cli, name="veraenderungen-firma")
cli.add_command(get_veraenderungen_urkunde_cli, name="veraenderungen-urkunde")
cli.add_command(get_urkunde_cli, name="urkunde")


if __name__ == "__main__":
    cli()
