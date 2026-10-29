"""adding more columns to posts

Revision ID: 01e35cdb21b7
Revises: 8c50db96938c
Create Date: 2026-10-29 16:08:55.970908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01e35cdb21b7'
down_revision: Union[str, Sequence[str], None] = '8c50db96938c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text('now()')
        )
    )
    op.add_column(
        'posts',
        sa.Column(
            'published',
            sa.Boolean,
            nullable=False,
            server_default="True"
        )
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "posts", "created_at"
    )
    op.drop_column("post", "published")
