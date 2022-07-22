from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.core.config import CONFIG
from src.models.base import PageModel
from src.models.film import FilmModelBrief, FilmModelFull
from src.services.film import FilmService
from src.services.giver import film_service as giver_service

router = APIRouter(prefix='/film', tags=['Films'])


@router.get(path='/{film_id}', name='Film Detail', response_model=FilmModelFull)
async def film_details(film_id: str, film_service: FilmService = Depends(giver_service)) -> FilmModelFull:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return film


@router.get(path='s', name='List Of Films', response_model=PageModel[FilmModelBrief])
async def films_list(
    page: int = CONFIG.APP.page,
    page_size: int = CONFIG.APP.page_size,
    search: str = '',
    sort: str = None,
    filters: str = None,
    film_service: FilmService = Depends(giver_service),
) -> PageModel[FilmModelBrief]:
    return await film_service.search(
        page=page, page_size=page_size, search_value=search, sort_fields=sort, filters=filters
    )
