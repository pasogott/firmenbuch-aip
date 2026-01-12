from firmenbuch_api_oesterreich.cli.common import ensure_list, extract_response


def test_extract_response_returns_nested_body():
    payload = {"Envelope": {"Body": {"TEST": {"value": 1}}}}
    assert extract_response(payload, "TEST") == {"value": 1}


def test_ensure_list_handles_none_dict_list():
    assert ensure_list(None) == []
    assert ensure_list({"a": 1}) == [{"a": 1}]
    assert ensure_list([1, 2]) == [1, 2]
