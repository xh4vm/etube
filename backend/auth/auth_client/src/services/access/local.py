import hashlib

import jwt
from auth_client.core.config import CONFIG, auth_logger
from auth_client.src.errors.permission import PermissionError
from auth_client.src.errors.token import TokenError


def authorized(token: str, method: str, url: str) -> tuple[bool, str]:

    try:
        payload = jwt.decode(jwt=token, key=CONFIG.APP.JWT_SECRET_KEY, algorithms=CONFIG.APP.JWT_DECODE_ALGORITHMS)

    except jwt.exceptions.InvalidSignatureError:
        auth_logger.info(TokenError.INVALIDED_SIGNATURE_ERROR)
        return False, TokenError.INVALIDED_SIGNATURE_ERROR

    except jwt.exceptions.ExpiredSignatureError:
        auth_logger.info(TokenError.EXPIRED_SIGNATURE_ERROR)
        return False, TokenError.EXPIRED_SIGNATURE_ERROR

    except jwt.exceptions.DecodeError:
        auth_logger.info(TokenError.DECODE_ERROR)
        return False, TokenError.DECODE_ERROR

    permissions = payload.get('permissions')

    if permissions is None:
        auth_logger.info(TokenError.FORMAT_ERROR)
        raise ValueError(TokenError.FORMAT_ERROR)

    md5_hashed_url = hashlib.md5(url.encode(), usedforsecurity=False).hexdigest()

    if (
        isinstance((allowed_methods := permissions.get(md5_hashed_url)), list)
        and method in allowed_methods
    ):
        auth_logger.info(PermissionError.ACCESS_SUCCESS)
        return True, PermissionError.ACCESS_SUCCESS

    auth_logger.info(PermissionError.ACCESS_ERROR)
    return False, PermissionError.ACCESS_ERROR
