__all__ = ["shorten_long_string"]
MAX_TEXT_LENGTH = 200


def shorten_long_string(value: str | None) -> str | None:
    if value is None or len(value) <= MAX_TEXT_LENGTH:
        return value
    return value[:MAX_TEXT_LENGTH] + "..."
