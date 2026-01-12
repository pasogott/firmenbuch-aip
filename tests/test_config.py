from pathlib import Path

from firmenbuch_api_oesterreich.config import get_env_api_key, load_env_file


def test_load_env_file_reads_key(tmp_path: Path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("FIRMENBUCH_API_KEY=TESTKEY\n")

    # Clear env first
    monkeypatch.delenv("FIRMENBUCH_API_KEY", raising=False)

    load_env_file(env_file)
    assert get_env_api_key() == "TESTKEY"
