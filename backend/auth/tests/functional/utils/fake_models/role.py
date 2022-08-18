from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field

from .base import fake, get_new_id


class FakeRole(BaseModel):
    id: str = Field(default_factory=get_new_id)
    title: str = Field(default_factory=fake.uri_page)
    description: str = Field(default_factory=fake.paragraphs(nb=1))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
