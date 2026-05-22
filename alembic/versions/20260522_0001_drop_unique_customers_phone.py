"""Drop unique index on customers.phone (allow duplicate phones).

Revision ID: 20260522_0001
Revises:
Create Date: 2026-05-22

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260522_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    row = conn.execute(
        sa.text(
            "SELECT sql FROM sqlite_master "
            "WHERE type='index' AND name='ix_customers_phone'"
        )
    ).fetchone()
    if row and row[0] and "UNIQUE" in row[0].upper():
        op.execute("DROP INDEX ix_customers_phone")
        op.execute("CREATE INDEX ix_customers_phone ON customers (phone)")


def downgrade() -> None:
    conn = op.get_bind()
    row = conn.execute(
        sa.text(
            "SELECT sql FROM sqlite_master "
            "WHERE type='index' AND name='ix_customers_phone'"
        )
    ).fetchone()
    if row:
        op.execute("DROP INDEX ix_customers_phone")
    op.execute("CREATE UNIQUE INDEX ix_customers_phone ON customers (phone)")
