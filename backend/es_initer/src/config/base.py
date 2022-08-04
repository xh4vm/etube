from typing import Any

import backoff
from pydantic import BaseSettings, Field


class ElasticsearchSettings(BaseSettings):
    protocol: str = Field(..., env='ES_PROTOCOL')
    user: str = Field(..., env='ES_USER')
    password: str = Field(..., env='ES_PASSWORD')
    host: str = Field(..., env='ES_HOST')
    port: int = Field(..., env='ES_PORT')


class ElasticsearchIndices(BaseSettings):
    movies: str = Field(..., env='INDEX_MOVIES')
    genres: str = Field(..., env='INDEX_GENRES')
    persons: str = Field(..., env='INDEX_PERSONS')


ELASTIC_CONFIG: ElasticsearchSettings = ElasticsearchSettings()
ELASTIC_INDICES: ElasticsearchIndices = ElasticsearchIndices()
BACKOFF_CONFIG: dict[str, Any] = {'wait_gen': backoff.expo, 'exception': Exception, 'max_value': 8}
