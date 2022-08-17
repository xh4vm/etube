from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field

from .base import fake, get_new_id


class FakePermission(BaseModel):
    id: str = Field(default_factory=get_new_id)
    title: str = Field(default_factory=fake.uri_page)
    description: str = Field(default_factory=fake.paragraphs(nb=1))
    http_method: str = Field(default_factory=fake.http_method)
    url: str = Field(default_factory=fake.url)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
