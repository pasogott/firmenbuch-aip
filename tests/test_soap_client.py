from firmenbuch_api_oesterreich.services.soap_client import build_envelope


def test_build_envelope_includes_namespace_and_body():
    body = "  <fb:TEST>ok</fb:TEST>"
    envelope = build_envelope("ns://example", body)

    assert "ns://example" in envelope
    assert "<fb:TEST>ok</fb:TEST>" in envelope
    assert envelope.startswith("<?xml")
    assert "<soap:Envelope" in envelope
