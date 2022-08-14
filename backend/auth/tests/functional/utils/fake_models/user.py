from typing import Any
from werkzeug.security import generate_password_hash

from pydantic import BaseModel, Field

from .base import fake, get_new_id



class FakeUser(BaseModel):
    id: str = Field(default_factory=get_new_id)
    login: str = Field(default_factory=fake.user_name)
    password: str = Field(default_factory=fake.password)
    email: str = Field(default_factory=fake.email)

    def __init__(self, **data: dict[str, Any]):
        data['password'] = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
        super().__init__(**data)
