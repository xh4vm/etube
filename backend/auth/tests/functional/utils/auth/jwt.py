from datetime import datetime
from typing import Any

import jwt
from functional.settings import CONFIG


def get_jwt_claims(token: str) -> dict[str, Any]:
    return jwt.decode(token, key=CONFIG.API.JWT_SECRET_KEY, algorithms=CONFIG.API.JWT_DECODE_ALGORITHMS)


def get_jwt_identity(token: str) -> int:
    return jwt.decode(token, key=CONFIG.API.JWT_SECRET_KEY, algorithms=CONFIG.API.JWT_DECODE_ALGORITHMS)['sub']


def get_jwt_exp(token: str) -> int:
    return jwt.decode(token, key=CONFIG.API.JWT_SECRET_KEY, algorithms=CONFIG.API.JWT_DECODE_ALGORITHMS)['exp']


def get_jti(token: str) -> str:
    return jwt.decode(token, key=CONFIG.API.JWT_SECRET_KEY, algorithms=CONFIG.API.JWT_DECODE_ALGORITHMS)['jti']


def verify_exp_jwt(token: str) -> bool:
    exp = get_jwt_exp(token)
    return exp > datetime.now().timestamp()


def create_token(claims: dict[str:Any]) -> str:
    return jwt.encode(claims, key=CONFIG.API.JWT_SECRET_KEY, algorithm=CONFIG.API.JWT_ALGORITHM)
