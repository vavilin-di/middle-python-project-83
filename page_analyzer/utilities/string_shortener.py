__all__ = ["shorten_long_string"]

MAX_TEXT_LENGTH = 200


def shorten_long_string(value: str | None) -> str | None:
    """Укорачивает длинную строку, добавляя многоточие в конце.

    Если строка превышает MAX_TEXT_LENGTH символов, она обрезается до
    MAX_TEXT_LENGTH символов с добавлением '...' в конце. Если строка
    короче или равна MAX_TEXT_LENGTH, возвращается без изменений.
    Если передано None, возвращается None.

    Args:
        value (str | None): Исходная строка для усечения или None.

    Returns:
        str | None: Усечённая строка с '...' на конце, если была длиннее
        MAX_TEXT_LENGTH, иначе исходная строка или None.

    Examples:
        >>> shorten_long_string("Короткая")
        'Короткая'
        >>> shorten_long_string("Очень длинная строка, которая точно превышает лимит в двести символов, потому что она очень длинная и содержит много лишних слов, которые не нужны для отображения в интерфейсе пользователя.")
        'Очень длинная строка, которая точно превышает лимит в двести символов, потому что она очень длинная и содержит много лишних слов, которые не нужны для отображения в интерфейсе...'
        >>> shorten_long_string(None) is None
        True
    """
    if value is None or len(value) <= MAX_TEXT_LENGTH:
        return value
    return value[:MAX_TEXT_LENGTH] + "..."
