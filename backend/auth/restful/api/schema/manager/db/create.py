from datetime import date

from pydantic import BaseModel, Field


class DbBodyParams(BaseModel):
    target_date: date = Field(title='Today')

class DbResponse(BaseModel):
    message: str = Field(title='Message')
