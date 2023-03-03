"""
Endpoints handling requests regarding UGC
"""
from fastapi import APIRouter, Depends, Request

from src.core.config import settings
from src.models import ViewEvent, ViewEventResponse
from src.services.decorators import access_check
from src.services.view_history import get_film_view_history_service, FilmViewHistoryService

router = APIRouter()


@router.post('/',
             response_model=ViewEventResponse,
             description='Storing Film View History',
             response_description='Posted a Film View History Event with a timestamp')
@access_check(assigned_roles=settings.ROLES)
async def store_view_history(
        request: Request,
        event: ViewEvent,
        service: FilmViewHistoryService = Depends(get_film_view_history_service),
) -> ViewEventResponse:
    user_id = request.receive
    res = await service.send(user_id, event)
    return res
