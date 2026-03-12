"""add ai insights table

Revision ID: 0005_add_ai_insights_table
Revises: 0004_add_stock_pools_and_strategy_fields
Create Date: 2026-03-12 16:40:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0005_add_ai_insights_table"
down_revision = "0004_add_stock_pools_and_strategy_fields"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_insights",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("backtest_job_id", sa.String(length=36), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("risks", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["backtest_job_id"], ["backtest_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("backtest_job_id"),
    )


def downgrade() -> None:
    op.drop_table("ai_insights")
