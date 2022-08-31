from faker import Faker

import aiohttp
from flask import redirect, Response
from requests import request

from .base import BaseOAuth
from api.utils.signature import create_signature
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

    async def get_api_data(self, request: request) -> tuple[dict, str]:
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
                user_data = {'user_service_id': user_service_id, 'email': email}
                user_data_as_str = ' '.join([f"{k}='{v}'" for k, v in user_data.items()])
                signature = create_signature(user_data_as_str)

                return user_data, signature
