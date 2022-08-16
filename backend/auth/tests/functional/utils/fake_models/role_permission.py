from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field

from .base import get_new_id


class FakeRolePermission(BaseModel):
    id: str = Field(default_factory=get_new_id)
    role_id: str = Field(default_factory=get_new_id)
    permission_id: str = Field(default_factory=get_new_id)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
