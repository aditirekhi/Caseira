"""Backfill recipe and ingredient search documents.

Revision ID: f4a6b8c0d2e4
Revises: d8d5d3dc1f21
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "f4a6b8c0d2e4"
down_revision: Union[str, Sequence[str], None] = "d8d5d3dc1f21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
            ON CONFLICT (recipe_id, ingredient_id) DO UPDATE
            SET document = EXCLUDED.document
            """
        )
    )


def downgrade() -> None:
    op.execute(sa.text("DELETE FROM recipe_ingredient_search_documents"))
