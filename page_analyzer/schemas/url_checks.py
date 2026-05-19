from datetime import datetime

from pydantic import BaseModel, ConfigDict


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


class UrlCheckResult(BaseModel):
    status_code: int
    h1: str
    title: str
    description: str
