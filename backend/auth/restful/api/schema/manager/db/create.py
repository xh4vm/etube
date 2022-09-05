from datetime import date

from pydantic import BaseModel, Field


class DbBodyParams(BaseModel):
    target_date: date = Field(title='Дата, для месяца которой нужно создать таблицу')


class DbResponse(BaseModel):
    message: str = Field(title='Сообщение ответа')
