from datetime import datetime, timedelta, timezone
from typing import Protocol
from uuid import uuid4

import jwt
from fastapi import HTTPException, status

from config import jwt_settings
from schemas.base import JWTTokenInfo


class UtilsServiceProtocol(Protocol):
    async def add_token_to_blacklist(self, token: dict) -> object: ...
    async def is_token_blacklisted(self, token: str) -> bool: ...


def generate_access_token(user_payload: dict, count: int = 1, expiry=timedelta(days=1)):
    print("-------------------------------- Entering generate_access_token")
    return jwt.encode(
        payload=JWTTokenInfo(
            **user_payload,
            exp=datetime.now(timezone.utc) + expiry,
            jti=str(uuid4()),
            count=count,
        ).model_dump(),
        algorithm=jwt_settings.JWT_ALGORITHM,
        key=jwt_settings.JWT_SECRET_KEY,
    )


def decode_access_token(token: str) -> dict:
    print("-------------------------------- Entering decode_access_token")
    print(f"Raw token received: {token}")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=jwt_settings.JWT_SECRET_KEY,
            algorithms=[jwt_settings.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
    except jwt.InvalidTokenError as exc:
        print(f"Invalid token: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        ) from exc
    except Exception as exc:
        print(f"Unexpected token decode error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        ) from exc

    if decoded_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    if not isinstance(decoded_token, dict):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is not valid",
        )

    return decoded_token


async def add_token_to_blacklist(
    token: dict, utils_service: UtilsServiceProtocol | None = None
):
    print("-------------------------------- Entering add_token_to_blacklist")

    if not isinstance(token, dict):
        raise TypeError("JWT payload must be a dictionary.")

    jti = token.get("jti")
    exp_value = token.get("exp")

    if jti is None:
        raise ValueError("JWT token is missing the 'jti' claim.")
    if exp_value is None:
        raise ValueError("JWT token is missing the 'exp' claim.")

    if utils_service is None:
        raise ValueError("Utils service is required to blacklist a token.")

    await utils_service.add_token_to_blacklist(
        {
            "jti": str(jti),
            "exp": datetime.fromtimestamp(float(exp_value), tz=timezone.utc),
        }
    )


async def is_token_blacklisted(
    token_id: str, utils_service: UtilsServiceProtocol | None = None
) -> bool:
    print("-------------------------------- Entering is_token_blacklisted")

    if token_id is None:
        return False

    if utils_service is None:
        raise ValueError("Utils service is required to check blacklisted tokens.")

    return await utils_service.is_token_blacklisted(str(token_id))
