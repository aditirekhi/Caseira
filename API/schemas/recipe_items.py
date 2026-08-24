from uuid import UUID

from pydantic import BaseModel


class RecipeItemsBase(BaseModel):
    item_name: str
    item_description: str


class RecipeItemsRead(RecipeItemsBase):
    recipe_item_id: UUID


class RecipeItemsCreate(RecipeItemsBase):
    recipe_id: UUID


class RecipeItemsUpdate(BaseModel):
    item_name: str | None = None
    item_description: str | None = None
    recipe_id: UUID | None = None


class RecipeItemsDelete(BaseModel):
    recipe_item_id: UUID
