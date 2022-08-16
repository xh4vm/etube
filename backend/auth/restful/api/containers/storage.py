from typing import Optional, Type

from dependency_injector import providers, resources

import api.app as application_factory

from ..services.storage.base import BaseStorage
from ..services.storage.redis import RedisStorage


class StorageResource(providers.Resource):
    provided_type: Optional[Type] = BaseStorage


class RedisStorageResource(resources.Resource):
    def init(self, *args, **kwargs) -> BaseStorage:
        return RedisStorage(redis=application_factory.redis_client)
