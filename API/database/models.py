from datetime import date, datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects import postgresql
from sqlmodel import CheckConstraint, Field, Relationship, SQLModel


class MetricDetails(Enum):
    kg = "kilogram"
    g = "gram"
    ml = "milliliter"
    liter = "liter"
    tbsp = "tablespoon"
    tsp = "teaspoon"
    pc = "piece"
    bag = "bag"
    box = "box"
    packet = "packet"
    other = "other"


class DifficultyLevelDetails(Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class AddressDetails(SQLModel, table=True):
    __tablename__: str = "address_details"

    address_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    contact_name: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    contact_number: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )
    address_line_1: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )
    address_line_2: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=True)
    )
    city: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    state_name: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    pincode: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    country: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    google_maps_link: str | None = Field(
        default=None, sa_column=Column(postgresql.TEXT, nullable=True)
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("NOW()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=True)
    )

    users: "UserDetails" = Relationship(
        back_populates="address", sa_relationship_kwargs={"lazy": "selectin"}
    )


class CategoryDetails(SQLModel, table=True):
    __tablename__: str = "category_details"

    category_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    category_name: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, unique=True)
    )
    category_description: str = Field(sa_column=Column(postgresql.TEXT, nullable=False))
    image_url: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("NOW()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    recipes: list["RecipeDetails"] = Relationship(
        back_populates="category", sa_relationship_kwargs={"lazy": "selectin"}
    )


class RegionsDetails(SQLModel, table=True):
    __tablename__: str = "regions_details"

    region_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    region_name: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, unique=True)
    )
    region_description: str = Field(sa_column=Column(postgresql.TEXT, nullable=False))
    image_url: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("NOW()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    recipes: list["RecipeDetails"] = Relationship(
        back_populates="regions", sa_relationship_kwargs={"lazy": "selectin"}
    )


