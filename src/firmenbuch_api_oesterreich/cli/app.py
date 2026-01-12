"""Firmenbuch CLI - Hauptapplikation."""

from enum import Enum
from pathlib import Path

import click
import typer
from rich.console import Console
from rich.panel import Panel

from ..config import load_env_file
from .commands import auszug, config, doctor, suche, urkunde, veraenderungen

# Haupt-App
app = typer.Typer(
    name="firmenbuchat",
    help="🇦🇹 Firmenbuch CLI - Zugriff auf das österreichische Firmenbuch",
    no_args_is_help=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)


@app.callback()
def main_callback(
    env_file: Path | None = typer.Option(
        None,
        "--env-file",
        "-e",
        help="Pfad zu einer .env Datei (überschreibt FIRMENBUCH_API_KEY)",
    ),
) -> None:
    """Globale Optionen laden."""
    if env_file:
        load_env_file(env_file)


# Sub-Commands registrieren
app.add_typer(config.app, name="config")
app.add_typer(auszug.app, name="auszug")
app.add_typer(suche.app, name="suche")
app.add_typer(urkunde.app, name="urkunde")
app.add_typer(veraenderungen.app, name="veraenderungen")
app.add_typer(doctor.app, name="doctor")


def _collect_commands(command: click.Command, info_name: str) -> list[tuple[str, click.Command]]:
    sections = [(info_name, command)]

    if isinstance(command, click.Group):
        for name, subcommand in command.commands.items():
            sections.extend(_collect_commands(subcommand, f"{info_name} {name}"))

    return sections


def _format_param_type(param: click.Parameter) -> str:
    param_type = getattr(param.type, "name", None) or str(param.type)
    if hasattr(param.type, "choices"):
        choices = ", ".join(param.type.choices)
        return f"{param_type} ({choices})"
    return param_type


def _format_default(value: object) -> str:
    if isinstance(value, Enum):
        return str(value.value)
    return str(value)


def _format_option(option: click.Option) -> str:
    flags = ", ".join([*option.opts, *option.secondary_opts])
    help_text = option.help or ""
    default = ""

    if option.show_default and option.default not in (None, (), False):
        default = f" [default: {_format_default(option.default)}]"

    envvar = option.envvar if isinstance(option.envvar, str) else None
    envvar_text = f" [env: {envvar}]" if envvar else ""
    return f"- {flags} ({_format_param_type(option)}): {help_text}{default}{envvar_text}".rstrip()


def _format_argument(argument: click.Argument) -> str:
    required = " [required]" if argument.required else ""
    help_text = getattr(argument, "help", "") or ""
    suffix = f" {help_text}".rstrip() if help_text else ""
    return f"- {argument.name} ({_format_param_type(argument)}):{required}{suffix}".rstrip()


def _format_help_section(name: str, command: click.Command) -> str:
    lines = [f"=== {name} ==="]
    if command.help:
        lines.append(command.help)

    arguments = [param for param in command.params if isinstance(param, click.Argument)]
    options = [param for param in command.params if isinstance(param, click.Option)]

    if arguments:
        lines.append("Arguments:")
        lines.extend(_format_argument(arg) for arg in arguments)

    if options:
        lines.append("Options:")
        lines.extend(_format_option(opt) for opt in options)

    if isinstance(command, click.Group) and command.commands:
        lines.append("Commands:")
        for sub_name, subcommand in command.commands.items():
            raw_help = subcommand.short_help or subcommand.help or ""
            first_line = raw_help.strip().splitlines()[0] if raw_help.strip() else ""
            lines.append(f"- {sub_name}: {first_line}".rstrip())

    return "\n".join(lines)


@app.command("help")
def help_all() -> None:
    """Zeigt die Hilfe für alle Commands (inkl. Subcommands)."""
    root_name = "firmenbuchat"
    sections: list[str] = []

    for name, command in _collect_commands(typer.main.get_command(app), root_name):
        sections.append(_format_help_section(name, command))

    typer.echo("\n\n".join(sections))


@app.command("version")
def version() -> None:
    """Zeigt die Version an."""
    console = Console()
    console.print("[bold]firmenbuch-cli[/bold] v0.2.0")


@app.command("info")
def info() -> None:
    """Zeigt Informationen zur API und wie man einen API-Key bekommt."""
    console = Console()

    console.print(
        Panel(
            "[bold cyan]🇦🇹 Firmenbuch WebServices API[/bold cyan]\n\n"
            "Zugriff auf das österreichische Firmenbuch über die\n"
            "offiziellen High-Value Dataset (HVD) WebServices.\n\n"
            "[dim]Basis-URL:[/dim] https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws",
            title="ℹ️  Info",
            border_style="blue",
        )
    )

    console.print("\n[bold]🔑 API-Key erhalten[/bold]\n")
    console.print(
        "  1. Gehe zu [link=https://www.justiz.gv.at/service/datenschutz/"
        "justizonline-api.2c94848b8b511b7a018c6a8e30e1045c.de.html]"
        "justiz.gv.at API-Registrierung[/link]"
    )
    console.print("  2. Registriere dich für die Firmenbuch-API")
    console.print("  3. Speichere deinen Key mit: [cyan]firmenbuchat config set-key[/cyan]")

    console.print("\n[bold]📚 Dokumentation[/bold]\n")
    console.print(
        "  • API-Docs: [link=https://github.com/pasogott/firmenbuch-aip/tree/main/docs]github.com/pasogott/firmenbuch-aip/docs[/link]"
    )
    console.print(
        "  • WSDL: [link=https://justizonline.gv.at/jop/api/at.gv.justiz.fbw/ws/fbw.wsdl]justizonline.gv.at/.../fbw.wsdl[/link]"
    )

    console.print("\n[bold]🚀 Schnellstart[/bold]\n")
    console.print("  [dim]# API-Key setzen[/dim]")
    console.print("  firmenbuchat config set-key\n")
    console.print("  [dim]# Firma suchen[/dim]")
    console.print('  firmenbuchat suche firma "Musterfirma*"\n')
    console.print("  [dim]# Firmenbuchauszug abrufen[/dim]")
    console.print("  firmenbuchat auszug 160573m\n")


def main() -> None:
    """Einstiegspunkt für die CLI."""
    app()


if __name__ == "__main__":
    main()
