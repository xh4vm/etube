from datetime import datetime
from typing import Any
import orjson
import hmac
import hashlib

from pydantic import BaseModel, Field, EmailStr
from werkzeug.security import generate_password_hash

from .base import fake, get_new_id


class FakeUser(BaseModel):
    id: str = Field(default_factory=get_new_id)
    login: str = Field(default_factory=fake.user_name)
    password: str = Field(default_factory=fake.password)
    email: str = Field(default_factory=fake.email)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **data: dict[str, Any]):
        data['password'] = generate_password_hash(
            data.get('password') or fake.password(), method='pbkdf2:sha256', salt_length=16
        )
        super().__init__(**data)


class FakeUserSocial(BaseModel):
    user_service_id: str = Field(title='Идентификатор пользователя в соц сервисе', default_factory=get_new_id)
    email: EmailStr = Field(title='Email пользователя', default_factory=fake.email)
    service_name: str = Field(title='Название сервиса', default='yandex')

    def sig(self, secret: str) -> str:
        packed_data = str(orjson.dumps(self.dict()))
        return hmac.new(bytes(secret, 'utf-8'), msg=bytes(packed_data, 'utf-8'),
                    digestmod=hashlib.sha256).hexdigest()
