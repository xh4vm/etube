from urllib.parse import urlencode

import aiohttp
from flask import redirect, Response
from requests import post, request

from .base import BaseOAuth
from core.config import OAUTH_CONFIG


class YandexAuth(BaseOAuth):

    def get_permission_code(self) -> Response:
        # Получение от яндекса кода, который используется для
        # получение токенов, которые нужны для доступа к API.
        return redirect(
            OAUTH_CONFIG.YANDEX.BASEURL + 'authorize?response_type=code&client_id={}'.format(
                OAUTH_CONFIG.YANDEX.CLIENT_ID
            )
        )

    def get_api_tokens(self, request: request) -> str:
        # Получение токенов от стороннего сервиса.
        # Токены используются для запроса к API.
        code = request.args.get('code')
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': OAUTH_CONFIG.YANDEX.CLIENT_ID,
            'client_secret': OAUTH_CONFIG.YANDEX.CLIENT_SECRET,
        }
        params = urlencode(params)
        response = post(OAUTH_CONFIG.YANDEX.BASEURL + 'token', params).json()
        api_access_token = response.get('access_token')

        return api_access_token

    async def get_api_data(self, access_token: str) -> dict:
        # Получение данных пользователя от API.
        async with aiohttp.ClientSession() as session:
            url = 'https://login.yandex.ru/info'
            headers = {'Authorization': f'OAuth {access_token}'}
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                user_service_id = data.get('id')
                email = data.get('default_email')
                hash = self.create_hash(user_service_id, email)

                return {'user_service_id': user_service_id, 'email': email, 'hash': hash}
