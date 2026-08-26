from datetime import datetime, timezone
from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import BacklistedJWTTokens
from services.base import BaseService


class UtilsService(BaseService[BacklistedJWTTokens]):
    def __init__(self, session: AsyncSession):
        super().__init__(BacklistedJWTTokens, session)

    async def add_token_to_blacklist(self, token: dict):
        print(
            "-------------------------------- Entering UtilsService.add_token_to_blacklist"
        )

        exp_value = token.get("exp")
        if exp_value is None:
            raise ValueError("JWT token is missing the 'exp' claim.")

        blacklist_entry = BacklistedJWTTokens(
            token_jti=str(token.get("jti")),
            expired_at=datetime.fromtimestamp(float(exp_value), tz=timezone.utc),
        )

        return await self._create(blacklist_entry)

    async def is_token_blacklisted(self, token: str) -> bool:
        print(
            "-------------------------------- Entering UtilsService.is_token_blacklisted"
        )

        model = cast(Any, BacklistedJWTTokens)

        result = await self.session.execute(
            select(model).where(model.token_jti == token)
        )

        return result.scalar_one_or_none() is not None
