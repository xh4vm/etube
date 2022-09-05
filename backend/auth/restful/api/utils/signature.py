"""
Создание и проверка подписи данных.

"""

import hashlib
import hmac

from core.config import OAUTH_CONFIG


def create_signature(data: str) -> str:
    return hmac.new(bytes(OAUTH_CONFIG.SECRET, 'utf-8'), msg=bytes(data, 'utf-8'),
                    digestmod=hashlib.sha256).hexdigest()


def check_signature(data: str, signature: str) -> bool:
    return signature == create_signature(data)
