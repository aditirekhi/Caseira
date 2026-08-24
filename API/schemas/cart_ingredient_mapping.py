from uuid import UUID

from pydantic import BaseModel

from schemas.ingredients import IngredientsClassRead


class CartIngredientMappingBaseClass(BaseModel):
    cart_id: UUID
    quantity: int
    price: float
    recipe_id: UUID | None


class CartIngredientMappingReadClass(CartIngredientMappingBaseClass):
    cart_ingredient_id: UUID
    ingredient_details: IngredientsClassRead
    ingredient_id: UUID


class CartIngredientMappingCreateClass(CartIngredientMappingBaseClass):
    ingredient_id: UUID


class CartIngredientMappingUpdateClass(BaseModel):
    cart_id: UUID | None = None
    ingredient_id: UUID | None = None
    quantity: int | None = None
    price: float | None = None
    recipe_id: UUID | None = None


class CartIngredientMappingDeleteClass(BaseModel):
    cart_id: UUID
    ingredient_id: UUID
