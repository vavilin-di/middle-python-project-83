__all__ = ["flash_validation_errors"]

from flask import flash
from pydantic_core import ValidationError


def flash_validation_errors(validation_error: ValidationError, prefix: str | None = None) -> None:
    """Вспомогательная функция для отображения ошибок валидации Pydantic с помощью flash-сообщений"""
    message_prefix = "" if prefix is None else f"{prefix}: "
    for error in validation_error.errors():
        flash(f"{message_prefix}{error['msg']}.", "error")
