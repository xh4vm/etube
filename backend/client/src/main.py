import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.core.config import APP_CONFIG

app = FastAPI(
    title=APP_CONFIG.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        port=8000,
    )
