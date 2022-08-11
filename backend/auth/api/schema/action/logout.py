from pydantic import BaseModel, Field
from ..base import AuthorizationHeader, JWT, BaseError


class LogoutBodyParams(BaseModel):
    access_token: str = Field(title='Кратковременный jwt токен')


class LogoutResponse(BaseModel):
    pass


class LogoutHeader(AuthorizationHeader):
    pass
