"""Added image url field for category and regions table

Revision ID: 8b85db9ca9a8
Revises: ad88796ebae6
Create Date: 2026-07-24 10:27:51.968520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b85db9ca9a8'
down_revision: Union[str, Sequence[str], None] = 'ad88796ebae6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
