from uuid import UUID

from pydantic import BaseModel

from schemas.base import BaseSchema, BaseUpdateSchema


class UserClassBase(BaseSchema):
    first_name: str
    last_name: str
    email_address: str


class UserClassRead(UserClassBase):
    user_id: UUID
    user_type_id: UUID


class UserClassCreate(UserClassBase):
    password: str


class UserClassUpdate(BaseUpdateSchema):
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "jwt"


class UserClassChangePassword(BaseModel):
    email_address: str
    new_password: str
