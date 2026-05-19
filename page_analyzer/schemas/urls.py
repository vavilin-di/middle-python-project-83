from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from page_analyzer.schemas.url_checks import UrlCheck


class UrlCreate(BaseModel):
    name: HttpUrl = Field(max_length=255)


class Url(BaseModel):
    id: int
    name: HttpUrl
    created_at: datetime
    checks: list[UrlCheck] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class UrlList(BaseModel):
    id: int
    name: HttpUrl
    last_check: datetime | None
    status_code: int | None

    model_config = ConfigDict(from_attributes=True)
