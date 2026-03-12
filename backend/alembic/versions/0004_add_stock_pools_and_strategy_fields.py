"""add stock pools and strategy fields

Revision ID: 0004_add_stock_pools_and_strategy_fields
Revises: 0003_add_data_coverage_table
Create Date: 2026-03-12 15:50:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0004_add_stock_pools_and_strategy_fields"
down_revision = "0003_add_data_coverage_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stock_pools",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("input_mode", sa.String(length=32), nullable=False),
        sa.Column("symbols", sa.JSON(), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    with op.batch_alter_table("strategy_instances") as batch_op:
        batch_op.add_column(sa.Column("stock_pool_id", sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column("slippage_bps", sa.Float(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("commission_bps", sa.Float(), nullable=False, server_default="0"))
        batch_op.add_column(
            sa.Column("benchmark_symbol", sa.String(length=32), nullable=False, server_default="000300.SH")
        )

    bind = op.get_bind()
    legacy_strategies = bind.execute(
        sa.text("SELECT id, name, created_by_user_id, created_at FROM strategy_instances")
    ).mappings()
    legacy_stock_pools = [
        {
            "id": row["id"],
            "name": f"{row['name']} legacy pool",
            "input_mode": "manual",
            "symbols": [],
            "created_by_user_id": row["created_by_user_id"],
            "created_at": row["created_at"],
        }
        for row in legacy_strategies
    ]
    if legacy_stock_pools:
        stock_pools_table = sa.table(
            "stock_pools",
            sa.column("id", sa.String(length=36)),
            sa.column("name", sa.String(length=128)),
            sa.column("input_mode", sa.String(length=32)),
            sa.column("symbols", sa.JSON()),
            sa.column("created_by_user_id", sa.String(length=36)),
            sa.column("created_at", sa.DateTime()),
        )
        op.bulk_insert(stock_pools_table, legacy_stock_pools)
        op.execute("UPDATE strategy_instances SET stock_pool_id = id WHERE stock_pool_id IS NULL")

    with op.batch_alter_table("strategy_instances") as batch_op:
        batch_op.create_foreign_key(
            "fk_strategy_instances_stock_pool_id",
            "stock_pools",
            ["stock_pool_id"],
            ["id"],
        )
        batch_op.alter_column("stock_pool_id", nullable=False)
        batch_op.alter_column("slippage_bps", server_default=None)
        batch_op.alter_column("commission_bps", server_default=None)
        batch_op.alter_column("benchmark_symbol", server_default=None)


def downgrade() -> None:
    with op.batch_alter_table("strategy_instances") as batch_op:
        batch_op.drop_constraint("fk_strategy_instances_stock_pool_id", type_="foreignkey")
        batch_op.drop_column("benchmark_symbol")
        batch_op.drop_column("commission_bps")
        batch_op.drop_column("slippage_bps")
        batch_op.drop_column("stock_pool_id")
    op.drop_table("stock_pools")
