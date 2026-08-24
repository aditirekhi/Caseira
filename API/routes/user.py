from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)

from schemas.base import ApiResponse
from schemas.user import UserClassChangePassword, UserClassCreate, UserLoginResponse
from services.dependencies import (
    UserServiceDependency,
    check_valid_request,
    get_user_access_token,
)
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/signin", response_model=ApiResponse[UserLoginResponse])
async def signin(
    payload: UserClassCreate,
    user_service: UserServiceDependency,
    constants: ConstantsDependency,
):
    created_user = await user_service.add_user(payload)
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User already exists.",
        )
    token = await user_service.login(payload.email_address, payload.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    result = {
        "success": True,
        "message": constants.user_signin_successful,
        "data": {"access_token": token, "token_type": "Bearer"},
    }

    return result


@router.post("/login", response_model=ApiResponse[UserLoginResponse])
async def login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDependency,
    constants: ConstantsDependency,
):
    token = await user_service.login(payload.username, payload.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return {
        "success": True,
        "message": constants.user_login_successful,
        "data": {
            "access_token": token,
            "token_type": "Bearer",
        },
    }


@router.post("/forgotPassword", response_model=ApiResponse[None])
async def change_password(
    payload: UserClassChangePassword,
    user_service: UserServiceDependency,
    constants: ConstantsDependency,
):
    result = await user_service.change_password(payload)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to change password",
        )
    return {
        "success": True,
        "message": constants.password_updated_successfully,
        "data": None,
    }


@router.post("/logout", response_model=ApiResponse[None])
async def logout(
    token: Annotated[dict, Depends(get_user_access_token)],
    user_service: UserServiceDependency,
    constants: ConstantsDependency,
    token_data: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    try:
        await check_valid_request(token_data.credentials)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.invalid_access_token,
        )
    logout_result = await user_service.logout(token["jti"])
    if logout_result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid jwt token",
        )
    return ApiResponse(
        success=True,
        message=constants.user_logout_successful,
        data=None,
    )
