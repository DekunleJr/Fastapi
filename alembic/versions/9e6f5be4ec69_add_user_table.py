"""add user table

Revision ID: 9e6f5be4ec69
Revises: 6c020f618c6c
Create Date: 2025-09-23 01:21:13.048912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e6f5be4ec69'
down_revision: Union[str, Sequence[str], None] = '6c020f618c6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
