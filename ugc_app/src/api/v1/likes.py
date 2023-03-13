from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import ORJSONResponse

from src.models.like import MovieLikeEvent, ReviewLikeEvent, MovieLikeEventWithUser, ReviewLikeEventWithUser
from src.models.review import ReviewEventWithUser
from src.services.movie_like import LikeService, get_like_service
from src.services.decorators import access_check
from src.core.config import settings

router = APIRouter(tags=["Likes"])


@router.post(
    "/movie-likes",
    summary="Add like to movie.",
    description="Add like to movie with ID movie_id with score - score (0-10).",
    status_code=status.HTTP_201_CREATED,
)
@access_check(assigned_roles=settings.ROLES)
async def add_movie_like(
        request: Request,
        like: MovieLikeEvent,
        service: LikeService = Depends(get_like_service),
) -> MovieLikeEventWithUser:
    body = await request.receive()
    user_id = body["user_id"]
    like = like.dict()
    like["user_id"] = user_id
    like = MovieLikeEventWithUser(**like)
    await service.add_movie_like(like)
    return like


@router.get(
    "/movie-likes/avg/{movie_id}",
    summary="Get AVG movie score.",
    description="Get avg movie score for movie with ID movie_id.",
    response_model=float | None,
    status_code=status.HTTP_200_OK,
)
@access_check(assigned_roles=settings.ROLES)
async def get_avg_movie_rating(
        request: Request,
        movie_id: str,
        service: LikeService = Depends(get_like_service),
) -> ORJSONResponse:
    result = await service.get_avg_movie_rating(movie_id)
    return ORJSONResponse({"rating": result})


@router.post(
    "/review-likes",
    summary="Add like to review.",
    description="Add like to review with ID review_id with score - score (1-10).",
    status_code=status.HTTP_201_CREATED,
)
@access_check(assigned_roles=settings.ROLES)
async def add_review_like(
        request: Request,
        review: ReviewLikeEvent,
        service: LikeService = Depends(get_like_service),
) -> ReviewLikeEventWithUser:
    body = await request.receive()
    user_id = body["user_id"]
    review = review.dict()
    review["user_id"] = user_id
    review = ReviewLikeEventWithUser(**review)
    await service.add_review_like(review)
    return review


@router.get(
    "/review-likes/avg/{review_id}",
    summary="Get AVG review score.",
    description="Get avg review score for review with ID review_id.",
    response_model=float,
    status_code=status.HTTP_200_OK,
)
@access_check(assigned_roles=settings.ROLES)
async def add_review_like(
        request: Request,
        review_id: str,
        service: LikeService = Depends(get_like_service),
) -> ORJSONResponse:
    result = await service.get_avg_review_rating(review_id)
    return ORJSONResponse({"rating": result})
