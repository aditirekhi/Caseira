"""Added a new search vector table for the recipes and ingredients

Revision ID: e075e70d6438
Revises: fd2664d21301
Create Date: 2026-09-03 19:28:18.508168

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e075e70d6438"
down_revision: Union[str, Sequence[str], None] = "fd2664d21301"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "recipe_ingredient_search_documents",
        sa.Column("recipe_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ingredient_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("document", postgresql.TSVECTOR(), nullable=False),
        sa.ForeignKeyConstraint(
            ["recipe_id"], ["recipe_details.recipe_id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredient_details.ingredient_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("recipe_id", "ingredient_id"),
    )
    op.create_index(
        "ix_recipe_ingredient_search_documents_document",
        "recipe_ingredient_search_documents",
        ["document"],
        postgresql_using="gin",
    )
    op.create_index(
        "ix_recipe_ingredient_search_documents_ingredient_id",
        "recipe_ingredient_search_documents",
        ["ingredient_id"],
    )
    op.execute(
        sa.text(
            """
            INSERT INTO recipe_ingredient_search_documents
                (recipe_id, ingredient_id, document)
            SELECT DISTINCT
                r.recipe_id,
                i.ingredient_id,
                to_tsvector(
                    'simple',
                    coalesce(r.recipe_name, '') || ' ' ||
                    coalesce(i.ingredient_name, '')
                )
            FROM recipe_details r
            JOIN recipe_ingredient_mapping rim
                ON rim.recipe_id = r.recipe_id
            JOIN ingredient_details i
                ON i.ingredient_id = rim.ingredient_id
            """
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_recipe_ingredient_search_documents_ingredient_id",
        table_name="recipe_ingredient_search_documents",
    )
    op.drop_index(
        "ix_recipe_ingredient_search_documents_document",
        table_name="recipe_ingredient_search_documents",
    )
    op.drop_table("recipe_ingredient_search_documents")
