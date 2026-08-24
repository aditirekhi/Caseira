from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.base import ApiResponse
from schemas.ingredients import (
    IngredientClassCreate,
    IngredientClassUpdate,
    IngredientsClassRead,
)
from services.dependencies import (
    CurrentUserDependency,
    IngredientServiceDependency,
    check_valid_request,
    get_current_user,
    get_user_access_token,
)
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/ingredient", tags=["Ingredient"])


@router.get("/all", response_model=ApiResponse[list[IngredientsClassRead]])
async def get_all_ingredients(
    ingredient_service: IngredientServiceDependency, constants: ConstantsDependency
):
    print("-------------------------------- Entering get_all_ingredients")
    ingredients = await ingredient_service.fetch_all_ingredients()
    return ApiResponse(
        success=True,
        message=constants.all_ingredients_fetched_successfully,
        data=ingredients,
    )


@router.get("/{ingredient_id}", response_model=ApiResponse[IngredientsClassRead])
async def get_ingredient_by_id(
    ingredient_id: UUID,
    ingredient_service: IngredientServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_ingredient_by_id")
    ingredient = await ingredient_service.fetch_ingredient_by_id(ingredient_id)
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )
    return ApiResponse(
        success=True,
        message=constants.ingredient_fetched_successfully,
        data=ingredient,
    )


@router.post("/create", response_model=ApiResponse[IngredientsClassRead])
async def create_ingredient(
    payload: IngredientClassCreate,
    ingredient_service: IngredientServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering create_ingredient")
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    ingredient = await ingredient_service.create_ingredient(
        payload, user_details.username
    )
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ingredient name already exists",
        )
    return ApiResponse(
        success=True,
        message=constants.ingredient_create_successful,
        data=ingredient,
    )


@router.patch(
    "/update/{ingredient_id}", response_model=ApiResponse[IngredientsClassRead]
)
async def update_ingredient(
    ingredient_id: UUID,
    payload: IngredientClassUpdate,
    ingredient_service: IngredientServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering update_ingredient")
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    ingredient = await ingredient_service.update_ingredient(
        ingredient_id, payload, user_details.username
    )
    if ingredient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )
    return ApiResponse(
        success=True,
        message=constants.ingredient_update_successful,
        data=ingredient,
    )


@router.delete("/delete/{ingredient_id}", response_model=ApiResponse[dict])
async def delete_ingredient(
    ingredient_id: UUID,
    ingredient_service: IngredientServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering delete_ingredient")
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    deleted = await ingredient_service.delete_ingredient(ingredient_id)
    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ingredient not found",
        )
    return ApiResponse(
        success=True,
        message=constants.ingredient_delete_successful,
        data={"ingredient_id": str(ingredient_id)},
    )
