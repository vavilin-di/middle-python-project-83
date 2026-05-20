__all__ = ["UrlCheckCreate", "UrlCheck", "UrlCheckResult"]

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

from page_analyzer.utilities.string_shortener import shorten_long_string


class UrlCheckCreate(BaseModel):
    """Схема для создания новой проверки URL.

    Используется для валидации входных данных при создании проверки.
    Содержит идентификатор URL, для которого создаётся проверка.

    Attributes:
        url_id (int): Идентификатор URL в базе данных.
    """

    url_id: int


class UrlCheck(BaseModel):
    """Схема для представления данных проверки URL.

    Соответствует записи в таблице `url_checks` базы данных.
    Используется для сериализации данных проверки при отображении.
    Включает кастомные сериализаторы для форматирования полей.

    Attributes:
        id (int): Уникальный идентификатор проверки.
        url_id (int): Идентификатор связанного URL.
        status_code (int | None): HTTP статус код ответа.
        h1 (str | None): Текст первого тега <h1> на странице.
        title (str | None): Заголовок страницы (тег <title>).
        description (str | None): Мета-описание страницы.
        created_at (datetime): Дата и время создания проверки.
    """

    id: int
    url_id: int
    status_code: int | None
    h1: str | None
    title: str | None
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("h1")
    def serialize_h1(self, value: str | None) -> str | None:
        """Сокращает длинный текст заголовка h1"""
        return shorten_long_string(value)

    @field_serializer("title")
    def serialize_title(self, value: str | None) -> str | None:
        """Сокращает длинный текст заголовка страницы"""
        return shorten_long_string(value)

    @field_serializer("description")
    def serialize_description(self, value: str | None) -> str | None:
        """Сокращает длинный текст описания метаданных"""
        return shorten_long_string(value)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        """Форматирует дату создания в строку формата ГГГГ-ММ-ДД"""
        return value.strftime("%Y-%m-%d")


class UrlCheckResult(BaseModel):
    """Схема для результатов проверки веб-сайта.

    Используется утилитой `check_site` для возврата данных,
    полученных при анализе HTML-страницы.
    Все поля обязательны и содержат непустые строки
    (или пустые строки, если элемент не найден).

    Attributes:
        status_code (int): HTTP статус код ответа сервера.
        h1 (str): Текст первого тега <h1> или пустая строка.
        title (str): Заголовок страницы (тег <title>) или пустая строка.
        description (str): Мета-описание страницы или пустая строка.
    """

    status_code: int
    h1: str
    title: str
    description: str
