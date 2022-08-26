from auth_client.core.config import CONFIG


def header_token_extractor(request, header_name: str = CONFIG.APP.JWT_HEADER_NAME):
        token = request.headers.get(header_name)

        if token is None or not isinstance(token, str):
            return None

        header, payload = token.split()

        return payload
