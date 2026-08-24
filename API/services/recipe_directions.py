from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import RecipeDirectionsDetails
from schemas.recipe_directions import (
    RecipeDirectionsCreate,
    RecipeDirectionsRead,
    RecipeDirectionsUpdate,
)
from services.base import BaseService


class RecipeDirectionsService(BaseService[RecipeDirectionsDetails]):
    def __init__(self, session):
        super().__init__(RecipeDirectionsDetails, session)

    async def get_recipe_directions(
        self, recipe_id: UUID, recipe_item_id: UUID
    ) -> RecipeDirectionsRead | None:
        print(
            "-------------------------------- Entering RecipeDirectionsService.get_recipe_directions"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.recipe_id == recipe_id, model.recipe_item_id == recipe_item_id
        )

        recipe_directions = await self.session.execute(statement)

        recipe_directions = recipe_directions.scalars().one_or_none()

        if not recipe_directions:
            return None

        return RecipeDirectionsRead(
            recipe_direction_id=recipe_directions.recipe_direction_id,
            recipe_directions=recipe_directions.recipe_direction,
            recipe_id=recipe_directions.recipe_id,
            recipe_item_id=recipe_directions.recipe_item_id,
        )

    async def create_recipe_directions(
        self, payload: RecipeDirectionsCreate, username: str
    ):
        print(
            "-------------------------------- Entering RecipeDirectionsService.create_recipe_directions"
        )

        recipe_directions = self.model(
            recipe_id=payload.recipe_id,
            recipe_item_id=payload.recipe_item_id,
            recipe_direction=payload.recipe_directions,
            created_by=username,
        )

        return await self._create(recipe_directions)

    async def update_recipe_directions(
        self, recipe_direction_id: UUID, payload: RecipeDirectionsUpdate, username: str
    ):
        print(
            "-------------------------------- Entering RecipeDirectionsService.update_recipe_directions"
        )

        recipe_directions = await self._get(recipe_direction_id)

        if recipe_directions is None:
            return None
        else:
            recipe_directions.recipe_id = (
                payload.recipe_id or recipe_directions.recipe_id
            )
            recipe_directions.recipe_item_id = (
                payload.recipe_item_id or recipe_directions.recipe_item_id
            )
            recipe_directions.recipe_direction = (
                payload.recipe_directions or recipe_directions.recipe_direction
            )
            recipe_directions.updated_by = username
            return await self._update(recipe_directions)

    async def delete_recipe_directions(self, recipe_direction_id: UUID):
        print(
            "-------------------------------- Entering RecipeDirectionsService.delete_recipe_directions"
        )

        recipe_directions = await self._get(recipe_direction_id)

        if recipe_directions is None:
            return None
        else:
            recipe_direction_deleted = await self._delete(recipe_directions)

            return recipe_direction_deleted
