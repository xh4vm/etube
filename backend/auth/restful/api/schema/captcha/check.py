from pydantic import BaseModel, Field


class CaptchaCheckBodyParams(BaseModel):
    """Схема body-параметров страницы проверки каптчи
    ---
    """

    x: str = Field(title='Переменная x')
    answer: str = Field(title='Ответ на задачу')


class CaptchaCheckHeader(BaseModel):
    """Схема заголовков страницы проверки каптчи
    ---
    """

    data_signature: str = Field(title='Подпись данных пользователя', alias='Data-Signature')
    redirect_url: str = Field(title='Адрес для редиректа после прохождения каптчи', alias='Redirect-Url')


class CaptchaCheckResponse(BaseModel):
    """Схема ответа страницы проверки каптчи
    ---
    """

    message: str = Field(title='Сообщение ответа')
    redirect_url: str = Field(title='Адрес для редиректа после прохождения каптчи')
