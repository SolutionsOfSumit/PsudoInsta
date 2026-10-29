"""Create tabled

Revision ID: dd9f6282eca2
Revises: 
Create Date: 2026-10-29 02:12:43.513675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd9f6282eca2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String, nullable=False)

    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'post'
    )
