from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

MAX_DESCRIPTION_LENGTH = 200


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

    @field_serializer("description")
    def serialize_description(self, value: str | None) -> str | None:
        if value is None or len(value) <= MAX_DESCRIPTION_LENGTH:
            return value
        return value[:MAX_DESCRIPTION_LENGTH] + "..."

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d")


class UrlCheckResult(BaseModel):
    status_code: int
    h1: str
    title: str
    description: str
