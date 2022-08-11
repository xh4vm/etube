from pydantic import BaseModel, Field
from ..base import UserAgentHeader, JWT, BaseError


class SignInBodyParams(BaseModel):
    login: str = Field(title='Login')
    password: str = Field(title='Password')


class SignInResponse(JWT):
    pass


class SignInHeader(UserAgentHeader):
    pass
