import aiohttp
from api.schema.base import UserSocial
from core.config import OAUTH_CONFIG
from flask import Response, redirect
from requests import request

from .base import BaseOAuth


class VKAuth(BaseOAuth):
    def get_permission_code(self) -> Response:
        return redirect(
            OAUTH_CONFIG.VK.BASEURL
            + 'authorize?client_id={}&redirect_uri={}&display={}&scope={}&response_type={}'.format(
                OAUTH_CONFIG.VK.CLIENT_ID,
                OAUTH_CONFIG.VK.REDIRECT,
                OAUTH_CONFIG.VK.DISPLAY,
                OAUTH_CONFIG.VK.SCOPE,
                OAUTH_CONFIG.VK.RESPONSE,
            )
        )

    async def get_api_data(self, request: request) -> UserSocial:
        # Получение данных пользователя от API.
        # TODO: Как-то обрабатывать этот код, а не просто пересылать
        code = request.args.get('code')
        async with aiohttp.ClientSession() as session:
            url = OAUTH_CONFIG.VK.BASEURL + 'access_token'
            params = {
                'client_id': OAUTH_CONFIG.VK.CLIENT_ID,
                'client_secret': OAUTH_CONFIG.VK.CLIENT_SECRET,
                'redirect_uri': OAUTH_CONFIG.VK.REDIRECT,
                'code': code,
            }
            async with session.get(url, params=params) as response:
                data = await response.json()
                user_service_id = str(data.get('user_id'))
                email = data.get('default_email') or self.faker.email()

                return UserSocial(user_service_id=user_service_id, email=email, service_name='vk')
