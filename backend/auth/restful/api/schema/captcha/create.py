from pydantic import BaseModel, Field


class CaptchaCreateHeader(BaseModel):
    """Схема заголовка страницы создания капчи
    ---
    """

    redirect_url: str = Field(title='Адрес для редиректа после прохождения капчи', alias='Redirect-Url')
    redirect_data: str = Field(
        title='Зашифрованная информация, которую нужно отправить на следующую страницу', alias='Redirect-Data',
    )
