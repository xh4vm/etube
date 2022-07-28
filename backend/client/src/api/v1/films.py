from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.core.config import CONFIG
from src.models.base import PageModel
from src.models.film import FilmModelBrief, FilmModelFull
from src.services.film import FilmService

from src.containers.film import ServiceRedisElasticContainer
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix='/film', tags=['Films'])


@router.get(path='/{film_id}', name='Film Detail', response_model=FilmModelFull)
@inject
async def film_details(
    film_id: str, 
    film_service: FilmService = Depends(Provide[ServiceRedisElasticContainer.film_service])
) -> FilmModelFull:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return film


@router.get(path='s', name='List Of Films', response_model=PageModel[FilmModelBrief])
@inject
async def films_list(
    page: int = CONFIG.APP.page,
    page_size: int = CONFIG.APP.page_size,
    search: str = '',
    sort: str = None,
    filters: str = None,
    film_service: FilmService = Depends(Provide[ServiceRedisElasticContainer.film_service])
) -> PageModel[FilmModelBrief]:
    return await film_service.search(
        page=page, page_size=page_size, search_value=search, sort_fields=sort, filters=filters
    )
