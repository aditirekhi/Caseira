"""Create recipe ingredient mapping table

Revision ID: f31b9e2a7c1d
Revises: b86e0a3fb766
Create Date: 2026-07-25 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f31b9e2a7c1d"
down_revision: Union[str, Sequence[str], None] = "b86e0a3fb766"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "recipe_ingredient_mapping",
        sa.Column(
            "recipe_ingredient_id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("recipe_id", sa.UUID(), nullable=False),
        sa.Column("ingredient_id", sa.UUID(), nullable=False),
        sa.Column("quantity", sa.VARCHAR(length=25), nullable=False),
        sa.Column("comment", sa.VARCHAR(length=100), nullable=True),
        sa.ForeignKeyConstraint(
            ["recipe_id"], ["recipe_details.recipe_id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["ingredient_id"], ["ingredient_details.ingredient_id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("recipe_ingredient_id"),
    )


def downgrade() -> None:
    op.drop_table("recipe_ingredient_mapping")
