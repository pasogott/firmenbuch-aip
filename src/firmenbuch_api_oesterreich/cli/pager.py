"""Pagination helper for CLI output."""

from typing import Iterable, List


def paginate(items: List, limit: int, offset: int) -> List:
    """Applies limit/offset to a list of items."""
    if offset < 0:
        offset = 0
    if limit is None or limit <= 0:
        return items[offset:]
    return items[offset : offset + limit]
