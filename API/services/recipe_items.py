from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import RecipeItemDetails
from schemas.recipe_items import (
    RecipeItemsCreate,
    RecipeItemsRead,
    RecipeItemsUpdate,
)
from services.base import BaseService


class RecipeItemsService(BaseService[RecipeItemDetails]):
    def __init__(self, session):
        super().__init__(RecipeItemDetails, session)

    async def fetch_all_recipe_items(self, recipe_id: UUID) -> list[RecipeItemsRead]:
        print(
            "-------------------------------- Entering RecipeItemsService.fetch_all_recipe_items"
        )

        model = cast(Any, self.model)
        statement = select(model).where(model.recipe_id == recipe_id)

        recipe_items = await self.session.execute(statement)

        rows = recipe_items.scalars().all()
        if not rows:
            return []
        return [
            RecipeItemsRead(
                recipe_item_id=row.recipe_item_id,
                item_name=row.item_name,
                item_description=row.item_description,
            )
            for row in rows
        ]

    async def create_recipe_item(self, payload: RecipeItemsCreate, username: str):
        print(
            "-------------------------------- Entering RecipeItemsService.create_recipe_item"
        )

        recipe_item = self.model(
            item_name=payload.item_name,
            recipe_id=payload.recipe_id,
            item_description=payload.item_description,
            created_by=username,
        )

        return await self._create(recipe_item)

    async def update_recipe_item(
        self, recipe_item_id: UUID, payload: RecipeItemsUpdate, username: str
    ):
        print(
            "-------------------------------- Entering RecipeItemsService.update_recipe_item"
        )

        recipe_item = await self._get(recipe_item_id)

        if recipe_item is None:
            return None
        else:
            recipe_item.item_name = payload.item_name or recipe_item.item_name
            recipe_item.recipe_id = payload.recipe_id or recipe_item.recipe_id

            return await self._update(recipe_item)

    async def delete_recipe_item(self, recipe_item_id: UUID):
        print(
            "-------------------------------- Entering RecipeItemsService.delete_recipe_item"
        )

        recipe_item = await self._get(recipe_item_id)

        if recipe_item is None:
            return None
        else:
            recipe_item_deleted = await self._delete(recipe_item)
            return recipe_item_deleted
