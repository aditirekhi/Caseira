from uuid import UUID

from pydantic import BaseModel

from schemas.recipes import RecipeCartReadClass


class CartRecipeMappingBaseClass(BaseModel):
    cart_id: UUID
    recipe_id: UUID
    quantity: int
    price: float


class CartRecipeMappingReadClass(CartRecipeMappingBaseClass):
    cart_recipe_id: UUID
    recipe_details: RecipeCartReadClass


class CartRecipeMappingCreateClass(CartRecipeMappingBaseClass):
    pass


class CartRecipeMappingUpdateClass(BaseModel):
    cart_id: UUID | None = None
    recipe_id: UUID | None = None
    quantity: int | None = None
    price: float | None = None
