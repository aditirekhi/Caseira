from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class SearchResult(BaseModel):
    recipe_id: UUID
    recipe_name: str
    ingredient_list: list[RecipeIngredientSearchList]


class RecipeIngredientSearchList(BaseModel):
    ingredient_id: UUID
    ingredient_name: str
