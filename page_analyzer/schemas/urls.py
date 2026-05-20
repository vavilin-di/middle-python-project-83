__all__ = ["UrlCreate", "Url", "UrlList"]

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer, field_validator

from page_analyzer.schemas.url_checks import UrlCheck


class UrlCreate(BaseModel):
    """Схема для создания URL.

    Используется для валидации входных данных при добавлении нового URL.

    Attributes:
        name (HttpUrl): URL-адрес. Максимальная длина 255 символов.
    """

    name: HttpUrl = Field(max_length=255)

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: HttpUrl) -> HttpUrl:
        return HttpUrl.build(scheme=value.scheme, host=value.host, port=value.port)  # type: ignore


class Url(BaseModel):
    """Схема для представления URL с проверками.

    Используется для сериализации данных URL, полученных из базы данных.

    Attributes:
        id (int): Уникальный идентификатор URL.
        name (HttpUrl): URL-адрес.
        created_at (datetime): Дата и время создания записи.
        checks (list[UrlCheck]): Список проверок URL (по умолчанию пустой).
    """

    id: int
    name: HttpUrl
    created_at: datetime
    checks: list[UrlCheck] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")


class UrlList(BaseModel):
    """Схема для отображения списка URL.

    Используется для вывода списка URL с информацией о последней проверке.

    Attributes:
        id (int): Уникальный идентификатор URL.
        name (HttpUrl): URL-адрес.
        last_check (datetime | None): Дата и время последней проверки.
        status_code (int | None): HTTP-статус последней проверки.
    """

    id: int
    name: HttpUrl
    last_check: datetime | None
    status_code: int | None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("last_check")
    def serialize_last_check(self, value: datetime | None) -> str | None:
        return None if value is None else value.strftime("%Y-%m-%d")
