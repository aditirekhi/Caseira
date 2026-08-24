from uuid import UUID

from pydantic import BaseModel

from schemas.base import BaseSchema, BaseUpdateSchema


class IngredientsClassBase(BaseSchema):
    ingredient_name: str
    ingredient_min_quantity: int
    ingredient_quantity_metric: str
    price_per_unit: float
    image_url: str


class IngredientsClassRead(IngredientsClassBase):
    ingredient_id: UUID


class IngredientClassCreate(IngredientsClassBase):
    created_by: str


class IngredientClassUpdate(BaseUpdateSchema):
    ingredient_name: str | None = None
    ingredient_min_quantity: int | None = None
    ingredient_quantity_metric: str | None = None
    price_per_unit: float | None = None
    image_url: str | None = None


class IngredientClassDelete(BaseModel):
    ingredient_id: UUID
