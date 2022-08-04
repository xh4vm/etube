from pydantic import BaseModel, Field

from .base import fake, get_new_id


class FakeGenreBrief(BaseModel):
    id: str = Field(default_factory=get_new_id)
    name: str = Field(default_factory=fake.name)


class FakeGenreFull(FakeGenreBrief):
    description: str = Field(default_factory=fake.text)
