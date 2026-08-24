from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from schemas.base import ApiResponse
from schemas.category import CategoryClassCreate, CategoryClassRead, CategoryClassUpdate
from services.dependencies import (
    CategoryServiceDependency,
    CurrentUserDependency,
)
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/category", tags=["Category"])


@router.get("/all", response_model=ApiResponse[list[CategoryClassRead]])
async def get_all_categories(
    category_service: CategoryServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_all_categories")

    categories = await category_service.fetch_all_categories()
    result = {
        "success": True,
        "message": constants.all_category_fetch_successful,
        "data": categories,
    }
    return result


@router.get("/{category_id}", response_model=ApiResponse[CategoryClassRead])
async def get_category_by_id(
    category_id: UUID,
    category_service: CategoryServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_category_by_id")

    category = await category_service.fetch_category_by_id(category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    result = ApiResponse(
        success=True,
        message=constants.category_fetch_successful,
        data=category,
    )

    return result


@router.post("/create", response_model=ApiResponse[CategoryClassRead])
async def create_category(
    category_details: CategoryClassCreate,
    category_service: CategoryServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering create_category")
    try:
        if user_details.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=constants.invalid_access_token,
            )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.invalid_access_token,
        )
    result = await category_service.create_category(
        category_details, user_details.username
    )
    if result is not None:
        return ApiResponse(
            success=True,
            message=constants.category_create_successful,
            data=result,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists",
        )


@router.patch("/update/{category_id}", response_model=ApiResponse[CategoryClassRead])
async def update_category(
    category_id: UUID,
    category_details: CategoryClassUpdate,
    category_service: CategoryServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering update_category")

    if user_details.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.invalid_access_token,
        )
    result = await category_service.update_category(
        category_id, category_details, user_details.username
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.category_update_successful,
            data=result,
        )


@router.delete("/delete/{category_id}", response_model=ApiResponse[CategoryClassRead])
async def delete_category(
    category_id: UUID,
    category_service: CategoryServiceDependency,
    user_details: CurrentUserDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering delete_category")
    if user_details.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.invalid_access_token,
        )
    result = await category_service.delete_category(category_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.category_delete_successful,
            data=result,
        )
