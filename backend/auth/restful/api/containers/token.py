from typing import Optional, Type
from dependency_injector import providers

from ..services.token.base import BaseTokenService


class TokenFactory(providers.Factory):
    provided_type: Optional[Type] = BaseTokenService
