"""base migration

Revision ID: 61e0ca7c6e43
Revises: 
Create Date: 2023-06-06 20:48:19.140899

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "61e0ca7c6e43"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.Uuid(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
        sa.UniqueConstraint("external_id", name=op.f("user_external_id_key")),
    )
    op.create_index(op.f("user_id_idx"), "user", ["id"], unique=False)
    op.create_index(op.f("user_username_idx"), "user", ["username"], unique=True)


def downgrade():
    op.drop_index(op.f("user_username_idx"), table_name="user")
    op.drop_index(op.f("user_id_idx"), table_name="user")
    op.drop_table("user")
