from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.config import APP_CONFIG


app = FastAPI(
    title=APP_CONFIG.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

from .api.v1.films import router as film_router
app.include_router(router=film_router)

from .api.v1.genres import router as genre_router
app.include_router(router=genre_router)

from .api.v1.persons import router as person_router
app.include_router(router=person_router)