class IngredientDetails(SQLModel, table=True):
    __tablename__: str = "ingredient_details"

    ingredient_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    ingredient_name: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, unique=True)
    )
    ingredient_min_quantity: int = Field(
        sa_column=Column(postgresql.INTEGER, nullable=False)
    )
    ingredient_quantity_metric: str = Field(
        sa_column=Column(
            postgresql.VARCHAR(15),
            CheckConstraint(
                f"ingredient_quantity_metric IN ({', '.join(repr(m.value) for m in MetricDetails)})"
            ),
            nullable=False,
        )
    )
    price_per_unit: float = Field(sa_column=Column(postgresql.FLOAT, nullable=False))
    image_url: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("NOW()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    ingredient_in_cart: list["CartIngredientMapping"] = Relationship(
        back_populates="ingredient", sa_relationship_kwargs={"lazy": "selectin"}
    )
    ingredient_in_order: list["OrderIngredientMapping"] = Relationship(
        back_populates="ingredient", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_ingredient_mapping: list["RecipeIngredientMapping"] = Relationship(
        back_populates="ingredient", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserTypeDetails(SQLModel, table=True):
    __tablename__: str = "user_type_details"

    user_type_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    user_type_name: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, unique=True)
    )
    user_type_description: str = Field(
        sa_column=Column(postgresql.TEXT, nullable=False)
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("NOW()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    users: list["UserDetails"] = Relationship(
        back_populates="user_type", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserDetails(SQLModel, table=True):
    __tablename__: str = "user_details"

    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    first_name: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    last_name: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    username: str = Field(sa_column=Column(postgresql.VARCHAR(255)))
    email_address: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, unique=True)
    )
    password_hash: str = Field(sa_column=Column(postgresql.TEXT, nullable=False))
    address_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("address_details.address_id", ondelete="CASCADE"),
            nullable=True,
        ),
    )
    user_type_id: UUID | None = Field(
        default="ab97c7b4-4823-4510-bdca-c3743b22fa77",
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_type_details.user_type_id", ondelete="CASCADE"),
            nullable=False,
            server_default=text("ab97c7b4-4823-4510-bdca-c3743b22fa77"),
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("NOW()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    address: AddressDetails = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )

    user_type: UserTypeDetails = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )

    most_viewed_recipes: list["UserMostViewedRecipes"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    bookmarked_favorites_recipes: list["UserBookmarkedFavoritesRecipes"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    cart_assigned: "CartDetails" = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    order: list["OrderDetails"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    user_payment_details: list["UserPaymentDetails"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews_by_user: list["RecipeReviews"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy": "selectin"}
    )
    calendar_plan_details: list["UserCalendarPlanDetails"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    helpful_reviews: list["HelpfulReviews"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )


class RecipeDetails(SQLModel, table=True):
    __tablename__: str = "recipe_details"

    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    recipe_name: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, unique=True)
    )
    image_url: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    number_of_total_visits: int = Field(
        sa_column=Column(
            postgresql.INTEGER,
            server_default=text("0"),
        )
    )
    kit_price: float = Field(
        sa_column=Column(postgresql.DOUBLE_PRECISION, nullable=False)
    )
    no_of_people_served: int = Field(
        sa_column=Column(
            postgresql.INTEGER,
            nullable=False,
            server_default=text("1"),
        )
    )
    nutrition_details: list[dict] = Field(
        sa_column=Column(
            postgresql.ARRAY(postgresql.JSONB),
            nullable=False,
        )
    )
    vegetarian: bool = Field(
        sa_column=Column(
            postgresql.BOOLEAN,
            nullable=False,
            server_default=text("false"),
        )
    )
    prep_time: str = Field(
        sa_column=Column(
            postgresql.VARCHAR(50), nullable=False, server_default=text("'0 mins'")
        )
    )
    cook_time: str = Field(
        sa_column=Column(
            postgresql.VARCHAR(50), nullable=False, server_default=text("'0 mins'")
        )
    )
    difficulty_level: DifficultyLevelDetails = Field(
        sa_column=Column(
            postgresql.VARCHAR(10),
            CheckConstraint(
                f"difficulty_level IN ({', '.join(repr(d.value) for d in DifficultyLevelDetails)})"
            ),
            nullable=False,
            server_default=text("'Easy'"),
        )
    )
    total_time: str = Field(
        sa_column=Column(
            postgresql.VARCHAR(50), nullable=False, server_default=text("'0 mins'")
        )
    )
    recipe_description: str = Field(
        sa_column=Column(
            postgresql.TEXT,
            nullable=False,
            server_default=text("'No description provided.'"),
        )
    )
    tips: list[dict] = Field(
        default_factory=list,
        sa_column=Column(
            postgresql.ARRAY(postgresql.JSONB),
            nullable=False,
            server_default=text("'{}'"),
        ),
    )
    features: list[str] = Field(
        default_factory=list,
        sa_column=Column(
            postgresql.ARRAY(postgresql.VARCHAR(50)),
            nullable=False,
            server_default=text("'{}'"),
        ),
    )
    category_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("category_details.category_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    region_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("regions_details.region_id", ondelete="CASCADE"),
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    category: CategoryDetails = Relationship(
        back_populates="recipes", sa_relationship_kwargs={"lazy": "selectin"}
    )
    regions: RegionsDetails = Relationship(
        back_populates="recipes", sa_relationship_kwargs={"lazy": "selectin"}
    )

    most_viewed_recipes: list["UserMostViewedRecipes"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    bookmarked_favorites_recipes: list["UserBookmarkedFavoritesRecipes"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_in_cart: list["CartRecipeMapping"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_ingredient_in_cart: list["CartIngredientMapping"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_in_order: list["OrderRecipeMapping"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_ingredient_mapping: list["RecipeIngredientMapping"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_item: list["RecipeItemDetails"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_directions: list["RecipeDirectionsDetails"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_reviews: list["RecipeReviews"] = Relationship(
        back_populates="recipes", sa_relationship_kwargs={"lazy": "selectin"}
    )
    calendar_plan_details: list["UserCalendarPlanDetails"] = Relationship(
        back_populates="recipe", sa_relationship_kwargs={"lazy": "selectin"}
    )


class RecipeItemDetails(SQLModel, table=True):
    __tablename__: str = "recipe_item_details"

    recipe_item_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    item_name: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=False))
    recipe_id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    item_description: str = Field(
        sa_column=Column(
            postgresql.TEXT,
            nullable=False,
            server_default=text("'No description provided.'"),
        )
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    recipe: RecipeDetails = Relationship(
        back_populates="recipe_item", sa_relationship_kwargs={"lazy": "selectin"}
    )

    recipe_directions: list["RecipeDirectionsDetails"] = Relationship(
        back_populates="recipe_item", sa_relationship_kwargs={"lazy": "selectin"}
    )

    recipe_ingredient_mapping: list["RecipeIngredientMapping"] = Relationship(
        back_populates="recipe_items", sa_relationship_kwargs={"lazy": "selectin"}
    )


class RecipeDirectionsDetails(SQLModel, table=True):
    __tablename__: str = "recipe_directions_details"

    recipe_direction_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            server_default=text("gen_random_uuid()"),
            primary_key=True,
        ),
    )
    recipe_direction: list[str] = Field(
        default_factory=list,
        sa_column=Column(postgresql.ARRAY(postgresql.TEXT), nullable=False),
    )
    recipe_id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    recipe_item_id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_item_details.recipe_item_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    recipe: RecipeDetails = Relationship(
        back_populates="recipe_directions", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe_item: RecipeItemDetails = Relationship(
        back_populates="recipe_directions", sa_relationship_kwargs={"lazy": "selectin"}
    )


class RecipeIngredientMapping(SQLModel, table=True):
    __tablename__: str = "recipe_ingredient_mapping"
    __table_args__ = (
        UniqueConstraint(
            "recipe_id",
            "recipe_item_id",
            "ingredient_id",
            name="uq_recipe_ingredient_mapping_natural_key",
        ),
    )

    recipe_ingredient_mapping_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    recipe_id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    recipe_item_id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_item_details.recipe_item_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    ingredient_id: UUID = Field(
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("ingredient_details.ingredient_id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    quantity: str = Field(sa_column=Column(postgresql.VARCHAR(25), nullable=False))
    comment: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(100), nullable=True)
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    recipe: RecipeDetails = Relationship(
        back_populates="recipe_ingredient_mapping",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    ingredient: IngredientDetails = Relationship(
        back_populates="recipe_ingredient_mapping",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    recipe_items: RecipeItemDetails = Relationship(
        back_populates="recipe_ingredient_mapping",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class UserMostViewedRecipes(SQLModel, table=True):
    __tablename__: str = "user_most_viewed_recipes"
    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id", name="uq_user_most_viewed_recipe"),
    )

    user_most_viewed_recipes_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    number_of_visits: int = Field(
        sa_column=Column(postgresql.INTEGER, server_default=text("0"))
    )
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    user: list[UserDetails] = Relationship(
        back_populates="most_viewed_recipes",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    recipe: list[RecipeDetails] = Relationship(
        back_populates="most_viewed_recipes",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class UserBookmarkedFavoritesRecipes(SQLModel, table=True):
    __tablename__: str = "user_bookmarked_favorites_recipes"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "recipe_id", name="uq_user_bookmarked_favorite_recipe"
        ),
    )

    user_bookmarked_favorites_recipes_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    bookmarked: bool | None = Field(
        default=None,
        sa_column=Column(
            postgresql.BOOLEAN,
            nullable=False,
            server_default=text("false"),
        ),
    )
    favorites: bool | None = Field(
        default=None,
        sa_column=Column(
            postgresql.BOOLEAN,
            nullable=False,
            server_default=text("false"),
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    user: list[UserDetails] = Relationship(
        back_populates="bookmarked_favorites_recipes",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    recipe: list[RecipeDetails] = Relationship(
        back_populates="bookmarked_favorites_recipes",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class CartDetails(SQLModel, table=True):
    __tablename__: str = "cart_details"

    cart_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    user: UserDetails = Relationship(
        back_populates="cart_assigned", sa_relationship_kwargs={"lazy": "selectin"}
    )

    recipe_in_cart: list["CartRecipeMapping"] = Relationship(
        back_populates="cart", sa_relationship_kwargs={"lazy": "selectin"}
    )
    ingredient_in_cart: list["CartIngredientMapping"] = Relationship(
        back_populates="cart", sa_relationship_kwargs={"lazy": "selectin"}
    )


class CartRecipeMapping(SQLModel, table=True):
    __tablename__: str = "cart_recipe_mapping"
    __table_args__ = (
        UniqueConstraint("cart_id", "recipe_id", name="uq_cart_recipe_mapping"),
    )

    cart_recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    cart_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("cart_details.cart_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    quantity: int = Field(sa_column=Column(postgresql.INTEGER, nullable=False))
    price: float = Field(sa_column=Column(postgresql.FLOAT, nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    cart: list[CartDetails] = Relationship(
        back_populates="recipe_in_cart", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe: list[RecipeDetails] = Relationship(
        back_populates="recipe_in_cart", sa_relationship_kwargs={"lazy": "selectin"}
    )


class CartIngredientMapping(SQLModel, table=True):
    __tablename__: str = "cart_ingredient_mapping"
    __table_args__ = (
        UniqueConstraint("cart_id", "ingredient_id", name="uq_cart_ingredient_mapping"),
    )

    cart_ingredient_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=text("gen_random_uuid()"),
        ),
    )
    cart_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("cart_details.cart_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    ingredient_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("ingredient_details.ingredient_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=True,
        ),
    )
    quantity: int = Field(sa_column=Column(postgresql.INTEGER, nullable=False))
    price: float = Field(sa_column=Column(postgresql.FLOAT, nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    cart: list[CartDetails] = Relationship(
        back_populates="ingredient_in_cart", sa_relationship_kwargs={"lazy": "selectin"}
    )
    ingredient: list[IngredientDetails] = Relationship(
        back_populates="ingredient_in_cart", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe: list[RecipeDetails] = Relationship(
        back_populates="recipe_ingredient_in_cart",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class OrderDetails(SQLModel, table=True):
    __tablename__: str = "order_details"

    order_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    total_amount: float = Field(sa_column=Column(postgresql.FLOAT, nullable=False))
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    user_payment_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_payment_details.user_payment_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    user: list[UserDetails] = Relationship(
        back_populates="order", sa_relationship_kwargs={"lazy": "selectin"}
    )
    user_payment_details: "UserPaymentDetails" = Relationship(
        back_populates="order_payment_details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    recipe_in_order: list["OrderRecipeMapping"] = Relationship(
        back_populates="order", sa_relationship_kwargs={"lazy": "selectin"}
    )
    ingredient_in_order: list["OrderIngredientMapping"] = Relationship(
        back_populates="order", sa_relationship_kwargs={"lazy": "selectin"}
    )


class OrderRecipeMapping(SQLModel, table=True):
    __tablename__: str = "order_recipe_mapping"
    __table_args__ = (
        UniqueConstraint("order_id", "recipe_id", name="uq_order_recipe_mapping"),
    )

    order_recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    order_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("order_details.order_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    quantity: int = Field(sa_column=Column(postgresql.INTEGER, nullable=False))
    price: float = Field(sa_column=Column(postgresql.FLOAT, nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    order: list[OrderDetails] = Relationship(
        back_populates="recipe_in_order", sa_relationship_kwargs={"lazy": "selectin"}
    )
    recipe: list[RecipeDetails] = Relationship(
        back_populates="recipe_in_order", sa_relationship_kwargs={"lazy": "selectin"}
    )


class OrderIngredientMapping(SQLModel, table=True):
    __tablename__: str = "order_ingredient_mapping"
    __table_args__ = (
        UniqueConstraint(
            "order_id", "ingredient_id", name="uq_order_ingredient_mapping"
        ),
    )

    order_ingredient_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    order_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("order_details.order_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    ingredient_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("ingredient_details.ingredient_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    quantity: int = Field(sa_column=Column(postgresql.INTEGER, nullable=False))
    price: float = Field(sa_column=Column(postgresql.FLOAT, nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    order: list[OrderDetails] = Relationship(
        back_populates="ingredient_in_order",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    ingredient: list[IngredientDetails] = Relationship(
        back_populates="ingredient_in_order",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class PaymentModeDetails(SQLModel, table=True):
    __tablename__: str = "payment_mode_details"

    payment_mode_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    payment_mode_name: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, unique=True)
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    user_payment_details: list["UserPaymentDetails"] = Relationship(
        back_populates="payment_mode", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserPaymentDetails(SQLModel, table=True):
    __tablename__: str = "user_payment_details"

    user_payment_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    payment_mode_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("payment_mode_details.payment_mode_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    upi_id: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=True))
    card_number: str = Field(sa_column=Column(postgresql.VARCHAR(255), nullable=True))
    card_holder_name: str = Field(
        sa_column=Column(postgresql.VARCHAR(255), nullable=True)
    )
    user_payment_expiry_date: datetime = Field(
        sa_column=Column(postgresql.TIMESTAMP(timezone=True), nullable=True)
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    user: list[UserDetails] = Relationship(
        back_populates="user_payment_details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    payment_mode: list[PaymentModeDetails] = Relationship(
        back_populates="user_payment_details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    order_payment_details: list[OrderDetails] = Relationship(
        back_populates="user_payment_details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )


class RecipeReviews(SQLModel, table=True):
    __tablename__: str = "recipe_reviews"

    recipe_review_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    ratings: int = Field(sa_column=Column(postgresql.INTEGER, nullable=False))
    comment: str | None = Field(sa_column=Column(postgresql.TEXT, nullable=False))
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    recipes: list[RecipeDetails] = Relationship(
        back_populates="recipe_reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )
    users: list[UserDetails] = Relationship(
        back_populates="reviews_by_user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    helpful_reviews: list["HelpfulReviews"] = Relationship(
        back_populates="recipe_review", sa_relationship_kwargs={"lazy": "selectin"}
    )


class HelpfulReviews(SQLModel, table=True):
    __tablename__: str = "helpful_reviews"
    __table_args__ = (
        UniqueConstraint("recipe_review_id", "user_id", name="uq_helpful_reviews"),
    )

    helpful_review_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    recipe_review_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_reviews.recipe_review_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None,
        sa_column=Column(postgresql.VARCHAR(255), nullable=False, default="system"),
    )

    recipe_review: RecipeReviews = Relationship(
        back_populates="helpful_reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )
    user: UserDetails = Relationship(
        back_populates="helpful_reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserCalendarPlanDetails(SQLModel, table=True):
    __tablename__: str = "user_calendar_plan_details"

    user_calendar_plan_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=text("gen_random_uuid()"),
        ),
    )
    user_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("user_details.user_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    recipe_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            postgresql.UUID(as_uuid=True),
            ForeignKey("recipe_details.recipe_id", ondelete="CASCADE"),
            nullable=False,
        ),
    )
    plan_date: date = Field(sa_column=Column(postgresql.DATE, nullable=False))
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            postgresql.TIMESTAMP(timezone=True), nullable=False, default=text("NOW()")
        ),
    )
    created_by: str | None = Field(
        default=None, sa_column=Column(postgresql.VARCHAR(255), nullable=False)
    )

    user: list[UserDetails] = Relationship(
        back_populates="calendar_plan_details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    recipe: list[RecipeDetails] = Relationship(
        back_populates="calendar_plan_details",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
