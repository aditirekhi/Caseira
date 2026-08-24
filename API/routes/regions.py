from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.base import ApiResponse
from schemas.regions import RegionsClassCreate, RegionsClassRead, RegionsClassUpdate
from services.dependencies import (
    CurrentUserDependency,
    RegionsServiceDependency,
    check_valid_request,
    get_current_user,
    get_user_access_token,
)
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/regions", tags=["Regions"])


@router.get("/all", response_model=ApiResponse[list[RegionsClassRead]])
async def get_all_regions(
    regions_service: RegionsServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_all_regions")
    regions = await regions_service.fetch_all_regions()

    return ApiResponse(
        success=True,
        message=constants.all_regions_fetch_successful,
        data=regions,
    )


@router.get("/{region_id}", response_model=ApiResponse[RegionsClassRead])
async def get_region_by_id(
    region_id: UUID,
    regions_service: RegionsServiceDependency,
    constants: ConstantsDependency,
):
    print("-------------------------------- Entering get_region_by_id")
    region = await regions_service.fetch_region_by_id(region_id)
    if region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found",
        )

    return ApiResponse(
        success=True,
        message=constants.region_fetch_successful,
        data=region,
    )


@router.post("/create", response_model=ApiResponse[RegionsClassRead])
async def create_region(
    payload: RegionsClassCreate,
    regions_service: RegionsServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering create_region")
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    region = await regions_service.create_region(payload, user_details.username)

    if region is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Region name already exists",
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.region_create_successful,
            data=region,
        )


@router.patch("/update/{region_id}", response_model=ApiResponse[RegionsClassRead])
async def update_region(
    region_id: UUID,
    payload: RegionsClassUpdate,
    regions_service: RegionsServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering update_region")
    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    region = await regions_service.update_region(
        payload, region_id, user_details.username
    )

    if region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found",
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.region_update_successful,
            data=region,
        )


@router.delete("/delete/{region_id}", response_model=ApiResponse[RegionsClassRead])
async def delete_region(
    region_id: UUID,
    regions_service: RegionsServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("-------------------------------- Entering delete_region")

    if not user_details.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    region = await regions_service.delete_region(region_id)

    if region is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found",
        )
    else:
        return ApiResponse(
            success=True,
            message=constants.region_delete_successful,
            data=region,
        )
