from pydantic import BaseModel, Field
from ..base import AuthorizationHeader, JWT, BaseError


class RefreshTokenBodyParams(BaseModel):
    access_token: str = Field(title='Кратковременный jwt токен')


class RefreshTokenResponse(JWT):
    pass


class RefreshTokenHeader(AuthorizationHeader):
    pass
