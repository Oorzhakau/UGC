from typing import List

from fastapi import APIRouter, Depends, Request, status, Query

from src.models.review import ReviewEvent, ReviewEventWithUser, ReviewEventComplete
from src.services.movie_review import ReviewService, get_review_service
from src.services.decorators import access_check
from src.core.config import settings

router = APIRouter(tags=["Reviews"])


@router.post(
    "/reviews",
    summary="Add review to movie.",
    description="Add review to movie with ID movie_id with score (0-10).",
    status_code=status.HTTP_201_CREATED,
)
@access_check(assigned_roles=settings.ROLES)
async def add_review(
        request: Request,
        review: ReviewEvent,
        service: ReviewService = Depends(get_review_service),
) -> ReviewEventComplete:
    body = await request.receive()
    user_id = body["user_id"]
    review = review.dict()
    review["user_id"] = user_id
    review = ReviewEventWithUser(**review)
    review = await service.add_review(review)
    return review


@router.get(
    "/reviews/{movie_id}",
    summary="Get movie`s revires.",
    description="Get all reviews for movie with ID - movie_id with pagination.",
    response_model=List[ReviewEventComplete],
    status_code=status.HTTP_200_OK,
)
@access_check(assigned_roles=settings.ROLES)
async def get_reviews(
        request: Request,
        movie_id: str,
        page_size: int = Query(default=20, alias="page[size]"),
        page_number: int = Query(default=1, alias="page[number]"),
        service: ReviewService = Depends(get_review_service),
) -> List[ReviewEventComplete]:
    return await service.get_reviews(page_size, page_number, movie_id)


@router.get(
    "/{user_id}/reviews/",
    summary="Get user's movie reviews.",
    description="Get all user's reviews for movies.",
    response_model=List[ReviewEventComplete],
    status_code=status.HTTP_200_OK,
)
@access_check(assigned_roles=settings.ROLES)
async def get_reviews(
        request: Request,
        user_id: str,
        page_size: int = Query(default=20, alias="page[size]"),
        page_number: int = Query(default=1, alias="page[number]"),
        service: ReviewService = Depends(get_review_service),
) -> List[ReviewEventComplete]:
    return await service.get_user_reviews(page_size, page_number, user_id)
