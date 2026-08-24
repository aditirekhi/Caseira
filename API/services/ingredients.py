from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import IngredientDetails
from schemas.ingredients import (
    IngredientClassCreate,
    IngredientClassUpdate,
    IngredientsClassRead,
)
from services.base import BaseService


class IngredientsService(BaseService[IngredientDetails]):
    def __init__(self, session):
        super().__init__(IngredientDetails, session)

    async def fetch_all_ingredients(self):
        print(
            "-------------------------------- Entering IngredientsService.fetch_all_ingredients"
        )

        model = cast(Any, self.model)
        statement = select(model).order_by(model.ingredient_name.asc())

        ingredients = await self.session.execute(statement)

        if ingredients is None:
            return []
        else:
            return ingredients.scalars().all()

    async def fetch_ingredient_by_name(self, ingredient_name: str):
        print(
            "-------------------------------- Entering IngredientsService.fetch_ingredient_by_name"
        )

        model = cast(Any, self.model)
        statement = select(model).where(model.ingredient_name == ingredient_name)

        ingredient = await self.session.execute(statement)

        return ingredient.scalars().one_or_none()

    async def fetch_ingredient_by_id(self, ingredient_id: UUID):
        print(
            "-------------------------------- Entering IngredientsService.fetch_ingredient_by_id"
        )

        ingredient = await self._get(ingredient_id)

        if ingredient is None:
            return None
        else:
            return ingredient

    async def create_ingredient(self, payload: IngredientClassCreate, username: str):
        print(
            "-------------------------------- Entering IngredientsService.create_ingredient"
        )

        ingredient_name_exists = await self.check_ingredient_name_exists(
            payload.ingredient_name
        )

        if ingredient_name_exists:
            return None
        else:
            ingredient = self.model(
                ingredient_name=payload.ingredient_name,
                ingredient_min_quantity=payload.ingredient_min_quantity,
                ingredient_quantity_metric=payload.ingredient_quantity_metric,
                price_per_unit=payload.price_per_unit,
                image_url=payload.image_url,
                created_by=username,
            )

            return await self._create(ingredient)

    async def update_ingredient(
        self, ingredient_id: UUID, payload: IngredientClassUpdate, username: str
    ):
        print(
            "-------------------------------- Entering IngredientsService.update_ingredient"
        )

        ingredient = await self._get(ingredient_id)

        if ingredient is None:
            return None
        else:
            ingredient.ingredient_name = (
                payload.ingredient_name or ingredient.ingredient_name
            )
            ingredient.ingredient_min_quantity = (
                payload.ingredient_min_quantity or ingredient.ingredient_min_quantity
            )
            ingredient.ingredient_quantity_metric = (
                payload.ingredient_quantity_metric
                or ingredient.ingredient_quantity_metric
            )
            ingredient.price_per_unit = (
                payload.price_per_unit or ingredient.price_per_unit
            )
            ingredient.image_url = payload.image_url or ingredient.image_url
            ingredient.updated_by = username

            return await self._update(ingredient)

    async def delete_ingredient(self, ingredient_id: UUID):
        print(
            "-------------------------------- Entering IngredientsService.delete_ingredient"
        )

        ingredient = await self._get(ingredient_id)

        if ingredient is None:
            return None
        else:
            return await self._delete(ingredient)

    async def check_ingredient_name_exists(self, ingredient_name):
        print(
            "-------------------------------- Entering IngredientsService.check_ingredient_name_exists"
        )

        model = cast(Any, self.model)
        statement = select(model).where(model.ingredient_name == ingredient_name)

        ingredient = await self.session.execute(statement)

        ingredient = ingredient.scalar_one_or_none()
        return ingredient

    async def fetch_ingredient_details_by_id(
        self, ingredient_id: UUID
    ) -> IngredientsClassRead | None:
        print(
            "-------------------------------- Entering IngredientsService.fetch_ingredient_details_by_id"
        )

        ingredient = await self._get(ingredient_id)

        if ingredient is None:
            return None
        else:
            return IngredientsClassRead(
                ingredient_id=ingredient.ingredient_id
                if ingredient.ingredient_id is not None
                else UUID(int=0),
                ingredient_name=ingredient.ingredient_name,
                ingredient_min_quantity=ingredient.ingredient_min_quantity,
                ingredient_quantity_metric=ingredient.ingredient_quantity_metric,
                price_per_unit=ingredient.price_per_unit,
                image_url=ingredient.image_url,
            )

    async def fetch_ingredient_details_by_ids(
        self, ingredient_ids: list[UUID]
    ) -> dict[UUID, IngredientsClassRead]:
        print(
            "-------------------------------- Entering IngredientsService.fetch_ingredient_details_by_ids"
        )

        if not ingredient_ids:
            return {}

        unique_ingredient_ids = list(dict.fromkeys(ingredient_ids))
        model = cast(Any, self.model)
        statement = select(model).where(model.ingredient_id.in_(unique_ingredient_ids))

        ingredients = await self.session.execute(statement)
        rows = ingredients.scalars().all()

        details_by_id: dict[UUID, IngredientsClassRead] = {}
        for ingredient in rows:
            if ingredient.ingredient_id is None:
                continue

            details_by_id[ingredient.ingredient_id] = IngredientsClassRead(
                ingredient_id=ingredient.ingredient_id,
                ingredient_name=ingredient.ingredient_name,
                ingredient_min_quantity=ingredient.ingredient_min_quantity,
                ingredient_quantity_metric=ingredient.ingredient_quantity_metric,
                price_per_unit=ingredient.price_per_unit,
                image_url=ingredient.image_url,
            )

        return details_by_id
