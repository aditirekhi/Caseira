from uuid import UUID

from pydantic import BaseModel


class RecipeDirectionsBase(BaseModel):
    recipe_directions: list[str]


class RecipeDirectionsRead(RecipeDirectionsBase):
    recipe_direction_id: UUID
    recipe_id: UUID
    recipe_item_id: UUID


class RecipeDirectionsCreate(RecipeDirectionsBase):
    recipe_id: UUID
    recipe_item_id: UUID


class RecipeDirectionsUpdate(BaseModel):
    recipe_directions: list[str] | None = None
    recipe_id: UUID | None = None
    recipe_item_id: UUID | None = None


class RecipeDirectionsDelete(BaseModel):
    recipe_direction_id: UUID
