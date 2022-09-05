from pydantic import BaseModel, Field


class CaptchaCheckBodyParams(BaseModel):
    """Схема body-параметров страницы проверки капчи
    ---
    """

    parameter: str = Field(title='Параметр задачи')
    message: str = Field(title='Текст задачи')
    answer: str = Field(title='Ответ на задачу')


class CaptchaCheckHeader(BaseModel):
    """Схема заголовков страницы проверки капчи
    ---
    """

    data_signature: str = Field(title='Подпись данных пользователя', alias='Data-Signature')
    redirect_url: str = Field(title='Адрес для редиректа после прохождения капчи', alias='Redirect-Url')
    redirect_data: str = Field(
        title='Зашифрованная информация, которую нужно отправить на следующую страницу', alias='Redirect-Data',
    )


class CaptchaCheckResponse(BaseModel):
    """Схема ответа страницы проверки капчи
    ---
    """

    message: str = Field(title='Сообщение ответа')
    redirect_url: str = Field(title='Адрес для редиректа после прохождения капчи')
    redirect_data: str = Field(title='Зашифрованная информация, которую нужно отправить на следующую страницу')
