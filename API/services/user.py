import random

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.utils import generate_access_token
from database.models import UserDetails
from database.redis import add_token_to_blacklist
from schemas.user import UserClassChangePassword, UserClassCreate
from services.base import BaseService

password_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserService(BaseService[UserDetails]):
    def __init__(self, session: AsyncSession):
        print("Entering UserService.__init__")
        super().__init__(UserDetails, session)

    async def create_username(self, first_name, last_name) -> str:
        print("-------------------------------- Entering UserService.create_username")
        username = f"{first_name.strip().lower()}_{last_name.strip().lower()}"

        while await self.check_username_exists(username):
            randomSuffix = random.randint(1, 999)
            username = f"{first_name.strip().lower()}_{last_name.strip().lower()}_{str(randomSuffix)}"

        return username

    async def check_username_exists(self, new_username) -> bool:
        print(
            "-------------------------------- Entering UserService.check_username_exists"
        )
        result = await self.session.execute(
            select(self.model).where(self.model.username == new_username)
        )

        return result.scalar_one_or_none() is not None

    async def add_user(self, payload: UserClassCreate):
        print("-------------------------------- Entering UserService.add_user")
        from services.cart import CartService

        cart_service = CartService(self.session, None, None)

        userExists = await self.get_user_by_email(payload.email_address)

        if not userExists:
            user = self.model(
                first_name=payload.first_name,
                last_name=payload.last_name,
                username=await self.create_username(
                    payload.first_name, payload.last_name
                ),
                email_address=payload.email_address,
                password_hash=password_context.hash(payload.password),
                created_by=f"{payload.first_name.strip().lower()}_{payload.last_name.strip().lower()}",
            )

            return await self._create(user)
        else:
            return None

    async def get_user_by_email(self, email: str):
        print("-------------------------------- Entering UserService.get_user_by_email")

        result = await self.session.execute(
            select(self.model).where(self.model.email_address == email)
        )

        print(result)

        user = result.scalar_one_or_none()
        return user

    async def login(self, email: str, password: str):
        print("-------------------------------- Entering UserService.login")
        user = await self.get_user_by_email(email)

        if user is None or not user.password_hash:
            return None

        try:
            valid_password = password_context.verify(password, user.password_hash)
        except Exception:
            return None

        if not valid_password:
            return None

        return generate_access_token(
            user_payload={
                "user_id": str(user.user_id),
                "email_address": user.email_address,
            },
            count=1,
        )

    async def logout(self, token_id: str):
        print("-------------------------------- Entering UserService.logout")

        if token_id is None:
            return None
        else:
            await add_token_to_blacklist(token_id)
            return True

    async def change_password(self, payload: UserClassChangePassword):

        print(f"User name: {payload.email_address}")
        print(f"New password hash: {payload.new_password}")
        print("-------------------------------- Entering UserService.change_password")
        user = await self.get_user_by_email(payload.email_address)

        if not user:
            return None

        same_password = password_context.verify(
            payload.new_password, user.password_hash
        )

        if same_password:
            return None
        password_hash = password_context.hash(payload.new_password)

        user.password_hash = password_hash
        await self._update(user)
        await self.session.commit()
        return {"message": "Password changed successfully"}
