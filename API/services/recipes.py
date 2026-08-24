import math
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from database.models import RecipeDetails
from schemas.ingredient_recipe_mapping import (
    IngredientRecipeMappingCreateClass,
)
from schemas.ingredients import IngredientClassCreate
from schemas.recipe_directions import RecipeDirectionsCreate
from schemas.recipe_items import RecipeItemsCreate
from schemas.recipes import (
    RecipeCartReadClass,
    RecipesClassCardRead,
    RecipesClassCreate,
    RecipesClassDetailRead,
    RecipesClassUpdate,
)
from schemas.tips import TipsClass
from services.base import BaseService
from services.ingredient_recipe_mapping import IngredientRecipeMappingService
from services.ingredients import IngredientsService


class RecipesService(BaseService[RecipeDetails]):
    def __init__(self, session):
        super().__init__(RecipeDetails, session)

    def getAvgRating(self, reviews):
        totalRatings = 0
        avgRating = 0

        if len(reviews) > 0:
            for review in reviews:
                totalRatings += review.ratings

            avgRating = totalRatings / len(reviews)

        whole = math.floor(avgRating)
        fraction = avgRating - whole

        if fraction <= 0.25:
            rounded_rating = whole
        elif fraction < 0.75:
            rounded_rating = whole + 0.5
        else:
            rounded_rating = whole + 1

        return round(rounded_rating, 1)

    async def fetch_all_recipe_cards(
        self,
        order_by_field: str = "recipe_name",
        direction: str = "asc",
        page_size: int = 20,
    ) -> list[RecipesClassCardRead]:
        print(
            "-------------------------------- Entering RecipesService.fetch_all_recipe_cards"
        )

        model = cast(Any, self.model)

        if direction == "asc":
            statement = (
                select(model).order_by(getattr(model, order_by_field)).limit(page_size)
            )
        else:
            print("Hello")
            statement = (
                select(model)
                .order_by(getattr(model, order_by_field).desc())
                .limit(page_size)
            )

        recipes = await self.session.execute(statement)

        rows = recipes.scalars().all()
        if rows is None:
            return []
        else:
            return [
                RecipesClassCardRead(
                    recipe_id=recipe.recipe_id,
                    recipe_name=recipe.recipe_name,
                    image_url=recipe.image_url,
                    number_of_total_visits=recipe.number_of_total_visits,
                    kit_price=recipe.kit_price,
                    vegetarian=recipe.vegetarian,
                    no_of_people_served=recipe.no_of_people_served,
                    category_id=recipe.category_id,
                    total_time=recipe.total_time,
                    region_id=recipe.region_id,
                    ingredients_count=len(recipe.recipe_ingredient_mapping),
                    recipe_description=recipe.recipe_description,
                    ratings=self.getAvgRating(recipe.recipe_reviews),
                    review_count=str(len(recipe.recipe_reviews)),
                )
                for recipe in rows
            ]

    async def fetch_recipe_by_id(
        self, recipe_id: UUID, user_id: UUID | None = None
    ) -> RecipesClassDetailRead | None:
        print(
            "-------------------------------- Entering RecipesService.fetch_recipe_by_id"
        )
        recipe = await self._get(recipe_id)

        if recipe is None:
            return None
        else:
            from services.category import CategoryService
            from services.recipe_directions import RecipeDirectionsService
            from services.recipe_items import RecipeItemsService
            from services.regions import RegionsService

            category_service = CategoryService(self.session)
            region_service = RegionsService(self.session)
            recipe_items_service = RecipeItemsService(self.session)
            recipe_directions_service = RecipeDirectionsService(self.session)

            if (
                recipe.recipe_id is None
                or recipe.category_id is None
                or recipe.region_id is None
            ):
                return None
            else:
                category = await category_service.fetch_category_by_id(
                    recipe.category_id
                )
                region = await region_service.fetch_region_by_id(recipe.region_id)

                if category is None or region is None:
                    return None

                recipe_items = await recipe_items_service.fetch_all_recipe_items(
                    recipe.recipe_id
                )

                recipe_directions = {}

                for item in recipe_items:
                    directions = await recipe_directions_service.get_recipe_directions(
                        recipe.recipe_id, item.recipe_item_id
                    )
                    if directions is None:
                        return None
                    recipe_directions[item.item_name] = directions.recipe_directions

                ingredient_recipe_mapping_service = IngredientRecipeMappingService(
                    self.session
                )

                ingredients = []

                for item in recipe_items:
                    ingredient_mapping = await ingredient_recipe_mapping_service.fetch_ingredient_for_recipe(
                        recipe.recipe_id, item.recipe_item_id
                    )
                    item_ingredient_mapping = {item.item_name: ingredient_mapping}
                    if ingredient_mapping is not None:
                        ingredients.append(item_ingredient_mapping)

                ingredients_in_cart = []

                print(
                    "recipe.recipe_ingredient_in_cart: ",
                    recipe.recipe_ingredient_in_cart,
                )

                if len(recipe.recipe_ingredient_in_cart) > 0:
                    for ingredient_in_cart in recipe.recipe_ingredient_in_cart:
                        ingredients_in_cart.append(ingredient_in_cart.ingredient_id)

                planned_date = None
                is_bookmarked = False
                is_favorited = False
                if user_id is not None:
                    for planned_recipe in recipe.calendar_plan_details:
                        if planned_recipe.user_id == user_id:
                            planned_date = planned_recipe.plan_date
                            break
                    for bookmarked_recipe in recipe.bookmarked_favorites_recipes:
                        if bookmarked_recipe.user_id == user_id:
                            if bookmarked_recipe.bookmarked:
                                is_bookmarked = True
                            if bookmarked_recipe.favorites:
                                is_favorited = True
                            break

                return RecipesClassDetailRead(
                    recipe_id=recipe.recipe_id,
                    recipe_name=recipe.recipe_name,
                    image_url=recipe.image_url,
                    number_of_total_visits=recipe.number_of_total_visits,
                    kit_price=recipe.kit_price,
                    vegetarian=recipe.vegetarian,
                    no_of_people_served=recipe.no_of_people_served,
                    category_name=category.category_name,
                    region_name=region.region_name,
                    recipe_items=recipe_items,
                    recipe_directions=recipe_directions,
                    nutrition_details=recipe.nutrition_details,
                    prep_time=recipe.prep_time,
                    cook_time=recipe.cook_time,
                    total_time=recipe.total_time,
                    features=recipe.features,
                    difficulty_level=recipe.difficulty_level,
                    ingredients=ingredients,
                    recipe_ingredient_in_cart=ingredients_in_cart,
                    recipe_description=recipe.recipe_description,
                    ratings=self.getAvgRating(recipe.recipe_reviews),
                    tips=[TipsClass.model_validate(tip) for tip in recipe.tips],
                    review_count=str(len(recipe.recipe_reviews)),
                    plan_date=str(planned_date),
                    is_bookmarked=is_bookmarked,
                    is_favorited=is_favorited,
                )

    async def create_recipe(self, payload: RecipesClassCreate, username: str):
        print("-------------------------------- Entering RecipesService.create_recipe")

        from services.category import CategoryService
        from services.regions import RegionsService

        category_service = CategoryService(self.session)
        region_service = RegionsService(self.session)

        category_id = await category_service.get_category_id_by_name(
            payload.category_name
        )
        region_id = await region_service.get_region_id_by_name(payload.region_name)

        if category_id is None or region_id is None:
            return None
        else:
            recipe = self.model(
                recipe_name=payload.recipe_name,
                image_url=payload.image_url,
                number_of_total_visits=payload.number_of_total_visits,
                kit_price=payload.kit_price,
                no_of_people_served=payload.no_of_people_served,
                vegetarian=payload.vegetarian,
                category_id=category_id,
                region_id=region_id,
                nutrition_details=payload.nutrition_details,
                prep_time=payload.prep_time,
                cook_time=payload.cook_time,
                total_time=payload.total_time,
                features=payload.features,
                difficulty_level=payload.difficulty_level,
                recipe_description=payload.recipe_description,
                created_by=username,
                tips=[tip.model_dump() for tip in payload.tips],
            )

            recipe_added = await self._create(recipe)

            if recipe_added.recipe_id is None:
                return None
            else:
                from services.recipe_directions import RecipeDirectionsService
                from services.recipe_items import RecipeItemsService

                recipe_items_service = RecipeItemsService(self.session)
                recipe_directions_service = RecipeDirectionsService(self.session)
                ingredients_service = IngredientsService(self.session)
                ingredient_recipe_mapping_service = IngredientRecipeMappingService(
                    self.session
                )

                for item in payload.recipe_items:
                    recipe_item_payload: RecipeItemsCreate = RecipeItemsCreate(
                        recipe_id=recipe_added.recipe_id,
                        item_name=item.item_name,
                        item_description=item.item_description,
                    )
                    recipe_item = await recipe_items_service.create_recipe_item(
                        recipe_item_payload, username
                    )
                    if recipe_item.recipe_item_id is None:
                        return None
                    else:
                        recipe_directions_payload: RecipeDirectionsCreate = (
                            RecipeDirectionsCreate(
                                recipe_id=recipe_added.recipe_id,
                                recipe_item_id=recipe_item.recipe_item_id,
                                recipe_directions=payload.recipe_direction[
                                    item.item_name
                                ],
                            )
                        )
                        await recipe_directions_service.create_recipe_directions(
                            recipe_directions_payload, username
                        )

                        for ingredient in payload.ingredients[item.item_name]:
                            ingredient_fetched = (
                                await ingredients_service.fetch_ingredient_by_name(
                                    ingredient.ingredient_name
                                )
                            )
                            if ingredient_fetched is None:
                                ingredient_payload: IngredientClassCreate = IngredientClassCreate(
                                    ingredient_name=ingredient.ingredient_name,
                                    ingredient_min_quantity=ingredient.ingredient_min_quantity,
                                    ingredient_quantity_metric=ingredient.ingredient_quantity_metric,
                                    price_per_unit=ingredient.price_per_unit,
                                    image_url=ingredient.image_url,
                                    created_by=username,
                                )
                                ingredient_created = (
                                    await ingredients_service.create_ingredient(
                                        ingredient_payload, username
                                    )
                                )
                                if ingredient_created is None:
                                    return None
                                if ingredient_created.ingredient_id is None:
                                    return None
                                recipe_ingredient_mapping_payload: IngredientRecipeMappingCreateClass = IngredientRecipeMappingCreateClass(
                                    recipe_id=recipe_added.recipe_id,
                                    recipe_item_id=recipe_item.recipe_item_id,
                                    ingredient_id=ingredient_created.ingredient_id,
                                    quantity=ingredient.quantity,
                                    comment=ingredient.comment,
                                )
                                await ingredient_recipe_mapping_service.create_ingredient_recipe_mapping(
                                    recipe_ingredient_mapping_payload, username
                                )
                            else:
                                recipe_ingredient_mapping_payload: IngredientRecipeMappingCreateClass = IngredientRecipeMappingCreateClass(
                                    recipe_id=recipe_added.recipe_id,
                                    recipe_item_id=recipe_item.recipe_item_id,
                                    ingredient_id=ingredient_fetched.ingredient_id,
                                    quantity=ingredient.quantity,
                                    comment=ingredient.comment,
                                )
                                await ingredient_recipe_mapping_service.create_ingredient_recipe_mapping(
                                    recipe_ingredient_mapping_payload, username
                                )

        return recipe

    async def update_recipe(
        self, recipe_id: UUID, payload: RecipesClassUpdate, username: str
    ):
        print("-------------------------------- Entering RecipesService.update_recipe")

        recipe = await self._get(recipe_id)

        if recipe is None:
            return None
        else:
            from services.category import CategoryService
            from services.regions import RegionsService

            category_service = CategoryService(self.session)
            region_service = RegionsService(self.session)

            category_id = None
            region_id = None

            if payload.category_name is not None:
                category_id = await category_service.get_category_id_by_name(
                    payload.category_name
                )
            if payload.region_name is not None:
                region_id = await region_service.get_region_id_by_name(
                    payload.region_name
                )

            recipe.recipe_name = payload.recipe_name or recipe.recipe_name
            recipe.vegetarian = payload.vegetarian or recipe.vegetarian
            recipe.image_url = payload.image_url or recipe.image_url
            recipe.category_id = category_id or recipe.category_id
            recipe.region_id = region_id or recipe.region_id
            recipe.number_of_total_visits = (
                payload.number_of_total_visits or recipe.number_of_total_visits
            )
            recipe.kit_price = payload.kit_price or recipe.kit_price
            recipe.no_of_people_served = (
                payload.no_of_people_served or recipe.no_of_people_served
            )
            recipe.nutrition_details = (
                payload.nutrition_details or recipe.nutrition_details
            )
            recipe.total_time = payload.total_time or recipe.total_time
            recipe.prep_time = payload.prep_time or recipe.prep_time
            recipe.cook_time = payload.cook_time or recipe.cook_time
            recipe.features = payload.features or recipe.features
            recipe.difficulty_level = (
                payload.difficulty_level or recipe.difficulty_level
            )
            recipe.recipe_description = (
                payload.recipe_description
                if payload.recipe_description is not None
                else recipe.recipe_description
            )
            if payload.tips is not None:
                recipe.tips = [tip.model_dump() for tip in payload.tips]

            if recipe.recipe_id is None:
                return None

            updated_recipe = await self._update(recipe)
            return updated_recipe

    async def delete_recipe(self, recipe_id: UUID):
        print("-------------------------------- Entering RecipesService.delete_recipe")

        recipe = await self._get(recipe_id)

        if recipe is None or recipe.recipe_id is None:
            return None
        else:
            from services.recipe_directions import RecipeDirectionsService
            from services.recipe_items import RecipeItemsService

            recipe_items_service = RecipeItemsService(self.session)
            recipe_directions_service = RecipeDirectionsService(self.session)

            recipe_items = await recipe_items_service.fetch_all_recipe_items(
                recipe.recipe_id
            )

            for item in recipe_items:
                recipe_directions_item = (
                    await recipe_directions_service.get_recipe_directions(
                        recipe.recipe_id, item.recipe_item_id
                    )
                )
                if recipe_directions_item is None:
                    return None
                await recipe_directions_service.delete_recipe_directions(
                    recipe_directions_item.recipe_direction_id
                )
                await recipe_items_service.delete_recipe_item(item.recipe_item_id)

            return await self._delete(recipe)

    async def fetch_todays_recipe(self) -> RecipesClassCardRead | None:
        print(
            "-------------------------------- Entering RecipesService.fetch_todays_recipe"
        )

        model = cast(Any, self.model)
        statement = select(model).order_by(model.number_of_total_visits.desc()).limit(5)

        recipes = await self.session.execute(statement)

        rows = recipes.scalars().all()

        if not rows or len(rows) < 5:
            return None
        else:
            return RecipesClassCardRead(
                recipe_id=rows[4].recipe_id,
                recipe_name=rows[4].recipe_name,
                image_url=rows[4].image_url,
                number_of_total_visits=rows[4].number_of_total_visits,
                kit_price=rows[4].kit_price,
                vegetarian=rows[4].vegetarian,
                no_of_people_served=rows[4].no_of_people_served,
                category_id=rows[4].category_id,
                region_id=rows[4].region_id,
                ingredients_count=len(rows[4].recipe_ingredient_mapping),
                recipe_description=rows[4].recipe_description,
                ratings=self.getAvgRating(rows[4].recipe_reviews),
                total_time=rows[4].total_time,
                review_count=str(len(rows[4].recipe_reviews)),
            )

    async def fetch_recipe_details_by_id(
        self, recipe_id: UUID
    ) -> RecipeCartReadClass | None:
        print(
            "-------------------------------- Entering RecipesService.fetch_recipe_details_by_id"
        )
        recipe = await self._get(recipe_id)

        if recipe is None:
            return None
        else:
            return RecipeCartReadClass(
                recipe_id=recipe.recipe_id is not None
                and recipe.recipe_id
                or UUID(int=0),
                recipe_name=recipe.recipe_name,
                image_url=recipe.image_url,
                kit_price=recipe.kit_price,
                vegetarian=recipe.vegetarian,
                category_id=recipe.category_id is not None
                and recipe.category_id
                or UUID(int=0),
                region_id=recipe.region_id is not None
                and recipe.region_id
                or UUID(int=0),
            )

    async def fetch_recipe_details_by_ids(
        self, recipe_ids: list[UUID]
    ) -> dict[UUID, RecipeCartReadClass]:
        print(
            "-------------------------------- Entering RecipesService.fetch_recipe_details_by_ids"
        )

        if not recipe_ids:
            return {}

        unique_recipe_ids = list(dict.fromkeys(recipe_ids))
        model = cast(Any, self.model)
        statement = select(model).where(model.recipe_id.in_(unique_recipe_ids))

        recipes = await self.session.execute(statement)
        rows = recipes.scalars().all()

        details_by_id: dict[UUID, RecipeCartReadClass] = {}
        for recipe in rows:
            if recipe.recipe_id is None:
                continue

            details_by_id[recipe.recipe_id] = RecipeCartReadClass(
                recipe_id=recipe.recipe_id,
                recipe_name=recipe.recipe_name,
                image_url=recipe.image_url,
                kit_price=recipe.kit_price,
                vegetarian=recipe.vegetarian,
                category_id=recipe.category_id or UUID(int=0),
                region_id=recipe.region_id or UUID(int=0),
            )

        return details_by_id
