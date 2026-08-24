from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from schemas.base import ApiResponse
from schemas.recipe_reviews import RecipeReviewRead, ReviewRead, ReviewUpdate
from services.dependencies import CurrentUserDependency, RecipeReviewsServiceDependency
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/reviews", tags=["Recipe Reviews"])


@router.get(
    "/byRecipeIdUserId/{recipe_id}/{user_id}",
    response_model=ApiResponse[list[ReviewRead]],
)
async def get_review_by_recipe_and_user_id(
    recipe_id: UUID,
    user_id: UUID,
    recipe_review_service: RecipeReviewsServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_review_by_recipe_and_user_id")

    result = await recipe_review_service.get_review_by_recipe_and_user_id(
        recipe_id, user_id
    )

    if result is None or len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.review_not_found,
        )
    return ApiResponse(
        success=True,
        message=constants.review_fetched_successfully,
        data=result,
    )


@router.get("/all", response_model=ApiResponse[list[ReviewRead]])
async def get_all_reviews(
    recipe_review_service: RecipeReviewsServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_all_reviews")

    result = await recipe_review_service.get_all_reviews()

    if result is None or len(result) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.reviews_not_found,
        )

    return ApiResponse(
        success=True,
        message=constants.all_reviews_fetched_successfully,
        data=result,
    )


@router.get("/id/{recipe_id}", response_model=ApiResponse[RecipeReviewRead])
async def get_review_by_id(
    recipe_id: UUID,
    recipe_review_service: RecipeReviewsServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_review_by_id")

    result = await recipe_review_service.get_review_by_recipe_id(recipe_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.review_not_found,
        )

    return ApiResponse(
        success=True,
        message=constants.review_fetched_successfully,
        data=result,
    )


@router.put("/update", response_model=ApiResponse[ReviewRead])
async def update_review(
    review: ReviewUpdate,
    recipe_review_service: RecipeReviewsServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering update_review")

    if not user_details or not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    result = await recipe_review_service.update_review(
        review, user_details.user_id, user_details.username
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.review_update_failed,
        )

    return ApiResponse(
        success=True,
        message=constants.review_update_successful,
        data=result,
    )


@router.delete("/delete/{recipe_review_id}", response_model=ApiResponse[ReviewRead])
async def delete_review(
    recipe_review_id: UUID,
    recipe_review_service: RecipeReviewsServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering delete_review")

    result = await recipe_review_service.delete_review(recipe_review_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.review_delete_failed,
        )

    return ApiResponse(
        success=True,
        message=constants.review_delete_successful,
        data=result,
    )
