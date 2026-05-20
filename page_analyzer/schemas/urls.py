__all__ = ["UrlCreate", "Url", "UrlList"]

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer, field_validator

from page_analyzer.schemas.url_checks import UrlCheck


class UrlCreate(BaseModel):
    name: HttpUrl = Field(max_length=255)

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, value: HttpUrl) -> HttpUrl:
        return HttpUrl.build(scheme=value.scheme, host=value.host, port=value.port)  # type: ignore


class Url(BaseModel):
    id: int
    name: HttpUrl
    created_at: datetime
    checks: list[UrlCheck] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")


class UrlList(BaseModel):
    id: int
    name: HttpUrl
    last_check: datetime | None
    status_code: int | None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("last_check")
    def serialize_last_check(self, value: datetime | None) -> str | None:
        return None if value is None else value.strftime("%Y-%m-%d")
