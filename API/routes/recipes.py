from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from schemas.base import ApiResponse
from schemas.recipes import (
    RecipesClassCardRead,
    RecipesClassCreate,
    RecipesClassDetailRead,
    RecipesClassUpdate,
)
from services.dependencies import (
    CurrentUserDependency,
    OptionalCurrentUserDependency,
    RecipesServiceDependency,
)
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("/all", response_model=ApiResponse[list[RecipesClassCardRead]])
async def get_recipes(
    recipes_service: RecipesServiceDependency,
    constants: ConstantsDependency,
    order_by_field: str = "recipe_name",
    direction: str = "asc",
    page_size: int = 20,
):
    print("-------------------------------- Entering get_recipes")

    print(direction)
    recipes = await recipes_service.fetch_all_recipe_cards(
        order_by_field, direction, page_size
    )

    return ApiResponse(
        success=True,
        message=constants.all_recipes_fetch_successful,
        data=recipes,
    )


@router.get("/todays-recipe", response_model=ApiResponse[RecipesClassCardRead])
async def get_todays_recipe(
    recipes_service: RecipesServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_todays_recipe")

    recipe = await recipes_service.fetch_todays_recipe()
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recipes found",
        )

    return ApiResponse(
        success=True,
        message=constants.fetch_todays_recipe_successful,
        data=recipe,
    )


@router.get("/id/{recipe_id}", response_model=ApiResponse[RecipesClassDetailRead])
async def get_recipe_by_id(
    recipe_id: UUID,
    recipes_service: RecipesServiceDependency,
    constants: ConstantsDependency,
    user_details: OptionalCurrentUserDependency,
):
    print("-------------------------------- Entering get_recipe_by_id")

    recipe = await recipes_service.fetch_recipe_by_id(
        recipe_id, user_details.user_id if user_details else None
    )
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    return ApiResponse(
        success=True,
        message=constants.recipe_fetch_successful,
        data=recipe,
    )


@router.post("/create", response_model=ApiResponse[RecipesClassCardRead])
async def create_recipe(
    payload: RecipesClassCreate,
    recipes_service: RecipesServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering create_recipe")

    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    recipe = await recipes_service.create_recipe(payload, user_details.username)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=constants.recipe_create_failed,
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.recipe_create_successful,
            data=recipe,
        )


@router.post("/create/multiple", response_model=ApiResponse[list[str]])
async def create_multiple_recipes(
    payload: list[RecipesClassCreate],
    recipes_service: RecipesServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    user = user_details

    created_recipes = []

    for recipe_payload in payload:
        recipe = await recipes_service.create_recipe(recipe_payload, user.username)
        if recipe is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=constants.recipe_create_failed,
            )
        else:
            created_recipes.append(recipe.recipe_name)

    return ApiResponse(
        success=True,
        message=constants.recipe_create_successful,
        data=created_recipes,
    )


@router.patch("/update/{recipe_id}", response_model=ApiResponse[RecipesClassCardRead])
async def update_recipe(
    recipe_id: UUID,
    payload: RecipesClassUpdate,
    recipes_service: RecipesServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    recipe = await recipes_service.update_recipe(
        recipe_id, payload, user_details.username
    )

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.recipe_update_successful,
            data=recipe,
        )


@router.delete("/delete/{recipe_id}", response_model=ApiResponse[RecipesClassCardRead])
async def delete_recipe(
    recipe_id: UUID,
    recipes_service: RecipesServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    recipe = await recipes_service.delete_recipe(recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.recipe_delete_successful,
            data=recipe,
        )
