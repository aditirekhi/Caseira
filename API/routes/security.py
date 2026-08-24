from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from schemas.base import ApiResponse
from schemas.user import UserLoginResponse
from services.dependencies import (
    SecurityServiceDependency,
    check_valid_request,
)
from shared.dependencies import ConstantsDependency

router = APIRouter(prefix="/security", tags=["Security"])


@router.get("/checkTokenExpiration", response_model=ApiResponse[bool])
async def check_token_expiration(
    constants: ConstantsDependency,
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    try:
        await check_valid_request(token.credentials)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.invalid_access_token,
        )
    return ApiResponse(
        success=True,
        message=constants.token_not_expired,
        data=False,
    )


@router.post("/refreshToken", response_model=ApiResponse[UserLoginResponse])
async def refresh_token(
    security_service: SecurityServiceDependency,
    constants: ConstantsDependency,
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    print("-------------------------------- Entering refresh_token")
    result = await security_service.refresh_token(token.credentials)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.invalid_access_token,
        )
    return ApiResponse(
        success=True,
        message=constants.token_refresh_successful,
        data={
            "access_token": result,
            "token_type": "Bearer",
        },
    )
