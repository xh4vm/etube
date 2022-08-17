"""
Контейнер сервисов регистрации пользователя.

"""

from typing import Optional, Type

from dependency_injector import containers, providers

from ..services.action.sign_up.base import BaseSignUpService
from ..services.action.sign_up.sign_up import SignUpService
from .base import BaseContainer


class SignUpFactory(providers.Factory):
    provided_type: Optional[Type] = BaseSignUpService


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..endpoint.action'])
    sign_up_service = SignUpFactory(SignUpService)
