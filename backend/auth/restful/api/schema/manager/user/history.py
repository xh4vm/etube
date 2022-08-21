from api.schema.base import AuthorizationHeader, SignInRecord
from pydantic import BaseModel, Field

from api.schema.base import Page, Paginator


class GetHistoryUserQuery(Paginator):
    """Схема запроса получения истории входа
    ---
    """

    pass


class GetHistoryUserResponse(BaseModel):
    """Схема ответа получения истории входа
    ---
    """

    __root__: Page[SignInRecord] = Field(title='История входа пользователя')


class GetHistoryUserHeader(AuthorizationHeader):
    """Схема заголовков получения истории входа
    ---
    """

    pass
