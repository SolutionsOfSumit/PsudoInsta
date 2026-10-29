"""User's table

Revision ID: abcf1b883630
Revises: c75b2b9abe2c
Create Date: 2026-10-29 14:09:03.981923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abcf1b883630'
down_revision: Union[str, Sequence[str], None] = 'c75b2b9abe2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', 
                    sa.Integer,
                    nullable=False, 
                    primary_key=True),
        sa.Column('email',
                    sa.String,
                    unique=True,
                    nullable=False),
        sa.Column('password', 
                    sa.String, 
                    nullable=False),
        sa.Column('created_at', 
                    sa.TIMESTAMP(timezone=True), 
                    server_default=sa.text('now()'), 
                    nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
