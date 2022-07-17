from typing import Optional
from elasticsearch import AsyncElasticsearch


elasticsearch: Optional[AsyncElasticsearch] = None

async def get_elasticsearch() -> Optional[AsyncElasticsearch]:
    return elasticsearch
