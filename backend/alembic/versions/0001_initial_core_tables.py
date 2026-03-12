"""initial core tables

Revision ID: 0001_initial_core_tables
Revises:
Create Date: 2026-03-12 15:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_core_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_table(
        "symbols",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("code", sa.String(length=16), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("market", sa.String(length=16), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "bar_daily",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("symbol_id", sa.String(length=36), nullable=False),
        sa.Column("trade_date", sa.Date(), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["symbol_id"], ["symbols.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol_id", "trade_date"),
    )
    op.create_table(
        "bar_minute",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("symbol_id", sa.String(length=36), nullable=False),
        sa.Column("bar_time", sa.DateTime(), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["symbol_id"], ["symbols.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol_id", "bar_time"),
    )
    op.create_table(
        "strategy_instances",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("template_type", sa.String(length=64), nullable=False),
        sa.Column("ranking_metric", sa.String(length=64), nullable=False),
        sa.Column("hold_count", sa.Integer(), nullable=False),
        sa.Column("rebalance_frequency", sa.String(length=32), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "backtest_jobs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("strategy_instance_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["strategy_instance_id"], ["strategy_instances.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "backtest_metrics",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("backtest_job_id", sa.String(length=36), nullable=False),
        sa.Column("total_return", sa.Float(), nullable=True),
        sa.Column("max_drawdown", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["backtest_job_id"], ["backtest_jobs.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("backtest_job_id"),
    )


def downgrade() -> None:
    op.drop_table("backtest_metrics")
    op.drop_table("backtest_jobs")
    op.drop_table("strategy_instances")
    op.drop_table("bar_minute")
    op.drop_table("bar_daily")
    op.drop_table("symbols")
    op.drop_table("sessions")
    op.drop_table("users")
