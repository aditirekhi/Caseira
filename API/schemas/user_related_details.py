from uuid import UUID

from pydantic import BaseModel


class UserDetailsClass(BaseModel):
    user_name: str
    user_email: str
