from firmenbuch_api_oesterreich.cli.pager import paginate


def test_paginate_handles_offset_and_limit():
    items = [1, 2, 3, 4, 5]

    assert paginate(items, limit=2, offset=0) == [1, 2]
    assert paginate(items, limit=2, offset=2) == [3, 4]
    assert paginate(items, limit=0, offset=3) == [4, 5]
