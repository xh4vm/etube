from urllib.parse import urlencode

import aiohttp
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
        code: int = request.args.get('code')
        print('***', code, type(code))
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': OAUTH_CONFIG.YANDEX.CLIENT_ID,
            'client_secret': OAUTH_CONFIG.YANDEX.CLIENT_SECRET,
        }
        data = urlencode(data)
        response = post(OAUTH_CONFIG.YANDEX.BASEURL + "token", data).json()
        api_access_token: str = response.get('access_token')

        return api_access_token

    async def get_api_data(self, access_token: str) -> dict:
        # Получение данных пользователя от Api.
        async with aiohttp.ClientSession() as session:
            url = f'https://login.yandex.ru/info'
            headers = {'Authorization': f'OAuth {access_token}'}
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                user_service_id = data.get('id')
                email = data.get('default_email')
                return {'user_service_id': user_service_id, 'email': email}
