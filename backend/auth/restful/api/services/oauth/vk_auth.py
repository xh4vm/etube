from faker import Faker

import aiohttp
from flask import redirect, Response
from requests import request

from .base import BaseOAuth
from core.config import OAUTH_CONFIG


class VKAuth(BaseOAuth):

    def get_permission_code(self) -> Response:
        return redirect(
            OAUTH_CONFIG.VK.BASEURL + 'authorize?client_id={}&redirect_uri={}&display={}&scope={}&response_type={}'.format(
                OAUTH_CONFIG.VK.CLIENT_ID,
                OAUTH_CONFIG.VK.REDIRECT,
                OAUTH_CONFIG.VK.DISPLAY,
                OAUTH_CONFIG.VK.SCOPE,
                OAUTH_CONFIG.VK.RESPONSE,
            )
        )

    async def get_api_data(self, request: request) -> dict:
        # Получение данных пользователя от API.
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
                email = data.get('default_email')
                if email is None:
                    email = Faker().email()
                hash = self.create_hash(user_service_id, email)

                return {'user_service_id': user_service_id, 'email': email, 'hash': hash}
