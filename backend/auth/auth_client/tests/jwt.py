from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from auth_client.core.config import CONFIG


def create_token(claims: dict[str:Any]) -> str:
    _claims = {'exp': int((datetime.now(timezone.utc) + timedelta(minutes=5)).timestamp())}
    _claims.update(claims)

    return jwt.encode(_claims, key=CONFIG.APP.JWT_SECRET_KEY, algorithm=CONFIG.APP.JWT_ALGORITHM)
