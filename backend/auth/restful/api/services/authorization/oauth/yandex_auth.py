from urllib.parse import urlencode

import aiohttp
from api.schema.base import UserSocial
from core.config import OAUTH_CONFIG
from flask import Response, redirect
from requests import request

from .base import BaseOAuth


class YandexAuth(BaseOAuth):
    def get_permission_code(self) -> Response:
        # Получение от яндекса кода, который используется для
        # получение токенов, которые нужны для доступа к API.
        return redirect(
            OAUTH_CONFIG.YANDEX.BASEURL
            + 'authorize?response_type=code&client_id={}'.format(OAUTH_CONFIG.YANDEX.CLIENT_ID)
        )

    async def get_api_tokens(self, request: request) -> str:
        # Получение токенов от стороннего сервиса.
        # Токены используются для запроса к API.
        # TODO: Как-то обрабатывать этот код, а не просто пересылать
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

    async def get_api_data(self, access_token: str) -> UserSocial:
        # Получение данных пользователя от API.
        async with aiohttp.ClientSession() as session:
            url = OAUTH_CONFIG.YANDEX.LOGINURL
            headers = {'Authorization': f'OAuth {access_token}'}

            async with session.get(url, headers=headers) as response:
                data = await response.json()
                user_service_id = str(data.get('id'))
                email = data.get('default_email') or self.faker.email()

                return UserSocial(user_service_id=user_service_id, email=email, service_name='yandex')
