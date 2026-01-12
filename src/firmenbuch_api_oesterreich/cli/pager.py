"""Pagination helper for CLI output."""


def paginate(items: list, limit: int, offset: int) -> list:
    """Applies limit/offset to a list of items."""
    if offset < 0:
        offset = 0
    if limit is None or limit <= 0:
        return items[offset:]
    return items[offset : offset + limit]
