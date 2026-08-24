from uuid import UUID

from pydantic import BaseModel

from schemas.base import BaseSchema, BaseUpdateSchema


class CategoryClassBase(BaseSchema):
    category_name: str
    category_description: str
    image_url: str


class CategoryClassRead(CategoryClassBase):
    category_id: UUID
    recipes_count: int = 0


class CategoryClassCreate(CategoryClassBase):
    pass


class CategoryClassUpdate(BaseUpdateSchema):
    category_name: str | None = None
    category_description: str | None = None
    image_url: str | None = None


class CategoryClassDelete(BaseModel):
    category_id: UUID
