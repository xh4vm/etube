"""
Создание и проверка подписи данных.

"""

import hashlib
import hmac

from core.config import OAUTH_CONFIG


def create_signature(data_string: str) -> str:
    message = '{}'.format(data_string)
    return hmac.new(bytes(OAUTH_CONFIG.SECRET, 'utf-8'), msg=bytes(message, 'utf-8'),
                    digestmod=hashlib.sha256).hexdigest()


def check_signature(data_string: str, signature: str) -> bool:
    return signature == create_signature(data_string)

