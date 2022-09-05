import hashlib
import hmac
from math import tan

import orjson
from pydantic import BaseModel, Field

from .base import fake


class FakeCaptchaTask(BaseModel):
    message: str = Field(title='Текст задания', default='Вычислите тангенс угла')
    parameter: int = Field(title='Параметр задачи', default_factory=fake.random_int)
    answer: float = Field(title='Ответ задачи')

    def __init__(self, *args, **kwargs) -> None:
        kwargs['answer'] = kwargs.get('answer') or round(tan(int(kwargs['parameter']) + 1), 3)
        super().__init__(*args, **kwargs)

    def sig(self, secret: str) -> str:
        packed_data = str(orjson.dumps(self.dict()))
        return hmac.new(bytes(secret, 'utf-8'), msg=bytes(packed_data, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

    def sig_check(self, secret: str, signature: str) -> bool:
        return signature == self.sig(secret)
