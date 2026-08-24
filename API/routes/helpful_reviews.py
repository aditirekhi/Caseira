from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from schemas.base import ApiResponse
from schemas.helpful_review import (
    HelpfulReviewCreate,
    HelpfulReviewDelete,
    HelpfulReviewRead,
)
from services.dependencies import CurrentUserDependency, HelpfulReviewsServiceDependency

router = APIRouter(
    prefix="/helpful-reviews",
    tags=["Helpful Reviews"],
)


@router.get("/{recipe_review_id}", response_model=ApiResponse[list[HelpfulReviewRead]])
async def get_helpful_reviews_by_review_id(
    recipe_review_id: UUID, helpful_reviews_service: HelpfulReviewsServiceDependency
):
    print("-------------------------------- Entering get_helpful_reviews_by_review_id")

    helpful_reviews = await helpful_reviews_service.get_helpful_reviews_by_review_id(
        recipe_review_id
    )

    if helpful_reviews is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Helpful reviews not found"
        )

    return ApiResponse(
        success=True,
        message="Helpful reviews fetched successfully",
        data=helpful_reviews,
    )


@router.post("/create", response_model=ApiResponse[HelpfulReviewRead])
async def create_helpful_review(
    payload: HelpfulReviewCreate,
    helpful_reviews_service: HelpfulReviewsServiceDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering create_helpful_review")

    if not user_details or not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    helpful_review = await helpful_reviews_service.create_helpful_review(
        payload, user_details.user_id, user_details.username
    )

    if helpful_review is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create helpful review",
        )

    return ApiResponse(
        success=True, message="Helpful review created successfully", data=helpful_review
    )


@router.delete(
    "/delete/{recipe_review_id}", response_model=ApiResponse[HelpfulReviewRead]
)
async def delete_helpful_review(
    recipe_review_id: UUID,
    helpful_reviews_service: HelpfulReviewsServiceDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering delete_helpful_review")

    if not user_details or not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated",
        )

    helpful_review = await helpful_reviews_service.delete_helpful_review(
        HelpfulReviewDelete(recipe_review_id=recipe_review_id), user_details.user_id
    )

    if helpful_review is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete helpful review",
        )
    else:
        return ApiResponse(
            success=True,
            message="Helpful review deleted successfully",
            data=helpful_review,
        )
