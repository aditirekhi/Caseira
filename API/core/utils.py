from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from fastapi import HTTPException, status

from config import jwt_settings
from schemas.base import JWTTokenInfo


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
