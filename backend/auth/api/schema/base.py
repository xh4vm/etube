from pydantic import BaseModel, Field, validator
from user_agents import parse


class AuthorizationHeader(BaseModel):
    """Схема заголовков JWT авторизации 
    ---
    """

    token: str = Field(
        title='Authorization JWT токен', 
        alias='X-Authorization-Token',
    )

    @validator('token')
    def load_user_agent(cls, token: str):
        if not token.startswith('Bearer '):
            raise ValueError('Bearer authorization токен не найден')
        return token


class UserAgentHeader(BaseModel):
    """Схема заголовков получения / обработки юзерагента пользователя  
    ---
    """

    user_agent: str = Field(
        title='Заголовок User-Agent', 
        alias='User-Agent', 
        example='Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
    )

    @validator('user_agent')
    def load_user_agent(cls, user_agent: str):
        return parse(user_agent)


class JWT(BaseModel):
    """Схема JWT токенаов  
    ---
    """
    
    access: str = Field(title='Кратковременный JWT токен', alias='access_token')
    refresh: str = Field(title='Долговременный JWT токен', alias='refresh_token')


class BaseError(BaseModel):
    """Базования схема ошибки  
    ---
    """
    
    message: str = Field(title='Сообщение об ошибке', default='Error')
    code: int = Field(title='Код ошибки')
