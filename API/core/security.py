from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/user/login")
oauth2_scheme_optional_user = OAuth2PasswordBearer(
    tokenUrl="/user/login", auto_error=False
)


class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request):
        auth_credentials = await super().__call__(request)

        if (
            auth_credentials is None
            or getattr(auth_credentials, "credentials", None) is None
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
            )

        token_code = auth_credentials.credentials

        if token_code is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorised"
            )

        return token_code
