from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class UrlCreate(BaseModel):
    name: HttpUrl = Field(max_length=255)


class Url(BaseModel):
    id: int
    name: HttpUrl
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
