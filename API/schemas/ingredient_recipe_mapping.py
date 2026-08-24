from uuid import UUID

from pydantic import BaseModel


class IngredientRecipeMappingBaseClass(BaseModel):
    recipe_id: UUID
    recipe_item_id: UUID
    ingredient_id: UUID
    quantity: str
    comment: str | None = None


class IngredientRecipeMappingReadClass(IngredientRecipeMappingBaseClass):
    recipe_ingredient_mapping_id: UUID
    ingredient_name: str
    ingredient_id: UUID
    price_per_unit: float
    # recipe_name: str
    # recipe_item_name: str


class IngredientRecipeMappingCreateClass(IngredientRecipeMappingBaseClass):
    pass


class IngredientRecipeMappingUpdateClass(BaseModel):
    recipe_id: UUID | None = None
    recipe_item_id: UUID | None = None
    ingredient_id: UUID | None = None
    quantity: str | None = None
    comment: str | None = None
    price_per_unit: float | None = None


class IngredientRecipeMappingDeleteClass(BaseModel):
    recipe_ingredient_mapping_id: UUID
