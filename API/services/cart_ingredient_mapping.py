from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import CartIngredientMapping
from schemas.cart_ingredient_mapping import (
    CartIngredientMappingCreateClass,
    CartIngredientMappingDeleteClass,
    CartIngredientMappingReadClass,
    CartIngredientMappingUpdateClass,
)
from schemas.ingredients import IngredientsClassRead
from services.base import BaseService
from services.ingredients import IngredientsService


class CartIngredientMappingService(BaseService[CartIngredientMapping]):
    def __init__(self, session: AsyncSession, ingredient_service: IngredientsService):
        super().__init__(CartIngredientMapping, session)
        self.ingredient_service = ingredient_service

    async def get_cart_ingredient_mapping_by_cart_id(
        self, cart_id: UUID
    ) -> list[CartIngredientMappingReadClass]:
        print(
            "-------------------------------- Entering CartIngredientMappingService.get_cart_ingredient_mapping_by_cart_id"
        )

        model = cast(Any, self.model)

        statement = select(model).where(model.cart_id == cart_id)

        result = await self.session.execute(statement)

        if result is None:
            return []

        rows = list(result.scalars())
        if not rows:
            return []

        ingredient_ids = [
            row.ingredient_id for row in rows if row.ingredient_id is not None
        ]
        ingredient_details_by_id = (
            await self.ingredient_service.fetch_ingredient_details_by_ids(
                ingredient_ids
            )
        )

        mapped_rows: list[CartIngredientMappingReadClass] = []
        for row in rows:
            ingredient_id = row.ingredient_id
            if (
                row.cart_ingredient_id is None
                or row.cart_id is None
                or ingredient_id is None
            ):
                continue

            ingredient_details = ingredient_details_by_id.get(ingredient_id)
            if ingredient_details is None:
                # Fallback when a mapping points to a missing ingredient record.
                ingredient_details = IngredientsClassRead(
                    ingredient_id=ingredient_id,
                    ingredient_name="Unknown ingredient",
                    ingredient_min_quantity=0,
                    ingredient_quantity_metric="other",
                    price_per_unit=0,
                    image_url="",
                )

            mapped_rows.append(
                CartIngredientMappingReadClass(
                    cart_ingredient_id=row.cart_ingredient_id,
                    cart_id=row.cart_id,
                    ingredient_id=ingredient_id,
                    quantity=row.quantity,
                    price=row.price,
                    ingredient_details=ingredient_details,
                    recipe_id=row.recipe_id,
                )
            )

        return mapped_rows

    async def get_cart_ingredient_mapping_by_cart_id_and_ingredient_id(
        self, cart_id: UUID, ingredient_id: UUID
    ) -> CartIngredientMapping | None:
        print(
            "-------------------------------- Entering CartIngredientMappingService.get_cart_ingredient_mapping_by_cart_id_and_ingredient_id"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.cart_id == cart_id, model.ingredient_id == ingredient_id
        )

        result = await self.session.execute(statement)

        mappings = list(result.scalars())

        if not mappings:
            return

        # Keep the oldest row when legacy data contains duplicate mappings.
        mapping = mappings[0]
        for duplicate in mappings[1:]:
            await self.session.delete(duplicate)

        return mapping

    async def create_cart_ingredient_mapping(
        self, payload: CartIngredientMappingCreateClass, username: str
    ) -> CartIngredientMappingReadClass | None:
        print(
            "-------------------------------- Entering CartIngredientMappingService.create_cart_ingredient_mapping"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            model.cart_id == payload.cart_id,
            model.ingredient_id == payload.ingredient_id,
        )

        mapping_result = await self.session.execute(query)

        if mapping_result.scalars().first():
            result = await self.update_cart_ingredient_mapping(
                CartIngredientMappingUpdateClass(
                    cart_id=payload.cart_id,
                    ingredient_id=payload.ingredient_id,
                    quantity=payload.quantity,
                    price=payload.price,
                    recipe_id=payload.recipe_id,
                ),
                username,
            )

            return result

        new_mapping = CartIngredientMapping(
            cart_id=payload.cart_id,
            ingredient_id=payload.ingredient_id,
            quantity=payload.quantity,
            price=payload.price,
            recipe_id=payload.recipe_id,
            created_by=username,
        )

        result = await self._create(new_mapping)

        if result is None:
            return None
        else:
            ingredient_details = await self.ingredient_service.fetch_ingredient_details_by_id(
                result.ingredient_id or UUID(int=0)
            )
            if ingredient_details is None:
                ingredient_details = IngredientsClassRead(
                    ingredient_id=result.ingredient_id or UUID(int=0),
                    ingredient_name="Unknown ingredient",
                    ingredient_min_quantity=0,
                    ingredient_quantity_metric="other",
                    price_per_unit=0,
                    image_url="",
                )

            return CartIngredientMappingReadClass(
                cart_ingredient_id=result.cart_ingredient_id or UUID(int=0),
                cart_id=result.cart_id or UUID(int=0),
                ingredient_id=result.ingredient_id or UUID(int=0),
                quantity=result.quantity,
                price=result.price,
                recipe_id=result.recipe_id,
                ingredient_details=ingredient_details,
            )

    async def update_cart_ingredient_mapping(
        self, payload: CartIngredientMappingUpdateClass, username: str
    ) -> CartIngredientMappingReadClass | None:
        print(
            "-------------------------------- Entering CartIngredientMappingService.update_cart_ingredient_mapping"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.cart_id == payload.cart_id,
            model.ingredient_id == payload.ingredient_id,
        )

        mapping_result = await self.session.execute(statement)
        existing_mapping = mapping_result.scalars().one_or_none()

        if not existing_mapping:
            return await self.create_cart_ingredient_mapping(
                CartIngredientMappingCreateClass(
                    cart_id=payload.cart_id or UUID(int=0),
                    ingredient_id=payload.ingredient_id or UUID(int=0),
                    quantity=payload.quantity or 0,
                    price=payload.price or 0.0,
                    recipe_id=payload.recipe_id,
                ),
                username=username,
            )

        else:
            existing_mapping.quantity = payload.quantity
            existing_mapping.price = payload.price

            result = await self._update(existing_mapping)

            if result is None:
                return None
            else:
                ingredient_details = await self.ingredient_service.fetch_ingredient_details_by_id(
                    result.ingredient_id or UUID(int=0)
                )
                if ingredient_details is None:
                    ingredient_details = IngredientsClassRead(
                        ingredient_id=result.ingredient_id or UUID(int=0),
                        ingredient_name="Unknown ingredient",
                        ingredient_min_quantity=0,
                        ingredient_quantity_metric="other",
                        price_per_unit=0,
                        image_url="",
                    )

                return CartIngredientMappingReadClass(
                    cart_ingredient_id=result.cart_ingredient_id or UUID(int=0),
                    cart_id=result.cart_id or UUID(int=0),
                    ingredient_id=result.ingredient_id or UUID(int=0),
                    quantity=result.quantity,
                    price=result.price,
                    recipe_id=result.recipe_id,
                    ingredient_details=ingredient_details,
                )

    async def delete_cart_ingredient_mapping_by_cart_id_and_ingredient_id(
        self, payload: CartIngredientMappingDeleteClass
    ):
        print(
            "-------------------------------- Entering CartIngredientMappingService.delete_cart_ingredient_mapping_by_cart_id_and_ingredient_id"
        )

        model = cast(Any, self.model)
        statement = select(model).where(
            model.cart_id == payload.cart_id,
            model.ingredient_id == payload.ingredient_id,
        )

        result = await self.session.execute(statement)

        rows = list(result.scalars())

        if not rows:
            return

        for row in rows:
            await self.session.delete(row)

        await self.session.flush()

        return rows[0]
