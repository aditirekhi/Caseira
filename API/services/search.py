from typing import Any, cast

from sqlmodel import func, select

from database.models import RecipeIngredientSearchDocument
from schemas.search import RecipeIngredientSearchList, SearchResult
from services.ingredients import IngredientsService
from services.recipes import RecipesService


class SearchService:
    def __init__(self, session):
        self.session = session
        self.model = RecipeIngredientSearchDocument

    async def search_recipes_ingredients(
        self, keyword: str, limit: int
    ) -> list[SearchResult]:
        print(
            "-------------------------------- Entering SearchService.search_recipes_ingredients"
        )

        if not keyword:
            return []

        model = cast(Any, self.model)

        prefix_query = " & ".join(f"{term}:*" for term in keyword.split() if term)
        ts_query = func.to_tsquery("simple", prefix_query)

        statement = (
            select(model).where(model.document.bool_op("@@")(ts_query)).limit(limit)
        )

        results = await self.session.execute(statement)

        rows = results.scalars().all()

        if not rows:
            return []

        ingredients_service = IngredientsService(self.session)
        recipes_service = RecipesService(self.session)

        search_results: list[SearchResult] = []

        terms = [t.lower() for t in keyword.split() if t]

        for row in rows:
            ingredient_name = await ingredients_service.get_ingredient_name(
                row.ingredient_id
            )

            # Only include this ingredient if the ingredient name actually
            # matches the search keyword. A row also matches when just the
            # recipe name matches, in which case the ingredient is unrelated.
            matched_ingredient = None
            if any(
                ingredient_name.lower().startswith(t) or t in ingredient_name.lower()
                for t in terms
            ):
                matched_ingredient = RecipeIngredientSearchList(
                    ingredient_id=row.ingredient_id,
                    ingredient_name=ingredient_name,
                )

            if row.recipe_id in [result.recipe_id for result in search_results]:
                result = next(
                    result
                    for result in search_results
                    if result.recipe_id == row.recipe_id
                )

                if matched_ingredient:
                    result.ingredient_list.append(matched_ingredient)
                continue

            search_results.append(
                SearchResult(
                    recipe_id=row.recipe_id,
                    recipe_name=await recipes_service.get_recipe_name(row.recipe_id),
                    ingredient_list=[matched_ingredient] if matched_ingredient else [],
                )
            )

        return search_results
