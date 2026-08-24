from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

Model = TypeVar("Model")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ApiResponse(BaseModel, Generic[Model]):
    success: bool
    data: Model
    message: str


class JWTTokenInfo(BaseModel):
    user_id: str
    email_address: str
    exp: datetime
    jti: str
    count: int
