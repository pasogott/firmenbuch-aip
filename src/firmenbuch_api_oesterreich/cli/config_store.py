"""Konfigurationsspeicher für die CLI."""

from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "firmenbuch"
CONFIG_FILE = CONFIG_DIR / "config"


def get_config_file() -> Path:
    """Gibt den Pfad zur Config-Datei zurück."""
    return CONFIG_FILE


def get_api_key_from_config() -> str | None:
    """Liest den API-Key aus der Config-Datei."""
    config_file = get_config_file()
    if not config_file.exists():
        return None

    content = config_file.read_text().strip()
    for line in content.split("\n"):
        if line.startswith("FIRMENBUCH_API_KEY="):
            return line.split("=", 1)[1].strip()
    return None


def save_api_key_to_config(api_key: str) -> None:
    """Speichert den API-Key in der Config-Datei."""
    config_file = get_config_file()
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(f"FIRMENBUCH_API_KEY={api_key}\n")
    config_file.chmod(0o600)


def delete_config() -> None:
    """Löscht die gespeicherte Konfiguration."""
    config_file = get_config_file()
    if config_file.exists():
        config_file.unlink()
