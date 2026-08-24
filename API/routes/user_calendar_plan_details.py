from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from schemas.base import ApiResponse
from schemas.user_calendar_plan_details import (
    UserCalendarPlanDetailsCreate,
    UserCalendarPlanDetailsRead,
)
from services.dependencies import (
    CurrentUserDependency,
    UserCalendarPlanDetailsServiceDependency,
)

router = APIRouter(
    prefix="/user-calendar-plan-details",
    tags=["User Calendar Plan Details"],
)


@router.get(
    "/fetchByUserId",
    response_model=ApiResponse[list[UserCalendarPlanDetailsRead]],
)
async def get_user_calendar_plan_details_by_user_id(
    userCalendarPlanDetailsService: UserCalendarPlanDetailsServiceDependency,
    user: CurrentUserDependency,
):
    print(
        "-------------------------------- Entering get_user_calendar_plan_details_by_user_id"
    )

    if not user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    plan_details = await userCalendarPlanDetailsService.fetch_user_calendar_plan_details_by_user_id(
        user.user_id
    )

    if not plan_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No plan details found for user_id {user.user_id}",
        )

    return ApiResponse(
        success=True,
        data=plan_details,
        message="User calendar plan details fetched successfully",
    )


@router.get(
    "/fetchByUserIdRecipeId/{recipe_id}",
    response_model=ApiResponse[UserCalendarPlanDetailsRead],
)
async def get_user_calendar_plan_details(
    userCalendarPlanDetailsService: UserCalendarPlanDetailsServiceDependency,
    recipe_id: UUID,
    user: CurrentUserDependency,
):
    print("-------------------------------- Entering get_user_calendar_plan_details")

    if not user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )
    plan_details = await userCalendarPlanDetailsService.fetch_user_calendar_plan_details_by_user_id_recipe_id(
        user.user_id, recipe_id
    )

    if not plan_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No plan details found for user_id {user.user_id} and recipe_id {recipe_id}",
        )

    return ApiResponse(
        success=True,
        data=plan_details,
        message="User calendar plan detail fetched successfully",
    )


@router.post(
    "/create",
    response_model=ApiResponse[UserCalendarPlanDetailsRead],
)
async def create_user_calendar_plan_details(
    payload: UserCalendarPlanDetailsCreate,
    userCalendarPlanDetailsService: UserCalendarPlanDetailsServiceDependency,
    user: CurrentUserDependency,
):
    print("-------------------------------- Entering create_user_calendar_plan_details")

    if not user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    plan_details = await userCalendarPlanDetailsService.create_new_user_calendar_plan(
        payload, user.user_id, user.username
    )
    if plan_details is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create user calendar plan detail",
        )
    return ApiResponse(
        success=True,
        data=plan_details,
        message="User calendar plan detail created successfully",
    )


@router.put(
    "/update",
    response_model=ApiResponse[UserCalendarPlanDetailsRead],
)
async def update_user_calendar_plan_details(
    payload: UserCalendarPlanDetailsCreate,
    userCalendarPlanDetailsService: UserCalendarPlanDetailsServiceDependency,
    user: CurrentUserDependency,
):
    print("-------------------------------- Entering update_user_calendar_plan_details")

    if not user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    plan_details = await userCalendarPlanDetailsService.update_calendar_plan(
        payload, user.user_id
    )
    if plan_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No plan details found for user_id {user.user_id} and recipe_id {payload.recipe_id}",
        )
    return ApiResponse(
        success=True,
        data=plan_details,
        message="User calendar plan detail updated successfully",
    )


@router.delete(
    "/delete/{user_calendar_plan_details_id}",
    response_model=ApiResponse[UserCalendarPlanDetailsRead],
)
async def delete_user_calendar_plan_details(
    user_calendar_plan_details_id: UUID,
    userCalendarPlanDetailsService: UserCalendarPlanDetailsServiceDependency,
    user: CurrentUserDependency,
):
    print("-------------------------------- Entering delete_user_calendar_plan_details")

    if not user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    plan_details = await userCalendarPlanDetailsService.delete_calendar_plan(
        user_calendar_plan_details_id
    )
    if plan_details is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No calendar plan found with id {user_calendar_plan_details_id}",
        )
    return ApiResponse(
        success=True,
        data=plan_details,
        message="User calendar plan detail deleted successfully",
    )
