from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

from page_analyzer.utilities.string_shortener import shorten_long_string


class UrlCheckCreate(BaseModel):
    url_id: int


class UrlCheck(BaseModel):
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
        return shorten_long_string(value)

    @field_serializer("title")
    def serialize_title(self, value: str | None) -> str | None:
        return shorten_long_string(value)

    @field_serializer("description")
    def serialize_description(self, value: str | None) -> str | None:
        return shorten_long_string(value)

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")


class UrlCheckResult(BaseModel):
    status_code: int
    h1: str
    title: str
    description: str
