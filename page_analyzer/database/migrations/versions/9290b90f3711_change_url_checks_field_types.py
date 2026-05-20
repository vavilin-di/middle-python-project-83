"""change_url_checks_field_types

Revision ID: 9290b90f3711
Revises: 124902322679
Create Date: 2026-05-20 17:07:31.615899

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '9290b90f3711'
down_revision: str | Sequence[str] | None = '124902322679'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("url_checks", "h1", type_=sa.Text())
    op.alter_column("url_checks", "title", type_=sa.Text())
    op.alter_column("url_checks", "description", type_=sa.Text())


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("url_checks", "h1", type_=sa.String(length=255))
    op.alter_column("url_checks", "title", type_=sa.String(length=255))
    op.alter_column("url_checks", "description", type_=sa.String(length=255))
