"""adding frogine key constrain to post table

Revision ID: 8c50db96938c
Revises: abcf1b883630
Create Date: 2026-10-29 14:41:26.233166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c50db96938c'
down_revision: Union[str, Sequence[str], None] = 'abcf1b883630'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'posts',
        sa.Column('user_id',
                sa.Integer,
                nullable=False
        )
    )
    op.create_foreign_key(
        'fk_users_to_posts',
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_users_to_posts', table_name="posts")
    op.drop_column('posts', 'user_id')
