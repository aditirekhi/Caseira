from uuid import UUID

from pydantic import BaseModel, field_validator

from database.models import DifficultyLevelDetails
from schemas.ingredient_recipe_mapping import IngredientRecipeMappingReadClass
from schemas.recipe_items import RecipeItemsCreate, RecipeItemsRead
from schemas.tips import TipsClass


class IngredientCreateDetails(BaseModel):
    ingredient_name: str
    ingredient_min_quantity: int
    ingredient_quantity_metric: str
    price_per_unit: float
    image_url: str
    quantity: str
    comment: str | None = None


class RecipesClassBase(BaseModel):
    recipe_name: str
    image_url: str
    number_of_total_visits: int = 0
    kit_price: float
    no_of_people_served: int
    vegetarian: bool
    total_time: str
    ratings: float = 0
    recipe_description: str


class RecipesClassCardRead(RecipesClassBase):
    recipe_id: UUID
    category_id: UUID
    region_id: UUID
    ingredients_count: int = 0
    review_count: str


class RecipesClassDetailRead(RecipesClassBase):
    recipe_id: UUID
    prep_time: str
    cook_time: str
    difficulty_level: DifficultyLevelDetails
    features: list[str]
    category_name: str
    region_name: str
    recipe_items: list[RecipeItemsRead]
    recipe_directions: dict[str, list[str]]
    nutrition_details: list[dict]
    ingredients: list[dict[str, list[IngredientRecipeMappingReadClass]]]
    recipe_ingredient_in_cart: list[UUID]
    tips: list[TipsClass]
    review_count: str
    plan_date: str | None = None
    is_bookmarked: bool = False
    is_favorited: bool = False


class RecipesClassCreate(RecipesClassBase):
    category_name: str
    region_name: str
    recipe_direction: dict[str, list[str]]
    recipe_items: list[RecipeItemsCreate]
    nutrition_details: list[dict]
    prep_time: str
    cook_time: str
    total_time: str
    features: list[str]
    difficulty_level: DifficultyLevelDetails
    ingredients: dict[str, list[IngredientCreateDetails]]
    tips: list[TipsClass]

    @field_validator("recipe_items", mode="before")
    @classmethod
    def validate_recipe_items(cls, value):
        if isinstance(value, str):
            raise TypeError("recipe_items must be an array of item names, not a string")
        if not isinstance(value, list):
            raise TypeError("recipe_items must be an array of item names")
        if any(not isinstance(item, str) for item in value):
            raise TypeError("recipe_items must contain only strings")
        return value

    @field_validator("recipe_direction", mode="before")
    @classmethod
    def validate_recipe_direction(cls, value):
        if not isinstance(value, dict):
            raise TypeError(
                "recipe_direction must be an object of item_name -> list of direction strings"
            )

        for item_name, directions in value.items():
            if not isinstance(item_name, str):
                raise TypeError("recipe_direction keys must be item names as strings")
            if isinstance(directions, str):
                raise TypeError(
                    f"Directions for '{item_name}' must be an array of strings, not a stringified array"
                )
            if not isinstance(directions, list):
                raise TypeError(
                    f"Directions for '{item_name}' must be an array of strings"
                )
            if any(not isinstance(step, str) for step in directions):
                raise TypeError(
                    f"Directions for '{item_name}' must contain only strings"
                )

        return value


class RecipesClassUpdate(BaseModel):
    recipe_name: str | None = None
    image_url: str | None = None
    number_of_total_visits: int | None = None
    kit_price: float | None = None
    no_of_people_served: int | None = None
    vegetarian: bool | None = None
    prep_time: str | None = None
    cook_time: str | None = None
    total_time: str | None = None
    features: list[str] | None = None
    difficulty_level: DifficultyLevelDetails | None = None
    recipe_description: str | None = None
    category_name: str | None = None
    region_name: str | None = None
    recipe_direction: dict[str, list[str]] | None = None
    recipe_items: list[str] | None = None
    nutrition_details: list[dict] | None = None
    tips: list[TipsClass] | None = None


class RecipesClassDelete(BaseModel):
    recipe_id: UUID


class RecipeCartReadClass(BaseModel):
    recipe_id: UUID
    recipe_name: str
    image_url: str
    kit_price: float
    vegetarian: bool
    category_id: UUID
    region_id: UUID
