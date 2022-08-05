import enum
from typing import Any, Generic, Optional, TypeVar

import orjson
from fastapi import Query
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from src.core.config import CONFIG


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JSONModel(GenericModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ModelClass(JSONModel):
    id: str


class StrEnum(str, enum.Enum):
    @classmethod
    def find_elem(cls, value: Any) -> Optional[enum.Enum]:
        for e in cls:
            if e.value == value:
                return e
        return None


PTYPE = TypeVar('PTYPE', bound=BaseModel)


class PageModel(JSONModel, Generic[PTYPE]):

    next_page: Optional[int] = Field(title='Номер следующей страницы', example=3)
    prev_page: Optional[int] = Field(title='Номер предыдущей страницы', example=1)
    page: Optional[int] = Field(default=CONFIG.APP.page, title='Номер текущей страницы', example=2)
    page_size: Optional[int] = Field(default=CONFIG.APP.page_size, title='Длина выборки', example=2)
    total: Optional[int] = Field(default=0, title='Общая мощность выборки', example=1000)
    items: list[PTYPE] = Field(default=[], title='Список объектов', example=[])


class Paginator(BaseModel):
    page: int = Query(default=CONFIG.APP.page, title='Номер текущей страницы', ge=1)
    page_size: int = Query(default=CONFIG.APP.page_size, title='Длина выборки', ge=1, le=500)
