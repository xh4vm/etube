from pydantic import BaseModel, Field
from ..base import UserAgentHeader, JWT, BaseError


class SignUpBodyParams(BaseModel):
    login: str = Field(title='Login')
    password: str = Field(title='Password')


class SignUpResponse(JWT):
    pass


class SignUpHeader(UserAgentHeader):
    pass
