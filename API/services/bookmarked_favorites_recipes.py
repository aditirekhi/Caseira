from typing import Any, cast
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import UserBookmarkedFavoritesRecipes
from schemas.bookmarked_favorites_recipes import (
    BookmarkedFavoritesReadClass,
    BookmarkedFavoritesRecipeCreateClass,
    IsBookmarkedResponse,
    IsFavoritedResponse,
)
from schemas.recipes import RecipesClassCardRead
from services.base import BaseService


class BookmarkedFavoritesRecipesService(BaseService[UserBookmarkedFavoritesRecipes]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserBookmarkedFavoritesRecipes, session=session)

    async def get_favorites_for_user(self, user_id: UUID) -> list[RecipesClassCardRead]:
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.get_favorites_for_user"
        )

        model = cast(Any, self.model)
        query = select(model).where(model.user_id == user_id, model.favorites == True)

        result = await self.session.execute(query)
        favorites = result.scalars().all()

        if favorites is None:
            return []
        else:
            return [
                RecipesClassCardRead(
                    recipe_id=favorite.recipe_id,
                    recipe_name=favorite.recipe_name,
                    image_url=favorite.image_url,
                    kit_price=favorite.kit_price,
                    no_of_people_served=favorite.no_of_people_served,
                    vegetarian=favorite.vegetarian,
                    total_time=favorite.total_time,
                    recipe_description=favorite.recipe_description,
                    category_id=favorite.category_id,
                    region_id=favorite.region_id,
                    review_count=favorite.review_count,
                )
                for favorite in favorites
            ]

    async def add_favorite_for_user(
        self, payload: BookmarkedFavoritesRecipeCreateClass, username: str
    ) -> BookmarkedFavoritesReadClass | None:
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.add_favorite_for_user"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            (model.user_id == payload.user_id) & (model.recipe_id == payload.recipe_id)
        )

        result = await self.session.execute(query)
        existing_recipe = result.scalars().first()

        if existing_recipe:
            existing_recipe.favorites = True
            result = await self._update(existing_recipe)
        else:
            new_favorite = self.model(
                user_id=payload.user_id,
                recipe_id=payload.recipe_id,
                bookmarked=False,
                favorites=True,
                created_by=username,
            )
            result = await self._create(new_favorite)

        if not result:
            return None

        return BookmarkedFavoritesReadClass(
            user_id=result.user_id or UUID(int=0),
            recipe_id=result.recipe_id or UUID(int=0),
            bookmarked=result.bookmarked or False,
            favorites=result.favorites or False,
        )

    async def remove_favorite_for_user(
        self, payload: BookmarkedFavoritesRecipeCreateClass
    ):
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.remove_favorite_for_user"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            (model.user_id == payload.user_id)
            & (model.recipe_id == payload.recipe_id)
            & (model.favorites == True)
        )

        result = await self.session.execute(query)
        favorite_to_remove = result.scalars().first()

        if not favorite_to_remove:
            return None

        favorite_to_remove.favorites = False
        if favorite_to_remove.bookmarked is False:
            await self._delete(favorite_to_remove)
        else:
            await self._update(favorite_to_remove)

        return favorite_to_remove

    async def is_recipe_favorited_by_user(
        self, user_id: UUID, recipe_id: UUID
    ) -> IsFavoritedResponse:
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.is_recipe_favorited_by_user"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            (model.user_id == user_id)
            & (model.recipe_id == recipe_id)
            & (model.favorites == True)
        )

        result = await self.session.execute(query)
        favorite = result.scalars().first()

        return IsFavoritedResponse(is_favorited=favorite is not None)

    async def get_bookmarked_recipes_for__user(
        self, user_id: UUID
    ) -> list[RecipesClassCardRead]:
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.get_bookmarked_recipes_for_user"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            (model.user_id == user_id) & (model.bookmarked == True)
        )

        result = await self.session.execute(query)
        bookmarked_recipes = result.scalars().all()

        if bookmarked_recipes is None:
            return []
        else:
            return [
                RecipesClassCardRead(
                    recipe_id=recipe.recipe_id,
                    recipe_name=recipe.recipe_name,
                    image_url=recipe.image_url,
                    kit_price=recipe.kit_price,
                    no_of_people_served=recipe.no_of_people_served,
                    vegetarian=recipe.vegetarian,
                    total_time=recipe.total_time,
                    recipe_description=recipe.recipe_description,
                    category_id=recipe.category_id,
                    region_id=recipe.region_id,
                    review_count=recipe.review_count,
                )
                for recipe in bookmarked_recipes
            ]

    async def add_bookmarked_recipe_for_user(
        self, payload: BookmarkedFavoritesRecipeCreateClass, username: str
    ) -> BookmarkedFavoritesReadClass | None:
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.add_bookmarked_recipe_for_user"
        )

        model = cast(Any, self.model)
        recipe_exists_query = select(model).where(
            (model.user_id == payload.user_id) & (model.recipe_id == payload.recipe_id)
        )

        result = await self.session.execute(recipe_exists_query)
        existing_recipe = result.scalars().first()
        if existing_recipe:
            existing_recipe.bookmarked = True
            result = await self._update(existing_recipe)
        else:
            new_bookmarked_recipe = self.model(
                user_id=payload.user_id,
                recipe_id=payload.recipe_id,
                bookmarked=True,
                favorites=False,
                created_by=username,
            )
            result = await self._create(new_bookmarked_recipe)

        if not result:
            return None

        return BookmarkedFavoritesReadClass(
            user_id=result.user_id or UUID(int=0),
            recipe_id=result.recipe_id or UUID(int=0),
            bookmarked=result.bookmarked or False,
            favorites=result.favorites or False,
        )

    async def remove_bookmarked_recipe_for_user(
        self, payload: BookmarkedFavoritesRecipeCreateClass
    ):
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.remove_bookmarked_recipe_for_user"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            (model.user_id == payload.user_id)
            & (model.recipe_id == payload.recipe_id)
            & (model.bookmarked == True)
        )

        result = await self.session.execute(query)
        bookmarked_recipe_to_remove = result.scalars().first()

        if not bookmarked_recipe_to_remove:
            return None

        bookmarked_recipe_to_remove.bookmarked = False
        if bookmarked_recipe_to_remove.favorites is False:
            await self._delete(bookmarked_recipe_to_remove)
        else:
            await self._update(bookmarked_recipe_to_remove)

        return bookmarked_recipe_to_remove

    async def is_recipe_bookmarked_by_user(
        self, user_id: UUID, recipe_id: UUID
    ) -> IsBookmarkedResponse:
        print(
            "-------------------------------- Entering BookmarkedFavoritesRecipesService.is_recipe_bookmarked_by_user"
        )

        model = cast(Any, self.model)
        query = select(model).where(
            (model.user_id == user_id)
            & (model.recipe_id == recipe_id)
            & (model.bookmarked == True)
        )

        result = await self.session.execute(query)
        bookmarked_recipe = result.scalars().first()

        return IsBookmarkedResponse(is_bookmarked=bookmarked_recipe is not None)
