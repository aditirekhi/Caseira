from uuid import UUID

from pydantic import BaseModel

from schemas.cart_ingredient_mapping import (
    CartIngredientMappingCreateClass,
    CartIngredientMappingReadClass,
    CartIngredientMappingUpdateClass,
)
from schemas.cart_recipe_mapping import (
    CartRecipeMappingCreateClass,
    CartRecipeMappingReadClass,
    CartRecipeMappingUpdateClass,
)


class CartBaseClass(BaseModel):
    recipe_in_cart: list[CartRecipeMappingReadClass]
    ingredients_in_cart: list[CartIngredientMappingReadClass]


class CartReadClass(CartBaseClass):
    cart_id: UUID


class CartCreateClass(CartBaseClass):
    recipe_in_cart: list[CartRecipeMappingCreateClass] | None = None
    ingredients_in_cart: list[CartIngredientMappingCreateClass] | None = None


class CartUpdateClass(BaseModel):
    recipe_in_cart: list[CartRecipeMappingUpdateClass] | None = None
    ingredients_in_cart: list[CartIngredientMappingUpdateClass] | None = None


class CartDeleteClass(BaseModel):
    user_id: UUID
    cart_id: UUID
    recipe_in_cart: list[UUID] | None = None
    ingredients_in_cart: list[UUID] | None = None
