from core.utils import (
    add_token_to_blacklist,
    decode_access_token,
    generate_access_token,
    is_token_blacklisted,
)
from services.utils import UtilsService


class SecurityClass:
    def __init__(self, session):
        self.session = session

    async def refresh_token(self, token: str):
        print("-------------------------------- Entering SecurityService.refresh_token")

        token_data = decode_access_token(token)

        print(f"Decoded token data: {token_data}")

        if token_data is None:
            return None

        token_id = token_data.get("jti")
        if token_id is None:
            return None

        utils_service = UtilsService(self.session)
        is_blacklisted = await is_token_blacklisted(token_id, utils_service)
        if not is_blacklisted:
            await add_token_to_blacklist(token_data, utils_service)

        count = token_data.get("count", 1)

        if count > 10:
            return None

        user_payload = {
            "user_id": token_data.get("user_id"),
            "email_address": token_data.get("email_address"),
        }

        return generate_access_token(
            user_payload=user_payload, count=token_data.get("count", 1) + 1
        )
