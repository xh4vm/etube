from ..base import JWT, AuthorizationHeader


class RefreshTokenResponse(JWT):
    """Схема ответа обновления токена
    ---
    """

    pass


class RefreshTokenHeader(AuthorizationHeader):
    """Схема заголовков обновления токена
    ---
    """

    pass
