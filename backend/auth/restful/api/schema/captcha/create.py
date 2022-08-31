from pydantic import BaseModel, Field


class CaptchaCreateHeader(BaseModel):
    """Схема заголовков страницы создания каптчи
    ---
    """

    redirect_url: str = Field(title='Адрес для редиректа после прохождения каптчи', alias='Redirect-Url')
