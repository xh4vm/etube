from datetime import datetime

from pydantic import BaseModel, Field

from .base import fake, get_new_id


class FakeSignInHistory(BaseModel):
    id: str = Field(default_factory=get_new_id)
    user_id: str = Field(default_factory=get_new_id)
    os: str = Field(default_factory=fake.linux_platform_token)
    device: str = Field(default_factory=fake.android_platform_token)
    browser: str = Field(default_factory=fake.chrome)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
