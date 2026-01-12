from datetime import date

import pytest

from firmenbuch_api_oesterreich.models.request_models import (
    SucheUrkundeRequest,
    UrkundeRequest,
    VeraenderungenUrkundeRequest,
)


def test_suche_urkunde_requires_fnr_or_az():
    with pytest.raises(ValueError):
        SucheUrkundeRequest()

    SucheUrkundeRequest(fnr="123a")
    SucheUrkundeRequest(az="AZ 1")


def test_urkunde_request_accepts_key_or_fnr_az():
    UrkundeRequest(key="KEY123")
    UrkundeRequest(fnr="123a", az="AZ 1")

    with pytest.raises(ValueError):
        UrkundeRequest(fnr="123a")


def test_veraenderungen_urkunde_date_range():
    with pytest.raises(ValueError):
        VeraenderungenUrkundeRequest(von=date(2024, 1, 2), bis=date(2024, 1, 1))

    VeraenderungenUrkundeRequest(von=date(2024, 1, 1), bis=date(2024, 1, 2))
