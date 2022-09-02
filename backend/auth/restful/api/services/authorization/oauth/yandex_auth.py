from urllib.parse import urlencode

import aiohttp
from flask import redirect, Response
from requests import request

from .base import BaseOAuth

from api.utils.signature import create_signature
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

    async def get_api_tokens(self, request: request) -> str:
        # Получение токенов от стороннего сервиса.
        # Токены используются для запроса к API.
        code = request.args.get('code')
        async with aiohttp.ClientSession() as session:
            params = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': OAUTH_CONFIG.YANDEX.CLIENT_ID,
                'client_secret': OAUTH_CONFIG.YANDEX.CLIENT_SECRET,
            }
            params = urlencode(params)
            url = OAUTH_CONFIG.YANDEX.BASEURL + 'token'
            async with session.post(url, data=params) as response:
                data = await response.json()
                api_access_token = data.get('access_token')

                return api_access_token

    async def get_api_data(self, access_token: str) -> tuple[dict, str]:
        # Получение данных пользователя от API.
        async with aiohttp.ClientSession() as session:
            url = 'https://login.yandex.ru/info'
            headers = {'Authorization': f'OAuth {access_token}'}
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                user_service_id = data.get('id')
                email = data.get('default_email')
                user_data = {'user_service_id': user_service_id, 'email': email}
                user_data_as_str = ' '.join([f"{k}='{v}'" for k, v in user_data.items()])
                signature = create_signature(user_data_as_str)

                return user_data, signature