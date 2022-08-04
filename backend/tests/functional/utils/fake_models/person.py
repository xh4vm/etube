from pydantic import BaseModel, Field

from .base import fake, get_new_id


class FakePersonBrief(BaseModel):
    id: str = Field(default_factory=get_new_id)
    name: str = Field(default_factory=fake.name)


class FakePersonFull(FakePersonBrief):
    pass
