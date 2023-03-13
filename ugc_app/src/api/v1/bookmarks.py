from typing import List

from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.responses import ORJSONResponse

from src.models.bookmark import BookmarkEvent, BookmarkEventWithUser, BookmarkEventComplete
from src.services.movie_bookmark import BookmarkService, get_bookmark_service
from src.services.decorators import access_check
from src.core.config import settings

router = APIRouter(tags=["Bookmarks"])


@router.get(
    "/bookmarks",
    summary="Get user`s bookmarks.",
    description="Get all user's bookmarks with pagination.",
    response_model=list[BookmarkEventComplete],
    status_code=status.HTTP_200_OK,
)
@access_check(assigned_roles=settings.ROLES)
async def get_bookmarks(
        request: Request,
        page_size: int = Query(default=20, alias="page[size]"),
        page_number: int = Query(default=1, alias="page[number]"),
        service: BookmarkService = Depends(get_bookmark_service),
) -> List[BookmarkEventComplete]:
    body = await request.receive()
    user_id = body["user_id"]
    res = await service.get_bookmarks(page_number, page_size, user_id)
    return res


@router.post(
    "/bookmarks",
    summary="Add bookmark for movie.",
    description="Add bookmark movie to user's bookmarks.",
    status_code=status.HTTP_201_CREATED,
)
@access_check(assigned_roles=settings.ROLES)
async def add_bookmark(
        request: Request,
        bookmark: BookmarkEvent,
        service: BookmarkService = Depends(get_bookmark_service),
) -> BookmarkEventWithUser:
    body = await request.receive()
    user_id = body["user_id"]
    bookmark = BookmarkEventWithUser(movie_id=bookmark.movie_id, user_id=user_id)
    await service.add_bookmark(bookmark)
    return bookmark


@router.delete(
    "/bookmarks/{bookmark_id}",
    summary="Delete bookmark_id from user's bookmark.",
    description="Delete bookmark from user.",
    status_code=status.HTTP_204_NO_CONTENT,
)
@access_check(assigned_roles=settings.ROLES)
async def delete_bookmark(
        request: Request,
        bookmark_id: str,
        service: BookmarkService = Depends(get_bookmark_service),
) -> ORJSONResponse:
    body = await request.receive()
    user_id = body["user_id"]
    await service.delete_bookmark(bookmark_id, user_id)
    return ORJSONResponse({"answer": "bookmark success remove."})
