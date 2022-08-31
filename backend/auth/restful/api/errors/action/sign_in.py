class SignInActionError:
    NOT_VALID_AUTH_DATA = 'Неверный логин или пароль'
    ALREADY_AUTH = 'Вы уже авторизованы'
    NOT_VALID_OAUTH_DATA = 'Неверный код авторизации'
    SIGNATURE_DOES_NOT_EXIST = 'Отсутствует подпись данных'
    NOT_VALID_SIGNATURE = 'Неправильная подпись данных'
