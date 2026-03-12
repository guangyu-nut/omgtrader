"""add python strategies table

Revision ID: 0006_add_python_strategies_table
Revises: 0005_add_ai_insights_table
Create Date: 2026-03-12 19:15:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0006_add_python_strategies_table"
down_revision = "0005_add_ai_insights_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "python_strategies",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("tags_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("parameter_schema_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    with op.batch_alter_table("python_strategies") as batch_op:
        batch_op.alter_column("description", server_default=None)
        batch_op.alter_column("tags_text", server_default=None)
        batch_op.alter_column("parameter_schema_text", server_default=None)


def downgrade() -> None:
    op.drop_table("python_strategies")
