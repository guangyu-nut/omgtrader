"""add data coverage table

Revision ID: 0003_add_data_coverage_table
Revises: 0002_add_market_data_source_tables
Create Date: 2026-03-12 15:35:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0003_add_data_coverage_table"
down_revision = "0002_add_market_data_source_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "data_coverages",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("symbol_code", sa.String(length=16), nullable=False),
        sa.Column("daily_start", sa.Date(), nullable=True),
        sa.Column("daily_end", sa.Date(), nullable=True),
        sa.Column("minute_start", sa.DateTime(), nullable=True),
        sa.Column("minute_end", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol_code"),
    )


def downgrade() -> None:
    op.drop_table("data_coverages")
