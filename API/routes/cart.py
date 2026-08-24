from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from schemas.base import ApiResponse
from schemas.cart import CartCreateClass, CartDeleteClass, CartReadClass
from services.dependencies import (
    CartServiceDependency,
    CurrentUserDependency,
)
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/userId", response_model=ApiResponse[CartReadClass])
async def get_cart_by_user_id(
    cart_service: CartServiceDependency,
    constants: ConstantsDependency,
    current_user: CurrentUserDependency,
):
    print("---------------------------- Entering get_cart_by_user_id")

    user_id = current_user.user_id

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    cart = await cart_service.get_cart_by_user_id(user_id)

    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.cart_not_found_for_user,
        )

    return ApiResponse(
        success=True, data=cart, message=constants.cart_fetched_successfully
    )


@router.get("/cartId/{cart_id}", response_model=ApiResponse[CartReadClass])
async def get_cart_by_cart_id(
    cart_id: UUID,
    cart_service: CartServiceDependency,
    constants: ConstantsDependency,
    user_details: CurrentUserDependency,
):
    print("---------------------------- Entering get_cart_by_cart_id")

    try:
        user_id = user_details.user_id
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
            )
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    result = await cart_service.get_cart_by_cart_id(cart_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.cart_not_found_for_user,
        )

    return ApiResponse(
        success=True, data=result, message=constants.cart_fetched_successfully
    )


@router.patch("/update/{cart_id}", response_model=ApiResponse[CartReadClass])
async def update_cart(
    cart_id: UUID,
    payload: CartCreateClass,
    cart_service: CartServiceDependency,
    constants: ConstantsDependency,
    current_user: CurrentUserDependency,
):
    print("---------------------------- Entering update_cart")

    user_id = current_user.user_id

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    created_by = (
        current_user.username or current_user.email_address or str(current_user.user_id)
    )

    result = await cart_service.update_cart_details(
        cart_id,
        payload,
        created_by=created_by,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.cart_not_found_for_user,
        )

    return ApiResponse(
        success=True, message=constants.cart_updated_successfully, data=result
    )


@router.delete("/delete", response_model=ApiResponse[None])
async def delete_cart(
    payload: CartDeleteClass,
    cart_service: CartServiceDependency,
    constants: ConstantsDependency,
    current_user: CurrentUserDependency,
):
    print("---------------------------- Entering delete_cart")

    user_id = current_user.user_id

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
        )

    result = await cart_service.delete_cart_by_cart_id(payload)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=constants.cart_not_found_for_user,
        )

    return ApiResponse(
        success=True, message=constants.cart_deleted_successfully, data=result
    )
