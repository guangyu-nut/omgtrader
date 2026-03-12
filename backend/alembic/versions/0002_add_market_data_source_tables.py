"""add market data source tables

Revision ID: 0002_add_market_data_source_tables
Revises: 0001_initial_core_tables
Create Date: 2026-03-12 15:20:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0002_add_market_data_source_tables"
down_revision = "0001_initial_core_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "data_source_configs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("provider_type", sa.String(length=32), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "data_sync_tasks",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("data_source_config_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["data_source_config_id"], ["data_source_configs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("data_sync_tasks")
    op.drop_table("data_source_configs")
