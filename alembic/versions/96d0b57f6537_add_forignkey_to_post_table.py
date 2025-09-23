"""add forignkey to post table

Revision ID: 96d0b57f6537
Revises: 9e6f5be4ec69
Create Date: 2025-09-23 01:28:54.230177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96d0b57f6537'
down_revision: Union[str, Sequence[str], None] = '9e6f5be4ec69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_posts_users', 'posts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_posts_users', 'posts')
    op.drop_column('posts', 'user_id')
    pass
