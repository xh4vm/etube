import hashlib

import jwt
from core.config import CONFIG, grpc_logger
from errors.permission import PermissionError
from errors.token import TokenError
from messages.permission_pb2 import AccessibleResponse
from messages.permission_pb2_grpc import PermissionServicer


class PermissionServer(PermissionServicer):
    async def is_accessible(self, request, context):

        try:
            payload = jwt.decode(jwt=request.token, key=CONFIG.JWT_SECRET_KEY, algorithms=CONFIG.JWT_DECODE_ALGORITHMS)

        except jwt.exceptions.InvalidSignatureError:
            grpc_logger.info(TokenError.INVALIDED_SIGNATURE_ERROR)
            return AccessibleResponse(is_accessible=False, message=TokenError.INVALIDED_SIGNATURE_ERROR)

        except jwt.exceptions.ExpiredSignatureError:
            grpc_logger.info(TokenError.EXPIRED_SIGNATURE_ERROR)
            return AccessibleResponse(is_accessible=False, message=TokenError.EXPIRED_SIGNATURE_ERROR)

        except jwt.exceptions.DecodeError:
            grpc_logger.info(TokenError.DECODE_ERROR)
            return AccessibleResponse(is_accessible=False, message=TokenError.DECODE_ERROR)

        permissions = payload.get('permissions')

        if permissions is None:
            grpc_logger.info(TokenError.FORMAT_ERROR)
            raise ValueError(TokenError.FORMAT_ERROR)

        md5_hashed_url = hashlib.md5(request.url.encode(), usedforsecurity=False).hexdigest()

        if (
            isinstance((allowed_methods := permissions.get(md5_hashed_url)), list)
            and request.method in allowed_methods
        ):
            grpc_logger.info(PermissionError.ACCESS_SUCCESS)
            return AccessibleResponse(is_accessible=True, message=PermissionError.ACCESS_SUCCESS)

        grpc_logger.info(PermissionError.ACCESS_ERROR)
        return AccessibleResponse(is_accessible=False, message=PermissionError.ACCESS_ERROR)
