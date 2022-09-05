from http import HTTPStatus

from auth_client.src.decorators import access_required
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request
from src.containers.film import ServiceContainer
from src.core.config import CONFIG
from src.errors.film import FilmError
from src.models.base import PageModel, Paginator
from src.models.film import FilmModelBrief, FilmModelFull
from src.services.film import FilmService
from src.utils.decorators import access_exception_handler, token_extractor

router = APIRouter(prefix='/film', tags=['Films'])
URL = f'{CONFIG.APP.host}:{CONFIG.APP.port}{CONFIG.APP.api_path}/{CONFIG.APP.version}/film'


@router.get(path='/{film_id}', name='Film Detail', response_model=FilmModelFull)
@token_extractor
@access_exception_handler
@access_required({URL: 'GET'})
@inject
async def film_details(
    film_id: str,
    request: Request,
    film_service: FilmService = Depends(Provide[ServiceContainer.film_service])
) -> FilmModelFull:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FilmError.NOT_FOUND)

    return film


@router.get(path='s', name='List Of Films', response_model=PageModel[FilmModelBrief])
@inject
async def films_list(
    paginator: Paginator = Depends(),
    search: str = '',
    sort: str = None,
    filters: str = None,
    film_service: FilmService = Depends(Provide[ServiceContainer.film_service]),
) -> PageModel[FilmModelBrief]:
    return await film_service.search(
        page=paginator.page, page_size=paginator.page_size, search_value=search, sort_fields=sort, filters=filters
    )
