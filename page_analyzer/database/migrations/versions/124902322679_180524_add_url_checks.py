"""180524_add_url_checks

Revision ID: 124902322679
Revises: edfe6ac01054
Create Date: 2026-05-18 16:25:51.945683

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "124902322679"
down_revision: str | Sequence[str] | None = "edfe6ac01054"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "url_checks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url_id", sa.Integer(), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=True),
        sa.Column("h1", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["url_id"], ["urls.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("url_checks")
