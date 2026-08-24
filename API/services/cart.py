import asyncio
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    CartDetails,
    CartIngredientMapping,
    CartRecipeMapping,
)
from schemas.cart import CartCreateClass, CartDeleteClass, CartReadClass
from schemas.cart_ingredient_mapping import (
    CartIngredientMappingCreateClass,
    CartIngredientMappingDeleteClass,
)
from schemas.cart_recipe_mapping import CartRecipeMappingCreateClass
from services.base import BaseService
from services.cart_ingredient_mapping import CartIngredientMappingService
from services.cart_recipe_mapping import CartRecipeMappingService


class CartService(BaseService[CartDetails]):
    def __init__(
        self,
        session: AsyncSession,
        cart_recipe_mapping_service: CartRecipeMappingService | None,
        cart_ingredient_mapping_service: CartIngredientMappingService | None,
    ):
        super().__init__(CartDetails, session)
        if cart_recipe_mapping_service and cart_ingredient_mapping_service:
            self.cart_recipe_mapping_service = cart_recipe_mapping_service
            self.cart_ingredient_mapping_service = cart_ingredient_mapping_service

    async def get_cart_by_user_id(self, user_id: UUID) -> CartReadClass | None:
        print("---------------------------- Entering get_cart_by_user_id")

        model = cast(Any, self.model)
        statement = select(model).where(model.user_id == user_id)

        result = await self.session.execute(statement)

        row = result.scalars().one_or_none()

        if not row:
            return None

        recipe_in_cart, ingredients_in_cart = await asyncio.gather(
            self.cart_recipe_mapping_service.get_cart_recipe_mapping_by_cart_id(
                row.cart_id
            ),
            self.cart_ingredient_mapping_service.get_cart_ingredient_mapping_by_cart_id(
                row.cart_id
            ),
        )

        return CartReadClass(
            cart_id=row.cart_id,
            recipe_in_cart=recipe_in_cart,
            ingredients_in_cart=ingredients_in_cart,
        )

    async def get_cart_by_cart_id(self, cart_id: UUID) -> CartReadClass | None:
        print("---------------------------- Entering get_cart_by_cart_id")

        model = cast(Any, self.model)
        statement = select(model).where(model.cart_id == cart_id)

        result = await self.session.execute(statement)

        row = result.scalars().one_or_none()

        if not row:
            return None

        recipe_in_cart, ingredients_in_cart = await asyncio.gather(
            self.cart_recipe_mapping_service.get_cart_recipe_mapping_by_cart_id(
                row.cart_id
            ),
            self.cart_ingredient_mapping_service.get_cart_ingredient_mapping_by_cart_id(
                row.cart_id
            ),
        )

        return CartReadClass(
            cart_id=row.cart_id,
            recipe_in_cart=recipe_in_cart,
            ingredients_in_cart=ingredients_in_cart,
        )

    def _build_recipe_mapping_instances(
        self,
        cart_id: UUID,
        payload_items: list[CartRecipeMappingCreateClass] | None,
    ) -> list[CartRecipeMapping]:
        return [
            CartRecipeMapping(
                cart_id=cart_id,
                recipe_id=item.recipe_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in payload_items or []
        ]

    def _build_ingredient_mapping_instances(
        self,
        cart_id: UUID,
        payload_items: list[CartIngredientMappingCreateClass] | None,
    ) -> list[CartIngredientMapping]:
        return [
            CartIngredientMapping(
                cart_id=cart_id,
                ingredient_id=item.ingredient_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in payload_items or []
        ]

    async def create_cart_by_user_id(
        self, user_id: UUID, created_by: str | None = None
    ) -> CartReadClass | None:
        print("---------------------------- Entering create_cart_by_user_id")

        model = cast(Any, self.model)

        statement = select(model).where(model.user_id == user_id)

        result = await self.session.execute(statement)

        cart = result.scalars().one_or_none()

        if not cart:
            new_cart = model(user_id=user_id, total_amount=0, created_by=created_by)

            result = await self._create(new_cart)

            return CartReadClass(
                cart_id=result.cart_id if result.cart_id else UUID(int=0),
                recipe_in_cart=[],
                ingredients_in_cart=[],
            )
        else:
            return None

    async def update_cart_details(
        self,
        cart_id: UUID,
        payload: CartCreateClass,
        created_by: str | None = None,
    ):
        print("---------------------------- Entering update_cart_details")

        cart_details = await self._get(cart_id)

        if not cart_details:
            return None
        else:
            if payload.recipe_in_cart is not None:
                for recipe_mapping in payload.recipe_in_cart:
                    if recipe_mapping.quantity == 0:
                        await (
                            self.cart_recipe_mapping_service.delete_cart_recipe_mapping(
                                cart_id, recipe_mapping.recipe_id
                            )
                        )
                        cart_details.recipe_in_cart = [
                            recipe_cart
                            for recipe_cart in cart_details.recipe_in_cart
                            if recipe_cart.recipe_id != recipe_mapping.recipe_id
                        ]
                    else:
                        recipe_mapping_instance = next(
                            (
                                recipe_cart
                                for recipe_cart in cart_details.recipe_in_cart
                                if recipe_cart.recipe_id == recipe_mapping.recipe_id
                            ),
                            None,
                        )

                        if recipe_mapping_instance:
                            recipe_mapping_instance.quantity = recipe_mapping.quantity
                            recipe_mapping_instance.price = recipe_mapping.price
                        else:
                            cart_details.recipe_in_cart.append(
                                CartRecipeMapping(
                                    cart_id=cart_id,
                                    recipe_id=recipe_mapping.recipe_id,
                                    quantity=recipe_mapping.quantity,
                                    price=recipe_mapping.price,
                                    created_by=created_by,
                                )
                            )
            if payload.ingredients_in_cart is not None:
                for ingredient_mapping in payload.ingredients_in_cart:
                    if ingredient_mapping.quantity == 0:
                        await self.cart_ingredient_mapping_service.delete_cart_ingredient_mapping_by_cart_id_and_ingredient_id(
                            CartIngredientMappingDeleteClass(
                                cart_id=cart_id,
                                ingredient_id=ingredient_mapping.ingredient_id,
                            )
                        )
                        cart_details.ingredient_in_cart = [
                            cart_ingredient
                            for cart_ingredient in cart_details.ingredient_in_cart
                            if cart_ingredient.ingredient_id
                            != ingredient_mapping.ingredient_id
                        ]
                    else:
                        cart_ingredient_mapping_instance = await self.cart_ingredient_mapping_service.get_cart_ingredient_mapping_by_cart_id_and_ingredient_id(
                            cart_id, ingredient_mapping.ingredient_id
                        )

                        print(
                            "cart_ingredient_mapping_instance: ",
                            cart_ingredient_mapping_instance,
                        )

                        if cart_ingredient_mapping_instance:
                            cart_ingredient_mapping_instance.quantity = (
                                ingredient_mapping.quantity
                            )
                            cart_ingredient_mapping_instance.price = (
                                ingredient_mapping.price
                            )
                        else:
                            await self.cart_ingredient_mapping_service.create_cart_ingredient_mapping(
                                CartIngredientMappingCreateClass(
                                    cart_id=cart_id,
                                    ingredient_id=ingredient_mapping.ingredient_id,
                                    quantity=ingredient_mapping.quantity,
                                    price=ingredient_mapping.price,
                                    recipe_id=ingredient_mapping.recipe_id,
                                ),
                                username=created_by or "",
                            )

            try:
                await self.session.commit()
            except Exception:
                await self.session.rollback()
                raise

            recipe_in_cart, ingredients_in_cart = await asyncio.gather(
                self.cart_recipe_mapping_service.get_cart_recipe_mapping_by_cart_id(
                    cart_id
                ),
                self.cart_ingredient_mapping_service.get_cart_ingredient_mapping_by_cart_id(
                    cart_id
                ),
            )

            return CartReadClass(
                cart_id=cart_details.cart_id or UUID(int=0),
                recipe_in_cart=recipe_in_cart,
                ingredients_in_cart=ingredients_in_cart,
            )

    async def delete_cart_by_cart_id(
        self, payload: CartDeleteClass
    ) -> CartReadClass | None:
        print("---------------------------- Entering delete_cart_by_cart_id")

        if payload.recipe_in_cart:
            for recipe in payload.recipe_in_cart:
                await self.cart_recipe_mapping_service.delete_cart_recipe_mapping(
                    payload.cart_id, recipe
                )

        if payload.ingredients_in_cart:
            for ingredient in payload.ingredients_in_cart:
                await self.cart_ingredient_mapping_service.delete_cart_ingredient_mapping_by_cart_id_and_ingredient_id(
                    CartIngredientMappingDeleteClass(
                        cart_id=payload.cart_id, ingredient_id=ingredient
                    )
                )

        cart_details = await self._get(payload.cart_id)

        if cart_details:
            try:
                await self.session.commit()
            except Exception:
                await self.session.rollback()
                raise
            return CartReadClass(
                cart_id=cart_details.cart_id or UUID(int=0),
                recipe_in_cart=[],
                ingredients_in_cart=[],
            )
        else:
            return None
