from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import CartRecipeMapping
from schemas.cart_recipe_mapping import CartRecipeMappingReadClass
from schemas.recipes import RecipeCartReadClass
from services.base import BaseService
from services.recipes import RecipesService


class CartRecipeMappingService(BaseService[CartRecipeMapping]):
    def __init__(self, session, recipe_service: RecipesService):
        super().__init__(CartRecipeMapping, session)
        self.recipe_service = recipe_service

    async def get_cart_recipe_mapping_by_cart_id(
        self, cart_id: UUID
    ) -> list[CartRecipeMappingReadClass]:
        print(
            "-------------------------------- Entering CartRecipeMappingService.get_cart_recipe_mapping_by_cart_id"
        )

        model = cast(Any, self.model)

        statement = select(model).where(model.cart_id == cart_id)

        result = await self.session.execute(statement)

        if result is None:
            return []

        rows = list(result.scalars())
        if not rows:
            return []

        recipe_ids = [row.recipe_id for row in rows if row.recipe_id is not None]
        recipe_details_by_id = await self.recipe_service.fetch_recipe_details_by_ids(
            recipe_ids
        )

        mapped_rows: list[CartRecipeMappingReadClass] = []
        for row in rows:
            recipe_id = row.recipe_id
            if row.cart_recipe_id is None or row.cart_id is None or recipe_id is None:
                continue

            recipe_details = recipe_details_by_id.get(recipe_id)
            if recipe_details is None:
                # Fallback when a mapping points to a missing recipe record.
                recipe_details = RecipeCartReadClass(
                    recipe_id=recipe_id,
                    recipe_name="Unknown recipe",
                    image_url="",
                    kit_price=0,
                    vegetarian=False,
                    category_id=UUID(int=0),
                    region_id=UUID(int=0),
                )

            mapped_rows.append(
                CartRecipeMappingReadClass(
                    cart_recipe_id=row.cart_recipe_id,
                    cart_id=row.cart_id,
                    recipe_id=recipe_id,
                    quantity=row.quantity,
                    price=row.price,
                    recipe_details=recipe_details,
                )
            )

        return mapped_rows

    async def get_cart_recipe_mapping_by_cart_id_and_recipe_id(
        self, cart_id: UUID, recipe_id: UUID
    ):
        print(
            "-------------------------------- Entering CartRecipeMappingService.get_cart_recipe_mapping_by_cart_id_and_recipe_id"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.cart_id == cart_id, model.recipe_id == recipe_id
        )

        result = await self.session.execute(statement)

        if not result:
            return None
        return result.scalars().one_or_none()

    async def create_cart_recipe_mapping(
        self, cart_id: UUID, recipe_id: UUID, quantity: int, price: float
    ):
        print(
            "-------------------------------- Entering CartRecipeMappingService.create_cart_recipe_mapping"
        )

        new_mapping = CartRecipeMapping(
            cart_id=cart_id,
            recipe_id=recipe_id,
            quantity=quantity,
            price=price,
        )
        self.session.add(new_mapping)
        await self.session.flush()

    async def delete_cart_recipe_mapping(self, cart_id: UUID, recipe_id: UUID):
        print(
            "-------------------------------- Entering CartRecipeMappingService.delete_cart_recipe_mapping"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.cart_id == cart_id, model.recipe_id == recipe_id
        )

        result = await self.session.execute(statement)

        if result is not None:
            mapping = result.scalars().one_or_none()
            if mapping:
                await self.session.delete(mapping)
                await self.session.flush()
                return mapping
        return None
