from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import RecipeIngredientMapping
from schemas.ingredient_recipe_mapping import (
    IngredientRecipeMappingCreateClass,
    IngredientRecipeMappingReadClass,
    IngredientRecipeMappingUpdateClass,
)
from services.base import BaseService
from services.ingredients import IngredientsService


class IngredientRecipeMappingService(BaseService[RecipeIngredientMapping]):
    def __init__(self, session):
        super().__init__(RecipeIngredientMapping, session)

    async def fetch_ingredient_for_recipe(
        self, recipe_id: UUID, recipe_item_id: UUID
    ) -> list[IngredientRecipeMappingReadClass]:
        print(
            "-------------------------------- Entering IngredientRecipeMappingService.fetch_ingredient_recipe_mapping"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.recipe_id == recipe_id, model.recipe_item_id == recipe_item_id
        )

        ingredient_recipe_mapping = await self.session.execute(statement)

        ingredients_service = IngredientsService(self.session)

        rows = ingredient_recipe_mapping.scalars().all()

        result: list[IngredientRecipeMappingReadClass] = []
        for ingredient_mapping in rows:
            ingredient = await ingredients_service.fetch_ingredient_by_id(
                ingredient_mapping.ingredient_id
            )
            if ingredient is None:
                continue

            result.append(
                IngredientRecipeMappingReadClass(
                    recipe_ingredient_mapping_id=ingredient_mapping.recipe_ingredient_mapping_id,
                    ingredient_name=ingredient.ingredient_name,
                    recipe_id=ingredient_mapping.recipe_id,
                    recipe_item_id=ingredient_mapping.recipe_item_id,
                    ingredient_id=ingredient_mapping.ingredient_id,
                    quantity=ingredient_mapping.quantity,
                    comment=ingredient_mapping.comment,
                    price_per_unit=ingredient.price_per_unit,
                )
            )

        if not rows:
            return []
        else:
            return result

    async def create_ingredient_recipe_mapping(
        self, payload: IngredientRecipeMappingCreateClass, username: str
    ):
        print(
            "-------------------------------- Entering IngredientRecipeMappingService.create_ingredient_recipe_mapping"
        )

        ingredient_recipe_mapping = self.model(
            recipe_id=payload.recipe_id,
            recipe_item_id=payload.recipe_item_id,
            ingredient_id=payload.ingredient_id,
            quantity=payload.quantity,
            comment=payload.comment,
            created_by=username,
        )

        return await self._create(ingredient_recipe_mapping)

    async def update_ingredient_recipe_mapping(
        self,
        recipe_ingredient_mapping_id: UUID,
        payload: IngredientRecipeMappingUpdateClass,
        username: str,
    ):
        print(
            "-------------------------------- Entering IngredientRecipeMappingService.update_ingredient_recipe_mapping"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.recipe_ingredient_mapping_id == recipe_ingredient_mapping_id
        )

        ingredient_recipe_mapping = await self.session.execute(statement)

        ingredient_recipe_mapping = ingredient_recipe_mapping.scalars().one()

        if not ingredient_recipe_mapping:
            return None

        ingredient_recipe_mapping.recipe_id = (
            payload.recipe_id or ingredient_recipe_mapping.recipe_id
        )
        ingredient_recipe_mapping.recipe_item_id = (
            payload.recipe_item_id or ingredient_recipe_mapping.recipe_item_id
        )
        ingredient_recipe_mapping.ingredient_id = (
            payload.ingredient_id or ingredient_recipe_mapping.ingredient_id
        )
        ingredient_recipe_mapping.quantity = (
            payload.quantity or ingredient_recipe_mapping.quantity
        )
        ingredient_recipe_mapping.comment = (
            payload.comment or ingredient_recipe_mapping.comment
        )
        ingredient_recipe_mapping.created_by = username

        return await self._update(ingredient_recipe_mapping)

    async def fetch_ingredient_recipe_mapping_by_id(
        self,
        recipe_id: UUID | None,
        recipe_item_id: UUID | None,
        ingredient_id: UUID | None,
        recipe_ingredient_mapping_id: UUID | None,
    ) -> IngredientRecipeMappingReadClass | None:
        print(
            "-------------------------------- Entering IngredientRecipeMappingService.fetch_ingredient_recipe_mapping_by_id"
        )

        model = cast(Any, self.model)
        if recipe_ingredient_mapping_id is not None:
            statement = select(model).where(
                model.recipe_ingredient_mapping_id == recipe_ingredient_mapping_id
            )
        elif (
            recipe_id is not None
            and recipe_item_id is not None
            and ingredient_id is not None
        ):
            statement = select(model).where(
                model.recipe_id == recipe_id,
                model.recipe_item_id == recipe_item_id,
                model.ingredient_id == ingredient_id,
            )

        ingredient_recipe_mapping = await self.session.execute(statement)

        return ingredient_recipe_mapping.scalars().one_or_none()

    async def delete_ingredient_recipe_mapping(
        self, recipe_ingredient_mapping_id: UUID
    ):
        print(
            "-------------------------------- Entering IngredientRecipeMappingService.delete_ingredient_recipe_mapping"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.recipe_ingredient_mapping_id == recipe_ingredient_mapping_id
        )

        ingredient_recipe_mapping = await self.session.execute(statement)

        ingredient_recipe_mapping = ingredient_recipe_mapping.scalars().one()

        if not ingredient_recipe_mapping:
            return None

        return await self._delete(ingredient_recipe_mapping)
