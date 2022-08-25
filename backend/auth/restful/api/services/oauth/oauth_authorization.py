
from urllib.parse import urlencode

import requests
from flask import redirect, Response
from requests import post, request

from .base import BaseOAuthAuthorization
from core.config import OAUTH_CONFIG


class YandexAuth(BaseOAuthAuthorization):

    def get_permission_code(self) -> Response:
        # Если скрипт был вызван без указания параметра "code",
        # то пользователь перенаправляется на страницу запроса доступа.
        # После предоставления доступа он возвращается на эту же страницу, но
        # уже с кодом доступа, по которому можно получить токены.
        return redirect(
            OAUTH_CONFIG.YANDEX.BASEURL + "authorize?response_type=code&client_id={}".format(
                OAUTH_CONFIG.YANDEX.CLIENT_ID
            )
        )

    def get_api_tokens(self, request: request) -> str:
        # Получение токенов от стороннего сервиса.
        # Токены используются для запроса к Api.
        data = {
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),
            'client_id': OAUTH_CONFIG.YANDEX.CLIENT_ID,
            'client_secret': OAUTH_CONFIG.YANDEX.CLIENT_SECRET,
        }
        data = urlencode(data)
        response = post(OAUTH_CONFIG.YANDEX.BASEURL + "token", data).json()
        api_access_token: str = response.get('access_token')

        return api_access_token

    def get_api_data(self, access_token: str) -> dict:
        # Получение данных пользователя от Api.
        response = requests.get(
            'https://login.yandex.ru/info',
            headers={'Authorization': f'OAuth {access_token}'},
        ).json()
        user_service_id = response.get('id')
        email = response.get('default_email')

        return {'user_service_id': user_service_id, 'email': email}
