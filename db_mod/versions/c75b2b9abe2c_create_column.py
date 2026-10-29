"""Create Column

Revision ID: c75b2b9abe2c
Revises: dd9f6282eca2
Create Date: 2026-10-29 02:40:42.499218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c75b2b9abe2c'
down_revision: Union[str, Sequence[str], None] = 'dd9f6282eca2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column("content", sa.String, nullable=False)
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("post", "content")
