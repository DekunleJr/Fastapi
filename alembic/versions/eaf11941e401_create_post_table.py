"""create post table

Revision ID: eaf11941e401
Revises: 
Create Date: 2025-09-23 00:59:41.011386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eaf11941e401'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op. create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        # sa.Column('content', sa.String(), nullable=False),
        # sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
        # sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
