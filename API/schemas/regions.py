from uuid import UUID

from schemas.base import BaseSchema, BaseUpdateSchema


class RegionsClassBase(BaseSchema):
    region_name: str
    region_description: str
    image_url: str


class RegionsClassRead(RegionsClassBase):
    region_id: UUID
    recipes_count: int = 0


class RegionsClassCreate(RegionsClassBase):
    pass


class RegionsClassUpdate(BaseUpdateSchema):
    region_name: str | None = None
    region_description: str | None = None
    image_url: str | None = None
