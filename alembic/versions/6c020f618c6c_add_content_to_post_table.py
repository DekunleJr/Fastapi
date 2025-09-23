"""add content to post table

Revision ID: 6c020f618c6c
Revises: eaf11941e401
Create Date: 2025-09-23 01:11:30.835198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c020f618c6c'
down_revision: Union[str, Sequence[str], None] = 'eaf11941e401'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
