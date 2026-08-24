"""Add natural-key uniqueness constraints to association tables.

Revision ID: 0f6c2a1b9d4e
Revises: 03e6ceb4c2e5
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "0f6c2a1b9d4e"
down_revision: Union[str, Sequence[str], None] = "03e6ceb4c2e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CONSTRAINTS = (
    (
        "cart_ingredient_mapping",
        "uq_cart_ingredient_mapping",
        ("cart_id", "ingredient_id"),
    ),
    ("cart_recipe_mapping", "uq_cart_recipe_mapping", ("cart_id", "recipe_id")),
    (
        "order_ingredient_mapping",
        "uq_order_ingredient_mapping",
        ("order_id", "ingredient_id"),
    ),
    ("order_recipe_mapping", "uq_order_recipe_mapping", ("order_id", "recipe_id")),
    (
        "recipe_ingredient_mapping",
        "uq_recipe_ingredient_mapping_natural_key",
        ("recipe_id", "recipe_item_id", "ingredient_id"),
    ),
    (
        "user_most_viewed_recipes",
        "uq_user_most_viewed_recipe",
        ("user_id", "recipe_id"),
    ),
    (
        "user_bookmarked_favorites_recipes",
        "uq_user_bookmarked_favorite_recipe",
        ("user_id", "recipe_id"),
    ),
)


def upgrade() -> None:
    connection = op.get_bind()

    for table, constraint_name, columns in CONSTRAINTS:
        column_list = ", ".join(columns)
        connection.execute(
            sa.text(
                f"DELETE FROM {table} WHERE ctid NOT IN "
                f"(SELECT min(ctid) FROM {table} GROUP BY {column_list})"
            )
        )
        op.create_unique_constraint(constraint_name, table, list(columns))


def downgrade() -> None:
    for table, constraint_name, _ in reversed(CONSTRAINTS):
        op.drop_constraint(constraint_name, table, type_="unique")
